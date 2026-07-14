# Model Card — Student Risk Logistic Regression v1.0.0

## Model purpose

Estimate the likelihood that a synthetic student-course enrolment will have an adverse course outcome, defined as `Fail` or `Withdrawn`. The output supports prioritisation for **human review** and supportive outreach.

## Intended use

- Aggregate risk monitoring
- Identifying potential support demand
- Prioritising a human-reviewed intervention queue
- Understanding broad patterns in engagement, attendance and assessment behaviour

## Prohibited use

- Automated adverse decisions
- Exclusion, disciplinary action, penalties or academic judgement
- Diagnosing health, disability, wellbeing or personal circumstances
- Inferring motivation, potential or character
- Use without approved governance and privacy controls

## Features

- Engagement score
- Attendance rate
- Week-on-week engagement change
- Three-week engagement average
- Missing submission count
- Late submission count
- Assessment average
- Prior course failure count
- Teaching week

`equity_group` is not a model feature. It may only be used in aggregate monitoring under appropriate governance.

## Model approach

- Binary logistic regression
- Median imputation and standardisation in an sklearn pipeline
- Stratified train/test split
- Class weighting to address outcome imbalance
- Capacity-aware operating threshold selected from the precision-recall trade-off

## Performance outputs

The training script writes the following reproducible artefacts:

- `artifacts/risk_model.joblib`
- `artifacts/risk_model_features.json`
- `artifacts/risk_model_metrics.json`
- `reports/generated/calibration_curve.csv`
- `reports/generated/risk_model_coefficients.csv`

## Limitations

- Synthetic data cannot demonstrate real-world validity
- Observational relationships do not establish causality
- Engagement signals can have multiple benign explanations
- Model performance may vary by term, programme, delivery mode and cohort
- Intervention effects require controlled evaluation before causal claims

## Monitoring requirements for a real deployment

- Monitor ROC-AUC, PR-AUC, calibration and operational precision/recall each term
- Monitor missing data, data drift and schema changes
- Review false-positive and false-negative patterns by relevant cohorts
- Revalidate after material changes to systems, policies or learning design
- Maintain a documented human override and incident process
