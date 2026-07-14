select
    student_key,
    course_id,
    term_id,
    cast(final_mark as double) as final_mark,
    outcome_status,
    cast(withdrawn_flag as integer) as withdrawn_flag,
    cast(failed_flag as integer) as failed_flag
from {{ source('raw', 'course_outcomes') }}
