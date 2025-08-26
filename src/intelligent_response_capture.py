#!/usr/bin/env python3
"""CLI for the Intelligent Response Capture system."""

import argparse

from agent_response_database import AgentResponseDatabase
from response_analytics import ResponseAnalytics
from response_capture import ResponseCapture


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Intelligent Response Capture System"
    )
    subparsers = parser.add_subparsers(dest="command")

    capture_parser = subparsers.add_parser(
        "capture", help="Capture a response file"
    )
    capture_parser.add_argument(
        "agent_id", help="ID of the agent providing the response"
    )
    capture_parser.add_argument(
        "response_file", help="Path to the response file"
    )

    subparsers.add_parser("summary", help="Display progress summary")

    args = parser.parse_args()

    db = AgentResponseDatabase()
    analytics = ResponseAnalytics(db)
    capture = ResponseCapture(db, analytics)

    if args.command == "capture":
        if not capture.capture_response(args.agent_id, args.response_file):
            print("Error: Failed to capture response.")
    elif args.command == "summary":
        summary = analytics.get_agent_progress_summary()
        for agent_stat in summary["agent_stats"]:
            agent_id, response_count, total_size, last_response = agent_stat
            print(f"{agent_id}: {response_count} responses, {total_size or 0} bytes")
        print(f"\nGenerated Tasks: {summary['total_generated_tasks']}")
        print(f"Total Responses: {summary['total_responses']}")
    else:
        parser.print_help()
