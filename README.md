# Student Success Intelligence Platform

> **Portfolio case study:** an enterprise-style, privacy-preserving learning analytics platform for early academic-risk detection, intervention prioritisation and governed decision support.

## Why this project exists

Higher-education institutions often hold student, learning-management-system, assessment and support-service data in separate systems. This project demonstrates how an analyst can transform those signals into a trusted, explainable and operationally useful decision-support product.

The platform is designed to answer:

1. Which student cohorts may benefit from timely academic support?
2. What behavioural and assessment signals are associated with risk?
3. Which courses and weeks require proactive intervention?
4. Are interventions reaching the intended population and improving engagement?
5. Can this be done with data quality, privacy, transparency and human oversight built in?

## Important scope and ethical statement

- This repository uses **fully synthetic data** generated for portfolio and demonstration purposes.
- It contains **no real student data, direct identifiers or institutional records**.
- Risk outputs are **decision-support signals**, not automated decisions. They must never be used to penalise, exclude, discipline or make high-impact decisions about a student.
- The intended operational model is **human-in-the-loop**: trained student-support professionals review context before acting.

This framing aligns with RMIT's published learning-analytics principles, including ethical use, transparency, student-centred practice and the principle that students must not be wholly defined by visible data or its interpretation. See [RMIT Learning Analytics](https://www.rmit.edu.au/about/governance-management/rmit-structure/education/learning-analytics).

## Architecture

```text
Synthetic SIS / LMS / assessment / attendance / intervention data
                    │
                    ▼
        DuckDB analytical warehouse
                    │
                    ▼
     dbt staging → intermediate → marts
                    │
                    ├── dbt tests and data-quality controls
                    ├── Python statistical analysis
                    ├── Explainable risk scoring
                    └── Power BI-ready curated exports
```

## Technology stack

| Area | Technology |
|---|---|
| Data generation | Python, pandas, NumPy, Faker |
| Analytics warehouse | DuckDB |
| Transformations and tests | dbt Core with dbt-duckdb |
| Statistical analysis | SciPy, statsmodels |
| Risk scoring | scikit-learn logistic regression |
| Quality checks | dbt tests, Pandera, pytest |
| Business intelligence | Power BI + DAX |
| Documentation | Markdown, dbt docs |

## Repository map

```text
src/                 Python pipeline modules
dbt_project/         dbt transformations, tests and warehouse models
data/synthetic/      generated source data
data/exports/        Power BI-ready curated exports
docs/                business, governance, privacy and model documentation
powerbi/             DAX catalogue and dashboard build instructions
notebooks/           reproducible exploratory/statistical analysis
r_analysis/          optional R validation analysis
tests/               Python tests
```

## Quick start — macOS

### 1. Clone and enter the repository

```bash
git clone https://github.com/ozzy2438/student-success-intelligence-platform.git
cd student-success-intelligence-platform
```

### 2. Create a Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Generate synthetic source data and load DuckDB

```bash
python -m src.generate_synthetic_data
python -m src.load_to_duckdb
```

### 4. Configure dbt

```bash
mkdir -p ~/.dbt
cp dbt_project/profiles.yml.example ~/.dbt/profiles.yml
cd dbt_project
dbt deps
dbt build
cd ..
```

### 5. Create risk scores and Power BI exports

```bash
python -m src.train_risk_model
python -m src.score_students
python -m src.export_for_powerbi
```

## Data model

### Dimensions

- `dim_student` — de-identified student attributes and cohort fields
- `dim_program` — faculty, school, program and level
- `dim_course` — course metadata
- `dim_term` — teaching term
- `dim_week` — teaching week

### Facts

- `fct_student_weekly_engagement`
- `fct_assessment_submission`
- `fct_course_outcome`
- `fct_support_intervention`
- `fct_student_risk_snapshot`

## Core operational KPIs

- Active students
- High and critical risk students
- At-risk rate
- Weekly risk movement
- LMS engagement trend
- On-time submission rate
- Withdrawal rate
- Intervention coverage
- Intervention response rate
- Data-quality score
- Model calibration and cohort monitoring

## Governance approach

The project uses data minimisation, pseudonymous student keys, defined data classifications, quality checks, documented lineage, role-based access concepts, model documentation and human review requirements. The Australian Office of the Australian Information Commissioner recommends considering whether personal information is required for analytics and using de-identified data where possible [OAIC guidance](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/more-guidance/guide-to-data-analytics-and-the-australian-privacy-principles).

## Delivery status

- [x] Repository foundation
- [x] Synthetic source-data generator
- [x] DuckDB loading layer
- [x] Initial dbt model structure
- [x] Governance and privacy documentation
- [ ] Statistical analysis notebooks
- [ ] Explainable risk model and calibration report
- [ ] Power BI dashboard build and screenshots
- [ ] Executive decision brief

## Portfolio positioning

This project is intentionally framed as an enterprise analytics delivery rather than a standalone machine-learning exercise. It demonstrates SQL, Python, data visualisation, statistics, data-quality controls, governance, stakeholder thinking and communication of actionable insights.
