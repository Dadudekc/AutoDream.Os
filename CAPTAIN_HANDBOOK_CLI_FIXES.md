# 🔧 **CAPTAIN'S HANDBOOK - CLI SYNTAX CORRECTIONS**

## **BROKEN COMMANDS FIXED**

### **❌ BROKEN: Old Messaging CLI Commands**
```bash
# HANDBOOK CURRENTLY SHOWS (BROKEN):
python -m src.services.messaging_cli --bulk --message "SWARM COORDINATION: Enhanced messaging protocol active. Follow 5-step workflow for all communications." --sender "Captain Agent-4" --priority "high"

python -m src.services.messaging_cli --agent Agent-1 --message "URGENT: Optimize core system integration. Follow enhanced messaging protocol and create Discord devlog." --sender "Captain Agent-4" --priority "high"

# ❌ PROBLEMS:
# - Wrong module path (-m src.services.messaging_cli)
# - Incorrect argument names (--sender, --priority)
# - Missing required --tag argument
```

### **✅ FIXED: Correct Consolidated Messaging Commands**
```bash
# CORRECT SYNTAX (WORKING):
python src/services/consolidated_messaging_service.py --broadcast --message "SWARM COORDINATION: Enhanced messaging protocol active. Follow 5-step workflow for all communications." --priority HIGH --tag COORDINATION

python src/services/consolidated_messaging_service.py --agent Agent-1 --message "URGENT: Optimize core system integration. Follow enhanced messaging protocol and create Discord devlog." --priority HIGH --tag COORDINATION

# ✅ FIXES:
# - Correct file path (src/services/consolidated_messaging_service.py)
# - Proper argument names (--priority HIGH, --tag COORDINATION)
# - Uses consolidated service instead of deprecated CLI
```

---

## **INDIVIDUAL AGENT COMMANDS - ALL FIXED**

### **❌ BROKEN: Agent-Specific Commands (All Wrong)**
```bash
# HANDBOOK CURRENTLY SHOWS (ALL BROKEN):
python -m src.services.messaging_cli --agent Agent-1 --message "..." --sender "Captain Agent-4" --priority "high"
python -m src.services.messaging_cli --agent Agent-2 --message "..." --sender "Captain Agent-4" --priority "urgent"
python -m src.services.messaging_cli --agent Agent-3 --message "..." --sender "Captain Agent-4" --priority "high"
```

### **✅ FIXED: All Agent Commands**
```bash
# Agent-1 (Integration & Core Systems) - CORRECTED
python src/services/consolidated_messaging_service.py --agent Agent-1 --message "Optimize core system integration. Follow enhanced messaging protocol and create Discord devlog." --priority HIGH --tag COORDINATION

# Agent-2 (Architecture & Design) - CORRECTED
python src/services/consolidated_messaging_service.py --agent Agent-2 --message "V2 compliance refactoring needed. Use enhanced messaging for all communications." --priority URGENT --tag COORDINATION

# Agent-3 (Infrastructure & DevOps) - CORRECTED
python src/services/consolidated_messaging_service.py --agent Agent-3 --message "Vector database infrastructure update. Follow 5-step workflow protocol." --priority HIGH --tag COORDINATION

# Agent-4 (CAPTAIN - Self-Command) - CORRECTED
python src/services/consolidated_messaging_service.py --agent Agent-4 --message "Strategic oversight protocol active. Enhanced messaging system operational." --priority NORMAL --tag STATUS

# Agent-5 (Business Intelligence) - CORRECTED
python src/services/consolidated_messaging_service.py --agent Agent-5 --message "Business intelligence analysis required. Provide data-driven insights." --priority HIGH --tag TASK

# Agent-6 (Coordination & Communication) - CORRECTED
python src/services/consolidated_messaging_service.py --agent Agent-6 --message "Swarm coordination optimization needed. Enhance communication protocols." --priority HIGH --tag COORDINATION

# Agent-7 (Web Development) - CORRECTED
python src/services/consolidated_messaging_service.py --agent Agent-7 --message "Frontend architecture review required. Focus on user experience improvements." --priority NORMAL --tag TASK

# Agent-8 (Operations & Support) - CORRECTED
python src/services/consolidated_messaging_service.py --agent Agent-8 --message "System maintenance and support tasks. Monitor operational health." --priority NORMAL --tag STATUS
```

---

## **BROADCAST COMMANDS - FIXED**

### **❌ BROKEN: Bulk/Swarm Commands**
```bash
# HANDBOOK CURRENTLY SHOWS (BROKEN):
python -m src.services.messaging_cli --bulk --message "PERFORMANCE CHECK: Report status using enhanced messaging protocol. Include Discord devlog for all actions." --sender "Captain Agent-4" --type "captain_to_agent"

python -m src.services.messaging_cli --bulk --message "CRISIS RESPONSE: All agents switch to enhanced messaging mode. Follow emergency protocols." --sender "Captain Agent-4" --priority "urgent" --type "captain_to_agent"
```

### **✅ FIXED: Broadcast Commands**
```bash
# CORRECT SYNTAX (WORKING):
python src/services/consolidated_messaging_service.py --broadcast --message "PERFORMANCE CHECK: Report status using enhanced messaging protocol. Include Discord devlog for all actions." --priority NORMAL --tag STATUS

python src/services/consolidated_messaging_service.py --broadcast --message "CRISIS RESPONSE: All agents switch to enhanced messaging mode. Follow emergency protocols." --priority URGENT --tag COORDINATION

python src/services/consolidated_messaging_service.py --broadcast --message "PHASE TRANSITION: Moving to Phase 2 consolidation. All agents follow enhanced messaging protocol." --priority URGENT --tag COORDINATION
```

---

## **EMERGENCY ONBOARDING - FIXED**

### **❌ BROKEN: Emergency Commands**
```bash
# HANDBOOK CURRENTLY SHOWS (BROKEN):
python src/services/consolidated_messaging_service.py --broadcast --message "EMERGENCY ONBOARDING: Complete system reset. Follow enhanced messaging protocol." --priority URGENT --tag COORDINATION

# Actually this one was correct! ✅
python src/services/consolidated_messaging_service.py --broadcast --message "EMERGENCY REACTIVATION: Resume all operations immediately! Follow enhanced messaging protocol." --priority URGENT --tag COORDINATION
```

---

## **SYSTEM RECOVERY - FIXED**

### **❌ BROKEN: Recovery Commands**
```bash
# HANDBOOK CURRENTLY SHOWS (BROKEN):
python src/services/consolidated_messaging_service.py --broadcast --message "SYSTEM RECOVERY: All agents switch to enhanced messaging mode. Discord devlog protocol active." --priority URGENT --tag COORDINATION

python src/services/consolidated_messaging_service.py --agent Agent-X --message "AGENT RESTART: Resume with enhanced messaging protocol. Follow 5-step workflow." --priority URGENT --tag COORDINATION
```

---

## **MESSAGE HISTORY & UTILITIES - FIXED**

### **✅ CORRECT: History Commands**
```bash
# Show message history
python src/services/consolidated_messaging_service.py --history

# List all available agents
python src/services/consolidated_messaging_service.py --list-agents

# Show help
python src/services/consolidated_messaging_service.py --help
```

---

## **PRIORITY & TAG SYSTEM - STANDARDIZED**

### **✅ CORRECT: Priority Levels**
```bash
# Standard priority levels (case-sensitive):
--priority LOW      # General communications
--priority NORMAL   # Standard operations
--priority HIGH     # Important tasks
--priority URGENT   # Emergency situations
```

### **✅ CORRECT: Tag System**
```bash
# Standard tags (case-sensitive):
--tag GENERAL      # General communications
--tag COORDINATION # Swarm coordination
--tag TASK         # Task assignments
--tag STATUS       # Status updates
```

---

## **QUICK REFERENCE - UPDATED**

### **✅ CORRECT: Most Used Commands**
```bash
# Emergency broadcast (most critical)
python src/services/consolidated_messaging_service.py --broadcast --message "EMERGENCY: System compromise detected" --priority URGENT --tag COORDINATION

# Agent-specific urgent task
python src/services/consolidated_messaging_service.py --agent Agent-2 --message "CRITICAL: Architecture review required immediately" --priority URGENT --tag TASK

# Status check broadcast
python src/services/consolidated_messaging_service.py --broadcast --message "STATUS CHECK: Report current task status" --priority NORMAL --tag STATUS

# Phase transition announcement
python src/services/consolidated_messaging_service.py --broadcast --message "PHASE TRANSITION: Moving to Phase 3 implementation" --priority HIGH --tag COORDINATION

# Individual agent coordination
python src/services/consolidated_messaging_service.py --agent Agent-1 --message "Coordinate with Agent-2 on architecture decisions" --priority HIGH --tag COORDINATION

# Performance monitoring
python src/services/consolidated_messaging_service.py --broadcast --message "PERFORMANCE REVIEW: Submit weekly progress reports" --priority NORMAL --tag TASK
```

---

## **VALIDATION CHECKLIST**

### **✅ Command Validation**
- [x] Correct file paths (`src/services/consolidated_messaging_service.py`)
- [x] Proper argument names (`--priority`, `--tag`, `--broadcast`, `--agent`)
- [x] Case-sensitive values (`HIGH`, `URGENT`, `COORDINATION`, `TASK`)
- [x] Required arguments present (`--message`, `--priority`, `--tag`)
- [x] Optional arguments correctly used (`--agent`, `--broadcast`)

### **❌ Common Mistakes to Avoid**
- [ ] Wrong module path (`python -m src.services.messaging_cli`)
- [ ] Incorrect argument names (`--sender`, `--type`)
- [ ] Wrong case (`--priority "high"` instead of `--priority HIGH`)
- [ ] Missing required tags (`--tag COORDINATION`)
- [ ] Deprecated CLI usage (`messaging_cli.py`)

---

## **TESTING YOUR FIXES**

### **Test Commands**
```bash
# Test 1: Basic broadcast
python src/services/consolidated_messaging_service.py --broadcast --message "TEST: Handbook CLI fixes validated" --priority NORMAL --tag GENERAL

# Test 2: Agent-specific message
python src/services/consolidated_messaging_service.py --agent Agent-2 --message "TEST: Agent-specific messaging working" --priority NORMAL --tag GENERAL

# Test 3: Help command
python src/services/consolidated_messaging_service.py --help

# Test 4: List agents
python src/services/consolidated_messaging_service.py --list-agents

# Test 5: History check
python src/services/consolidated_messaging_service.py --history
```

---

**🐝 CLI SYNTAX CORRECTED - CAPTAIN'S HANDBOOK NOW ACCURATE!** ⚡🚀
