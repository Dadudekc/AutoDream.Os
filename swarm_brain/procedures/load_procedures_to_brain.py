#!/usr/bin/env python3
"""
Load Documented Procedures into Swarm Brain
============================================

Loads all procedure files into the Swarm Brain knowledge base.

Author: Agent-5 (Memory Safety & Performance Engineer)
Date: 2025-10-14
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.swarm_brain.swarm_memory import SwarmMemory

def load_procedures():
    """Load all procedures into Swarm Brain."""
    
    memory = SwarmMemory(agent_id='Agent-5')
    procedures_dir = Path(__file__).parent
    
    procedures = [
        "PROCEDURE_AGENT_ONBOARDING.md",
        "PROCEDURE_CONFIG_SSOT_VALIDATION.md",
        "PROCEDURE_DISCORD_SETUP.md",
        "PROCEDURE_V2_COMPLIANCE_CHECK.md",
        "PROCEDURE_PROJECT_SCANNING.md",
        "PROCEDURE_GIT_COMMIT_WORKFLOW.md",
        "PROCEDURE_MESSAGE_AGENT.md",
        "PROCEDURE_SWARM_BRAIN_CONTRIBUTION.md",
        "PROCEDURE_EMERGENCY_RESPONSE.md",
        "PROCEDURE_MEMORY_LEAK_DEBUGGING.md",
        "PROCEDURE_FILE_REFACTORING.md",
        "PROCEDURE_TEST_EXECUTION.md",
        "PROCEDURE_DEPLOYMENT_WORKFLOW.md",
        "PROCEDURE_CODE_REVIEW.md",
        "PROCEDURE_PERFORMANCE_OPTIMIZATION.md",
    ]
    
    print("📚 Loading Procedures into Swarm Brain...")
    print("=" * 60)
    
    loaded_count = 0
    for proc_file in procedures:
        proc_path = procedures_dir / proc_file
        
        if not proc_path.exists():
            print(f"⚠️  Skipped: {proc_file} (not found)")
            continue
        
        # Read procedure content
        content = proc_path.read_text(encoding='utf-8')
        
        # Extract title from filename
        title = proc_file.replace("PROCEDURE_", "").replace(".md", "").replace("_", " ").title()
        
        # Extract category from first line
        category = "procedure"
        
        # Determine tags from filename
        tags = ["procedure", proc_file.replace("PROCEDURE_", "").replace(".md", "").lower()]
        
        # Add to Swarm Brain
        memory.share_learning(
            title=f"PROCEDURE: {title}",
            content=content,
            tags=tags
        )
        
        loaded_count += 1
        print(f"✅ Loaded: {title}")
    
    print("=" * 60)
    print(f"🎯 TOTAL LOADED: {loaded_count} procedures")
    print("✅ All procedures now searchable in Swarm Brain!")
    print()
    print("Test with:")
    print("  python -c \"from src.swarm_brain.swarm_memory import SwarmMemory; m = SwarmMemory('Agent-X'); print(len(m.search_swarm_knowledge('procedure')))\"")

if __name__ == "__main__":
    load_procedures()

