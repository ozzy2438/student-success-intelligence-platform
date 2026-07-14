# Privacy and Ethics

## Portfolio design

This repository uses locally generated synthetic data. It intentionally excludes names, emails, phone numbers, addresses, real student identifiers and institutional records.

## Privacy-by-design choices

- Direct identifiers are not generated
- `student_key` is synthetic and non-reversible
- Only decision-relevant attributes are included
- Equity-related fields are used only for aggregate monitoring demonstrations, not as risk-model features
- Power BI exports are curated analytics tables rather than raw operational extracts
- Risk outputs carry a human-review requirement

## Ethical safeguards

| Risk | Safeguard |
|---|---|
| Students being reduced to a score | Explanatory drivers, contextual review and prohibition on automated decisions |
| Stigmatising outreach | Support-first intervention language and trained adviser review |
| Proxy discrimination | Exclude equity group from model training; monitor aggregate outcomes |
| Excessive data use | Purpose limitation and data-minimisation standard |
| Incorrect signals | dbt quality tests, model performance checks and feedback loop |
| Mission creep | Documented non-goals and governance approval for any new use case |

## Relevant Australian context

The Australian Privacy Principles cover governance and accountability, collection, use, disclosure, integrity, correction and access in relation to personal information [OAIC Australian Privacy Principles](https://www.oaic.gov.au/privacy/australian-privacy-principles)

The OAIC advises organisations conducting analytics to assess whether personal information is needed and to use de-identified data where possible [OAIC guide to data analytics](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/more-guidance/guide-to-data-analytics-and-the-australian-privacy-principles)

RMIT’s published learning-analytics principles include ethical use, transparent handling of student data, student-centred practice, inclusive participation and meaningful student engagement [RMIT Learning Analytics](https://www.rmit.edu.au/about/governance-management/rmit-structure/education/learning-analytics)
