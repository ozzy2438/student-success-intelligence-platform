select
    intervention_id,
    student_key,
    term_id,
    cast(risk_week as integer) as risk_week,
    intervention_type,
    contact_status,
    cast(accepted_support_flag as integer) as accepted_support_flag,
    outcome_status,
    assigned_team
from {{ source('raw', 'interventions') }}
