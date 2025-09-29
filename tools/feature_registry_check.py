#!/usr/bin/env python3
"""
Feature Registry Check Tool
===========================

Automated tool to check for feature duplication before development.
Part of the Duplication Prevention Protocol.

Author: Agent 5 (Quality Assurance Specialist)
License: MIT
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logger = __import__("logging").getLogger(__name__)


class FeatureRegistry:
    """Feature registry for tracking existing capabilities."""

    def __init__(self, registry_file: str = "FEATURE_REGISTRY.json"):
        """Initialize feature registry."""
        self.registry_file = Path(registry_file)
        self.registry = self._load_registry()

    def _load_registry(self) -> dict[str, Any]:
        """Load feature registry from file."""
        if self.registry_file.exists():
            with open(self.registry_file) as f:
                return json.load(f)
        return self._create_default_registry()

    def _create_default_registry(self) -> dict[str, Any]:
        """Create default feature registry."""
        return {
            "features": {
                "messaging": {
                    "name": "Consolidated Messaging Service",
                    "owner": "Agent 2",
                    "status": "operational",
                    "files": ["src/services/consolidated_messaging_service.py"],
                    "description": "PyAutoGUI-based agent coordination system",
                    "last_updated": "2025-09-21",
                },
                "ml_pipeline": {
                    "name": "ML Pipeline System",
                    "owner": "Agent 3",
                    "status": "operational",
                    "files": ["src/ml/ml_pipeline_system.py"],
                    "description": "TensorFlow/PyTorch ML pipeline with deployment",
                    "last_updated": "2025-09-21",
                },
                "tracing": {
                    "name": "Distributed Tracing System",
                    "owner": "Agent 4",
                    "status": "operational",
                    "files": ["src/tracing/distributed_tracing_system.py"],
                    "description": "OpenTelemetry + Jaeger tracing system",
                    "last_updated": "2025-09-21",
                },
                "web_dashboard": {
                    "name": "Swarm Coordination Dashboard",
                    "owner": "Agent 4",
                    "status": "operational",
                    "files": ["src/services/dashboard/"],
                    "description": "Real-time monitoring and coordination dashboard",
                    "last_updated": "2025-09-21",
                },
                "mobile_framework": {
                    "name": "Mobile App Framework",
                    "owner": "Agent 5",
                    "status": "built",
                    "files": ["src/mobile/"],
                    "description": "React Native mobile application framework",
                    "last_updated": "2025-09-21",
                },
                "api_gateway": {
                    "name": "API Gateway Core",
                    "owner": "Agent 2",
                    "status": "operational",
                    "files": ["src/services/api_gateway/"],
                    "description": "Authentication and rate limiting gateway",
                    "last_updated": "2025-09-21",
                },
                "nlp_system": {
                    "name": "Command Understanding",
                    "owner": "Agent 2",
                    "status": "basic",
                    "files": ["src/services/messaging/"],
                    "description": "Pattern-based command parsing system",
                    "last_updated": "2025-09-21",
                },
                "cloud_infrastructure": {
                    "name": "Cloud Configuration System",
                    "owner": "Agent 1",
                    "status": "basic",
                    "files": ["src/infrastructure/cloud/"],
                    "description": "AWS/Azure configuration management",
                    "last_updated": "2025-09-21",
                },
            },
            "last_updated": "2025-09-21",
        }

    def save_registry(self):
        """Save registry to file."""
        with open(self.registry_file, "w") as f:
            json.dump(self.registry, f, indent=2)

    def check_feature_duplication(self, feature_name: str, description: str = "") -> dict[str, Any]:
        """Check if feature already exists or duplicates existing functionality."""
        result = {
            "feature_exists": False,
            "similar_features": [],
            "duplication_risk": "low",
            "recommendation": "proceed",
            "details": [],
        }

        # Check for exact matches
        for feature_id, feature in self.registry["features"].items():
            if feature_id.lower() == feature_name.lower():
                result["feature_exists"] = True
                result["details"].append(f"Exact match found: {feature['name']}")
                result["recommendation"] = "integrate_with_existing"
                return result

        # Check for similar functionality
        feature_keywords = set(feature_name.lower().split())
        for feature_id, feature in self.registry["features"].items():
            feature_desc = feature["description"].lower()
            overlap = len(feature_keywords.intersection(set(feature_desc.split())))

            if overlap > 0:
                similarity = overlap / len(feature_keywords)
                if similarity > 0.5:
                    result["similar_features"].append(
                        {
                            "feature_id": feature_id,
                            "name": feature["name"],
                            "similarity": similarity,
                            "description": feature["description"],
                        }
                    )

        # Assess duplication risk
        if result["similar_features"]:
            max_similarity = max(f["similarity"] for f in result["similar_features"])
            if max_similarity > 0.8:
                result["duplication_risk"] = "high"
                result["recommendation"] = "review_existing_first"
            elif max_similarity > 0.6:
                result["duplication_risk"] = "medium"
                result["recommendation"] = "consider_integration"

        return result

    def register_new_feature(
        self,
        feature_name: str,
        owner: str,
        description: str,
        files: list[str],
        status: str = "planned",
    ) -> bool:
        """Register a new feature in the registry."""
        feature_id = feature_name.lower().replace(" ", "_")

        self.registry["features"][feature_id] = {
            "name": feature_name,
            "owner": owner,
            "status": status,
            "files": files,
            "description": description,
            "last_updated": str(__import__("datetime").date.today()),
        }

        self.save_registry()
        return True


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Feature Registry Check Tool")
    parser.add_argument("--feature", required=True, help="Feature name to check")
    parser.add_argument("--description", default="", help="Feature description")
    parser.add_argument("--check-duplication", action="store_true", help="Check for duplication")
    parser.add_argument("--register", action="store_true", help="Register new feature")

    args = parser.parse_args()

    registry = FeatureRegistry()

    if args.check_duplication:
        result = registry.check_feature_duplication(args.feature, args.description)

        print(f"\n🔍 FEATURE DUPLICATION CHECK: {args.feature}")
        print("=" * 50)
        print(f"Feature Exists: {'❌' if result['feature_exists'] else '✅'}")

        if result["similar_features"]:
            print(f"\nSimilar Features Found: {len(result['similar_features'])}")
            for similar in result["similar_features"]:
                print(f"  • {similar['name']} (Similarity: {similar['similarity']:.1%})")
                print(f"    {similar['description']}")

        print(f"\nDuplication Risk: {result['duplication_risk'].upper()}")
        print(f"Recommendation: {result['recommendation'].replace('_', ' ').upper()}")

        if result["details"]:
            print("Details:")
            for detail in result["details"]:
                print(f"  • {detail}")

        # Exit with error code if high duplication risk
        if result["duplication_risk"] == "high":
            print("❌ HIGH DUPLICATION RISK - Review existing features first!")
            return 1

    if args.register:
        print(f"\n📝 REGISTERING NEW FEATURE: {args.feature}")
        success = registry.register_new_feature(
            feature_name=args.feature,
            owner="Agent-X",  # TODO: Get from environment
            description=args.description,
            files=[],  # TODO: Get from command line
        )

        if success:
            print("✅ Feature registered successfully")
        else:
            print("❌ Failed to register feature")
            return 1

    return 0


if __name__ == "__main__":
    exit(main())
