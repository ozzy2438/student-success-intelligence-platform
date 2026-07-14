select *
from {{ ref('fct_student_weekly_engagement') }}
where attendance_rate < 0
   or attendance_rate > 1
   or engagement_score < 0
   or engagement_score > 1
