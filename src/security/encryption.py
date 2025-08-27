#!/usr/bin/env python3
"""Encryption utilities meeting ISO27001 requirements.

This module provides high level helpers for encrypting data at rest and
creating secure contexts for data in transit. It uses the ``cryptography``
package for symmetric encryption and the ``ssl`` module for TLS context
creation.  The functionality is intentionally small but covers the common
use cases required by the project and keeps the implementation easily
understandable for auditing.
"""

from __future__ import annotations

from pathlib import Path
import ssl
from typing import Optional

from cryptography.fernet import Fernet


class EncryptionManager:
    """Simple AES based encryption manager.

    Data is encrypted using the ``Fernet`` implementation which provides
    AES‑128 in CBC mode with HMAC for authentication.  The helper also
    exposes utilities for encrypting files (data at rest) and producing a
    TLS context (data in transit).
    """

    def __init__(self, key: Optional[bytes] = None) -> None:
        self.key: bytes = key or Fernet.generate_key()
        self._cipher = Fernet(self.key)

    # ------------------------------------------------------------------
    # Symmetric encryption helpers
    # ------------------------------------------------------------------
    @staticmethod
    def generate_key() -> bytes:
        """Generate a new encryption key."""

        return Fernet.generate_key()

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt arbitrary bytes using the managed key."""

        return self._cipher.encrypt(data)

    def decrypt(self, token: bytes) -> bytes:
        """Decrypt data previously encrypted with :meth:`encrypt`."""

        return self._cipher.decrypt(token)

    # ------------------------------------------------------------------
    # Data at rest helpers
    # ------------------------------------------------------------------
    def encrypt_file(self, input_path: str, output_path: str) -> None:
        """Encrypt file contents and write to ``output_path``."""

        data = Path(input_path).read_bytes()
        Path(output_path).write_bytes(self.encrypt(data))

    def decrypt_file(self, input_path: str, output_path: str) -> None:
        """Decrypt previously encrypted file contents."""

        data = Path(input_path).read_bytes()
        Path(output_path).write_bytes(self.decrypt(data))

    # ------------------------------------------------------------------
    # Data in transit helpers
    # ------------------------------------------------------------------
    @staticmethod
    def create_secure_context() -> ssl.SSLContext:
        """Return a hardened :class:`ssl.SSLContext` for TLS connections."""

        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        return context


__all__ = ["EncryptionManager"]
