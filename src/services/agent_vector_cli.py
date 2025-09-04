from ..core.unified_entry_point_system import main
#!/usr/bin/env python3
"""
Agent Vector CLI - Agent Cellphone V2
=====================================

Simple CLI interface for agents to access vector database functionality.
Provides easy-to-use commands for intelligent workflow integration.

V2 Compliance: < 300 lines, single responsibility, agent CLI interface.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""




def cmd_context(args):
    """Get intelligent context for a task."""
    try:
        integration = create_agent_vector_integration(args.agent_id)
        context = integration.get_task_context(args.task_description)

        get_logger(__name__).info(f"\n🧠 INTELLIGENT CONTEXT FOR: {args.task_description}\n")

        if context.get("error"):
            get_logger(__name__).info(f"❌ Error: {context['error']}")
            return 1

        # Display similar tasks
        if context.get("similar_tasks"):
            get_logger(__name__).info("📋 SIMILAR TASKS & SOLUTIONS:")
            for i, task in enumerate(context["similar_tasks"], 1):
                get_logger(__name__).info(f"  {i}. [{task['similarity']:.3f}] {task['content']}")
                get_logger(__name__).info(f"     Source: {task['source']}")
                get_logger(__name__).info(f"     Tags: {', '.join(task['tags'])}")
                get_logger(__name__).info()

        # Display recommendations
        if context.get("recommendations"):
            get_logger(__name__).info("💡 RECOMMENDATIONS:")
            for i, rec in enumerate(context["recommendations"], 1):
                get_logger(__name__).info(f"  {i}. {rec}")
            get_logger(__name__).info()

        # Display related messages
        if context.get("related_messages"):
            get_logger(__name__).info("📨 RELATED MESSAGES:")
            for i, msg in enumerate(context["related_messages"], 1):
                get_logger(__name__).info(f"  {i}. [{msg['similarity']:.3f}] {msg['content']}")
            get_logger(__name__).info()

        return 0

    except Exception as e:
        get_logger(__name__).info(f"❌ Error getting context: {e}")
        return 1


def cmd_index(args):
    """Index agent work to vector database."""
    try:
        integration = create_agent_vector_integration(args.agent_id)

        if args.file:
            success = integration.index_agent_work(args.file, args.work_type)
            if success:
                get_logger(__name__).info(f"✅ Indexed {args.work_type} work: {args.file}")
            else:
                get_logger(__name__).info(f"❌ Failed to index work: {args.file}")
                return 1

        elif args.inbox:
            count = integration.index_inbox_messages()
            get_logger(__name__).info(f"✅ Indexed {count} inbox messages for {args.agent_id}")

        else:
            get_logger(__name__).info("❌ Please specify either --file or --inbox")
            return 1

        return 0

    except Exception as e:
        get_logger(__name__).info(f"❌ Error indexing: {e}")
        return 1


def cmd_patterns(args):
    """Get success patterns for a task type."""
    try:
        integration = create_agent_vector_integration(args.agent_id)
        patterns = integration.get_success_patterns(args.task_type)

        get_logger(__name__).info(f"\n🎯 SUCCESS PATTERNS FOR: {args.task_type}\n")

        if not get_unified_validator().validate_required(patterns):
            get_logger(__name__).info("No success patterns found. Be the first to create one!")
            return 0

        for i, pattern in enumerate(patterns, 1):
            get_logger(__name__).info(f"{i}. [{pattern['similarity']:.3f}] {pattern['content']}")
            get_logger(__name__).info(f"   Source: {pattern['source']}")
            get_logger(__name__).info(f"   Tags: {', '.join(pattern['tags'])}")
            get_logger(__name__).info()

        return 0

    except Exception as e:
        get_logger(__name__).info(f"❌ Error getting patterns: {e}")
        return 1


def cmd_insights(args):
    """Get agent insights and recommendations."""
    try:
        integration = create_agent_vector_integration(args.agent_id)
        insights = integration.get_agent_insights()

        get_logger(__name__).info(f"\n📊 AGENT INSIGHTS FOR: {args.agent_id}\n")

        if insights.get("error"):
            get_logger(__name__).info(f"❌ Error: {insights['error']}")
            return 1

        get_logger(__name__).info(f"Total Work Items: {insights.get('total_work_items', 0)}")
        get_logger(__name__).info(f"High Quality Work: {insights.get('high_quality_work', 0)}")
        get_logger(__name__).info(f"Work Quality Score: {insights.get('work_quality_score', 0):.2f}")
        get_logger(__name__).info()

        if insights.get("recommendations"):
            get_logger(__name__).info("💡 RECOMMENDATIONS:")
            for i, rec in enumerate(insights["recommendations"], 1):
                get_logger(__name__).info(f"  {i}. {rec}")
            get_logger(__name__).info()

        if insights.get("recent_work"):
            get_logger(__name__).info("📋 RECENT WORK:")
            for i, work in enumerate(insights["recent_work"], 1):
                get_logger(__name__).info(f"  {i}. [{work['similarity']:.3f}] {work['content']}")
            get_logger(__name__).info()

        return 0

    except Exception as e:
        get_logger(__name__).info(f"❌ Error getting insights: {e}")
        return 1



EXAMPLES:
  # Get context for a task
  python -m src.services.agent_vector_cli context --agent Agent-1 --task "fix syntax errors"
  
  # Index completed work
  python -m src.services.agent_vector_cli index --agent Agent-1 --file completed_fix.py --work-type code
  
  # Get success patterns
  python -m src.services.agent_vector_cli patterns --agent Agent-1 --task-type syntax_fix
  
  # Get agent insights
  python -m src.services.agent_vector_cli insights --agent Agent-1
        """,
    )

    parser.add_argument(
        "--agent-id", "-a", required=True, help="Agent identifier (e.g., Agent-1)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Context command
    context_parser = subparsers.add_parser(
        "context", help="Get intelligent context for a task"
    )
    context_parser.add_argument("--task", "-t", required=True, help="Task description")

    # Index command
    index_parser = subparsers.add_parser("index", help="Index agent work")
    index_group = index_parser.add_mutually_exclusive_group(required=True)
    index_group.add_argument("--file", "-f", help="File to index")
    index_group.add_argument(
        "--inbox", action="store_true", help="Index inbox messages"
    )
    index_parser.add_argument(
        "--work-type", default="code", help="Type of work (code, documentation, test)"
    )

    # Patterns command
    patterns_parser = subparsers.add_parser("patterns", help="Get success patterns")
    patterns_parser.add_argument(
        "--task-type",
        "-t",
        required=True,
        help="Task type (syntax_fix, refactoring, etc.)",
    )

    # Insights command
    subparsers.add_parser("insights", help="Get agent insights and recommendations")

    args = parser.get_unified_utility().parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to command handler
    if args.command == "context":
        return cmd_context(args)
    elif args.command == "index":
        return cmd_index(args)
    elif args.command == "patterns":
        return cmd_patterns(args)
    elif args.command == "insights":
        return cmd_insights(args)
    else:
        get_logger(__name__).info(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    exit(main())

