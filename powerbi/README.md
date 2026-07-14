# Power BI Build Guide

## Data source

After running the pipeline, connect Power BI Desktop to the curated CSV files in `data/exports/` or directly to the DuckDB marts using an approved DuckDB connector.

For the portfolio version, CSV exports are the simplest and most reproducible approach.

## Recommended tables

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

## Relationships

| From | To | Cardinality | Filter direction |
|---|---|---:|---|
| dim_student[student_key] | all fact tables[student_key] | 1:* | Single |
| dim_course[course_id] | course-related facts[course_id] | 1:* | Single |
| dim_program[program_id] | dim_student[program_id] | 1:* | Single |
| dim_term[term_id] | all term-based facts[term_id] | 1:* | Single |
| dim_week[week_number] | weekly engagement and risk facts[week_number] | 1:* | Single |

## Dashboard pages

1. **Executive Overview** — risk rate, risk trend, intervention coverage, withdrawal and data-quality KPIs
2. **Risk & Cohort Explorer** — faculty/program/course drill-down, engagement trends and cohort distribution
3. **Intervention Operations** — restricted queue, SLA, recommended action and capacity metrics
4. **Course & Assessment Insights** — on-time submission, late submission, assessment results and engagement patterns
5. **Governance & Responsible Analytics** — freshness, completeness, quality tests, model version and use guardrails

## Portfolio rule

Use only anonymised `student_key` values in screenshots. Never show names, emails or real institutional data.
