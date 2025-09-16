#!/usr/bin/env python3
"""
File Serialization Operations Module - V2 Compliant
=================================================

File serialization functionality extracted from consolidated_file_operations.py
for V2 compliance (≤400 lines).

Provides:
- JSON serialization and deserialization
- YAML serialization and deserialization
- File I/O operations with error handling
- Data validation and type checking

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class FileSerializationOperations:
    """Handles file serialization and deserialization operations."""

    def __init__(self):
        self.default_encoding = 'utf-8'
        self.json_indent = 2
        self.yaml_default_flow_style = False

    def save_json(self, data: Any, file_path: Path, indent: int = None) -> bool:
        """Save data to JSON file."""
        try:
            if indent is None:
                indent = self.json_indent
            
            with open(file_path, 'w', encoding=self.default_encoding) as f:
                json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
            
            logger.info(f"Successfully saved JSON data to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save JSON data to {file_path}: {e}")
            return False

    def load_json(self, file_path: Path) -> Any:
        """Load data from JSON file."""
        try:
            with open(file_path, 'r', encoding=self.default_encoding) as f:
                data = json.load(f)
            
            logger.info(f"Successfully loaded JSON data from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load JSON data from {file_path}: {e}")
            raise

    def save_yaml(self, data: Any, file_path: Path, default_flow_style: bool = None) -> bool:
        """Save data to YAML file."""
        try:
            if default_flow_style is None:
                default_flow_style = self.yaml_default_flow_style
            
            with open(file_path, 'w', encoding=self.default_encoding) as f:
                yaml.dump(data, f, default_flow_style=default_flow_style, allow_unicode=True, default_style=None)
            
            logger.info(f"Successfully saved YAML data to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save YAML data to {file_path}: {e}")
            return False

    def load_yaml(self, file_path: Path) -> Any:
        """Load data from YAML file."""
        try:
            with open(file_path, 'r', encoding=self.default_encoding) as f:
                data = yaml.safe_load(f)
            
            logger.info(f"Successfully loaded YAML data from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load YAML data from {file_path}: {e}")
            raise

    def save_text(self, text: str, file_path: Path, encoding: str = None) -> bool:
        """Save text to file."""
        try:
            if encoding is None:
                encoding = self.default_encoding
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(text)
            
            logger.info(f"Successfully saved text to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save text to {file_path}: {e}")
            return False

    def load_text(self, file_path: Path, encoding: str = None) -> str:
        """Load text from file."""
        try:
            if encoding is None:
                encoding = self.default_encoding
            
            with open(file_path, 'r', encoding=encoding) as f:
                text = f.read()
            
            logger.info(f"Successfully loaded text from {file_path}")
            return text
            
        except Exception as e:
            logger.error(f"Failed to load text from {file_path}: {e}")
            raise

    def save_binary(self, data: bytes, file_path: Path) -> bool:
        """Save binary data to file."""
        try:
            with open(file_path, 'wb') as f:
                f.write(data)
            
            logger.info(f"Successfully saved binary data to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save binary data to {file_path}: {e}")
            return False

    def load_binary(self, file_path: Path) -> bytes:
        """Load binary data from file."""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            logger.info(f"Successfully loaded binary data from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load binary data from {file_path}: {e}")
            raise

    def append_text(self, text: str, file_path: Path, encoding: str = None) -> bool:
        """Append text to file."""
        try:
            if encoding is None:
                encoding = self.default_encoding
            
            with open(file_path, 'a', encoding=encoding) as f:
                f.write(text)
            
            logger.info(f"Successfully appended text to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to append text to {file_path}: {e}")
            return False

    def append_json(self, data: Any, file_path: Path) -> bool:
        """Append data to JSON file (as new line)."""
        try:
            json_line = json.dumps(data, ensure_ascii=False, default=str) + '\n'
            return self.append_text(json_line, file_path)
            
        except Exception as e:
            logger.error(f"Failed to append JSON data to {file_path}: {e}")
            return False

    def load_json_lines(self, file_path: Path) -> list[Any]:
        """Load JSON Lines format file."""
        try:
            data = []
            with open(file_path, 'r', encoding=self.default_encoding) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data.append(json.loads(line))
            
            logger.info(f"Successfully loaded {len(data)} JSON lines from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load JSON lines from {file_path}: {e}")
            raise

    def save_json_lines(self, data: list[Any], file_path: Path) -> bool:
        """Save data as JSON Lines format."""
        try:
            with open(file_path, 'w', encoding=self.default_encoding) as f:
                for item in data:
                    json_line = json.dumps(item, ensure_ascii=False, default=str)
                    f.write(json_line + '\n')
            
            logger.info(f"Successfully saved {len(data)} JSON lines to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save JSON lines to {file_path}: {e}")
            return False

    def validate_json(self, file_path: Path) -> bool:
        """Validate JSON file format."""
        try:
            with open(file_path, 'r', encoding=self.default_encoding) as f:
                json.load(f)
            return True
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to validate JSON file {file_path}: {e}")
            return False

    def validate_yaml(self, file_path: Path) -> bool:
        """Validate YAML file format."""
        try:
            with open(file_path, 'r', encoding=self.default_encoding) as f:
                yaml.safe_load(f)
            return True
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in {file_path}: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to validate YAML file {file_path}: {e}")
            return False

    def convert_json_to_yaml(self, json_file: Path, yaml_file: Path) -> bool:
        """Convert JSON file to YAML format."""
        try:
            data = self.load_json(json_file)
            return self.save_yaml(data, yaml_file)
        except Exception as e:
            logger.error(f"Failed to convert JSON to YAML: {e}")
            return False

    def convert_yaml_to_json(self, yaml_file: Path, json_file: Path) -> bool:
        """Convert YAML file to JSON format."""
        try:
            data = self.load_yaml(yaml_file)
            return self.save_json(data, json_file)
        except Exception as e:
            logger.error(f"Failed to convert YAML to JSON: {e}")
            return False

    def get_file_encoding(self, file_path: Path) -> str:
        """Detect file encoding."""
        try:
            import chardet
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                return result.get('encoding', self.default_encoding)
        except Exception as e:
            logger.error(f"Failed to detect encoding for {file_path}: {e}")
            return self.default_encoding

    def set_default_encoding(self, encoding: str):
        """Set default encoding for file operations."""
        self.default_encoding = encoding
        logger.info(f"Default encoding set to {encoding}")

    def set_json_indent(self, indent: int):
        """Set JSON indentation level."""
        self.json_indent = indent
        logger.info(f"JSON indent set to {indent}")

    def set_yaml_flow_style(self, flow_style: bool):
        """Set YAML flow style."""
        self.yaml_default_flow_style = flow_style
        logger.info(f"YAML flow style set to {flow_style}")


if __name__ == "__main__":
    # Example usage
    serialization_ops = FileSerializationOperations()
    
    # Test data
    test_data = {
        "name": "Test Data",
        "values": [1, 2, 3, 4, 5],
        "nested": {
            "key": "value",
            "number": 42
        }
    }
    
    # Test JSON operations
    json_file = Path("test.json")
    if serialization_ops.save_json(test_data, json_file):
        loaded_data = serialization_ops.load_json(json_file)
        print(f"JSON operations successful: {loaded_data == test_data}")
    
    # Test YAML operations
    yaml_file = Path("test.yaml")
    if serialization_ops.save_yaml(test_data, yaml_file):
        loaded_data = serialization_ops.load_yaml(yaml_file)
        print(f"YAML operations successful: {loaded_data == test_data}")
    
    # Test conversion
    if serialization_ops.convert_json_to_yaml(json_file, Path("converted.yaml")):
        print("JSON to YAML conversion successful")
    
    # Cleanup
    for file in [json_file, yaml_file, Path("converted.yaml")]:
        if file.exists():
            file.unlink()
