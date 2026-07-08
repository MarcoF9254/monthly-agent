from validators.business_rules import (
    br001_required_fields,
    br002_fee_uncertainty,
    br003_registration_period,
    br004_qa_status,
)


RULES = [
    br001_required_fields,
    br002_fee_uncertainty,
    br003_registration_period,
    br004_qa_status,
]
