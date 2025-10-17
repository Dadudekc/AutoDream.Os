/**
 * Repository Navigator Configuration
 * ====================================
 * 
 * User-configurable options for the Repository Navigator extension.
 * 
 * Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
 * Date: 2025-10-16
 * Task: VSCode Extension Enhancement (Task #2 from queue)
 */

import * as vscode from 'vscode';

/**
 * Configuration keys for the extension
 */
export enum ConfigKey {
    AutoRefresh = 'repositoryNavigator.autoRefresh',
    RefreshInterval = 'repositoryNavigator.refreshInterval',
    ShowHealthStatus = 'repositoryNavigator.showHealthStatus',
    ExpandByDefault = 'repositoryNavigator.expandByDefault',
    EnableImportHelper = 'repositoryNavigator.enableImportHelper',
    MetadataPath = 'repositoryNavigator.metadataPath',
}

/**
 * Default configuration values
 */
export const DEFAULT_CONFIG = {
    autoRefresh: true,
    refreshInterval: 30000, // 30 seconds
    showHealthStatus: true,
    expandByDefault: false,
    enableImportHelper: true,
    metadataPath: '.vscode/repo-integrations.json',
};

/**
 * Configuration manager for Repository Navigator
 */
export class RepositoryNavigatorConfig {
    private config: vscode.WorkspaceConfiguration;

    constructor() {
        this.config = vscode.workspace.getConfiguration();
    }

    /**
     * Get configuration value
     */
    get<T>(key: ConfigKey, defaultValue?: T): T {
        return this.config.get(key, defaultValue as T) as T;
    }

    /**
     * Update configuration value
     */
    async update(key: ConfigKey, value: any, target: vscode.ConfigurationTarget = vscode.ConfigurationTarget.Workspace): Promise<void> {
        await this.config.update(key, value, target);
    }

    /**
     * Get auto-refresh setting
     */
    getAutoRefresh(): boolean {
        return this.get(ConfigKey.AutoRefresh, DEFAULT_CONFIG.autoRefresh);
    }

    /**
     * Get refresh interval (milliseconds)
     */
    getRefreshInterval(): number {
        return this.get(ConfigKey.RefreshInterval, DEFAULT_CONFIG.refreshInterval);
    }

    /**
     * Get show health status setting
     */
    getShowHealthStatus(): boolean {
        return this.get(ConfigKey.ShowHealthStatus, DEFAULT_CONFIG.showHealthStatus);
    }

    /**
     * Get expand by default setting
     */
    getExpandByDefault(): boolean {
        return this.get(ConfigKey.ExpandByDefault, DEFAULT_CONFIG.expandByDefault);
    }

    /**
     * Get enable import helper setting
     */
    getEnableImportHelper(): boolean {
        return this.get(ConfigKey.EnableImportHelper, DEFAULT_CONFIG.enableImportHelper);
    }

    /**
     * Get metadata file path
     */
    getMetadataPath(): string {
        return this.get(ConfigKey.MetadataPath, DEFAULT_CONFIG.metadataPath);
    }

    /**
     * Reset all settings to defaults
     */
    async resetToDefaults(): Promise<void> {
        for (const [key, value] of Object.entries(DEFAULT_CONFIG)) {
            const configKey = `repositoryNavigator.${key}` as ConfigKey;
            await this.update(configKey, value);
        }
    }
}

/**
 * Get configuration instance
 */
export function getConfig(): RepositoryNavigatorConfig {
    return new RepositoryNavigatorConfig();
}

