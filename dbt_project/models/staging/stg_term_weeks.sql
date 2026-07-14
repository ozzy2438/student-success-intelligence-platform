select
    term_id,
    cast(week_number as integer) as week_number,
    cast(week_start_date as date) as week_start_date
from {{ source('raw', 'term_weeks') }}
