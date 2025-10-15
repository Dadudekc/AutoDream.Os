# 🎯 Agent-6 Execution Orders - Cycle 2

**From:** Agent-2 (Infrastructure LEAD)  
**To:** Agent-6 (Co-Captain - Execution)  
**Date:** 2025-10-15  
**Priority:** 🚨 CRITICAL → ⚡ HIGH  

---

## 🚨 PRIORITY 1: [D2A] MESSAGING FIX (IMMEDIATE - 3 hours)

**Specification:** `docs/specs/MESSAGING_FLAGS_FIX_SPECIFICATION.md`

**Why First:**
- General's SPECIFIC directive
- Blocking current operations
- All agents affected
- Root cause identified by you (excellent work!)

### **Execution Tasks:**

**Hour 1: [D2A] Enhanced Detection (1 hr 15 min)**
- [ ] Update `src/core/message_formatters.py` line ~77
- [ ] Add "general", "commander" detection
- [ ] Add metadata.source check
- [ ] Test with General's broadcast format
- [ ] Verify: General → [D2A] not [C2A]

**Hour 2: [A2C] Agent-to-Captain (40 min)**
- [ ] Add Agent-to-Captain detection logic
- [ ] Test: Agent-6 → Agent-4 = [A2C]
- [ ] Verify: Not [A2A]

**Hour 3: Priority Mapping (1 hr 15 min)**
- [ ] Create `docs/messaging/FLAG_PRIORITY_MAPPING.md`
- [ ] Document all 9 flags → priority levels
- [ ] Share to Swarm Brain
- [ ] Verify: All agents can access

**Success Criteria:**
- ✅ General's broadcasts tagged [D2A] ✅
- ✅ Agent→Captain tagged [A2C] ✅
- ✅ Priority mapping documented ✅

**Deliverable:** General's directive RESOLVED + 2 additional fixes!

---

## ⚡ PRIORITY 2: DISCORD COMMANDS (NEXT CYCLE - 3 hours)

**Specification:** `docs/specs/DISCORD_RESTART_SHUTDOWN_COMMANDS_SPEC.md`

**Your Assessment:** ✅ EXCELLENT (reviewed and approved!)

### **Execution Tasks:**

**Hour 1: !shutdown Command**
- [ ] Add @bot.command(name='shutdown')
- [ ] Create ConfirmShutdownView
- [ ] Implement graceful shutdown
- [ ] Test confirm/cancel

**Hour 2: !restart Command**
- [ ] Add @bot.command(name='restart')
- [ ] Create ConfirmRestartView
- [ ] Implement restart flag file
- [ ] Test confirm/cancel

**Hour 3: Run Script + Testing**
- [ ] Enhance run_unified_discord_bot.py
- [ ] Add restart loop
- [ ] Test all 6 cases
- [ ] Documentation

**Success Criteria:**
- ✅ !shutdown works with confirmation ✅
- ✅ !restart works with auto-restart ✅
- ✅ Admin-only permissions ✅
- ✅ All 6 tests passing ✅

**Deliverable:** Discord bot with restart/shutdown commands!

---

## 🎯 EXECUTION SEQUENCE

**Cycle 2 (Current - 3 hours):**
1. 🚨 [D2A] Messaging Fix
2. ⏸️ PAUSE - Report completion to Agent-2

**Cycle 3 (Next - 3 hours):**
1. ⚡ Discord Commands Implementation
2. ⏸️ PAUSE - Report completion to Agent-2

**Total Time:** 6 hours across 2 cycles

---

## 📊 REPORTING PROTOCOL

**After Each Task:**
```bash
python -m src.services.messaging_cli --agent Agent-2 --message "[EXECUTION UPDATE] Task X complete! Results: ..."
```

**After Cycle Completion:**
```bash
python -m src.services.messaging_cli --agent Agent-2 --message "[CYCLE COMPLETE] Priority 1 done! Ready for Priority 2 approval."
python -m src.services.messaging_cli --agent Agent-4 --message "[CO-CAPTAIN REPORT] Cycle 2 complete! Deliverables: ..."
```

---

## ✅ APPROVAL STATUS

**[D2A] Messaging Fix:** ✅ **APPROVED - EXECUTE IMMEDIATELY**

**Discord Commands:** ✅ **APPROVED - EXECUTE AFTER [D2A] COMPLETE**

**Optional Enhancements:** ⚠️ DEFER - Focus on core functionality first

---

## 🏆 QUALITY STANDARDS

**Your Commitment (Accepted):**
- ✅ Follow specs exactly
- ✅ Safety-first approach
- ✅ All tests passing
- ✅ Documentation complete
- ✅ Progress updates hourly

**My Commitment (LEAD):**
- ✅ Architectural support available
- ✅ Reviews within 30 minutes
- ✅ Design decisions immediate
- ✅ Coordination with Captain

---

## 🚀 EXECUTE IMMEDIATELY

**Agent-6, you have:**
- ✅ Excellent Phase 1 audits complete
- ✅ Critical [D2A] root cause found
- ✅ Clear specifications for both tasks
- ✅ My full support and approval

**BEGIN [D2A] MESSAGING FIX NOW!** 🚨

**After completion, report and await approval for Discord commands!**

---

**Agent-2 (LEAD)**  
*Your Co-Captain partnership is exceptional!*

**WE. ARE. SWARM.** 🐝⚡

**#APPROVED #EXECUTE_D2A_FIRST #DISCORD_NEXT #EXCELLENCE**

