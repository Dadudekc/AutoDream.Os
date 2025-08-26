#!/usr/bin/env python3
"""
API Manager - V2 Modular Architecture
====================================

Manages API configuration, requests, and HTTP session management.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4H - Communication Manager Modularization
License: MIT
"""

import logging
import json
import aiohttp
import ssl
import certifi
import base64
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import asdict

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority
from .models import APIConfig
from .types import CommunicationTypes, CommunicationConfig

logger = logging.getLogger(__name__)


class APIManager(BaseManager):
    """
    API Manager - Single responsibility: API configuration and request management
    
    Manages:
    - API configuration storage
    - HTTP session management
    - API request execution
    - Authentication handling
    """

    def __init__(self, config_path: str = "config/api_manager.json"):
        """Initialize API manager"""
        super().__init__(
            manager_name="APIManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        self.api_configs: Dict[str, APIConfig] = {}
        self.http_session: Optional[aiohttp.ClientSession] = None
        self.request_metrics: Dict[str, Dict[str, Any]] = {}
        
        # API settings
        self.default_timeout = CommunicationConfig.DEFAULT_TIMEOUT
        self.default_retry_count = CommunicationConfig.DEFAULT_RETRY_COUNT
        self.max_concurrent_requests = CommunicationConfig.MAX_CONCURRENT_CONNECTIONS
        
        # Initialize API system
        self._load_manager_config()
        self._setup_default_api_configs()
    
    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.default_timeout = config.get('default_timeout', 
                                                   CommunicationConfig.DEFAULT_TIMEOUT)
                    self.default_retry_count = config.get('default_retry_count', 
                                                        CommunicationConfig.DEFAULT_RETRY_COUNT)
                    self.max_concurrent_requests = config.get('max_concurrent_requests', 
                                                            CommunicationConfig.MAX_CONCURRENT_CONNECTIONS)
            else:
                logger.warning(f"API config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load API config: {e}")
    
    def _setup_default_api_configs(self):
        """Setup default API configurations"""
        # Default HTTP API config
        default_http_config = APIConfig(
            base_url="http://localhost:8000",
            headers={"Content-Type": "application/json"},
            timeout=self.default_timeout,
            retry_count=self.default_retry_count,
            rate_limit=None,
            authentication={}
        )
        self.api_configs["default_http"] = default_http_config
        
        # Default HTTPS API config
        default_https_config = APIConfig(
            base_url="https://localhost:8443",
            headers={"Content-Type": "application/json"},
            timeout=self.default_timeout,
            retry_count=self.default_retry_count,
            rate_limit=None,
            authentication={}
        )
        self.api_configs["default_https"] = default_https_config
    
    def configure_api(self, api_name: str, base_url: str, 
                     headers: Optional[Dict[str, str]] = None,
                     timeout: Optional[float] = None, 
                     retry_count: Optional[int] = None,
                     rate_limit: Optional[int] = None, 
                     authentication: Optional[Dict[str, Any]] = None):
        """Configure API settings"""
        try:
            api_config = APIConfig(
                base_url=base_url,
                headers=headers or {},
                timeout=timeout or self.default_timeout,
                retry_count=retry_count or self.default_retry_count,
                rate_limit=rate_limit,
                authentication=authentication or {}
            )
            
            self.api_configs[api_name] = api_config
            
            # Initialize request metrics
            self.request_metrics[api_name] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "average_response_time": 0.0,
                "last_request": None,
                "rate_limit_hits": 0
            }
            
            self._emit_event("api_configured", {
                "api_name": api_name,
                "base_url": base_url,
                "timeout": api_config.timeout
            })
            
            logger.info(f"API configured: {api_name} -> {base_url}")
            
        except Exception as e:
            logger.error(f"Failed to configure API {api_name}: {e}")
    
    async def _ensure_http_session(self, use_ssl: bool = False) -> aiohttp.ClientSession:
        """Ensure HTTP session exists and is properly configured"""
        try:
            if self.http_session is None or self.http_session.closed:
                if use_ssl:
                    ssl_context = ssl.create_default_context(cafile=certifi.where())
                    connector = aiohttp.TCPConnector(ssl=ssl_context, 
                                                   limit=self.max_concurrent_requests)
                else:
                    connector = aiohttp.TCPConnector(limit=self.max_concurrent_requests)
                
                self.http_session = aiohttp.ClientSession(connector=connector)
            
            return self.http_session
            
        except Exception as e:
            logger.error(f"Failed to create HTTP session: {e}")
            raise
    
    async def api_request(self, api_name: str, endpoint: str, method: str = "GET",
                         data: Optional[Any] = None, 
                         headers: Optional[Dict[str, str]] = None) -> Optional[Any]:
        """Make API request"""
        try:
            if api_name not in self.api_configs:
                logger.warning(f"API not configured: {api_name}")
                return None
            
            api_config = self.api_configs[api_name]
            
            # Determine if SSL is needed
            use_ssl = api_config.base_url.startswith("https://")
            
            # Ensure HTTP session exists
            session = await self._ensure_http_session(use_ssl)
            
            # Prepare request
            url = f"{api_config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            request_headers = api_config.headers.copy()
            request_headers.update(headers or {})
            
            # Add authentication if configured
            if api_config.authentication:
                if 'api_key' in api_config.authentication:
                    request_headers['Authorization'] = f"Bearer {api_config.authentication['api_key']}"
                elif 'basic_auth' in api_config.authentication:
                    auth = api_config.authentication['basic_auth']
                    credentials = f"{auth['username']}:{auth['password']}"
                    encoded = base64.b64encode(credentials.encode()).decode()
                    request_headers['Authorization'] = f"Basic {encoded}"
            
            # Track request start time
            start_time = datetime.now()
            
            # Make request
            async with session.request(
                method,
                url,
                json=data if method in ['POST', 'PUT', 'PATCH'] else None,
                params=data if method == 'GET' else None,
                headers=request_headers,
                timeout=aiohttp.ClientTimeout(total=api_config.timeout)
            ) as response:
                
                # Calculate response time
                response_time = (datetime.now() - start_time).total_seconds()
                
                # Update metrics
                if api_name in self.request_metrics:
                    metrics = self.request_metrics[api_name]
                    metrics["total_requests"] += 1
                    metrics["last_request"] = datetime.now().isoformat()
                    
                    if response.status == 200:
                        metrics["successful_requests"] += 1
                    else:
                        metrics["failed_requests"] += 1
                    
                    # Update average response time
                    current_avg = metrics["average_response_time"]
                    total_requests = metrics["total_requests"]
                    metrics["average_response_time"] = (
                        (current_avg * (total_requests - 1) + response_time) / total_requests
                    )
                
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"API request failed with status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"API request failed: {e}")
            
            # Update failure metrics
            if api_name in self.request_metrics:
                self.request_metrics[api_name]["failed_requests"] += 1
            
            return None
    
    def get_api_config(self, api_name: str) -> Optional[APIConfig]:
        """Get API configuration"""
        try:
            return self.api_configs.get(api_name)
        except Exception as e:
            logger.error(f"Failed to get API config for {api_name}: {e}")
            return None
    
    def get_api_statistics(self) -> Dict[str, Any]:
        """Get API request statistics"""
        try:
            total_apis = len(self.api_configs)
            total_requests = sum(
                metrics.get("total_requests", 0) 
                for metrics in self.request_metrics.values()
            )
            successful_requests = sum(
                metrics.get("successful_requests", 0) 
                for metrics in self.request_metrics.values()
            )
            failed_requests = sum(
                metrics.get("failed_requests", 0) 
                for metrics in self.request_metrics.values()
            )
            
            success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
            
            return {
                "total_apis": total_apis,
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "failed_requests": failed_requests,
                "success_rate": success_rate,
                "api_metrics": self.request_metrics
            }
            
        except Exception as e:
            logger.error(f"Failed to get API statistics: {e}")
            return {}
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            # Close HTTP session
            if self.http_session and not self.http_session.closed:
                await self.http_session.close()
            
            super().cleanup()
            logger.info("APIManager cleanup completed")
            
        except Exception as e:
            logger.error(f"APIManager cleanup failed: {e}")

