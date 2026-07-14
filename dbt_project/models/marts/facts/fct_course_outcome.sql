select
    student_key,
    course_id,
    term_id,
    final_mark,
    outcome_status,
    withdrawn_flag,
    failed_flag,
    case when outcome_status in ('Fail', 'Withdrawn') then 1 else 0 end as adverse_outcome_flag
from {{ ref('stg_course_outcomes') }}
