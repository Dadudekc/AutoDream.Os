import json
import logging
import os
import sys


class JsonFormatter(logging.Formatter):
    def format(self, record):
        base = {
            "lvl": record.levelname,
            "msg": record.getMessage(),
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "logger": record.name,
        }
        if record.exc_info:
            base["exc"] = self.formatException(record.exc_info)
        return json.dumps(base)

def configure_logging():
    level = getattr(logging, os.getenv("LOG_LEVEL","INFO").upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
