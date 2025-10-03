"""
Documentation Bloat Eliminator - V2 Compliant
=============================================

Eliminates redundant and unnecessary documentation files.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict


class DocumentationBloatEliminator:
    """Eliminates documentation bloat."""
    
    def __init__(self):
        """Initialize documentation bloat eliminator."""
        self.eliminated_files = []
        self.time_saved = 0.0
    
    def identify_redundant_docs(self) -> List[Path]:
        """Identify redundant documentation files."""
        redundant_patterns = [
            "*documentation*.md",
            "*DOCUMENTATION*.md", 
            "*summary*.md",
            "*SUMMARY*.md",
            "*report*.md",
            "*REPORT*.md",
            "*analysis*.md",
            "*ANALYSIS*.md",
            "*integration*.md",
            "*INTEGRATION*.md",
            "*status*.md",
            "*STATUS*.md",
            "*update*.md",
            "*UPDATE*.md",
            "*completion*.md",
            "*COMPLETION*.md",
            "*passdown*.md",
            "*PASSDOWN*.md",
            "*guide*.md",
            "*GUIDE*.md",
            "*setup*.md",
            "*SETUP*.md",
            "*instructions*.md",
            "*INSTRUCTIONS*.md"
        ]
        
        redundant_files = []
        for pattern in redundant_patterns:
            redundant_files.extend(Path(".").glob(pattern))
        
        # Filter out essential files
        essential_files = {
            "README.md",
            "CHANGELOG.md", 
            "DEVELOPMENT_GUIDELINES.md",
            "QUALITY_COMPLIANCE.md",
            "ANTI_SLOP_PROTOCOL.md",
            "ANTI_AI_SLOP_PROTOCOL.md",
            "GENERAL_CYCLE.md",
            "SWARM_COORDINATION.md",
            "TOOL_INTEGRATION.md",
            "NAMING_STANDARDS.md",
            "SECURITY_GUIDELINES.md",
            "STATIC_ANALYSIS_SETUP.md"
        }
        
        # Remove essential files from redundant list
        redundant_files = [f for f in redundant_files if f.name not in essential_files]
        
        return redundant_files
    
    def eliminate_redundant_docs(self, dry_run: bool = True) -> Dict:
        """Eliminate redundant documentation files."""
        redundant_files = self.identify_redundant_docs()
        
        eliminated_count = 0
        total_size = 0
        
        for file_path in redundant_files:
            try:
                # Calculate file size
                file_size = file_path.stat().st_size
                total_size += file_size
                
                if not dry_run:
                    # Move to backup directory
                    backup_dir = Path("documentation_backup")
                    backup_dir.mkdir(exist_ok=True)
                    
                    backup_path = backup_dir / file_path.name
                    shutil.move(str(file_path), str(backup_path))
                    
                    self.eliminated_files.append(file_path)
                    eliminated_count += 1
                    
                    print(f"Eliminated: {file_path}")
                else:
                    print(f"Would eliminate: {file_path} ({file_size} bytes)")
                    eliminated_count += 1
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # Calculate time saved (estimate 10 minutes per file)
        self.time_saved = eliminated_count * 10.0
        
        return {
            "files_eliminated": eliminated_count,
            "total_size_bytes": total_size,
            "time_saved_minutes": self.time_saved,
            "eliminated_files": self.eliminated_files
        }
    
    def eliminate_duplicate_content(self, dry_run: bool = True) -> Dict:
        """Eliminate files with duplicate content."""
        md_files = list(Path(".").glob("**/*.md"))
        
        content_map = {}
        duplicates = []
        
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Normalize content for comparison
                    normalized_content = content.lower().strip()
                    
                    if normalized_content in content_map:
                        duplicates.append(file_path)
                    else:
                        content_map[normalized_content] = file_path
                        
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        eliminated_count = 0
        for duplicate_file in duplicates:
            try:
                if not dry_run:
                    backup_dir = Path("documentation_backup")
                    backup_dir.mkdir(exist_ok=True)
                    
                    backup_path = backup_dir / duplicate_file.name
                    shutil.move(str(duplicate_file), str(backup_path))
                    
                    self.eliminated_files.append(duplicate_file)
                    eliminated_count += 1
                    
                    print(f"Eliminated duplicate: {duplicate_file}")
                else:
                    print(f"Would eliminate duplicate: {duplicate_file}")
                    eliminated_count += 1
                    
            except Exception as e:
                print(f"Error processing duplicate {duplicate_file}: {e}")
        
        return {
            "duplicates_eliminated": eliminated_count,
            "time_saved_minutes": eliminated_count * 5.0
        }
    
    def get_elimination_summary(self) -> Dict:
        """Get documentation elimination summary."""
        return {
            "total_files_eliminated": len(self.eliminated_files),
            "total_time_saved": self.time_saved,
            "eliminated_files": [str(f) for f in self.eliminated_files]
        }


def main():
    """CLI entry point for documentation bloat elimination."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Documentation Bloat Eliminator")
    parser.add_argument("--eliminate-redundant", action="store_true", help="Eliminate redundant documentation")
    parser.add_argument("--eliminate-duplicates", action="store_true", help="Eliminate duplicate content")
    parser.add_argument("--eliminate-all", action="store_true", help="Eliminate all documentation bloat")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be eliminated without actually doing it")
    parser.add_argument("--summary", action="store_true", help="Show elimination summary")
    
    args = parser.parse_args()
    
    eliminator = DocumentationBloatEliminator()
    
    if args.eliminate_redundant:
        result = eliminator.eliminate_redundant_docs(dry_run=args.dry_run)
        print(f"Redundant docs {'would be' if args.dry_run else ''} eliminated: {result['files_eliminated']}")
        print(f"Time saved: {result['time_saved_minutes']:.1f} minutes")
    
    elif args.eliminate_duplicates:
        result = eliminator.eliminate_duplicate_content(dry_run=args.dry_run)
        print(f"Duplicate files {'would be' if args.dry_run else ''} eliminated: {result['duplicates_eliminated']}")
        print(f"Time saved: {result['time_saved_minutes']:.1f} minutes")
    
    elif args.eliminate_all:
        print("Eliminating all documentation bloat...")
        redundant_result = eliminator.eliminate_redundant_docs(dry_run=args.dry_run)
        duplicate_result = eliminator.eliminate_duplicate_content(dry_run=args.dry_run)
        
        total_eliminated = redundant_result['files_eliminated'] + duplicate_result['duplicates_eliminated']
        total_time_saved = redundant_result['time_saved_minutes'] + duplicate_result['time_saved_minutes']
        
        print(f"Total files {'would be' if args.dry_run else ''} eliminated: {total_eliminated}")
        print(f"Total time saved: {total_time_saved:.1f} minutes")
    
    elif args.summary:
        eliminator.eliminate_redundant_docs(dry_run=True)
        eliminator.eliminate_duplicate_content(dry_run=True)
        summary = eliminator.get_elimination_summary()
        print("Documentation Elimination Summary:")
        print(f"  Files that would be eliminated: {summary['total_files_eliminated']}")
        print(f"  Time that would be saved: {summary['total_time_saved']:.1f} minutes")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

