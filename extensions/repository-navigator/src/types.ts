/**
 * Repository Navigator Extension - Type Definitions
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1
 */

export interface RepoIntegrationMetadata {
    version: string;
    last_updated: string;
    agent: string;
    integrations: Integration[];
    statistics: Statistics;
    conservative_scoping_methodology: ScopingMethodology;
    vscode_extension_support: ExtensionSupport;
}

export interface Integration {
    id: string;
    name: string;
    source_repo: string;
    target_path: string;
    status: 'operational' | 'warning' | 'error';
    files_ported: number;
    total_source_files: number;
    percentage_ported: number;
    integration_date: string;
    v2_compliant: boolean;
    imports_working: boolean;
    modules: Module[];
    backward_compat: string | null;
    health_check: HealthCheck;
}

export interface Module {
    name: string;
    file: string;
    lines: number;
    purpose: string;
    dependencies: string[];
    optional?: boolean;
    import_path: string;
}

export interface HealthCheck {
    last_test: string;
    imports_passing: boolean;
    errors: string[];
}

export interface Statistics {
    total_integrations: number;
    total_files_ported: number;
    average_port_percentage: number;
    operational_integrations: number;
    v2_compliance_rate: number;
    import_success_rate: number;
}

export interface ScopingMethodology {
    principle: string;
    benefits: string[];
    process: string[];
}

export interface ExtensionSupport {
    repository_navigator: { enabled: boolean; tree_view_data: string };
    import_path_helper: { enabled: boolean; suggestions_from: string };
    status_dashboard: { enabled: boolean; health_data: string };
    scoping_wizard: { enabled: boolean; methodology: string };
}

/**
 * Import suggestion for IntelliSense
 * Phase 2: Import Path Helper
 */
export interface ImportSuggestion {
    /** Module name (e.g., 'memory_system') */
    moduleName: string;
    /** Full import statement (e.g., 'from src.integrations.jarvis import memory_system') */
    importPath: string;
    /** Module purpose/description */
    description: string;
    /** Module file path */
    filePath: string;
    /** Integration name (e.g., 'Jarvis AI Assistant') */
    integrationName: string;
    /** Integration ID (e.g., 'jarvis') */
    integrationId: string;
    /** Module lines of code */
    lines: number;
    /** Is this module optional? */
    optional?: boolean;
    /** Module dependencies */
    dependencies?: string[];
}

