# Power BI Build Guide

## 1. Import curated tables

In **Get data → Text/CSV**, import all CSV files from `data/exports/`:

- `dim_student.csv`
- `dim_program.csv`
- `dim_course.csv`
- `dim_term.csv`
- `dim_week.csv`
- `fct_student_weekly_engagement.csv`
- `fct_assessment_submission.csv`
- `fct_course_outcome.csv`
- `fct_support_intervention.csv`
- `fct_student_risk_snapshot.csv`
- `data_quality_summary.csv`

Use **Import** mode for this portfolio build.

## 2. Create relationships

| From | Cardinality | To | Cross-filter |
|---|---|---|---|
| `dim_student[student_key]` | 1:* | all facts on `student_key` | Single |
| `dim_course[course_id]` | 1:* | engagement, submissions, outcomes, risk | Single |
| `dim_term[term_id]` | 1:* | all facts on `term_id` | Single |
| `dim_program[program_id]` | 1:* | `dim_student[program_id]` | Single |
| `dim_week[term_id, week_number]` | logical composite | weekly engagement and risk | Use a calculated `term_week_key` if preferred |

### Recommended calculated key

Create this calculated column in both weekly fact tables and `dim_week`:

```DAX
Term Week Key = [term_id] & "-W" & FORMAT([week_number], "00")
```

Then relate `dim_week[Term Week Key]` one-to-many to the corresponding fact key.

## 3. Create measures

Copy the full measure catalogue from [dax_measures.md](dax_measures.md). Create a dedicated table named `Measures` in Power BI to store them.

## 4. Build dashboard pages

Follow the exact visual, KPI and audience design in [docs/dashboard_design.md](../docs/dashboard_design.md).

## 5. Responsible-use banner

Add this text to the top of the Intervention Operations page:

> **Synthetic demonstration only. Risk scores are decision-support signals requiring human review. Do not use them for automated or adverse student decisions.**

## 6. Portfolio screenshots

Export one screenshot per page as PNG after visual assembly. Save them in `powerbi/screenshots/` and link them from the main README.
