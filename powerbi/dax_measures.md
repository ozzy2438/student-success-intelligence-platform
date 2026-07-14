# DAX Measure Catalogue

Create a dedicated `Measures` table in Power BI and add the following measures.

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
Average Risk Probability =
AVERAGE('fct_student_risk_snapshot'[model_risk_probability])
```

```DAX
Priority Queue Count =
CALCULATE(
    COUNTROWS('fct_student_risk_snapshot'),
    'fct_student_risk_snapshot'[priority_flag] = 1
)
```

```DAX
Average Engagement Score =
AVERAGE('fct_student_weekly_engagement'[engagement_score])
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
Missing Submissions =
CALCULATE(
    COUNTROWS('fct_assessment_submission'),
    'fct_assessment_submission'[submitted_flag] = 0
)
```

```DAX
Average Assessment Score =
AVERAGE('fct_assessment_submission'[score])
```

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
Adverse Outcome Rate =
DIVIDE(
    CALCULATE(
        COUNTROWS('fct_course_outcome'),
        'fct_course_outcome'[adverse_outcome_flag] = 1
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
Contacted Students =
CALCULATE(
    DISTINCTCOUNT('fct_support_intervention'[student_key]),
    'fct_support_intervention'[contact_status] = "Contacted"
)
```

```DAX
Support Acceptance Rate =
DIVIDE(
    CALCULATE(
        COUNTROWS('fct_support_intervention'),
        'fct_support_intervention'[accepted_support_flag] = 1
    ),
    COUNTROWS('fct_support_intervention'),
    0
)
```

```DAX
Engagement Improved Interventions =
CALCULATE(
    COUNTROWS('fct_support_intervention'),
    'fct_support_intervention'[outcome_status] = "Engagement improved"
)
```

```DAX
Data Quality Score =
AVERAGE('data_quality_summary'[quality_score])
```

```DAX
High Risk Count by Course =
CALCULATE(
    COUNTROWS('fct_student_risk_snapshot'),
    'fct_student_risk_snapshot'[risk_tier] IN {"High", "Critical"}
)
```

```DAX
Weekly At-Risk Change =
[At-Risk Rate]
    - CALCULATE(
        [At-Risk Rate],
        DATEADD('dim_week'[week_start_date], -7, DAY)
    )
```

## Formatting guidance

- Format rate and probability measures as percentages with one decimal place
- Format `Data Quality Score` as a percentage
- Use conditional colour: green for low risk / valid quality, amber for moderate, red for high or critical
- Use a tooltip on risk visuals: `Risk signals support human review; they are not automated decisions`
