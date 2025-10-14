/**
 * Unit Tests - TreeDataProvider
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1 Day 2
 * Testing Strategy by: Agent-8 (Testing Specialist)
 * New: TreeDataProvider tests for 85% coverage
 */

import { RepoTreeDataProvider, RepoTreeItem } from '../../../src/treeDataProvider';
import { MetadataReader } from '../../../src/metadataReader';
import * as vscode from 'vscode';

// Mock vscode module
jest.mock('vscode', () => ({
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
    workspace: {
        workspaceFolders: [{
            uri: { fsPath: '/mock/workspace' }
        }]
    }
}), { virtual: true });

// Mock MetadataReader
jest.mock('../../../src/metadataReader');

describe('RepoTreeDataProvider', () => {
    let provider: RepoTreeDataProvider;
    let mockMetadataReader: jest.Mocked<MetadataReader>;

    beforeEach(() => {
        jest.clearAllMocks();
        mockMetadataReader = new MetadataReader() as jest.Mocked<MetadataReader>;
        provider = new RepoTreeDataProvider();
        (provider as any).metadataReader = mockMetadataReader;
    });

    describe('getTreeItem', () => {
        it('should return the same tree item', () => {
            const item = new RepoTreeItem(
                'Test',
                'test-id',
                vscode.TreeItemCollapsibleState.None,
                'repo'
            );
            
            const result = provider.getTreeItem(item);
            
            expect(result).toBe(item);
        });
    });

    describe('getChildren - root level', () => {
        it('should return integrated repositories', async () => {
            const mockMetadata = {
                version: '1.0.0',
                last_updated: '2025-10-13',
                agent: 'Agent-7',
                integrations: [
                    {
                        id: 'jarvis',
                        name: 'Jarvis AI',
                        source_repo: 'jarvis_repo',
                        status: 'operational' as const,
                        files_ported: 15,
                        total_source_files: 20,
                        percentage_ported: 75,
                        v2_compliant: true,
                        imports_working: true,
                        target_path: '/path/to/jarvis',
                        integration_date: '2025-10-01',
                        modules: [],
                        backward_compat: null,
                        health_check: {
                            last_test: '2025-10-13',
                            imports_passing: true,
                            errors: []
                        }
                    }
                ],
                statistics: {
                    total_integrations: 1,
                    total_files_ported: 15,
                    average_port_percentage: 75,
                    operational_integrations: 1,
                    v2_compliance_rate: 100,
                    import_success_rate: 100
                },
                conservative_scoping_methodology: {
                    principle: 'Test',
                    benefits: [],
                    process: []
                },
                vscode_extension_support: {
                    repository_navigator: { enabled: true, tree_view_data: 'test' },
                    import_path_helper: { enabled: true, suggestions_from: 'test' },
                    status_dashboard: { enabled: true, health_data: 'test' },
                    scoping_wizard: { enabled: true, methodology: 'test' }
                }
            };
            
            mockMetadataReader.readMetadata.mockResolvedValue(mockMetadata);
            
            const result = await provider.getChildren();
            
            expect(result).toHaveLength(1);
            expect(result[0].label).toContain('Jarvis AI');
            expect(result[0].contextValue).toBe('repo');
        });

        it('should return info message when no integrations', async () => {
            mockMetadataReader.readMetadata.mockResolvedValue(null);
            
            const result = await provider.getChildren();
            
            expect(result).toHaveLength(1);
            expect(result[0].label).toBe('No integrations found');
            expect(result[0].contextValue).toBe('info');
        });
    });

    describe('getChildren - repo level', () => {
        it('should return modules for a repository', async () => {
            const mockMetadata = {
                version: '1.0.0',
                last_updated: '2025-10-13',
                agent: 'Agent-7',
                integrations: [
                    {
                        id: 'jarvis',
                        name: 'Jarvis AI',
                        source_repo: 'jarvis_repo',
                        status: 'operational' as const,
                        files_ported: 15,
                        total_source_files: 20,
                        percentage_ported: 75,
                        v2_compliant: true,
                        imports_working: true,
                        target_path: '/path/to/jarvis',
                        integration_date: '2025-10-01',
                        backward_compat: null,
                        health_check: {
                            last_test: '2025-10-13',
                            imports_passing: true,
                            errors: []
                        },
                        modules: [
                            {
                                name: 'memory_system',
                                file: 'memory.py',
                                lines: 250,
                                purpose: 'Memory management',
                                dependencies: ['sqlite3'],
                                optional: false,
                                import_path: 'from src.integrations.jarvis import memory_system'
                            }
                        ]
                    }
                ],
                statistics: {
                    total_integrations: 1,
                    total_files_ported: 15,
                    average_port_percentage: 75,
                    operational_integrations: 1,
                    v2_compliance_rate: 100,
                    import_success_rate: 100
                },
                conservative_scoping_methodology: {
                    principle: 'Test',
                    benefits: [],
                    process: []
                },
                vscode_extension_support: {
                    repository_navigator: { enabled: true, tree_view_data: 'test' },
                    import_path_helper: { enabled: true, suggestions_from: 'test' },
                    status_dashboard: { enabled: true, health_data: 'test' },
                    scoping_wizard: { enabled: true, methodology: 'test' }
                }
            };
            
            mockMetadataReader.readMetadata.mockResolvedValue(mockMetadata);
            
            const repoItem = new RepoTreeItem(
                'Jarvis AI',
                'jarvis',
                vscode.TreeItemCollapsibleState.Collapsed,
                'repo'
            );
            
            const result = await provider.getChildren(repoItem);
            
            expect(result).toHaveLength(1);
            expect(result[0].label).toContain('memory.py');
            expect(result[0].contextValue).toBe('module');
        });

        it('should return empty array for unknown repository', async () => {
            mockMetadataReader.readMetadata.mockResolvedValue({
                version: '1.0.0',
                last_updated: '2025-10-13',
                agent: 'Agent-7',
                integrations: [],
                statistics: {
                    total_integrations: 0,
                    total_files_ported: 0,
                    average_port_percentage: 0,
                    operational_integrations: 0,
                    v2_compliance_rate: 0,
                    import_success_rate: 0
                },
                conservative_scoping_methodology: {
                    principle: 'Test',
                    benefits: [],
                    process: []
                },
                vscode_extension_support: {
                    repository_navigator: { enabled: true, tree_view_data: 'test' },
                    import_path_helper: { enabled: true, suggestions_from: 'test' },
                    status_dashboard: { enabled: true, health_data: 'test' },
                    scoping_wizard: { enabled: true, methodology: 'test' }
                }
            });
            
            const repoItem = new RepoTreeItem(
                'Unknown Repo',
                'unknown',
                vscode.TreeItemCollapsibleState.Collapsed,
                'repo'
            );
            
            const result = await provider.getChildren(repoItem);
            
            expect(result).toHaveLength(0);
        });
    });

    describe('getChildren - module level', () => {
        it('should return empty array for modules', async () => {
            const moduleItem = new RepoTreeItem(
                'memory.py',
                'memory_system',
                vscode.TreeItemCollapsibleState.None,
                'module'
            );
            
            const result = await provider.getChildren(moduleItem);
            
            expect(result).toHaveLength(0);
        });
    });

    describe('refresh', () => {
        it('should fire tree data change event', () => {
            const mockFire = jest.fn();
            (provider as any)._onDidChangeTreeData.fire = mockFire;
            
            provider.refresh();
            
            expect(mockFire).toHaveBeenCalled();
        });
    });
});

describe('RepoTreeItem', () => {
    it('should construct with all properties', () => {
        const item = new RepoTreeItem(
            'Test Label',
            'test-id',
            vscode.TreeItemCollapsibleState.Collapsed,
            'repo',
            'Test Description',
            'Test Tooltip',
            '/path/to/file'
        );
        
        expect(item.label).toBe('Test Label');
        expect(item.repoId).toBe('test-id');
        expect(item.description).toBe('Test Description');
        expect(item.tooltip).toBe('Test Tooltip');
        expect(item.filePath).toBe('/path/to/file');
        expect(item.contextValue).toBe('repo');
    });

    it('should set command for module items', () => {
        const item = new RepoTreeItem(
            'module.py',
            'module-id',
            vscode.TreeItemCollapsibleState.None,
            'module',
            undefined,
            undefined,
            '/path/to/module.py'
        );
        
        expect(item.command).toBeDefined();
        expect(item.command?.command).toBe('repoNav.openFile');
        expect(item.command?.arguments).toEqual(['/path/to/module.py']);
    });

    it('should not set command for repo items', () => {
        const item = new RepoTreeItem(
            'Repo',
            'repo-id',
            vscode.TreeItemCollapsibleState.Collapsed,
            'repo'
        );
        
        expect(item.command).toBeUndefined();
    });
});

