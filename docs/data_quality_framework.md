# Data-Quality Framework

## Quality dimensions

| Dimension | Control | Implementation |
|---|---|---|
| Completeness | Required keys and metrics should be populated | dbt `not_null` tests and summary export |
| Uniqueness | Fact grain should not contain duplicates | `assert_no_duplicate_student_week.sql` |
| Validity | Scores and rates must remain within allowed ranges | custom dbt range tests |
| Referential integrity | Facts must resolve to dimensions | dbt `relationships` tests |
| Consistency | Controlled categorical values should be standardised | dbt `accepted_values` tests |
| Freshness | Operational data should be refreshed within agreed SLA | production design requirement and dashboard status card |

## Critical controls

1. A student-week fact record must be unique at `student_key`, `course_id`, `term_id`, `week_number`
2. `engagement_score`, `attendance_rate` and model probability must remain within 0–1
3. Course outcome must be `Pass`, `Fail` or `Withdrawn`
4. Risk tier must be `Low`, `Moderate`, `High` or `Critical`
5. Student keys, programme keys and course keys must resolve across the star schema
6. Failures must stop publication of a production data product until triaged

## Incident workflow

1. Detect failed test or abnormal metric
2. Identify source, affected period and downstream dashboards
3. Quarantine or label affected output as unavailable
4. Notify data owner and dashboard owner
5. Correct source or transformation issue
6. Re-run pipeline, validate results and document resolution
