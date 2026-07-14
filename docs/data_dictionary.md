# Data Dictionary

All assets in this portfolio project are fully synthetic. `student_key` is a non-reversible synthetic identifier, not a real student identifier.

## Core entities

| Asset | Grain | Key fields | Purpose |
|---|---|---|---|
| `dim_student` | One record per synthetic student | `student_key` | De-identified cohort segmentation |
| `dim_program` | One record per programme | `program_id` | Faculty, school and programme context |
| `dim_course` | One record per course | `course_id` | Course and assessment context |
| `dim_term` | One record per teaching term | `term_id` | Time context |
| `dim_week` | One record per term-week | `week_key` | Teaching-period analysis |
| `fct_student_weekly_engagement` | Student-course-term-week | student, course, term, week | Engagement and attendance trend analysis |
| `fct_assessment_submission` | Student-assessment | `submission_id` | Submission, lateness and score analysis |
| `fct_course_outcome` | Student-course-term | student, course, term | Outcome and adverse-outcome label |
| `fct_support_intervention` | Intervention event | `intervention_id` | Support operations and outcome tracking |
| `fct_student_risk_snapshot` | Student-course-term-week | student, course, term, week | Explainable risk prioritisation |

## Selected fields

| Field | Definition | Classification | Quality rule |
|---|---|---|---|
| `student_key` | Synthetic pseudonymous identifier | Restricted | Not null; no direct identifiers |
| `engagement_score` | Composite score from LMS activity and attendance | Restricted | Range 0–1 |
| `attendance_rate` | Weekly attendance proportion | Restricted | Range 0–1 |
| `missing_submission_count` | Count of assessment items not submitted | Restricted | Integer >= 0 |
| `late_submission_count` | Count of submitted items with lateness > 0 | Restricted | Integer >= 0 |
| `assessment_average` | Mean score across submitted assessments | Restricted | Range 0–100 where present |
| `model_risk_probability` | Model-estimated probability of adverse course outcome | Restricted decision support | Range 0–1; human review required |
| `risk_tier` | Operational grouping of model probability | Restricted decision support | Low, Moderate, High or Critical |
| `primary_risk_driver` | Dominant explainable feature contributing to priority | Restricted decision support | Must be populated |
| `recommended_intervention` | Support-oriented next action | Restricted decision support | Never an adverse decision |
