with submissions as (
    select * from {{ ref('stg_submissions') }}
),
aggregated as (
    select
        student_key,
        course_id,
        term_id,
        count(*) as assessment_count,
        sum(case when submitted_flag = 0 then 1 else 0 end) as missing_submission_count,
        sum(case when late_days > 0 then 1 else 0 end) as late_submission_count,
        avg(case when submitted_flag = 1 then score end) as assessment_average,
        avg(late_days) as average_late_days
    from submissions
    group by 1, 2, 3
)
select * from aggregated
