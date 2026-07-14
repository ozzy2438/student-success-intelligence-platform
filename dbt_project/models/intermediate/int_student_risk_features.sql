with weekly as (
    select * from {{ ref('int_student_weekly_engagement') }}
),
assessment as (
    select * from {{ ref('int_student_assessment_features') }}
),
students as (
    select * from {{ ref('stg_students') }}
)
select
    w.student_key,
    w.course_id,
    w.term_id,
    w.week_number,
    w.engagement_score,
    w.week_on_week_engagement_change,
    w.three_week_engagement_average,
    w.attendance_rate,
    coalesce(a.missing_submission_count, 0) as missing_submission_count,
    coalesce(a.late_submission_count, 0) as late_submission_count,
    coalesce(a.assessment_average, 0.0) as assessment_average,
    s.prior_course_failures,
    case
        when w.engagement_score < 0.35 then 1 else 0
    end as low_engagement_flag,
    case
        when w.attendance_rate < 0.55 then 1 else 0
    end as low_attendance_flag,
    case
        when w.week_on_week_engagement_change <= -0.20 then 1 else 0
    end as material_engagement_decline_flag
from weekly w
inner join students s using (student_key)
left join assessment a using (student_key, course_id, term_id)
