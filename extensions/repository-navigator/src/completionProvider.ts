import * as vscode from 'vscode';
import { ImportPathProvider } from './importPathProvider';
import { ImportSuggestion } from './types';

/**
 * Provides IntelliSense completion items for import paths
 */
export class ImportCompletionProvider implements vscode.CompletionItemProvider {
    private importPathProvider: ImportPathProvider;

    /**
     * Creates an ImportCompletionProvider instance
     * @param importPathProvider - The import path provider
     */
    constructor(importPathProvider: ImportPathProvider) {
        this.importPathProvider = importPathProvider;
    }

    /**
     * Provides completion items for import statements
     * @param document - The current document
     * @param position - The cursor position
     * @param token - Cancellation token
     * @param context - Completion context
     * @returns Array of completion items or undefined
     */
    provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken,
        context: vscode.CompletionContext
    ): vscode.CompletionItem[] | undefined {
        const linePrefix = document.lineAt(position).text.substring(0, position.character);

        // Check if we're in an import context
        if (!this.isImportContext(linePrefix)) {
            return undefined;
        }

        // Get all suggestions and convert to completion items
        const suggestions = this.importPathProvider.getAllSuggestions();
        return suggestions.map(suggestion => this.createCompletionItem(suggestion));
    }

    /**
     * Checks if the current line context is an import statement
     * @param linePrefix - The line text before cursor
     * @returns True if in import context
     */
    private isImportContext(linePrefix: string): boolean {
        // Match "from " or "import " patterns
        return /\b(from|import)\s+/.test(linePrefix);
    }

    /**
     * Creates a completion item from an import suggestion
     * @param suggestion - The import suggestion
     * @returns VSCode completion item
     */
    private createCompletionItem(suggestion: ImportSuggestion): vscode.CompletionItem {
        const item = new vscode.CompletionItem(
            suggestion.moduleName,
            vscode.CompletionItemKind.Module
        );

        // Set the text to insert (full import path)
        item.insertText = suggestion.importPath;

        // Set sort text to prioritize non-optional modules
        item.sortText = suggestion.optional ? `z_${suggestion.moduleName}` : suggestion.moduleName;

        // Set filter text for search
        item.filterText = `${suggestion.moduleName} ${suggestion.integrationName}`;

        // Set basic detail
        item.detail = `${suggestion.integrationName} - ${suggestion.lines} lines`;

        // Set documentation
        item.documentation = this.createDocumentation(suggestion);

        return item;
    }

    /**
     * Creates documentation for a completion item
     * @param suggestion - The import suggestion
     * @returns Markdown documentation
     */
    private createDocumentation(suggestion: ImportSuggestion): vscode.MarkdownString {
        const markdown = new vscode.MarkdownString();

        // Add description
        markdown.appendMarkdown(`**${suggestion.moduleName}**\n\n`);
        markdown.appendMarkdown(`${suggestion.description}\n\n`);

        // Add integration info
        markdown.appendMarkdown(`**Integration:** ${suggestion.integrationName}\n\n`);

        // Add import path
        markdown.appendCodeblock(suggestion.importPath, 'python');

        // Add file location
        markdown.appendMarkdown(`\n**File:** \`${suggestion.filePath}\`\n\n`);

        // Add module info
        markdown.appendMarkdown(`**Lines:** ${suggestion.lines}\n\n`);

        // Add optional flag
        if (suggestion.optional) {
            markdown.appendMarkdown(`⚠️ *Optional module*\n\n`);
        }

        // Add dependencies
        if (suggestion.dependencies && suggestion.dependencies.length > 0) {
            markdown.appendMarkdown(`**Dependencies:** ${suggestion.dependencies.join(', ')}\n\n`);
        }

        markdown.isTrusted = true;
        return markdown;
    }

    /**
     * Resolves additional information for a completion item
     * @param item - The completion item to resolve
     * @param token - Cancellation token
     * @returns Resolved completion item
     */
    resolveCompletionItem(
        item: vscode.CompletionItem,
        token: vscode.CancellationToken
    ): vscode.CompletionItem {
        // Additional resolution could be added here if needed
        return item;
    }
}


