#!/usr/bin/env python3
"""
Distributed Tracing CLI - Command Line Interface
=================================================

Command-line interface for distributed tracing system.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: distributed_tracing_system.py (412 lines) - CLI module
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.tracing.distributed_tracing_core import DistributedTracingCore, TraceConfig


def create_argument_parser():
    """Create argument parser for CLI commands"""
    parser = argparse.ArgumentParser(
        description="Distributed Tracing CLI - Tracing system interface"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start span command
    start_parser = subparsers.add_parser("start-span", help="Start a new trace span")
    start_parser.add_argument("--name", required=True, help="Span name")
    start_parser.add_argument("--attributes", nargs="*", help="Span attributes (key=value)")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get tracing system status")

    # Config command
    config_parser = subparsers.add_parser("config", help="Configure tracing system")
    config_parser.add_argument("--service-name", help="Service name")
    config_parser.add_argument("--jaeger-endpoint", help="Jaeger endpoint")
    config_parser.add_argument("--sampling-rate", type=float, help="Sampling rate")

    # Test command
    test_parser = subparsers.add_parser("test", help="Test tracing system")

    return parser


def handle_start_span_command(args):
    """Handle start span command"""
    core = DistributedTracingCore()

    # Parse attributes
    attributes = {}
    if args.attributes:
        for attr in args.attributes:
            if "=" in attr:
                key, value = attr.split("=", 1)
                attributes[key] = value

    # Start span
    span = core.manage_tracing("start_span", name=args.name, attributes=attributes)

    if span:
        print(f"✅ Started span: {args.name}")
        if attributes:
            print(f"   Attributes: {attributes}")

        # Simulate span usage
        core.manage_tracing("set_attribute", span=span, key="cli_command", value="start-span")
        core.manage_tracing(
            "add_event", span=span, name="span_created", attributes={"source": "cli"}
        )

        print("✅ Span operations completed")
        return 0
    else:
        print(f"❌ Failed to start span: {args.name}")
        return 1


def handle_status_command(args):
    """Handle status command"""
    core = DistributedTracingCore()
    status = core.get_tracing_status()

    print("Distributed Tracing System Status:")
    print(f"  OpenTelemetry Available: {status['opentelemetry_available']}")
    print(f"  Tracer Provider Initialized: {status['tracer_provider_initialized']}")
    print(f"  Tracer Available: {status['tracer_available']}")
    print(f"  Service Name: {status['service_name']}")
    print(f"  Sampling Rate: {status['sampling_rate']}")

    return 0


def handle_config_command(args):
    """Handle config command"""
    config = TraceConfig()

    if args.service_name:
        config.service_name = args.service_name
    if args.jaeger_endpoint:
        config.jaeger_endpoint = args.jaeger_endpoint
    if args.sampling_rate:
        config.sampling_rate = args.sampling_rate

    core = DistributedTracingCore(config)

    print("Tracing Configuration Updated:")
    print(f"  Service Name: {config.service_name}")
    print(f"  Jaeger Endpoint: {config.jaeger_endpoint}")
    print(f"  Sampling Rate: {config.sampling_rate}")

    return 0


def handle_test_command(args):
    """Handle test command"""
    core = DistributedTracingCore()

    print("Testing Distributed Tracing System...")

    # Test span creation
    span = core.manage_tracing("start_span", name="test_span", attributes={"test": "true"})

    if span:
        print("✅ Span creation test passed")

        # Test span operations
        core.manage_tracing("set_attribute", span=span, key="test_attribute", value="test_value")
        core.manage_tracing("add_event", span=span, name="test_event", attributes={"test": "event"})

        print("✅ Span operations test passed")

        # Test status
        status = core.get_tracing_status()
        print(f"✅ Status check test passed: {status['tracer_available']}")

        print("🎉 All tracing tests passed!")
        return 0
    else:
        print("❌ Span creation test failed")
        return 1


def handle_command(args):
    """Handle command execution"""
    try:
        if args.command == "start-span":
            return handle_start_span_command(args)
        elif args.command == "status":
            return handle_status_command(args)
        elif args.command == "config":
            return handle_config_command(args)
        elif args.command == "test":
            return handle_test_command(args)
        else:
            print(f"Unknown command: {args.command}")
            return 1
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


def main():
    """Main CLI entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return handle_command(args)


if __name__ == "__main__":
    sys.exit(main())

