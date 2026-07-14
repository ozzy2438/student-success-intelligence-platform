# Student Success Intelligence Platform — Business Case

## Problem statement

Student outcomes can be affected by an accumulation of signals across learning engagement, assessment behaviour, attendance and access to support. When these signals are fragmented across operational systems, student-support teams may discover a problem too late or lack a consistent, governed way to prioritise outreach.

## Proposed capability

The Student Success Intelligence Platform creates a governed analytics layer that integrates de-identified, synthetic examples of student information system, LMS, assessment, attendance and intervention data. It produces cohort-level insight and a human-reviewed prioritisation queue.

## Decisions enabled

1. Which courses, programs and weeks show an emerging concentration of academic risk?
2. Which students should be reviewed for proactive support this week?
3. Which risk signals are most prevalent in the selected cohort?
4. Is support capacity aligned to the size and severity of the queue?
5. Are intervention patterns associated with later engagement improvement?

## Stakeholders

| Stakeholder | Decision / need | Product output |
|---|---|---|
| Executive leadership | Monitor strategic student-success outcomes | Executive dashboard, KPI trends |
| Faculty leadership | Identify program and course hotspots | Cohort and course explorer |
| Course coordinators | Understand assessment and engagement patterns | Course performance dashboard |
| Student support teams | Prioritise outreach with context | Restricted action queue |
| Data & Analytics | Create trusted, reusable metrics | Governed star schema, dbt tests |
| Privacy / governance | Validate appropriate and transparent use | Data classification, model card, access matrix |

## Measures of success

- Reduction in time from risk signal to human review
- High-risk students covered by timely outreach
- Student-support queue aligned with operational capacity
- Data-quality tests passing at agreed refresh cadence
- Transparent documentation of assumptions and limitations
- Evidence that dashboard users can identify and act on priority cohorts

## Non-goals

- Automated student sanctions, exclusion or high-impact decisions
- Replacing professional judgement, academic advising or wellbeing support
- Identifying individual students from portfolio data
- Claiming causal intervention impact without an approved evaluation design
