select
    intervention_id,
    student_key,
    term_id,
    risk_week,
    intervention_type,
    contact_status,
    accepted_support_flag,
    outcome_status,
    assigned_team,
    pre_intervention_engagement,
    post_intervention_engagement,
    engagement_change_after_intervention
from {{ ref('int_intervention_outcomes') }}
