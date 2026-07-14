# Governance Framework

## Purpose limitation

The platform exists only to support beneficial, proportionate and human-reviewed student-success interventions. It is not designed for surveillance, disciplinary action, automated exclusion or any adverse high-impact decision.

## Governance principles

1. **Student benefit first** — insights must plausibly support learning, access or appropriate support
2. **Data minimisation** — use the least data necessary for the stated decision
3. **De-identification by default** — use pseudonymous keys and aggregate reporting wherever possible
4. **Transparency** — document collection, analysis, interpretation, limitations and responsible use
5. **Human oversight** — staff review context before outreach or action
6. **Equity monitoring** — assess whether performance or operational consequences differ across cohorts
7. **Quality before publication** — do not publish untested data products
8. **Accountability** — nominate data owners, stewards, model owners and dashboard owners

## Role-based access concept

| Role | Aggregate dashboards | Student-level queue | Direct identifiers | Model artefacts |
|---|---:|---:|---:|---:|
| Executive | Yes | No | No | Summary only |
| Faculty leader | Faculty scope | No | No | Summary only |
| Student-support adviser | Limited operational scope | Assigned cases only | Approved operational system only | Reason codes only |
| Data analyst | De-identified | De-identified | No | Yes |
| Data engineer | Pipeline minimum | No | Restricted only when justified | No |
| Privacy / governance | Audit scope | Controlled | Controlled | Yes |

## Required controls before real deployment

- Privacy Impact Assessment
- Approved data-sharing and retention arrangements
- Student-facing transparency notice and engagement plan
- Access-control design and audit logging
- Human-review workflow and escalation pathway
- Model validation across terms and cohorts
- Regular data-quality, drift and unintended-impact monitoring
