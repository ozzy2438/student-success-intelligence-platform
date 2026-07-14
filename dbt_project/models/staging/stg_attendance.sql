select
    student_key,
    course_id,
    term_id,
    cast(week_number as integer) as week_number,
    cast(attendance_rate as double) as attendance_rate
from {{ source('raw', 'attendance') }}
