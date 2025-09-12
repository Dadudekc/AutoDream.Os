from __future__ import annotations
import argparse, logging, sys
import os

# Handle both module import and direct script execution
if __name__ == "__main__":
    # Add parent directories to path when run as script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    grandparent_dir = os.path.dirname(parent_dir)
    sys.path.insert(0, grandparent_dir)
    sys.path.insert(0, parent_dir)

    # Use absolute imports when run as script
    from src.services.messaging.service import MessagingService
    from src.services.messaging.coordinates import list_agents
    from src.services.messaging.task_handlers import handle_claim, handle_complete
    from src.services.messaging.onboarding_bridge import hard_onboarding
    from src.services.messaging.thea_handlers import send_to_thea
else:
    # Use relative imports when imported as module
    from .service import MessagingService
    from .coordinates import list_agents
    from .task_handlers import handle_claim, handle_complete
    from .onboarding_bridge import hard_onboarding
    from .thea_handlers import send_to_thea

logger = logging.getLogger(__name__)

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Consolidated Messaging (Modular)")
    p.add_argument("--agent","-a")
    p.add_argument("--message","-m")
    p.add_argument("--priority","-p", default="NORMAL", choices=["LOW","NORMAL","HIGH","URGENT"])
    p.add_argument("--tag","-t", default="GENERAL", choices=["GENERAL","COORDINATION","TASK","STATUS"])
    p.add_argument("--broadcast","-b", action="store_true")
    p.add_argument("--list-agents","-l", action="store_true")
    # Tasks
    p.add_argument("--claim-task", action="store_true")
    p.add_argument("--complete-task", action="store_true")
    p.add_argument("--task-id")
    p.add_argument("--task-notes")
    # Onboarding
    p.add_argument("--hard-onboarding", action="store_true")
    p.add_argument("--agents")
    p.add_argument("--onboarding-mode", default="quality-suite", choices=["cleanup","quality-suite","consolidation","testing"])
    p.add_argument("--assign-roles", default="")
    p.add_argument("--use-ui", action="store_true")
    p.add_argument("--ui-retries", type=int, default=3)
    p.add_argument("--ui-tolerance", type=int, default=10)
    # Thea
    p.add_argument("--thea-message")
    p.add_argument("--thea-username")
    p.add_argument("--thea-password")
    p.add_argument("--thea-headless", action="store_true", default=True)
    p.add_argument("--thea-no-headless", action="store_true")
    # misc
    p.add_argument("--dry-run", action="store_true")
    return p

def main(argv: list[str] | None = None):
    args = build_parser().parse_args(argv)
    if args.thea_no_headless: args.thea_headless = False
    svc = MessagingService(dry_run=args.dry_run)

    if args.list_agents:
        for a in list_agents():
            print(f"- {a}")
        return

    if args.broadcast:
        if not args.message:
            print("❌ --message required for --broadcast"); return
        res = svc.broadcast(args.message)
        for a,ok in res.items(): print(("✅" if ok else "❌"), a)
        return

    if args.claim_task:
        if not args.agent: print("❌ --agent required"); return
        print(handle_claim(args.agent)); return

    if args.complete_task:
        if not args.agent or not args.task_id:
            print("❌ --agent and --task-id required"); return
        print(handle_complete(args.agent, args.task_id, args.task_notes or "done")); return

    if args.hard_onboarding:
        if not args.agents: print("❌ --agents missing"); return
        agents = [a.strip() for a in args.agents.split(",") if a.strip()]
        code = hard_onboarding(agents, args.onboarding_mode, args.assign_roles, args.dry_run, args.use_ui, args.ui_retries, args.ui_tolerance)
        print("✅ Onboarding OK" if code==0 else ("⚠️ Partial" if code==2 else "❌ Failed")); return

    if args.thea_message:
        ok = send_to_thea(args.thea_message, username=args.thea_username, password=args.thea_password,
                          headless=args.thea_headless)
        print("✅ Thea OK" if ok else "❌ Thea failed"); return

    if args.agent and args.message:
        ok = svc.send(args.agent, args.message, args.priority, args.tag)
        print("✅ Sent" if ok else "❌ Failed"); return

    build_parser().print_help()

if __name__ == "__main__":
    main(sys.argv[1:])
