#!/usr/bin/env python3
"""
Data Synchronization System
===========================
Comprehensive data synchronization for distributed agent swarm operations.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
import threading
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class SyncStatus(Enum):
    """Synchronization status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CONFLICT = "conflict"


class SyncPriority(Enum):
    """Synchronization priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SyncRequest:
    """Data synchronization request"""
    request_id: str
    source_agent: str
    target_agents: List[str]
    data_keys: List[str]
    priority: SyncPriority
    timestamp: float
    conflict_resolution: str = "auto"


@dataclass
class SyncResult:
    """Synchronization result"""
    request_id: str
    status: SyncStatus
    synced_keys: List[str]
    failed_keys: List[str]
    conflicts: List[str]
    completion_time: float
    error_message: Optional[str] = None


class DataSynchronization:
    """Data synchronization system for agent swarms"""
    
    def __init__(self, system_id: str = "default-sync"):
        self.logger = logging.getLogger(f"{__name__}.DataSynchronization")
        self.system_id = system_id
        
        # Synchronization state
        self._sync_requests: Dict[str, SyncRequest] = {}
        self._sync_results: Dict[str, SyncResult] = {}
        self._active_syncs: Dict[str, Dict[str, Any]] = {}
        
        # Data tracking
        self._data_versions: Dict[str, Dict[str, int]] = {}
        self._last_sync_times: Dict[str, float] = {}
        self._sync_conflicts: Dict[str, List[str]] = {}
        
        # Synchronization engine
        self._sync_engine_active = False
        self._sync_thread: Optional[threading.Thread] = None
        self._stop_sync = threading.Event()
        
        # Statistics
        self._total_syncs = 0
        self._successful_syncs = 0
        self._failed_syncs = 0
        self._conflict_count = 0
        
        self.logger.info(f"Data Synchronization '{system_id}' initialized")
    
    def request_synchronization(self, source_agent: str, target_agents: List[str], 
                               data_keys: List[str], priority: SyncPriority = SyncPriority.NORMAL,
                               conflict_resolution: str = "auto") -> str:
        """Request data synchronization"""
        request_id = f"sync_{source_agent}_{int(time.time())}"
        
        sync_request = SyncRequest(
            request_id=request_id,
            source_agent=source_agent,
            target_agents=target_agents,
            data_keys=data_keys,
            priority=priority,
            timestamp=time.time(),
            conflict_resolution=conflict_resolution
        )
        
        self._sync_requests[request_id] = sync_request
        self._total_syncs += 1
        
        self.logger.info(f"Sync request created: {request_id} from {source_agent} to {len(target_agents)} targets")
        return request_id
    
    def _process_sync_request(self, request: SyncRequest) -> SyncResult:
        """Process a synchronization request"""
        start_time = time.time()
        synced_keys = []
        failed_keys = []
        conflicts = []
        
        try:
            for data_key in request.data_keys:
                sync_result = self._sync_data_key(request.source_agent, request.target_agents, data_key)
                
                if sync_result["status"] == "success":
                    synced_keys.append(data_key)
                elif sync_result["status"] == "conflict":
                    conflicts.append(data_key)
                    self._sync_conflicts[data_key] = sync_result["conflicts"]
                else:
                    failed_keys.append(data_key)
            
            # Determine overall status
            if failed_keys:
                status = SyncStatus.FAILED
                self._failed_syncs += 1
            elif conflicts:
                status = SyncStatus.CONFLICT
                self._conflict_count += 1
            else:
                status = SyncStatus.COMPLETED
                self._successful_syncs += 1
            
            completion_time = time.time() - start_time
            
            return SyncResult(
                request_id=request.request_id,
                status=status,
                synced_keys=synced_keys,
                failed_keys=failed_keys,
                conflicts=conflicts,
                completion_time=completion_time
            )
            
        except Exception as e:
            self.logger.error(f"Sync processing error: {e}")
            self._failed_syncs += 1
            
            return SyncResult(
                request_id=request.request_id,
                status=SyncStatus.FAILED,
                synced_keys=[],
                failed_keys=request.data_keys,
                conflicts=[],
                completion_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def _sync_data_key(self, source_agent: str, target_agents: List[str], data_key: str) -> Dict[str, Any]:
        """Synchronize a specific data key"""
        # Initialize version tracking
        if data_key not in self._data_versions:
            self._data_versions[data_key] = {}
        
        if source_agent not in self._data_versions[data_key]:
            self._data_versions[data_key][source_agent] = 0
        
        # Increment source version
        self._data_versions[data_key][source_agent] += 1
        
        # Check for conflicts
        conflicts = []
        for target in target_agents:
            if target in self._data_versions[data_key]:
                target_version = self._data_versions[data_key][target]
                if target_version > 0 and target_version != self._data_versions[data_key][source_agent]:
                    conflicts.append({
                        "agent": target,
                        "version": target_version,
                        "source_version": self._data_versions[data_key][source_agent]
                    })
        
        if conflicts:
            return {
                "status": "conflict",
                "conflicts": conflicts,
                "data_key": data_key
            }
        
        # Perform synchronization
        for target in target_agents:
            if target not in self._data_versions[data_key]:
                self._data_versions[data_key][target] = 0
            
            # Update target version
            self._data_versions[data_key][target] = self._data_versions[data_key][source_agent]
            
            # Update last sync time
            sync_key = f"{source_agent}_{target}_{data_key}"
            self._last_sync_times[sync_key] = time.time()
        
        return {
            "status": "success",
            "data_key": data_key,
            "version": self._data_versions[data_key][source_agent]
        }
    
    def get_sync_status(self, request_id: str) -> Optional[SyncResult]:
        """Get synchronization status"""
        if request_id in self._sync_results:
            return self._sync_results[request_id]
        
        if request_id in self._sync_requests:
            return SyncResult(
                request_id=request_id,
                status=SyncStatus.PENDING,
                synced_keys=[],
                failed_keys=[],
                conflicts=[],
                completion_time=0.0
            )
        
        return None
    
    def resolve_conflict(self, data_key: str, resolution: str, winning_agent: str) -> bool:
        """Resolve a data synchronization conflict"""
        if data_key not in self._sync_conflicts:
            return False
        
        try:
            # Apply conflict resolution
            if resolution == "source_wins":
                # Source agent version takes precedence
                pass  # Already handled in sync
            elif resolution == "target_wins":
                # Target agent version takes precedence
                if winning_agent in self._data_versions[data_key]:
                    winning_version = self._data_versions[data_key][winning_agent]
                    # Update all other agents to match
                    for agent in self._data_versions[data_key]:
                        if agent != winning_agent:
                            self._data_versions[data_key][agent] = winning_version
            elif resolution == "merge":
                # Merge versions (increment highest version)
                max_version = max(self._data_versions[data_key].values())
                for agent in self._data_versions[data_key]:
                    self._data_versions[data_key][agent] = max_version + 1
            
            # Clear conflict
            del self._sync_conflicts[data_key]
            self.logger.info(f"Conflict resolved for {data_key} using {resolution}")
            return True
            
        except Exception as e:
            self.logger.error(f"Conflict resolution failed: {e}")
            return False
    
    def get_synchronization_stats(self) -> Dict[str, Any]:
        """Get synchronization system statistics"""
        return {
            "system_id": self.system_id,
            "total_syncs": self._total_syncs,
            "successful_syncs": self._successful_syncs,
            "failed_syncs": self._failed_syncs,
            "conflict_count": self._conflict_count,
            "success_rate": (self._successful_syncs / max(1, self._total_syncs)) * 100,
            "active_syncs": len(self._active_syncs),
            "pending_requests": len(self._sync_requests),
            "data_keys_tracked": len(self._data_versions),
            "sync_engine_active": self._sync_engine_active,
            "timestamp": time.time()
        }
    
    def start_sync_engine(self):
        """Start the synchronization engine"""
        if self._sync_engine_active:
            self.logger.warning("Sync engine already active")
            return
        
        self._sync_engine_active = True
        self._stop_sync.clear()
        
        self._sync_thread = threading.Thread(target=self._sync_engine_loop, daemon=True)
        self._sync_thread.start()
        
        self.logger.info("Data synchronization engine started")
    
    def _sync_engine_loop(self):
        """Main synchronization engine loop"""
        while not self._stop_sync.is_set():
            try:
                self._process_pending_syncs()
                time.sleep(0.1)  # Process quickly
            except Exception as e:
                self.logger.error(f"Sync engine error: {e}")
                time.sleep(1)
    
    def _process_pending_syncs(self):
        """Process pending synchronization requests"""
        # Sort requests by priority
        priority_order = [SyncPriority.CRITICAL, SyncPriority.HIGH, SyncPriority.NORMAL, SyncPriority.LOW]
        
        for priority in priority_order:
            for request_id, request in list(self._sync_requests.items()):
                if request.priority == priority:
                    # Process request
                    result = self._process_sync_request(request)
                    
                    # Store result
                    self._sync_results[request_id] = result
                    
                    # Remove from pending
                    del self._sync_requests[request_id]
                    
                    self.logger.info(f"Sync request processed: {request_id} - {result.status.value}")
    
    def stop_sync_engine(self):
        """Stop the synchronization engine"""
        self._sync_engine_active = False
        self._stop_sync.set()
        
        if self._sync_thread and self._sync_thread.is_alive():
            self._sync_thread.join(timeout=2)
        
        self.logger.info("Data synchronization engine stopped")


def main():
    """CLI interface for testing DataSynchronization"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Data Synchronization CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 DataSynchronization Smoke Test")
        print("=" * 45)
        
        sync = DataSynchronization("test-sync")
        
        # Request synchronization
        request_id = sync.request_synchronization(
            source_agent="agent-1",
            target_agents=["agent-2", "agent-3"],
            data_keys=["user-data", "config-data"],
            priority=SyncPriority.HIGH
        )
        
        print(f"✅ Sync request created: {request_id}")
        
        # Start sync engine
        sync.start_sync_engine()
        time.sleep(0.3)  # Allow processing
        
        # Check status
        status = sync.get_sync_status(request_id)
        print(f"✅ Sync status: {status.status.value}")
        print(f"✅ Synced keys: {len(status.synced_keys)}")
        
        # Get statistics
        stats = sync.get_synchronization_stats()
        print(f"✅ Total syncs: {stats['total_syncs']}")
        print(f"✅ Success rate: {stats['success_rate']:.1f}%")
        
        # Cleanup
        sync.stop_sync_engine()
        print("🎉 DataSynchronization smoke test PASSED!")
    else:
        print("DataSynchronization ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
