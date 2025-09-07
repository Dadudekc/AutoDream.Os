# 🚨 PROMPTS DIRECTORY - CUSTOMIZABLE MESSAGE SYSTEM 🚨

**Purpose:** Centralized location for all customizable prompts and messages used by the Captain and agent onboarding system.

## 📁 **DIRECTORY STRUCTURE:**

```
prompts/
├── README.md                           # This file
├── captain/                            # Captain-specific prompts
│   ├── onboarding.md                   # Captain onboarding instructions
│   ├── auto_resume.md                  # --auto flag resume messages
│   ├── stall_detection.md              # Stall detection alerts
│   └── system_oversight.md             # System oversight commands
├── agents/                             # Agent-specific prompts
│   ├── onboarding_template.md          # Agent onboarding template
│   ├── activation.md                   # Agent activation messages
│   ├── resume.md                       # Resume workflow prompts
│   └── feedback_loop.md                # Feedback loop instructions
└── system/                             # System-wide prompts
    ├── emergency.md                    # Emergency protocols
    ├── coordination.md                  # Cross-agent coordination
    └── status_update.md                # Status update requirements
```

## 🔧 **USAGE:**

1. **Edit any prompt file** to customize messages
2. **Captain system reads** from these files
3. **--auto flag uses** these customizable prompts
4. **Easy tweaking** without code changes

## 🎯 **QUICK START:**

- **Modify prompts** in their respective files
- **Save changes** to update message content
- **System automatically uses** updated prompts
- **No restart required** - changes take effect immediately

**Captain Agent-4 - Prompts Directory System Ready for Customization!**
