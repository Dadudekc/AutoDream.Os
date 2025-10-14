/**
 * Jest Configuration - Repository Navigator Extension
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 2
 * Testing Strategy by: Agent-8 (Testing Specialist)
 */

module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    roots: ['<rootDir>/test/suite/unit'],
    testMatch: ['**/*.test.ts'],
    moduleNameMapper: {
        '^vscode$': '<rootDir>/__mocks__/vscode.js'
    },
    collectCoverageFrom: [
        'src/**/*.ts',
        '!src/**/*.d.ts',
        '!src/types.ts'
    ],
    coverageThreshold: {
        global: {
            branches: 60,
            functions: 70,
            lines: 80,
            statements: 80
        }
    },
    coverageDirectory: 'coverage',
    verbose: true
};
