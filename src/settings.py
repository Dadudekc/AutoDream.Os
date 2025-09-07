
# MIGRATED: This file has been migrated to the centralized configuration system
"""Application-wide configuration settings (SSOT)."""

from __future__ import annotations

import os

# Shared configuration values
SECRET_KEY = os.getenv("PORTAL_SECRET_KEY", "change-me")
DEBUG = os.getenv("PORTAL_DEBUG", "false").lower() == "true"
