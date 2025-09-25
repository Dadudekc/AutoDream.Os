#!/usr/bin/env python3
"""
Security CLI Tool
================

Command-line interface for security management using existing components.

V2 Compliance: ≤400 lines, single responsibility
Author: Security Implementation Team
License: MIT
"""

import click
import json
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

# Import existing security components
from .security_manager import SecurityManager, SecurityLevel
from ..validation.enhanced_security_validator import EnhancedSecurityValidator


@click.group()
def security():
    """Security management CLI tool."""
    pass


@security.group()
def validate():
    """Input validation commands."""
    pass


@validate.command()
@click.argument('input_value')
@click.argument('input_type')
def input(input_value: str, input_type: str):
    """Validate input value."""
    validator = EnhancedSecurityValidator()
    result = validator.validate_input(input_value, input_type)
    
    if result["is_valid"]:
        click.echo(f"✅ Input is valid: {result['sanitized_value']}")
    else:
        click.echo(f"❌ Input validation failed:")
        for error in result["errors"]:
            click.echo(f"  - {error}")


@security.group()
def analyze():
    """Security analysis commands."""
    pass


@analyze.command()
@click.option('--project-path', default='.', help='Project path to analyze')
@click.option('--output', help='Output file for report')
def static(project_path: str, output: Optional[str]):
    """Run static security analysis."""
    validator = EnhancedSecurityValidator()
    
    click.echo("🔍 Running enhanced security analysis...")
    result = validator.validate()
    
    click.echo(f"\n📊 Analysis Results:")
    click.echo(f"Status: {result['status']}")
    click.echo(f"Files scanned: {result['results']['total_files_scanned']}")
    click.echo(f"Total findings: {result['results']['total_findings']}")
    click.echo(f"Real violations: {result['results']['real_violations']}")
    click.echo(f"False positives: {result['results']['false_positives']}")
    
    if result['results']['real_violations'] > 0:
        click.echo(f"\n🚨 Real Violations:")
        for violation in result['results']['real_violations_list']:
            click.echo(f"  {violation['file']}:{violation['line']} - {violation['type']}")
    
    if output:
        with open(output, 'w') as f:
            json.dump(result, f, indent=2)
        click.echo(f"📄 Report saved to: {output}")


@security.group()
def password():
    """Password management commands."""
    pass


@password.command()
@click.argument('password')
def hash(password: str):
    """Hash a password securely."""
    security_manager = SecurityManager()
    
    try:
        password_hash, salt = security_manager.hash_password(password)
        click.echo(f"🔐 Password hashed successfully")
        click.echo(f"Algorithm: {salt}")
        click.echo(f"Hash: {password_hash}")
        
    except Exception as e:
        click.echo(f"❌ Error hashing password: {e}")


@password.command()
@click.argument('password')
@click.argument('password_hash')
@click.argument('salt')
def verify(password: str, password_hash: str, salt: str):
    """Verify a password against its hash."""
    security_manager = SecurityManager()
    
    try:
        is_valid = security_manager.verify_password(password, password_hash, salt)
        if is_valid:
            click.echo("✅ Password verification successful")
        else:
            click.echo("❌ Password verification failed")
            
    except Exception as e:
        click.echo(f"❌ Error verifying password: {e}")


@security.group()
def session():
    """Session management commands."""
    pass


@session.command()
@click.argument('user_id')
@click.option('--agent-id', help='Agent ID')
@click.option('--roles', help='Comma-separated roles')
def create(user_id: str, agent_id: Optional[str], roles: Optional[str]):
    """Create a new session."""
    security_manager = SecurityManager()
    
    try:
        roles_list = roles.split(',') if roles else []
        token = security_manager.create_session(user_id, agent_id, roles_list)
        click.echo(f"✅ Session created successfully")
        click.echo(f"Token: {token}")
        
    except Exception as e:
        click.echo(f"❌ Error creating session: {e}")


@session.command()
@click.argument('token')
def validate(token: str):
    """Validate a session token."""
    security_manager = SecurityManager()
    
    try:
        session_info = security_manager.validate_session(token)
        if session_info:
            click.echo("✅ Session is valid")
            click.echo(f"User ID: {session_info['user_id']}")
            click.echo(f"Agent ID: {session_info.get('agent_id', 'N/A')}")
            click.echo(f"Roles: {', '.join(session_info.get('roles', []))}")
        else:
            click.echo("❌ Session is invalid or expired")
            
    except Exception as e:
        click.echo(f"❌ Error validating session: {e}")


@session.command()
@click.argument('token')
def revoke(token: str):
    """Revoke a session token."""
    security_manager = SecurityManager()
    
    try:
        success = security_manager.revoke_session(token)
        if success:
            click.echo("✅ Session revoked successfully")
        else:
            click.echo("❌ Session not found")
            
    except Exception as e:
        click.echo(f"❌ Error revoking session: {e}")


@security.command()
@click.option('--project-path', default='.', help='Project path to scan')
@click.option('--output', help='Output file for comprehensive report')
def audit(project_path: str, output: Optional[str]):
    """Run comprehensive security audit."""
    click.echo("🔍 Starting comprehensive security audit...")
    
    # Static analysis
    click.echo("\n📋 Running static analysis...")
    validator = EnhancedSecurityValidator()
    static_result = validator.validate()
    
    # Display summary
    click.echo(f"\n📊 Security Audit Summary:")
    click.echo(f"Status: {static_result['status']}")
    click.echo(f"Files scanned: {static_result['results']['total_files_scanned']}")
    click.echo(f"Real violations: {static_result['results']['real_violations']}")
    click.echo(f"False positives: {static_result['results']['false_positives']}")
    
    # Generate comprehensive report
    audit_report = {
        "audit_metadata": {
            "timestamp": datetime.now().isoformat(),
            "project_path": project_path,
            "audit_type": "comprehensive"
        },
        "static_analysis": static_result,
        "summary": {
            "overall_status": static_result['status'],
            "critical_issues": static_result['results']['real_violations'],
            "recommendations": _generate_recommendations(static_result)
        }
    }
    
    if audit_report['summary']['recommendations']:
        click.echo(f"\n💡 Recommendations:")
        for rec in audit_report['summary']['recommendations']:
            click.echo(f"  - {rec}")
    
    # Save report
    if output:
        with open(output, 'w') as f:
            json.dump(audit_report, f, indent=2)
        click.echo(f"\n📄 Comprehensive report saved to: {output}")


def _generate_recommendations(static_result: dict) -> list:
    """Generate security recommendations."""
    recommendations = []
    
    if static_result['status'] == 'FAILED':
        real_violations = static_result['results']['real_violations']
        if real_violations > 0:
            recommendations.append(f"Address {real_violations} security violations")
    
    false_positives = static_result['results']['false_positives']
    if false_positives > 0:
        recommendations.append(f"Review {false_positives} false positive findings")
    
    if static_result['results']['real_violations'] > 0:
        recommendations.append("Review and fix hardcoded secrets")
        recommendations.append("Implement proper secret management")
    
    return recommendations


if __name__ == '__main__':
    security()

