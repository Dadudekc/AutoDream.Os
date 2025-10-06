#!/usr/bin/env python3
"""
Generate .env.example from .env file
Creates a template version with placeholder values
"""

import os
import re
from collections import defaultdict


def generate_env_example():
    """Generate .env.example from .env file"""

    env_file = ".env"
    if not os.path.exists(env_file):
        print("❌ .env file not found")
        return False

    try:
        with open(env_file, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

    # Parse environment variables
    env_vars = defaultdict(list)
    comments = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Handle comments
        if line.startswith("#"):
            comments.append(line)
            continue

        # Handle key=value pairs
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            # Determine placeholder based on key name and value pattern
            if detect_sensitive_value(key, value):
                placeholder = generate_placeholder(key, value)
            else:
                # Keep non-sensitive values
                placeholder = value

            env_vars[key].append(placeholder)

    # Generate organized .env.example
    sections = organize_into_sections(env_vars, comments)

    try:
        with open(".env.example", "w", encoding="utf-8") as f:
            write_env_example(f, sections)
        print("✅ .env.example generated successfully")
        return True
    except Exception as e:
        print(f"❌ Error writing .env.example: {e}")
        return False


def detect_sensitive_value(key, value):
    """Detect if a value is sensitive and should be replaced with placeholder"""

    sensitive_patterns = [
        r"token|secret|key|password|pass|phrase",
        r"api.*key|bot.*token",
        r"webhook.*url",
        r"channel.*id|guild.*id",
        r"connection.*string",
        r"redis.*password|rabbitmq.*password",
    ]

    key_lower = key.lower()
    for pattern in sensitive_patterns:
        if re.search(pattern, key_lower):
            return True

    # Check if value looks like sensitive data
    sensitive_value_patterns = [
        r"^[a-zA-Z0-9-_]{20,}$",  # Long tokens
        r"^.+/api/webhooks/.+",  # Webhook URLs
        r"^\d{17,19}$",  # Discord IDs
        r"^[a-zA-Z0-9]{20,50}$",  # API keys
    ]

    for pattern in sensitive_value_patterns:
        if re.match(pattern, value):
            return True

    return False


def generate_placeholder(key, value):
    """Generate appropriate placeholder for key"""

    key_lower = key.lower()

    # Channel/Guild IDs
    if "channel_id" in key_lower or "guild_id" in key_lower:
        if re.match(r"^\d{17,19}$", value):
            return "your_channel_id_here"
        return "your_" + key_lower.replace("_", "_").replace("discord", "discord_") + "_here"

    # Webhook URLs
    if "webhook" in key_lower:
        return "https://discord.com/api/webhooks/your_webhook_url_here"

    # API Keys
    if "api_key" in key_lower or "token" in key_lower:
        return "your_" + key.split("_")[0].lower() + "_key_here"

    # Database connections
    if "connection" in key_lower and "string" in key_lower:
        return "your_postgres_connection_here"

    # Default placeholder
    return "your_" + key_lower.replace("_", "_") + "_here"


def organize_into_sections(env_vars, comments):
    """Organize environment variables into logical sections"""

    sections = {
        "GENERAL": [],
        "DISCORD": [],
        "API_KEYS": [],
        "DATABASE": [],
        "SECURITY": [],
        "TESTING": [],
        "PATHS": [],
        "OTHER": [],
    }

    for key, values in env_vars.items():
        key_lower = key.lower()
        value = values[0]  # Take first value

        if "discord" in key_lower:
            sections["DISCORD"].append((key, value))
        elif any(x in key_lower for x in ["api_key", "token"]):
            sections["API_KEYS"].append((key, value))
        elif any(x in key_lower for x in ["database", "db_", "connection"]):
            sections["DATABASE"].append((key, value))
        elif any(x in key_lower for x in ["secret", "password", "security"]):
            sections["SECURITY"].append((key, value))
        elif any(x in key_lower for x in ["test", "debug", "development"]):
            sections["TESTING"].append((key, value))
        elif any(x in key_lower for x in ["path", "directory", "dir"]):
            sections["PATHS"].append((key, value))
        else:
            sections["OTHER"].append((key, value))

    return sections


def write_env_example(f, sections):
    """Write organized .env.example file"""

    f.write("# Environment Configuration - Generated from .env\n")
    f.write("# Copy this file to .env and modify values as needed\n")
    f.write("# Generated by: generate_env_example.py\n\n")

    section_names = {
        "GENERAL might be necessary": "General Configuration",
        "DISCORD": "Discord Configuration",
        "API_KEYS": "API Keys and Tokens",
        "DATABASE": "Database Configuration",
        "SECURITY": "Security and Secrets",
        "TESTING": "Testing and Development",
        "PATHS": "Paths and Directories",
        "OTHER": "Other Configuration",
    }

    for section_key, section_vars in sections.items():
        if not section_vars:
            continue

        section_title = section_names.get(section_key, section_key)
        f.write(
            "\n# =============================================================================\n"
        )
        f.write(f"# {section_title.upper()}\n")
        f.write("# =============================================================================\n")

        for key, value in sorted(section_vars):
            # Add helpful comments for common keys
            if "discord" in key.lower():
                if "channel" in key.lower():
                    f.write("# Discord Channel ID (numeric only)\n")
                elif "webhook" in key.lower():
                    f.write("# Discord Webhook URL (complete URL)\n")

            f.write(f"{key}={value}\n")

        f.write("\n")


if __name__ == "__main__":
    success = generate_env_example()
    if success:
        print("✅ Operation completed successfully")
    else:
        print("❌ Operation failed")
        exit(1)
