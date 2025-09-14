#!/usr/bin/env python3
"""
V2 Compliance Analysis CLI Tool
================================

Core tool for analyzing V2 compliance violations and enforcing CI gates.

Features:
- Detect syntax errors, LOC violations, line length issues, and print statements
- Generate detailed violation reports
- Provide CI gate functionality
- Support for different output formats

Usage:
    python tools/analysis_cli.py --violations --n 100000 > runtime/violations_full.txt
    python tools/analysis_cli.py --ci-gate
"""
from __future__ import annotations

import argparse
import ast
import json
import logging
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)
MAX_FILE_LOC = 400
MAX_CLASS_LOC = 100
MAX_FUNCTION_LOC = 50
MAX_LINE_LENGTH = 100
EXCLUDE_PATTERNS = ['__pycache__', '.venv', 'node_modules', '.git', 'build',
    'dist', '*.pyc', '*.pyo', '*.pyd', '.pytest_cache', '.tox', '.coverage',
    'htmlcov', '*.egg-info', '.mypy_cache', '.DS_Store']


def should_exclude_file(path: Path) ->bool:
    """Check if file should be excluded from analysis."""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    if 'test' in path_str.lower() and not path_str.endswith('test_models.py'):
        return False
    return False


def count_lines(node: ast.AST) ->int:
    """Count lines of code for an AST node."""
    if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
        return (node.end_lineno or 0) - (node.lineno or 0) + 1
    return 0


def analyze_python_file(file_path: Path) ->dict[str, Any]:
    """Analyze a single Python file for V2 compliance violations."""
    try:
        with open(file_path, encoding='utf-8') as f:
            source = f.read()
        violations = []
        lines = source.splitlines()
        file_loc = len(lines)
        if file_loc > MAX_FILE_LOC:
            violations.append({'type': 'file_loc', 'file': str(file_path),
                'line': 1, 'message':
                f'File exceeds {MAX_FILE_LOC} LOC ({file_loc} LOC)',
                'severity': 'critical', 'excess': file_loc - MAX_FILE_LOC})
        if 'test' not in str(file_path).lower():
            print_lines = []
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith('print(') or stripped.startswith(
                    'print '):
                    print_lines.append(i)
            if print_lines:
                violations.append({'type': 'print_statement', 'file': str(
                    file_path), 'line': print_lines[0], 'message':
                    f'Found {len(print_lines)} print() statement(s) - use logging instead'
                    , 'severity': 'major', 'lines': print_lines})
        try:
            tree = ast.parse(source, str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_loc = count_lines(node)
                    if class_loc > MAX_CLASS_LOC:
                        violations.append({'type': 'class_loc', 'file': str
                            (file_path), 'line': node.lineno, 'message':
                            f"Class '{node.name}' exceeds {MAX_CLASS_LOC} LOC ({class_loc} LOC)"
                            , 'severity': 'major', 'excess': class_loc -
                            MAX_CLASS_LOC, 'class_name': node.name})
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_loc = count_lines(node)
                    if func_loc > MAX_FUNCTION_LOC:
                        violations.append({'type': 'function_loc', 'file':
                            str(file_path), 'line': node.lineno, 'message':
                            f"Function '{node.name}' exceeds {MAX_FUNCTION_LOC} LOC ({func_loc} LOC)"
                            , 'severity': 'minor', 'excess': func_loc -
                            MAX_FUNCTION_LOC, 'function_name': node.name})
        except SyntaxError as e:
            violations.append({'type': 'syntax_error', 'file': str(
                file_path), 'line': e.lineno or 1, 'message':
                f'Syntax error: {e.msg}', 'severity': 'critical',
                'error_details': str(e)})
        except Exception as e:
            violations.append({'type': 'parse_error', 'file': str(file_path
                ), 'line': 1, 'message': f'Failed to parse file: {str(e)}',
                'severity': 'critical'})
        long_lines = []
        for i, line in enumerate(lines, 1):
            if len(line) > MAX_LINE_LENGTH:
                stripped = line.strip()
                if not (stripped.startswith(('http://', 'https://',
                    'ftp://')) or stripped.startswith('import ') or
                    stripped.startswith('from ')):
                    long_lines.append((i, len(line)))
        if long_lines:
            violations.append({'type': 'line_length', 'file': str(file_path
                ), 'line': long_lines[0][0], 'message':
                f'Found {len(long_lines)} line(s) exceeding {MAX_LINE_LENGTH} characters'
                , 'severity': 'minor', 'long_lines': long_lines})
        return {'file': str(file_path), 'violations': violations, 'stats':
            {'total_lines': file_loc, 'total_violations': len(violations)}}
    except Exception as e:
        return {'file': str(file_path), 'violations': [{'type':
            'file_error', 'file': str(file_path), 'line': 1, 'message':
            f'Failed to analyze file: {str(e)}', 'severity': 'critical'}],
            'stats': {'total_lines': 0, 'total_violations': 1}}


def analyze_project(root_path: Path, max_files: int=100000) ->dict[str, Any]:
    """Analyze entire project for V2 compliance violations."""
    all_files = []
    violations_summary = {'syntax_errors': 0, 'file_loc_violations': 0,
        'class_loc_violations': 0, 'function_loc_violations': 0,
        'line_length_violations': 0, 'print_violations': 0,
        'total_violations': 0, 'files_analyzed': 0, 'files_with_violations': 0}
    logger.info(f'Analyzing Python files in {root_path}...')
    for py_file in root_path.rglob('*.py'):
        if should_exclude_file(py_file):
            continue
        if len(all_files) >= max_files:
            break
        result = analyze_python_file(py_file)
        all_files.append(result)
        if result['violations']:
            violations_summary['files_with_violations'] += 1
        violations_summary['files_analyzed'] += 1
        for violation in result['violations']:
            violations_summary['total_violations'] += 1
            if violation['type'] == 'syntax_error':
                violations_summary['syntax_errors'] += 1
            elif violation['type'] == 'file_loc':
                violations_summary['file_loc_violations'] += 1
            elif violation['type'] == 'class_loc':
                violations_summary['class_loc_violations'] += 1
            elif violation['type'] == 'function_loc':
                violations_summary['function_loc_violations'] += 1
            elif violation['type'] == 'line_length':
                violations_summary['line_length_violations'] += 1
            elif violation['type'] == 'print_statement':
                violations_summary['print_violations'] += 1
    return {'summary': violations_summary, 'files': all_files,
        'analysis_config': {'max_file_loc': MAX_FILE_LOC, 'max_class_loc':
        MAX_CLASS_LOC, 'max_function_loc': MAX_FUNCTION_LOC,
        'max_line_length': MAX_LINE_LENGTH}}


def ci_gate_check(results: dict[str, Any]) ->tuple[bool, str]:
    """Check if project passes CI gate (no critical violations)."""
    summary = results['summary']
    critical_issues = summary['syntax_errors']
    major_issues = summary['file_loc_violations'] + summary[
        'class_loc_violations'] + summary['print_violations']
    if critical_issues > 0:
        return (False,
            f'CRITICAL CI GATE FAILED: {critical_issues} critical violation(s) (syntax errors)'
            )
    if major_issues > 0:
        return (False,
            f'MAJOR CI GATE FAILED: {major_issues} major violation(s)')
    total_violations = summary['total_violations']
    if total_violations > 0:
        return (False,
            f'MINOR CI GATE FAILED: {total_violations} total violation(s)')
    return True, 'SUCCESS CI GATE PASSED: No V2 compliance violations found'


def format_violations_text(results: dict[str, Any]) ->str:
    """Format violations as human-readable text."""
    summary = results['summary']
    files = results['files']
    output = []
    output.append('V2 Compliance Analysis Report')
    output.append('=' * 50)
    output.append('')
    output.append('SUMMARY:')
    output.append(f"Files analyzed: {summary['files_analyzed']}")
    output.append(f"Files with violations: {summary['files_with_violations']}")
    output.append(f"Total violations: {summary['total_violations']}")
    output.append('')
    if summary['syntax_errors'] > 0:
        output.append(f"CRITICAL Syntax errors: {summary['syntax_errors']}")
    if summary['file_loc_violations'] > 0:
        output.append(
            f"CRITICAL File LOC violations: {summary['file_loc_violations']}")
    if summary['class_loc_violations'] > 0:
        output.append(
            f"MAJOR Class LOC violations: {summary['class_loc_violations']}")
    if summary['function_loc_violations'] > 0:
        output.append(
            f"MINOR Function LOC violations: {summary['function_loc_violations']}"
            )
    if summary['line_length_violations'] > 0:
        output.append(
            f"MINOR Line length violations: {summary['line_length_violations']}"
            )
    if summary['print_violations'] > 0:
        output.append(
            f"MAJOR Print statement violations: {summary['print_violations']}")
    output.append('')
    output.append('VIOLATION DETAILS:')
    output.append('')
    for file_result in files:
        if not file_result['violations']:
            continue
        output.append(f"FILE {file_result['file']}:")
        for violation in file_result['violations']:
            severity_icon = {'critical': 'CRITICAL', 'major': 'MAJOR',
                'minor': 'MINOR'}.get(violation['severity'], 'INFO')
            output.append(
                f"  {severity_icon} Line {violation['line']}: {violation['message']}"
                )
            if violation['type'] in ['file_loc', 'class_loc', 'function_loc']:
                output.append(f"    Excess LOC: {violation['excess']}")
        output.append('')
    return '\n'.join(output)


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description=
        'V2 Compliance Analysis CLI Tool')
    parser.add_argument('--violations', action='store_true', help=
        'Analyze and report all V2 compliance violations')
    parser.add_argument('--ci-gate', action='store_true', help=
        'Run CI gate check (fails if any violations found)')
    parser.add_argument('--json', action='store_true', help=
        'Output results as JSON instead of text')
    parser.add_argument('-n', '--max-files', type=int, default=1000, help=
        'Maximum number of files to analyze (default: 1000)')
    parser.add_argument('--root', type=Path, default=Path('.'), help=
        'Root directory to analyze (default: current directory)')
    args = parser.parse_args()
    if not args.violations and not args.ci_gate:
        parser.error('Must specify --violations or --ci-gate')
        return 1  # Return instead of exit

    results = analyze_project(args.root, args.max_files)
    exit_code = 0

    if args.ci_gate:
        passed, message = ci_gate_check(results)
        logger.info(message)
        if args.json:
            gate_result = {'passed': passed, 'message': message, 'summary':
                results['summary']}
            logger.info(json.dumps(gate_result, indent=2))
        exit_code = 0 if passed else 1
    elif args.violations:
        if args.json:
            logger.info(json.dumps(results, indent=2))
        else:
            logger.info(format_violations_text(results))

    return exit_code


if __name__ == '__main__':
    exit_code = main()
    print()  # Add line break for agent coordination
    print("🐝 WE. ARE. SWARM. ⚡️🔥")  # Completion indicator
    sys.exit(exit_code)
