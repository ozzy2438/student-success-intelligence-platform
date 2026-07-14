with source as (
    select * from {{ source('raw', 'students') }}
)

select
    student_key,
    program_id,
    faculty,
    study_level,
    study_load,
    delivery_preference,
    equity_group,
    commencement_term,
    cast(prior_course_failures as integer) as prior_course_failures
from source
