"""Train an explainable logistic-regression model for adverse academic outcomes.

The model is deliberately transparent and intended for portfolio demonstration.
It must be treated as a decision-support signal, not an automated decision.
"""

from __future__ import annotations

import json

import duckdb
import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    classification_report,
    precision_recall_curve,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import ARTIFACTS_DIR, DUCKDB_PATH, MODEL_VERSION, REPORTS_DIR

FEATURES = [
    "engagement_score",
    "attendance_rate",
    "week_on_week_engagement_change",
    "three_week_engagement_average",
    "missing_submission_count",
    "late_submission_count",
    "assessment_average",
    "prior_course_failures",
    "week_number",
]


def choose_capacity_aware_threshold(y_true: pd.Series, probabilities: np.ndarray, target_precision: float = 0.55) -> float:
    precision, recall, thresholds = precision_recall_curve(y_true, probabilities)
    viable = np.where(precision[:-1] >= target_precision)[0]
    if len(viable) == 0:
        return 0.50
    best_index = viable[np.argmax(recall[viable])]
    return float(thresholds[best_index])


def main() -> None:
    if not DUCKDB_PATH.exists():
        raise FileNotFoundError("Warehouse missing. Run `python -m src.load_to_duckdb` and `dbt build` first.")

    query = """
        with latest_week as (
            select
                student_key,
                course_id,
                term_id,
                max(week_number) as max_week
            from analytics.fct_student_risk_snapshot
            group by 1, 2, 3
        )
        select
            r.student_key,
            r.course_id,
            r.term_id,
            r.week_number,
            r.engagement_score,
            r.attendance_rate,
            r.week_on_week_engagement_change,
            r.three_week_engagement_average,
            f.missing_submission_count,
            f.late_submission_count,
            f.assessment_average,
            f.prior_course_failures,
            o.adverse_outcome_flag as target_adverse_outcome
        from intermediate.int_student_risk_features r
        inner join latest_week l
            on r.student_key = l.student_key
            and r.course_id = l.course_id
            and r.term_id = l.term_id
            and r.week_number = l.max_week
        inner join intermediate.int_student_assessment_features f
            using (student_key, course_id, term_id)
        inner join analytics.fct_course_outcome o
            using (student_key, course_id, term_id)
    """
    connection = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    frame = connection.execute(query).fetchdf()
    connection.close()

    X = frame[FEATURES]
    y = frame["target_adverse_outcome"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=20260714, stratify=y
    )

    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    preprocessor = ColumnTransformer(transformers=[("numeric", numeric_transformer, FEATURES)])
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=20260714)),
        ]
    )
    pipeline.fit(X_train, y_train)
    probabilities = pipeline.predict_proba(X_test)[:, 1]
    threshold = choose_capacity_aware_threshold(y_test, probabilities)
    predictions = (probabilities >= threshold).astype(int)

    metrics = {
        "model_version": MODEL_VERSION,
        "training_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "positive_rate_test": round(float(y_test.mean()), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
        "average_precision": round(float(average_precision_score(y_test, probabilities)), 4),
        "brier_score": round(float(brier_score_loss(y_test, probabilities)), 4),
        "operating_threshold": round(float(threshold), 4),
        "classification_report": classification_report(y_test, predictions, output_dict=True),
    }

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, ARTIFACTS_DIR / "risk_model.joblib")
    (ARTIFACTS_DIR / "risk_model_features.json").write_text(json.dumps(FEATURES, indent=2))
    (ARTIFACTS_DIR / "risk_model_metrics.json").write_text(json.dumps(metrics, indent=2, default=float))

    probability_true, probability_pred = calibration_curve(y_test, probabilities, n_bins=10, strategy="quantile")
    calibration = pd.DataFrame({"mean_predicted_probability": probability_pred, "observed_positive_rate": probability_true})
    calibration.to_csv(REPORTS_DIR / "calibration_curve.csv", index=False)

    classifier = pipeline.named_steps["classifier"]
    coefficients = pd.DataFrame(
        {"feature": FEATURES, "coefficient": classifier.coef_[0], "odds_ratio": np.exp(classifier.coef_[0])}
    ).sort_values("coefficient", ascending=False)
    coefficients.to_csv(REPORTS_DIR / "risk_model_coefficients.csv", index=False)

    print("Risk model trained successfully")
    print(json.dumps({key: value for key, value in metrics.items() if key != "classification_report"}, indent=2))
    print(f"Saved model artefacts → {ARTIFACTS_DIR}")


if __name__ == "__main__":
    main()
