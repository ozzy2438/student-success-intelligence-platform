# Privacy, Ethics and Responsible Learning Analytics

## Purpose

This document defines responsible-use guardrails for the Student Success Intelligence Platform portfolio prototype.

## Data status

All data in this repository are synthetically generated. No real students, staff, course records, institutional systems or personally identifiable information are included.

## Design principles

1. **Student benefit:** Use analytics to improve access to timely support, not to punish or exclude.
2. **Data minimisation:** Use only variables necessary for a defined analytical purpose.
3. **De-identification:** Use a pseudonymous `student_key`; names, email addresses, phone numbers and addresses are not generated or retained.
4. **Transparency:** Document purpose, inputs, risk signals, limitations and governance controls.
5. **Human oversight:** A qualified person reviews any recommended action before contact or intervention.
6. **Equity monitoring:** Monitor aggregate performance and potential error differences across permitted cohort views.
7. **Security and access control:** Restrict operational views according to the minimum-access principle.
8. **No automated adverse decisions:** Scores are not eligibility, disciplinary, progression or exclusion decisions.

## Australian privacy framing

The Australian Privacy Principles govern the collection, use, disclosure, governance, integrity and access/correction of personal information [OAIC APP overview](https://www.oaic.gov.au/privacy/australian-privacy-principles). The OAIC's analytics guidance recommends considering whether analytics requires personal information and using de-identified data where possible [OAIC analytics guidance](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/more-guidance/guide-to-data-analytics-and-the-australian-privacy-principles).

## RMIT-aligned learning-analytics considerations

RMIT publishes principles that frame learning analytics as ethical and student-centred, require transparency, caution against defining students solely through visible data, and encourage students as active agents in learning analytics [RMIT Learning Analytics](https://www.rmit.edu.au/about/governance-management/rmit-structure/education/learning-analytics).

## Prohibited uses

- Automatic academic penalties or sanctions
- Admissions, exclusion, scholarship or visa decisions
- Inferring sensitive personal attributes
- Ranking student worth or potential
- Sharing identifiable student-level data outside authorised roles
- Using the score without checking source quality, context and recency

## Required human-review workflow

```text
Risk signal generated
        ↓
Data-quality and recency checks pass
        ↓
Authorised adviser reviews contextual information
        ↓
Supportive and proportionate outreach is considered
        ↓
Interaction and outcome are recorded for aggregate evaluation
```

## Minimum controls for a real deployment

- Privacy Impact Assessment before implementation
- Approved purpose statement and student-facing transparency notice
- Named data owners and data stewards
- Role-based access control and audit logging
- Secure storage, encryption and retention schedule
- Regular model performance, calibration and equity monitoring
- Formal incident escalation process
- Periodic review with student representation
