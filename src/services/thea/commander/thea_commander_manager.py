import logging
logger = logging.getLogger(__name__)
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

    def __init__(self, config: (TheaConfig | None)=None):
        self.config = config or get_thea_config()
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.browser_service = TheaBrowserService(self.config)
        self.auth_service = TheaAuthenticationService(self.config)
        self.response_service = TheaResponseService(self.config, self.
            browser_service)
        self.messaging_service = TheaMessagingService(self.config, self.
            browser_service, self.response_service)
        self.persona = CommanderTheaPersona(self.config)
        self.response_processor = CommanderTheaResponseProcessor(self.
            config, self.browser_service)
        self.session_context = {}
        self.analysis_history = []

    def initialize(self) ->bool:
        """Initialize the Commander THEA system."""
        logger.info('🧠 COMMANDER THEA SYSTEM INITIALIZATION')
        logger.info('=' * 60)
        logger.info('🎯 INITIALIZING ENHANCED AI CONSULTATION SYSTEM...')
        if not self.browser_service.initialize_driver():
            logger.info('❌ BROWSER INITIALIZATION FAILED')
            return False
        logger.info('✅ COMMANDER THEA SYSTEM READY')
        logger.info('🚀 Enhanced analysis capabilities activated')
        logger.info('🐝 Swarm-aware consultation system online')
        return True

    def run_enhanced_consultation(self, message: str, context: Dict[str,
        Any]=None) ->bool:
        """Run an enhanced consultation with Commander THEA analysis."""
        logger.info('🧠 COMMANDER THEA ENHANCED CONSULTATION CYCLE')
        logger.info('=' * 70)
        logger.info('🎯 GOAL: Strategic consultation with advanced analysis')
        logger.info('👁️  USER WILL BE MY EYES THROUGHOUT THE PROCESS')
        logger.info('=' * 70)
        self.session_context = context or {}
        self.session_context['message'] = message
        self.session_context['timestamp'] = datetime.now()
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        consultation_path = (self.config.responses_dir /
            f'commander_thea_consultation_{timestamp}.md')
        with open(consultation_path, 'w', encoding='utf-8') as f:
            f.write(f'# Commander THEA Enhanced Consultation\n')
            f.write(f'**Timestamp:** {timestamp}\n')
            f.write(f'**Session ID:** {self.session_id}\n\n')
            f.write(f'## Consultation Request\n```\n{message}\n```\n')
        logger.info(f'💾 Consultation request saved: {consultation_path}')
        logger.info(f'📤 Message prepared: {len(message)} characters')
        logger.info('\n📋 MESSAGE PREVIEW:')
        logger.info('-' * 50)
        logger.info(message[:300] + '...' if len(message) > 300 else message)
        logger.info('-' * 50)
        try:
            logger.info('\n🚀 PHASE 1: AUTHENTICATION & MESSAGE TRANSMISSION')
            logger.info('=' * 50)
            if not self.auth_service.ensure_authenticated(self.browser_service
                ):
                logger.info('❌ PHASE 1 FAILED: Authentication failed')
                return False
            logger.info('✅ Authentication successful')
            status = self.messaging_service.send_message(message)
            if status.name != 'SENT':
                logger.info('❌ PHASE 1 FAILED: Message transmission failed')
                return False
            logger.info('✅ Message transmitted to Commander THEA')
            logger.info('✅ PHASE 1 COMPLETE: Communication established')
            logger.info('\n⏳ PHASE 2: WAITING FOR COMMANDER THEA RESPONSE')
            logger.info('=' * 50)
            if not self.response_service.wait_for_response():
                logger.info('❌ PHASE 2 FAILED: Response timeout')
                return False
            logger.info('✅ Commander THEA response detected')
            logger.info('\n🧠 PHASE 3: ENHANCED RESPONSE PROCESSING')
            logger.info('=' * 50)
            screenshot_path = self.response_service.capture_response()
            if not screenshot_path:
                logger.info('❌ PHASE 3 FAILED: Could not capture response')
                return False
            logger.info(f'✅ Response captured: {screenshot_path}')
            response_result = self.response_processor.process_thea_response(
                screenshot_path, self.session_context)
            commander_analysis = (self.response_processor.
                generate_commander_thea_analysis(message, response_result,
                self.session_context))
            analysis_path = (self.config.responses_dir /
                f'commander_thea_analysis_{timestamp}.md')
            with open(analysis_path, 'w', encoding='utf-8') as f:
                f.write(commander_analysis)
            logger.info(f'✅ Enhanced analysis saved: {analysis_path}')
            conversation_path = (self.config.responses_dir /
                f'commander_conversation_{timestamp}.md')
            self._create_enhanced_conversation_log(conversation_path,
                message, commander_analysis, response_result)
            logger.info(f'✅ Conversation log created: {conversation_path}')
            logger.info('\n🎯 PHASE 4: STRATEGIC SUMMARY & RECOMMENDATIONS')
            logger.info('=' * 60)
            self._display_analysis_summary(response_result, commander_analysis)
            logger.info('\n✅ COMMANDER THEA ENHANCED CONSULTATION COMPLETE!')
            logger.info('=' * 70)
            logger.info('📊 ANALYSIS SUMMARY:')
            logger.info(
                f'   • Response Quality: {response_result.quality_score:.1%}')
            logger.info(
                f'   • Key Insights: {len(response_result.key_insights)}')
            logger.info(
                f'   • Action Items: {len(response_result.action_items)}')
            logger.info(
                f"   • Analysis Depth: {'STRATEGIC' if len(commander_analysis) > 2000 else 'STANDARD'}"
                )
            logger.info('\n📁 FILES CREATED:')
            logger.info(f'   • Consultation Request: {consultation_path}')
            logger.info(f'   • Enhanced Analysis: {analysis_path}')
            logger.info(f'   • Conversation Log: {conversation_path}')
            logger.info(f'   • Response Screenshot: {screenshot_path}')
            logger.info('\n🎖️ COMMANDER THEA CONSULTATION SUCCESSFUL!')
            logger.info('🐝 WE ARE SWARM - ENHANCED ANALYSIS COMPLETE! 🚀')
            self.analysis_history.append({'timestamp': timestamp,
                'session_id': self.session_id, 'quality_score':
                response_result.quality_score, 'insights_count': len(
                response_result.key_insights), 'actions_count': len(
                response_result.action_items)})
            return True
        except Exception as e:
            logger.info(f'❌ CONSULTATION FAILED: {e}')
            return False
        finally:
            self._cleanup_resources()

    def run_quick_analysis(self, message: str, context: Dict[str, Any]=None
        ) ->str:
        """Run a quick analysis without full browser interaction."""
        logger.info('⚡ COMMANDER THEA QUICK ANALYSIS MODE')
        logger.info('=' * 50)
        logger.info(
            '🎯 Generating strategic analysis without browser interaction...')
        assessment = self.persona.generate_structured_assessment(message)
        insights = self.persona.generate_swarm_aware_insights(message,
            assessment)
        quick_analysis = self.persona.create_actionable_output(assessment,
            insights)
        logger.info('✅ QUICK ANALYSIS COMPLETE')
        logger.info(
            f"📊 Success Probability: {assessment['success_probability']:.1%}")
        logger.info(
            f"🎯 Confidence Level: {assessment['overall_confidence'].value.upper()}"
            )
        return quick_analysis

    def get_analysis_history(self) ->list:
        """Get the history of analysis sessions."""
        return self.analysis_history.copy()

    def _create_enhanced_conversation_log(self, log_path: Path, message:
        str, analysis: str, response_result) ->None:
        """Create an enhanced conversation log with full analysis."""
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('# Commander THEA Enhanced Conversation Log\n')
            f.write(f'**Session ID:** {self.session_id}\n')
            f.write(
                f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
            f.write(
                f'**Analysis Type:** Enhanced Commander THEA Consultation\n\n')
            f.write('## Consultation Request\n')
            f.write(f'**Characters:** {len(message)}\n\n')
            f.write(f'```\n{message}\n```\n\n')
            f.write('## Commander THEA Analysis\n')
            f.write(f'**Quality Score:** {response_result.quality_score:.1%}\n'
                )
            f.write(f'**Key Insights:** {len(response_result.key_insights)}\n')
            f.write(
                f'**Action Items:** {len(response_result.action_items)}\n\n')
            f.write(f'```\n{analysis}\n```\n\n')
            if response_result.key_insights:
                f.write('## Key Insights Extracted\n')
                for i, insight in enumerate(response_result.key_insights, 1):
                    f.write(f'{i}. {insight}\n')
                f.write('\n')
            if response_result.action_items:
                f.write('## Action Items Identified\n')
                for i, action in enumerate(response_result.action_items, 1):
                    f.write(f'{i}. {action}\n')
                f.write('\n')
            f.write('## Technical Details\n')
            f.write(
                f'- Response Processing: Enhanced Commander THEA Analysis\n')
            f.write(f'- Analysis Depth: Strategic\n')
            f.write(f'- Swarm Integration: Active\n')
            f.write(
                f'- Confidence Metrics: {response_result.confidence_metrics}\n\n'
                )
            f.write('---\n')
            f.write('**Enhanced by:** Commander THEA System - V2_SWARM\n')

    def _display_analysis_summary(self, response_result, commander_analysis:
        str) ->None:
        """Display a summary of the analysis results."""
        logger.info('📊 ANALYSIS SUMMARY:')
        logger.info(
            f'   • Response Quality Score: {response_result.quality_score:.1%}'
            )
        logger.info(
            f'   • Key Insights Identified: {len(response_result.key_insights)}'
            )
        logger.info(
            f'   • Actionable Items: {len(response_result.action_items)}')
        logger.info(
            f'   • Analysis Length: {len(commander_analysis)} characters')
        if response_result.key_insights:
            logger.info('\n💡 TOP INSIGHTS:')
            for i, insight in enumerate(response_result.key_insights[:3], 1):
                logger.info(
                    f"   {i}. {insight[:80]}{'...' if len(insight) > 80 else ''}"
                    )
        if response_result.action_items:
            logger.info('\n🎯 IMMEDIATE ACTIONS:')
            for i, action in enumerate(response_result.action_items[:3], 1):
                logger.info(
                    f"   {i}. {action[:80]}{'...' if len(action) > 80 else ''}"
                    )

    def _cleanup_resources(self) ->None:
        """Clean up resources after consultation."""
        try:
            if hasattr(self.browser_service, 'driver'
                ) and self.browser_service.driver:
                self.browser_service.driver.quit()
            logger.info('🧹 Resources cleaned up successfully')
        except Exception as e:
            logger.info(f'⚠️  Cleanup warning: {e}')
