module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: [
    'eslint:recommended'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
    // === V2 COMPLIANCE - LOC LIMITS ===

    // File-level limits (V2 Compliance: under 300 lines)
    'max-lines': ['error', {
      max: 300,
      skipBlankLines: true,
      skipComments: true
    }],

    // Function-level limits (10-30 LOC sweet spot)
    'max-lines-per-function': ['error', {
      max: 30,
      skipBlankLines: true,
      skipComments: true,
      IIFEs: true
    }],

    // Statement limits (smaller for better testability)
    'max-statements': ['warn', 15, { ignoreTopLevelFunctions: true }],
    'max-statements-per-line': ['error', { max: 2 }],

    // === CODE QUALITY ENFORCEMENT ===

    // Complexity limits
    'complexity': ['error', 10],

    // Parameter limits (too many params = complex function)
    'max-params': ['error', 4],

    // Nested depth (deep nesting = hard to read)
    'max-depth': ['error', 4],
    'max-nested-callbacks': ['error', 3],

    // === CLEAN CODE PRACTICES ===

    // Enforce single responsibility
    'max-classes-per-file': ['error', 1],

    // Prevent god objects/functions
    'no-multi-assign': 'error',

    // Function length (additional check)
    'max-len': ['error', {
      code: 100,
      tabWidth: 2,
      ignoreUrls: true,
      ignoreStrings: true,
      ignoreTemplateLiterals: true,
      ignoreComments: true
    }],

    // === V2 COMPLIANCE REPORTING ===

    // Additional code quality rules
    'no-console': 'warn',
    'prefer-const': 'error',
    'no-var': 'error'
  },
  overrides: [
    // Special rules for test files
    {
      files: ['**/*.test.js', '**/*.spec.js'],
      rules: {
        'max-lines': 'off',
        'max-lines-per-function': 'off',
        'max-statements': 'off',
        'max-params': 'off',
        'complexity': 'off'
      }
    },

    // Special rules for config files
    {
      files: ['**/webpack.config.js', '**/rollup.config.js', '**/.eslintrc.cjs'],
      rules: {
        'max-lines': 'off'
      }
    },

    // Exclude corrupted files
    {
      files: ['**/system-integration-test-core.js'],
      rules: {
        'max-lines': 'off'
      }
    },

    // Allow console in development mode for main application files
    {
      files: ['**/trading-robot-main.js'],
      rules: {
        'no-console': ['warn', { allow: ['log', 'error'] }]
      }
    },

    // Allow console for logging utility files
    {
      files: ['**/utilities/logging-utils.js', '**/logging-utils.js'],
      rules: {
        'no-console': ['warn', { allow: ['info', 'error', 'warn', 'log'] }]
      }
    },

    // Utility modules (slightly more lenient)
    {
      files: ['**/utils/**', '**/utilities/**', '**/helpers/**'],
      rules: {
        'max-lines': ['error', 400], // Utility files can be larger
        'max-lines-per-function': ['error', 20], // But functions stay small
        'complexity': ['error', 15] // Slightly higher complexity allowed
      }
    },

    // Service layer files
    {
      files: ['**/services/**', '**/core/**'],
      rules: {
        'max-lines': ['error', 350], // Services can be slightly larger
        'max-params': ['error', 5] // Services might need more params
      }
    }
  ]
};
