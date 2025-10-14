/**
 * Repository Tree Data Provider
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1
 * Based on: Agent-7's integration metadata
 */

import * as vscode from 'vscode';
import * as path from 'path';
import { MetadataReader } from './metadataReader';
import { Integration, Module } from './types';

export class RepoTreeDataProvider 
    implements vscode.TreeDataProvider<RepoTreeItem> {
    
    private _onDidChangeTreeData: vscode.EventEmitter<
        RepoTreeItem | undefined | null | void
    > = new vscode.EventEmitter<RepoTreeItem | undefined | null | void>();
    
    readonly onDidChangeTreeData: vscode.Event<
        RepoTreeItem | undefined | null | void
    > = this._onDidChangeTreeData.event;

    private metadataReader: MetadataReader;

    constructor() {
        this.metadataReader = new MetadataReader();
    }

    /**
     * Refresh tree view
     */
    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    /**
     * Get tree item representation
     */
    getTreeItem(element: RepoTreeItem): vscode.TreeItem {
        return element;
    }

    /**
     * Get children for tree view
     */
    async getChildren(element?: RepoTreeItem): Promise<RepoTreeItem[]> {
        if (!element) {
            // Root level: Show all integrated repositories
            return this.getIntegratedRepos();
        } else if (element.contextValue === 'repo') {
            // Repo level: Show modules
            return this.getRepoModules(element.repoId);
        } else {
            // Module level: No children
            return [];
        }
    }

    /**
     * Get all integrated repositories
     */
    private async getIntegratedRepos(): Promise<RepoTreeItem[]> {
        const metadata = await this.metadataReader.readMetadata();
        
        if (!metadata || !metadata.integrations) {
            return [
                new RepoTreeItem(
                    'No integrations found',
                    'info',
                    vscode.TreeItemCollapsibleState.None,
                    'info',
                    undefined,
                    undefined
                )
            ];
        }

        return metadata.integrations.map(integration =>
            this.createRepoTreeItem(integration)
        );
    }

    /**
     * Get modules for a specific repository
     */
    private async getRepoModules(repoId: string): Promise<RepoTreeItem[]> {
        const metadata = await this.metadataReader.readMetadata();
        
        if (!metadata) {
            return [];
        }

        const integration = metadata.integrations.find(
            i => i.id === repoId
        );
        
        if (!integration) {
            return [];
        }

        return integration.modules.map(module =>
            this.createModuleTreeItem(module, integration)
        );
    }

    /**
     * Create tree item for repository
     */
    private createRepoTreeItem(integration: Integration): RepoTreeItem {
        const statusIcon = this.getStatusIcon(integration.status);
        const label = `${statusIcon} ${integration.name}`;
        const description = `${integration.files_ported} files`;
        const tooltip = this.createRepoTooltip(integration);

        return new RepoTreeItem(
            label,
            integration.id,
            vscode.TreeItemCollapsibleState.Collapsed,
            'repo',
            description,
            tooltip,
            integration.target_path
        );
    }

    /**
     * Create tree item for module
     */
    private createModuleTreeItem(
        module: Module,
        integration: Integration
    ): RepoTreeItem {
        const icon = module.optional ? '📄' : '📄';
        const label = `${icon} ${module.file}`;
        const description = `${module.lines} lines`;
        const tooltip = this.createModuleTooltip(module);
        const filePath = path.join(
            integration.target_path,
            module.file
        );

        return new RepoTreeItem(
            label,
            module.name,
            vscode.TreeItemCollapsibleState.None,
            'module',
            description,
            tooltip,
            filePath
        );
    }

    /**
     * Get status icon
     */
    private getStatusIcon(status: string): string {
        switch (status) {
            case 'operational': return '✅';
            case 'warning': return '⚠️';
            case 'error': return '❌';
            default: return '❓';
        }
    }

    /**
     * Create repository tooltip
     */
    private createRepoTooltip(integration: Integration): string {
        return [
            `${integration.name}`,
            ``,
            `Status: ${integration.status}`,
            `Files Ported: ${integration.files_ported}/${integration.total_source_files}`,
            `Coverage: ${integration.percentage_ported.toFixed(1)}%`,
            `V2 Compliant: ${integration.v2_compliant ? '✅' : '❌'}`,
            `Imports Working: ${integration.imports_working ? '✅' : '❌'}`,
            ``,
            `Path: ${integration.target_path}`,
            `Integration Date: ${integration.integration_date}`
        ].join('\n');
    }

    /**
     * Create module tooltip
     */
    private createModuleTooltip(module: Module): string {
        return [
            `${module.name}`,
            ``,
            `Purpose: ${module.purpose}`,
            `Lines: ${module.lines}`,
            `Dependencies: ${module.dependencies.join(', ')}`,
            module.optional ? 'Optional: Yes' : '',
            ``,
            `Import: ${module.import_path}`
        ].filter(line => line.length > 0).join('\n');
    }
}

/**
 * Tree Item for Repository Navigator
 */
export class RepoTreeItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly repoId: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly contextValue: string,
        public readonly description?: string,
        public readonly tooltip?: string,
        public readonly filePath?: string
    ) {
        super(label, collapsibleState);
        
        this.description = description;
        this.tooltip = tooltip;

        // Set command to open file when clicked (for modules)
        if (contextValue === 'module' && filePath) {
            this.command = {
                command: 'repoNav.openFile',
                title: 'Open File',
                arguments: [filePath]
            };
        }
    }
}

