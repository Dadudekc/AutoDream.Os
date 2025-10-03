#!/usr/bin/env python3
"""
Centralized Content Registry Operations
=====================================
Operations and utilities for centralized content management system
V2 Compliant: ≤400 lines, focused operations
"""

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
import sys
sys.path.insert(0, str(project_root))

from src.core.centralized_content_registry_core import (
    CentralizedContentRegistryCore, ContentType, ContentStatus, ContentMetadata
)

class ContentRegistryOperations:
    """Operations and utilities for content registry management"""
    
    def __init__(self, registry: CentralizedContentRegistryCore = None):
        self.registry = registry or CentralizedContentRegistryCore()
    
    def manage_operations(self, action: str, **kwargs) -> Any:
        """Consolidated operations management"""
        if action == "bulk_register":
            return self.bulk_register_content(
                kwargs["directory"], kwargs["content_type"], 
                kwargs["agent_id"], kwargs.get("recursive", False)
            )
        elif action == "export_registry":
            return self.export_registry(kwargs["output_file"])
        elif action == "import_registry":
            return self.import_registry(kwargs["input_file"])
        elif action == "validate_registry":
            return self.validate_registry()
        elif action == "migrate_content":
            return self.migrate_content(
                kwargs["source_dir"], kwargs["target_dir"], 
                kwargs.get("dry_run", False)
            )
        elif action == "backup_registry":
            return self.backup_registry(kwargs["backup_dir"])
        elif action == "restore_registry":
            return self.restore_registry(kwargs["backup_file"])
        elif action == "analyze_usage":
            return self.analyze_content_usage(kwargs.get("days", 30))
        elif action == "optimize_registry":
            return self.optimize_registry()
        return None
    
    def bulk_register_content(self, directory: str, content_type: ContentType, 
                             agent_id: str, recursive: bool = False) -> Dict[str, Any]:
        """Bulk register content from a directory"""
        directory_path = Path(directory)
        if not directory_path.exists():
            return {"success": False, "error": f"Directory {directory} does not exist"}
        
        results = {
            "success": True,
            "registered": 0,
            "failed": 0,
            "errors": []
        }
        
        # Get files to process
        if recursive:
            files = list(directory_path.rglob("*"))
        else:
            files = list(directory_path.iterdir())
        
        # Filter to only files
        files = [f for f in files if f.is_file()]
        
        for file_path in files:
            try:
                success = self.registry.manage_registry_operations(
                    "register",
                    file_path=str(file_path),
                    content_type=content_type,
                    agent_id=agent_id,
                    description=f"Bulk registered from {directory}",
                    tags=["bulk_import"]
                )
                
                if success:
                    results["registered"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(f"Failed to register {file_path}")
                    
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Error registering {file_path}: {e}")
        
        return results
    
    def export_registry(self, output_file: str) -> bool:
        """Export registry to a file"""
        try:
            stats = self.registry.manage_registry_operations("statistics")
            
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "registry_statistics": stats,
                "content_metadata": {
                    k: {
                        "file_path": v.file_path,
                        "content_type": v.content_type.value,
                        "agent_id": v.agent_id,
                        "created_at": v.created_at,
                        "last_modified": v.last_modified,
                        "file_size": v.file_size,
                        "description": v.description,
                        "tags": v.tags,
                        "status": v.status.value,
                        "quality_score": v.quality_score,
                        "v2_compliant": v.v2_compliant
                    }
                    for k, v in self.registry.content_registry.items()
                }
            }
            
            with open(output_file, 'w') as f:
                import json
                json.dump(export_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error exporting registry: {e}")
            return False
    
    def import_registry(self, input_file: str) -> bool:
        """Import registry from a file"""
        try:
            with open(input_file, 'r') as f:
                import json
                import_data = json.load(f)
            
            # Validate import data structure
            if "content_metadata" not in import_data:
                print("Invalid import file format")
                return False
            
            # Import content metadata
            imported_count = 0
            for file_path, metadata in import_data["content_metadata"].items():
                try:
                    # Create ContentMetadata object
                    content_metadata = ContentMetadata(
                        file_path=metadata["file_path"],
                        content_type=ContentType(metadata["content_type"]),
                        agent_id=metadata["agent_id"],
                        created_at=metadata["created_at"],
                        last_modified=metadata["last_modified"],
                        last_accessed=datetime.now().isoformat(),
                        file_size=metadata["file_size"],
                        content_hash="",  # Will be recalculated
                        description=metadata["description"],
                        tags=metadata["tags"],
                        dependencies=[],
                        status=ContentStatus(metadata["status"]),
                        quality_score=metadata["quality_score"],
                        v2_compliant=metadata["v2_compliant"]
                    )
                    
                    self.registry.content_registry[file_path] = content_metadata
                    imported_count += 1
                    
                except Exception as e:
                    print(f"Error importing {file_path}: {e}")
            
            # Save updated registry
            self.registry.manage_registry_operations("save")
            print(f"Successfully imported {imported_count} content items")
            return True
            
        except Exception as e:
            print(f"Error importing registry: {e}")
            return False
    
    def validate_registry(self) -> Dict[str, Any]:
        """Validate registry integrity"""
        validation_report = {
            "valid": True,
            "issues": [],
            "statistics": {
                "total_files": len(self.registry.content_registry),
                "missing_files": 0,
                "invalid_paths": 0,
                "corrupted_metadata": 0
            }
        }
        
        for file_path, metadata in self.registry.content_registry.items():
            # Check if file exists
            if not Path(file_path).exists():
                validation_report["statistics"]["missing_files"] += 1
                validation_report["issues"].append(f"Missing file: {file_path}")
            
            # Check if path is valid
            try:
                Path(file_path).resolve()
            except Exception:
                validation_report["statistics"]["invalid_paths"] += 1
                validation_report["issues"].append(f"Invalid path: {file_path}")
            
            # Check metadata integrity
            try:
                if not isinstance(metadata.content_type, ContentType):
                    validation_report["statistics"]["corrupted_metadata"] += 1
                    validation_report["issues"].append(f"Invalid content type for {file_path}")
                
                if not isinstance(metadata.status, ContentStatus):
                    validation_report["statistics"]["corrupted_metadata"] += 1
                    validation_report["issues"].append(f"Invalid status for {file_path}")
                    
            except Exception:
                validation_report["statistics"]["corrupted_metadata"] += 1
                validation_report["issues"].append(f"Corrupted metadata for {file_path}")
        
        if validation_report["issues"]:
            validation_report["valid"] = False
        
        return validation_report
    
    def migrate_content(self, source_dir: str, target_dir: str, 
                       dry_run: bool = False) -> Dict[str, Any]:
        """Migrate content from source to target directory"""
        source_path = Path(source_dir)
        target_path = Path(target_dir)
        
        if not source_path.exists():
            return {"success": False, "error": f"Source directory {source_dir} does not exist"}
        
        migration_report = {
            "success": True,
            "migrated": 0,
            "failed": 0,
            "errors": [],
            "dry_run": dry_run
        }
        
        # Create target directory if it doesn't exist
        if not dry_run:
            target_path.mkdir(parents=True, exist_ok=True)
        
        # Process files in registry
        for file_path, metadata in self.registry.content_registry.items():
            file_path_obj = Path(file_path)
            
            # Check if file is in source directory
            try:
                if not file_path_obj.is_relative_to(source_path):
                    continue
                
                # Calculate new path
                relative_path = file_path_obj.relative_to(source_path)
                new_path = target_path / relative_path
                
                if not dry_run:
                    # Create target directory structure
                    new_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(file_path, new_path)
                    
                    # Update registry
                    metadata.file_path = str(new_path)
                
                migration_report["migrated"] += 1
                
            except Exception as e:
                migration_report["failed"] += 1
                migration_report["errors"].append(f"Error migrating {file_path}: {e}")
        
        if not dry_run and migration_report["migrated"] > 0:
            self.registry.manage_registry_operations("save")
        
        return migration_report
    
    def backup_registry(self, backup_dir: str) -> bool:
        """Create backup of registry"""
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_path / f"content_registry_backup_{timestamp}.json"
            
            # Export registry
            return self.export_registry(str(backup_file))
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def restore_registry(self, backup_file: str) -> bool:
        """Restore registry from backup"""
        try:
            # Create backup of current registry
            current_backup = f"content_registry_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.export_registry(current_backup)
            
            # Restore from backup
            return self.import_registry(backup_file)
            
        except Exception as e:
            print(f"Error restoring registry: {e}")
            return False
    
    def analyze_content_usage(self, days: int = 30) -> Dict[str, Any]:
        """Analyze content usage patterns"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        usage_report = {
            "analysis_period_days": days,
            "total_content": len(self.registry.content_registry),
            "active_content": 0,
            "unused_content": 0,
            "most_accessed": [],
            "least_accessed": [],
            "agent_activity": {},
            "type_usage": {}
        }
        
        access_times = []
        
        for file_path, metadata in self.registry.content_registry.items():
            last_accessed = datetime.fromisoformat(metadata.last_accessed)
            
            if last_accessed >= cutoff_date:
                usage_report["active_content"] += 1
            else:
                usage_report["unused_content"] += 1
            
            access_times.append((file_path, last_accessed, metadata.access_count))
            
            # Agent activity
            if metadata.agent_id not in usage_report["agent_activity"]:
                usage_report["agent_activity"][metadata.agent_id] = 0
            usage_report["agent_activity"][metadata.agent_id] += 1
            
            # Type usage
            content_type = metadata.content_type.value
            if content_type not in usage_report["type_usage"]:
                usage_report["type_usage"][content_type] = 0
            usage_report["type_usage"][content_type] += 1
        
        # Sort by access count and time
        access_times.sort(key=lambda x: (x[2], x[1]), reverse=True)
        
        usage_report["most_accessed"] = [
            {"file_path": fp, "last_accessed": la.isoformat(), "access_count": ac}
            for fp, la, ac in access_times[:10]
        ]
        
        usage_report["least_accessed"] = [
            {"file_path": fp, "last_accessed": la.isoformat(), "access_count": ac}
            for fp, la, ac in access_times[-10:]
        ]
        
        return usage_report
    
    def optimize_registry(self) -> Dict[str, Any]:
        """Optimize registry by removing invalid entries and consolidating data"""
        optimization_report = {
            "success": True,
            "removed_invalid": 0,
            "consolidated_duplicates": 0,
            "updated_metadata": 0,
            "errors": []
        }
        
        # Remove invalid entries
        invalid_files = []
        for file_path, metadata in self.registry.content_registry.items():
            if not Path(file_path).exists():
                invalid_files.append(file_path)
        
        for file_path in invalid_files:
            del self.registry.content_registry[file_path]
            optimization_report["removed_invalid"] += 1
        
        # Update metadata for existing files
        for file_path, metadata in self.registry.content_registry.items():
            try:
                file_path_obj = Path(file_path)
                if file_path_obj.exists():
                    stat = file_path_obj.stat()
                    
                    # Update file size and modification time
                    metadata.file_size = stat.st_size
                    metadata.last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
                    
                    # Recalculate quality score and V2 compliance
                    metadata.quality_score = self.registry.calculate_quality_score(file_path, metadata.content_type)
                    metadata.v2_compliant = self.registry.check_v2_compliance(file_path)
                    
                    optimization_report["updated_metadata"] += 1
                    
            except Exception as e:
                optimization_report["errors"].append(f"Error updating {file_path}: {e}")
        
        # Save optimized registry
        if optimization_report["removed_invalid"] > 0 or optimization_report["updated_metadata"] > 0:
            self.registry.manage_registry_operations("save")
        
        return optimization_report
