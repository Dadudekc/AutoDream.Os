# 🎯 CONTRACT MANAGEMENT GUIDE - AGENT CELLPHONE V2

**For All Agents: How to Use the Automated Contract Management System**

---

## 🚀 **QUICK START**

### **1. Check Your Contracts**
```bash
# List all your contracts
python contract_cli.py list agent-1

# List all contracts in the system
python contract_cli.py list
```

### **2. Update Task Progress**
```bash
# Mark a requirement as completed
python contract_cli.py update TASK_1B task_completion true "Task completed successfully"

# Mark a requirement as not completed
python contract_cli.py update TASK_1B progress_documentation false "Still working on documentation"
```

### **3. Check Status & Validation**
```bash
# Check detailed status
python contract_cli.py status TASK_1B

# Validate completion
python contract_cli.py validate TASK_1B

# Show progress
python contract_cli.py progress TASK_1B
```

---

## 📋 **AVAILABLE COMMANDS**

### **📊 `list [agent_id]` - List Contracts**
Shows all contracts or contracts for a specific agent.

**Examples:**
```bash
python contract_cli.py list                    # All contracts
python contract_cli.py list agent-1            # Agent-1 contracts only
python contract_cli.py list agent-2            # Agent-2 contracts only
```

**Output:**
```
📋 CONTRACTS FOR AGENT-1:
⏳ TASK_1B: PENDING
   Progress: 0.0% (0/3)
   Agent: AGENT-1
   Last Updated: 2025-08-26T05:34:06
   Validation: ❌ Invalid (Score: 0.00)

🔄 TASK_1C: IN_PROGRESS
   Progress: 80.0% (2/3)
   Agent: AGENT-1
   Last Updated: 2025-08-26T05:30:00
   Validation: ❌ Invalid (Score: 0.67)
```

### **🎯 `status <contract_id>` - Detailed Status**
Shows comprehensive status of a specific contract.

**Examples:**
```bash
python contract_cli.py status TASK_1B
python contract_cli.py status TASK_2D
```

**Output:**
```
🎯 CONTRACT STATUS: TASK_1B
Agent: AGENT-1
Status: PENDING
Progress: 0.0% (0/3)
Last Updated: 2025-08-26T05:34:06

📊 VALIDATION RESULTS:
Valid: ❌ No
Score: 0.00

❌ MISSING REQUIREMENTS:
  - Complete the specific task based on current status
  - Document current progress and completion
  - Verify integration with existing completed systems
```

### **✅ `update <contract_id> <requirement_id> <completed> [notes]` - Update Requirements**
Updates the status of individual contract requirements.

**Parameters:**
- `contract_id`: The task ID (e.g., TASK_1B)
- `requirement_id`: The specific requirement to update
- `completed`: true/false, 1/0, yes/no, or y/n
- `notes`: Optional notes about the update

**Examples:**
```bash
# Mark task completion as done
python contract_cli.py update TASK_1B task_completion true "Workflow engine integration completed"

# Mark progress documentation as not done
python contract_cli.py update TASK_1B progress_documentation false "Still writing devlog"

# Mark integration verification as done
python contract_cli.py update TASK_1B integration_verification true "All systems integrated successfully"
```

**Available Requirement IDs:**
- `task_completion`: Complete the specific task
- `progress_documentation`: Document progress and completion
- `integration_verification`: Verify system integration
- `devlog_entry`: Create devlog entry
- `architecture_compliance`: Ensure V2 standards compliance

### **🔍 `validate <contract_id>` - Validate Completion**
Automatically validates contract completion and shows results.

**Examples:**
```bash
python contract_cli.py validate TASK_1B
python contract_cli.py validate TASK_2D
```

**Output:**
```
🔍 Validating contract TASK_1B...
❌ Contract TASK_1B is INVALID (Score: 0.67)

❌ Missing Requirements:
  - Complete the specific task based on current status
  - Document current progress and completion

⚠️  Warnings:
  - Some requirements lack completion timestamps
```

### **🚀 `complete <contract_id>` - Mark as Completed**
Automatically marks all requirements as completed.

**Examples:**
```bash
python contract_cli.py complete TASK_1B
python contract_cli.py complete TASK_2D
```

**Output:**
```
✅ Contract TASK_1B marked as completed successfully!
```

### **📊 `progress <contract_id>` - Show Progress**
Displays visual progress bar and detailed progress information.

**Examples:**
```bash
python contract_cli.py progress TASK_1B
python contract_cli.py progress TASK_2D
```

**Output:**
```
📊 PROGRESS REPORT: TASK_1B
Overall Progress: 66.7%
Requirements: 2/3
Progress Bar: [████████████████████░░░░░░░░] 66.7%
Status: 🔄 IN PROGRESS
Last Updated: 2025-08-26T05:35:00
```

### **🚨 `bounce <contract_id>` - Bounce Back for Review**
Bounces a contract back to the agent for review (Captain use only).

**Examples:**
```bash
python contract_cli.py bounce TASK_1B
python contract_cli.py bounce TASK_2D
```

**Output:**
```
🚨 Contract TASK_1B has been bounced back for review
Agent AGENT-1 will need to address issues and resubmit
```

---

## 🎯 **REQUIREMENT IDS EXPLAINED**

### **`task_completion`**
- **What it means**: The actual work described in the contract
- **Examples**: 
  - Complete workflow engine integration
  - Finish health system consolidation
  - Implement repository system
- **When to mark true**: When the core task is functionally complete

### **`progress_documentation`**
- **What it means**: Documenting your progress and completion
- **Examples**:
  - Update existing devlogs
  - Create progress reports
  - Document any cleanup tasks completed
- **When to mark true**: When documentation is complete

### **`integration_verification`**
- **What it means**: Ensuring your work integrates with existing systems
- **Examples**:
  - Test integration with existing components
  - Verify no duplication of functionality
  - Ensure V2 standards compliance
- **When to mark true**: When integration is verified

### **`devlog_entry`**
- **What it means**: Creating a proper devlog entry
- **Examples**:
  - Document task execution
  - Record any issues encountered
  - Note cleanup tasks completed
- **When to mark true**: When devlog is created

### **`architecture_compliance`**
- **What it means**: Following V2 architecture standards
- **Examples**:
  - Single Responsibility Principle
  - ≤200 LOC per module
  - Proper OOP patterns
- **When to mark true**: When V2 standards are verified

---

## 🚨 **GUARDRAILS & VALIDATION**

### **Automatic Status Updates**
The system automatically updates contract status based on validation:
- **PENDING**: 0-20% complete
- **IN_PROGRESS**: 20-80% complete
- **REVIEW_NEEDED**: 80-95% complete
- **COMPLETED**: 95-100% complete
- **BOUNCED_BACK**: Validation errors detected

### **Validation Scoring**
- **Score 0.0-0.5**: Contract bounced back
- **Score 0.5-0.8**: In progress
- **Score 0.8-0.95**: Review needed
- **Score 0.95-1.0**: Completed

### **Automatic Bounce-Back**
Contracts are automatically bounced back when:
- Required files are missing
- Critical requirements are incomplete
- Validation errors are detected
- Score falls below 0.5

---

## 📝 **WORKFLOW EXAMPLES**

### **Example 1: Starting a New Task**
```bash
# 1. Check your contracts
python contract_cli.py list agent-1

# 2. Check status of specific task
python contract_cli.py status TASK_1B

# 3. Start working on task completion
# ... do the work ...

# 4. Mark task completion as done
python contract_cli.py update TASK_1B task_completion true "Workflow engine integration completed"

# 5. Check progress
python contract_cli.py progress TASK_1B

# 6. Continue with other requirements...
```

### **Example 2: Completing a Task**
```bash
# 1. Mark all requirements as completed
python contract_cli.py update TASK_1B task_completion true "Task completed"
python contract_cli.py update TASK_1B progress_documentation true "Documentation complete"
python contract_cli.py update TASK_1B integration_verification true "Integration verified"

# 2. Validate completion
python contract_cli.py validate TASK_1B

# 3. Check final status
python contract_cli.py status TASK_1B
```

### **Example 3: Handling Bounced Contracts**
```bash
# 1. Check why contract was bounced
python contract_cli.py status TASK_1B

# 2. Address the issues shown in validation
# ... fix the problems ...

# 3. Re-validate
python contract_cli.py validate TASK_1B

# 4. Check if status improved
python contract_cli.py progress TASK_1B
```

---

## ⚠️ **IMPORTANT NOTES**

### **Always Run from Repository Root**
```bash
cd /path/to/Agent_Cellphone_V2_Repository
python contract_cli.py [command]
```

### **Use Descriptive Notes**
When updating requirements, provide clear notes:
```bash
# Good
python contract_cli.py update TASK_1B task_completion true "Workflow engine successfully integrated with FSM Core V2"

# Bad
python contract_cli.py update TASK_1B task_completion true "Done"
```

### **Check Status Regularly**
- Use `progress` command to monitor progress
- Use `validate` command before marking complete
- Address validation errors immediately

### **Don't Skip Requirements**
- All requirements must be completed for contract validation
- Missing requirements will cause contract to bounce back
- Each requirement contributes to overall score

---

## 🆘 **TROUBLESHOOTING**

### **"Contract not found" Error**
- Check contract ID spelling (e.g., TASK_1B not task_1b)
- Ensure you're running from repository root
- Verify contract exists in your agent's directory

### **"Requirement not found" Error**
- Check requirement ID spelling
- Use `status` command to see available requirements
- Ensure contract file exists and is readable

### **Import Errors**
- Make sure you're in the repository root directory
- Check that `src/core/task_management/contract_management_system.py` exists
- Verify Python path includes the src directory

### **Validation Always Fails**
- Check that all requirements are marked as completed
- Ensure contract file exists and is readable
- Look for validation errors in the output
- Address any missing requirements

---

## 🎯 **BEST PRACTICES**

### **1. Regular Updates**
- Update requirements as you complete them
- Don't wait until the end to mark everything complete

### **2. Clear Documentation**
- Provide descriptive notes for each update
- Document any issues or challenges encountered

### **3. Validation First**
- Always validate before marking complete
- Address validation errors immediately

### **4. Progress Monitoring**
- Use progress command to track advancement
- Monitor for any status changes

### **5. Communication**
- Report issues to Captain Agent-4
- Ask for clarification if requirements are unclear

---

## 🚀 **GETTING HELP**

### **Show Help**
```bash
python contract_cli.py help
python contract_cli.py --help
python contract_cli.py -h
```

### **Contact Captain**
- **Agent-4 (Captain)**: For contract clarification and issues
- **Co-Captain Agent-2**: For technical guidance and coordination

---

**Generated by**: Captain Agent-4 Contract Management System  
**Purpose**: Enable agents to efficiently manage contracts with automated validation  
**Status**: **READY FOR USE** 🚀
