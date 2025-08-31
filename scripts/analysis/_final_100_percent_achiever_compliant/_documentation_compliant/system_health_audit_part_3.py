"""
system_health_audit_part_3.py
Module: system_health_audit_part_3.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:16
"""

# Part 3 of system_health_audit.py
# Original file: .\scripts\analysis\system_health_audit.py

            
            # Extract contract counts
            task_list_counts = {
                "total": task_list_data.get("total_contracts", 0),
                "available": task_list_data.get("available_contracts", 0),
                "claimed": task_list_data.get("claimed_contracts", 0),
                "completed": task_list_data.get("completed_contracts", 0)
            }
            
            meeting_counts = {
                "total": meeting_data.get("contract_system_status", {}).get("total_contracts", 0),
                "available": meeting_data.get("contract_system_status", {}).get("available", 0),
                "claimed": meeting_data.get("contract_system_status", {}).get("claimed", 0),
                "completed": meeting_data.get("contract_system_status", {}).get("completed", 0)
            }
            
            # Check for discrepancies
            discrepancies = []
            for key in task_list_counts:
                if task_list_counts[key] != meeting_counts[key]:
                    discrepancies.append({
                        "field": key,
                        "task_list": task_list_counts[key],
                        "meeting_json": meeting_counts[key],
                        "difference": abs(task_list_counts[key] - meeting_counts[key])
                    })
            
            if discrepancies:
                self.corruption_detected = True
                self.corruption_details.append({
                    "type": "CONTRACT_COUNT_MISMATCH",
                    "discrepancies": discrepancies
                })
                
                return {
                    "status": "CORRUPTED",
                    "task_list_counts": task_list_counts,
                    "meeting_counts": meeting_counts,
                    "discrepancies": discrepancies,
                    "corruption_detected": True
                }
            
            return {
                "status": "VALID",
                "task_list_counts": task_list_counts,
                "meeting_counts": meeting_counts,
                "discrepancies": [],
                "corruption_detected": False
            }
            

