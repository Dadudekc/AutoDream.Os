#!/usr/bin/env python3
"""
Simple PR Monitor for Captain Agent-4
=====================================

Monitors for open pull requests and messages Captain Agent-4
when PRs are ready to be merged.

Usage:
    python pr_monitor.py [--interval 300] [--once]
"""

import os
import sys
import time
import json
import subprocess
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class PullRequest:
    """Pull Request data structure."""

    number: int
    title: str
    author: str
    state: str
    created_at: str
    updated_at: str
    url: str
    ready_for_merge: bool = False


class PRMonitor:
    """Simple PR Monitor for Captain Agent-4."""

    def __init__(self, check_interval: int = 300):
        """Initialize PR Monitor."""
        self.check_interval = check_interval
        self.known_prs = set()
        self.captain_agent_id = "Agent-4"

        logger.info(f"PR Monitor initialized with {check_interval}s check interval")

    def get_open_pull_requests(self) -> List[PullRequest]:
        """Get open pull requests from the repository."""
        try:
            # Use GitHub CLI to get PR information
            result = subprocess.run(
                [
                    "gh",
                    "pr",
                    "list",
                    "--state",
                    "open",
                    "--json",
                    "number,title,author,state,createdAt,updatedAt,url",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            pr_data = json.loads(result.stdout)
            prs = []

            for pr in pr_data:
                pr_obj = PullRequest(
                    number=pr["number"],
                    title=pr["title"],
                    author=pr["author"]["login"],
                    state=pr["state"],
                    created_at=pr["createdAt"],
                    updated_at=pr["updatedAt"],
                    url=pr["url"],
                    ready_for_merge=self._is_pr_ready_for_merge(pr),
                )
                prs.append(pr_obj)

            logger.info(f"Found {len(prs)} open pull requests")
            return prs

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get pull requests: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse PR data: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting pull requests: {e}")
            return []

    def _is_pr_ready_for_merge(self, pr_data: Dict) -> bool:
        """Check if a PR is ready for merge."""
        try:
            # Check if PR has required status checks
            pr_number = pr_data["number"]
            result = subprocess.run(
                ["gh", "pr", "view", str(pr_number), "--json", "statusCheckRollup"],
                capture_output=True,
                text=True,
                check=True,
            )

            status_data = json.loads(result.stdout)
            status_rollup = status_data.get("statusCheckRollup", [])

            # Check if all status checks are passing
            for check in status_rollup:
                if check.get("state") != "SUCCESS":
                    return False

            return True

        except Exception as e:
            logger.warning(f"Could not check PR {pr_data['number']} status: {e}")
            return False

    def send_pr_notification(self, pr: PullRequest) -> bool:
        """Send PR notification to Captain Agent-4."""
        try:
            message = (
                f"🚨 **PR MONITORING ALERT** 🚨\n\n"
                f"**Captain Agent-4**: Open PR detected and ready for merge\n\n"
                f"**PR Details:**\n"
                f"- **Number**: #{pr.number}\n"
                f"- **Title**: {pr.title}\n"
                f"- **Author**: {pr.author}\n"
                f"- **State**: {pr.state}\n"
                f"- **Created**: {pr.created_at}\n"
                f"- **Updated**: {pr.updated_at}\n"
                f"- **URL**: {pr.url}\n"
                f"- **Ready for Merge**: {'✅ YES' if pr.ready_for_merge else '❌ NO'}\n\n"
                f"**Action Required**: Review and merge PR if approved\n"
                f"**Priority**: NORMAL - PR ready for merge\n\n"
                f"**PR Monitoring System**\n"
                f"**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"**WE. ARE. SWARM.** ⚡️🔥"
            )

            # Send message to Captain Agent-4 using messaging CLI
            try:
                result = subprocess.run(
                    [
                        "python",
                        "-m",
                        "src.services.messaging_cli",
                        "--agent",
                        self.captain_agent_id,
                        "--message",
                        message,
                        "--sender",
                        "PR Monitoring System",
                        "--type",
                        "system_to_agent",
                        "--priority",
                        "normal",
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                success = True
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to send message via CLI: {e}")
                success = False

            if success:
                logger.info(
                    f"PR notification sent to Captain Agent-4 for PR #{pr.number}"
                )
                return True
            else:
                logger.error(f"Failed to send PR notification for PR #{pr.number}")
                return False

        except Exception as e:
            logger.error(f"Error sending PR notification: {e}")
            return False

    def check_for_new_prs(self) -> List[PullRequest]:
        """Check for new pull requests and send notifications."""
        try:
            open_prs = self.get_open_pull_requests()
            new_prs = []

            for pr in open_prs:
                pr_id = f"{pr.number}_{pr.updated_at}"

                if pr_id not in self.known_prs:
                    self.known_prs.add(pr_id)
                    new_prs.append(pr)

                    # Send notification for new PR
                    if pr.ready_for_merge:
                        logger.info(f"New PR #{pr.number} ready for merge: {pr.title}")
                        self.send_pr_notification(pr)
                    else:
                        logger.info(
                            f"New PR #{pr.number} detected but not ready for merge: {pr.title}"
                        )

            return new_prs

        except Exception as e:
            logger.error(f"Error checking for new PRs: {e}")
            return []

    def start_monitoring(self):
        """Start continuous PR monitoring."""
        logger.info("Starting PR monitoring system...")

        try:
            while True:
                try:
                    # Check for new PRs
                    new_prs = self.check_for_new_prs()

                    if new_prs:
                        logger.info(f"Found {len(new_prs)} new PRs")
                    else:
                        logger.debug("No new PRs found")

                    # Wait for next check
                    time.sleep(self.check_interval)

                except KeyboardInterrupt:
                    logger.info("PR monitoring stopped by user")
                    break
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}")
                    time.sleep(self.check_interval)

        except Exception as e:
            logger.error(f"Fatal error in PR monitoring: {e}")
            raise


def main():
    """Main function to run PR monitoring."""
    parser = argparse.ArgumentParser(
        description="PR Monitor - Monitor for open PRs and notify Captain Agent-4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Run continuous monitoring with 5-minute intervals
    python pr_monitor.py

    # Run with custom interval (2 minutes)
    python pr_monitor.py --interval 120

    # Check once and exit
    python pr_monitor.py --once

    # Check once with custom interval
    python pr_monitor.py --once --interval 60
        """,
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Check interval in seconds (default: 300 = 5 minutes)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Check once and exit instead of continuous monitoring",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("PR Monitor starting...")
    logger.info(f"Check interval: {args.interval} seconds")
    logger.info(f"Mode: {'Single check' if args.once else 'Continuous monitoring'}")

    try:
        # Initialize PR monitoring system
        pr_monitor = PRMonitor(check_interval=args.interval)

        if args.once:
            # Check once and exit
            logger.info("Running single PR check...")
            new_prs = pr_monitor.check_for_new_prs()
            logger.info(f"Found {len(new_prs)} new PRs")

            if new_prs:
                print(f"\n🚨 Found {len(new_prs)} new PR(s):")
                for pr in new_prs:
                    print(f"  - PR #{pr.number}: {pr.title} (by {pr.author})")
                    if pr.ready_for_merge:
                        print(f"    ✅ Ready for merge")
                    else:
                        print(f"    ⏳ Not ready for merge")
            else:
                print("\n✅ No new PRs found")

        else:
            # Start continuous monitoring
            print(f"\n🔄 Starting continuous PR monitoring...")
            print(f"   Check interval: {args.interval} seconds")
            print(f"   Press Ctrl+C to stop")
            print()

            pr_monitor.start_monitoring()

    except KeyboardInterrupt:
        logger.info("PR monitoring stopped by user")
        print("\n👋 PR monitoring stopped")
    except Exception as e:
        logger.error(f"Fatal error in PR monitoring: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
