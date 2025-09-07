"""
analyze_test_coverage_part_5.py
Module: analyze_test_coverage_part_5.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:16
"""

# Part 5 of analyze_test_coverage.py
# Original file: .\scripts\analysis\analyze_test_coverage.py

        report.append("")

        high_priority = []
        medium_priority = []
        low_priority = []

        for component_path, coverage in self.test_coverage.items():
            if not coverage["has_tests"]:
                component = coverage["component"]
                priority = component.get("complexity", "UNKNOWN")

                if priority == "HIGH":
                    high_priority.append((component_path, component))
                elif priority == "MEDIUM":
                    medium_priority.append((component_path, component))
                else:
                    low_priority.append((component_path, component))

        # High priority components
        report.append("### 🔴 High Complexity (Critical)")
        for component_path, component in high_priority:
            report.append(f"- **{component_path}** ({component['line_count']} lines)")
            report.append(f"  - Classes: {len(component['classes'])}")
            report.append(f"  - Functions: {len(component['functions'])}")
            report.append("")

        # Medium priority components
        if medium_priority:
            report.append("### 🟡 Medium Complexity (High)")
            for component_path, component in medium_priority:
                report.append(
                    f"- **{component_path}** ({component['line_count']} lines)"
                )
                report.append(f"  - Classes: {len(component['classes'])}")
                report.append(f"  - Functions: {len(component['functions'])}")
                report.append("")

        # Low priority components
        if low_priority:
            report.append("### 🟢 Low Complexity (Medium)")
            for component_path, component in low_priority:
                report.append(
                    f"- **{component_path}** ({component['line_count']} lines)"
                )
                report.append(f"  - Classes: {len(component['classes'])}")
                report.append(f"  - Functions: {len(component['functions'])}")
                report.append("")

        # Test files summary
        report.append("## 🧪 Test Files Summary")

