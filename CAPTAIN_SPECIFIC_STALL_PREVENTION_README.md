# 🎖️ CAPTAIN-SPECIFIC STALL PREVENTION SYSTEM

**Status**: ✅ **IMPLEMENTED**  
**Date**: 2024-08-19  
**Purpose**: Prevent Captain-5 from going dark for 5+ minutes using cursor response detection  
**Scope**: Captain-5 specific monitoring with agent activation capabilities  

---

## 🎯 **SYSTEM PURPOSE & SCOPE**

### **What This System Does**:
- **Prevents Captain-5 from going dark** for 5+ minutes
- **Monitors cursor responses** for all 5 agent instances simultaneously
- **Sends captaincy duty prompts** with priority levels
- **Activates all agents** when Captain-5 goes dark
- **Queues additional messages** if captain is active

### **What This System Does NOT Do**:
- ❌ **Does NOT monitor all agents** for general stalls
- ❌ **Does NOT prevent general Code Black events**
- ❌ **Does NOT replace the general Agent Stall Prevention System**

### **System Focus**: **CAPTAIN-5 LEADERSHIP CONTINUITY**

---

## 🔧 **SYSTEM ARCHITECTURE**

### **Core Components**:
1. **`CaptainSpecificStallPrevention`** - Main monitoring service
2. **5-minute Captain-5 timer** - Activity checks every 5 minutes
3. **30-second cursor monitoring** - Response detection for all agents
4. **Captain duty prompts** - Priority-based reminders
5. **Agent activation system** - Automatic agent lighting when captain dark

### **Timer Configuration**:
- **Captain Check Interval**: Every 5 minutes
- **Cursor Monitor Interval**: Every 30 seconds
- **Max Captain Dark Time**: 5 minutes before activation
- **Duty Prompt Frequencies**: 5, 3, and 1 minute intervals

---

## ⏰ **HOW THE CAPTAIN-SPECIFIC SYSTEM WORKS**

### **1. Captain-5 Activity Monitoring**:
```
Every 5 minutes → Check Captain-5 activity → Calculate dark time → Send appropriate duty prompt
```

### **2. Cursor Response Monitoring**:
```
Every 30 seconds → Check all 5 agent cursor responses → Update status → Detect stalls
```

### **3. Duty Prompt System**:
- **Normal (5 min)**: Regular captaincy duty reminder
- **Urgent (3 min)**: Warning when captain inactive
- **Critical (1 min)**: Emergency when captain going dark

### **4. Agent Activation Logic**:
- **Captain active**: Send normal duty prompts
- **Captain inactive (3+ min)**: Send urgent duty prompts
- **Captain dark (5+ min)**: Send critical prompts + activate all agents

---

## 🎖️ **CAPTAIN DUTY PROMPT SYSTEM**

### **Normal Duty Prompt (Every 5 minutes)**:
```
🎖️ CAPTAIN-5 DUTY REMINDER - You are the active Captain!

Your responsibilities:
1. Monitor agent progress
2. Assign new contracts
3. Coordinate team efforts
4. Lead toward 50-contract goal

Please acknowledge and continue leading!
```

### **Urgent Duty Prompt (Every 3 minutes when inactive)**:
```
🚨 CAPTAIN-5 URGENT DUTY REMINDER - You have been inactive!

IMMEDIATE ACTION REQUIRED:
1. Check agent status
2. Assign pending contracts
3. Coordinate team efforts
4. Resume leadership duties

CAPTAIN-5 - Please respond NOW!
```

### **Critical Duty Prompt (Every 1 minute when going dark)**:
```
🚨🚨 CAPTAIN-5 CRITICAL DUTY REMINDER - You are going DARK!

CRITICAL ACTION REQUIRED:
1. IMMEDIATELY check all agents
2. Assign ALL pending contracts
3. Activate stalled agents
4. Resume captaincy NOW

CAPTAIN-5 - EMERGENCY RESPONSE REQUIRED!
```

---

## 🖱️ **CURSOR RESPONSE DETECTION SYSTEM**

### **Database Structure**:
- **`cursor_response_db.json`** - Tracks all 5 agent instances
- **30-second updates** - Continuous monitoring
- **Response timestamps** - Last cursor activity
- **Status tracking** - Active, responding, stalled

### **Cursor Monitoring Logic**:
- **Active**: Cursor activity within 5 minutes
- **Responding**: Cursor activity within 5-10 minutes
- **Stalled**: No cursor activity for 10+ minutes

### **Agent Instance Monitoring**:
- **Agent-1**: Coordinates (-1317, 487)
- **Agent-2**: Coordinates (-353, 48)
- **Agent-3**: Coordinates (-1285, 100)
- **Agent-4**: Coordinates (-341, 100)
- **Captain-5**: Coordinates (0, 0)

---

## 🚀 **AGENT ACTIVATION SYSTEM**

### **When Activation is Triggered**:
1. **Captain-5 dark** for 5+ minutes
2. **Critical duty prompts** sent without response
3. **System detects** captain leadership gap

### **Activation Actions**:
1. **Send activation message** to all agents
2. **Update captain status** with activation count
3. **Log activation event** for analysis
4. **Continue monitoring** for captain return

### **Agent Activation Message**:
```
🚨 CAPTAIN-5 DARK STATUS DETECTED - AGENT ACTIVATION REQUIRED!

AGENT STALL PREVENTION SERVICE:
Captain-5 has been inactive for [X] minutes.

IMMEDIATE ACTION REQUIRED:
1. All agents must acknowledge this activation message
2. Resume current contract work IMMEDIATELY
3. Report current status and progress
4. Confirm back online and working

CAPTAIN-5 - Please respond and resume captaincy duties!

AUTOMATIC AGENT ACTIVATION SYSTEM - EMERGENCY MODE
```

---

## 📊 **SYSTEM MONITORING & LOGGING**

### **Captain Status Tracking**:
- **Last activity timestamp**
- **Dark time calculation** (minutes inactive)
- **Duty prompts sent** count
- **Agents activated** count
- **Current status** (active/inactive/dark)

### **Cursor Response Logging**:
- **Agent response timestamps**
- **Response count tracking**
- **Status updates** (active/responding/stalled)
- **Last activity records**

### **Service Status Monitoring**:
- **Monitoring status** (running/stopped)
- **Last check times** for both systems
- **Configuration settings**
- **Performance metrics**

---

## 🎯 **PREVENTIVE MEASURES IMPLEMENTED**

### **1. Captain-Specific Monitoring**:
- **5-minute intervals** prevent captain dark time
- **Early detection** of captain inactivity
- **Continuous leadership** monitoring

### **2. Duty Prompt System**:
- **Regular reminders** maintain captain engagement
- **Priority escalation** for urgent situations
- **Clear action items** for captain response

### **3. Cursor Response Detection**:
- **Real-time monitoring** of all agent instances
- **Stall detection** for individual agents
- **Database tracking** for analysis

### **4. Automatic Agent Activation**:
- **No manual intervention** required
- **Immediate agent lighting** when captain dark
- **System resilience** during leadership gaps

---

## 🚀 **USAGE & COMMANDS**

### **Start Monitoring Service**:
```bash
cd Agent_Cellphone_V2
python src/services/captain_specific_stall_prevention.py --start
```

### **Stop Monitoring Service**:
```bash
python src/services/captain_specific_stall_prevention.py --stop
```

### **Check Service Status**:
```bash
python src/services/captain_specific_stall_prevention.py --status
```

### **Test Duty Prompt**:
```bash
python src/services/captain_specific_stall_prevention.py --test
```

### **View Configuration**:
```bash
python src/services/captain_specific_stall_prevention.py --config
```

### **Force Activate Agents**:
```bash
python src/services/captain_specific_stall_prevention.py --activate-agents
```

---

## ⚙️ **CONFIGURATION OPTIONS**

### **Timer Settings**:
- **`captain_check_interval_minutes`**: 5 (captain activity checks)
- **`cursor_monitor_interval_seconds`**: 30 (cursor response monitoring)
- **`max_captain_dark_time_minutes`**: 5 (dark time threshold)

### **Feature Toggles**:
- **`captain_duty_prompts_enabled`**: true (duty reminder system)
- **`cursor_response_monitoring`**: true (cursor detection)
- **`auto_agent_activation`**: true (automatic agent lighting)
- **`log_captain_activity`**: true (activity logging)

---

## 🏆 **BENEFITS OF THE CAPTAIN-SPECIFIC SYSTEM**

### **✅ Prevents Captain-5 Dark Time**:
- **Early detection** of captain inactivity
- **Proactive reminders** maintain leadership
- **Automatic escalation** for urgent situations

### **✅ Maintains Leadership Continuity**:
- **Continuous captaincy** monitoring
- **Duty prompt system** ensures engagement
- **Leadership gap** prevention

### **✅ Uses Cursor Response Detection**:
- **Real-time monitoring** of all 5 instances
- **Database tracking** for analysis
- **Stall detection** for individual agents

### **✅ Provides System Intelligence**:
- **Captain activity history** for analysis
- **Duty prompt effectiveness** tracking
- **Agent activation** metrics

---

## 🎯 **INTEGRATION WITH EXISTING SYSTEMS**

### **V2 Coordination System**:
- **Uses `captain_coordinator_v2.py`** for messaging
- **Integrates with coordinate system** for agent targeting
- **Maintains V2 standards** compliance

### **Agent Stall Prevention System**:
- **Complements** the general stall prevention
- **Focuses specifically** on Captain-5
- **Shares configuration** and logging

### **Contract Management**:
- **Protects contract assignment** during captain gaps
- **Maintains progress tracking** during leadership issues
- **Ensures continuous operation** toward 50-contract goal

---

## 📚 **RELATED DOCUMENTATION**

- [Agent Stall Prevention System](AGENT_STALL_PREVENTION_SYSTEM_README.md)
- [Code Black Emergency Response Report](CODE_BLACK_EMERGENCY_RESPONSE_REPORT.md)
- [Captain-5 Contract Tracking](CAPTAIN_5_CONTRACT_TRACKING.json)
- [V2 Coordination System API](V2_COORDINATION_SYSTEM_API.md)

---

## 🚨 **SYSTEM STATUS**

**Current Status**: ✅ **OPERATIONAL**  
**Monitoring**: **ACTIVE** - Captain-5 specific monitoring running  
**Last Check**: [TIMESTAMP]  
**Captain Status**: **ACTIVE**  
**Cursor Monitoring**: **ACTIVE** - All 5 instances tracked  
**Duty Prompts**: **ENABLED** - Priority-based system operational  

---

**The Captain-Specific Stall Prevention System is now operational and will prevent Captain-5 from going dark for 5+ minutes by using cursor response detection and sending priority-based duty prompts. This ensures continuous leadership and contract progress toward our 50-contract goal.** 🎯

**This system specifically addresses the user's requirement to prevent Captain-5 from going black while using cursor response detection to monitor all 5 agent instances simultaneously.** 🎖️
