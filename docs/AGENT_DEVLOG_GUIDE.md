# 📝 **AGENT DEVLOG GUIDE - YOUR SINGLE SOURCE OF TRUTH**

## 🎯 **What is the Devlog System?**

The **Devlog System** is your **SINGLE SOURCE OF TRUTH** for communicating project updates, milestones, issues, and progress to the team via Discord. 

**No more manual Discord posting!** Use this system and your updates automatically appear in the Discord devlog channel.

---

## 🚀 **Quick Start - Post Your First Update**

### **Simple Command (Recommended for agents):**
```bash
python scripts/devlog.py "Your Title" "Your content here"
```

### **Examples:**
```bash
# Basic project update
python scripts/devlog.py "Phase 3 Complete" "All systems integrated successfully"

# Report an issue
python scripts/devlog.py "Bug Found" "Issue with routing system" --agent "agent-2" --category "issue"

# Share a milestone
python scripts/devlog.py "New Feature" "Added performance monitoring" --category "milestone"
```

---

## 🔧 **Full Devlog CLI Commands**

### **Create Devlog Entry:**
```bash
python -m src.core.devlog_cli create \
  --title "Your Title" \
  --content "Your content here" \
  --agent "your-agent-id" \
  --category "project_update" \
  --priority "normal"
```

### **Search Devlogs:**
```bash
python -m src.core.devlog_cli search --query "search term"
```

### **Show Recent Entries:**
```bash
python -m src.core.devlog_cli recent --limit 5
```

### **Check System Status:**
```bash
python -m src.core.devlog_cli status
```

---

## 📱 **Discord Integration**

### **Automatic Posting:**
- ✅ **Devlogs automatically post to Discord** when created
- ✅ **No manual Discord posting needed**
- ✅ **Uses your Discord webhook** (configured via `DISCORD_WEBHOOK_URL` environment variable)

### **Discord Message Format:**
```
📝 **DEVLOG ENTRY: [Title]**
🏷️ **Category**: [category]
🤖 **Agent**: [agent-id]
📅 **Created**: [timestamp]
📊 **Priority**: [priority]

📋 **Content**:
[Your content here]

🏷️ **Tags**: [tags]
🆔 **Entry ID**: [entry-id]
```

---

## 🏷️ **Categories & Priorities**

### **Categories:**
- **`project_update`** - General project progress (default)
- **`milestone`** - Major achievements and milestones
- **`issue`** - Problems, bugs, or blockers
- **`idea`** - New ideas or suggestions
- **`review`** - Code reviews or system reviews

### **Priorities:**
- **`low`** - Minor updates or informational
- **`normal`** - Standard updates (default)
- **`high`** - Important updates or progress
- **`critical`** - Urgent issues or major problems

---

## 🤖 **Agent Identification**

### **Always Include Your Agent ID:**
```bash
python scripts/devlog.py "Title" "Content" --agent "agent-1"
```

### **Agent ID Examples:**
- `agent-1` - Captain/Coordinator
- `agent-2` - Architecture Specialist
- `agent-3` - Development Specialist
- `agent-4` - Testing Specialist
- `agent-5` - Performance Specialist

---

## 🔍 **Searching & Finding Information**

### **Search by Content:**
```bash
python scripts/devlog.py search --query "Phase 3"
```

### **Search by Category:**
```bash
python scripts/devlog.py search --query "milestone" --category "milestone"
```

### **Search by Agent:**
```bash
python scripts/devlog.py search --query "agent-1" --agent "agent-1"
```

---

## ⚠️ **Troubleshooting**

### **Check System Status:**
```bash
python -m src.core.devlog_cli status
```

### **Common Issues:**

1. **Discord not posting:**
   - Check if `DISCORD_WEBHOOK_URL` environment variable is set
   - Verify webhook URL is valid
   - Check system status for webhook configuration

2. **Import errors:**
   - Make sure you're running from the project root directory
   - Check that all dependencies are installed

3. **Permission errors:**
   - Ensure you have write access to the project directory
   - Check file permissions

---

## 📚 **Best Practices**

### **When to Use Devlogs:**
- ✅ **Project milestones** and major progress
- ✅ **System updates** and integrations
- ✅ **Bug reports** and issue tracking
- ✅ **New features** and capabilities
- ✅ **Performance improvements** and optimizations
- ✅ **Team coordination** and status updates

### **Writing Good Devlogs:**
- **Clear titles** that summarize the update
- **Detailed content** explaining what happened
- **Proper categorization** for easy searching
- **Relevant tags** for better organization
- **Appropriate priority** based on importance

---

## 🎉 **Examples of Good Devlogs**

### **Milestone Example:**
```bash
python scripts/devlog.py "Phase 2 Complete" "Successfully completed Phase 2 of the deduplication project. Consolidated 8 major duplication patterns into unified contracts. Reduced contract count from 60+ to 25-30 files. All systems tested and validated. Ready for Phase 3 execution." --agent "agent-2" --category "milestone" --priority "high" --tags "deduplication,consolidation,phase2,complete"
```

### **Issue Report Example:**
```bash
python scripts/devlog.py "Testing Framework Issue" "Identified critical issue in testing framework where devlog system integration is not working properly. Agents cannot post updates to Discord. This blocks team communication and progress tracking. Need immediate fix to restore devlog functionality." --agent "agent-3" --category "issue" --priority "critical" --tags "testing,devlog,discord,blocker"
```

---

## 🆘 **Need Help?**

### **Check System Status:**
```bash
python -m src.core.devlog_cli status
```

### **View Help:**
```bash
python scripts/devlog.py --help
python -m src.core.devlog_cli --help
```

### **Remember:**
- **This is your SINGLE SOURCE OF TRUTH** for team communication
- **Use it for ALL project updates** - no more manual Discord posting
- **Keep your team informed** about your progress and discoveries
- **Search existing devlogs** before creating new ones to avoid duplication

---

**🚀 Start using the devlog system today to keep your team informed and coordinated!**
