/**
 * Unit tests for ImportCompletionProvider
 * Agent-6 - Phase 2 Day 2 Testing
 */

import * as vscode from 'vscode';
import { ImportCompletionProvider } from '../../../src/completionProvider';
import { ImportPathProvider } from '../../../src/importPathProvider';
import { ImportSuggestion } from '../../../src/types';

// Mock vscode
jest.mock('vscode');

describe('ImportCompletionProvider', () => {
    let provider: ImportCompletionProvider;
    let mockImportPathProvider: jest.Mocked<ImportPathProvider>;

    const mockSuggestions: ImportSuggestion[] = [
        {
            moduleName: 'test_module',
            importPath: 'from src.test import test_module',
            description: 'Test module',
            filePath: 'src/test/test_module.py',
            integrationName: 'Test Integration',
            integrationId: 'test',
            lines: 100,
            dependencies: ['logging']
        },
        {
            moduleName: 'optional_module',
            importPath: 'from src.test import optional_module',
            description: 'Optional module',
            filePath: 'src/test/optional_module.py',
            integrationName: 'Test Integration',
            integrationId: 'test',
            lines: 50,
            optional: true,
            dependencies: ['typing']
        }
    ];

    beforeEach(() => {
        mockImportPathProvider = {
            getAllSuggestions: jest.fn().mockReturnValue(mockSuggestions)
        } as any;

        provider = new ImportCompletionProvider(mockImportPathProvider);

        // Mock VSCode CompletionItem and MarkdownString
        (vscode.CompletionItem as any) = jest.fn().mockImplementation((label, kind) => ({
            label,
            kind,
            insertText: '',
            sortText: '',
            filterText: '',
            detail: '',
            documentation: {}
        }));

        (vscode.CompletionItemKind as any) = { Module: 9 };

        (vscode.MarkdownString as any) = jest.fn().mockImplementation(() => ({
            appendMarkdown: jest.fn(),
            appendCodeblock: jest.fn(),
            isTrusted: false
        }));
    });

    describe('provideCompletionItems', () => {
        const mockDocument = {
            lineAt: jest.fn()
        } as any;

        const mockPosition = { character: 10 } as any;
        const mockToken = {} as any;
        const mockContext = {} as any;

        it('should provide completion items for "from " context', () => {
            mockDocument.lineAt.mockReturnValue({ text: 'from ' });

            const items = provider.provideCompletionItems(
                mockDocument,
                mockPosition,
                mockToken,
                mockContext
            );

            expect(items).toHaveLength(2);
            expect(mockImportPathProvider.getAllSuggestions).toHaveBeenCalled();
        });

        it('should provide completion items for "import " context', () => {
            mockDocument.lineAt.mockReturnValue({ text: 'import ' });

            const items = provider.provideCompletionItems(
                mockDocument,
                mockPosition,
                mockToken,
                mockContext
            );

            expect(items).toHaveLength(2);
        });

        it('should return undefined for non-import context', () => {
            mockDocument.lineAt.mockReturnValue({ text: 'def function():' });

            const items = provider.provideCompletionItems(
                mockDocument,
                mockPosition,
                mockToken,
                mockContext
            );

            expect(items).toBeUndefined();
        });

        it('should create completion items with correct properties', () => {
            mockDocument.lineAt.mockReturnValue({ text: 'from ' });

            const items = provider.provideCompletionItems(
                mockDocument,
                mockPosition,
                mockToken,
                mockContext
            );

            expect(items![0].label).toBe('test_module');
            expect(items![0].insertText).toBe('from src.test import test_module');
        });

        it('should prioritize non-optional modules', () => {
            mockDocument.lineAt.mockReturnValue({ text: 'from ' });

            const items = provider.provideCompletionItems(
                mockDocument,
                mockPosition,
                mockToken,
                mockContext
            );

            // Non-optional module should have lower sortText (sorts first)
            expect(items![0].sortText).toBe('test_module');
            expect(items![1].sortText).toBe('z_optional_module');
        });
    });

    describe('resolveCompletionItem', () => {
        it('should return the same item', () => {
            const mockItem = { label: 'test' } as vscode.CompletionItem;
            const mockToken = {} as any;

            const result = provider.resolveCompletionItem(mockItem, mockToken);

            expect(result).toBe(mockItem);
        });
    });
});


