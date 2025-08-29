import logging


class LoggingMixin:
    """Mixin providing basic logging facilities."""

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        super().__init__(*args, **kwargs)
