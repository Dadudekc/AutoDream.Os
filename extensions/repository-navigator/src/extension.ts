/**
 * Repository Navigator Extension - Main Entry Point
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1
 * Metadata by: Agent-7 (Repository Cloning Specialist)
 * Testing Strategy by: Agent-8 (Testing Specialist)
 */

import * as vscode from 'vscode';
import * as path from 'path';
import { RepoTreeDataProvider } from './treeDataProvider';
import { MetadataReader } from './metadataReader';
import { ImportPathProvider } from './importPathProvider';
import { ImportCompletionProvider } from './completionProvider';

let treeDataProvider: RepoTreeDataProvider;
let importPathProvider: ImportPathProvider;

/**
 * Extension activation
 */
export function activate(context: vscode.ExtensionContext) {
    console.log('Repository Navigator extension activating...');

    // Initialize metadata reader
    const metadataReader = new MetadataReader();

    // Check if metadata exists
    if (!metadataReader.metadataExists()) {
        vscode.window.showWarningMessage(
            'Repository Navigator: Metadata file (.vscode/repo-integrations.json) not found. ' +
            'Please ensure repository integrations are configured.'
        );
    }

    // Create tree data provider
    treeDataProvider = new RepoTreeDataProvider();

    // Register tree view
    const treeView = vscode.window.createTreeView('repositoryNavigator', {
        treeDataProvider: treeDataProvider,
        showCollapseAll: true
    });

    // Initialize import path provider (Phase 2)
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0].uri.fsPath;
    if (workspaceRoot) {
        importPathProvider = new ImportPathProvider(workspaceRoot);
        
        // Load import suggestions
        importPathProvider.loadSuggestions().then(success => {
            if (success) {
                console.log(`Import Path Helper: Loaded ${importPathProvider.getCount()} suggestions`);
            } else {
                console.warn('Import Path Helper: Failed to load suggestions');
            }
        });

        // Register completion provider for Python files
        const completionProvider = vscode.languages.registerCompletionItemProvider(
            { language: 'python', scheme: 'file' },
            new ImportCompletionProvider(importPathProvider),
            ' ', // Trigger on space after "from" or "import"
            '.'  // Trigger on dot for package paths
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
    const refreshCommand = vscode.commands.registerCommand(
        'repoNav.refresh',
        () => {
            treeDataProvider.refresh();
            vscode.window.showInformationMessage(
                'Repository Navigator refreshed'
            );
        }
    );

    const openFileCommand = vscode.commands.registerCommand(
        'repoNav.openFile',
        async (filePath: string) => {
            await openRepoFile(filePath);
        }
    );

    // Register import helper refresh command
    const refreshImportsCommand = vscode.commands.registerCommand(
        'importHelper.refresh',
        async () => {
            if (importPathProvider) {
                const success = await importPathProvider.refresh();
                const count = importPathProvider.getCount();
                vscode.window.showInformationMessage(
                    success 
                        ? `Import Path Helper refreshed: ${count} suggestions loaded`
                        : 'Import Path Helper: Failed to refresh suggestions'
                );
            }
        }
    );

    // Add to subscriptions for cleanup
    context.subscriptions.push(
        treeView,
        metadataWatcher,
        refreshCommand,
        openFileCommand,
        refreshImportsCommand
    );

    console.log('Repository Navigator extension activated successfully!');
}

/**
 * Open repository file in editor
 */
async function openRepoFile(filePath: string): Promise<void> {
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
    } catch (error) {
        vscode.window.showErrorMessage(
            `Failed to open file: ${error instanceof Error ? error.message : 'Unknown error'}`
        );
        console.error('Error opening file:', error);
    }
}

/**
 * Extension deactivation
 */
export function deactivate() {
    console.log('Repository Navigator extension deactivated');
}

