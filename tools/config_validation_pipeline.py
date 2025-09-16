import logging
logger = logging.getLogger(__name__)
"""
Configuration Validation Pipeline
=================================

Infrastructure & DevOps support for CONFIG-ORGANIZE-001 mission.
Validates configuration files and schemas with comprehensive error reporting.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: CONFIG-ORGANIZE-001 - Configuration and Schema Management
"""
import json
import yaml
import jsonschema
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationResult:
    """Result of configuration validation."""
    file_path: str
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    validation_time: float


class ConfigurationValidator:
    """Validates configuration files and schemas."""

    def __init__(self, config_dir: str='config', schema_dir: str='schemas'):
        self.config_dir = Path(config_dir)
        self.schema_dir = Path(schema_dir)
        self.validation_results: List[ValidationResult] = []

    def validate_all_configs(self) ->Dict[str, Any]:
        """Validate all configuration files."""
        start_time = datetime.now()
        validation_summary = {'timestamp': start_time.isoformat(),
            'total_files': 0, 'valid_files': 0, 'invalid_files': 0,
            'total_errors': 0, 'total_warnings': 0, 'results': []}
        config_files = self._find_config_files()
        validation_summary['total_files'] = len(config_files)
        for file_path in config_files:
            result = self._validate_file(file_path)
            self.validation_results.append(result)
            validation_summary['results'].append({'file': str(file_path),
                'valid': result.is_valid, 'errors': len(result.errors),
                'warnings': len(result.warnings)})
            if result.is_valid:
                validation_summary['valid_files'] += 1
            else:
                validation_summary['invalid_files'] += 1
            validation_summary['total_errors'] += len(result.errors)
            validation_summary['total_warnings'] += len(result.warnings)
        end_time = datetime.now()
        validation_summary['duration'] = (end_time - start_time).total_seconds(
            )
        return validation_summary

    def _find_config_files(self) ->List[Path]:
        """Find all configuration files to validate."""
        config_extensions = ['.yaml', '.yml', '.json']
        config_files = []
        if not self.config_dir.exists():
            return config_files
        for file_path in self.config_dir.iterdir():
            if file_path.is_file() and file_path.suffix in config_extensions:
                config_files.append(file_path)
        return config_files

    def _validate_file(self, file_path: Path) ->ValidationResult:
        """Validate a single configuration file."""
        start_time = datetime.now()
        errors = []
        warnings = []
        try:
            if file_path.suffix in ['.yaml', '.yml']:
                self._validate_yaml_file(file_path, errors, warnings)
            elif file_path.suffix == '.json':
                self._validate_json_file(file_path, errors, warnings)
            self._validate_config_structure(file_path, errors, warnings)
        except Exception as e:
            errors.append(f'Validation error: {str(e)}')
        end_time = datetime.now()
        validation_time = (end_time - start_time).total_seconds()
        return ValidationResult(file_path=str(file_path), is_valid=len(
            errors) == 0, errors=errors, warnings=warnings, validation_time
            =validation_time)

    def _validate_yaml_file(self, file_path: Path, errors: List[str],
        warnings: List[str]) ->None:
        """Validate YAML file syntax and structure."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            if content is None:
                warnings.append('File is empty or contains only comments')
            elif not isinstance(content, dict):
                errors.append('Root element must be a dictionary/mapping')
        except yaml.YAMLError as e:
            errors.append(f'YAML syntax error: {str(e)}')
        except Exception as e:
            errors.append(f'File read error: {str(e)}')

    def _validate_json_file(self, file_path: Path, errors: List[str],
        warnings: List[str]) ->None:
        """Validate JSON file syntax and structure."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            if not isinstance(content, dict):
                errors.append('Root element must be a dictionary/object')
        except json.JSONDecodeError as e:
            errors.append(f'JSON syntax error: {str(e)}')
        except Exception as e:
            errors.append(f'File read error: {str(e)}')

    def _validate_config_structure(self, file_path: Path, errors: List[str],
        warnings: List[str]) ->None:
        """Validate configuration file structure and content."""
        file_name = file_path.name.lower()
        if 'unified_config' in file_name:
            self._validate_unified_config(file_path, errors, warnings)
        elif 'coordinates' in file_name:
            self._validate_coordinates_config(file_path, errors, warnings)
        elif 'messaging' in file_name:
            self._validate_messaging_config(file_path, errors, warnings)
        elif 'discord' in file_name:
            self._validate_discord_config(file_path, errors, warnings)

    def _validate_unified_config(self, file_path: Path, errors: List[str],
        warnings: List[str]) ->None:
        """Validate unified configuration structure."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            required_sections = ['system', 'agents', 'messaging']
            for section in required_sections:
                if section not in config:
                    errors.append(f'Missing required section: {section}')
            if 'system' in config:
                system = config['system']
                required_system_fields = ['name', 'version']
                for field in required_system_fields:
                    if field not in system:
                        errors.append(f'Missing system field: {field}')
            if 'agents' in config:
                agents = config['agents']
                if 'coordinates' not in agents:
                    warnings.append('Missing agents.coordinates section')
        except Exception as e:
            errors.append(f'Unified config validation error: {str(e)}')

    def _validate_coordinates_config(self, file_path: Path, errors: List[
        str], warnings: List[str]) ->None:
        """Validate coordinates configuration structure."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            if 'agents' not in config:
                errors.append("Missing 'agents' section")
            else:
                agents = config['agents']
                for agent_id, agent_config in agents.items():
                    required_fields = ['chat_input_coordinates',
                        'onboarding_input_coords']
                    for field in required_fields:
                        if field not in agent_config:
                            errors.append(
                                f'Agent {agent_id} missing field: {field}')
                        elif not isinstance(agent_config[field], list) or len(
                            agent_config[field]) != 2:
                            errors.append(
                                f'Agent {agent_id} {field} must be a list of 2 coordinates'
                                )
        except Exception as e:
            errors.append(f'Coordinates config validation error: {str(e)}')

    def _validate_messaging_config(self, file_path: Path, errors: List[str],
        warnings: List[str]) ->None:
        """Validate messaging configuration structure."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            if not isinstance(config, dict):
                errors.append('Messaging config must be a dictionary')
                return
            messaging_keys = ['systems', 'providers', 'delivery', 'queue']
            found_keys = [key for key in messaging_keys if key in config]
            if not found_keys:
                warnings.append(
                    'No standard messaging configuration keys found')
        except Exception as e:
            errors.append(f'Messaging config validation error: {str(e)}')

    def _validate_discord_config(self, file_path: Path, errors: List[str],
        warnings: List[str]) ->None:
        """Validate Discord configuration structure."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            if not isinstance(config, dict):
                errors.append('Discord config must be a dictionary')
                return
            discord_keys = ['bot_token', 'guild_id', 'channels', 'permissions']
            found_keys = [key for key in discord_keys if key in config]
            if not found_keys:
                warnings.append('No standard Discord configuration keys found')
        except Exception as e:
            errors.append(f'Discord config validation error: {str(e)}')

    def validate_against_schema(self, config_file: Path, schema_file: Path
        ) ->Dict[str, Any]:
        """Validate configuration file against JSON schema."""
        validation_result = {'config_file': str(config_file), 'schema_file':
            str(schema_file), 'valid': False, 'errors': [], 'warnings': []}
        try:
            with open(schema_file, 'r') as f:
                schema = json.load(f)
            if config_file.suffix in ['.yaml', '.yml']:
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
            else:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            jsonschema.validate(config, schema)
            validation_result['valid'] = True
        except jsonschema.ValidationError as e:
            validation_result['errors'].append(
                f'Schema validation error: {str(e)}')
        except Exception as e:
            validation_result['errors'].append(f'Validation error: {str(e)}')
        return validation_result

    def generate_validation_report(self, output_file: str=
        'runtime/reports/config_validation_report.json') ->str:
        """Generate comprehensive validation report."""
        validation_summary = self.validate_all_configs()
        validation_summary['detailed_results'] = []
        for result in self.validation_results:
            validation_summary['detailed_results'].append({'file': result.
                file_path, 'valid': result.is_valid, 'errors': result.
                errors, 'warnings': result.warnings, 'validation_time':
                result.validation_time})
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(validation_summary, f, indent=2)
        logger.info(f'✅ Validation report generated: {output_file}')
        return str(output_path)


def main():
    """Main function for command-line usage."""
    import argparse
    parser = argparse.ArgumentParser(description=
        'Configuration Validation Pipeline')
    parser.add_argument('--config-dir', default='config', help=
        'Configuration directory')
    parser.add_argument('--schema-dir', default='schemas', help=
        'Schema directory')
    parser.add_argument('--output', default=
        'runtime/reports/config_validation_report.json', help=
        'Output report file')
    parser.add_argument('--validate-file', help='Validate specific file')
    parser.add_argument('--schema', help='Schema file for validation')
    args = parser.parse_args()
    validator = ConfigurationValidator(args.config_dir, args.schema_dir)
    if args.validate_file and args.schema:
        config_file = Path(args.validate_file)
        schema_file = Path(args.schema)
        result = validator.validate_against_schema(config_file, schema_file)
        logger.info(json.dumps(result, indent=2))
    else:
        report_file = validator.generate_validation_report(args.output)
        logger.info(f'Validation complete. Report saved to: {report_file}')


if __name__ == '__main__':
    main()
