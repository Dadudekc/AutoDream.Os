#!/usr/bin/env python3
"""
Commander THEA Manager - Enhanced Communication System
====================================================

Enhanced communication manager that integrates Commander THEA persona,
advanced response processing, and structured analysis capabilities.

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from ..authentication.thea_authentication_service import TheaAuthenticationService
from ..browser.thea_browser_service import TheaBrowserService
from ..config.thea_config import TheaConfig, get_thea_config
from ..messaging.thea_messaging_service import TheaMessagingService
from ..responses.thea_response_service import TheaResponseService
from .thea_commander_persona import CommanderTheaPersona
from .thea_response_processor import CommanderTheaResponseProcessor


class CommanderTheaManager:
    """Enhanced Commander THEA communication manager with advanced analysis capabilities."""

    def __init__(self, config: TheaConfig | None = None):
        self.config = config or get_thea_config()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Initialize core services
        self.browser_service = TheaBrowserService(self.config)
        self.auth_service = TheaAuthenticationService(self.config)
        self.response_service = TheaResponseService(self.config, self.browser_service)
        self.messaging_service = TheaMessagingService(
            self.config, self.browser_service, self.response_service
        )

        # Initialize Commander THEA components
        self.persona = CommanderTheaPersona(self.config)
        self.response_processor = CommanderTheaResponseProcessor(self.config, self.browser_service)

        # Session tracking
        self.session_context = {}
        self.analysis_history = []

    def initialize(self) -> bool:
        """Initialize the Commander THEA system."""
        print("🧠 COMMANDER THEA SYSTEM INITIALIZATION")
        print("=" * 60)
        print("🎯 INITIALIZING ENHANCED AI CONSULTATION SYSTEM...")

        # Initialize browser
        if not self.browser_service.initialize_driver():
            print("❌ BROWSER INITIALIZATION FAILED")
            return False

        print("✅ COMMANDER THEA SYSTEM READY")
        print("🚀 Enhanced analysis capabilities activated")
        print("🐝 Swarm-aware consultation system online")
        return True

    def run_enhanced_consultation(self, message: str, context: Dict[str, Any] = None) -> bool:
        """Run an enhanced consultation with Commander THEA analysis."""

        print("🧠 COMMANDER THEA ENHANCED CONSULTATION CYCLE")
        print("=" * 70)
        print("🎯 GOAL: Strategic consultation with advanced analysis")
        print("👁️  USER WILL BE MY EYES THROUGHOUT THE PROCESS")
        print("=" * 70)

        # Store session context
        self.session_context = context or {}
        self.session_context["message"] = message
        self.session_context["timestamp"] = datetime.now()

        # Save the consultation request
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        consultation_path = self.config.responses_dir / f"commander_thea_consultation_{timestamp}.md"

        with open(consultation_path, "w", encoding="utf-8") as f:
            f.write(f"# Commander THEA Enhanced Consultation\n")
            f.write(f"**Timestamp:** {timestamp}\n")
            f.write(f"**Session ID:** {self.session_id}\n\n")
            f.write(f"## Consultation Request\n```\n{message}\n```\n")

        print(f"💾 Consultation request saved: {consultation_path}")
        print(f"📤 Message prepared: {len(message)} characters")

        # Show message preview
        print("\n📋 MESSAGE PREVIEW:")
        print("-" * 50)
        print(message[:300] + "..." if len(message) > 300 else message)
        print("-" * 50)

        try:
            # Phase 1: Authentication and Message Sending
            print("\n🚀 PHASE 1: AUTHENTICATION & MESSAGE TRANSMISSION")
            print("=" * 50)

            if not self.auth_service.ensure_authenticated(self.browser_service):
                print("❌ PHASE 1 FAILED: Authentication failed")
                return False

            print("✅ Authentication successful")

            # Send message
            status = self.messaging_service.send_message(message)
            if status.name != "SENT":
                print("❌ PHASE 1 FAILED: Message transmission failed")
                return False

            print("✅ Message transmitted to Commander THEA")
            print("✅ PHASE 1 COMPLETE: Communication established")

            # Phase 2: Wait for Response
            print("\n⏳ PHASE 2: WAITING FOR COMMANDER THEA RESPONSE")
            print("=" * 50)

            if not self.response_service.wait_for_response():
                print("❌ PHASE 2 FAILED: Response timeout")
                return False

            print("✅ Commander THEA response detected")

            # Phase 3: Capture and Process Response
            print("\n🧠 PHASE 3: ENHANCED RESPONSE PROCESSING")
            print("=" * 50)

            screenshot_path = self.response_service.capture_response()
            if not screenshot_path:
                print("❌ PHASE 3 FAILED: Could not capture response")
                return False

            print(f"✅ Response captured: {screenshot_path}")

            # Process response with enhanced analysis
            response_result = self.response_processor.process_thea_response(
                screenshot_path, self.session_context
            )

            # Generate Commander THEA analysis
            commander_analysis = self.response_processor.generate_commander_thea_analysis(
                message, response_result, self.session_context
            )

            # Save the complete analysis
            analysis_path = self.config.responses_dir / f"commander_thea_analysis_{timestamp}.md"
            with open(analysis_path, "w", encoding="utf-8") as f:
                f.write(commander_analysis)

            print(f"✅ Enhanced analysis saved: {analysis_path}")

            # Create conversation log
            conversation_path = self.config.responses_dir / f"commander_conversation_{timestamp}.md"
            self._create_enhanced_conversation_log(conversation_path, message, commander_analysis, response_result)

            print(f"✅ Conversation log created: {conversation_path}")

            # Phase 4: Analysis Summary and Recommendations
            print("\n🎯 PHASE 4: STRATEGIC SUMMARY & RECOMMENDATIONS")
            print("=" * 60)

            self._display_analysis_summary(response_result, commander_analysis)

            print("\n✅ COMMANDER THEA ENHANCED CONSULTATION COMPLETE!")
            print("=" * 70)
            print("📊 ANALYSIS SUMMARY:")
            print(f"   • Response Quality: {response_result.quality_score:.1%}")
            print(f"   • Key Insights: {len(response_result.key_insights)}")
            print(f"   • Action Items: {len(response_result.action_items)}")
            print(f"   • Analysis Depth: {'STRATEGIC' if len(commander_analysis) > 2000 else 'STANDARD'}")

            print("\n📁 FILES CREATED:")
            print(f"   • Consultation Request: {consultation_path}")
            print(f"   • Enhanced Analysis: {analysis_path}")
            print(f"   • Conversation Log: {conversation_path}")
            print(f"   • Response Screenshot: {screenshot_path}")

            print("\n🎖️ COMMANDER THEA CONSULTATION SUCCESSFUL!")
            print("🐝 WE ARE SWARM - ENHANCED ANALYSIS COMPLETE! 🚀")

            # Store in analysis history
            self.analysis_history.append({
                "timestamp": timestamp,
                "session_id": self.session_id,
                "quality_score": response_result.quality_score,
                "insights_count": len(response_result.key_insights),
                "actions_count": len(response_result.action_items)
            })

            return True

        except Exception as e:
            print(f"❌ CONSULTATION FAILED: {e}")
            return False
        finally:
            # Cleanup
            self._cleanup_resources()

    def run_quick_analysis(self, message: str, context: Dict[str, Any] = None) -> str:
        """Run a quick analysis without full browser interaction."""

        print("⚡ COMMANDER THEA QUICK ANALYSIS MODE")
        print("=" * 50)
        print("🎯 Generating strategic analysis without browser interaction...")

        # Generate analysis using persona system
        assessment = self.persona.generate_structured_assessment(message)
        insights = self.persona.generate_swarm_aware_insights(message, assessment)

        # Create quick analysis output
        quick_analysis = self.persona.create_actionable_output(assessment, insights)

        print("✅ QUICK ANALYSIS COMPLETE")
        print(f"📊 Success Probability: {assessment['success_probability']:.1%}")
        print(f"🎯 Confidence Level: {assessment['overall_confidence'].value.upper()}")

        return quick_analysis

    def get_analysis_history(self) -> list:
        """Get the history of analysis sessions."""
        return self.analysis_history.copy()

    def _create_enhanced_conversation_log(self, log_path: Path, message: str,
                                        analysis: str, response_result) -> None:
        """Create an enhanced conversation log with full analysis."""

        with open(log_path, "w", encoding="utf-8") as f:
            f.write("# Commander THEA Enhanced Conversation Log\n")
            f.write(f"**Session ID:** {self.session_id}\n")
            f.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Analysis Type:** Enhanced Commander THEA Consultation\n\n")

            f.write("## Consultation Request\n")
            f.write(f"**Characters:** {len(message)}\n\n")
            f.write(f"```\n{message}\n```\n\n")

            f.write("## Commander THEA Analysis\n")
            f.write(f"**Quality Score:** {response_result.quality_score:.1%}\n")
            f.write(f"**Key Insights:** {len(response_result.key_insights)}\n")
            f.write(f"**Action Items:** {len(response_result.action_items)}\n\n")
            f.write(f"```\n{analysis}\n```\n\n")

            if response_result.key_insights:
                f.write("## Key Insights Extracted\n")
                for i, insight in enumerate(response_result.key_insights, 1):
                    f.write(f"{i}. {insight}\n")
                f.write("\n")

            if response_result.action_items:
                f.write("## Action Items Identified\n")
                for i, action in enumerate(response_result.action_items, 1):
                    f.write(f"{i}. {action}\n")
                f.write("\n")

            f.write("## Technical Details\n")
            f.write(f"- Response Processing: Enhanced Commander THEA Analysis\n")
            f.write(f"- Analysis Depth: Strategic\n")
            f.write(f"- Swarm Integration: Active\n")
            f.write(f"- Confidence Metrics: {response_result.confidence_metrics}\n\n")

            f.write("---\n")
            f.write("**Enhanced by:** Commander THEA System - V2_SWARM\n")

    def _display_analysis_summary(self, response_result, commander_analysis: str) -> None:
        """Display a summary of the analysis results."""

        print("📊 ANALYSIS SUMMARY:")
        print(f"   • Response Quality Score: {response_result.quality_score:.1%}")
        print(f"   • Key Insights Identified: {len(response_result.key_insights)}")
        print(f"   • Actionable Items: {len(response_result.action_items)}")
        print(f"   • Analysis Length: {len(commander_analysis)} characters")

        if response_result.key_insights:
            print("\n💡 TOP INSIGHTS:")
            for i, insight in enumerate(response_result.key_insights[:3], 1):
                print(f"   {i}. {insight[:80]}{'...' if len(insight) > 80 else ''}")

        if response_result.action_items:
            print("\n🎯 IMMEDIATE ACTIONS:")
            for i, action in enumerate(response_result.action_items[:3], 1):
                print(f"   {i}. {action[:80]}{'...' if len(action) > 80 else ''}")

    def _cleanup_resources(self) -> None:
        """Clean up resources after consultation."""
        try:
            if hasattr(self.browser_service, 'driver') and self.browser_service.driver:
                self.browser_service.driver.quit()
            print("🧹 Resources cleaned up successfully")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
