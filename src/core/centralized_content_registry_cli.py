#!/usr/bin/env python3
"""
Centralized Content Registry CLI
==============================
Command-line interface for centralized content management system
V2 Compliant: ≤400 lines, focused CLI operations
"""

import argparse
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.centralized_content_registry_core import (
    CentralizedContentRegistryCore,
    ContentStatus,
    ContentType,
)


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Centralized Content Registry CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Register command
    register_parser = subparsers.add_parser("register", help="Register new content")
    register_parser.add_argument("file_path", help="Path to file to register")
    register_parser.add_argument(
        "content_type", choices=[ct.value for ct in ContentType], help="Type of content"
    )
    register_parser.add_argument("agent_id", help="Agent ID creating the content")
    register_parser.add_argument("--description", default="", help="Content description")
    register_parser.add_argument("--tags", nargs="*", help="Content tags")
    register_parser.add_argument("--dependencies", nargs="*", help="Content dependencies")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search content")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--tags", nargs="*", help="Filter by tags")

    # List command
    list_parser = subparsers.add_parser("list", help="List content")
    list_parser.add_argument("--agent", help="Filter by agent ID")
    list_parser.add_argument(
        "--type", choices=[ct.value for ct in ContentType], help="Filter by content type"
    )
    list_parser.add_argument(
        "--status", choices=[cs.value for cs in ContentStatus], help="Filter by status"
    )

    # Archive command
    archive_parser = subparsers.add_parser("archive", help="Archive content")
    archive_parser.add_argument("file_path", help="Path to file to archive")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete content")
    delete_parser.add_argument("file_path", help="Path to file to delete")
    delete_parser.add_argument(
        "--permanent", action="store_true", help="Permanently delete from filesystem"
    )

    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up old content")
    cleanup_parser.add_argument("--days", type=int, help="Days threshold for cleanup")

    # Statistics command
    stats_parser = subparsers.add_parser("stats", help="Show registry statistics")

    return parser


def handle_register(args, registry: CentralizedContentRegistryCore) -> None:
    """Handle register command"""
    content_type = ContentType(args.content_type)

    success = registry.manage_registry_operations(
        "register",
        file_path=args.file_path,
        content_type=content_type,
        agent_id=args.agent_id,
        description=args.description,
        tags=args.tags,
        dependencies=args.dependencies,
    )

    if success:
        print(f"✅ Successfully registered {args.file_path}")
    else:
        print(f"❌ Failed to register {args.file_path}")
        sys.exit(1)


def handle_search(args, registry: CentralizedContentRegistryCore) -> None:
    """Handle search command"""
    results = registry.manage_registry_operations("search", query=args.query, tags=args.tags)

    if not results:
        print("No content found matching your search criteria.")
        return

    print(f"Found {len(results)} content items:")
    for metadata in results:
        print(f"  📄 {metadata.file_path}")
        print(f"     Type: {metadata.content_type.value}")
        print(f"     Agent: {metadata.agent_id}")
        print(f"     Status: {metadata.status.value}")
        print(f"     Quality: {metadata.quality_score:.2f}")
        print(f"     V2 Compliant: {'✅' if metadata.v2_compliant else '❌'}")
        if metadata.description:
            print(f"     Description: {metadata.description}")
        if metadata.tags:
            print(f"     Tags: {', '.join(metadata.tags)}")
        print()


def handle_list(args, registry: CentralizedContentRegistryCore) -> None:
    """Handle list command"""
    if args.agent:
        results = registry.manage_registry_operations("get_by_agent", agent_id=args.agent)
    elif args.type:
        content_type = ContentType(args.type)
        results = registry.manage_registry_operations("get_by_type", content_type=content_type)
    else:
        # Get all content
        results = list(registry.content_registry.values())

    # Filter by status if specified
    if args.status:
        status = ContentStatus(args.status)
        results = [r for r in results if r.status == status]

    if not results:
        print("No content found matching your criteria.")
        return

    print(f"Found {len(results)} content items:")
    for metadata in results:
        print(f"  📄 {metadata.file_path}")
        print(f"     Type: {metadata.content_type.value}")
        print(f"     Agent: {metadata.agent_id}")
        print(f"     Status: {metadata.status.value}")
        print(f"     Size: {metadata.file_size} bytes")
        print(f"     Quality: {metadata.quality_score:.2f}")
        print(f"     V2 Compliant: {'✅' if metadata.v2_compliant else '❌'}")
        print(f"     Created: {metadata.created_at}")
        print()


def handle_archive(args, registry: CentralizedContentRegistryCore) -> None:
    """Handle archive command"""
    success = registry.manage_registry_operations("archive", file_path=args.file_path)

    if success:
        print(f"✅ Successfully archived {args.file_path}")
    else:
        print(f"❌ Failed to archive {args.file_path}")
        sys.exit(1)


def handle_delete(args, registry: CentralizedContentRegistryCore) -> None:
    """Handle delete command"""
    success = registry.manage_registry_operations(
        "delete", file_path=args.file_path, permanent=args.permanent
    )

    if success:
        action = "permanently deleted" if args.permanent else "marked for deletion"
        print(f"✅ Successfully {action} {args.file_path}")
    else:
        print(f"❌ Failed to delete {args.file_path}")
        sys.exit(1)


def handle_cleanup(args, registry: CentralizedContentRegistryCore) -> None:
    """Handle cleanup command"""
    report = registry.manage_registry_operations("cleanup", days_threshold=args.days)

    print("🧹 Cleanup completed:")
    print(f"   Archived: {report['archived']} files")
    print(f"   Deleted: {report['deleted']} files")
    print(f"   Total processed: {len(report['processed_files'])} files")

    if report["processed_files"]:
        print("\nProcessed files:")
        for file_path in report["processed_files"]:
            print(f"   📄 {file_path}")


def handle_stats(args, registry: CentralizedContentRegistryCore) -> None:
    """Handle statistics command"""
    stats = registry.manage_registry_operations("statistics")

    print("📊 Registry Statistics:")
    print(f"   Total files: {stats['total_files']}")
    print(f"   Total size: {stats['total_size']:,} bytes")
    print(f"   Average quality score: {stats['average_quality_score']:.2f}")
    print(f"   V2 compliant files: {stats['v2_compliant_count']}")
    print(f"   Last updated: {stats['last_updated']}")

    print("\n📈 Status Breakdown:")
    for status, count in stats["status_breakdown"].items():
        print(f"   {status}: {count}")

    print("\n📂 Type Breakdown:")
    for content_type, count in stats["type_breakdown"].items():
        print(f"   {content_type}: {count}")

    print("\n👥 Agent Breakdown:")
    for agent_id, count in stats["agent_breakdown"].items():
        print(f"   {agent_id}: {count}")


def main():
    """Main CLI function"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize registry
    registry = CentralizedContentRegistryCore()

    # Handle commands
    if args.command == "register":
        handle_register(args, registry)
    elif args.command == "search":
        handle_search(args, registry)
    elif args.command == "list":
        handle_list(args, registry)
    elif args.command == "archive":
        handle_archive(args, registry)
    elif args.command == "delete":
        handle_delete(args, registry)
    elif args.command == "cleanup":
        handle_cleanup(args, registry)
    elif args.command == "stats":
        handle_stats(args, registry)


if __name__ == "__main__":
    main()
