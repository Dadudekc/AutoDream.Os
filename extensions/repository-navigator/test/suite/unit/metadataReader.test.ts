/**
 * Unit Tests - MetadataReader (Enhanced)
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1 Day 2
 * Testing Strategy by: Agent-8 (Testing Specialist)
 * Added: 8 unit tests + fs mocking for 85% coverage
 */

import { MetadataReader } from '../../../src/metadataReader';
import * as fs from 'fs';

// Mock vscode module
jest.mock('vscode', () => ({
    workspace: {
        workspaceFolders: [{
            uri: { fsPath: '/mock/workspace' }
        }],
        createFileSystemWatcher: jest.fn(() => ({
            onDidChange: jest.fn(),
            onDidCreate: jest.fn(),
            onDidDelete: jest.fn()
        }))
    },
    RelativePattern: jest.fn()
}), { virtual: true });

// Mock fs module (Agent-8's requirement)
jest.mock('fs', () => ({
    existsSync: jest.fn(),
    readFileSync: jest.fn()
}));

describe('MetadataReader', () => {
    let reader: MetadataReader;
    const mockFs = fs as jest.Mocked<typeof fs>;

    beforeEach(() => {
        jest.clearAllMocks();
        reader = new MetadataReader();
    });

    describe('constructor', () => {
        it('should initialize with workspace path', () => {
            expect(reader).toBeDefined();
            expect(reader.getMetadataPath()).toContain('.vscode');
            expect(reader.getMetadataPath()).toContain('repo-integrations.json');
        });

        it('should throw error if no workspace folder', () => {
            const mockVscode = require('vscode');
            mockVscode.workspace.workspaceFolders = null;

            expect(() => new MetadataReader()).toThrow('No workspace folder found');
            
            // Restore mock
            mockVscode.workspace.workspaceFolders = [{
                uri: { fsPath: '/mock/workspace' }
            }];
        });
    });

    describe('readMetadata', () => {
        it('should return null if file does not exist', async () => {
            mockFs.existsSync.mockReturnValue(false);
            
            const result = await reader.readMetadata();
            
            expect(result).toBeNull();
            expect(mockFs.existsSync).toHaveBeenCalledWith(
                expect.stringContaining('repo-integrations.json')
            );
        });

        it('should parse valid JSON metadata', async () => {
            const mockMetadata = {
                integrations: [
                    {
                        id: 'jarvis',
                        name: 'Jarvis AI',
                        status: 'operational',
                        modules: []
                    }
                ]
            };
            
            mockFs.existsSync.mockReturnValue(true);
            mockFs.readFileSync.mockReturnValue(JSON.stringify(mockMetadata));
            
            const result = await reader.readMetadata();
            
            expect(result).toEqual(mockMetadata);
            expect(mockFs.readFileSync).toHaveBeenCalledWith(
                expect.stringContaining('repo-integrations.json'),
                'utf8'
            );
        });

        it('should return null for invalid JSON', async () => {
            mockFs.existsSync.mockReturnValue(true);
            mockFs.readFileSync.mockReturnValue('invalid json{');
            
            const result = await reader.readMetadata();
            
            expect(result).toBeNull();
        });

        it('should return null if integrations array is missing', async () => {
            mockFs.existsSync.mockReturnValue(true);
            mockFs.readFileSync.mockReturnValue(JSON.stringify({ wrong: 'format' }));
            
            const result = await reader.readMetadata();
            
            expect(result).toBeNull();
        });

        it('should return null if integrations is not an array', async () => {
            mockFs.existsSync.mockReturnValue(true);
            mockFs.readFileSync.mockReturnValue(
                JSON.stringify({ integrations: 'not-an-array' })
            );
            
            const result = await reader.readMetadata();
            
            expect(result).toBeNull();
        });
    });

    describe('metadataExists', () => {
        it('should return true when file exists', () => {
            mockFs.existsSync.mockReturnValue(true);
            
            const exists = reader.metadataExists();
            
            expect(exists).toBe(true);
        });

        it('should return false when file does not exist', () => {
            mockFs.existsSync.mockReturnValue(false);
            
            const exists = reader.metadataExists();
            
            expect(exists).toBe(false);
        });
    });

    describe('getMetadataPath', () => {
        it('should return correct metadata path', () => {
            const metadataPath = reader.getMetadataPath();
            expect(metadataPath).toContain('.vscode');
            expect(metadataPath).toContain('repo-integrations.json');
            expect(metadataPath).toMatch(/[\/\\]mock[\/\\]workspace/);
        });
    });

    describe('watchMetadata', () => {
        it('should create file system watcher', () => {
            const mockCallback = jest.fn();
            const mockVscode = require('vscode');
            
            const watcher = reader.watchMetadata(mockCallback);
            
            expect(mockVscode.workspace.createFileSystemWatcher).toHaveBeenCalled();
            expect(watcher).toBeDefined();
        });
    });
});
