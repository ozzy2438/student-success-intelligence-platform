"""Score current student-course-week snapshots using the trained transparent model."""

from __future__ import annotations

import json

import duckdb
import joblib
import numpy as np
import pandas as pd

from src.config import ARTIFACTS_DIR, DUCKDB_PATH, MODEL_VERSION


def risk_tier(probability: float) -> str:
    if probability >= 0.75:
        return "Critical"
    if probability >= 0.50:
        return "High"
    if probability >= 0.25:
        return "Moderate"
    return "Low"


def primary_driver(row: pd.Series) -> str:
    candidates = {
        "Missing assessment submission": row["missing_submission_count"] * 1.0,
        "Low attendance": max(0.0, 0.55 - row["attendance_rate"]) * 3.0,
        "Low LMS engagement": max(0.0, 0.35 - row["engagement_score"]) * 3.2,
        "Rapid engagement decline": max(0.0, -row["week_on_week_engagement_change"]) * 2.0,
        "Repeated late submissions": row["late_submission_count"] * 0.4,
        "Prior academic difficulty": row["prior_course_failures"] * 0.3,
    }
    return max(candidates, key=candidates.get)


def recommended_intervention(tier: str) -> str:
    return {
        "Critical": "Priority human review within 2 business days",
        "High": "Academic outreach within 5 business days",
        "Moderate": "Automated nudge and self-service support",
        "Low": "Continue monitoring",
    }[tier]


def main() -> None:
    model_path = ARTIFACTS_DIR / "risk_model.joblib"
    features_path = ARTIFACTS_DIR / "risk_model_features.json"
    metrics_path = ARTIFACTS_DIR / "risk_model_metrics.json"
    if not all(path.exists() for path in [model_path, features_path, metrics_path]):
        raise FileNotFoundError("Model artefacts missing. Run `python -m src.train_risk_model` first.")

    model = joblib.load(model_path)
    features = json.loads(features_path.read_text())
    threshold = json.loads(metrics_path.read_text())["operating_threshold"]

    connection = duckdb.connect(str(DUCKDB_PATH))
    query = """
        select
            r.student_key,
            r.course_id,
            r.term_id,
            r.week_number,
            r.engagement_score,
            r.attendance_rate,
            r.week_on_week_engagement_change,
            r.three_week_engagement_average,
            r.missing_submission_count,
            r.late_submission_count,
            r.assessment_average,
            r.prior_course_failures
        from intermediate.int_student_risk_features r
    """
    frame = connection.execute(query).fetchdf()
    frame["model_risk_probability"] = model.predict_proba(frame[features])[:, 1]
    frame["risk_tier"] = frame["model_risk_probability"].map(risk_tier)
    frame["primary_risk_driver"] = frame.apply(primary_driver, axis=1)
    frame["recommended_intervention"] = frame["risk_tier"].map(recommended_intervention)
    frame["priority_flag"] = (frame["model_risk_probability"] >= threshold).astype(int)
    frame["model_version"] = MODEL_VERSION
    frame["priority_rank"] = frame.groupby(["term_id", "week_number"])["model_risk_probability"].rank(method="dense", ascending=False).astype(int)

    connection.register("scored_frame", frame)
    connection.execute("CREATE SCHEMA IF NOT EXISTS scored")
    connection.execute("CREATE OR REPLACE TABLE scored.student_risk_scores AS SELECT * FROM scored_frame")
    connection.unregister("scored_frame")
    connection.close()

    print(f"Scored {len(frame):,} student-course-week snapshots")
    print(f"Capacity-aware priority threshold: {threshold:.3f}")
    print("Created DuckDB table: scored.student_risk_scores")


if __name__ == "__main__":
    main()
