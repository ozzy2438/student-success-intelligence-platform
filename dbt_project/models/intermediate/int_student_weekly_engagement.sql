with weekly_base as (
    select
        l.student_key,
        l.course_id,
        l.term_id,
        l.week_number,
        l.login_count,
        l.content_views,
        l.active_minutes,
        a.attendance_rate,
        case
            when l.active_minutes >= 180 then 1.0
            else cast(l.active_minutes as double) / 180.0
        end as active_minutes_component,
        least(cast(l.login_count as double) / 8.0, 1.0) as login_component,
        least(cast(l.content_views as double) / 20.0, 1.0) as content_component
    from {{ ref('stg_lms_activity') }} l
    inner join {{ ref('stg_attendance') }} a
        using (student_key, course_id, term_id, week_number)
),
scored as (
    select
        *,
        least(
            1.0,
            greatest(
                0.0,
                0.45 * active_minutes_component
                + 0.20 * login_component
                + 0.20 * content_component
                + 0.15 * attendance_rate
            )
        ) as engagement_score
    from weekly_base
)
select
    *,
    engagement_score
        - lag(engagement_score) over (
            partition by student_key, course_id, term_id
            order by week_number
        ) as week_on_week_engagement_change,
    avg(engagement_score) over (
        partition by student_key, course_id, term_id
        order by week_number
        rows between 2 preceding and current row
    ) as three_week_engagement_average
from scored
