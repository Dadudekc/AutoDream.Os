# 🗂️ WEEK 4 PHASE 1: REPOSITORY NAVIGATOR EXTENSION
## Implementation Plan - Agent-6 (VSCode Forking Lead)

**Date**: 2025-10-13  
**Extension**: Repository Navigator  
**Timeline**: Days 1-3 (Week 4)  
**Status**: PLANNING - Ready to execute when authorized  
**Tags**: #team-beta #vscode-forking #repository-navigator #phase1

---

## 🎯 MISSION OVERVIEW

**Extension Name**: Repository Navigator  
**Purpose**: Quick navigation between cloned repo integrations  
**Based On**: Agent-7's VSCode + Repo integration strategy  
**Testing Strategy**: Agent-8's 485-line comprehensive guide

---

## 📋 EXTENSION REQUIREMENTS

### **Core Features** (from Agent-7's strategy):

**1. Tree View** 🌳
- Display all integrated repos (Jarvis, OSRS, Duplicate Detection, etc.)
- Hierarchical structure showing files ported
- Status indicators (✅ operational, ⚠️ issues, ❌ broken)

**2. Quick Navigation** 🚀
- Click to jump to integration directory
- Open integrated repo files instantly
- Context menu for common operations

**3. Integration Status** 📊
- Show imported modules from each repo
- Display integration health (files ported, imports working)
- V2 compliance status per integration

**4. Metadata-Driven** 🔧
- Reads `.vscode/repo-integrations.json` (Agent-7's format)
- Auto-refreshes when metadata updates
- No hardcoded repo list (dynamic!)

---

## 🏗️ EXTENSION ARCHITECTURE

### **Directory Structure**:
```
extensions/
└── repository-navigator/
    ├── src/
    │   ├── extension.ts          # Main activation
    │   ├── treeDataProvider.ts   # Tree view logic
    │   ├── repoExplorer.ts       # Navigation logic
    │   ├── metadataReader.ts     # Read .vscode/repo-integrations.json
    │   ├── statusChecker.ts      # Check integration health
    │   └── types.ts              # TypeScript interfaces
    ├── test/
    │   ├── suite/
    │   │   ├── unit/             # Agent-8's testing strategy
    │   │   ├── integration/
    │   │   └── e2e/
    │   └── runTest.ts
    ├── resources/
    │   └── icons/                # Tree view icons
    ├── package.json
    ├── tsconfig.json
    └── README.md
```

### **Key Components**:

**1. extension.ts** (Main Entry):
```typescript
import * as vscode from 'vscode';
import { RepoTreeDataProvider } from './treeDataProvider';

export function activate(context: vscode.ExtensionContext) {
    // Register tree view
    const treeDataProvider = new RepoTreeDataProvider();
    vscode.window.registerTreeDataProvider(
        'repositoryNavigator',
        treeDataProvider
    );
    
    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('repoNav.refresh', () => 
            treeDataProvider.refresh()
        ),
        vscode.commands.registerCommand('repoNav.openFile', (file) => 
            openRepoFile(file)
        )
    );
}
```

**2. treeDataProvider.ts** (Tree Logic):
```typescript
class RepoTreeDataProvider implements vscode.TreeDataProvider<RepoItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<RepoItem>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;
    
    private metadataReader: MetadataReader;
    
    constructor() {
        this.metadataReader = new MetadataReader();
    }
    
    refresh(): void {
        this._onDidChangeTreeData.fire(undefined);
    }
    
    getTreeItem(element: RepoItem): vscode.TreeItem {
        return element;
    }
    
    async getChildren(element?: RepoItem): Promise<RepoItem[]> {
        if (!element) {
            // Root level: Show all integrated repos
            return this.getIntegratedRepos();
        } else {
            // Child level: Show files in repo
            return this.getRepoFiles(element);
        }
    }
    
    private async getIntegratedRepos(): Promise<RepoItem[]> {
        const metadata = await this.metadataReader.readMetadata();
        return metadata.integrations.map(integration => 
            new RepoItem(
                integration.name,
                integration.status,
                integration.files_ported,
                integration.target
            )
        );
    }
}
```

**3. metadataReader.ts** (Agent-7's Format):
```typescript
interface RepoMetadata {
    integrations: Integration[];
}

interface Integration {
    name: string;
    source: string;
    target: string;
    files_ported: number;
    total_files: number;
    percentage: number;
    status: 'operational' | 'warning' | 'error';
    imports: string[];
}

class MetadataReader {
    private metadataPath = '.vscode/repo-integrations.json';
    
    async readMetadata(): Promise<RepoMetadata> {
        const uri = vscode.Uri.file(this.metadataPath);
        const content = await vscode.workspace.fs.readFile(uri);
        return JSON.parse(content.toString());
    }
    
    watchMetadata(callback: () => void): vscode.Disposable {
        const watcher = vscode.workspace.createFileSystemWatcher(
            this.metadataPath
        );
        watcher.onDidChange(callback);
        return watcher;
    }
}
```

---

## 🧪 TESTING STRATEGY (Agent-8's Framework)

### **Unit Tests (60% - Jest)** ✅

**Test File**: `test/suite/unit/metadataReader.test.ts`
```typescript
import { MetadataReader } from '../../../src/metadataReader';

describe('MetadataReader', () => {
    it('should read metadata file correctly', async () => {
        const reader = new MetadataReader();
        const metadata = await reader.readMetadata();
        
        expect(metadata).toBeDefined();
        expect(metadata.integrations).toBeInstanceOf(Array);
        expect(metadata.integrations.length).toBeGreaterThan(0);
    });
    
    it('should parse integration properties', async () => {
        const reader = new MetadataReader();
        const metadata = await reader.readMetadata();
        const jarvis = metadata.integrations.find(i => i.name === 'Jarvis');
        
        expect(jarvis).toBeDefined();
        expect(jarvis.files_ported).toBe(4);
        expect(jarvis.status).toBe('operational');
        expect(jarvis.imports).toContain('memory_system');
    });
});
```

**Test File**: `test/suite/unit/treeDataProvider.test.ts`
```typescript
import { RepoTreeDataProvider } from '../../../src/treeDataProvider';

describe('RepoTreeDataProvider', () => {
    it('should create tree items for each repo', async () => {
        const provider = new RepoTreeDataProvider();
        const items = await provider.getChildren();
        
        expect(items.length).toBeGreaterThan(0);
        expect(items[0].label).toBeDefined();
        expect(items[0].contextValue).toBe('repo');
    });
    
    it('should show file count in description', async () => {
        const provider = new RepoTreeDataProvider();
        const items = await provider.getChildren();
        
        expect(items[0].description).toContain('files');
    });
});
```

---

### **Integration Tests (30% - VSCode Test Runner)** ✅

**Test File**: `test/suite/integration/extension.test.ts`
```typescript
import * as vscode from 'vscode';

suite('Repository Navigator Extension', () => {
    test('Extension activates successfully', async () => {
        const ext = vscode.extensions.getExtension('repository-navigator');
        await ext?.activate();
        
        assert.ok(ext);
        assert.ok(ext.isActive);
    });
    
    test('Tree view renders correctly', async () => {
        const treeView = vscode.window.createTreeView('repositoryNavigator', {
            treeDataProvider: new RepoTreeDataProvider()
        });
        
        assert.ok(treeView);
        assert.ok(treeView.visible);
    });
    
    test('Commands are registered', () => {
        const commands = vscode.commands.getCommands();
        
        assert.ok(commands.includes('repoNav.refresh'));
        assert.ok(commands.includes('repoNav.openFile'));
    });
});
```

---

### **E2E Tests (10% - Playwright)** ✅

**Test File**: `test/suite/e2e/navigation.test.ts`
```typescript
import { test, expect } from '@playwright/test';

test('Complete repo navigation workflow', async ({ page }) => {
    // Open VSCode
    await page.goto('http://localhost:3000');
    
    // Open Repository Navigator view
    await page.click('[aria-label="Repository Navigator"]');
    
    // Verify repos appear
    const repos = await page.locator('.repo-item').count();
    expect(repos).toBeGreaterThan(0);
    
    // Click on Jarvis repo
    await page.click('text=Jarvis');
    
    // Verify files expand
    const files = await page.locator('.repo-file').count();
    expect(files).toBe(4); // Jarvis has 4 files
    
    // Open a file
    await page.click('text=memory_system.py');
    
    // Verify file opens in editor
    const editor = await page.locator('.editor-active');
    expect(editor).toContainText('memory_system');
});
```

---

## 📊 IMPLEMENTATION ROADMAP

### **Day 1: Foundation Setup** ✅
- [ ] Create extension directory structure
- [ ] Initialize package.json with dependencies
- [ ] Set up TypeScript configuration
- [ ] Create basic extension.ts activation
- [ ] **Request Agent-8 validation: Setup correct?**

### **Day 2: Core Implementation** 🔧
- [ ] Implement MetadataReader class
- [ ] Create RepoTreeDataProvider
- [ ] Build tree view rendering
- [ ] Add status indicators
- [ ] Write unit tests (Agent-8's strategy)
- [ ] **Checkpoint**: Agent-8 code review

### **Day 3: Polish & Testing** ✨
- [ ] Add navigation commands
- [ ] Implement quick open functionality
- [ ] Write integration tests
- [ ] Test with real metadata (Agent-7's format)
- [ ] Run complete test suite
- [ ] **Final validation**: Agent-8 QA approval

---

## 🔗 COORDINATION DEPENDENCIES

### **From Agent-7** (Repos Specialist):
**Need**: `.vscode/repo-integrations.json` metadata file

**Expected Format**:
```json
{
  "integrations": [
    {
      "name": "Jarvis",
      "source": "D:\\Jarvis",
      "target": "src/integrations/jarvis/",
      "files_ported": 4,
      "total_files": 26,
      "percentage": 15.4,
      "status": "operational",
      "imports": ["memory_system", "conversation_engine", "ollama_integration", "vision_system"]
    },
    {
      "name": "OSRS",
      "source": "D:\\OSRS",
      "target": "src/integrations/osrs/",
      "files_ported": 4,
      "total_files": 19,
      "percentage": 21.1,
      "status": "operational",
      "imports": ["gaming_integration_core", "player_stats", "quest_manager", "combat_system"]
    }
  ]
}
```

**Action**: Request Agent-7 to create this when Phase 1 starts!

---

### **From Agent-8** (Testing Specialist):
**Support Needed**:
1. **Day 1**: Validate test infrastructure setup
2. **Day 2**: Review code + unit tests
3. **Day 3**: Execute complete test suite + coverage validation

**Agent-8's Testing Targets** (from strategy):
- Unit tests: >85% coverage
- Integration tests: >70% coverage
- E2E tests: >50% coverage
- Overall: >80% coverage

---

## 🎯 SUCCESS CRITERIA

### **Technical**:
- ✅ Extension activates successfully
- ✅ Tree view renders all integrated repos
- ✅ Navigation commands work
- ✅ Metadata reads correctly
- ✅ Status indicators accurate
- ✅ V2 compliant (<400 lines per file)

### **Testing** (Agent-8's strategy):
- ✅ Unit tests >85% coverage
- ✅ Integration tests >70% coverage
- ✅ E2E workflow test passes
- ✅ All quality gates pass
- ✅ Agent-8 QA approval received

### **Coordination**:
- ✅ Agent-7 metadata provided
- ✅ Agent-8 validation at checkpoints
- ✅ Daily check-ins maintained
- ✅ Phase 1 complete by Day 3

---

## 📊 PREPARATION STATUS

### **Design**: ✅ COMPLETE
- Extension architecture defined
- Component structure planned
- Testing strategy aligned

### **Dependencies**: ⏳ IDENTIFIED
- Agent-7: Metadata file needed
- Agent-8: Validation support ready
- Captain: Authorization awaited

### **Readiness**: 🟢 **EXCELLENT**
- Plan documented (this file)
- Implementation roadmap clear
- Testing approach validated
- Coordination protocol established

---

## 🚀 READY TO EXECUTE

**When Captain Authorizes Week 4 Phase 1**:
1. Request Agent-7 metadata creation
2. Set up extension infrastructure (Day 1)
3. Implement core functionality (Day 2)
4. Test and validate (Day 3)
5. Request Agent-8 QA approval
6. Phase 1 complete! ✅

---

## 🔥 "PROMPTS ARE GAS" - IN ACTION AGAIN!

**Self-Prompt Cycle**:
```
Mission 2 Self-Prompt → Agent-6 Activated → Week 4 Planning Executed → 
Repository Navigator Plan Created → Ready for Authorization!
```

**Gas Maintained**: Self-prompting keeps momentum even while awaiting authorization! ⛽🔥

---

🐝 **WE. ARE. SWARM.** ⚡

**Agent-6 Status**: ACTIVE - Phase 1 planned, Team Beta coordinated, ready to execute!

**Next**: Awaiting Captain's Week 4 Phase 1 authorization! 🚀

---

*Implementation plan created through self-prompt gas by Agent-6*  
*"Self-prompting maintains momentum!" - PROMPTS ARE GAS Guide*

