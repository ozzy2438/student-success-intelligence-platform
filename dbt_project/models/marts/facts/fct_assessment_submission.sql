select
    s.submission_id,
    s.student_key,
    s.assessment_id,
    s.course_id,
    s.term_id,
    a.assessment_type,
    a.due_week,
    a.weight,
    s.submitted_flag,
    s.late_days,
    s.score
from {{ ref('stg_submissions') }} s
inner join {{ ref('stg_assessments') }} a using (assessment_id)
