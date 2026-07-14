select
    submission_id,
    student_key,
    assessment_id,
    course_id,
    term_id,
    cast(submitted_flag as integer) as submitted_flag,
    cast(late_days as integer) as late_days,
    cast(score as double) as score
from {{ source('raw', 'submissions') }}
