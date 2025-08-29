    import argparse
from src.utils.validators import (

#!/usr/bin/env python3
"""Facade module aggregating various validation utilities."""

    DataValidators,
    FormatValidators,
    ValueValidators,
)


class ValidationUtils(FormatValidators, DataValidators, ValueValidators):
    """Facade combining different validator categories."""


def main() -> None:
    """CLI interface for validation utilities testing."""

    parser = argparse.ArgumentParser(description="Validation Utils CLI")
    parser.add_argument("--email", help="Validate email address")
    parser.add_argument("--url", help="Validate URL")
    parser.add_argument("--json", help="Validate JSON string")
    parser.add_argument("--file-ext", help="Validate file extension")
    parser.add_argument("--string-length", help="Validate string length")
    parser.add_argument("--numeric-range", help="Validate numeric range")
    parser.add_argument("--choice", help="Validate choice")
    parser.add_argument("--pattern", help="Validate pattern")

    args = parser.parse_args()

    if args.email:
        is_valid = ValidationUtils.is_valid_email(args.email)
        print(f"Email '{args.email}' is valid: {is_valid}")
    elif args.url:
        is_valid = ValidationUtils.is_valid_url(args.url)
        print(f"URL '{args.url}' is valid: {is_valid}")
    elif args.json:
        is_valid = ValidationUtils.validate_json_string(args.json)
        print(f"JSON string is valid: {is_valid}")
    elif args.file_ext:
        is_valid = ValidationUtils.validate_file_extension(
            args.file_ext, ["txt", "json", "yaml"]
        )
        print(f"File extension is valid: {is_valid}")
    elif args.string_length:
        is_valid = ValidationUtils.validate_string_length(args.string_length, 1, 100)
        print(f"String length is valid: {is_valid}")
    elif args.numeric_range:
        try:
            value = float(args.numeric_range)
            is_valid = ValidationUtils.validate_numeric_range(value, 0, 100)
            print(f"Numeric range is valid: {is_valid}")
        except ValueError:
            print("Invalid numeric value")
    elif args.choice:
        is_valid = ValidationUtils.validate_choice(
            args.choice, ["option1", "option2", "option3"]
        )
        print(f"Choice is valid: {is_valid}")
    elif args.pattern:
        is_valid = ValidationUtils.validate_pattern(args.pattern, r"^[A-Za-z0-9]+$")
        print(f"Pattern is valid: {is_valid}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
