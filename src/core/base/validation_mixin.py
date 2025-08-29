class ValidationMixin:
    """Mixin providing simple validation utilities."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_config(self) -> bool:
        config = getattr(self, "config", None)
        if not config:
            return False
        required = ["manager_id", "name"]
        return all(getattr(config, field, None) for field in required)
