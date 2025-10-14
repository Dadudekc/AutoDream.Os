/**
 * Jest Setup File
 * Mocks VSCode API globally for all tests
 */

// Mock vscode module globally
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
    CompletionItemKind: {
        Module: 9
    },
    CompletionItem: jest.fn().mockImplementation((label, kind) => ({
        label,
        kind,
        insertText: '',
        sortText: '',
        filterText: '',
        detail: '',
        documentation: {}
    })),
    MarkdownString: jest.fn().mockImplementation(() => ({
        appendMarkdown: jest.fn(),
        appendCodeblock: jest.fn(),
        isTrusted: false
    })),
    Uri: {
        file: jest.fn((path) => ({ fsPath: path }))
    }
}), { virtual: true });


