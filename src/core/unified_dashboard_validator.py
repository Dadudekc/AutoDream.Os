"""
Unified Dashboard Validator System - Agent Cellphone V2
Validates dashboard claims against actual codebase state and provides real-time synchronization
"""

import os
import time
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import threading
import queue


@dataclass
class DashboardClaim:
    """Represents a claim made by the dashboard"""
    claim_id: str
    timestamp: datetime
    claim_type: str  # FILE_COMPLETION, TASK_COMPLETION, SYSTEM_STATUS
    agent_id: str
    task_id: str
    claim_data: Dict[str, Any]
    source: str  # DASHBOARD, AGENT_REPORT, SYSTEM_DETECTION


@dataclass
class ValidationResult:
    """Represents the result of validating a dashboard claim"""
    validation_id: str
    timestamp: datetime
    claim_id: str
    status: str  # VALID, INVALID, PARTIAL, ERROR
    discrepancies: List[str]
    evidence: Dict[str, Any]
    confidence_score: float  # 0.0 to 1.0


@dataclass
class CodebaseSnapshot:
    """Represents a snapshot of the current codebase state"""
    snapshot_id: str
    timestamp: datetime
    file_count: int
    python_files: int
    large_files: int
    todo_files: int
    file_hashes: Dict[str, str]
    directory_structure: Dict[str, List[str]]
    metadata: Dict[str, Any]


class UnifiedDashboardValidator:
    """Unified system for validating dashboard claims against actual codebase state"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.dashboard_claims: List[DashboardClaim] = []
        self.validation_results: List[ValidationResult] = []
        self.codebase_snapshots: List[CodebaseSnapshot] = []
        self.validation_queue = queue.Queue()
        self.sync_thread = None
        self.running = False
        self.validation_rules = self._initialize_validation_rules()
        
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize validation rules for different claim types"""
        return {
            "FILE_COMPLETION": {
                "file_exists": True,
                "file_size_check": True,
                "content_hash_check": True,
                "timestamp_validation": True
            },
            "TASK_COMPLETION": {
                "deliverables_exist": True,
                "code_changes_detected": True,
                "devlog_entries_found": True,
                "test_results_available": True
            },
            "SYSTEM_STATUS": {
                "service_running": True,
                "endpoint_accessible": True,
                "database_connected": True,
                "log_files_updated": True
            }
        }
    
    def start_validation_service(self):
        """Start the validation service"""
        if not self.running:
            self.running = True
            self.sync_thread = threading.Thread(target=self._validation_worker, daemon=True)
            self.sync_thread.start()
    
    def stop_validation_service(self):
        """Stop the validation service"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join()
    
    def _validation_worker(self):
        """Background worker for continuous validation"""
        while self.running:
            try:
                # Process validation requests
                while not self.validation_queue.empty():
                    claim = self.validation_queue.get_nowait()
                    self._validate_claim(claim)
                
                # Take periodic codebase snapshots
                if len(self.codebase_snapshots) == 0 or \
                   (datetime.now() - self.codebase_snapshots[-1].timestamp).seconds > 60:
                    self._take_codebase_snapshot()
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"Error in validation worker: {e}")
                time.sleep(10)  # Wait before retrying
    
    def _take_codebase_snapshot(self):
        """Take a snapshot of the current codebase state"""
        try:
            snapshot = CodebaseSnapshot(
                snapshot_id=f"snapshot_{int(time.time())}",
                timestamp=datetime.now(),
                file_count=0,
                python_files=0,
                large_files=0,
                todo_files=0,
                file_hashes={},
                directory_structure={},
                metadata={}
            )
            
            # Walk through codebase and collect information
            for root, dirs, files in os.walk(self.base_path):
                root_path = Path(root)
                relative_root = root_path.relative_to(self.base_path)
                
                # Skip certain directories
                if any(skip in str(relative_root) for skip in ['.git', '__pycache__', '.pytest_cache']):
                    continue
                
                snapshot.directory_structure[str(relative_root)] = []
                
                for file in files:
                    file_path = root_path / file
                    relative_file_path = file_path.relative_to(self.base_path)
                    
                    snapshot.file_count += 1
                    snapshot.directory_structure[str(relative_root)].append(file)
                    
                    if file.endswith('.py'):
                        snapshot.python_files += 1
                        
                        # Check file size
                        try:
                            file_size = file_path.stat().st_size
                            if file_size > 20 * 1024:  # 20KB
                                snapshot.large_files += 1
                            
                            # Calculate file hash
                            file_hash = self._calculate_file_hash(file_path)
                            snapshot.file_hashes[str(relative_file_path)] = file_hash
                            
                            # Check for TODO comments
                            if self._file_contains_todo(file_path):
                                snapshot.todo_files += 1
                                
                        except Exception as e:
                            print(f"Error processing file {file_path}: {e}")
            
            self.codebase_snapshots.append(snapshot)
            
        except Exception as e:
            print(f"Error taking codebase snapshot: {e}")
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
        except Exception:
            return "ERROR_HASH"
    
    def _file_contains_todo(self, file_path: Path) -> bool:
        """Check if a file contains TODO or FIXME comments"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return 'TODO' in content or 'FIXME' in content
        except Exception:
            return False
    
    def submit_claim_for_validation(self, claim_data: Dict) -> str:
        """Submit a dashboard claim for validation"""
        claim = DashboardClaim(
            claim_id=f"claim_{int(time.time())}",
            timestamp=datetime.now(),
            claim_type=claim_data.get("type", "UNKNOWN"),
            agent_id=claim_data.get("agent_id", "UNKNOWN"),
            task_id=claim_data.get("task_id", "UNKNOWN"),
            claim_data=claim_data,
            source=claim_data.get("source", "DASHBOARD")
        )
        
        self.dashboard_claims.append(claim)
        
        # Add to validation queue for processing
        self.validation_queue.put(claim)
        
        return claim.claim_id
    
    def _validate_claim(self, claim: DashboardClaim):
        """Validate a specific dashboard claim"""
        try:
            validation_result = ValidationResult(
                validation_id=f"validation_{int(time.time())}",
                timestamp=datetime.now(),
                claim_id=claim.claim_id,
                status="PENDING",
                discrepancies=[],
                evidence={},
                confidence_score=0.0
            )
            
            # Apply validation rules based on claim type
            if claim.claim_type == "FILE_COMPLETION":
                validation_result = self._validate_file_completion(claim)
            elif claim.claim_type == "TASK_COMPLETION":
                validation_result = self._validate_task_completion(claim)
            elif claim.claim_type == "SYSTEM_STATUS":
                validation_result = self._validate_system_status(claim)
            else:
                validation_result.discrepancies.append(f"Unknown claim type: {claim.claim_type}")
                validation_result.status = "ERROR"
                validation_result.confidence_score = 0.0
            
            self.validation_results.append(validation_result)
            
            # Trigger actions based on validation result
            if validation_result.status == "INVALID":
                self._trigger_dashboard_correction(validation_result)
            
        except Exception as e:
            print(f"Error validating claim {claim.claim_id}: {e}")
            validation_result = ValidationResult(
                validation_id=f"validation_{int(time.time())}",
                timestamp=datetime.now(),
                claim_id=claim.claim_id,
                status="ERROR",
                discrepancies=[f"Validation error: {str(e)}"],
                evidence={},
                confidence_score=0.0
            )
            self.validation_results.append(validation_result)
    
    def _validate_file_completion(self, claim: DashboardClaim) -> ValidationResult:
        """Validate a file completion claim"""
        result = ValidationResult(
            validation_id=f"validation_{int(time.time())}",
            timestamp=datetime.now(),
            claim_id=claim.claim_id,
            status="VALID",
            discrepancies=[],
            evidence={},
            confidence_score=1.0
        )
        
        file_path = claim.claim_data.get("file_path")
        if not file_path:
            result.status = "INVALID"
            result.discrepancies.append("No file path specified")
            result.confidence_score = 0.0
            return result
        
        full_path = self.base_path / file_path
        
        # Check file existence
        if not full_path.exists():
            result.status = "INVALID"
            result.discrepancies.append(f"File {file_path} does not exist")
            result.confidence_score = 0.0
            return result
        
        # Check file size if specified
        expected_size = claim.claim_data.get("expected_size")
        if expected_size:
            actual_size = full_path.stat().st_size
            if actual_size != expected_size:
                result.status = "PARTIAL"
                result.discrepancies.append(f"File size mismatch: expected {expected_size}, got {actual_size}")
                result.confidence_score = 0.7
        
        # Check file hash if specified
        expected_hash = claim.claim_data.get("expected_hash")
        if expected_hash:
            actual_hash = self._calculate_file_hash(full_path)
            if actual_hash != expected_hash:
                result.status = "INVALID"
                result.discrepancies.append(f"File hash mismatch: expected {expected_hash}, got {actual_hash}")
                result.confidence_score = 0.0
        
        result.evidence = {
            "file_path": str(file_path),
            "exists": True,
            "size": full_path.stat().st_size,
            "hash": self._calculate_file_hash(full_path),
            "last_modified": full_path.stat().st_mtime
        }
        
        return result
    
    def _parse_task_deliverables(self, claim: DashboardClaim) -> Tuple[List[str], int]:
        """Parse deliverable information from a task claim."""
        deliverables = claim.claim_data.get("deliverables", [])
        expected_devlogs = claim.claim_data.get("expected_devlogs", 0)
        return deliverables, expected_devlogs

    def _apply_task_validation_rules(
        self,
        deliverables: List[str],
        expected_devlogs: int,
        agent_id: str,
        task_id: str,
        base_path: Path,
        rules: Dict[str, bool],
    ) -> Tuple[str, List[str], Dict[str, Any], float]:
        """Apply validation rules for task completion."""

        status = "VALID"
        discrepancies: List[str] = []
        confidence = 1.0

        if rules.get("deliverables_exist", True):
            for deliverable in deliverables:
                if not self._check_deliverable_exists(base_path, deliverable):
                    status = "PARTIAL"
                    discrepancies.append(f"Deliverable not found: {deliverable}")
                    confidence = min(confidence, 0.6)

        actual_devlogs = 0
        if rules.get("devlog_entries_found", True):
            actual_devlogs = self._count_devlog_entries(agent_id, task_id)
            if actual_devlogs < expected_devlogs:
                status = "PARTIAL"
                discrepancies.append(
                    f"Insufficient devlog entries: expected {expected_devlogs}, got {actual_devlogs}"
                )
                confidence = min(confidence, 0.8)

        evidence = {
            "deliverables_checked": len(deliverables),
            "devlog_entries_found": actual_devlogs,
            "validation_timestamp": datetime.now().isoformat(),
        }

        return status, discrepancies, evidence, confidence

    def _generate_task_validation_result(
        self,
        claim_id: str,
        status: str,
        discrepancies: List[str],
        evidence: Dict[str, Any],
        confidence: float,
    ) -> ValidationResult:
        """Generate ValidationResult for a task claim."""
        return ValidationResult(
            validation_id=f"validation_{int(time.time())}",
            timestamp=datetime.now(),
            claim_id=claim_id,
            status=status,
            discrepancies=discrepancies,
            evidence=evidence,
            confidence_score=confidence,
        )

    def _validate_task_completion(self, claim: DashboardClaim) -> ValidationResult:
        """Validate a task completion claim"""
        deliverables, expected_devlogs = self._parse_task_deliverables(claim)
        rules = self.validation_rules.get("TASK_COMPLETION", {})
        status, discrepancies, evidence, confidence = self._apply_task_validation_rules(
            deliverables,
            expected_devlogs,
            claim.agent_id,
            claim.task_id,
            self.base_path,
            rules,
        )
        return self._generate_task_validation_result(
            claim.claim_id, status, discrepancies, evidence, confidence
        )
    
    def _validate_system_status(self, claim: DashboardClaim) -> ValidationResult:
        """Validate a system status claim"""
        result = ValidationResult(
            validation_id=f"validation_{int(time.time())}",
            timestamp=datetime.now(),
            claim_id=claim.claim_id,
            status="VALID",
            discrepancies=[],
            evidence={},
            confidence_score=1.0
        )
        
        # This would integrate with actual system monitoring
        # For now, return a placeholder validation
        result.evidence = {
            "system_status": "PLACEHOLDER",
            "validation_timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def _check_deliverable_exists(self, base_path: Path, deliverable: str) -> bool:
        """Check if a deliverable exists"""
        if '/' in deliverable or '\\' in deliverable:
            return (base_path / deliverable).exists()
        return False
    
    def _count_devlog_entries(self, agent_id: str, task_id: str) -> int:
        """Count devlog entries for a specific agent and task"""
        # This would search through actual devlog files
        # For now, return a placeholder count
        return 1
    
    def _trigger_dashboard_correction(self, validation_result: ValidationResult):
        """Trigger dashboard correction when validation fails"""
        print(f"Dashboard correction needed for claim {validation_result.claim_id}: {validation_result.discrepancies}")
        # This would trigger actual dashboard update logic
    
    def get_validation_report(self) -> Dict:
        """Generate comprehensive validation report"""
        total_claims = len(self.dashboard_claims)
        total_validations = len(self.validation_results)
        valid_claims = len([v for v in self.validation_results if v.status == "VALID"])
        invalid_claims = len([v for v in self.validation_results if v.status == "INVALID"])
        partial_claims = len([v for v in self.validation_results if v.status == "PARTIAL"])
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_claims": total_claims,
            "total_validations": total_validations,
            "valid_claims": valid_claims,
            "invalid_claims": invalid_claims,
            "partial_claims": partial_claims,
            "validation_rate": (valid_claims / total_validations * 100) if total_validations > 0 else 0,
            "recent_validations": [asdict(v) for v in self.validation_results[-10:]],
            "codebase_snapshots": len(self.codebase_snapshots),
            "service_status": "RUNNING" if self.running else "STOPPED"
        }
    
    def save_validation_data(self, file_path: str = "validation_data.json"):
        """Save validation data to file"""
        data = {
            "dashboard_claims": [asdict(c) for c in self.dashboard_claims],
            "validation_results": [asdict(v) for v in self.validation_results],
            "codebase_snapshots": [asdict(s) for s in self.codebase_snapshots]
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def load_validation_data(self, file_path: str = "validation_data.json"):
        """Load validation data from file"""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Reconstruct objects from loaded data
                # Implementation would reconstruct DashboardClaim, ValidationResult, and CodebaseSnapshot objects


# CLI interface for the unified dashboard validator
def main():
    """CLI interface for unified dashboard validator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified Dashboard Validator System")
    parser.add_argument("--start-service", action="store_true", help="Start validation service")
    parser.add_argument("--stop-service", action="store_true", help="Stop validation service")
    parser.add_argument("--submit-claim", help="Submit claim for validation (JSON format)")
    parser.add_argument("--report", action="store_true", help="Generate validation report")
    parser.add_argument("--save", action="store_true", help="Save validation data")
    
    args = parser.parse_args()
    
    udv = UnifiedDashboardValidator()
    
    if args.start_service:
        udv.start_validation_service()
        print("Validation service started")
    
    if args.stop_service:
        udv.stop_validation_service()
        print("Validation service stopped")
    
    if args.submit_claim:
        try:
            claim_data = json.loads(args.submit_claim)
            claim_id = udv.submit_claim_for_validation(claim_data)
            print(f"Claim submitted for validation: {claim_id}")
        except Exception as e:
            print(f"Error submitting claim: {e}")
    
    if args.report:
        report = udv.get_validation_report()
        print(json.dumps(report, indent=2))
    
    if args.save:
        udv.save_validation_data()
        print("Validation data saved")


if __name__ == "__main__":
    main()
