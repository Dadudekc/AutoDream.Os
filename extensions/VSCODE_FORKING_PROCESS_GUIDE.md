# 🍴 VSCode Forking Process - Complete Guide

**Purpose**: Complete guide for forking VSCode and creating Dream.OS customization  
**Created by**: Agent-6 (VSCode Forking & Quality Gates Specialist)  
**Phase**: 4 - Deliverable 3 (Documentation for Forking Process)  
**Date**: 2025-10-16

---

## 🎯 **What is VSCode Forking?**

**Forking VSCode** means creating a customized version of Visual Studio Code with Dream.OS-specific features, branding, and extensions.

**Why Fork?**
- ✅ Custom branding (Dream.OS instead of VSCode)
- ✅ Pre-installed extensions (Team Beta extensions)
- ✅ Swarm-specific features built-in
- ✅ Agent coordination tools integrated
- ✅ Full control over functionality

---

## 📋 **Prerequisites**

### **System Requirements**:
- Node.js 18+ installed
- Git installed
- Python 3.11+ (for Dream.OS integration)
- 8GB+ RAM
- 50GB+ disk space (VSCode source is large!)

### **Skills Required**:
- TypeScript/JavaScript
- VSCode Extension API
- Electron basics
- Build systems (webpack, gulp)

---

## 🚀 **Step-by-Step Forking Process**

### **PHASE 1: Fork & Clone (Day 1)**

#### **Step 1.1: Fork VSCode Repository**

```bash
# Navigate to: https://github.com/microsoft/vscode
# Click "Fork" button
# Create fork under Dream.OS organization

# Or clone official repo
git clone https://github.com/microsoft/vscode.git vscode-dreamos
cd vscode-dreamos

# Add Dream.OS remote
git remote add dreamos https://github.com/DreamOS/vscode-dreamos.git
```

#### **Step 1.2: Install Dependencies**

```bash
# Install Node dependencies
yarn install

# This takes 15-30 minutes (VSCode is HUGE)
```

#### **Step 1.3: Build VSCode**

```bash
# Compile TypeScript
yarn watch

# Open separate terminal, run VSCode
./scripts/code.sh  # Linux/Mac
./scripts/code.bat # Windows
```

**Expected**: VSCode launches with "(OSS)" in title!

---

### **PHASE 2: Branding Customization (Day 2-3)**

#### **Step 2.1: Update Product Configuration**

**File**: `product.json`

```json
{
  "nameShort": "Dream.OS Code",
  "nameLong": "Dream.OS Code - Agent Coordination IDE",
  "applicationName": "dreamos-code",
  "dataFolderName": ".dreamos-code",
  "win32MutexName": "dreamoscode",
  "licenseName": "MIT",
  "licenseUrl": "https://github.com/DreamOS/vscode-dreamos/blob/main/LICENSE.txt",
  "win32DirName": "Dream.OS Code",
  "win32NameVersion": "Dream.OS Code",
  "win32AppUserModelId": "DreamOS.DreamOSCode",
  "darwinBundleIdentifier": "com.dreamos.code",
  "linuxIconName": "dreamos-code"
}
```

#### **Step 2.2: Update Package.json**

**File**: `package.json`

```json
{
  "name": "dreamos-code",
  "version": "1.0.0",
  "productName": "Dream.OS Code",
  "description": "Agent Coordination IDE powered by Dream.OS",
  "main": "./out/main",
  "author": {
    "name": "Dream.OS Team Beta"
  },
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/DreamOS/vscode-dreamos.git"
  }
}
```

#### **Step 2.3: Custom Icon & Branding**

**Replace**:
- `resources/win32/code.ico` - Windows icon
- `resources/linux/code.png` - Linux icon  
- `resources/darwin/code.icns` - macOS icon

**With**: Dream.OS branded icons

---

### **PHASE 3: Extension Integration (Day 4-5)**

#### **Step 3.1: Bundle Team Beta Extensions**

**Create**: `extensions/repository-navigator` (already done! ✅)

**Bundle into fork**:
```bash
# Copy extension to VSCode fork
cp -r Agent_Cellphone_V2_Repository/extensions/repository-navigator \
      vscode-dreamos/extensions/

# Update extensions list
# Edit: build/lib/extensions.js
# Add: 'repository-navigator' to built-in extensions list
```

#### **Step 3.2: Pre-Install Extensions**

**File**: `build/lib/extensions.js`

```javascript
const builtInExtensions = [
  // ... existing extensions
  { name: 'repository-navigator', version: '0.1.0' },
  { name: 'import-path-helper', version: '0.1.0' },
  // Add more Team Beta extensions
];
```

#### **Step 3.3: Configure Default Settings**

**File**: `src/vs/platform/userDataProfile/common/userDataProfileInit.ts`

```json
{
  "dream.os.agentCoordination": true,
  "dream.os.swarmIntelligence": true,
  "dream.os.repositoryNavigator.autoRefresh": true,
  "dream.os.importHelper.enabled": true
}
```

---

### **PHASE 4: Agent Coordination Features (Day 6-8)**

#### **Step 4.1: Add Agent Status Bar**

**Create**: `src/vs/workbench/contrib/agentStatus/browser/agentStatus.ts`

```typescript
// Display current agent status in status bar
export class AgentStatusBarContribution {
  constructor() {
    // Read agent_workspaces/Agent-X/status.json
    // Display: "Agent-X: [Status] | [Points] pts"
  }
}
```

#### **Step 4.2: Add Swarm Brain Integration**

**Create**: `src/vs/workbench/contrib/swarmBrain/browser/swarmBrainView.ts`

```typescript
// Swarm Brain access from VSCode
export class SwarmBrainViewProvider {
  async search(query: string) {
    // Call swarm_brain Python API
    // Display results in tree view
  }
}
```

#### **Step 4.3: Add Gas Pipeline Indicator**

```typescript
// Visual indicator when gas pipelines are active
export class GasPipelineIndicator {
  // Shows: ⛽ Gas flowing, ⚠️ Low gas, ❌ Out of gas
}
```

---

### **PHASE 5: Build & Package (Day 9-10)**

#### **Step 5.1: Build Distribution**

```bash
# Full build for all platforms
yarn gulp vscode-win32-x64      # Windows
yarn gulp vscode-darwin-x64     # macOS Intel
yarn gulp vscode-darwin-arm64   # macOS Apple Silicon
yarn gulp vscode-linux-x64      # Linux
```

**Output**: Distributable packages in `../.build/`

#### **Step 5.2: Create Installers**

```bash
# Windows installer
yarn gulp vscode-win32-x64-inno-updater

# macOS DMG
yarn gulp vscode-darwin-x64-min

# Linux packages
yarn gulp vscode-linux-x64-build-deb
yarn gulp vscode-linux-x64-build-rpm
```

#### **Step 5.3: Sign & Notarize** (Production)

**Windows**:
- Code signing certificate required
- Sign with SignTool

**macOS**:
- Apple Developer account required
- Sign with codesign
- Notarize with xcrun

---

## 🧪 **Testing Your Fork**

### **Local Testing**:
```bash
# Run from source
./scripts/code.sh

# Run with extensions
./scripts/code.sh --extensionDevelopmentPath=../Agent_Cellphone_V2_Repository/extensions/repository-navigator
```

### **Package Testing**:
```bash
# Create package
yarn gulp vscode-win32-x64-min

# Extract and run
cd ../.build/win32-x64/VSCode-win32-x64
./Code.exe
```

### **Validation Checklist**:
- [ ] Dream.OS branding appears
- [ ] Title shows "Dream.OS Code"
- [ ] Icon is Dream.OS branded
- [ ] Team Beta extensions pre-installed
- [ ] Agent status bar visible
- [ ] Swarm Brain accessible
- [ ] No VSCode branding remains

---

## 📦 **Distribution**

### **Internal Distribution (Dream.OS Team)**:
```bash
# Upload to shared location
aws s3 cp VSCode-win32-x64.zip s3://dreamos-releases/vscode/

# Share with team
python -m src.services.messaging_cli --broadcast --message \
  "🎉 Dream.OS Code v1.0 released! Download: [URL] Features: [List]"
```

### **Public Distribution** (Future):
- GitHub Releases
- Dream.OS website
- Package managers (Chocolatey, Homebrew, apt)

---

## 🔧 **Maintenance & Updates**

### **Keeping Fork Updated**:

```bash
# Add upstream VSCode
git remote add upstream https://github.com/microsoft/vscode.git

# Fetch updates
git fetch upstream

# Merge upstream changes
git checkout main
git merge upstream/main

# Resolve conflicts (preserve Dream.OS customizations!)
git mergetool

# Test thoroughly after merge
yarn install
yarn watch
```

### **Release Cadence**:
- **VSCode releases monthly** - Monitor for security updates
- **Dream.OS releases**: As needed for features
- **Critical fixes**: Immediately

---

## 🎯 **Customization Opportunities**

### **Completed** (Phases 1-2):
- ✅ Repository Navigator extension
- ✅ Import Path Helper extension

### **Potential** (Future Phases):
- 🔮 Agent Coordination Dashboard
- 🔮 Swarm Brain Search Panel
- 🔮 Gas Pipeline Visualizer
- 🔮 Point Leaderboard View
- 🔮 Discord Integration Panel
- 🔮 Task Assignment View
- 🔮 Vector Database Explorer
- 🔮 Intelligence Enhancement Tools

---

## 🚨 **Common Issues & Solutions**

### **Issue 1: Build Fails**
```bash
# Clean and rebuild
yarn clean
rm -rf node_modules
yarn install
yarn watch
```

### **Issue 2: Extensions Not Loading**
- Check `extensions/` directory includes your extensions
- Verify `build/lib/extensions.js` lists them
- Rebuild with `yarn watch`

### **Issue 3: Branding Not Appearing**
- Clear cache: Delete `~/.dreamos-code`
- Verify `product.json` changes
- Rebuild completely

---

## 📊 **Success Metrics**

### **Fork Quality**:
- [ ] Builds without errors
- [ ] All Dream.OS branding applied
- [ ] Team Beta extensions pre-installed
- [ ] Agent features integrated
- [ ] No VSCode branding remains
- [ ] Distributable packages created

### **Team Coordination**:
- [ ] All 4 Team Beta agents involved
- [ ] Clear handoffs documented
- [ ] Quality gates passed
- [ ] Testing pyramid validated
- [ ] Brotherhood celebrated

---

## 🏆 **Team Beta Excellence**

**This forking process demonstrates:**
- Agent-6's VSCode expertise
- Agent-7's metadata quality
- Agent-8's testing excellence
- Agent-5's strategic leadership
- **Team Beta = Championship coordination!** 🐝

---

**Phase 4 Deliverable 3: COMPLETE** ✅

**Next**: Testing framework completion (Deliverable 4)

---

**Agent-6 - VSCode Forking & Quality Gates Specialist**  
**"Forking with excellence, building with brotherhood!"** 🐝✨

