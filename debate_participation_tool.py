#!/usr/bin/env python3
"""
SWARM DEBATE PARTICIPATION TOOL
===============================

Tool for agents to participate in SWARM architecture debates.

Author: V2_SWARM_CAPTAIN
License: MIT
"""

import argparse
import sys
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


class DebateParticipationTool:
    """Tool for managing SWARM debate participation."""

    def __init__(self, debate_file: str = "swarm_debate_consolidation.xml"):
        """Initialize the debate participation tool."""
        self.debate_file = Path(debate_file)
        self.agent_id = None
        self.specialty = "Quality Assurance Specialist (CAPTAIN)"

    def set_agent(self, agent_id: str):
        """Set the current agent."""
        self.agent_id = agent_id

    def read_debate_xml(self) -> ET.ElementTree:
        """Read and parse the debate XML file."""
        if not self.debate_file.exists():
            print(f"❌ Debate file not found: {self.debate_file}")
            sys.exit(1)

        try:
            tree = ET.parse(self.debate_file)
            return tree
        except ET.ParseError as e:
            print(f"❌ Failed to parse debate XML: {e}")
            sys.exit(1)

    def write_debate_xml(self, tree: ET.ElementTree):
        """Write the debate XML file."""
        try:
            # Pretty print the XML
            ET.indent(tree, space="    ", level=0)
            tree.write(self.debate_file, encoding='utf-8', xml_declaration=True)
            print(f"✅ Debate file updated: {self.debate_file}")
        except Exception as e:
            print(f"❌ Failed to write debate XML: {e}")
            sys.exit(1)

    def check_debate_status(self):
        """Check the current debate status."""
        tree = self.read_debate_xml()
        root = tree.getroot()

        # Find metadata
        metadata = root.find('.//{http://www.autodreamos.com/swarm/debate}metadata')
        if metadata is not None:
            status = metadata.find('.//{http://www.autodreamos.com/swarm/debate}status')
            deadline = metadata.find('.//{http://www.autodreamos.com/swarm/debate}deadline')

            print("🐝 SWARM DEBATE STATUS")
            print("=" * 50)
            print(f"📊 Status: {status.text if status is not None else 'Unknown'}")
            print(f"⏰ Deadline: {deadline.text if deadline is not None else 'Unknown'}")

            # Count arguments
            arguments = root.findall('.//{http://www.autodreamos.com/swarm/debate}argument')
            print(f"💬 Total Arguments: {len(arguments)}")

            # Count participants
            participants = root.findall('.//{http://www.autodreamos.com/swarm/debate}participant')
            print(f"👥 Total Participants: {len(participants)}")

            # Show arguments by option
            option_counts = {}
            for arg in arguments:
                option = arg.find('.//{http://www.autodreamos.com/swarm/debate}supports_option')
                if option is not None:
                    opt_id = option.text
                    option_counts[opt_id] = option_counts.get(opt_id, 0) + 1

            print("📊 Arguments by Option:")
            for opt, count in option_counts.items():
                print(f"   {opt}: {count} arguments")

    def list_options(self):
        """List all debate options."""
        tree = self.read_debate_xml()
        root = tree.getroot()

        options = root.findall('.//{http://www.autodreamos.com/swarm/debate}option')

        print("🎯 DEBATE OPTIONS")
        print("=" * 50)

        for i, option in enumerate(options, 1):
            option_id = option.find('.//{http://www.autodreamos.com/swarm/debate}option_id')
            title = option.find('.//{http://www.autodreamos.com/swarm/debate}title')
            description = option.find('.//{http://www.autodreamos.com/swarm/debate}description')
            feasibility = option.find('.//{http://www.autodreamos.com/swarm/debate}feasibility_score')

            print(f"{i}. {option_id.text if option_id is not None else 'Unknown'}")
            print(f"   Title: {title.text if title is not None else 'Unknown'}")
            print(f"   Description: {description.text if description is not None else 'Unknown'}")
            print(f"   Feasibility: {feasibility.text if feasibility is not None else 'Unknown'}/10")
            print()

    def list_arguments(self):
        """List all current arguments."""
        tree = self.read_debate_xml()
        root = tree.getroot()

        arguments = root.findall('.//{http://www.autodreamos.com/swarm/debate}argument')

        print("💬 CURRENT ARGUMENTS")
        print("=" * 50)

        for arg in arguments:
            arg_id = arg.find('.//{http://www.autodreamos.com/swarm/debate}argument_id')
            author = arg.find('.//{http://www.autodreamos.com/swarm/debate}author_agent')
            title = arg.find('.//{http://www.autodreamos.com/swarm/debate}title')
            supports = arg.find('.//{http://www.autodreamos.com/swarm/debate}supports_option')
            confidence = arg.find('.//{http://www.autodreamos.com/swarm/debate}confidence_level')
            feasibility = arg.find('.//{http://www.autodreamos.com/swarm/debate}technical_feasibility')
            business_value = arg.find('.//{http://www.autodreamos.com/swarm/debate}business_value')

            print(f"🎯 {title.text if title is not None else 'Unknown'}")
            print(f"   Author: {author.text if author is not None else 'Unknown'}")
            print(f"   Supports: {supports.text if supports is not None else 'Unknown'}")
            print(f"   Confidence: {confidence.text if confidence is not None else 'N/A'}/10")
            print(f"   Feasibility: {feasibility.text if feasibility is not None else 'N/A'}/10")
            print(f"   Business Value: {business_value.text if business_value is not None else 'N/A'}/10")
            print()

    def add_argument(self, title: str, content: str, supports_option: str,
                    confidence: int, technical_feasibility: int, business_value: int):
        """Add a new argument to the debate."""
        if not self.agent_id:
            print("❌ Agent ID not set. Use --agent-id to specify your agent.")
            sys.exit(1)

        tree = self.read_debate_xml()
        root = tree.getroot()

        # Find the arguments section
        arguments_section = root.find('.//{http://www.autodreamos.com/swarm/debate}arguments')
        if arguments_section is None:
            print("❌ Arguments section not found in debate file.")
            sys.exit(1)

        # Create new argument element
        ns = "http://www.autodreamos.com/swarm/debate"
        argument = ET.SubElement(arguments_section, f"{{{ns}}}argument")

        # Generate unique argument ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        arg_id = f"arg_{self.agent_id}_{timestamp}_{unique_id}"

        # Add argument elements
        ET.SubElement(argument, f"{{{ns}}}argument_id").text = arg_id
        ET.SubElement(argument, f"{{{ns}}}author_agent").text = self.agent_id
        ET.SubElement(argument, f"{{{ns}}}timestamp").text = datetime.now().isoformat()
        ET.SubElement(argument, f"{{{ns}}}argument_type").text = "supporting"
        ET.SubElement(argument, f"{{{ns}}}supports_option").text = supports_option
        ET.SubElement(argument, f"{{{ns}}}title").text = title
        ET.SubElement(argument, f"{{{ns}}}content").text = content
        ET.SubElement(argument, f"{{{ns}}}confidence_level").text = str(confidence)
        ET.SubElement(argument, f"{{{ns}}}technical_feasibility").text = str(technical_feasibility)
        ET.SubElement(argument, f"{{{ns}}}business_value").text = str(business_value)

        # Update participant contribution count
        xpath = f'.//{{{ns}}}participant[{{{ns}}}agent_id="{self.agent_id}"]'
        participant = root.find(xpath)
        if participant is not None:
            contribution_count = participant.find(f'{{{ns}}}contribution_count')
            if contribution_count is not None:
                current_count = int(contribution_count.text or "0")
                contribution_count.text = str(current_count + 1)

            last_contribution = participant.find(f'{{{ns}}}last_contribution')
            if last_contribution is not None:
                last_contribution.text = datetime.now().isoformat()

        # Write the updated XML
        self.write_debate_xml(tree)

        print("✅ Argument successfully added!")
        print(f"   ID: {arg_id}")
        print(f"   Title: {title}")
        print(f"   Supports: {supports_option}")
        print(f"   Confidence: {confidence}/10")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="SWARM Debate Participation Tool")
    parser.add_argument("--agent-id", required=True, help="Your agent ID (e.g., Agent-7)")
    parser.add_argument("--status", action="store_true", help="Check debate status")
    parser.add_argument("--list-options", action="store_true", help="List all debate options")
    parser.add_argument("--list-arguments", action="store_true", help="List all current arguments")
    parser.add_argument("--add-argument", action="store_true", help="Add a new argument")
    parser.add_argument("--title", help="Argument title")
    parser.add_argument("--content", help="Argument content")
    parser.add_argument("--supports-option", help="Option to support (option_1, option_2, etc.)")
    parser.add_argument("--confidence", type=int, help="Confidence level (1-10)")
    parser.add_argument("--technical-feasibility", type=int, help="Technical feasibility (1-10)")
    parser.add_argument("--business-value", type=int, help="Business value (1-10)")

    args = parser.parse_args()

    tool = DebateParticipationTool()
    tool.set_agent(args.agent_id)

    if args.status:
        tool.check_debate_status()
    elif args.list_options:
        tool.list_options()
    elif args.list_arguments:
        tool.list_arguments()
    elif args.add_argument:
        if not all([args.title, args.content, args.supports_option,
                   args.confidence is not None, args.technical_feasibility is not None,
                   args.business_value is not None]):
            print("❌ Missing required arguments for --add-argument")
            print("   Required: --title, --content, --supports-option, --confidence, --technical-feasibility, --business-value")
            sys.exit(1)

        tool.add_argument(
            title=args.title,
            content=args.content,
            supports_option=args.supports_option,
            confidence=args.confidence,
            technical_feasibility=args.technical_feasibility,
            business_value=args.business_value
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
