# Student Success Intelligence Platform

> **Portfolio case study:** an enterprise-style, privacy-preserving learning-analytics platform for early academic-risk detection, intervention prioritisation and governed decision support.

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/Warehouse-DuckDB-FFF000?logo=duckdb&logoColor=black)](https://duckdb.org/)
[![dbt](https://img.shields.io/badge/Transform-dbt-FF694B?logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![BI](https://img.shields.io/badge/BI-Power%20BI-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)

## Portfolio outcome

This repository demonstrates how a Data Analyst can convert fragmented higher-education signals into a **trusted, explainable and operationally useful decision-support product**. It is deliberately designed as an enterprise analytics delivery, not as a standalone machine-learning demo.

The project was designed for a higher-education environment where decision-makers need timely visibility of student engagement and academic-risk patterns, while protecting privacy, documenting quality and preserving human judgement.

## Business questions

1. Which student cohorts may benefit from timely academic support?
2. Which engagement, attendance and assessment signals are associated with academic risk?
3. Which courses and teaching weeks warrant proactive outreach?
4. Are interventions reaching the intended population and improving downstream engagement?
5. Can the workflow be governed through documented lineage, quality controls, privacy safeguards and human oversight?

## Scope and responsible-use statement

- All source data are **synthetic** and are generated locally by `src/generate_synthetic_data.py`
- The repository contains **no real student data, institutional records or direct identifiers**
- Risk outputs are **decision-support signals**, never automated decisions
- The platform must not be used to penalise, exclude, discipline or make high-impact decisions about a student
- Any operational deployment requires approved data governance, privacy impact assessment, role-based access control, ongoing validation and trained human review

RMIT’s public learning-analytics principles emphasise ethical and transparent use, student-centred practice, inclusive participation and the principle that students must not be wholly defined by their visible data or its interpretation [RMIT Learning Analytics](https://www.rmit.edu.au/about/governance-management/rmit-structure/education/learning-analytics)

The Australian Office of the Australian Information Commissioner recommends evaluating whether personal information is necessary for an analytics activity and using de-identified data where possible [OAIC analytics guidance](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/more-guidance/guide-to-data-analytics-and-the-australian-privacy-principles)

## Architecture

```text
Synthetic source systems
(SIS, LMS, assessment, attendance, support interactions)
                        │
                        ▼
              DuckDB analytical warehouse
                        │
                        ▼
          dbt sources → staging → marts
                        │
       ┌────────────────┼───────────────────┐
       ▼                ▼                   ▼
Data tests       Python statistics     Risk scoring
& lineage        and validation        and monitoring
       │                │                   │
       └────────────────┴───────────────────┘
                        │
                        ▼
           Power BI-ready curated exports
```

## Technology stack

| Capability | Technology |
|---|---|
| Synthetic data generation | Python, pandas, NumPy, Faker |
| Analytical warehouse | DuckDB |
| Transformation and testing | dbt Core with dbt-duckdb |
| Statistical analysis | SciPy, statsmodels |
| Explainable risk scoring | scikit-learn logistic regression |
| Quality assurance | dbt data tests, Pandera, pytest |
| Business intelligence | Power BI and DAX |
| Reproducibility | Git, GitHub, Makefile |

## Repository map

```text
src/                  Python pipeline modules
dbt_project/          dbt models, source declarations and tests
data/synthetic/       generated source-system CSV files
data/exports/         Power BI-ready curated CSV files
data/warehouse/       generated local DuckDB database, ignored by Git
docs/                 business, governance, privacy and model documentation
powerbi/              DAX catalogue and dashboard build instructions
notebooks/            reproducible analysis notebooks
tests/                Python tests
```

## macOS quick start

### 1. Clone the repository

```bash
git clone https://github.com/ozzy2438/student-success-intelligence-platform.git
cd student-success-intelligence-platform
```

### 2. Create and activate an isolated Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Generate sources and load the warehouse

```bash
python -m src.generate_synthetic_data
python -m src.load_to_duckdb
```

### 4. Transform, test and document with dbt

```bash
mkdir -p ~/.dbt
cp dbt_project/profiles.yml.example ~/.dbt/profiles.yml
cd dbt_project
dbt deps
dbt build
dbt docs generate
cd ..
```

### 5. Train the transparent risk model and create curated exports

```bash
python -m src.train_risk_model
python -m src.score_students
python -m src.export_for_powerbi
```

### 6. Open the Power BI dashboard

Follow [Power BI build instructions](powerbi/README.md), point Power BI Desktop to the files in `data/exports/`, create the documented relationships, then paste the measures in [DAX catalogue](powerbi/dax_measures.md)

## Data model

### Core dimensions

- `dim_student` — de-identified student cohort attributes
- `dim_program` — faculty, school, programme and level
- `dim_course` — course metadata and assessment intensity
- `dim_term` — academic term
- `dim_week` — teaching week

### Core facts

- `fct_student_weekly_engagement`
- `fct_assessment_submission`
- `fct_course_outcome`
- `fct_support_intervention`
- `fct_student_risk_snapshot`

## Operational KPIs

- Active students
- High and critical risk students
- At-risk rate
- Weekly risk movement
- LMS engagement trend
- On-time submission rate
- Withdrawal rate
- Intervention coverage and response rate
- Data-quality score
- Model calibration and cohort monitoring

## Delivery sequence

```bash
make install
make generate
make warehouse
make transform
make model
make export
make test
```

The equivalent commands remain available individually if you prefer to inspect each step.

## Project documentation

- [Business case](docs/business_case.md)
- [Stakeholder map](docs/stakeholder_map.md)
- [Data dictionary](docs/data_dictionary.md)
- [Data lineage](docs/data_lineage.md)
- [Data-quality framework](docs/data_quality_framework.md)
- [Governance framework](docs/governance_framework.md)
- [Privacy and ethics](docs/privacy_and_ethics.md)
- [Model card](docs/model_card.md)
- [Implementation roadmap](docs/implementation_roadmap.md)
- [Power BI dashboard design](docs/dashboard_design.md)

## What this demonstrates in a Data Analyst application

- SQL-based data modelling and transformation
- Data quality checks, semantic definitions and documentation
- Python-based statistical analysis and explainable predictive modelling
- Power BI and DAX dashboard design for executives, faculty and operational teams
- Translation of analytical findings into intervention recommendations
- Privacy-by-design, data governance and responsible analytics thinking
- Reproducible project delivery through Git, dbt, tests and documented runbooks

## Status

- [x] Project architecture and documentation
- [x] Synthetic source-data generator
- [x] DuckDB loading pipeline
- [x] dbt dimensional transformation layer and tests
- [x] Explainable risk-model workflow
- [x] Power BI exports, relationship design and DAX catalogue
- [ ] Power BI `.pbix` visual assembly and screenshot upload — complete locally in Power BI Desktop
- [ ] Optional 90-second walkthrough video
