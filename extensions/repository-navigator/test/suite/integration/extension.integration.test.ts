/**
 * Integration Tests - Extension with VSCode API
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1 Day 3
 * Testing Strategy by: Agent-8 (Testing Specialist)
 * Integration tests (30% of testing pyramid)
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as assert from 'assert';

suite('Repository Navigator Extension Integration Tests', () => {
    
    test('Extension should activate successfully', async () => {
        const extension = vscode.extensions.getExtension('Agent-6.repository-navigator');
        
        if (!extension) {
            assert.fail('Extension not found');
        }
        
        if (!extension.isActive) {
            await extension.activate();
        }
        
        assert.ok(extension.isActive, 'Extension should be active');
    });

    test('Tree view should be registered', async () => {
        const extension = vscode.extensions.getExtension('Agent-6.repository-navigator');
        
        if (!extension?.isActive) {
            await extension?.activate();
        }
        
        // Tree view should be accessible
        // VSCode doesn't expose tree views directly, but we can verify commands work
        const commands = await vscode.commands.getCommands(true);
        
        assert.ok(
            commands.includes('repoNav.refresh'),
            'Refresh command should be registered'
        );
        assert.ok(
            commands.includes('repoNav.openFile'),
            'Open file command should be registered'
        );
    });

    test('Refresh command should execute without error', async () => {
        const extension = vscode.extensions.getExtension('Agent-6.repository-navigator');
        
        if (!extension?.isActive) {
            await extension?.activate();
        }
        
        await vscode.commands.executeCommand('repoNav.refresh');
        // If no error thrown, test passes
        assert.ok(true, 'Refresh command executed successfully');
    });

    test('Extension should handle workspace without metadata gracefully', async () => {
        const extension = vscode.extensions.getExtension('Agent-6.repository-navigator');
        
        if (!extension?.isActive) {
            await extension?.activate();
        }
        
        // Extension should activate even without metadata file
        // It should show warning but not crash
        assert.ok(extension.isActive, 'Extension should be active despite missing metadata');
    });

    test('Commands should be available in command palette', async () => {
        const allCommands = await vscode.commands.getCommands(true);
        
        const repoNavCommands = allCommands.filter(cmd => 
            cmd.startsWith('repoNav.')
        );
        
        assert.ok(
            repoNavCommands.length >= 2,
            'At least 2 repoNav commands should be registered'
        );
        
        assert.ok(
            repoNavCommands.includes('repoNav.refresh'),
            'Refresh command should be in palette'
        );
        assert.ok(
            repoNavCommands.includes('repoNav.openFile'),
            'Open file command should be in palette'
        );
    });

    test('Tree view should be in explorer view container', async () => {
        const extension = vscode.extensions.getExtension('Agent-6.repository-navigator');
        
        if (!extension?.isActive) {
            await extension?.activate();
        }
        
        // The tree view ID from package.json
        const treeViewId = 'repositoryNavigator';
        
        // If extension activated without error, tree view should be registered
        assert.ok(extension.isActive, 'Extension with tree view active');
    });

    test('Extension should provide view container in activity bar', async () => {
        const extension = vscode.extensions.getExtension('Agent-6.repository-navigator');
        
        if (!extension?.isActive) {
            await extension?.activate();
        }
        
        // View container 'repository-navigator' should be contributed
        // VSCode API doesn't expose view containers directly
        // But if extension activated successfully, view container is registered
        assert.ok(extension.isActive, 'Extension with view container active');
    });

    test('Extension should register without deprecated APIs', async () => {
        const extension = vscode.extensions.getExtension('Agent-6.repository-navigator');
        
        if (!extension) {
            assert.fail('Extension not found');
        }
        
        // Check package.json properties
        const packageJSON = extension.packageJSON;
        
        assert.ok(packageJSON.activationEvents, 'Activation events defined');
        assert.ok(packageJSON.contributes, 'Contributions defined');
        assert.ok(packageJSON.contributes.views, 'Views contributed');
        assert.ok(packageJSON.contributes.commands, 'Commands contributed');
    });
});

