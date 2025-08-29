"""Rule definitions for onboarding validation."""

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


def is_valid_stage(stage: str) -> bool:
    """Return True if *stage* is a valid onboarding stage."""
    return stage.lower() in ONBOARDING_STAGES


def is_valid_verification_method(method: str) -> bool:
    """Return True if *method* is an allowed verification method."""
    return method.lower() in VERIFICATION_METHODS
