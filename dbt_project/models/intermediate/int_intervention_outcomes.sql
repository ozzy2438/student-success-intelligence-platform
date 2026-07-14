with interventions as (
    select * from {{ ref('stg_interventions') }}
),
weekly as (
    select * from {{ ref('int_student_weekly_engagement') }}
),
pre_post as (
    select
        i.intervention_id,
        i.student_key,
        i.term_id,
        i.risk_week,
        i.intervention_type,
        i.contact_status,
        i.accepted_support_flag,
        i.outcome_status,
        i.assigned_team,
        avg(case when w.week_number between i.risk_week - 2 and i.risk_week - 1 then w.engagement_score end) as pre_intervention_engagement,
        avg(case when w.week_number between i.risk_week + 1 and i.risk_week + 2 then w.engagement_score end) as post_intervention_engagement
    from interventions i
    left join weekly w
        on i.student_key = w.student_key
        and i.term_id = w.term_id
    group by 1, 2, 3, 4, 5, 6, 7, 8, 9
)
select
    *,
    post_intervention_engagement - pre_intervention_engagement as engagement_change_after_intervention
from pre_post
