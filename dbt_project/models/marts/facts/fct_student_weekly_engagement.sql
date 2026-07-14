select
    student_key,
    course_id,
    term_id,
    week_number,
    login_count,
    content_views,
    active_minutes,
    attendance_rate,
    engagement_score,
    week_on_week_engagement_change,
    three_week_engagement_average
from {{ ref('int_student_weekly_engagement') }}
