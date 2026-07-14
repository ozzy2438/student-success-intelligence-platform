with features as (
    select * from {{ ref('int_student_risk_features') }}
),
risk_score as (
    select
        *,
        1.0 / (
            1.0 + exp(-(
                -3.15
                + 2.15 * (1 - engagement_score)
                + 1.45 * (1 - attendance_rate)
                + 0.75 * missing_submission_count
                + 0.28 * late_submission_count
                + 0.18 * prior_course_failures
                + 0.65 * low_engagement_flag
                + 0.45 * low_attendance_flag
                + 0.35 * material_engagement_decline_flag
            ))
        ) as baseline_risk_probability
    from features
)
select
    student_key,
    course_id,
    term_id,
    week_number,
    baseline_risk_probability,
    case
        when baseline_risk_probability >= 0.75 then 'Critical'
        when baseline_risk_probability >= 0.50 then 'High'
        when baseline_risk_probability >= 0.25 then 'Moderate'
        else 'Low'
    end as risk_tier,
    case
        when missing_submission_count > 0 then 'Missing assessment submission'
        when attendance_rate < 0.55 then 'Low attendance'
        when engagement_score < 0.35 then 'Low LMS engagement'
        when material_engagement_decline_flag = 1 then 'Rapid engagement decline'
        when late_submission_count > 0 then 'Repeated late submissions'
        else 'Monitor engagement'
    end as primary_risk_driver,
    case
        when baseline_risk_probability >= 0.75 then 'Priority human review within 2 business days'
        when baseline_risk_probability >= 0.50 then 'Academic outreach within 5 business days'
        when baseline_risk_probability >= 0.25 then 'Automated nudge and self-service support'
        else 'Continue monitoring'
    end as recommended_intervention,
    '{{ var("risk_model_version") }}' as model_version
from risk_score
