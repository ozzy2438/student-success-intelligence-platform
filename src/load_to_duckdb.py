"""Load synthetic source-system CSV files into a local DuckDB warehouse."""

from __future__ import annotations

import duckdb

from src.config import DUCKDB_PATH, SYNTHETIC_DIR

TABLES = {
    "raw_students": "students.csv",
    "raw_programs": "programs.csv",
    "raw_courses": "courses.csv",
    "raw_terms": "terms.csv",
    "raw_term_weeks": "term_weeks.csv",
    "raw_enrolments": "enrolments.csv",
    "raw_assessments": "assessments.csv",
    "raw_lms_activity": "lms_activity.csv",
    "raw_attendance": "attendance.csv",
    "raw_submissions": "submissions.csv",
    "raw_course_outcomes": "course_outcomes.csv",
    "raw_interventions": "interventions.csv",
}


def main() -> None:
    missing = [filename for filename in TABLES.values() if not (SYNTHETIC_DIR / filename).exists()]
    if missing:
        joined = ", ".join(missing)
        raise FileNotFoundError(
            f"Missing source files: {joined}. Run `python -m src.generate_synthetic_data` first."
        )

    connection = duckdb.connect(str(DUCKDB_PATH))
    try:
        connection.execute("CREATE SCHEMA IF NOT EXISTS raw")
        for table_name, filename in TABLES.items():
            csv_path = (SYNTHETIC_DIR / filename).as_posix()
            relation_name = f"raw.{table_name.removeprefix('raw_')}"
            connection.execute(
                f"CREATE OR REPLACE TABLE {relation_name} AS "
                f"SELECT * FROM read_csv_auto('{csv_path}', header=true)"
            )
            row_count = connection.execute(f"SELECT COUNT(*) FROM {relation_name}").fetchone()[0]
            print(f"Loaded {row_count:>7,} rows → {relation_name}")

        connection.execute("CREATE OR REPLACE VIEW raw.source_inventory AS SELECT table_name FROM information_schema.tables WHERE table_schema = 'raw'")
        print(f"\nDuckDB warehouse ready: {DUCKDB_PATH}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
