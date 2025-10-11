"""
Vision CLI - V2 Compliant
========================

Command-line interface for vision system operations.
Provides commands for screen capture, OCR, and visual analysis.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Vision & Automation Specialist
License: MIT
"""

import argparse
import json
import sys
from pathlib import Path

from .integration import VisionSystem


def create_vision_parser() -> argparse.ArgumentParser:
    """Create argument parser for vision CLI."""
    parser = argparse.ArgumentParser(
        description="Vision System CLI", formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Capture command
    capture_parser = subparsers.add_parser("capture", help="Capture screen")
    capture_parser.add_argument("--agent", help="Agent ID for region capture")
    capture_parser.add_argument("--region", help="Region as x,y,width,height")
    capture_parser.add_argument("--output", default="screenshot.png", help="Output filename")
    capture_parser.add_argument("--ocr", action="store_true", help="Extract text with OCR")
    capture_parser.add_argument(
        "--analyze", action="store_true", help="Perform visual analysis"
    )

    # OCR command
    ocr_parser = subparsers.add_parser("ocr", help="Extract text from image")
    ocr_parser.add_argument("--input", required=True, help="Input image file")
    ocr_parser.add_argument("--output", help="Output JSON file")
    ocr_parser.add_argument("--language", default="eng", help="OCR language")

    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Start continuous monitoring")
    monitor_parser.add_argument("--agent", help="Agent ID to monitor")
    monitor_parser.add_argument("--duration", type=int, help="Duration in seconds")
    monitor_parser.add_argument("--frequency", type=float, default=1.0, help="Capture frequency")

    # Analysis command
    analysis_parser = subparsers.add_parser("analyze", help="Analyze image")
    analysis_parser.add_argument("--input", required=True, help="Input image file")
    analysis_parser.add_argument("--output", help="Output JSON file")

    # Info command
    subparsers.add_parser("info", help="Show vision system capabilities")

    return parser


def capture_screen(args: argparse.Namespace) -> None:
    """Capture screen with optional OCR and analysis."""
    vision = VisionSystem()

    try:
        # Parse region if provided
        region = None
        if args.region:
            parts = args.region.split(",")
            if len(parts) == 4:
                region = tuple(map(int, parts))

        # Capture and analyze
        analysis = vision.capture_and_analyze(
            region=region, agent_id=args.agent, include_ocr=args.ocr, include_ui_detection=args.analyze
        )

        if not analysis.get("success"):
            print(f"❌ Capture failed: {analysis.get('error')}")
            sys.exit(1)

        # Save image if capture was successful
        if "image" in analysis:
            vision.screen_capture.save_image(analysis["image"], args.output)
            print(f"✅ Screen captured: {args.output}")

        # Display results
        if args.ocr:
            ocr_results = analysis.get("ocr", {})
            print(f"\n📝 OCR Results:")
            print(f"Text: {ocr_results.get('full_text', 'No text found')[:200]}")
            print(f"Regions: {len(ocr_results.get('text_regions', []))}")

        if args.analyze:
            ui_elements = analysis.get("ui_elements", [])
            print(f"\n🔍 Visual Analysis:")
            print(f"UI Elements: {len(ui_elements)}")

        # Save analysis to JSON
        analysis_file = Path(args.output).with_suffix(".json")
        vision.save_vision_data(analysis, str(analysis_file))
        print(f"📊 Analysis saved: {analysis_file}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def extract_text_from_image(args: argparse.Namespace) -> None:
    """Extract text from image file."""
    vision = VisionSystem()

    try:
        # Load image
        from PIL import Image
        import numpy as np

        image = Image.open(args.input)
        image_array = np.array(image)

        # Extract text
        vision.text_extractor.set_language(args.language)
        ocr_results = vision.text_extractor.extract_text_with_regions(image_array)

        # Display results
        print(f"\n📝 OCR Results:")
        print(f"Text: {ocr_results.get('full_text', 'No text found')}")
        print(f"Regions: {len(ocr_results.get('text_regions', []))}")

        # Save to file if specified
        if args.output:
            with open(args.output, "w") as f:
                json.dump(ocr_results, f, indent=2)
            print(f"\n✅ Results saved: {args.output}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def start_monitoring(args: argparse.Namespace) -> None:
    """Start continuous screen monitoring."""
    vision = VisionSystem()

    def monitoring_callback(analysis):
        """Print monitoring updates."""
        timestamp = analysis.get("timestamp", 0)
        print(f"[{timestamp}] Screen update captured")

    try:
        print(f"🔍 Starting monitoring (duration: {args.duration or 'indefinite'})")
        print("Press Ctrl+C to stop")

        vision.start_monitoring(
            callback=monitoring_callback, duration=args.duration, frequency=args.frequency
        )

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def analyze_image(args: argparse.Namespace) -> None:
    """Analyze image file."""
    vision = VisionSystem()

    try:
        # Load image
        from PIL import Image
        import numpy as np

        image = Image.open(args.input)
        image_array = np.array(image)

        # Perform analysis
        analysis = vision.visual_analyzer.analyze_screen_content(image_array)

        # Display results
        print(f"\n🔍 Visual Analysis Results:")
        print(f"Image Size: {analysis.get('width')}x{analysis.get('height')}")
        print(f"UI Elements: {len(analysis.get('ui_elements', []))}")
        print(f"Edge Density: {analysis.get('edge_density', 0):.2%}")

        # Save to file if specified
        if args.output:
            with open(args.output, "w") as f:
                json.dump(analysis, f, indent=2, default=str)
            print(f"\n✅ Analysis saved: {args.output}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def show_info() -> None:
    """Show vision system capabilities."""
    vision = VisionSystem()
    capabilities = vision.get_vision_capabilities()

    print("\n📊 Vision System Capabilities:\n")
    print(f"Screen Capture: {capabilities['screen_capture']['pil_available']}")
    print(f"OCR: {capabilities['ocr']['tesseract_available']}")
    print(f"Visual Analysis: {capabilities['visual_analysis']['opencv_available']}")
    print(
        f"Coordinate Integration: {capabilities['integration']['coordinate_loader_available']}"
    )
    print(f"Data Persistence: {capabilities['integration']['data_persistence']}")
    print()


def main():
    """Main CLI entry point."""
    parser = create_vision_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "capture":
            capture_screen(args)
        elif args.command == "ocr":
            extract_text_from_image(args)
        elif args.command == "monitor":
            start_monitoring(args)
        elif args.command == "analyze":
            analyze_image(args)
        elif args.command == "info":
            show_info()
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

