select
    term_id,
    term_name,
    term_start_date
from {{ ref('stg_terms') }}
