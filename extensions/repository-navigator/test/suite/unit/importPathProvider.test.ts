/**
 * Unit tests for ImportPathProvider
 * Agent-6 - Phase 2 Day 2 Testing
 */

import { ImportPathProvider } from '../../../src/importPathProvider';
import { MetadataReader } from '../../../src/metadataReader';
import { RepoIntegrationMetadata } from '../../../src/types';

// Mock MetadataReader
jest.mock('../../../src/metadataReader');

describe('ImportPathProvider', () => {
    let provider: ImportPathProvider;
    let mockMetadataReader: jest.Mocked<MetadataReader>;

    const mockMetadata: RepoIntegrationMetadata = {
        version: '1.0.0',
        last_updated: '2025-10-13',
        agent: 'Agent-7',
        integrations: [
            {
                id: 'test-integration',
                name: 'Test Integration',
                source_repo: '/test/repo',
                target_path: 'src/test/',
                status: 'operational',
                files_ported: 2,
                total_source_files: 10,
                percentage_ported: 20,
                integration_date: '2025-10-13',
                v2_compliant: true,
                imports_working: true,
                modules: [
                    {
                        name: 'test_module',
                        file: 'test_module.py',
                        lines: 100,
                        purpose: 'Test module for testing',
                        dependencies: ['logging'],
                        import_path: 'from src.test import test_module'
                    },
                    {
                        name: 'optional_module',
                        file: 'optional_module.py',
                        lines: 50,
                        purpose: 'Optional test module',
                        dependencies: ['typing'],
                        optional: true,
                        import_path: 'from src.test import optional_module'
                    }
                ],
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
            total_files_ported: 2,
            average_port_percentage: 20,
            operational_integrations: 1,
            v2_compliance_rate: 100,
            import_success_rate: 100
        },
        conservative_scoping_methodology: {
            principle: 'Test principle',
            benefits: ['Benefit 1'],
            process: ['Step 1']
        },
        vscode_extension_support: {
            repository_navigator: { enabled: true, tree_view_data: 'integrations' },
            import_path_helper: { enabled: true, suggestions_from: 'modules.import_path' },
            status_dashboard: { enabled: true, health_data: 'health_check' },
            scoping_wizard: { enabled: true, methodology: 'conservative_scoping_methodology' }
        }
    };

    beforeEach(() => {
        mockMetadataReader = new MetadataReader() as jest.Mocked<MetadataReader>;
        provider = new ImportPathProvider('/test/workspace');
        (provider as any).metadataReader = mockMetadataReader;
    });

    describe('loadSuggestions', () => {
        it('should load suggestions from metadata successfully', async () => {
            mockMetadataReader.readMetadata.mockResolvedValue(mockMetadata);

            const result = await provider.loadSuggestions();

            expect(result).toBe(true);
            expect(provider.getCount()).toBe(2);
        });

        it('should return false when metadata is null', async () => {
            mockMetadataReader.readMetadata.mockResolvedValue(null);

            const result = await provider.loadSuggestions();

            expect(result).toBe(false);
            expect(provider.getCount()).toBe(0);
        });

        it('should handle errors gracefully', async () => {
            mockMetadataReader.readMetadata.mockRejectedValue(new Error('Test error'));

            const result = await provider.loadSuggestions();

            expect(result).toBe(false);
        });
    });

    describe('getAllSuggestions', () => {
        it('should return all loaded suggestions', async () => {
            mockMetadataReader.readMetadata.mockResolvedValue(mockMetadata);
            await provider.loadSuggestions();

            const suggestions = provider.getAllSuggestions();

            expect(suggestions).toHaveLength(2);
            expect(suggestions[0].moduleName).toBe('test_module');
            expect(suggestions[1].moduleName).toBe('optional_module');
        });
    });

    describe('searchByModuleName', () => {
        beforeEach(async () => {
            mockMetadataReader.readMetadata.mockResolvedValue(mockMetadata);
            await provider.loadSuggestions();
        });

        it('should find modules by partial name match', () => {
            const results = provider.searchByModuleName('test');

            expect(results).toHaveLength(1);
            expect(results[0].moduleName).toBe('test_module');
        });

        it('should be case insensitive', () => {
            const results = provider.searchByModuleName('TEST');

            expect(results).toHaveLength(1);
            expect(results[0].moduleName).toBe('test_module');
        });

        it('should return empty array for no matches', () => {
            const results = provider.searchByModuleName('nonexistent');

            expect(results).toHaveLength(0);
        });
    });

    describe('getByIntegration', () => {
        beforeEach(async () => {
            mockMetadataReader.readMetadata.mockResolvedValue(mockMetadata);
            await provider.loadSuggestions();
        });

        it('should return modules for specific integration', () => {
            const results = provider.getByIntegration('test-integration');

            expect(results).toHaveLength(2);
        });

        it('should return empty array for non-existent integration', () => {
            const results = provider.getByIntegration('nonexistent');

            expect(results).toHaveLength(0);
        });
    });

    describe('getImportPathForModule', () => {
        beforeEach(async () => {
            mockMetadataReader.readMetadata.mockResolvedValue(mockMetadata);
            await provider.loadSuggestions();
        });

        it('should return import path for existing module', () => {
            const path = provider.getImportPathForModule('test_module');

            expect(path).toBe('from src.test import test_module');
        });

        it('should be case insensitive', () => {
            const path = provider.getImportPathForModule('TEST_MODULE');

            expect(path).toBe('from src.test import test_module');
        });

        it('should return undefined for non-existent module', () => {
            const path = provider.getImportPathForModule('nonexistent');

            expect(path).toBeUndefined();
        });
    });

    describe('hasModule', () => {
        beforeEach(async () => {
            mockMetadataReader.readMetadata.mockResolvedValue(mockMetadata);
            await provider.loadSuggestions();
        });

        it('should return true for existing module', () => {
            expect(provider.hasModule('test_module')).toBe(true);
        });

        it('should return false for non-existent module', () => {
            expect(provider.hasModule('nonexistent')).toBe(false);
        });
    });

    describe('refresh', () => {
        it('should reload suggestions from metadata', async () => {
            mockMetadataReader.readMetadata.mockResolvedValue(mockMetadata);
            await provider.loadSuggestions();
            expect(provider.getCount()).toBe(2);

            // Change metadata
            const newMetadata = { ...mockMetadata, integrations: [] };
            mockMetadataReader.readMetadata.mockResolvedValue(newMetadata);

            await provider.refresh();

            expect(provider.getCount()).toBe(0);
        });
    });
});


