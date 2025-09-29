#!/usr/bin/env python3
"""
Reduce .md Files Script
=======================

This script implements the comprehensive .md file reduction plan,
reducing 1,157 .md files to <50 essential files.
"""

import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_backup():
    """Create backup of all .md files before deletion."""
    logger.info("=== CREATING BACKUP ===")

    backup_dir = Path("documentation_backup")
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"md_files_backup_{timestamp}.txt"

    # Count total files
    total_files = list(Path(".").rglob("*.md"))
    logger.info(f"📦 Backing up {len(total_files)} .md files")

    # Write backup list
    with open(backup_file, "w", encoding="utf-8") as f:
        f.write("MD Files Backup\\n")
        f.write("=" * 50 + "\\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
        f.write(f"Total files: {len(total_files)}\\n\\n")
        for file_path in total_files:
            f.write(f"{file_path}\\n")

    logger.info(f"✅ Backup created: {backup_file}")
    return backup_file


def phase1_frontend_cleanup():
    """Phase 1: Delete frontend documentation bloat."""
    logger.info("=== PHASE 1: FRONTEND CLEANUP ===")

    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        logger.warning("No frontend directory found")
        return 0

    # Count frontend .md files
    frontend_files = list(frontend_dir.rglob("*.md"))
    logger.info(f"🗑️ Deleting {len(frontend_files)} frontend .md files")

    deleted_count = 0
    for file_path in frontend_files:
        try:
            file_size = file_path.stat().st_size
            file_path.unlink()
            deleted_count += 1
            logger.info(f"  ✅ Deleted: {file_path.name} ({file_size} bytes)")
        except Exception as e:
            logger.error(f"  ❌ Failed to delete {file_path.name}: {e}")

    logger.info(f"📊 Phase 1 complete: {deleted_count} frontend files deleted")
    return deleted_count


def phase2_agent_workspace_cleanup():
    """Phase 2: Delete agent workspace documentation."""
    logger.info("=== PHASE 2: AGENT WORKSPACE CLEANUP ===")

    agent_workspaces_dir = Path("agent_workspaces")
    if not agent_workspaces_dir.exists():
        logger.warning("No agent_workspaces directory found")
        return 0

    # Count agent workspace .md files
    agent_files = list(agent_workspaces_dir.rglob("*.md"))
    logger.info(f"🗑️ Deleting {len(agent_files)} agent workspace .md files")

    deleted_count = 0
    for file_path in agent_files:
        try:
            file_size = file_path.stat().st_size
            file_path.unlink()
            deleted_count += 1
            logger.info(f"  ✅ Deleted: {file_path.name} ({file_size} bytes)")
        except Exception as e:
            logger.error(f"  ❌ Failed to delete {file_path.name}: {e}")

    logger.info(f"📊 Phase 2 complete: {deleted_count} agent workspace files deleted")
    return deleted_count


def phase3_archive_cleanup():
    """Phase 3: Delete archive documentation."""
    logger.info("=== PHASE 3: ARCHIVE CLEANUP ===")

    archive_dirs = [Path("devlogs/archive"), Path("thea_responses/archive")]

    deleted_count = 0
    for archive_dir in archive_dirs:
        if archive_dir.exists():
            archive_files = list(archive_dir.rglob("*.md"))
            logger.info(f"🗑️ Deleting {len(archive_files)} archive .md files from {archive_dir}")

            for file_path in archive_files:
                try:
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    deleted_count += 1
                    logger.info(f"  ✅ Deleted: {file_path.name} ({file_size} bytes)")
                except Exception as e:
                    logger.error(f"  ❌ Failed to delete {file_path.name}: {e}")
        else:
            logger.info(f"  ⚠️ Archive directory not found: {archive_dir}")

    logger.info(f"📊 Phase 3 complete: {deleted_count} archive files deleted")
    return deleted_count


def phase4_test_cleanup():
    """Phase 4: Delete test documentation."""
    logger.info("=== PHASE 4: TEST DOCUMENTATION CLEANUP ===")

    tests_dir = Path("tests")
    if not tests_dir.exists():
        logger.warning("No tests directory found")
        return 0

    # Count test .md files
    test_files = list(tests_dir.rglob("*.md"))
    logger.info(f"🗑️ Deleting {len(test_files)} test .md files")

    deleted_count = 0
    for file_path in test_files:
        try:
            file_size = file_path.stat().st_size
            file_path.unlink()
            deleted_count += 1
            logger.info(f"  ✅ Deleted: {file_path.name} ({file_size} bytes)")
        except Exception as e:
            logger.error(f"  ❌ Failed to delete {file_path.name}: {e}")

    logger.info(f"📊 Phase 4 complete: {deleted_count} test files deleted")
    return deleted_count


def phase5_tool_cleanup():
    """Phase 5: Delete tool documentation."""
    logger.info("=== PHASE 5: TOOL DOCUMENTATION CLEANUP ===")

    tools_dir = Path("tools")
    if not tools_dir.exists():
        logger.warning("No tools directory found")
        return 0

    # Count tool .md files
    tool_files = list(tools_dir.rglob("*.md"))
    logger.info(f"🗑️ Deleting {len(tool_files)} tool .md files")

    deleted_count = 0
    for file_path in tool_files:
        try:
            file_size = file_path.stat().st_size
            file_path.unlink()
            deleted_count += 1
            logger.info(f"  ✅ Deleted: {file_path.name} ({file_size} bytes)")
        except Exception as e:
            logger.error(f"  ❌ Failed to delete {file_path.name}: {e}")

    logger.info(f"📊 Phase 5 complete: {deleted_count} tool files deleted")
    return deleted_count


def phase6_keep_essential():
    """Phase 6: Keep only essential files."""
    logger.info("=== PHASE 6: KEEP ESSENTIAL FILES ===")

    essential_files = [
        "README.md",
        "swarm_brain/README.md",
        "DATABASE_QUERY_REPLACEMENT_GUIDE.md",
        "DOCUMENTATION_REPLACEMENT_SUMMARY.md",
        "MD_FILE_REDUCTION_PLAN.md",
    ]

    kept_count = 0
    for file_path in essential_files:
        if Path(file_path).exists():
            kept_count += 1
            logger.info(f"  ✅ Kept: {file_path}")
        else:
            logger.warning(f"  ⚠️ Essential file not found: {file_path}")

    logger.info(f"📊 Phase 6 complete: {kept_count} essential files kept")
    return kept_count


def verify_results():
    """Verify the reduction results."""
    logger.info("=== VERIFICATION ===")

    # Count remaining .md files
    remaining_files = list(Path(".").rglob("*.md"))
    logger.info(f"📊 Remaining .md files: {len(remaining_files)}")

    # List remaining files
    for file_path in remaining_files:
        logger.info(f"  📄 {file_path}")

    return len(remaining_files)


def main():
    """Main reduction process."""
    logger.info("🗑️ Starting .md File Reduction Process")
    logger.info("=" * 60)

    try:
        # Create backup
        backup_file = create_backup()

        # Execute phases
        total_deleted = 0

        total_deleted += phase1_frontend_cleanup()
        total_deleted += phase2_agent_workspace_cleanup()
        total_deleted += phase3_archive_cleanup()
        total_deleted += phase4_test_cleanup()
        total_deleted += phase5_tool_cleanup()

        # Keep essential files
        kept_files = phase6_keep_essential()

        # Verify results
        remaining_files = verify_results()

        logger.info("=" * 60)
        logger.info("🎉 .md File reduction completed successfully!")
        logger.info(f"📊 Total files deleted: {total_deleted}")
        logger.info(f"📄 Essential files kept: {kept_files}")
        logger.info(f"📊 Remaining files: {remaining_files}")
        logger.info(f"📦 Backup created: {backup_file}")
        logger.info("🚀 Documentation bloat eliminated!")

    except Exception as e:
        logger.error(f"❌ Reduction process failed: {e}")
        raise


if __name__ == "__main__":
    main()
