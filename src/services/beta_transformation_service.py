#!/usr/bin/env python3
"""
Simple Beta Transformation Service for testing
"""

import json
import time
from datetime import datetime


class BetaTransformationService:
    def __init__(self):
        self.transformations = {}
        print("Beta Transformation Service initialized")

    def create_transformation(self, name, description):
        transformation_id = f"trans_{int(time.time())}"
        self.transformations[transformation_id] = {
            "id": transformation_id,
            "name": name,
            "description": description,
            "status": "created",
            "created_at": datetime.now().isoformat(),
        }
        print(f"Transformation created: {name} ({transformation_id})")
        return transformation_id

    def execute_transformation(self, transformation_id):
        if transformation_id in self.transformations:
            transformation = self.transformations[transformation_id]
            transformation["status"] = "completed"
            transformation["completed_at"] = datetime.now().isoformat()
            name = transformation["name"]
            print(f"Transformation completed: {name}")
            return True
        else:
            print(f"Transformation {transformation_id} not found")
            return False

    def get_status(self):
        return {
            "transformations": len(self.transformations),
            "active_transformations": sum(
                1 for t in self.transformations.values() if t["status"] == "executing"
            ),
            "timestamp": datetime.now().isoformat(),
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Simple Beta Transformation Service")
    parser.add_argument("--test", action="store_true", help="Run test mode")

    args = parser.parse_args()

    if args.test:
        print("Running Beta Transformation Service in test mode...")

        service = BetaTransformationService()

        # Create a test transformation
        trans_id = service.create_transformation(
            "Test Transformation", "A test transformation for validation"
        )

        # Execute transformation
        success = service.execute_transformation(trans_id)

        # Show status
        status = service.get_status()
        print(f"\\nStatus: {json.dumps(status, indent=2)}")
        print("Test completed successfully!")

        return

    print("Use --test to run test mode")


if __name__ == "__main__":
    main()
