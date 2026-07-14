select
    assessment_id,
    course_id,
    assessment_type,
    cast(due_week as integer) as due_week,
    cast(weight as double) as weight
from {{ source('raw', 'assessments') }}
