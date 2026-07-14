"""Export governed, Power BI-ready tables from DuckDB."""

from __future__ import annotations

import duckdb

from src.config import DUCKDB_PATH, EXPORT_DIR

EXPORT_QUERIES = {
    "dim_student.csv": "select * from analytics.dim_student",
    "dim_program.csv": "select * from analytics.dim_program",
    "dim_course.csv": "select * from analytics.dim_course",
    "dim_term.csv": "select * from analytics.dim_term",
    "dim_week.csv": "select * from analytics.dim_week",
    "fct_student_weekly_engagement.csv": "select * from analytics.fct_student_weekly_engagement",
    "fct_assessment_submission.csv": "select * from analytics.fct_assessment_submission",
    "fct_course_outcome.csv": "select * from analytics.fct_course_outcome",
    "fct_support_intervention.csv": "select * from analytics.fct_support_intervention",
    "fct_student_risk_snapshot.csv": "select * from scored.student_risk_scores",
    "data_quality_summary.csv": """
        select 'Student weekly engagement' as data_asset, count(*) as record_count,
               avg(case when engagement_score between 0 and 1 then 1.0 else 0.0 end) as validity_score,
               avg(case when attendance_rate between 0 and 1 then 1.0 else 0.0 end) as completeness_score,
               1.0 as freshness_score
        from analytics.fct_student_weekly_engagement
        union all
        select 'Risk snapshots' as data_asset, count(*) as record_count,
               avg(case when model_risk_probability between 0 and 1 then 1.0 else 0.0 end) as validity_score,
               avg(case when primary_risk_driver is not null then 1.0 else 0.0 end) as completeness_score,
               1.0 as freshness_score
        from scored.student_risk_scores
        union all
        select 'Assessment submissions' as data_asset, count(*) as record_count,
               avg(case when score between 0 and 100 then 1.0 else 0.0 end) as validity_score,
               avg(case when submission_id is not null then 1.0 else 0.0 end) as completeness_score,
               1.0 as freshness_score
        from analytics.fct_assessment_submission
    """,
}


def main() -> None:
    if not DUCKDB_PATH.exists():
        raise FileNotFoundError("Warehouse missing. Run generation, loading, dbt and scoring steps first.")

    connection = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    try:
        for filename, query in EXPORT_QUERIES.items():
            output_path = EXPORT_DIR / filename
            frame = connection.execute(query).fetchdf()
            if filename == "data_quality_summary.csv":
                frame["quality_score"] = frame[["validity_score", "completeness_score", "freshness_score"]].mean(axis=1)
            frame.to_csv(output_path, index=False)
            print(f"Exported {len(frame):>7,} rows → {output_path.relative_to(EXPORT_DIR.parent.parent)}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
