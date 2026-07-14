select
    enrolment_id,
    student_key,
    course_id,
    term_id,
    enrolment_status,
    cast(credit_points as integer) as credit_points
from {{ source('raw', 'enrolments') }}
