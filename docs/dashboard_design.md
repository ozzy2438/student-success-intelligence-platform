# Dashboard Design

## Page 1 — Executive Overview

**Audience:** executive leadership, Chief Data and Analytics Officer, senior faculty leaders

- KPI cards: Active Students, High/Critical Risk Students, At-Risk Rate, Withdrawal Rate, On-Time Submission Rate, Intervention Coverage Rate, Data Quality Score
- Line chart: At-risk rate by teaching week
- Bar chart: High/Critical risk students by faculty
- Heatmap: Faculty by week risk concentration
- Bar chart: Top courses by high-risk count
- Narrative card: weekly recommended action

## Page 2 — Student Risk & Cohort Explorer

**Audience:** faculty and student-success managers

- Slicers: term, faculty, programme, course, week, risk tier, study level, intervention status
- Stacked column: risk tier distribution
- Line chart: engagement score versus week
- Scatter: attendance rate versus risk probability
- Decomposition tree: faculty → programme → course → risk tier
- Drill-through: anonymised student-course risk context

## Page 3 — Intervention Operations

**Audience:** student-support managers and authorised advisers

- Priority queue table: student key, course, risk tier, driver, recommendation, priority rank
- Cards: priority demand, contacted students, support acceptance, engagement improved
- Bar chart: intervention type and outcome
- Matrix: assigned team by contact status
- Note: this page is a synthetic operational prototype; real use requires role-based access and human review

## Page 4 — Course & Assessment Performance

**Audience:** course coordinators and learning designers

- Cards: on-time rate, missing submissions, average assessment score, withdrawal rate
- Line: late submissions by week
- Box/column: score distribution by course
- Heatmap: course by due week for missing submissions
- Scatter: engagement score versus final mark

## Page 5 — Governance & Responsible Analytics

**Audience:** data governance, privacy, analytics leadership

- Data-quality score by asset
- Table: completeness, validity and freshness status
- Model version and threshold cards
- Responsible-use policy text
- RAG status for key controls
- Link-style text to model card, data dictionary and privacy framework
