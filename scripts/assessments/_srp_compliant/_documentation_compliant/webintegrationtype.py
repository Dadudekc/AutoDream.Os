"""
webintegrationtype.py
Module: webintegrationtype.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:06
"""

# WebIntegrationType - Extracted for SRP compliance

class WebIntegrationType(Enum):
    """Web integration types"""
    API_ENDPOINTS = "api_endpoints"
    WEBHOOKS = "webhooks"
    WEBSOCKETS = "websockets"
    HTTP_CLIENT = "http_client"
    BROWSER_AUTOMATION = "browser_automation"
    UI_TESTING = "ui_testing"


@dataclass

