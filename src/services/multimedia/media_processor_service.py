#!/usr/bin/env python3
"""
Media Processor Service
Central coordinator for all multimedia operations and real-time processing
"""

import logging
import threading
import time

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, Optional, Callable, List
from pathlib import Path
import json

from .video_capture_service import VideoCaptureService
from .audio_processing_service import AudioProcessingService

logger = logging.getLogger(__name__)


class MediaProcessorService:
    """
    Central multimedia processing coordinator
    Manages video capture, audio processing, and real-time effects
    """

    def __init__(self):
        self.video_service = VideoCaptureService()
        self.audio_service = AudioProcessingService()
        self.processing_pipelines = {}
        self.effect_chains = {}
        self.media_config = {
            "sync_video_audio": True,
            "max_processing_threads": 8,
            "buffer_size": 1000,
            "quality_preset": "high",
        }
        self.is_processing = False

    def start_multimedia_pipeline(
        self, pipeline_name: str, config: Dict[str, Any]
    ) -> bool:
        """
        Start a complete multimedia processing pipeline

        Args:
            pipeline_name: Name of the pipeline
            config: Pipeline configuration

        Returns:
            bool: True if pipeline started successfully
        """
        try:
            if pipeline_name in self.processing_pipelines:
                logger.warning(f"Pipeline {pipeline_name} already running")
                return False

            # Validate configuration
            if not self._validate_pipeline_config(config):
                logger.error(f"Invalid pipeline configuration for {pipeline_name}")
                return False

            # Start video capture if configured
            video_started = False
            if config.get("enable_video", False):
                video_config = config.get("video", {})
                device_id = video_config.get("device_id", 0)
                callback = self._create_video_callback(pipeline_name, config)
                video_started = self.video_service.start_webcam_capture(
                    device_id, callback
                )

                if not video_started:
                    logger.error(
                        f"Failed to start video capture for pipeline {pipeline_name}"
                    )
                    return False

            # Start audio capture if configured
            audio_started = False
            if config.get("enable_audio", False):
                audio_config = config.get("audio", {})
                device_id = audio_config.get("device_id", 0)
                callback = self._create_audio_callback(pipeline_name, config)
                audio_started = self.audio_service.start_audio_capture(
                    device_id, callback
                )

                if not audio_started:
                    logger.error(
                        f"Failed to start audio capture for pipeline {pipeline_name}"
                    )
                    return False

            # Create processing pipeline
            self.processing_pipelines[pipeline_name] = {
                "config": config,
                "video_active": video_started,
                "audio_active": audio_started,
                "start_time": time.time(),
                "frames_processed": 0,
                "audio_chunks_processed": 0,
            }

            self.is_processing = True
            logger.info(f"Multimedia pipeline {pipeline_name} started successfully")
            return True

        except Exception as e:
            logger.error(f"Error starting multimedia pipeline {pipeline_name}: {e}")
            return False

    def _validate_pipeline_config(self, config: Dict[str, Any]) -> bool:
        """Validate pipeline configuration"""
        required_fields = ["name", "type"]

        for field in required_fields:
            if field not in config:
                logger.error(f"Missing required field: {field}")
                return False

        # Validate video configuration if enabled
        if config.get("enable_video", False):
            video_config = config.get("video", {})
            if "device_id" not in video_config:
                logger.error("Video enabled but device_id not specified")
                return False

        # Validate audio configuration if enabled
        if config.get("enable_audio", False):
            audio_config = config.get("audio", {})
            if "device_id" not in audio_config:
                logger.error("Audio enabled but device_id not specified")
                return False

        return True

    def _create_video_callback(
        self, pipeline_name: str, config: Dict[str, Any]
    ) -> Callable:
        """Create video processing callback for pipeline"""

        def video_callback(frame):
            try:
                # Apply video effects if configured
                effects = config.get("video_effects", [])
                processed_frame = frame

                for effect in effects:
                    effect_type = effect.get("type")
                    effect_params = effect.get("params", {})

                    if effect_type and hasattr(self.video_service, "apply_filter"):
                        processed_frame = self.video_service.apply_filter(
                            processed_frame, effect_type, **effect_params
                        )

                # Update pipeline statistics
                if pipeline_name in self.processing_pipelines:
                    self.processing_pipelines[pipeline_name]["frames_processed"] += 1

                return processed_frame

            except Exception as e:
                logger.error(f"Video callback error in pipeline {pipeline_name}: {e}")
                return frame

        return video_callback

    def _create_audio_callback(
        self, pipeline_name: str, config: Dict[str, Any]
    ) -> Callable:
        """Create audio processing callback for pipeline"""

        def audio_callback(audio_data):
            try:
                # Apply audio effects if configured
                effects = config.get("audio_effects", [])
                processed_audio = audio_data

                for effect in effects:
                    effect_type = effect.get("type")
                    effect_params = effect.get("params", {})

                    if effect_type and hasattr(
                        self.audio_service, "apply_audio_filter"
                    ):
                        processed_audio = self.audio_service.apply_audio_filter(
                            processed_audio, effect_type, **effect_params
                        )

                # Update pipeline statistics
                if pipeline_name in self.processing_pipelines:
                    self.processing_pipelines[pipeline_name][
                        "audio_chunks_processed"
                    ] += 1

                return processed_audio

            except Exception as e:
                logger.error(f"Audio callback error in pipeline {pipeline_name}: {e}")
                return audio_data

        return audio_callback

    def stop_multimedia_pipeline(self, pipeline_name: str) -> bool:
        """
        Stop a multimedia processing pipeline

        Args:
            pipeline_name: Name of the pipeline to stop

        Returns:
            bool: True if pipeline stopped successfully
        """
        try:
            if pipeline_name not in self.processing_pipelines:
                logger.warning(f"Pipeline {pipeline_name} not found")
                return False

            pipeline = self.processing_pipelines[pipeline_name]

            # Stop video capture if active
            if pipeline["video_active"]:
                video_config = pipeline["config"].get("video", {})
                device_id = video_config.get("device_id", 0)
                self.video_service.stop_capture(device_id)

            # Stop audio capture if active
            if pipeline["audio_active"]:
                audio_config = pipeline["config"].get("audio", {})
                device_id = audio_config.get("device_id", 0)
                self.audio_service.stop_audio(device_id)

            # Remove pipeline
            del self.processing_pipelines[pipeline_name]

            # Check if any pipelines are still running
            if not self.processing_pipelines:
                self.is_processing = False

            logger.info(f"Multimedia pipeline {pipeline_name} stopped successfully")
            return True

        except Exception as e:
            logger.error(f"Error stopping multimedia pipeline {pipeline_name}: {e}")
            return False

    def create_effect_chain(
        self, chain_name: str, effects: List[Dict[str, Any]]
    ) -> bool:
        """
        Create a reusable effect chain for multimedia processing

        Args:
            chain_name: Name of the effect chain
            effects: List of effect configurations

        Returns:
            bool: True if effect chain created successfully
        """
        try:
            if chain_name in self.effect_chains:
                logger.warning(f"Effect chain {chain_name} already exists")
                return False

            # Validate effects
            for effect in effects:
                if "type" not in effect:
                    logger.error(f"Effect missing type: {effect}")
                    return False

            self.effect_chains[chain_name] = {
                "effects": effects,
                "created_time": time.time(),
                "usage_count": 0,
            }

            logger.info(f"Effect chain {chain_name} created successfully")
            return True

        except Exception as e:
            logger.error(f"Error creating effect chain {chain_name}: {e}")
            return False

    def apply_effect_chain(
        self, chain_name: str, media_data: Any, media_type: str
    ) -> Any:
        """
        Apply an effect chain to media data

        Args:
            chain_name: Name of the effect chain
            media_data: Media data to process
            media_type: Type of media ('video' or 'audio')

        Returns:
            Processed media data
        """
        try:
            if chain_name not in self.effect_chains:
                logger.error(f"Effect chain {chain_name} not found")
                return media_data

            chain = self.effect_chains[chain_name]
            processed_data = media_data

            # Apply each effect in the chain
            for effect in chain["effects"]:
                effect_type = effect["type"]
                effect_params = effect.get("params", {})

                if media_type == "video":
                    if hasattr(self.video_service, "apply_filter"):
                        processed_data = self.video_service.apply_filter(
                            processed_data, effect_type, **effect_params
                        )
                elif media_type == "audio":
                    if hasattr(self.audio_service, "apply_audio_filter"):
                        processed_data = self.audio_service.apply_audio_filter(
                            processed_data, effect_type, **effect_params
                        )

            # Update usage count
            chain["usage_count"] += 1

            return processed_data

        except Exception as e:
            logger.error(f"Error applying effect chain {chain_name}: {e}")
            return media_data

    def get_pipeline_status(
        self, pipeline_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get status of multimedia pipelines

        Args:
            pipeline_name: Specific pipeline name or None for all

        Returns:
            Dict containing pipeline status information
        """
        try:
            if pipeline_name:
                if pipeline_name in self.processing_pipelines:
                    pipeline = self.processing_pipelines[pipeline_name]
                    return {
                        "name": pipeline_name,
                        "status": "active"
                        if pipeline["video_active"] or pipeline["audio_active"]
                        else "inactive",
                        "uptime": time.time() - pipeline["start_time"],
                        "frames_processed": pipeline["frames_processed"],
                        "audio_chunks_processed": pipeline["audio_chunks_processed"],
                        "config": pipeline["config"],
                    }
                else:
                    return {"error": f"Pipeline {pipeline_name} not found"}
            else:
                # Return all pipeline statuses
                statuses = {}
                for name, pipeline in self.processing_pipelines.items():
                    statuses[name] = {
                        "status": "active"
                        if pipeline["video_active"] or pipeline["audio_active"]
                        else "inactive",
                        "uptime": time.time() - pipeline["start_time"],
                        "frames_processed": pipeline["frames_processed"],
                        "audio_chunks_processed": pipeline["audio_chunks_processed"],
                    }

                return {
                    "total_pipelines": len(statuses),
                    "active_pipelines": sum(
                        1 for s in statuses.values() if s["status"] == "active"
                    ),
                    "pipelines": statuses,
                }

        except Exception as e:
            logger.error(f"Error getting pipeline status: {e}")
            return {"error": str(e)}

    def get_system_status(self) -> Dict[str, Any]:
        """
        Get overall multimedia system status

        Returns:
            Dict containing system status information
        """
        try:
            video_status = self.video_service.get_capture_status()
            audio_status = self.audio_service.get_audio_status()

            return {
                "system_status": "active" if self.is_processing else "inactive",
                "total_pipelines": len(self.processing_pipelines),
                "effect_chains": len(self.effect_chains),
                "video_service": video_status,
                "audio_service": audio_status,
                "config": self.media_config.copy(),
            }

        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}

    def save_pipeline_config(self, pipeline_name: str, filepath: str) -> bool:
        """
        Save pipeline configuration to file

        Args:
            pipeline_name: Name of the pipeline
            filepath: Output file path

        Returns:
            bool: True if saved successfully
        """
        try:
            if pipeline_name not in self.processing_pipelines:
                logger.error(f"Pipeline {pipeline_name} not found")
                return False

            pipeline = self.processing_pipelines[pipeline_name]
            config_data = {
                "name": pipeline_name,
                "config": pipeline["config"],
                "created_time": pipeline["start_time"],
                "statistics": {
                    "frames_processed": pipeline["frames_processed"],
                    "audio_chunks_processed": pipeline["audio_chunks_processed"],
                },
            }

            Path(filepath).parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, "w") as f:
                json.dump(config_data, f, indent=2)

            logger.info(f"Pipeline configuration saved to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error saving pipeline configuration: {e}")
            return False

    def load_pipeline_config(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Load pipeline configuration from file

        Args:
            filepath: Input file path

        Returns:
            Dict containing pipeline configuration or None if failed
        """
        try:
            with open(filepath, "r") as f:
                config_data = json.load(f)

            logger.info(f"Pipeline configuration loaded from {filepath}")
            return config_data

        except Exception as e:
            logger.error(f"Error loading pipeline configuration: {e}")
            return None
