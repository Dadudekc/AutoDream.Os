#!/usr/bin/env python3
"""Network monitoring utilities including scanning and anomaly detection."""

import ipaddress
import socket
import platform
import subprocess
import time
import logging
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from .network_security_policies import NetworkDevice
from .network_security_config import (
    DEFAULT_MAX_THREADS,
    DEFAULT_TIMEOUT,
    DEFAULT_ANOMALY_THRESHOLD,
)


class NetworkScanner:
    """Advanced network scanning and discovery system."""

    def __init__(self, max_threads: int = DEFAULT_MAX_THREADS, timeout: int = DEFAULT_TIMEOUT):
        self.max_threads = max_threads
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self.scan_results: Dict[str, List[int]] = {}

    def discover_devices(self, network_range: str) -> List[NetworkDevice]:
        """Discover active devices on the network using ARP scanning."""
        try:
            network = ipaddress.ip_network(network_range, strict=False)
            devices: List[NetworkDevice] = []

            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                future_to_ip = {
                    executor.submit(self._ping_device, str(ip)): str(ip)
                    for ip in network.hosts()
                }

                for future in as_completed(future_to_ip):
                    ip = future_to_ip[future]
                    try:
                        if future.result():
                            device = NetworkDevice(
                                ip_address=ip,
                                mac_address=self._get_mac_address(ip),
                                hostname=self._get_hostname(ip),
                                is_active=True,
                                last_seen=time.time(),
                                open_ports=[],
                                services=[],
                            )
                            devices.append(device)
                            self.logger.info(f"Discovered device: {ip}")
                    except Exception as e:
                        self.logger.debug(f"Failed to scan {ip}: {e}")

            return devices

        except Exception as e:
            self.logger.error(f"Network discovery failed: {e}")
            return []

    def scan_ports(self, target: str, ports: List[int]) -> List[int]:
        """Scan for open ports on target host."""
        open_ports: List[int] = []

        def scan_port(port: int) -> Optional[int]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                result = sock.connect_ex((target, port))
                sock.close()
                return port if result == 0 else None
            except Exception:
                return None

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_port = {executor.submit(scan_port, port): port for port in ports}

            for future in as_completed(future_to_port):
                try:
                    result = future.result()
                    if result is not None:
                        open_ports.append(result)
                        self.logger.info(f"Open port {result} on {target}")
                except Exception as e:
                    self.logger.debug(f"Port scan failed: {e}")

        return open_ports

    def grab_banner(self, target: str, port: int) -> Optional[str]:
        """Grab service banner from an open port."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((target, port))
            sock.send(b"GET / HTTP/1.0\r\n\r\n")
            response = sock.recv(1024)
            sock.close()
            if response:
                return response.decode("utf-8", errors="ignore").strip()
            return None
        except Exception as e:
            self.logger.debug(f"Banner grab failed for {target}:{port}: {e}")
            return None

    def _ping_device(self, ip: str) -> bool:
        """Ping device to check if it's active."""
        try:
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", "1000", ip]
            else:
                cmd = ["ping", "-c", "1", "-W", "1", ip]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
            return result.returncode == 0
        except Exception:
            return False

    def _get_mac_address(self, ip: str) -> Optional[str]:
        """Get MAC address for IP (platform dependent)."""
        try:
            if platform.system().lower() == "windows":
                cmd = ["arp", "-a", ip]
            else:
                cmd = ["arp", "-n", ip]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                lines = result.stdout.split("\n")
                for line in lines:
                    if ip in line:
                        parts = line.split()
                        for part in parts:
                            if ":" in part and len(part) == 17:
                                return part
            return None
        except Exception:
            return None

    def _get_hostname(self, ip: str) -> Optional[str]:
        """Get hostname for IP address."""
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return None


class AnomalyDetector:
    """AI-powered anomaly detection system."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_initialized = True
        self.model_loaded = True
        self.anomaly_threshold = DEFAULT_ANOMALY_THRESHOLD
        self.detection_history: List[Dict] = []

    def detect_anomalies(self, network_traffic: List[Dict]) -> List[Dict]:
        """Detect anomalies in network traffic."""
        anomalies: List[Dict] = []
        try:
            for traffic in network_traffic:
                anomaly_score = self._calculate_anomaly_score(traffic)
                if anomaly_score > self.anomaly_threshold:
                    anomaly = {
                        "type": "network_anomaly",
                        "source_ip": traffic.get("source_ip"),
                        "destination_ip": traffic.get("destination_ip"),
                        "anomaly_score": anomaly_score,
                        "timestamp": time.time(),
                        "details": traffic,
                        "severity": self._classify_anomaly_severity(anomaly_score),
                    }
                    anomalies.append(anomaly)
                    self.logger.warning(f"Anomaly detected: {anomaly}")
            return anomalies
        except Exception as e:
            self.logger.error(f"Anomaly detection failed: {e}")
            return []

    def _calculate_anomaly_score(self, traffic: Dict) -> float:
        """Calculate anomaly score for traffic pattern."""
        score = 0.0
        if traffic.get("port") in [22, 23, 3389]:
            score += 0.3
        if traffic.get("bytes", 0) > 1_000_000:
            score += 0.2
        current_hour = time.localtime().tm_hour
        if current_hour < 6 or current_hour > 22:
            score += 0.2
        if self._is_suspicious_pattern(traffic):
            score += 0.4
        return min(score, 1.0)

    def _is_suspicious_pattern(self, traffic: Dict) -> bool:
        """Check for suspicious traffic patterns."""
        suspicious_patterns = [
            "port_scan",
            "brute_force",
            "data_exfiltration",
            "command_injection",
        ]
        for pattern in suspicious_patterns:
            if pattern in str(traffic).lower():
                return True
        return False

    def _classify_anomaly_severity(self, score: float) -> str:
        """Classify anomaly severity based on score."""
        if score >= 0.9:
            return "critical"
        if score >= 0.7:
            return "high"
        if score >= 0.5:
            return "medium"
        return "low"




__all__ = ["NetworkScanner", "AnomalyDetector"]

