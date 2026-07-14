select
    course_id,
    course_name,
    faculty,
    cast(credit_points as integer) as credit_points,
    delivery_mode,
    assessment_intensity
from {{ source('raw', 'courses') }}
