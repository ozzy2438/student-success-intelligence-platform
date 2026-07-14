# Data Governance Framework

## Governance objective

Ensure the platform produces trusted, comprehensible and appropriately controlled decision-support information.

## Data classifications

| Data class | Examples | Portfolio handling | Real deployment handling |
|---|---|---|---|
| Public | Aggregated methodology | Documented in GitHub | Public where approved |
| Internal | Course metadata, generic KPI definitions | Included | Controlled internal access |
| Restricted | De-identified engagement and assessment records | Synthetic only | Role-based access and audit logs |
| Highly restricted | Direct identifiers, wellbeing case notes | Not generated | Separate controlled systems; minimum necessary access |
| Restricted decision-support | Risk score, outreach priority | Synthetic only | Human review, limited audience, monitoring |

## Ownership and stewardship

| Asset | Accountable owner | Data steward | Typical quality responsibility |
|---|---|---|---|
| Student enrolment | Student administration | SIS data steward | Completeness, valid enrollment status |
| LMS activity | Learning systems | LMS data steward | Timeliness, valid activity measures |
| Assessments | Academic services | Assessment data steward | Submission and score validity |
| Interventions | Student support | Support-services data steward | Appropriate case recording |
| Curated marts | Data & Analytics | Analytics engineer / analyst | Transformation logic, metric definitions |

## Quality dimensions

- Completeness
- Validity
- Uniqueness
- Consistency
- Timeliness
- Referential integrity

## Core controls

| Control | Example implementation |
|---|---|
| Source freshness | dbt source freshness / generated-at audit column |
| Key uniqueness | `student_key + course_id + term_id + week_number` uniqueness test |
| Accepted values | Risk tiers and outcome statuses constrained to approved values |
| Referential integrity | Facts must resolve to valid dimensions |
| Score validity | Risk probability must be in `[0, 1]` |
| Documentation | dbt model descriptions, data dictionary and lineage |
| Change management | Git pull requests, semantic versioning for model logic |

## Data-quality incident workflow

```text
Failed test → triage severity → identify source/transformation owner → remediate → rerun tests → document resolution
```

## Metric governance

Every executive KPI must have:

- Business definition
- Calculation logic
- Grain
- Source tables
- Refresh cadence
- Accountable owner
- Known limitations
