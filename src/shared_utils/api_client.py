"""API client utilities for the unified workspace.

Concrete improvements implemented:
- Synchronous client now has retry with backoff, default timeouts, and context manager support
- Async client reuses a session, applies default timeout, and simple retry with backoff for transient errors
"""

from __future__ import annotations

import asyncio
from collections.abc import Iterable
from typing import Any

import aiohttp
import requests

try:
    from requests.adapters import HTTPAdapter
    from urllib3.util import Retry  # type: ignore
except Exception:  # pragma: no cover
    Retry = None  # type: ignore
    HTTPAdapter = None  # type: ignore

from .config import get_setting


class APIClient:
    """Synchronous API client with retries, timeouts, and context manager support."""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        timeout_seconds: float | None = None,
        retry_total: int = 3,
        retry_status_forcelist: Iterable[int] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or get_setting("API_KEY")
        self.timeout = float(timeout_seconds or get_setting("API_TIMEOUT", "10") or 10)
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

        # Configure retries for idempotent methods and common transient statuses
        status_forcelist = list(retry_status_forcelist or [429, 500, 502, 503, 504])
        if Retry and HTTPAdapter:
            retry = Retry(
                total=retry_total,
                backoff_factor=0.5,
                status_forcelist=status_forcelist,
                allowed_methods=["GET", "HEAD", "OPTIONS", "PUT", "DELETE"],
                raise_on_status=False,
            )
            adapter = HTTPAdapter(max_retries=retry)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)

    def __enter__(self) -> APIClient:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # noqa: D401
        self.close()

    def close(self) -> None:
        self.session.close()

    def get(self, endpoint: str, timeout: float | None = None, **kwargs: Any) -> requests.Response:
        """Perform a GET request with a default timeout."""
        return self.session.get(
            f"{self.base_url}{endpoint}", timeout=timeout or self.timeout, **kwargs
        )

    def post(
        self,
        endpoint: str,
        data: dict[str, Any],
        timeout: float | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Perform a POST request with JSON body and a default timeout."""
        return self.session.post(
            f"{self.base_url}{endpoint}", json=data, timeout=timeout or self.timeout, **kwargs
        )


class AsyncAPIClient:
    """Asynchronous API client with reusable session, timeout, and simple retries."""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        timeout_seconds: float | None = None,
        retry_total: int = 3,
        retry_statuses: Iterable[int] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or get_setting("API_KEY")
        self.headers: dict[str, str] = {}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
        total = float(timeout_seconds or get_setting("API_TIMEOUT", "10") or 10)
        self.timeout = aiohttp.ClientTimeout(total=total)
        self._session: aiohttp.ClientSession | None = None
        self.retry_total = retry_total
        self.retry_statuses = set(retry_statuses or {429, 500, 502, 503, 504})

    async def __aenter__(self) -> AsyncAPIClient:
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: D401
        await self.aclose()

    async def _ensure_session(self) -> None:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self.timeout)

    async def aclose(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def _request_with_retries(
        self,
        method: str,
        endpoint: str,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> aiohttp.ClientResponse:
        await self._ensure_session()
        assert self._session is not None
        url = f"{self.base_url}{endpoint}"
        attempt = 0
        last_exc: BaseException | None = None
        while attempt <= self.retry_total:
            try:
                async with self._session.request(
                    method, url, headers=self.headers, json=json, **kwargs
                ) as resp:
                    if resp.status in self.retry_statuses and attempt < self.retry_total:
                        # exponential backoff with jitter
                        delay = (2**attempt) * 0.5 + (0.1 * attempt)
                        await asyncio.sleep(delay)
                        attempt += 1
                        continue
                    return resp
            except (TimeoutError, aiohttp.ClientError) as exc:  # transient
                last_exc = exc
                if attempt >= self.retry_total:
                    raise
                delay = (2**attempt) * 0.5 + (0.1 * attempt)
                await asyncio.sleep(delay)
                attempt += 1
        # Should not reach here
        if last_exc:
            raise last_exc
        raise RuntimeError("Async request failed without exception")

    async def get(self, endpoint: str, **kwargs: Any) -> aiohttp.ClientResponse:
        return await self._request_with_retries("GET", endpoint, **kwargs)

    async def post(
        self, endpoint: str, data: dict[str, Any], **kwargs: Any
    ) -> aiohttp.ClientResponse:
        return await self._request_with_retries("POST", endpoint, json=data, **kwargs)
