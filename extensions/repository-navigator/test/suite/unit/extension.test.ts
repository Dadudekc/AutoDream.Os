/**
 * Unit Tests - Extension Activation
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1 Day 2
 * Testing Strategy by: Agent-8 (Testing Specialist)
 * New: Extension activation tests
 */

import * as vscode from 'vscode';
import { activate, deactivate } from '../../../src/extension';

// Mock vscode module
jest.mock('vscode', () => ({
    window: {
        registerTreeDataProvider: jest.fn(),
        createTreeView: jest.fn(() => ({
            dispose: jest.fn()
        })),
        showInformationMessage: jest.fn(),
        showErrorMessage: jest.fn(),
        showWarningMessage: jest.fn(),
        showTextDocument: jest.fn()
    },
    commands: {
        registerCommand: jest.fn(() => ({
            dispose: jest.fn()
        }))
    },
    languages: {
        registerCompletionItemProvider: jest.fn(() => ({
            dispose: jest.fn()
        }))
    },
    workspace: {
        openTextDocument: jest.fn(),
        workspaceFolders: [{
            uri: { fsPath: '/mock/workspace' }
        }]
    },
    TreeItemCollapsibleState: {
        None: 0,
        Collapsed: 1,
        Expanded: 2
    },
    TreeItem: class TreeItem {
        constructor(public label: string, public collapsibleState: number) {}
    },
    EventEmitter: jest.fn(() => ({
        event: jest.fn(),
        fire: jest.fn()
    })),
    Uri: {
        file: jest.fn((path: string) => ({ fsPath: path }))
    },
    ViewColumn: {
        One: 1
    }
}), { virtual: true });

// Mock MetadataReader
jest.mock('../../../src/metadataReader');

// Mock TreeDataProvider
jest.mock('../../../src/treeDataProvider');

describe('Extension', () => {
    let mockContext: vscode.ExtensionContext;
    let mockMetadataReader: any;

    beforeEach(() => {
        jest.clearAllMocks();
        mockContext = {
            subscriptions: []
        } as any;
        
        // Mock MetadataReader to return true for metadataExists
        const { MetadataReader } = require('../../../src/metadataReader');
        mockMetadataReader = MetadataReader.prototype;
        mockMetadataReader.metadataExists = jest.fn().mockReturnValue(true);
    });

    describe('activate', () => {
        it('should create tree view', () => {
            activate(mockContext);
            
            expect(vscode.window.createTreeView).toHaveBeenCalledWith(
                'repositoryNavigator',
                expect.objectContaining({
                    treeDataProvider: expect.any(Object),
                    showCollapseAll: true
                })
            );
        });

        it('should register refresh command', () => {
            activate(mockContext);
            
            expect(vscode.commands.registerCommand).toHaveBeenCalledWith(
                'repoNav.refresh',
                expect.any(Function)
            );
        });

        it('should register openFile command', () => {
            activate(mockContext);
            
            expect(vscode.commands.registerCommand).toHaveBeenCalledWith(
                'repoNav.openFile',
                expect.any(Function)
            );
        });

        it('should add disposables to subscriptions', () => {
            activate(mockContext);
            
            expect(mockContext.subscriptions.length).toBeGreaterThan(0);
        });
    });

    describe('deactivate', () => {
        it('should complete without errors', () => {
            expect(() => deactivate()).not.toThrow();
        });
    });

    describe('openFile command', () => {
        it('should open text document', async () => {
            const mockOpenTextDocument = vscode.workspace.openTextDocument as jest.Mock;
            const mockShowTextDocument = vscode.window.showTextDocument as any;
            
            mockOpenTextDocument.mockResolvedValue({});
            
            activate(mockContext);
            
            // Get the openFile command handler
            const registerCommandCalls = (vscode.commands.registerCommand as jest.Mock).mock.calls;
            const openFileCall = registerCommandCalls.find(
                call => call[0] === 'repoNav.openFile'
            );
            
            expect(openFileCall).toBeDefined();
            
            const openFileHandler = openFileCall[1];
            await openFileHandler('/path/to/file.py');
            
            expect(mockOpenTextDocument).toHaveBeenCalled();
        });
    });
});

