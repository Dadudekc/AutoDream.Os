"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ImportPathProvider = void 0;
const metadataReader_1 = require("./metadataReader");
/**
 * Provides import path suggestions from repository integration metadata
 */
class ImportPathProvider {
    /**
     * Creates an ImportPathProvider instance
     * @param workspaceRoot - The workspace root path (unused, kept for API compatibility)
     */
    constructor(workspaceRoot) {
        this.suggestions = [];
        this.metadataReader = new metadataReader_1.MetadataReader();
    }
    /**
     * Loads import suggestions from metadata
     * @returns Promise resolving to true if successful
     */
    async loadSuggestions() {
        try {
            const metadata = await this.metadataReader.readMetadata();
            if (!metadata) {
                console.warn('No metadata available for import suggestions');
                return false;
            }
            this.suggestions = this.parseImportSuggestions(metadata);
            return true;
        }
        catch (error) {
            console.error('Failed to load import suggestions:', error);
            return false;
        }
    }
    /**
     * Parses metadata into import suggestions
     * @param metadata - The repository integration metadata
     * @returns Array of import suggestions
     */
    parseImportSuggestions(metadata) {
        const suggestions = [];
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
    getAllSuggestions() {
        return [...this.suggestions];
    }
    /**
     * Searches import suggestions by module name
     * @param query - Search query (module name fragment)
     * @returns Array of matching suggestions
     */
    searchByModuleName(query) {
        const lowerQuery = query.toLowerCase();
        return this.suggestions.filter(suggestion => suggestion.moduleName.toLowerCase().includes(lowerQuery));
    }
    /**
     * Searches import suggestions by integration
     * @param integrationId - Integration ID to filter by
     * @returns Array of suggestions for the integration
     */
    getByIntegration(integrationId) {
        return this.suggestions.filter(suggestion => suggestion.integrationId === integrationId);
    }
    /**
     * Gets import path for a specific module
     * @param moduleName - The module name to find
     * @returns Import path or undefined if not found
     */
    getImportPathForModule(moduleName) {
        const suggestion = this.suggestions.find(s => s.moduleName.toLowerCase() === moduleName.toLowerCase());
        return suggestion?.importPath;
    }
    /**
     * Gets suggestion for a specific module
     * @param moduleName - The module name to find
     * @returns Import suggestion or undefined if not found
     */
    getSuggestionForModule(moduleName) {
        return this.suggestions.find(s => s.moduleName.toLowerCase() === moduleName.toLowerCase());
    }
    /**
     * Checks if a module exists in suggestions
     * @param moduleName - The module name to check
     * @returns True if module exists
     */
    hasModule(moduleName) {
        return this.suggestions.some(s => s.moduleName.toLowerCase() === moduleName.toLowerCase());
    }
    /**
     * Gets count of available import suggestions
     * @returns Number of suggestions
     */
    getCount() {
        return this.suggestions.length;
    }
    /**
     * Refreshes suggestions from metadata
     * @returns Promise resolving to true if successful
     */
    async refresh() {
        return this.loadSuggestions();
    }
}
exports.ImportPathProvider = ImportPathProvider;
//# sourceMappingURL=importPathProvider.js.map