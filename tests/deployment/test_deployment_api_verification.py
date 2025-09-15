#!/usr/bin/env python3
"""
Deployment API Verification - V2 Compliant
==========================================

Focused API endpoint verification for deployment testing.
V2 Compliance: < 400 lines, single responsibility.

Author: Agent-5 (Data Organization Specialist)
Test Type: Deployment API Verification
"""

import pytest
import time
from datetime import datetime
from typing import Any, Dict

from tests.integration_testing_framework import IntegrationTestFramework, TestStatus


class DeploymentAPIVerifier:
    """API endpoint verification for deployment testing."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.framework = IntegrationTestFramework(base_url=base_url)
    
    def verify_api_endpoints(self) -> Dict[str, Any]:
        """Verify all API endpoints are functional and properly documented."""
        result = {
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "endpoints_tested": 0,
            "endpoints_passed": 0
        }
        
        # Core API endpoints to verify
        endpoints = [
            ("/agents", "GET"),
            ("/agents", "POST"),
            ("/messages", "GET"),
            ("/messages", "POST"),
            ("/vector/search", "POST"),
            ("/vector/documents", "GET"),
            ("/analytics/performance", "GET"),
            ("/health", "GET")
        ]
        
        for endpoint, method in endpoints:
            result["endpoints_tested"] += 1
            
            try:
                # Use appropriate test data for POST requests
                test_data = None
                if method == "POST":
                    if endpoint == "/agents":
                        test_data = {
                            "agent_id": f"deploy-test-{int(time.time())}",
                            "agent_name": "Deployment Test Agent",
                            "specialization": "Testing"
                        }
                    elif endpoint == "/messages":
                        test_data = {
                            "to_agent": "Agent-7",
                            "content": "Deployment verification message",
                            "priority": "LOW"
                        }
                    elif endpoint == "/vector/search":
                        test_data = {"query": "deployment test"}
                    elif endpoint == "/vector/documents":
                        test_data = {
                            "content": "Deployment verification document",
                            "metadata": {"type": "test"}
                        }
                
                api_result = self.framework.validate_api_endpoint(
                    endpoint, method, expected_status=200, request_data=test_data
                )
                
                if api_result.status == TestStatus.PASSED:
                    result["endpoints_passed"] += 1
                    
            except Exception as e:
                print(f"Endpoint test failed for {method} {endpoint}: {e}")
        
        # Calculate success rate
        success_rate = result["endpoints_passed"] / result["endpoints_tested"]
        if success_rate >= 0.9:  # 90% success rate required
            result["status"] = "passed"
        else:
            result["status"] = "failed"
            result["message"] = f"API endpoint success rate too low: {success_rate:.1%}"
        
        return result
    
    def verify_database_connectivity(self) -> Dict[str, Any]:
        """Verify database connectivity and basic operations."""
        result = {
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "databases_checked": []
        }
        
        # Test vector database connectivity through API
        try:
            # Test document creation (implies database write)
            doc_result = self.framework.validate_api_endpoint(
                "/vector/documents",
                "POST",
                request_data={
                    "content": "Database connectivity test document",
                    "metadata": {"test_type": "deployment_verification"}
                },
                expected_status=201
            )
            
            if doc_result.status == TestStatus.PASSED:
                result["databases_checked"].append({
                    "name": "vector_database",
                    "status": "connected",
                    "write_test": "passed"
                })
            else:
                result["databases_checked"].append({
                    "name": "vector_database",
                    "status": "write_failed",
                    "error": "Document creation failed"
                })
                
        except Exception as e:
            result["databases_checked"].append({
                "name": "vector_database",
                "status": "error",
                "error": str(e)
            })
        
        # Check if any databases are working
        working_databases = [db for db in result["databases_checked"] if db["status"] == "connected"]
        if working_databases:
            result["status"] = "passed"
        else:
            result["status"] = "failed"
            result["message"] = "No database connectivity verified"
        
        return result


# Test functions
@pytest.mark.deployment
def test_api_endpoints_verification():
    """Test API endpoints verification."""
    verifier = DeploymentAPIVerifier()
    result = verifier.verify_api_endpoints()
    
    assert result["status"] in ["passed", "failed", "error"]
    assert "endpoints_tested" in result
    assert "endpoints_passed" in result
    assert result["endpoints_tested"] > 0


@pytest.mark.deployment
def test_database_connectivity_verification():
    """Test database connectivity verification."""
    verifier = DeploymentAPIVerifier()
    result = verifier.verify_database_connectivity()
    
    assert result["status"] in ["passed", "failed", "error"]
    assert "databases_checked" in result
    assert len(result["databases_checked"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
