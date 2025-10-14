"use strict";
/**
 * Repository Navigator Extension - Main Entry Point
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1
 * Metadata by: Agent-7 (Repository Cloning Specialist)
 * Testing Strategy by: Agent-8 (Testing Specialist)
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
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const treeDataProvider_1 = require("./treeDataProvider");
const metadataReader_1 = require("./metadataReader");
const importPathProvider_1 = require("./importPathProvider");
const completionProvider_1 = require("./completionProvider");
let treeDataProvider;
let importPathProvider;
/**
 * Extension activation
 */
function activate(context) {
    console.log('Repository Navigator extension activating...');
    // Initialize metadata reader
    const metadataReader = new metadataReader_1.MetadataReader();
    // Check if metadata exists
    if (!metadataReader.metadataExists()) {
        vscode.window.showWarningMessage('Repository Navigator: Metadata file (.vscode/repo-integrations.json) not found. ' +
            'Please ensure repository integrations are configured.');
    }
    // Create tree data provider
    treeDataProvider = new treeDataProvider_1.RepoTreeDataProvider();
    // Register tree view
    const treeView = vscode.window.createTreeView('repositoryNavigator', {
        treeDataProvider: treeDataProvider,
        showCollapseAll: true
    });
    // Initialize import path provider (Phase 2)
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0].uri.fsPath;
    if (workspaceRoot) {
        importPathProvider = new importPathProvider_1.ImportPathProvider(workspaceRoot);
        // Load import suggestions
        importPathProvider.loadSuggestions().then(success => {
            if (success) {
                console.log(`Import Path Helper: Loaded ${importPathProvider.getCount()} suggestions`);
            }
            else {
                console.warn('Import Path Helper: Failed to load suggestions');
            }
        });
        // Register completion provider for Python files
        const completionProvider = vscode.languages.registerCompletionItemProvider({ language: 'python', scheme: 'file' }, new completionProvider_1.ImportCompletionProvider(importPathProvider), ' ', // Trigger on space after "from" or "import"
        '.' // Trigger on dot for package paths
        );
        context.subscriptions.push(completionProvider);
    }
    // Watch metadata for changes and refresh tree + import suggestions
    const metadataWatcher = metadataReader.watchMetadata(() => {
        console.log('Metadata changed, refreshing tree and import suggestions...');
        treeDataProvider.refresh();
        if (importPathProvider) {
            importPathProvider.refresh();
        }
    });
    // Register commands
    const refreshCommand = vscode.commands.registerCommand('repoNav.refresh', () => {
        treeDataProvider.refresh();
        vscode.window.showInformationMessage('Repository Navigator refreshed');
    });
    const openFileCommand = vscode.commands.registerCommand('repoNav.openFile', async (filePath) => {
        await openRepoFile(filePath);
    });
    // Register import helper refresh command
    const refreshImportsCommand = vscode.commands.registerCommand('importHelper.refresh', async () => {
        if (importPathProvider) {
            const success = await importPathProvider.refresh();
            const count = importPathProvider.getCount();
            vscode.window.showInformationMessage(success
                ? `Import Path Helper refreshed: ${count} suggestions loaded`
                : 'Import Path Helper: Failed to refresh suggestions');
        }
    });
    // Add to subscriptions for cleanup
    context.subscriptions.push(treeView, metadataWatcher, refreshCommand, openFileCommand, refreshImportsCommand);
    console.log('Repository Navigator extension activated successfully!');
}
/**
 * Open repository file in editor
 */
async function openRepoFile(filePath) {
    try {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0].uri.fsPath;
        if (!workspaceRoot) {
            throw new Error('No workspace folder found');
        }
        // Construct full file path
        const fullPath = path.join(workspaceRoot, filePath);
        // Open document
        const uri = vscode.Uri.file(fullPath);
        const document = await vscode.workspace.openTextDocument(uri);
        // Show in editor
        await vscode.window.showTextDocument(document);
        console.log('Opened file:', fullPath);
    }
    catch (error) {
        vscode.window.showErrorMessage(`Failed to open file: ${error instanceof Error ? error.message : 'Unknown error'}`);
        console.error('Error opening file:', error);
    }
}
/**
 * Extension deactivation
 */
function deactivate() {
    console.log('Repository Navigator extension deactivated');
}
//# sourceMappingURL=extension.js.map