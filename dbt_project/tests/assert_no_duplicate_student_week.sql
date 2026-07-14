select
    student_key,
    course_id,
    term_id,
    week_number,
    count(*) as record_count
from {{ ref('fct_student_weekly_engagement') }}
group by 1, 2, 3, 4
having count(*) > 1
