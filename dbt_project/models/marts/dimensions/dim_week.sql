select
    concat(term_id, '-W', lpad(cast(week_number as varchar), 2, '0')) as week_key,
    term_id,
    week_number,
    week_start_date
from {{ ref('stg_term_weeks') }}
