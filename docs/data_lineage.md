# Data Lineage

```text
Synthetic source CSV files
  ├── students.csv
  ├── programs.csv
  ├── courses.csv
  ├── terms.csv and term_weeks.csv
  ├── enrolments.csv
  ├── lms_activity.csv
  ├── attendance.csv
  ├── assessments.csv and submissions.csv
  ├── course_outcomes.csv
  └── interventions.csv
          │
          ▼
DuckDB raw schema
          │
          ▼
dbt staging models
          │
          ├── stg_students, stg_programs, stg_courses
          ├── stg_enrolments, stg_lms_activity, stg_attendance
          ├── stg_assessments, stg_submissions
          ├── stg_course_outcomes, stg_interventions
          ▼
dbt intermediate models
          ├── int_student_weekly_engagement
          ├── int_student_assessment_features
          ├── int_student_risk_features
          └── int_intervention_outcomes
          ▼
dbt marts
          ├── dimensions
          └── facts
                  │
                  ▼
Python logistic-regression artefacts and scored.student_risk_scores
                  │
                  ▼
Power BI CSV exports and governed dashboard semantic model
```

## Lineage controls

- Every source-to-mart transformation is version controlled in dbt SQL
- dbt source/model tests validate key structural assumptions
- Python training and scoring scripts are deterministic through a fixed random seed
- Model version is embedded in each scored record
- Power BI consumes curated exports rather than raw source files
