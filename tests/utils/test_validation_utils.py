#!/usr/bin/env python3
"""Unit tests for validation utilities."""

import unittest
from src.utils.validation_utils import ValidationUtils


class TestValidationUtils(unittest.TestCase):
    """Test validation utilities functionality."""

    def setUp(self):
        self.validation = ValidationUtils()

    def test_email_validation(self):
        """Email addresses are validated correctly."""
        valid_emails = ["test@example.com", "user.name@domain.co.uk"]
        invalid_emails = ["invalid-email", "@domain.com", "user@", "user.domain.com"]
        for email in valid_emails:
            self.assertTrue(self.validation.is_valid_email(email))
        for email in invalid_emails:
            self.assertFalse(self.validation.is_valid_email(email))

    def test_url_validation(self):
        """URLs are validated correctly."""
        valid_urls = ["https://example.com", "http://test.org/path"]
        invalid_urls = ["not-a-url", "ftp://example.com", "example.com"]
        for url in valid_urls:
            self.assertTrue(self.validation.is_valid_url(url))
        for url in invalid_urls:
            self.assertFalse(self.validation.is_valid_url(url))

    def test_required_fields_validation(self):
        """Missing fields are reported."""
        data = {"name": "test", "email": "", "age": None}
        required_fields = ["name", "email", "age", "missing"]
        errors = self.validation.validate_required_fields(data, required_fields)
        self.assertIn("email", errors)
        self.assertIn("age", errors)
        self.assertIn("missing", errors)
        self.assertNotIn("name", errors)
