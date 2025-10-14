"use strict";
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
exports.ImportCompletionProvider = void 0;
const vscode = __importStar(require("vscode"));
/**
 * Provides IntelliSense completion items for import paths
 */
class ImportCompletionProvider {
    /**
     * Creates an ImportCompletionProvider instance
     * @param importPathProvider - The import path provider
     */
    constructor(importPathProvider) {
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
    provideCompletionItems(document, position, token, context) {
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
    isImportContext(linePrefix) {
        // Match "from " or "import " patterns
        return /\b(from|import)\s+/.test(linePrefix);
    }
    /**
     * Creates a completion item from an import suggestion
     * @param suggestion - The import suggestion
     * @returns VSCode completion item
     */
    createCompletionItem(suggestion) {
        const item = new vscode.CompletionItem(suggestion.moduleName, vscode.CompletionItemKind.Module);
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
    createDocumentation(suggestion) {
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
    resolveCompletionItem(item, token) {
        // Additional resolution could be added here if needed
        return item;
    }
}
exports.ImportCompletionProvider = ImportCompletionProvider;
//# sourceMappingURL=completionProvider.js.map