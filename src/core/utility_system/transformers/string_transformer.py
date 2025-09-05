#!/usr/bin/env python3
"""
String Transformer - V2 Compliance Module
=========================================

String transformation utilities.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import json
import re
from typing import Any, Dict


class StringTransformer:
    """String transformation utilities."""

    def sanitize(self, text: str, remove_special: bool = True, normalize_whitespace: bool = True) -> str:
        """Sanitize string."""
        try:
            sanitized = text
            
            if remove_special:
                sanitized = re.sub(r'[^\w\s-]', '', sanitized)
            
            if normalize_whitespace:
                sanitized = re.sub(r'\s+', ' ', sanitized).strip()
            
            return sanitized
        except Exception:
            return text

    def transform(self, data: Any, transformation_type: str, **kwargs) -> Any:
        """Transform data based on type."""
        try:
            if transformation_type == "json_stringify":
                return json.dumps(data, **kwargs)
            elif transformation_type == "json_parse":
                return json.loads(data, **kwargs)
            elif transformation_type == "string_lower":
                return str(data).lower()
            elif transformation_type == "string_upper":
                return str(data).upper()
            elif transformation_type == "string_title":
                return str(data).title()
            elif transformation_type == "string_strip":
                return str(data).strip()
            elif transformation_type == "string_replace":
                old = kwargs.get("old", "")
                new = kwargs.get("new", "")
                return str(data).replace(old, new)
            elif transformation_type == "string_split":
                delimiter = kwargs.get("delimiter", " ")
                return str(data).split(delimiter)
            elif transformation_type == "string_join":
                delimiter = kwargs.get("delimiter", " ")
                return delimiter.join(data)
            else:
                return data
        except Exception:
            return data
