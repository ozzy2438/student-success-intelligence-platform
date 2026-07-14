select
    program_id,
    faculty,
    school,
    program_name,
    program_level
from {{ ref('stg_programs') }}
