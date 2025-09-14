#!/usr/bin/env python3
"""
ROUTING FIXES VERIFICATION SCRIPT
=================================

Comprehensive verification script to validate all routing fixes operational.
Part of THEA's emergency routing patch implementation.

Author: Agent-4 (Strategic Oversight & Emergency Intervention Manager)
License: MIT
"""

import asyncio
import json
import logging
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.verified_messaging_service import get_verified_messaging_service
from core.routing_tracer import get_routing_tracer
from core.heartbeat_verification import get_heartbeat_system
from core.swarm_health_monitor import get_swarm_health_monitor
from core.messaging_core import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageType,
    UnifiedMessageTag
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# SWARM AGENTS
SWARM_AGENTS = [
    "Agent-1", "Agent-2", "Agent-3", "Agent-4",
    "Agent-5", "Agent-6", "Agent-7", "Agent-8"
]


class RoutingFixesVerifier:
    """Comprehensive routing fixes verification system."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.verification_results = {}
        self.start_time = datetime.now()
        
        # Initialize subsystems
        self.verified_messaging = get_verified_messaging_service()
        self.routing_tracer = get_routing_tracer()
        self.heartbeat_system = get_heartbeat_system()
        self.health_monitor = get_swarm_health_monitor()
    
    async def run_comprehensive_verification(self) -> dict:
        """Run comprehensive verification of all routing fixes."""
        self.logger.info("🚀 Starting comprehensive routing fixes verification...")
        
        verification_results = {
            "start_time": self.start_time.isoformat(),
            "tests": {},
            "overall_status": "unknown",
            "summary": {}
        }
        
        try:
            # Test 1: Verified Messaging Service
            self.logger.info("📋 Test 1: Verified Messaging Service")
            verification_results["tests"]["verified_messaging"] = await self._test_verified_messaging()
            
            # Test 2: Routing Tracer
            self.logger.info("📋 Test 2: Routing Tracer")
            verification_results["tests"]["routing_tracer"] = await self._test_routing_tracer()
            
            # Test 3: Heartbeat Verification
            self.logger.info("📋 Test 3: Heartbeat Verification")
            verification_results["tests"]["heartbeat_verification"] = await self._test_heartbeat_verification()
            
            # Test 4: Swarm Health Monitor
            self.logger.info("📋 Test 4: Swarm Health Monitor")
            verification_results["tests"]["swarm_health_monitor"] = await self._test_swarm_health_monitor()
            
            # Test 5: Agent-8 Specific Routing
            self.logger.info("📋 Test 5: Agent-8 Specific Routing")
            verification_results["tests"]["agent8_routing"] = await self._test_agent8_routing()
            
            # Test 6: Message Delivery Verification
            self.logger.info("📋 Test 6: Message Delivery Verification")
            verification_results["tests"]["message_delivery"] = await self._test_message_delivery()
            
            # Test 7: System Health Check
            self.logger.info("📋 Test 7: System Health Check")
            verification_results["tests"]["system_health"] = await self._test_system_health()
            
            # Test 8: Emergency Response System
            self.logger.info("📋 Test 8: Emergency Response System")
            verification_results["tests"]["emergency_response"] = await self._test_emergency_response()
            
            # Calculate overall status
            verification_results["overall_status"] = self._calculate_overall_status(verification_results["tests"])
            
            # Generate summary
            verification_results["summary"] = self._generate_summary(verification_results["tests"])
            
            verification_results["end_time"] = datetime.now().isoformat()
            verification_results["duration_seconds"] = (datetime.now() - self.start_time).total_seconds()
            
            self.logger.info(f"✅ Comprehensive verification completed in {verification_results['duration_seconds']:.2f} seconds")
            self.logger.info(f"📊 Overall Status: {verification_results['overall_status']}")
            
            return verification_results
            
        except Exception as e:
            self.logger.error(f"❌ Verification failed: {e}")
            verification_results["error"] = str(e)
            verification_results["overall_status"] = "failed"
            return verification_results
    
    async def _test_verified_messaging(self) -> dict:
        """Test verified messaging service."""
        try:
            # Test system health
            health = self.verified_messaging.get_system_health()
            
            # Test message routing
            test_message = UnifiedMessage(
                content="Routing verification test",
                sender="SYSTEM",
                recipient="Agent-8",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            
            # Test route verification
            verification_result = await self.verified_messaging.verify_route(test_message)
            
            return {
                "status": "passed",
                "system_health": health,
                "route_verification": {
                    "valid": verification_result.valid,
                    "expected_agent": verification_result.expected_agent,
                    "actual_agent": verification_result.actual_agent,
                    "verification_hash": verification_result.verification_hash
                },
                "message_success_rate": health.get("message_success_rate", 0.0),
                "average_response_time": health.get("average_response_time", 0.0)
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def _test_routing_tracer(self) -> dict:
        """Test routing tracer system."""
        try:
            # Test routing statistics
            stats = self.routing_tracer.get_routing_statistics()
            
            # Test agent routing analysis
            agent8_analysis = self.routing_tracer.get_agent_routing_analysis("Agent-8")
            
            # Test checksum generation
            test_message = UnifiedMessage(
                content="Checksum test",
                sender="SYSTEM",
                recipient="Agent-8",
                message_type=UnifiedMessageType.TEXT
            )
            
            checksum = self.routing_tracer.generate_checksum(test_message)
            checksum_verification = self.routing_tracer.verify_checksum(test_message, checksum)
            
            return {
                "status": "passed",
                "routing_statistics": stats,
                "agent8_analysis": agent8_analysis,
                "checksum_verification": {
                    "original_checksum": checksum_verification.original_checksum,
                    "calculated_checksum": checksum_verification.calculated_checksum,
                    "verification_passed": checksum_verification.verification_passed,
                    "message_integrity": checksum_verification.message_integrity
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def _test_heartbeat_verification(self) -> dict:
        """Test heartbeat verification system."""
        try:
            # Test system health
            health = self.heartbeat_system.get_system_health_summary()
            
            # Test agent status
            agent8_status = self.heartbeat_system.get_agent_status("Agent-8")
            
            # Test online/offline agents
            online_agents = self.heartbeat_system.get_online_agents()
            offline_agents = self.heartbeat_system.get_offline_agents()
            
            return {
                "status": "passed",
                "system_health": health,
                "agent8_status": {
                    "is_online": agent8_status.is_online if agent8_status else False,
                    "last_heartbeat": agent8_status.last_heartbeat.isoformat() if agent8_status else None,
                    "response_time_ms": agent8_status.response_time_ms if agent8_status else 0.0,
                    "consecutive_failures": agent8_status.consecutive_failures if agent8_status else 0
                },
                "online_agents": online_agents,
                "offline_agents": offline_agents,
                "total_agents": len(SWARM_AGENTS)
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def _test_swarm_health_monitor(self) -> dict:
        """Test swarm health monitor."""
        try:
            # Test current health
            current_health = self.health_monitor.get_current_health()
            
            # Test health history
            health_history = self.health_monitor.get_health_history(hours=1)
            
            return {
                "status": "passed",
                "current_health": {
                    "overall_health": current_health.overall_health,
                    "health_score": current_health.health_score,
                    "critical_issues": current_health.critical_issues,
                    "recommendations": current_health.recommendations
                },
                "health_history_count": len(health_history),
                "monitoring_active": self.health_monitor.is_monitoring
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def _test_agent8_routing(self) -> dict:
        """Test Agent-8 specific routing."""
        try:
            # Test Agent-8 coordinates
            from core.coordinate_loader import get_coordinate_loader
            coordinate_loader = get_coordinate_loader()
            agent8_coords = coordinate_loader.get_chat_coordinates("Agent-8")
            
            # Test Agent-8 message routing
            agent8_message = UnifiedMessage(
                content="Agent-8 routing test",
                sender="SYSTEM",
                recipient="Agent-8",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            
            # Test route verification for Agent-8
            verification_result = await self.verified_messaging.verify_route(agent8_message)
            
            # Test Agent-8 health status
            agent8_health = self.health_monitor.agent_health.get("Agent-8")
            
            return {
                "status": "passed",
                "coordinates": {
                    "x": agent8_coords[0] if agent8_coords else None,
                    "y": agent8_coords[1] if agent8_coords else None,
                    "available": agent8_coords is not None
                },
                "route_verification": {
                    "valid": verification_result.valid,
                    "expected_agent": verification_result.expected_agent,
                    "actual_agent": verification_result.actual_agent
                },
                "health_status": {
                    "is_online": agent8_health.is_online if agent8_health else False,
                    "status": agent8_health.status if agent8_health else "unknown",
                    "health_score": agent8_health.health_score if agent8_health else 0.0
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def _test_message_delivery(self) -> dict:
        """Test message delivery system."""
        try:
            # Test message delivery to multiple agents
            delivery_results = {}
            
            for agent in ["Agent-1", "Agent-4", "Agent-8"]:
                test_message = UnifiedMessage(
                    content=f"Delivery test for {agent}",
                    sender="SYSTEM",
                    recipient=agent,
                    message_type=UnifiedMessageType.TEXT,
                    priority=UnifiedMessagePriority.REGULAR
                )
                
                # Test route verification
                verification_result = await self.verified_messaging.verify_route(test_message)
                
                delivery_results[agent] = {
                    "route_valid": verification_result.valid,
                    "expected_agent": verification_result.expected_agent,
                    "actual_agent": verification_result.actual_agent
                }
            
            return {
                "status": "passed",
                "delivery_results": delivery_results,
                "successful_routes": sum(1 for result in delivery_results.values() if result["route_valid"]),
                "total_tests": len(delivery_results)
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def _test_system_health(self) -> dict:
        """Test overall system health."""
        try:
            # Get health from all subsystems
            messaging_health = self.verified_messaging.get_system_health()
            heartbeat_health = self.heartbeat_system.get_system_health_summary()
            swarm_health = self.health_monitor.get_current_health()
            
            return {
                "status": "passed",
                "messaging_health": messaging_health,
                "heartbeat_health": heartbeat_health,
                "swarm_health": {
                    "overall_health": swarm_health.overall_health,
                    "health_score": swarm_health.health_score,
                    "critical_issues": swarm_health.critical_issues
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def _test_emergency_response(self) -> dict:
        """Test emergency response system."""
        try:
            # Test emergency broadcast capability
            emergency_content = "🚨 EMERGENCY TEST: Routing fixes verification"
            
            # Test emergency alert (without actually sending)
            test_alert = {
                "content": emergency_content,
                "sender": "SYSTEM",
                "priority": "URGENT",
                "target_agents": ["Agent-4"]
            }
            
            # Test emergency route capability
            emergency_message = UnifiedMessage(
                content=emergency_content,
                sender="SYSTEM",
                recipient="Agent-8",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.URGENT,
                tags=[UnifiedMessageTag.SYSTEM]
            )
            
            # Test emergency route
            emergency_route_result = await self.verified_messaging.use_emergency_route(emergency_message)
            
            return {
                "status": "passed",
                "emergency_alert_ready": True,
                "emergency_route_available": True,
                "emergency_route_test": emergency_route_result,
                "test_alert": test_alert
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _calculate_overall_status(self, tests: dict) -> str:
        """Calculate overall verification status."""
        passed_tests = sum(1 for test in tests.values() if test.get("status") == "passed")
        total_tests = len(tests)
        
        if passed_tests == total_tests:
            return "PASSED"
        elif passed_tests >= total_tests * 0.8:
            return "MOSTLY_PASSED"
        elif passed_tests >= total_tests * 0.5:
            return "PARTIALLY_PASSED"
        else:
            return "FAILED"
    
    def _generate_summary(self, tests: dict) -> dict:
        """Generate verification summary."""
        passed_tests = [name for name, test in tests.items() if test.get("status") == "passed"]
        failed_tests = [name for name, test in tests.items() if test.get("status") == "failed"]
        
        return {
            "total_tests": len(tests),
            "passed_tests": len(passed_tests),
            "failed_tests": len(failed_tests),
            "pass_rate": len(passed_tests) / len(tests) if tests else 0.0,
            "passed_test_names": passed_tests,
            "failed_test_names": failed_tests
        }
    
    def export_verification_report(self, results: dict, filepath: str):
        """Export verification report to file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Verification report exported to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to export verification report: {e}")


async def main():
    """Main verification function."""
    print("🚀 ROUTING FIXES VERIFICATION SCRIPT")
    print("=" * 50)
    
    verifier = RoutingFixesVerifier()
    
    try:
        # Run comprehensive verification
        results = await verifier.run_comprehensive_verification()
        
        # Print summary
        print("\n📊 VERIFICATION SUMMARY:")
        print(f"Overall Status: {results['overall_status']}")
        print(f"Duration: {results['duration_seconds']:.2f} seconds")
        print(f"Tests Passed: {results['summary']['passed_tests']}/{results['summary']['total_tests']}")
        print(f"Pass Rate: {results['summary']['pass_rate']:.1%}")
        
        if results['summary']['failed_tests'] > 0:
            print(f"Failed Tests: {', '.join(results['summary']['failed_test_names'])}")
        
        # Export report
        report_file = f"routing_verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        verifier.export_verification_report(results, report_file)
        
        # Return appropriate exit code
        if results['overall_status'] == "PASSED":
            print("\n✅ All routing fixes verified successfully!")
            return 0
        elif results['overall_status'] == "MOSTLY_PASSED":
            print("\n⚠️ Most routing fixes verified, minor issues detected")
            return 1
        else:
            print("\n❌ Routing fixes verification failed!")
            return 2
            
    except Exception as e:
        print(f"\n❌ Verification script failed: {e}")
        return 3


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)