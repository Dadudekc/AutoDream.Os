#!/usr/bin/env python3
"""
Response Analyzer
================

Analyzes Thea responses and creates analysis reports.
"""

from .response_handler import ResponseHandler


class ResponseAnalyzer(ResponseHandler):
    """Response analyzer using the consolidated response handler."""
    
    def create_analysis(self, screenshot_path: str):
        """Create analysis using the parent handler."""
        # The analysis is created automatically in the response handler
        return screenshot_path
