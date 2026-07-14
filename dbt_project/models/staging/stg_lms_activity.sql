select
    student_key,
    course_id,
    term_id,
    cast(week_number as integer) as week_number,
    cast(login_count as integer) as login_count,
    cast(content_views as integer) as content_views,
    cast(active_minutes as integer) as active_minutes
from {{ source('raw', 'lms_activity') }}
