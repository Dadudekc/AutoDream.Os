# Onboarding Workspace - Agent Cellphone V2

This workspace contains onboarding system artifacts and configurations, including comprehensive Single Source of Truth (SSOT) training materials.

## V2 Artifacts

### **Core Components**
- Configuration files and protocols
- Templates and definitions
- Operational data and metrics
- Training materials and assessments

### **SSOT Training Materials** 🆕
- **SSOT Compliance Training**: Complete training module with assessments
- **Devlog Training Module**: MANDATORY training for all agents 🆕
- **Practical Exercises**: Hands-on workflow examples and exercises
- **Troubleshooting Guide**: Comprehensive issue resolution guide
- **Agent Responsibilities Matrix**: Role-specific SSOT duties and expectations

## Training Structure

### **Phase 1: Foundation Training**
1. **System Orientation** (60 min)
2. **Role-Specific Training** (120 min)

### **Phase 2: SSOT Training** 🆕
3. **Single Source of Truth Training** (45 min)
   - SSOT fundamentals and principles
   - Compliance workflow procedures
   - Validation tools and scripts
4. **Devlog System Training** (30 min) 🆕
   - **MANDATORY** - All agents must complete
   - SSOT principles and compliance
   - Devlog tool usage and best practices
   - Discord integration and team communication
5. **Messaging Etiquette Framework Training** (45 min) 🆕
   - **MANDATORY** - All agents must complete
   - Response protocol and time standards
   - CLI command mastery and troubleshooting
   - Protocol violation prevention and handling

### **Phase 3: Integration**
5. **System Integration** (90 min)
6. **Performance Validation** (60 min)

### **Phase 4: Contract Automation Training** 🆕
7. **Contract Claiming System Training** (45 min) 🆕
   - **MANDATORY** - All agents must complete
   - Contract claiming and completion workflow
   - Automated task distribution system
   - Extra credit system and points tracking
   - Continuous work cycle automation
8. **Automated Workflow Integration** (30 min) 🆕
   - **MANDATORY** - All agents must complete
   - Integration with messaging system
   - Automated task claiming and completion
   - Continuous work without stopping

## Quick Start Guide

### **For New Agents**
1. Complete foundation training modules
2. **Complete SSOT training and certification** 🆕
3. **Complete Devlog training and certification** 🆕 (MANDATORY)
4. **Complete Messaging Etiquette training and certification** 🆕 (MANDATORY)
5. **Run role validation script** 🆕 - `python scripts/onboarding/validate_phase2_roles.py [Agent-Name] "[Claimed-Role]"`
6. Pass all assessments (85% minimum)
7. Receive role-specific assignments

### **For Existing Agents**
1. **Complete SSOT training immediately** 🆕
2. **Complete Devlog training immediately** 🆕 (MANDATORY)
3. **Complete Messaging Etiquette training immediately** 🆕 (MANDATORY)
4. **Run role validation script** 🆕 - `python scripts/onboarding/validate_phase2_roles.py [Agent-Name] "[Claimed-Role]"`
5. Review agent-specific responsibilities
6. Practice with troubleshooting guide
7. Get certified in SSOT procedures

## Training Materials

### **Location**: `training_documents/`
- `agent_roles_and_responsibilities.md` - Agent role definitions
- `system_overview.md` - System architecture overview
- `ssot_compliance_training.md` - SSOT training module 🆕
- `devlog_training_module.md` - Devlog system training 🆕 (MANDATORY)
- `messaging_etiquette_framework.md` - Messaging etiquette training 🆕 (MANDATORY)
- `universal_development_principles.md` - Universal development principles
- `troubleshooting_guide.md` - Issue resolution guide

### **Mandatory Training Modules** 🆕
1. **SSOT Compliance Training** - Required for all agents
2. **Devlog System Training** - Required for all agents (team communication SSOT)
3. **Messaging Etiquette Framework Training** - Required for all agents (agent coordination SSOT)
4. **Contract Claiming System Training** - Required for all agents (automated workflow SSOT) 🆕
5. **Automated Workflow Integration Training** - Required for all agents (continuous work cycle SSOT) 🆕

## SSOT Compliance Requirements

### **Core Principles**
- **Single Source of Truth**: All project information must have one authoritative source
- **Devlog System**: All team communication must go through the devlog system
- **No Duplication**: Information must not be scattered across multiple systems
- **Searchable History**: All communications must be retrievable and searchable

### **Devlog System Requirements** 🆕
- **✅ MANDATORY**: All project updates must use devlog system
- **✅ MANDATORY**: No manual Discord posting for project updates
- **✅ MANDATORY**: All agents must identify themselves in entries
- **✅ MANDATORY**: Proper categorization and content standards
- **❌ PROHIBITED**: Project updates via email, chat, or direct Discord
- **❌ PROHIBITED**: Vague or unclear content in devlog entries

### **Contract Automation System Requirements** 🆕
- **✅ MANDATORY**: All agents must use contract claiming system for tasks
- **✅ MANDATORY**: Complete contracts to claim extra credit points
- **✅ MANDATORY**: Use automated workflow for continuous task execution
- **✅ MANDATORY**: Run completion commands to get next task automatically
- **❌ PROHIBITED**: Manual task assignment outside contract system
- **❌ PROHIBITED**: Stopping work without claiming next contract

### **Compliance Validation**
- **Training Completion**: Must complete devlog training module
- **Practical Assessment**: Must demonstrate proper tool usage

## Contract Automation Workflow 🆕

### **Continuous Work Cycle**
**TASK → EXECUTE → COMPLETE → AUTO-CLAIM NEXT → REPEAT**

### **Step-by-Step Workflow**
1. **Get Next Task**: `python -m src.services.messaging --agent Agent-X --get-next-task`
2. **Claim Contract**: `python -m src.services.messaging --agent Agent-X --claim-contract CONTRACT-ID`
3. **Execute Task**: Complete the contract requirements and deliverables
4. **Complete Contract**: `python -m src.services.messaging --agent Agent-X --complete-contract CONTRACT-ID`
5. **Auto-Continue**: System automatically provides next available task
6. **Repeat**: Continue the cycle without stopping

### **Contract Categories Available**
- **Coordination Enhancement**: 6 contracts (1,080 points)
- **Phase Transition Optimization**: 6 contracts (1,120 points)
- **Testing Framework Enhancement**: 4 contracts (685 points)
- **Strategic Oversight**: 3 contracts (600 points)
- **Refactoring Tool Preparation**: 3 contracts (625 points)
- **Performance Optimization**: 2 contracts (425 points)

### **Total Available**: 24 contracts, 4,175 extra credit points

### **Automation Benefits**
- **Continuous Work**: Agents never stop working
- **Automatic Task Distribution**: No manual intervention needed
- **Extra Credit System**: Points-based motivation and tracking
- **Role-Based Prioritization**: Tasks automatically matched to agent roles
- **Progress Tracking**: Real-time contract status and completion metrics
- **Ongoing Compliance**: Must use devlog for all project communications
- **Team Enforcement**: All agents responsible for maintaining SSOT

## Training Completion Tracking

### **Required Certifications**
- [ ] **SSOT Compliance Training** - Completed and certified
- [ ] **Devlog System Training** - Completed and certified 🆕
- [ ] **Messaging Etiquette Framework Training** - Completed and certified 🆕
- [ ] **Role-Specific Training** - Completed and certified
- [ ] **Practical Assessment** - Passed with 85% minimum

### **Validation Commands**
```bash
# Validate role and training completion
python scripts/onboarding/validate_phase2_roles.py [Agent-Name] "[Claimed-Role]"

# Check devlog system status
python -m src.core.devlog_cli status

# Test devlog functionality
python scripts/devlog.py "Training Test" "Testing devlog system" --agent "test-agent"
```

## Support and Resources

### **Training Support**
- **Devlog Training**: `docs/onboarding/DEVLOG_TRAINING_MODULE.md` 🆕
- **SSOT Training**: `docs/onboarding/SSOT_COMPLIANCE_TRAINING.md`
- **User Guide**: `docs/AGENT_DEVLOG_GUIDE.md`
- **System Overview**: `docs/DEVLOG_SYSTEM_FIXED.md`

### **Technical Support**
- **System Status**: `python -m src.core.devlog_cli status`
- **Help Commands**: `python scripts/devlog.py --help`
- **Full CLI Help**: `python -m src.core.devlog_cli --help`

### **Compliance Support**
- **SSOT Guide**: `docs/standards/SINGLE_SOURCE_OF_TRUTH_GUIDE.md`
- **Troubleshooting**: `docs/onboarding/troubleshooting_guide.md`
- **Best Practices**: `docs/onboarding/universal_development_principles.md`

## Next Steps

### **Immediate Actions**
1. **Complete mandatory training modules** (SSOT + Devlog)
2. **Get certified** in all required areas
3. **Start using devlog system** for all communications
4. **Enforce SSOT principles** in daily work

### **Ongoing Compliance**
1. **Use devlog for all updates** - no exceptions
2. **Maintain content standards** - clear and actionable
3. **Encourage team compliance** - lead by example
4. **Report compliance issues** - through devlog system

---

## 🎯 **SSOT Compliance Status**

**Current Status**: 🟢 **ACTIVE - TRAINING REQUIRED**  
**Next Milestone**: 🎯 **100% Agent Certification**  
**Compliance Goal**: 🏆 **Single Source of Truth Achieved**

**WE. ARE. SWARM!** 🚀

---

*This onboarding system ensures all agents understand and comply with SSOT principles, making the devlog system the single source of truth for team communication.*

