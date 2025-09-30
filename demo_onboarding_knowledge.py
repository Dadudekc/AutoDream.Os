#!/usr/bin/env python3
"""
Onboarding Knowledge Query Demonstration
=======================================

Demonstrate how to query all the onboarding documentation and agent definitions
from the vector database.

Author: Agent-4 (Captain & Operations Coordinator)
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from onboarding_knowledge_demo_core import OnboardingKnowledgeDemo


def main():
    """Demonstrate onboarding knowledge queries."""
    demo = OnboardingKnowledgeDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()