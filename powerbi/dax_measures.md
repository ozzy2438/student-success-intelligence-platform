# Power BI DAX Measure Catalogue

## Student and risk metrics

```DAX
Active Students =
DISTINCTCOUNT('fct_student_risk_snapshot'[student_key])
```

```DAX
High and Critical Risk Students =
CALCULATE(
    DISTINCTCOUNT('fct_student_risk_snapshot'[student_key]),
    'fct_student_risk_snapshot'[risk_tier] IN {"High", "Critical"}
)
```

```DAX
At-Risk Rate =
DIVIDE([High and Critical Risk Students], [Active Students], 0)
```

```DAX
Average Risk Score =
AVERAGE('fct_student_risk_snapshot'[risk_probability])
```

```DAX
Critical Risk Students =
CALCULATE(
    DISTINCTCOUNT('fct_student_risk_snapshot'[student_key]),
    'fct_student_risk_snapshot'[risk_tier] = "Critical"
)
```

## Engagement and assessment metrics

```DAX
Average Weekly Active Minutes =
AVERAGE('fct_student_weekly_engagement'[active_minutes])
```

```DAX
On-Time Submission Rate =
DIVIDE(
    CALCULATE(
        COUNTROWS('fct_assessment_submission'),
        'fct_assessment_submission'[submitted_flag] = 1,
        'fct_assessment_submission'[late_days] = 0
    ),
    CALCULATE(
        COUNTROWS('fct_assessment_submission'),
        'fct_assessment_submission'[submitted_flag] = 1
    ),
    0
)
```

```DAX
Late Submission Rate =
DIVIDE(
    CALCULATE(
        COUNTROWS('fct_assessment_submission'),
        'fct_assessment_submission'[late_days] > 0
    ),
    COUNTROWS('fct_assessment_submission'),
    0
)
```

```DAX
Average Assessment Score =
AVERAGE('fct_assessment_submission'[score])
```

## Outcomes and interventions

```DAX
Withdrawal Rate =
DIVIDE(
    CALCULATE(
        COUNTROWS('fct_course_outcome'),
        'fct_course_outcome'[withdrawn_flag] = 1
    ),
    COUNTROWS('fct_course_outcome'),
    0
)
```

```DAX
Intervention Coverage Rate =
DIVIDE(
    DISTINCTCOUNT('fct_support_intervention'[student_key]),
    [High and Critical Risk Students],
    0
)
```

```DAX
Average Days to Contact =
AVERAGE('fct_support_intervention'[days_to_contact])
```

## Data governance metrics

```DAX
Data Quality Score =
AVERAGE('data_quality_summary'[quality_score])
```

```DAX
Passing Quality Checks =
CALCULATE(
    COUNTROWS('data_quality_summary'),
    'data_quality_summary'[test_status] = "PASS"
)
```
