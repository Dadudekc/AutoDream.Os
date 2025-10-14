"use strict";
/**
 * Metadata Reader - Reads .vscode/repo-integrations.json
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1
 * Based on: Agent-7's metadata format
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
exports.MetadataReader = void 0;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
class MetadataReader {
    constructor() {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            throw new Error('No workspace folder found');
        }
        this.workspaceRoot = workspaceFolders[0].uri.fsPath;
        this.metadataPath = path.join(this.workspaceRoot, '.vscode', 'repo-integrations.json');
    }
    /**
     * Read and parse repo integration metadata
     */
    async readMetadata() {
        try {
            // Check if file exists
            if (!fs.existsSync(this.metadataPath)) {
                console.warn('Metadata file not found:', this.metadataPath);
                return null;
            }
            // Read file
            const content = fs.readFileSync(this.metadataPath, 'utf8');
            // Parse JSON
            const metadata = JSON.parse(content);
            // Basic validation
            if (!metadata.integrations || !Array.isArray(metadata.integrations)) {
                console.error('Invalid metadata: integrations array missing');
                return null;
            }
            return metadata;
        }
        catch (error) {
            console.error('Error reading metadata:', error);
            return null;
        }
    }
    /**
     * Watch metadata file for changes
     */
    watchMetadata(callback) {
        const pattern = new vscode.RelativePattern(this.workspaceRoot, '.vscode/repo-integrations.json');
        const watcher = vscode.workspace.createFileSystemWatcher(pattern);
        watcher.onDidChange(() => callback());
        watcher.onDidCreate(() => callback());
        watcher.onDidDelete(() => callback());
        return watcher;
    }
    /**
     * Get metadata file path
     */
    getMetadataPath() {
        return this.metadataPath;
    }
    /**
     * Check if metadata exists
     */
    metadataExists() {
        return fs.existsSync(this.metadataPath);
    }
}
exports.MetadataReader = MetadataReader;
//# sourceMappingURL=metadataReader.js.map