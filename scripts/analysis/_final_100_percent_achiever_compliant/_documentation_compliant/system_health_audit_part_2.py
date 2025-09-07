"""
system_health_audit_part_2.py
Module: system_health_audit_part_2.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:16
"""

# Part 2 of system_health_audit.py
# Original file: .\scripts\analysis\system_health_audit.py

            
            # Calculate integrity score
            integrity_score = 100 if json_valid else 0
            
            return {
                "status": "VALID" if json_valid else "CORRUPTED",
                "checksum": checksum,
                "file_size": len(content),
                "json_valid": json_valid,
                "json_error": json_error,
                "integrity_score": integrity_score,
                "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            }
            
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "integrity_score": 0
            }
    
    def validate_contract_system_integrity(self) -> Dict[str, Any]:
        """Validate contract system data integrity between task_list.json and meeting.json"""
        logger.info("🔍 Validating contract system integrity...")
        
        # Validate both files
        task_list_integrity = self.validate_file_integrity(self.task_list_path)
        meeting_integrity = self.validate_file_integrity(self.meeting_json_path)
        
        if task_list_integrity["status"] != "VALID" or meeting_integrity["status"] != "VALID":
            self.corruption_detected = True
            self.corruption_details.append({
                "type": "FILE_CORRUPTION",
                "task_list": task_list_integrity,
                "meeting_json": meeting_integrity
            })
            return {
                "status": "CORRUPTED",
                "task_list": task_list_integrity,
                "meeting_json": meeting_integrity,
                "corruption_detected": True
            }
        
        # Load and compare contract counts
        try:
            with open(self.task_list_path, 'r') as f:
                task_list_data = json.load(f)
            
            with open(self.meeting_json_path, 'r') as f:
                meeting_data = json.load(f)

