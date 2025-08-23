#!/usr/bin/env python3
"""
Audio Processing Service
Real-time audio capture and processing with threading support
"""

import threading
import time
import logging
import wave
import numpy as np
from typing import Optional, Callable, Dict, Any, List
from pathlib import Path
import queue

logger = logging.getLogger(__name__)


class AudioProcessingService:
    """
    High-performance audio processing service with threading support
    Supports real-time audio capture, processing, and effects
    """

    def __init__(self):
        self.audio_threads = {}
        self.is_processing = False
        self.audio_buffers = {}
        self.audio_config = {
            "sample_rate": 44100,
            "channels": 2,
            "chunk_size": 1024,
            "format": "int16",
            "buffer_size": 1000,
        }
        self.audio_queues = {}

    def start_audio_capture(
        self, device_id: int = 0, callback: Optional[Callable] = None
    ) -> bool:
        """
        Start audio capture with threading support

        Args:
            device_id: Audio device ID (default: 0)
            callback: Audio processing callback function

        Returns:
            bool: True if capture started successfully
        """
        try:
            if device_id in self.audio_threads:
                logger.warning(f"Audio capture already running on device {device_id}")
                return False

            # Initialize audio capture
            try:
                import pyaudio

                audio = pyaudio.PyAudio()

                # Open audio stream
                stream = audio.open(
                    format=audio.get_format_from_width(2),  # 16-bit
                    channels=self.audio_config["channels"],
                    rate=self.audio_config["sample_rate"],
                    input=True,
                    input_device_index=device_id,
                    frames_per_buffer=self.audio_config["chunk_size"],
                )

            except ImportError:
                logger.error("PyAudio not available for audio capture")
                return False
            except Exception as e:
                logger.error(f"Failed to initialize audio device {device_id}: {e}")
                return False

            # Initialize audio buffer and queue
            self.audio_buffers[device_id] = []
            self.audio_queues[device_id] = queue.Queue(
                maxsize=self.audio_config["buffer_size"]
            )

            # Start capture thread
            self.is_processing = True
            capture_thread = threading.Thread(
                target=self._audio_capture_loop,
                args=(stream, device_id, callback, audio),
                daemon=True,
            )
            capture_thread.start()

            self.audio_threads[device_id] = {
                "thread": capture_thread,
                "stream": stream,
                "audio": audio,
                "active": True,
            }

            logger.info(f"Audio capture started on device {device_id}")
            return True

        except Exception as e:
            logger.error(f"Error starting audio capture: {e}")
            return False

    def _audio_capture_loop(
        self, stream, device_id: int, callback: Optional[Callable], audio
    ):
        """Internal audio capture loop with threading"""
        try:
            while self.is_processing and self.audio_threads[device_id]["active"]:
                try:
                    # Read audio data
                    data = stream.read(self.audio_config["chunk_size"])

                    # Convert to numpy array
                    audio_data = np.frombuffer(data, dtype=np.int16)

                    # Process audio if callback provided
                    if callback:
                        try:
                            processed_audio = callback(audio_data)
                            if processed_audio is not None:
                                audio_data = processed_audio
                        except Exception as e:
                            logger.error(f"Audio callback error: {e}")

                    # Store in buffer and queue
                    self.audio_buffers[device_id].append(audio_data)
                    if (
                        len(self.audio_buffers[device_id])
                        > self.audio_config["buffer_size"]
                    ):
                        self.audio_buffers[device_id].pop(0)

                    # Add to queue for real-time access
                    try:
                        self.audio_queues[device_id].put_nowait(audio_data)
                    except queue.Full:
                        # Remove oldest item if queue is full
                        try:
                            self.audio_queues[device_id].get_nowait()
                            self.audio_queues[device_id].put_nowait(audio_data)
                        except queue.Empty:
                            pass

                except Exception as e:
                    logger.error(f"Audio read error: {e}")
                    break

        except Exception as e:
            logger.error(f"Audio capture loop error: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            if device_id in self.audio_threads:
                self.audio_threads[device_id]["active"] = False

    def start_audio_playback(self, audio_data: np.ndarray, device_id: int = 0) -> bool:
        """
        Start audio playback with threading support

        Args:
            audio_data: Audio data to play
            device_id: Audio output device ID

        Returns:
            bool: True if playback started successfully
        """
        try:
            try:
                import pyaudio

                audio = pyaudio.PyAudio()

                # Open audio output stream
                stream = audio.open(
                    format=audio.get_format_from_width(2),  # 16-bit
                    channels=self.audio_config["channels"],
                    rate=self.audio_config["sample_rate"],
                    output=True,
                    output_device_index=device_id,
                    frames_per_buffer=self.audio_config["chunk_size"],
                )

            except ImportError:
                logger.error("PyAudio not available for audio playback")
                return False

            # Start playback thread
            playback_thread = threading.Thread(
                target=self._audio_playback_loop,
                args=(stream, audio_data, audio),
                daemon=True,
            )
            playback_thread.start()

            self.audio_threads[f"playback_{device_id}"] = {
                "thread": playback_thread,
                "stream": stream,
                "audio": audio,
                "active": True,
            }

            logger.info(f"Audio playback started on device {device_id}")
            return True

        except Exception as e:
            logger.error(f"Error starting audio playback: {e}")
            return False

    def _audio_playback_loop(self, stream, audio_data: np.ndarray, audio):
        """Internal audio playback loop with threading"""
        try:
            # Convert numpy array to bytes
            audio_bytes = audio_data.astype(np.int16).tobytes()

            # Play audio in chunks
            chunk_size = (
                self.audio_config["chunk_size"] * self.audio_config["channels"] * 2
            )  # 2 bytes per sample

            for i in range(0, len(audio_bytes), chunk_size):
                chunk = audio_bytes[i : i + chunk_size]
                if chunk:
                    stream.write(chunk)

        except Exception as e:
            logger.error(f"Audio playback error: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

    def stop_audio(self, device_id: Optional[int] = None) -> bool:
        """
        Stop audio capture/playback

        Args:
            device_id: Specific device to stop, or None for all

        Returns:
            bool: True if stopped successfully
        """
        try:
            if device_id is not None:
                if device_id in self.audio_threads:
                    self.audio_threads[device_id]["active"] = False
                    self.audio_threads[device_id]["stream"].stop_stream()
                    del self.audio_threads[device_id]
                    logger.info(f"Audio stopped on device {device_id}")
                    return True
                return False
            else:
                # Stop all audio
                self.is_processing = False
                for dev_id, audio_info in list(self.audio_threads.items()):
                    audio_info["active"] = False
                    if "stream" in audio_info:
                        audio_info["stream"].stop_stream()
                    del self.audio_threads[dev_id]

                logger.info("All audio stopped")
                return True

        except Exception as e:
            logger.error(f"Error stopping audio: {e}")
            return False

    def get_audio_data(self, device_id: int = 0) -> Optional[np.ndarray]:
        """
        Get current audio data from specified device

        Args:
            device_id: Audio device ID

        Returns:
            np.ndarray: Current audio data or None if not available
        """
        if device_id in self.audio_queues:
            try:
                return self.audio_queues[device_id].get_nowait()
            except queue.Empty:
                return None
        return None

    def apply_audio_filter(
        self, audio_data: np.ndarray, filter_type: str, **kwargs
    ) -> np.ndarray:
        """
        Apply real-time audio filter

        Args:
            audio_data: Input audio data
            filter_type: Type of filter to apply
            **kwargs: Filter-specific parameters

        Returns:
            np.ndarray: Filtered audio data
        """
        try:
            if filter_type == "normalize":
                # Normalize audio levels
                max_val = np.max(np.abs(audio_data))
                if max_val > 0:
                    return audio_data * (32767 / max_val)
                return audio_data

            elif filter_type == "low_pass":
                # Simple low-pass filter
                cutoff = kwargs.get("cutoff", 1000)
                from scipy import signal

                b, a = signal.butter(
                    4, cutoff / (self.audio_config["sample_rate"] / 2), "low"
                )
                return signal.filtfilt(b, a, audio_data)

            elif filter_type == "high_pass":
                # Simple high-pass filter
                cutoff = kwargs.get("cutoff", 1000)
                from scipy import signal

                b, a = signal.butter(
                    4, cutoff / (self.audio_config["sample_rate"] / 2), "high"
                )
                return signal.filtfilt(b, a, audio_data)

            elif filter_type == "echo":
                # Simple echo effect
                delay_samples = kwargs.get(
                    "delay", int(self.audio_config["sample_rate"] * 0.1)
                )
                decay = kwargs.get("decay", 0.5)

                if len(audio_data) > delay_samples:
                    echo_data = np.zeros_like(audio_data)
                    echo_data[delay_samples:] = audio_data[:-delay_samples] * decay
                    return audio_data + echo_data
                return audio_data

            else:
                logger.warning(f"Unknown audio filter type: {filter_type}")
                return audio_data

        except Exception as e:
            logger.error(f"Audio filter application error: {e}")
            return audio_data

    def save_audio(self, audio_data: np.ndarray, filepath: str) -> bool:
        """
        Save audio data to WAV file

        Args:
            audio_data: Audio data to save
            filepath: Output file path

        Returns:
            bool: True if saved successfully
        """
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)

            with wave.open(filepath, "wb") as wav_file:
                wav_file.setnchannels(self.audio_config["channels"])
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.audio_config["sample_rate"])
                wav_file.writeframes(audio_data.astype(np.int16).tobytes())

            return True

        except Exception as e:
            logger.error(f"Error saving audio: {e}")
            return False

    def load_audio(self, filepath: str) -> Optional[np.ndarray]:
        """
        Load audio data from WAV file

        Args:
            filepath: Input file path

        Returns:
            np.ndarray: Loaded audio data or None if failed
        """
        try:
            with wave.open(filepath, "rb") as wav_file:
                # Read audio data
                frames = wav_file.readframes(wav_file.getnframes())
                audio_data = np.frombuffer(frames, dtype=np.int16)

                # Reshape if stereo
                if wav_file.getnchannels() == 2:
                    audio_data = audio_data.reshape(-1, 2)

                return audio_data

        except Exception as e:
            logger.error(f"Error loading audio: {e}")
            return None

    def get_audio_status(self) -> Dict[str, Any]:
        """
        Get current audio status

        Returns:
            Dict containing audio status information
        """
        return {
            "is_processing": self.is_processing,
            "active_streams": len(self.audio_threads),
            "devices": list(self.audio_threads.keys()),
            "buffers": {k: len(v) for k, v in self.audio_buffers.items()},
            "config": self.audio_config.copy(),
        }

    def get_audio_levels(self, device_id: int = 0) -> Dict[str, float]:
        """
        Get current audio levels for monitoring

        Args:
            device_id: Audio device ID

        Returns:
            Dict containing audio level metrics
        """
        try:
            if device_id in self.audio_buffers and self.audio_buffers[device_id]:
                latest_audio = self.audio_buffers[device_id][-1]

                return {
                    "rms": np.sqrt(np.mean(latest_audio.astype(np.float32) ** 2)),
                    "peak": np.max(np.abs(latest_audio)),
                    "average": np.mean(np.abs(latest_audio)),
                    "dynamic_range": np.max(latest_audio) - np.min(latest_audio),
                }
            else:
                return {"rms": 0.0, "peak": 0.0, "average": 0.0, "dynamic_range": 0.0}

        except Exception as e:
            logger.error(f"Error getting audio levels: {e}")
            return {"rms": 0.0, "peak": 0.0, "average": 0.0, "dynamic_range": 0.0}
