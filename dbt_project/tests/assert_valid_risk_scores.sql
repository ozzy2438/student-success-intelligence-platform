select *
from {{ ref('fct_student_risk_snapshot') }}
where baseline_risk_probability < 0
   or baseline_risk_probability > 1
   or baseline_risk_probability is null
