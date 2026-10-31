#!/usr/bin/env python3
"""Entry point for the CLI agent swarm."""
import argparse
import json
import sys

from dotenv import load_dotenv
load_dotenv()

from swarm.orchestrator import Orchestrator


def pretty_print(result: dict) -> None:
    if result.get("ok"):
        print(f"✅ {result.get('agent', '?')} robot")
        if result.get("command"):
            print(f"   $ {' '.join(result['command'])}")
        if result.get("dry_run"):
            print("   (dry run — not executed)")
        elif result.get("stdout"):
            print()
            print(result["stdout"].rstrip())
        if result.get("stderr"):
            print(f"\n⚠️  stderr:\n{result['stderr'].rstrip()}")
    else:
        print(f"❌ {result.get('agent', '?')} robot")
        print(f"   error: {result.get('error')}")
        if result.get("command"):
            print(f"   $ {' '.join(result['command'])}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="swarm",
        description="A swarm of small agents that each know one CLI tool.",
    )
    parser.add_argument("request", nargs="*", help="What you want done")
    parser.add_argument("--dry-run", action="store_true", help="Show command but don't run it")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--ai", action="store_true", help="Use OpenAI to route + build commands")
    parser.add_argument("--list-agents", action="store_true", help="List available agents")
    args = parser.parse_args()

    orch = Orchestrator(use_ai=args.ai)

    if args.list_agents:
        for a in orch.agents:
            print(f"- {a.name:10s}  {a.description}")
        return

    if not args.request:
        parser.print_help()
        sys.exit(1)

    text = " ".join(args.request)
    result = orch.handle(text, dry_run=args.dry_run)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        pretty_print(result)

    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()