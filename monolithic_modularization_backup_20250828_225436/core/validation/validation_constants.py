"""Constants for onboarding validation modules."""

ONBOARDING_STAGES = [
    "registration",
    "verification",
    "profile_setup",
    "training",
    "activation",
    "completion",
]

VERIFICATION_METHODS = [
    "email",
    "sms",
    "phone",
    "document",
    "biometric",
    "social",
    "manual",
]

VERIFICATION_STATUSES = [
    "pending",
    "in_progress",
    "completed",
    "failed",
    "expired",
]

COMPLIANCE_STATUSES = [
    "pending",
    "in_review",
    "approved",
    "rejected",
    "requires_action",
]

REQUIRED_FIELDS = ["user_id", "stage", "start_date", "status"]

STAGE_REQUIRED_FIELDS = ["name", "order", "required"]

__all__ = [
    "ONBOARDING_STAGES",
    "VERIFICATION_METHODS",
    "VERIFICATION_STATUSES",
    "COMPLIANCE_STATUSES",
    "REQUIRED_FIELDS",
    "STAGE_REQUIRED_FIELDS",
]
