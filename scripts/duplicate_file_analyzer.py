#!/usr/bin/env python3
"""
Duplicate File Analyzer - V2 Compliance System
Identifies and prioritizes duplicate files for consolidation
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict
from datetime import datetime


class DuplicateFileAnalyzer:
    """Advanced duplicate file analysis system for V2 compliance"""
    
    def __init__(self):
        """Initialize the duplicate file analyzer."""
        self.file_hashes = {}
        self.duplicate_groups = defaultdict(list)
        self.analysis_results = {}
        self.priority_scores = {}
        
        # File type priorities (higher = more critical)
        self.file_type_priorities = {
            '.py': 10,      # Python source files - highest priority
            '.json': 8,     # Configuration files
            '.md': 6,       # Documentation files
            '.yaml': 7,     # YAML configuration files
            '.yml': 7,      # YAML configuration files
            '.txt': 5,      # Text files
            '.ini': 6,      # Configuration files
            '.cfg': 6,      # Configuration files
            '.toml': 8,     # TOML configuration files
            '.xml': 5,      # XML files
            '.html': 4,     # HTML files
            '.css': 3,      # CSS files
            '.js': 4,       # JavaScript files
            '.sql': 7,      # Database files
            '.sh': 6,       # Shell scripts
            '.ps1': 6,      # PowerShell scripts
            '.bat': 5,      # Batch files
            '.exe': 1,      # Executables - lowest priority
            '.dll': 1,      # Libraries - lowest priority
            '.so': 1,       # Shared objects - lowest priority
        }
        
        # Directory priorities (higher = more critical)
        self.directory_priorities = {
            'src/': 10,           # Source code - highest priority
            'emergency_database_recovery/': 9,  # Critical systems
            'agent_workspaces/': 8,  # Agent workspaces
            'config/': 8,         # Configuration files
            'tests/': 7,          # Test files
            'scripts/': 7,        # Script files
            'tools/': 6,          # Tool files
            'docs/': 6,           # Documentation
            'examples/': 5,       # Example files
            'data/': 5,           # Data files
            'logs/': 2,           # Log files - low priority
            'build/': 1,          # Build artifacts - lowest priority
            'dist/': 1,           # Distribution files - lowest priority
            '__pycache__/': 0,    # Python cache - ignore
            '.git/': 0,           # Git files - ignore
            'venv/': 0,           # Virtual environment - ignore
            '.venv/': 0,          # Virtual environment - ignore
        }
        
        # Exclusion patterns
        self.exclude_patterns = [
            '*/__pycache__/*',
            '*/venv/*',
            '*/.venv/*',
            '*/build/*',
            '*/dist/*',
            '*/.git/*',
            '*/node_modules/*',
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '*.log',
            '*.tmp',
            '*.cache',
            '*.bak',
            '*.backup'
        ]
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file content."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def get_file_priority_score(self, file_path: Path) -> float:
        """Calculate priority score for a file based on type and location."""
        score = 0.0
        
        # File type priority
        file_ext = file_path.suffix.lower()
        if file_ext in self.file_type_priorities:
            score += self.file_type_priorities[file_ext] * 10
        
        # Directory priority
        file_str = str(file_path)
        for dir_pattern, priority in self.directory_priorities.items():
            if dir_pattern in file_str:
                score += priority * 5
                break
        
        # Size factor (larger files get higher priority)
        try:
            file_size = file_path.stat().st_size
            if file_size > 1024 * 1024:  # > 1MB
                score += 20
            elif file_size > 100 * 1024:  # > 100KB
                score += 10
            elif file_size > 10 * 1024:   # > 10KB
                score += 5
        except:
            pass
        
        # Recency factor (newer files get higher priority)
        try:
            mtime = file_path.stat().st_mtime
            days_old = (datetime.now().timestamp() - mtime) / (24 * 3600)
            if days_old < 7:      # < 1 week
                score += 15
            elif days_old < 30:   # < 1 month
                score += 10
            elif days_old < 90:   # < 3 months
                score += 5
        except:
            pass
        
        return score
    
    def scan_for_duplicates(self, root_path: str = ".") -> Dict[str, Any]:
        """Scan repository for duplicate files."""
        print("🔍 Scanning repository for duplicate files...")
        
        root = Path(root_path)
        total_files = 0
        processed_files = 0
        
        # Count total files first
        for file_path in root.rglob('*'):
            if file_path.is_file():
                total_files += 1
        
        print(f"📊 Total files to scan: {total_files}")
        
        # Scan files and calculate hashes
        for file_path in root.rglob('*'):
            if not file_path.is_file():
                continue
                
            # Check exclusion patterns
            if any(pattern.replace('*', '') in str(file_path) for pattern in self.exclude_patterns):
                continue
            
            processed_files += 1
            if processed_files % 100 == 0:
                print(f"   Progress: {processed_files}/{total_files} files processed")
            
            file_hash = self.calculate_file_hash(file_path)
            if file_hash:
                self.file_hashes[str(file_path)] = file_hash
                self.duplicate_groups[file_hash].append(str(file_path))
        
        print(f"✅ Scan complete: {processed_files} files processed")
        return self._analyze_duplicates()
    
    def _analyze_duplicates(self) -> Dict[str, Any]:
        """Analyze duplicate files and generate priority scores."""
        print("📊 Analyzing duplicate files...")
        
        # Filter groups with actual duplicates
        actual_duplicates = {
            hash_val: files for hash_val, files in self.duplicate_groups.items()
            if len(files) > 1
        }
        
        print(f"🔍 Found {len(actual_duplicates)} duplicate groups")
        
        # Calculate priority scores for each duplicate group
        for hash_val, files in actual_duplicates.items():
            group_score = 0
            file_details = []
            
            for file_path in files:
                path_obj = Path(file_path)
                priority_score = self.get_file_priority_score(path_obj)
                group_score += priority_score
                
                try:
                    file_size = path_obj.stat().st_size
                    mtime = path_obj.stat().st_mtime
                    file_details.append({
                        "path": file_path,
                        "priority_score": priority_score,
                        "size_bytes": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2),
                        "modified": datetime.fromtimestamp(mtime).isoformat(),
                        "relative_path": str(path_obj.relative_to(Path.cwd()))
                    })
                except Exception as e:
                    file_details.append({
                        "path": file_path,
                        "priority_score": priority_score,
                        "error": str(e)
                    })
            
            # Sort files by priority score (highest first)
            file_details.sort(key=lambda x: x.get('priority_score', 0), reverse=True)
            
            self.analysis_results[hash_val] = {
                "duplicate_count": len(files),
                "total_priority_score": group_score,
                "average_priority_score": round(group_score / len(files), 2),
                "files": file_details,
                "consolidation_priority": self._get_consolidation_priority(group_score, len(files))
            }
        
        # Sort results by consolidation priority
        sorted_results = dict(sorted(
            self.analysis_results.items(),
            key=lambda x: x[1]['consolidation_priority'],
            reverse=True
        ))
        
        return {
            "scan_timestamp": datetime.now().isoformat(),
            "total_files_scanned": len(self.file_hashes),
            "duplicate_groups_found": len(actual_duplicates),
            "total_duplicate_files": sum(len(files) for files in actual_duplicates.values()),
            "potential_space_savings_mb": self._calculate_space_savings(actual_duplicates),
            "priority_analysis": sorted_results,
            "summary_by_priority": self._generate_priority_summary(sorted_results)
        }
    
    def _get_consolidation_priority(self, total_score: float, file_count: int) -> str:
        """Determine consolidation priority based on score and file count."""
        if total_score >= 100 and file_count >= 5:
            return "CRITICAL"
        elif total_score >= 80 and file_count >= 3:
            return "HIGH"
        elif total_score >= 60 and file_count >= 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_space_savings(self, duplicates: Dict[str, List[str]]) -> float:
        """Calculate potential space savings from consolidation."""
        total_savings = 0
        
        for files in duplicates.values():
            if len(files) > 1:
                # Keep one file, remove the rest
                try:
                    first_file_size = Path(files[0]).stat().st_size
                    savings = first_file_size * (len(files) - 1)
                    total_savings += savings
                except:
                    continue
        
        return round(total_savings / (1024 * 1024), 2)  # Convert to MB
    
    def _generate_priority_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics by priority level."""
        summary = {
            "CRITICAL": {"count": 0, "files": 0, "total_score": 0},
            "HIGH": {"count": 0, "files": 0, "total_score": 0},
            "MEDIUM": {"count": 0, "files": 0, "total_score": 0},
            "LOW": {"count": 0, "files": 0, "total_score": 0}
        }
        
        for group_data in results.values():
            priority = group_data["consolidation_priority"]
            summary[priority]["count"] += 1
            summary[priority]["files"] += group_data["duplicate_count"]
            summary[priority]["total_score"] += group_data["total_priority_score"]
        
        return summary
    
    def generate_captain_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate detailed report for Captain Agent-4."""
        report = []
        report.append("# 🚨 DUPLICATE FILE ANALYSIS REPORT - AGENT-2")
        report.append("")
        report.append("## 📋 **EXECUTIVE SUMMARY**")
        report.append("")
        report.append(f"**Scan Timestamp:** {analysis_results['scan_timestamp']}")
        report.append(f"**Total Files Scanned:** {analysis_results['total_files_scanned']:,}")
        report.append(f"**Duplicate Groups Found:** {analysis_results['duplicate_groups_found']}")
        report.append(f"**Total Duplicate Files:** {analysis_results['total_duplicate_files']:,}")
        report.append(f"**Potential Space Savings:** {analysis_results['potential_space_savings_mb']} MB")
        report.append("")
        
        # Priority Summary
        report.append("## 🎯 **CONSOLIDATION PRIORITY BREAKDOWN**")
        report.append("")
        summary = analysis_results['summary_by_priority']
        
        for priority in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            data = summary[priority]
            if data["count"] > 0:
                report.append(f"### **{priority} PRIORITY:** {data['count']} groups, {data['files']} files")
                report.append(f"- **Groups:** {data['count']}")
                report.append(f"- **Total Files:** {data['files']}")
                report.append(f"- **Average Score:** {round(data['total_score'] / data['count'], 1) if data['count'] > 0 else 0}")
                report.append("")
        
        # Top 10 Critical Duplicates
        report.append("## 🚨 **TOP 10 CRITICAL DUPLICATES - IMMEDIATE ACTION REQUIRED**")
        report.append("")
        
        critical_count = 0
        for hash_val, group_data in analysis_results['priority_analysis'].items():
            if group_data['consolidation_priority'] == "CRITICAL" and critical_count < 10:
                critical_count += 1
                report.append(f"### **{critical_count}. Duplicate Group (Score: {group_data['total_priority_score']})**")
                report.append(f"- **Files:** {group_data['duplicate_count']}")
                report.append(f"- **Priority:** {group_data['consolidation_priority']}")
                report.append("")
                
                # Show file details
                for i, file_info in enumerate(group_data['files'][:5]):  # Show first 5 files
                    report.append(f"  **{i+1}.** `{file_info.get('relative_path', file_info['path'])}`")
                    report.append(f"      - Size: {file_info.get('size_mb', 'N/A')} MB")
                    report.append(f"      - Score: {file_info.get('priority_score', 'N/A')}")
                    report.append(f"      - Modified: {file_info.get('modified', 'N/A')}")
                    report.append("")
                
                if group_data['duplicate_count'] > 5:
                    report.append(f"  *... and {group_data['duplicate_count'] - 5} more duplicate files*")
                    report.append("")
        
        # Recommendations
        report.append("## 💡 **IMMEDIATE ACTION RECOMMENDATIONS**")
        report.append("")
        report.append("### **Phase 1 (0-24 hours): CRITICAL PRIORITY**")
        report.append("1. **Immediate Consolidation:** Address all CRITICAL priority duplicates")
        report.append("2. **Space Recovery:** Target {analysis_results['potential_space_savings_mb']} MB savings")
        report.append("3. **Priority Assessment:** Review HIGH priority groups for immediate action")
        report.append("")
        
        report.append("### **Phase 2 (1-7 days): HIGH PRIORITY**")
        report.append("1. **Systematic Review:** Analyze all HIGH priority duplicate groups")
        report.append("2. **Consolidation Planning:** Develop consolidation strategies")
        report.append("3. **Backup Verification:** Ensure safe consolidation procedures")
        report.append("")
        
        report.append("### **Phase 3 (1-4 weeks): MEDIUM/LOW PRIORITY**")
        report.append("1. **Long-term Planning:** Address remaining duplicate groups")
        report.append("2. **Prevention Measures:** Implement duplicate detection systems")
        report.append("3. **Documentation:** Create consolidation guidelines")
        report.append("")
        
        # Technical Details
        report.append("## 🔧 **TECHNICAL ANALYSIS DETAILS**")
        report.append("")
        report.append("### **Priority Scoring Factors:**")
        report.append("- **File Type:** Python (.py) = 100, JSON (.json) = 80, etc.")
        report.append("- **Directory Location:** src/ = 50, config/ = 40, etc.")
        report.append("- **File Size:** >1MB = 20, >100KB = 10, >10KB = 5")
        report.append("- **Recency:** <1 week = 15, <1 month = 10, <3 months = 5")
        report.append("")
        
        report.append("### **Consolidation Priority Levels:**")
        report.append("- **CRITICAL:** Score ≥100 + ≥5 files")
        report.append("- **HIGH:** Score ≥80 + ≥3 files")
        report.append("- **MEDIUM:** Score ≥60 + ≥2 files")
        report.append("- **LOW:** All other duplicates")
        report.append("")
        
        # Footer
        report.append("---")
        report.append("**Agent-2 (Phase Transition Optimization Manager)**")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}")
        report.append("**Status:** ✅ **DUPLICATE ANALYSIS COMPLETE - IMMEDIATE ACTION REQUIRED**")
        
        return "\n".join(report)
    
    def save_analysis_report(self, analysis_results: Dict[str, Any], output_file: str = None) -> None:
        """Save analysis results to JSON file."""
        if output_file is None:
            output_file = f"reports/duplicate_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Analysis report saved to: {output_path}")
    
    def save_captain_report(self, captain_report: str, output_file: str = None) -> None:
        """Save Captain Agent-4 report to markdown file."""
        if output_file is None:
            output_file = f"reports/CAPTAIN_DUPLICATE_ANALYSIS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(captain_report)
        
        print(f"📋 Captain report saved to: {output_path}")


def main():
    """Main entry point for duplicate file analyzer."""
    print("🚀 Starting Duplicate File Analysis for V2 Compliance...")
    
    analyzer = DuplicateFileAnalyzer()
    
    # Scan for duplicates
    analysis_results = analyzer.scan_for_duplicates()
    
    # Generate Captain Agent-4 report
    captain_report = analyzer.generate_captain_report(analysis_results)
    
    # Save reports
    analyzer.save_analysis_report(analysis_results)
    analyzer.save_captain_report(captain_report)
    
    # Print summary
    print("\n" + "="*80)
    print("🎯 DUPLICATE ANALYSIS COMPLETE - CAPTAIN AGENT-4 REPORT READY")
    print("="*80)
    print(f"📊 Total files scanned: {analysis_results['total_files_scanned']:,}")
    print(f"🔍 Duplicate groups found: {analysis_results['duplicate_groups_found']}")
    print(f"💾 Potential space savings: {analysis_results['potential_space_savings_mb']} MB")
    print(f"🚨 Critical priority groups: {analysis_results['summary_by_priority']['CRITICAL']['count']}")
    print(f"⚠️  High priority groups: {analysis_results['summary_by_priority']['HIGH']['count']}")
    print("="*80)
    
    # Show top 3 critical duplicates
    print("\n🚨 TOP 3 CRITICAL DUPLICATES:")
    critical_count = 0
    for hash_val, group_data in analysis_results['priority_analysis'].items():
        if group_data['consolidation_priority'] == "CRITICAL" and critical_count < 3:
            critical_count += 1
            print(f"\n{critical_count}. Score: {group_data['total_priority_score']}, Files: {group_data['duplicate_count']}")
            for file_info in group_data['files'][:3]:
                print(f"   - {file_info.get('relative_path', file_info['path'])} ({file_info.get('size_mb', 'N/A')} MB)")


if __name__ == "__main__":
    main()
