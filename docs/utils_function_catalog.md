# Utils Function Catalog

Summary of top-level functions and classes within directories containing 'utils'.

## src\ai_automation\utils\__init__.py

## src\ai_automation\utils\filesystem.py
- Functions: make_executable

## src\core\utils\__init__.py

## src\core\utils\agent_matching.py
- Classes: AgentCapability, AgentMatchingUtils

## src\core\utils\coordination_utils.py
- Classes: CoordinationUtils

## src\core\utils\message_queue_utils.py
- Classes: MessageQueueUtils

## src\core\utils\simple_utils.py
- Functions: copy_file, create_directory, delete_file, format_string, get_file_size, get_timestamp, is_valid_path, list_files, read_file, write_file

## src\gaming\utils\__init__.py

## src\gaming\utils\gaming_alert_utils.py
- Functions: calculate_alert_priority, create_alert_id, format_alert_message, validate_alert_metadata

## src\gaming\utils\gaming_handlers.py
- Classes: GamingEventHandlers

## src\gaming\utils\gaming_monitors.py
- Classes: GamingPerformanceMonitors

## src\services\utils\__init__.py

## src\services\utils\agent_utils_registry.py
- Functions: list_agents

## src\services\utils\messaging_templates.py

## src\services\utils\onboarding_constants.py
- Functions: get_agent_assignments, get_phase_2_status, get_targets, is_phase_2_active

## src\services\utils\vector_config_utils.py
- Functions: load_simple_config

## src\services\utils\vector_integration_helpers.py
- Functions: format_search_result, generate_agent_recommendations, generate_recommendations

## src\utils\__init__.py

## src\utils\autonomous_config_orchestrator.py
- Functions: run_autonomous_config_system
- Classes: AutonomousConfigOrchestrator

## src\utils\backup.py
- Classes: BackupManager

## src\utils\config_auto_migrator.py
- Functions: auto_migrate_directory
- Classes: ConfigAutoMigrator, MigrationAction

## src\utils\config_consolidator.py
- Functions: run_configuration_consolidation
- Classes: ConfigPattern, ConfigurationConsolidator

## src\utils\config_core\__init__.py
- Functions: get_config

## src\utils\config_core\fsm_config.py
- Classes: FSMConfig

## src\utils\config_file_scanner.py
- Classes: FileScanner

## src\utils\config_models.py
- Classes: ConfigPattern

## src\utils\config_remediator.py
- Classes: ConfigRemediator, RemediationAction

## src\utils\config_scanners.py
- Classes: ConfigConstantScanner, ConfigurationScanner, EnvironmentVariableScanner, HardcodedValueScanner, SettingsPatternScanner

## src\utils\confirm.py
- Functions: confirm

## src\utils\file_operations\__init__.py

## src\utils\file_operations\backup_operations.py
- Functions: create_backup_manager
- Classes: BackupManager, BackupOperations

## src\utils\file_operations\directory_operations.py
- Classes: DirectoryOperations

## src\utils\file_operations\file_metadata.py
- Classes: FileMetadataOperations, FileOperation

## src\utils\file_operations\file_serialization.py
- Classes: DataSerializationOperations

## src\utils\file_operations\scanner_operations.py
- Classes: UnifiedFileScanner

## src\utils\file_operations\validation_operations.py
- Classes: FileValidationResult, FileValidator

## src\utils\file_scanner.py
- Classes: FileScanner

## src\utils\file_utils.py
- Classes: FileUtils

## src\utils\logger.py
- Functions: get_contract_logger, get_core_logger, get_logger, get_messaging_logger
- Classes: StructuredFormatter, V2Logger

## src\utils\scanner_registry.py
- Functions: auto_register
- Classes: ScannerRegistry

## src\utils\unified_config_utils.py
- Functions: run_configuration_consolidation
- Classes: ConfigConstantScanner, ConfigPattern, ConfigurationScanner, EnvironmentVariableScanner, FileScanner, HardcodedValueScanner, SettingsPatternScanner, UnifiedConfigurationConsolidator

## src\utils\unified_file_utils.py
- Functions: create_backup_manager
- Classes: BackupManager, BackupOperations, FileValidationResult, FileValidator, UnifiedFileScanner, UnifiedFileUtils

## src\utils\unified_utilities.py
- Functions: ensure_directory, get_config_path, get_logger, get_project_root, get_unified_utility
- Classes: UnifiedUtility
