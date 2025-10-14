"use strict";
/**
 * Repository Tree Data Provider
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1
 * Based on: Agent-7's integration metadata
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.RepoTreeItem = exports.RepoTreeDataProvider = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const metadataReader_1 = require("./metadataReader");
class RepoTreeDataProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        this.metadataReader = new metadataReader_1.MetadataReader();
    }
    /**
     * Refresh tree view
     */
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    /**
     * Get tree item representation
     */
    getTreeItem(element) {
        return element;
    }
    /**
     * Get children for tree view
     */
    async getChildren(element) {
        if (!element) {
            // Root level: Show all integrated repositories
            return this.getIntegratedRepos();
        }
        else if (element.contextValue === 'repo') {
            // Repo level: Show modules
            return this.getRepoModules(element.repoId);
        }
        else {
            // Module level: No children
            return [];
        }
    }
    /**
     * Get all integrated repositories
     */
    async getIntegratedRepos() {
        const metadata = await this.metadataReader.readMetadata();
        if (!metadata || !metadata.integrations) {
            return [
                new RepoTreeItem('No integrations found', 'info', vscode.TreeItemCollapsibleState.None, 'info', undefined, undefined)
            ];
        }
        return metadata.integrations.map(integration => this.createRepoTreeItem(integration));
    }
    /**
     * Get modules for a specific repository
     */
    async getRepoModules(repoId) {
        const metadata = await this.metadataReader.readMetadata();
        if (!metadata) {
            return [];
        }
        const integration = metadata.integrations.find(i => i.id === repoId);
        if (!integration) {
            return [];
        }
        return integration.modules.map(module => this.createModuleTreeItem(module, integration));
    }
    /**
     * Create tree item for repository
     */
    createRepoTreeItem(integration) {
        const statusIcon = this.getStatusIcon(integration.status);
        const label = `${statusIcon} ${integration.name}`;
        const description = `${integration.files_ported} files`;
        const tooltip = this.createRepoTooltip(integration);
        return new RepoTreeItem(label, integration.id, vscode.TreeItemCollapsibleState.Collapsed, 'repo', description, tooltip, integration.target_path);
    }
    /**
     * Create tree item for module
     */
    createModuleTreeItem(module, integration) {
        const icon = module.optional ? '📄' : '📄';
        const label = `${icon} ${module.file}`;
        const description = `${module.lines} lines`;
        const tooltip = this.createModuleTooltip(module);
        const filePath = path.join(integration.target_path, module.file);
        return new RepoTreeItem(label, module.name, vscode.TreeItemCollapsibleState.None, 'module', description, tooltip, filePath);
    }
    /**
     * Get status icon
     */
    getStatusIcon(status) {
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
    createRepoTooltip(integration) {
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
    createModuleTooltip(module) {
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
exports.RepoTreeDataProvider = RepoTreeDataProvider;
/**
 * Tree Item for Repository Navigator
 */
class RepoTreeItem extends vscode.TreeItem {
    constructor(label, repoId, collapsibleState, contextValue, description, tooltip, filePath) {
        super(label, collapsibleState);
        this.label = label;
        this.repoId = repoId;
        this.collapsibleState = collapsibleState;
        this.contextValue = contextValue;
        this.description = description;
        this.tooltip = tooltip;
        this.filePath = filePath;
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
exports.RepoTreeItem = RepoTreeItem;
//# sourceMappingURL=treeDataProvider.js.map