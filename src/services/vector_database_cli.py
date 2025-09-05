from ..core.unified_entry_point_system import main
#!/usr/bin/env python3
"""
Vector Database CLI - Agent Cellphone V2
======================================

Command-line interface for vector database operations.
Provides commands for indexing, searching, and managing vector data.

V2 Compliance: < 300 lines, single responsibility, CLI interface.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import logging



def setup_logging(verbose: bool = False):
    """Setup logging for CLI operations."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def cmd_search(args):
    """Search command handler."""
    try:
        # Initialize vector integration
        config = load_vector_database_config(args.config)
        integration = VectorMessagingIntegration(config)

        # Perform search
        if args.type == "messages":
            results = integration.search_messages(
                query_text=args.query,
                agent_id=args.agent,
                limit=args.limit,
                similarity_threshold=args.threshold,
            )
        elif args.type == "devlogs":
            results = integration.search_devlogs(
                query_text=args.query,
                agent_id=args.agent,
                limit=args.limit,
                similarity_threshold=args.threshold,
            )
        else:  # all
            results = integration.search_all(
                query_text=args.query,
                agent_id=args.agent,
                limit=args.limit,
                similarity_threshold=args.threshold,
            )

        # Display results
        if not get_unified_validator().validate_required(results):
            get_logger(__name__).info("No results found.")
            return

        get_logger(__name__).info(f"\nFound {len(results)} results for query: '{args.query}'\n")

        for i, result in enumerate(results, 1):
            get_logger(__name__).info(
                f"{i}. [{result.similarity_score:.3f}] {result.document.document_type.value.upper()}"
            )
            get_logger(__name__).info(f"   ID: {result.document.id}")
            if result.document.agent_id:
                get_logger(__name__).info(f"   Agent: {result.document.agent_id}")
            get_logger(__name__).info(f"   Content: {result.document.content[:100]}...")
            if result.document.tags:
                get_logger(__name__).info(f"   Tags: {', '.join(result.document.tags)}")
            get_logger(__name__).info()

    except Exception as e:
        get_logger(__name__).info(f"❌ Error during search: {e}")
        return 1


def cmd_index(args):
    """Index command handler."""
    try:
        # Initialize vector integration
        config = load_vector_database_config(args.config)
        integration = VectorMessagingIntegration(config)

        if args.inbox:
            # Index inbox files
            agent_id = args.agent or "unknown"
            indexed_count = integration.index_inbox_files(agent_id, args.inbox)
            get_logger(__name__).info(f"✅ Indexed {indexed_count} files from {args.inbox}")

        elif args.file:
            # Index single file
            file_path = get_unified_utility().Path(args.file)
            if not file_path.exists():
                get_logger(__name__).info(f"❌ File not found: {args.file}")
                return 1

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Create document

            doc = VectorDocument(
                content=content,
                document_type=(
                    DocumentType.CODE
                    if file_path.suffix in [".py", ".js", ".ts"]
                    else DocumentType.DOCUMENTATION
                ),
                source_file=str(file_path),
                tags=[file_path.suffix[1:], "file"],
            )

            # Add to database
            success = integration.vector_db.add_document(doc)
            if success:
                get_logger(__name__).info(f"✅ Indexed file: {args.file}")
            else:
                get_logger(__name__).info(f"❌ Failed to index file: {args.file}")
                return 1

        else:
            get_logger(__name__).info("❌ Please specify either --inbox or --file")
            return 1

    except Exception as e:
        get_logger(__name__).info(f"❌ Error during indexing: {e}")
        return 1


def cmd_stats(args):
    """Stats command handler."""
    try:
        # Initialize vector integration
        config = load_vector_database_config(args.config)
        integration = VectorMessagingIntegration(config)

        # Get statistics
        stats = integration.get_database_stats()

        get_logger(__name__).info("\n📊 Vector Database Statistics\n")
        get_logger(__name__).info(f"Total Documents: {stats.get('total_documents', 0)}")
        get_logger(__name__).info(f"Total Collections: {stats.get('total_collections', 0)}")
        get_logger(__name__).info(f"Storage Size: {stats.get('storage_size_mb', 0):.2f} MB")
        get_logger(__name__).info(f"Last Updated: {stats.get('last_updated', 'Unknown')}")

        if stats.get("collections"):
            get_logger(__name__).info("\nCollections:")
            for name, count in stats["collections"].items():
                get_logger(__name__).info(f"  {name}: {count} documents")

    except Exception as e:
        get_logger(__name__).info(f"❌ Error getting stats: {e}")
        return 1


def cmd_collections(args):
    """Collections command handler."""
    try:
        # Initialize vector integration
        config = load_vector_database_config(args.config)
        integration = VectorMessagingIntegration(config)

        # Get collection info
        client = integration.vector_db._get_client()
        collections = client.list_collections()

        get_logger(__name__).info("\n📁 Vector Database Collections\n")

        if not get_unified_validator().validate_required(collections):
            get_logger(__name__).info("No collections found.")
            return

        for collection in collections:
            count = collection.count()
            get_logger(__name__).info(f"{collection.name}: {count} documents")
            if collection.metadata:
                get_logger(__name__).info(f"  Description: {collection.metadata.get('description', 'N/A')}")

    except Exception as e:
        get_logger(__name__).info(f"❌ Error listing collections: {e}")
        return 1


def cmd_related(args):
    """Related messages command handler."""
    try:
        # Initialize vector integration
        config = load_vector_database_config(args.config)
        integration = VectorMessagingIntegration(config)

        # Find related messages
        results = integration.get_related_messages(args.message_id, args.limit)

        if not get_unified_validator().validate_required(results):
            get_logger(__name__).info("No related messages found.")
            return

        get_logger(__name__).info(f"\nFound {len(results)} related messages for: {args.message_id}\n")

        for i, result in enumerate(results, 1):
            get_logger(__name__).info(
                f"{i}. [{result.similarity_score:.3f}] {result.document.document_type.value.upper()}"
            )
            get_logger(__name__).info(f"   ID: {result.document.id}")
            get_logger(__name__).info(f"   Content: {result.document.content[:100]}...")
            get_logger(__name__).info()

    except Exception as e:
        get_logger(__name__).info(f"❌ Error finding related messages: {e}")
        return 1



if __name__ == "__main__":
    exit(main())

