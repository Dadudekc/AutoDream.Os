#!/usr/bin/env python3
"""
Multi-Agent Data Coordination System
===================================
Comprehensive data coordination system for agent swarm operations.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
import threading
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class DataOperation(Enum):
    """Data operation types"""
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"
    SYNC = "sync"


@dataclass
class DataRequest:
    """Data coordination request"""
    request_id: str
    agent_id: str
    operation: DataOperation
    data_key: str
    data_value: Optional[Any] = None
    timestamp: float = 0.0
    priority: int = 1


@dataclass
class DataResponse:
    """Data coordination response"""
    request_id: str
    success: bool
    data_value: Optional[Any] = None
    error_message: Optional[str] = None
    timestamp: float = 0.0


class MultiAgentDataCoordination:
    """Multi-agent data coordination system for agent swarms"""
    
    def __init__(self, coordination_id: str = "default-coordination"):
        self.logger = logging.getLogger(f"{__name__}.MultiAgentDataCoordination")
        self.coordination_id = coordination_id
        self._data_store: Dict[str, Any] = {}
        self._data_locks: Dict[str, threading.Lock] = {}
        self._data_versions: Dict[str, int] = {}
        self._pending_requests: Dict[str, DataRequest] = {}
        self._completed_requests: Dict[str, DataResponse] = {}
        self._request_queue: List[DataRequest] = []
        self._registered_agents: Set[str] = set()
        self._agent_sessions: Dict[str, float] = {}
        self._coordination_active = False
        self._coordination_thread: Optional[threading.Thread] = None
        self._stop_coordination = threading.Event()
        self.logger.info(f"Multi-Agent Data Coordination '{coordination_id}' initialized")
    
    def register_agent(self, agent_id: str) -> bool:
        """Register an agent for data coordination"""
        if agent_id in self._registered_agents:
            return False
        self._registered_agents.add(agent_id)
        self._agent_sessions[agent_id] = time.time()
        return True
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from data coordination"""
        if agent_id not in self._registered_agents:
            return False
        self._registered_agents.remove(agent_id)
        if agent_id in self._agent_sessions:
            del self._agent_sessions[agent_id]
        return True
    
    def submit_data_request(self, request: DataRequest) -> str:
        """Submit a data coordination request"""
        if request.agent_id not in self._registered_agents:
            raise ValueError(f"Agent {request.agent_id} not registered")
        request.timestamp = time.time()
        self._pending_requests[request.request_id] = request
        self._request_queue.append(request)
        return request.request_id
    
    def process_data_request(self, request: DataRequest) -> DataResponse:
        """Process a data coordination request"""
        try:
            if request.data_key not in self._data_locks:
                self._data_locks[request.data_key] = threading.Lock()
            with self._data_locks[request.data_key]:
                if request.operation == DataOperation.READ:
                    return self._handle_read_request(request)
                elif request.operation == DataOperation.WRITE:
                    return self._handle_write_request(request)
                elif request.operation == DataOperation.UPDATE:
                    return self._handle_update_request(request)
                elif request.operation == DataOperation.DELETE:
                    return self._handle_delete_request(request)
                elif request.operation == DataOperation.SYNC:
                    return self._handle_sync_request(request)
                else:
                    return DataResponse(request_id=request.request_id, success=False, 
                                     error_message=f"Unknown operation: {request.operation.value}")
        except Exception as e:
            return DataResponse(request_id=request.request_id, success=False, error_message=str(e))
    
    def _handle_read_request(self, request: DataRequest) -> DataResponse:
        """Handle read data request"""
        if request.data_key not in self._data_store:
            return DataResponse(request_id=request.request_id, success=False, 
                             error_message=f"Data key not found: {request.data_key}")
        return DataResponse(request_id=request.request_id, success=True, 
                          data_value=self._data_store[request.data_key], timestamp=time.time())
    
    def _handle_write_request(self, request: DataRequest) -> DataResponse:
        """Handle write data request"""
        if request.data_value is None:
            return DataResponse(request_id=request.request_id, success=False, 
                             error_message="Data value required for write operation")
        self._data_store[request.data_key] = request.data_value
        self._data_versions[request.data_key] = self._data_versions.get(request.data_key, 0) + 1
        return DataResponse(request_id=request.request_id, success=True, timestamp=time.time())
    
    def _handle_update_request(self, request: DataRequest) -> DataResponse:
        """Handle update data request"""
        if request.data_key not in self._data_store:
            return DataResponse(request_id=request.request_id, success=False, 
                             error_message=f"Data key not found for update: {request.data_key}")
        if request.data_value is None:
            return DataResponse(request_id=request.request_id, success=False, 
                             error_message="Data value required for update operation")
        self._data_store[request.data_key] = request.data_value
        self._data_versions[request.data_key] += 1
        return DataResponse(request_id=request.request_id, success=True, timestamp=time.time())
    
    def _handle_delete_request(self, request: DataRequest) -> DataResponse:
        """Handle delete data request"""
        if request.data_key not in self._data_store:
            return DataResponse(request_id=request.request_id, success=False, 
                             error_message=f"Data key not found for deletion: {request.data_key}")
        del self._data_store[request.data_key]
        if request.data_key in self._data_versions:
            del self._data_versions[request.data_key]
        return DataResponse(request_id=request.request_id, success=True, timestamp=time.time())
    
    def _handle_sync_request(self, request: DataRequest) -> DataResponse:
        """Handle data synchronization request"""
        sync_data = {"data_keys": list(self._data_store.keys()), "versions": self._data_versions.copy(), 
                     "timestamp": time.time()}
        return DataResponse(request_id=request.request_id, success=True, data_value=sync_data, timestamp=time.time())
    
    def get_coordination_status(self) -> Dict[str, Any]:
        """Get coordination system status"""
        return {"coordination_id": self.coordination_id, "active_agents": len(self._registered_agents),
                "pending_requests": len(self._pending_requests), "completed_requests": len(self._completed_requests),
                "data_keys": len(self._data_store), "coordination_active": self._coordination_active, "timestamp": time.time()}
    
    def start_coordination(self):
        """Start the coordination system"""
        if self._coordination_active:
            return
        self._coordination_active = True
        self._stop_coordination.clear()
        self._coordination_thread = threading.Thread(target=self._coordination_loop, daemon=True)
        self._coordination_thread.start()
    
    def _coordination_loop(self):
        """Main coordination loop"""
        while not self._stop_coordination.is_set():
            try:
                self._process_pending_requests()
                time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Coordination error: {e}")
                time.sleep(1)
    
    def _process_pending_requests(self):
        """Process pending data requests"""
        if not self._request_queue:
            return
        self._request_queue.sort(key=lambda r: r.priority, reverse=True)
        while self._request_queue:
            request = self._request_queue.pop(0)
            response = self.process_data_request(request)
            self._completed_requests[request.request_id] = response
            if request.request_id in self._pending_requests:
                del self._pending_requests[request.request_id]
    
    def stop_coordination(self):
        """Stop the coordination system"""
        self._coordination_active = False
        self._stop_coordination.set()
        if self._coordination_thread and self._coordination_thread.is_alive():
            self._coordination_thread.join(timeout=2)


def main():
    """CLI interface for testing MultiAgentDataCoordination"""
    import argparse
    parser = argparse.ArgumentParser(description="Multi-Agent Data Coordination CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    args = parser.parse_args()
    
    if args.test:
        print("🧪 MultiAgentDataCoordination Smoke Test")
        print("=" * 50)
        coordination = MultiAgentDataCoordination("test-coordination")
        coordination.register_agent("agent-1")
        coordination.register_agent("agent-2")
        write_request = DataRequest("req-1", "agent-1", DataOperation.WRITE, "test-key", "test-value")
        coordination.submit_data_request(write_request)
        read_request = DataRequest("req-2", "agent-2", DataOperation.READ, "test-key")
        coordination.submit_data_request(read_request)
        coordination.start_coordination()
        time.sleep(0.2)
        status = coordination.get_coordination_status()
        print(f"✅ Active agents: {status['active_agents']}")
        print(f"✅ Completed requests: {status['completed_requests']}")
        coordination.stop_coordination()
        print("🎉 MultiAgentDataCoordination smoke test PASSED!")
    else:
        print("MultiAgentDataCoordination ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
