select
    term_id,
    term_name,
    cast(start_date as date) as term_start_date
from {{ source('raw', 'terms') }}
