#!/usr/bin/env python3
"""
Response Capturer
================

Captures Thea responses using various methods.
"""

from .response_handler import ResponseHandler


class ResponseCapturer(ResponseHandler):
    """Response capturer using the consolidated response handler."""

    def capture_response(self, use_selenium: bool = True, driver=None):
        """Capture response using the parent handler."""
        return super().capture_response(use_selenium, driver)
