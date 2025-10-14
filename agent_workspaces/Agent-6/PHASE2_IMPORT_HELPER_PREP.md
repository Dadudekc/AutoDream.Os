# Phase 2: Import Path Helper - Preparation Document

**Agent**: Agent-6 (Coordination & Communication Specialist)
**Date**: October 13, 2025
**Status**: AUTHORIZED - Ready to Execute Post-QA

## 🎯 MISSION OBJECTIVE

**Build VSCode Extension**: Import Path Helper
- **Purpose**: Auto-suggest correct import paths for integrated repositories
- **Data Source**: Agent-7's `.vscode/repo-integrations.json` (modules.import_path fields)
- **User Experience**: IntelliSense-style suggestions when typing imports

## 📊 METADATA ANALYSIS

**Agent-7's Import Path Data** (from repo-integrations.json):
- **12 modules** across 3 integrations
- Each module has `import_path` field (e.g., "from src.integrations.jarvis import memory_system")
- **Extensions Support** confirmed at lines 200-203:
  ```json
  "import_path_helper": {
    "enabled": true,
    "suggestions_from": "modules.import_path fields"
  }
  ```

**Import Paths Available**:

### Jarvis Integration (4 modules):
1. `from src.integrations.jarvis import memory_system`
2. `from src.integrations.jarvis import conversation_engine`
3. `from src.integrations.jarvis import ollama_integration`
4. `from src.integrations.jarvis import vision_system`

### OSRS Integration (4 modules):
1. `from src.integrations.osrs import gaming_integration_core`
2. `from src.integrations.osrs import osrs_agent_core`
3. `from src.integrations.osrs import swarm_coordinator`
4. `from src.integrations.osrs import performance_validation`

### Duplicate Detection (4 modules):
1. `from src.tools.duplicate_detection import find_duplicates`
2. `from src.tools.duplicate_detection import file_hash`
3. `from src.tools.duplicate_detection import dups_format`
4. `from src.tools.duplicate_detection import duplicate_gui`

## 🏗️ EXTENSION ARCHITECTURE

### Core Components (Parallel to Phase 1):

1. **`src/types.ts`** (extend existing)
   - Add `ImportSuggestion` interface
   - Add `ImportPathProvider` interface

2. **`src/importPathProvider.ts`** (NEW)
   - Class to read import paths from metadata
   - Methods:
     - `getImportSuggestions()` - Return all import paths
     - `searchImportPaths(query)` - Filter by module name
     - `getImportForModule(moduleName)` - Get specific import

3. **`src/completionProvider.ts`** (NEW)
   - Implements `vscode.CompletionItemProvider`
   - Provides IntelliSense suggestions
   - Triggers on "from" keyword or "import" keyword
   - Methods:
     - `provideCompletionItems()` - Core IntelliSense logic
     - `resolveCompletionItem()` - Add documentation

4. **`src/extension.ts`** (UPDATE)
   - Register completion provider
   - Register import path refresh command
   - Watch metadata for changes

### Features:

1. **IntelliSense Suggestions**
   - Trigger when user types "from src.integrations" or "import"
   - Show all available modules with descriptions
   - Insert correct import path on selection

2. **Search & Filter**
   - Filter by module name as user types
   - Show module purpose in suggestion detail
   - Highlight optional modules differently

3. **Documentation**
   - Show module lines, dependencies, purpose
   - Link to integration files
   - Show health status

4. **Refresh Command**
   - `importHelper.refresh` command
   - Reloads metadata on changes
   - Updates suggestions dynamically

## 🧪 TESTING STRATEGY (Agent-8's 60/30/10 Pyramid)

### Unit Tests (60% - ~16 tests):
1. **importPathProvider.ts** (~8 tests)
   - Read metadata correctly
   - Parse import paths
   - Search/filter logic
   - Handle missing metadata
   - Handle malformed data

2. **completionProvider.ts** (~8 tests)
   - Generate completion items
   - Filter suggestions
   - Resolve completion details
   - Handle edge cases

### Integration Tests (30% - ~8 tests):
1. Completion provider registration
2. Metadata changes trigger refresh
3. Command execution
4. VSCode API integration

### E2E Tests (10% - ~3 tests):
1. User types "from", sees suggestions
2. User selects suggestion, import inserted
3. Metadata update reflected in suggestions

**Total**: ~27 tests (matching Phase 1 unit test count)

## 📁 FILE STRUCTURE

```
extensions/repository-navigator/  (existing)
├── src/
│   ├── types.ts                    (EXTEND)
│   ├── metadataReader.ts          (REUSE - already has readMetadata)
│   ├── importPathProvider.ts      (NEW)
│   ├── completionProvider.ts      (NEW)
│   └── extension.ts               (UPDATE)
├── test/
│   └── suite/
│       ├── unit/
│       │   ├── importPathProvider.test.ts   (NEW)
│       │   └── completionProvider.test.ts   (NEW)
│       ├── integration/
│       │   └── importHelper.integration.test.ts  (NEW)
│       └── e2e/
│           └── importHelper.e2e.test.ts     (NEW)
└── package.json                   (UPDATE - add completion provider)
```

## 🎯 EXECUTION TIMELINE

**Estimated**: 1-2 days (matching Phase 1 pace)

### Day 1: Core Implementation
- [ ] Extend `types.ts` with import interfaces
- [ ] Implement `importPathProvider.ts` (read + search)
- [ ] Implement `completionProvider.ts` (IntelliSense)
- [ ] Update `extension.ts` (register provider)
- [ ] Update `package.json` (add activation events)

**Estimated**: ~6-8 files, ~500 lines

### Day 2: Testing
- [ ] Unit tests (16 tests, 85%+ coverage)
- [ ] Integration tests (8 tests)
- [ ] E2E tests (3 tests)
- [ ] Test documentation

**Estimated**: ~5 test files, ~600 lines

### Total Phase 2: ~11 files, ~1,100 lines, ~27 tests

## 🤝 TEAM BETA COORDINATION

**Agent-7** (Metadata Provider):
- ✅ Import paths ready in repo-integrations.json
- ✅ 12 modules documented
- ✅ Extension support confirmed

**Agent-8** (Testing Strategist):
- ✅ 60/30/10 pyramid proven in Phase 1
- ✅ Will apply same strategy to Phase 2
- ✅ QA checkpoints established

**Agent-6** (Implementation Lead):
- ✅ Phase 1 experience (9 files, 40 tests)
- ✅ Metadata structure understood
- ✅ Testing pyramid mastered
- ✅ Ready for instant execution post-QA

## 🔥 READINESS CHECKLIST

- [x] Metadata analyzed (12 import paths identified)
- [x] Architecture designed (4 new/updated files)
- [x] Testing strategy defined (60/30/10 pyramid)
- [x] Timeline estimated (1-2 days)
- [x] Team Beta coordination confirmed
- [x] Phase 1 experience applied
- [x] Agent-7's data validated
- [x] Agent-8's strategy ready

## 🚀 ACTIVATION TRIGGER

**Awaiting**: Agent-8 Phase 1 QA validation approval

**Upon Approval**: Execute Phase 2 immediately (ZERO delay)

**First Command**: Implement `importPathProvider.ts` with metadata reading

---

**Status**: PREPPED AND READY - Instant execution upon QA validation! 🏆🐝⚡


