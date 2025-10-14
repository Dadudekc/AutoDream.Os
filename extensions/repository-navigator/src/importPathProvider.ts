import * as vscode from 'vscode';
import { MetadataReader } from './metadataReader';
import { ImportSuggestion, RepoIntegrationMetadata } from './types';

/**
 * Provides import path suggestions from repository integration metadata
 */
export class ImportPathProvider {
    private metadataReader: MetadataReader;
    private suggestions: ImportSuggestion[] = [];

    /**
     * Creates an ImportPathProvider instance
     * @param workspaceRoot - The workspace root path (unused, kept for API compatibility)
     */
    constructor(workspaceRoot: string) {
        this.metadataReader = new MetadataReader();
    }

    /**
     * Loads import suggestions from metadata
     * @returns Promise resolving to true if successful
     */
    async loadSuggestions(): Promise<boolean> {
        try {
            const metadata = await this.metadataReader.readMetadata();
            if (!metadata) {
                console.warn('No metadata available for import suggestions');
                return false;
            }
            this.suggestions = this.parseImportSuggestions(metadata);
            return true;
        } catch (error) {
            console.error('Failed to load import suggestions:', error);
            return false;
        }
    }

    /**
     * Parses metadata into import suggestions
     * @param metadata - The repository integration metadata
     * @returns Array of import suggestions
     */
    private parseImportSuggestions(metadata: RepoIntegrationMetadata): ImportSuggestion[] {
        const suggestions: ImportSuggestion[] = [];

        for (const integration of metadata.integrations) {
            for (const module of integration.modules) {
                suggestions.push({
                    moduleName: module.name,
                    importPath: module.import_path,
                    description: module.purpose,
                    filePath: `${integration.target_path}${module.file}`,
                    integrationName: integration.name,
                    integrationId: integration.id,
                    lines: module.lines,
                    optional: module.optional,
                    dependencies: module.dependencies
                });
            }
        }

        return suggestions;
    }

    /**
     * Gets all import suggestions
     * @returns Array of all import suggestions
     */
    getAllSuggestions(): ImportSuggestion[] {
        return [...this.suggestions];
    }

    /**
     * Searches import suggestions by module name
     * @param query - Search query (module name fragment)
     * @returns Array of matching suggestions
     */
    searchByModuleName(query: string): ImportSuggestion[] {
        const lowerQuery = query.toLowerCase();
        return this.suggestions.filter(suggestion =>
            suggestion.moduleName.toLowerCase().includes(lowerQuery)
        );
    }

    /**
     * Searches import suggestions by integration
     * @param integrationId - Integration ID to filter by
     * @returns Array of suggestions for the integration
     */
    getByIntegration(integrationId: string): ImportSuggestion[] {
        return this.suggestions.filter(suggestion =>
            suggestion.integrationId === integrationId
        );
    }

    /**
     * Gets import path for a specific module
     * @param moduleName - The module name to find
     * @returns Import path or undefined if not found
     */
    getImportPathForModule(moduleName: string): string | undefined {
        const suggestion = this.suggestions.find(s =>
            s.moduleName.toLowerCase() === moduleName.toLowerCase()
        );
        return suggestion?.importPath;
    }

    /**
     * Gets suggestion for a specific module
     * @param moduleName - The module name to find
     * @returns Import suggestion or undefined if not found
     */
    getSuggestionForModule(moduleName: string): ImportSuggestion | undefined {
        return this.suggestions.find(s =>
            s.moduleName.toLowerCase() === moduleName.toLowerCase()
        );
    }

    /**
     * Checks if a module exists in suggestions
     * @param moduleName - The module name to check
     * @returns True if module exists
     */
    hasModule(moduleName: string): boolean {
        return this.suggestions.some(s =>
            s.moduleName.toLowerCase() === moduleName.toLowerCase()
        );
    }

    /**
     * Gets count of available import suggestions
     * @returns Number of suggestions
     */
    getCount(): number {
        return this.suggestions.length;
    }

    /**
     * Refreshes suggestions from metadata
     * @returns Promise resolving to true if successful
     */
    async refresh(): Promise<boolean> {
        return this.loadSuggestions();
    }
}

