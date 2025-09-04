#!/usr/bin/env python3
"""
Utility Consolidation Coordinator - Agent Cellphone V2
====================================================

Autonomous utility function consolidation system for technical debt elimination.
Identifies and consolidates duplicate utility functions across the codebase.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""



class ConsolidationType(Enum):
    """Types of utility consolidation."""

    DUPLICATE_ELIMINATION = "duplicate_elimination"
    FUNCTION_MERGING = "function_merging"
    MODULE_CONSOLIDATION = "module_consolidation"
    INTERFACE_UNIFICATION = "interface_unification"


@dataclass
class UtilityFunction:
    """Utility function metadata."""

    name: str
    file_path: str
    line_start: int
    line_end: int
    content: str
    parameters: List[str]
    return_type: Optional[str] = None
    complexity_score: int = 0
    usage_count: int = 0


@dataclass
class ConsolidationOpportunity:
    """Consolidation opportunity identified."""

    consolidation_type: ConsolidationType
    primary_function: UtilityFunction
    duplicate_functions: List[UtilityFunction]
    consolidation_strategy: str
    estimated_reduction: int
    priority: str = "MEDIUM"


class UtilityConsolidationCoordinator:
    """
    Autonomous utility function consolidation coordinator.

    Provides comprehensive utility consolidation capabilities:
    - Duplicate function identification
    - Consolidation strategy generation
    - Automated consolidation execution
    - Performance optimization
    - V2 compliance validation
    """

    def __init__(self):
        """Initialize the utility consolidation coordinator."""
        self.utility_functions: Dict[str, List[UtilityFunction]] = {}
        self.consolidation_opportunities: List[ConsolidationOpportunity] = []
        self.consolidation_results: Dict[str, Any] = {}

        # Consolidation patterns
        self.consolidation_patterns = {
            "string_utilities": {
                "pattern": r"(formatString|sanitizeString|validateString)",
                "consolidation_strategy": "Merge into unified StringUtils class",
            },
            "validation_utilities": {
                "pattern": r"(validateEmail|validateUrl|validateInput)",
                "consolidation_strategy": "Merge into unified ValidationUtils class",
            },
            "cache_utilities": {
                "pattern": r"(getCache|setCache|clearCache)",
                "consolidation_strategy": "Merge into unified CacheUtils class",
            },
            "logging_utilities": {
                "pattern": r"(logInfo|logError|logDebug)",
                "consolidation_strategy": "Merge into unified LoggingUtils class",
            },
        }

    def analyze_utility_duplication(self, codebase_path: str = "src") -> Dict[str, Any]:
        """
        Analyze utility function duplication across the codebase.

        Args:
            codebase_path: Path to analyze for utility functions

        Returns:
            Comprehensive duplication analysis results
        """
        get_logger(__name__).info("🔍 Analyzing utility function duplication across codebase...")

        start_time = datetime.now()
        analysis_results = {
            "timestamp": start_time.isoformat(),
            "codebase_path": codebase_path,
            "utility_functions_found": 0,
            "duplicate_functions": 0,
            "consolidation_opportunities": 0,
            "estimated_reduction": 0,
            "analysis_details": {},
        }

        try:
            # Scan for utility functions
            self._scan_utility_functions(codebase_path)

            # Identify duplicates
            self._identify_duplicates()

            # Generate consolidation opportunities
            self._generate_consolidation_opportunities()

            # Calculate metrics
            analysis_results.update(self._calculate_analysis_metrics())

            execution_time = (datetime.now() - start_time).total_seconds()
            analysis_results["execution_time"] = execution_time

            get_logger(__name__).info(
                f"✅ Utility duplication analysis completed in {execution_time:.2f} seconds"
            )
            get_logger(__name__).info(
                f"📊 Found {analysis_results['utility_functions_found']} utility functions"
            )
            get_logger(__name__).info(
                f"🔄 Identified {analysis_results['duplicate_functions']} duplicate functions"
            )
            get_logger(__name__).info(
                f"🎯 Generated {analysis_results['consolidation_opportunities']} consolidation opportunities"
            )

        except Exception as e:
            get_logger(__name__).info(f"❌ Error in utility duplication analysis: {e}")
            analysis_results["error"] = str(e)

        return analysis_results

    def _scan_utility_functions(self, codebase_path: str) -> None:
        """Scan codebase for utility functions."""
        get_logger(__name__).info("🔍 Scanning for utility functions...")

        for root, dirs, files in os.walk(codebase_path):
            for file in files:
                if file.endswith((".js", ".py", ".ts")):
                    file_path = get_unified_utility().path.join(root, file)
                    self._scan_file_for_utilities(file_path)

    def _scan_file_for_utilities(self, file_path: str) -> None:
        """Scan individual file for utility functions."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            # Look for utility function patterns
            for i, line in enumerate(lines):
                # JavaScript function patterns
                js_function_match = re.search(r"function\s+(\w+)\s*\(", line)
                if js_function_match:
                    func_name = js_function_match.group(1)
                    if self._is_utility_function(func_name, content, i):
                        self._extract_function_metadata(
                            func_name, file_path, i, lines, content
                        )

                # Python function patterns
                py_function_match = re.search(r"def\s+(\w+)\s*\(", line)
                if py_function_match:
                    func_name = py_function_match.group(1)
                    if self._is_utility_function(func_name, content, i):
                        self._extract_function_metadata(
                            func_name, file_path, i, lines, content
                        )

        except Exception as e:
            get_logger(__name__).info(f"⚠️ Error scanning file {file_path}: {e}")

    def _is_utility_function(
        self, func_name: str, content: str, line_index: int
    ) -> bool:
        """Determine if a function is a utility function."""
        utility_indicators = [
            "util",
            "helper",
            "common",
            "format",
            "validate",
            "sanitize",
            "parse",
            "convert",
            "transform",
            "process",
            "clean",
            "normalize",
        ]

        # Check function name
        func_lower = func_name.lower()
        if any(indicator in func_lower for indicator in utility_indicators):
            return True

        # Check for utility class patterns
        if re.search(r"class\s+\w*Util\w*", content):
            return True

        return False

    def _extract_function_metadata(
        self,
        func_name: str,
        file_path: str,
        line_index: int,
        lines: List[str],
        content: str,
    ) -> None:
        """Extract metadata for a utility function."""
        # Find function end
        end_line = self._find_function_end(lines, line_index)

        # Extract function content
        func_content = "\n".join(lines[line_index : end_line + 1])

        # Extract parameters
        params = self._extract_parameters(func_content)

        # Calculate complexity
        complexity = self._calculate_complexity(func_content)

        utility_func = UtilityFunction(
            name=func_name,
            file_path=file_path,
            line_start=line_index + 1,
            line_end=end_line + 1,
            content=func_content,
            parameters=params,
            complexity_score=complexity,
        )

        # Group by function name
        if func_name not in self.utility_functions:
            self.utility_functions[func_name] = []
        self.utility_functions[func_name].append(utility_func)

    def _find_function_end(self, lines: List[str], start_line: int) -> int:
        """Find the end of a function."""
        brace_count = 0
        in_function = False

        for i in range(start_line, len(lines)):
            line = lines[i]

            # Count braces/brackets
            brace_count += line.count("{") - line.count("}")
            brace_count += line.count("(") - line.count(")")

            if not in_function and ("{" in line or "(" in line):
                in_function = True
            elif in_function and brace_count <= 0:
                return i

        return len(lines) - 1

    def _extract_parameters(self, func_content: str) -> List[str]:
        """Extract function parameters."""
        param_match = re.search(r"\(([^)]*)\)", func_content)
        if param_match:
            params_str = param_match.group(1).strip()
            if params_str:
                return [p.strip() for p in params_str.split(",")]
        return []

    def _calculate_complexity(self, func_content: str) -> int:
        """Calculate function complexity score."""
        complexity_indicators = [
            "if",
            "else",
            "for",
            "while",
            "switch",
            "case",
            "try",
            "catch",
            "&&",
            "||",
            "?",
            ":",
            "return",
        ]

        complexity = 1  # Base complexity
        for indicator in complexity_indicators:
            complexity += func_content.count(indicator)

        return complexity

    def _identify_duplicates(self) -> None:
        """Identify duplicate utility functions."""
        get_logger(__name__).info("🔄 Identifying duplicate utility functions...")

        for func_name, functions in self.utility_functions.items():
            if len(functions) > 1:
                # Group by similar functionality
                self._group_similar_functions(func_name, functions)

    def _group_similar_functions(
        self, func_name: str, functions: List[UtilityFunction]
    ) -> None:
        """Group similar functions for consolidation."""
        # Simple similarity check based on parameters and complexity
        groups = []

        for func in functions:
            added_to_group = False
            for group in groups:
                if self._are_functions_similar(func, group[0]):
                    group.append(func)
                    added_to_group = True
                    break

            if not get_unified_validator().validate_required(added_to_group):
                groups.append([func])

        # Create consolidation opportunities for groups with duplicates
        for group in groups:
            if len(group) > 1:
                opportunity = ConsolidationOpportunity(
                    consolidation_type=ConsolidationType.DUPLICATE_ELIMINATION,
                    primary_function=group[0],
                    duplicate_functions=group[1:],
                    consolidation_strategy=f"Merge {len(group)} duplicate {func_name} functions",
                    estimated_reduction=sum(
                        len(f.content.split("\n")) for f in group[1:]
                    ),
                )
                self.consolidation_opportunities.append(opportunity)

    def _are_functions_similar(
        self, func1: UtilityFunction, func2: UtilityFunction
    ) -> bool:
        """Check if two functions are similar enough to consolidate."""
        # Check parameter similarity
        params1 = set(func1.parameters)
        params2 = set(func2.parameters)
        param_similarity = len(params1.intersection(params2)) / max(
            len(params1), len(params2), 1
        )

        # Check complexity similarity
        complexity_diff = abs(func1.complexity_score - func2.complexity_score)

        return param_similarity > 0.5 and complexity_diff < 5

    def _generate_consolidation_opportunities(self) -> None:
        """Generate consolidation opportunities based on patterns."""
        get_logger(__name__).info("🎯 Generating consolidation opportunities...")

        for pattern_name, pattern_info in self.consolidation_patterns.items():
            pattern = pattern_info["pattern"]
            strategy = pattern_info["consolidation_strategy"]

            matching_functions = []
            for func_name, functions in self.utility_functions.items():
                if re.search(pattern, func_name, re.IGNORECASE):
                    matching_functions.extend(functions)

            if len(matching_functions) > 1:
                opportunity = ConsolidationOpportunity(
                    consolidation_type=ConsolidationType.MODULE_CONSOLIDATION,
                    primary_function=matching_functions[0],
                    duplicate_functions=matching_functions[1:],
                    consolidation_strategy=strategy,
                    estimated_reduction=len(matching_functions) * 10,  # Estimate
                    priority="HIGH",
                )
                self.consolidation_opportunities.append(opportunity)

    def _calculate_analysis_metrics(self) -> Dict[str, Any]:
        """Calculate analysis metrics."""
        total_functions = sum(
            len(functions) for functions in self.utility_functions.values()
        )
        duplicate_functions = sum(
            len(functions) - 1
            for functions in self.utility_functions.values()
            if len(functions) > 1
        )
        total_reduction = sum(
            opp.estimated_reduction for opp in self.consolidation_opportunities
        )

        return {
            "utility_functions_found": total_functions,
            "duplicate_functions": duplicate_functions,
            "consolidation_opportunities": len(self.consolidation_opportunities),
            "estimated_reduction": total_reduction,
            "analysis_details": {
                "function_groups": len(self.utility_functions),
                "high_priority_opportunities": len(
                    [
                        opp
                        for opp in self.consolidation_opportunities
                        if opp.priority == "HIGH"
                    ]
                ),
                "medium_priority_opportunities": len(
                    [
                        opp
                        for opp in self.consolidation_opportunities
                        if opp.priority == "MEDIUM"
                    ]
                ),
                "low_priority_opportunities": len(
                    [
                        opp
                        for opp in self.consolidation_opportunities
                        if opp.priority == "LOW"
                    ]
                ),
            },
        }

    def generate_consolidation_report(self) -> Dict[str, Any]:
        """Generate comprehensive consolidation report."""
        get_logger(__name__).info("📊 Generating consolidation report...")

        report = {
            "timestamp": datetime.now().isoformat(),
            "consolidation_summary": {
                "total_opportunities": len(self.consolidation_opportunities),
                "estimated_lines_reduced": sum(
                    opp.estimated_reduction for opp in self.consolidation_opportunities
                ),
                "high_priority_count": len(
                    [
                        opp
                        for opp in self.consolidation_opportunities
                        if opp.priority == "HIGH"
                    ]
                ),
                "consolidation_types": {},
            },
            "detailed_opportunities": [],
            "recommendations": [],
        }

        # Group by consolidation type
        for opp in self.consolidation_opportunities:
            cons_type = opp.consolidation_type.value
            if cons_type not in report["consolidation_summary"]["consolidation_types"]:
                report["consolidation_summary"]["consolidation_types"][cons_type] = 0
            report["consolidation_summary"]["consolidation_types"][cons_type] += 1

            # Add detailed opportunity
            report["detailed_opportunities"].append(
                {
                    "type": cons_type,
                    "primary_function": opp.primary_function.name,
                    "duplicate_count": len(opp.duplicate_functions),
                    "strategy": opp.consolidation_strategy,
                    "estimated_reduction": opp.estimated_reduction,
                    "priority": opp.priority,
                    "files_affected": list(
                        set(
                            [
                                f.file_path
                                for f in [opp.primary_function]
                                + opp.duplicate_functions
                            ]
                        )
                    ),
                }
            )

        # Generate recommendations
        report["recommendations"] = self._generate_recommendations()

        return report

    def _generate_recommendations(self) -> List[str]:
        """Generate consolidation recommendations."""
        recommendations = []

        if self.consolidation_opportunities:
            recommendations.append(
                "🚀 HIGH PRIORITY: Consolidate duplicate utility functions to eliminate technical debt"
            )
            recommendations.append(
                "📦 MODULE CONSOLIDATION: Merge similar utility modules into unified classes"
            )
            recommendations.append(
                "🔧 INTERFACE UNIFICATION: Standardize utility function interfaces across modules"
            )
            recommendations.append(
                "⚡ PERFORMANCE: Reduce code duplication to improve maintainability"
            )
            recommendations.append(
                "✅ V2 COMPLIANCE: Ensure consolidated utilities meet V2 standards"
            )

        return recommendations


if __name__ == "__main__":
    coordinator = UtilityConsolidationCoordinator()

    get_logger(__name__).info("🚀 AUTONOMOUS UTILITY CONSOLIDATION COORDINATOR")
    get_logger(__name__).info("=" * 60)

    # Analyze utility duplication
    analysis_results = coordinator.analyze_utility_duplication()

    # Generate consolidation report
    consolidation_report = coordinator.generate_consolidation_report()

    get_logger(__name__).info("\n📊 CONSOLIDATION REPORT:")
    get_logger(__name__).info(json.dumps(consolidation_report, indent=2))

    get_logger(__name__).info("\n✅ Autonomous utility consolidation analysis complete!")
