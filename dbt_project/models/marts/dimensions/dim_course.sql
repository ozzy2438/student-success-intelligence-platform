select
    course_id,
    course_name,
    faculty,
    credit_points,
    delivery_mode,
    assessment_intensity
from {{ ref('stg_courses') }}
