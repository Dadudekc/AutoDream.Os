/**
 * Metadata Reader - Reads .vscode/repo-integrations.json
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1
 * Based on: Agent-7's metadata format
 */

import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { RepoIntegrationMetadata } from './types';

export class MetadataReader {
    private metadataPath: string;
    private workspaceRoot: string;

    constructor() {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            throw new Error('No workspace folder found');
        }
        this.workspaceRoot = workspaceFolders[0].uri.fsPath;
        this.metadataPath = path.join(
            this.workspaceRoot,
            '.vscode',
            'repo-integrations.json'
        );
    }

    /**
     * Read and parse repo integration metadata
     */
    async readMetadata(): Promise<RepoIntegrationMetadata | null> {
        try {
            // Check if file exists
            if (!fs.existsSync(this.metadataPath)) {
                console.warn(
                    'Metadata file not found:', 
                    this.metadataPath
                );
                return null;
            }

            // Read file
            const content = fs.readFileSync(this.metadataPath, 'utf8');
            
            // Parse JSON
            const metadata: RepoIntegrationMetadata = JSON.parse(content);
            
            // Basic validation
            if (!metadata.integrations || !Array.isArray(metadata.integrations)) {
                console.error('Invalid metadata: integrations array missing');
                return null;
            }

            return metadata;
        } catch (error) {
            console.error('Error reading metadata:', error);
            return null;
        }
    }

    /**
     * Watch metadata file for changes
     */
    watchMetadata(callback: () => void): vscode.Disposable {
        const pattern = new vscode.RelativePattern(
            this.workspaceRoot,
            '.vscode/repo-integrations.json'
        );
        
        const watcher = vscode.workspace.createFileSystemWatcher(pattern);
        
        watcher.onDidChange(() => callback());
        watcher.onDidCreate(() => callback());
        watcher.onDidDelete(() => callback());
        
        return watcher;
    }

    /**
     * Get metadata file path
     */
    getMetadataPath(): string {
        return this.metadataPath;
    }

    /**
     * Check if metadata exists
     */
    metadataExists(): boolean {
        return fs.existsSync(this.metadataPath);
    }
}

