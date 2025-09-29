#!/usr/bin/env python3
"""
Protocol Creation Validator - Prevents Unnecessary Protocol Creation
Agent-3: Infrastructure & DevOps Specialist
Mission: V3 Infrastructure Deployment
"""

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ValidationResult:
    """Result of protocol validation"""

    is_necessary: bool
    confidence_score: float
    reasons: list[str]
    alternatives: list[str]
    existing_protocols: list[str]
    recommendations: list[str]


class ProtocolCreationValidator:
    """Validates whether a protocol is necessary before creation"""

    def __init__(self):
        self.protocol_files = self._get_protocol_files()
        self.knowledge_base = self._load_knowledge_base()

    def _get_protocol_files(self) -> list[Path]:
        """Get all protocol files from docs directory"""
        docs_dir = Path("docs")
        protocol_files = []

        if docs_dir.exists():
            for file_path in docs_dir.glob("*.md"):
                if "PROTOCOL" in file_path.name.upper() or "GUIDE" in file_path.name.upper():
                    protocol_files.append(file_path)

        return protocol_files

    def _load_knowledge_base(self) -> dict[str, Any]:
        """Load knowledge base content"""
        kb_file = Path("docs/AGENT_KNOWLEDGE_BASE.md")
        if kb_file.exists():
            try:
                content = kb_file.read_text(encoding="utf-8")
                return {
                    "content": content,
                    "solutions": self._extract_solutions(content),
                    "categories": self._extract_categories(content),
                }
            except:
                return {"content": "", "solutions": [], "categories": []}
        return {"content": "", "solutions": [], "categories": []}

    def _extract_solutions(self, content: str) -> list[str]:
        """Extract solution topics from knowledge base"""
        solutions = []
        lines = content.split("\n")

        for line in lines:
            if line.startswith("### ") or line.startswith("## "):
                solutions.append(line.strip())

        return solutions

    def _extract_categories(self, content: str) -> list[str]:
        """Extract categories from knowledge base"""
        categories = []
        lines = content.split("\n")

        for line in lines:
            if line.startswith("## "):
                categories.append(line.replace("## ", "").strip())

        return categories

    def validate_protocol_necessity(
        self, title: str, description: str, problem_statement: str, proposed_solution: str
    ) -> ValidationResult:
        """Validate if protocol is necessary"""

        reasons = []
        alternatives = []
        existing_protocols = []
        recommendations = []

        # Check 1: Duplicate protocols
        duplicate_check = self._check_duplicates(title, description)
        if duplicate_check["found"]:
            reasons.append(
                f"Similar protocol already exists: {duplicate_check['similar_protocol']}"
            )
            existing_protocols.extend(duplicate_check["existing_protocols"])
            alternatives.append("Extend existing protocol instead of creating new one")

        # Check 2: Knowledge base coverage
        kb_coverage = self._check_knowledge_base_coverage(problem_statement, proposed_solution)
        if kb_coverage["covered"]:
            reasons.append(
                f"Problem already covered in knowledge base: {kb_coverage['relevant_solutions']}"
            )
            alternatives.append("Reference existing knowledge base solutions")

        # Check 3: Over-engineering
        if self._is_over_engineered(description, proposed_solution):
            reasons.append("Solution appears over-engineered for the problem")
            alternatives.append("Consider simpler approach or existing tools")

        # Check 4: Insufficient problem justification
        if not self._has_strong_problem_justification(problem_statement):
            reasons.append("Problem statement lacks sufficient justification")
            recommendations.append("Provide specific examples and measurable impact")

        # Check 5: Solution complexity vs problem size
        complexity_ratio = self._calculate_complexity_ratio(description, problem_statement)
        if complexity_ratio > 0.7:
            reasons.append("Solution complexity exceeds problem scope")
            alternatives.append("Consider simpler, more targeted approach")

        # Check 6: Existing tools coverage
        tools_coverage = self._check_existing_tools_coverage(proposed_solution)
        if tools_coverage["covered"]:
            reasons.append(
                f"Solution can be achieved with existing tools: {tools_coverage['existing_tools']}"
            )
            alternatives.append("Use or extend existing tools instead")

        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            reasons, alternatives, existing_protocols
        )

        # Determine necessity
        is_necessary = confidence_score < 0.3 and len(reasons) < 2

        return ValidationResult(
            is_necessary=is_necessary,
            confidence_score=confidence_score,
            reasons=reasons,
            alternatives=alternatives,
            existing_protocols=existing_protocols,
            recommendations=recommendations,
        )

    def _check_duplicates(self, title: str, description: str) -> dict[str, Any]:
        """Check for duplicate protocols"""
        found = False
        similar_protocol = None
        existing_protocols = []

        for protocol_file in self.protocol_files:
            try:
                content = protocol_file.read_text(encoding="utf-8")

                # Check title similarity
                if self._calculate_similarity(title.lower(), protocol_file.stem.lower()) > 0.6:
                    found = True
                    similar_protocol = protocol_file.name
                    existing_protocols.append(str(protocol_file))

                # Check content similarity
                if self._calculate_similarity(description.lower(), content.lower()) > 0.4:
                    found = True
                    if not similar_protocol:
                        similar_protocol = protocol_file.name
                    existing_protocols.append(str(protocol_file))

            except:
                continue

        return {
            "found": found,
            "similar_protocol": similar_protocol,
            "existing_protocols": existing_protocols,
        }

    def _check_knowledge_base_coverage(self, problem: str, solution: str) -> dict[str, Any]:
        """Check if problem is covered in knowledge base"""
        covered = False
        relevant_solutions = []

        if not self.knowledge_base["content"]:
            return {"covered": False, "relevant_solutions": []}

        # Check problem keywords against knowledge base
        problem_keywords = self._extract_keywords(problem)
        kb_content = self.knowledge_base["content"].lower()

        for keyword in problem_keywords:
            if keyword in kb_content:
                covered = True
                # Find relevant sections
                for solution in self.knowledge_base["solutions"]:
                    if keyword in solution.lower():
                        relevant_solutions.append(solution)

        return {"covered": covered, "relevant_solutions": relevant_solutions[:3]}  # Limit to top 3

    def _is_over_engineered(self, description: str, solution: str) -> bool:
        """Check if solution is over-engineered"""
        over_engineering_indicators = [
            len(description) > 2000,  # Very long description
            "comprehensive framework" in solution.lower(),
            "complete system" in solution.lower(),
            "enterprise-grade" in solution.lower(),
            solution.count("protocol") > 3,
            solution.count("system") > 5,
            "multiple" in solution.lower() and "layers" in solution.lower(),
            "complex" in solution.lower() and "architecture" in solution.lower(),
        ]

        return sum(over_engineering_indicators) >= 3

    def _has_strong_problem_justification(self, problem: str) -> bool:
        """Check if problem statement is well-justified"""
        if len(problem) < 100:
            return False

        justification_indicators = [
            "pain point" in problem.lower(),
            "issue" in problem.lower(),
            "problem" in problem.lower(),
            "inefficient" in problem.lower(),
            "time-consuming" in problem.lower(),
            "error-prone" in problem.lower(),
            "manual" in problem.lower() and "process" in problem.lower(),
            "duplicate" in problem.lower() and "effort" in problem.lower(),
            "standardize" in problem.lower(),
            "consistency" in problem.lower(),
        ]

        return sum(justification_indicators) >= 3

    def _calculate_complexity_ratio(self, description: str, problem: str) -> float:
        """Calculate ratio of solution complexity to problem size"""
        # Simple heuristic: longer description relative to problem suggests over-engineering
        if len(problem) == 0:
            return 1.0

        return min(len(description) / (len(problem) * 2), 1.0)

    def _check_existing_tools_coverage(self, solution: str) -> dict[str, Any]:
        """Check if solution can be achieved with existing tools"""
        covered = False
        existing_tools = []

        tools_dir = Path("tools")
        if not tools_dir.exists():
            return {"covered": False, "existing_tools": []}

        solution_keywords = self._extract_keywords(solution)

        for tool_file in tools_dir.glob("*.py"):
            try:
                content = tool_file.read_text(encoding="utf-8")

                # Check if tool addresses similar functionality
                tool_keywords = self._extract_keywords(content)
                overlap = len(set(solution_keywords) & set(tool_keywords))

                if overlap > 3:  # Significant keyword overlap
                    covered = True
                    existing_tools.append(tool_file.name)

            except:
                continue

        return {"covered": covered, "existing_tools": existing_tools[:3]}  # Limit to top 3

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract meaningful keywords from text"""
        # Simple keyword extraction
        words = text.lower().split()

        # Filter out common words
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "can",
        }

        keywords = [word for word in words if word not in stop_words and len(word) > 3]

        # Remove duplicates and return top keywords
        return list(set(keywords))[:20]

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity"""
        words1 = set(text1.split())
        words2 = set(text2.split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def _calculate_confidence_score(
        self, reasons: list[str], alternatives: list[str], existing_protocols: list[str]
    ) -> float:
        """Calculate confidence score for protocol necessity"""
        # Higher score = less necessary
        score = 0.0

        # Reasons reduce necessity
        score += len(reasons) * 0.2

        # Alternatives reduce necessity
        score += len(alternatives) * 0.15

        # Existing protocols reduce necessity
        score += len(existing_protocols) * 0.1

        # Cap at 1.0
        return min(score, 1.0)

    def get_protocol_alternatives(self, problem: str) -> dict[str, list[str]]:
        """Get alternatives to creating new protocol"""
        alternatives = {
            "existing_protocols": [],
            "knowledge_base_solutions": [],
            "existing_tools": [],
            "simple_approaches": [],
        }

        # Check existing protocols
        for protocol_file in self.protocol_files:
            try:
                content = protocol_file.read_text(encoding="utf-8")
                if any(keyword in content.lower() for keyword in self._extract_keywords(problem)):
                    alternatives["existing_protocols"].append(protocol_file.name)
            except:
                continue

        # Check knowledge base
        if self.knowledge_base["content"]:
            for solution in self.knowledge_base["solutions"]:
                if any(keyword in solution.lower() for keyword in self._extract_keywords(problem)):
                    alternatives["knowledge_base_solutions"].append(solution)

        # Check existing tools
        tools_dir = Path("tools")
        if tools_dir.exists():
            for tool_file in tools_dir.glob("*.py"):
                try:
                    content = tool_file.read_text(encoding="utf-8")
                    if any(
                        keyword in content.lower() for keyword in self._extract_keywords(problem)
                    ):
                        alternatives["existing_tools"].append(tool_file.name)
                except:
                    continue

        # Simple approaches
        alternatives["simple_approaches"] = [
            "Use existing documentation templates",
            "Extend current workflow procedures",
            "Create simple checklist instead of full protocol",
            "Use existing tools with minor modifications",
            "Reference existing protocols and add specific notes",
        ]

        return alternatives


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Protocol Creation Validator")
    parser.add_argument("--validate", action="store_true", help="Validate protocol necessity")
    parser.add_argument(
        "--alternatives", action="store_true", help="Get alternatives to protocol creation"
    )
    parser.add_argument("--title", help="Protocol title")
    parser.add_argument("--description", help="Protocol description")
    parser.add_argument("--problem", help="Problem statement")
    parser.add_argument("--solution", help="Proposed solution")

    args = parser.parse_args()

    validator = ProtocolCreationValidator()

    if args.validate:
        if not all([args.title, args.description, args.problem, args.solution]):
            print(
                "❌ ERROR: All fields required for validation: --title, --description, --problem, --solution"
            )
            return

        result = validator.validate_protocol_necessity(
            args.title, args.description, args.problem, args.solution
        )

        print("📋 PROTOCOL NECESSITY VALIDATION")
        print("=" * 50)
        print(f"Necessary: {'✅ YES' if result.is_necessary else '❌ NO'}")
        print(f"Confidence Score: {result.confidence_score:.2f} (lower = more necessary)")

        if result.reasons:
            print("\n🚨 Reasons against creation:")
            for reason in result.reasons:
                print(f"  - {reason}")

        if result.alternatives:
            print("\n💡 Alternatives:")
            for alternative in result.alternatives:
                print(f"  - {alternative}")

        if result.existing_protocols:
            print("\n📚 Existing protocols:")
            for protocol in result.existing_protocols:
                print(f"  - {protocol}")

        if result.recommendations:
            print("\n🔧 Recommendations:")
            for recommendation in result.recommendations:
                print(f"  - {recommendation}")

    elif args.alternatives:
        if not args.problem:
            print("❌ ERROR: --problem required for alternatives")
            return

        alternatives = validator.get_protocol_alternatives(args.problem)

        print("📋 PROTOCOL ALTERNATIVES")
        print("=" * 50)

        if alternatives["existing_protocols"]:
            print("📚 Existing Protocols:")
            for protocol in alternatives["existing_protocols"]:
                print(f"  - {protocol}")

        if alternatives["knowledge_base_solutions"]:
            print("\n🧠 Knowledge Base Solutions:")
            for solution in alternatives["knowledge_base_solutions"]:
                print(f"  - {solution}")

        if alternatives["existing_tools"]:
            print("\n🛠️ Existing Tools:")
            for tool in alternatives["existing_tools"]:
                print(f"  - {tool}")

        print("\n💡 Simple Approaches:")
        for approach in alternatives["simple_approaches"]:
            print(f"  - {approach}")

    else:
        print("📋 PROTOCOL CREATION VALIDATOR")
        print("=" * 50)
        print("Available commands:")
        print("  --validate      Validate protocol necessity")
        print("  --alternatives  Get alternatives to protocol creation")
        print("\nExample:")
        print(
            "  python protocol_creation_validator.py --validate --title 'New Protocol' --description 'Description' --problem 'Problem statement' --solution 'Proposed solution'"
        )
        print(
            "  python protocol_creation_validator.py --alternatives --problem 'Need to standardize workflow'"
        )


if __name__ == "__main__":
    main()
