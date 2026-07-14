select
    student_key,
    program_id,
    faculty,
    study_level,
    study_load,
    delivery_preference,
    equity_group,
    commencement_term,
    prior_course_failures
from {{ ref('stg_students') }}
