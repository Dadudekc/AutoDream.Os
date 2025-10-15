# 🧪 Discord Restart & Shutdown Commands - Test Plan

**Implementation:** Agent-6 (Co-Captain)  
**Spec:** Agent-2 (Architecture LEAD)  
**Date:** 2025-10-15  
**Status:** READY FOR TESTING  

---

## 🎯 TEST CASES (6 Total)

### **Test Case 1: !shutdown with Confirmation**

**Objective:** Verify shutdown works when user confirms

**Steps:**
1. Start Discord bot: `python run_unified_discord_bot_with_restart.py`
2. In Discord, type: `!shutdown`
3. Bot shows confirmation embed with buttons
4. Click "✅ Confirm Shutdown" button
5. Bot announces shutdown
6. Bot gracefully closes
7. Runner script exits cleanly

**Expected Result:**
- ✅ Bot stops
- ✅ No errors in logs
- ✅ Clean exit
- ✅ No restart (flag file not created)

**Status:** ⏳ PENDING

---

### **Test Case 2: !shutdown with Cancel**

**Objective:** Verify shutdown is cancelled when user cancels

**Steps:**
1. Start Discord bot
2. In Discord, type: `!shutdown`
3. Bot shows confirmation embed
4. Click "❌ Cancel" button
5. Bot announces cancellation
6. Bot continues running

**Expected Result:**
- ✅ Bot stays online
- ✅ "Shutdown cancelled" message shown
- ✅ No shutdown occurs
- ✅ Bot fully functional

**Status:** ⏳ PENDING

---

### **Test Case 3: !restart with Confirmation**

**Objective:** Verify restart works when user confirms

**Steps:**
1. Start Discord bot
2. In Discord, type: `!restart`
3. Bot shows confirmation embed
4. Click "🔄 Confirm Restart" button
5. Bot announces restart
6. Bot shuts down
7. Runner detects `.discord_bot_restart` flag
8. Runner waits 3 seconds
9. Bot automatically restarts
10. Bot comes back online

**Expected Result:**
- ✅ Bot restarts successfully
- ✅ Restart time < 10 seconds
- ✅ Bot fully functional after restart
- ✅ No errors in logs
- ✅ Flag file cleaned up

**Status:** ⏳ PENDING

---

### **Test Case 4: !restart with Cancel**

**Objective:** Verify restart is cancelled when user cancels

**Steps:**
1. Start Discord bot
2. In Discord, type: `!restart`
3. Bot shows confirmation embed
4. Click "❌ Cancel" button
5. Bot announces cancellation
6. Bot continues running

**Expected Result:**
- ✅ Bot stays online
- ✅ "Restart cancelled" message shown
- ✅ No restart occurs
- ✅ No flag file created
- ✅ Bot fully functional

**Status:** ⏳ PENDING

---

### **Test Case 5: Admin Permission Check**

**Objective:** Verify only admins can use commands

**Steps:**
1. Start Discord bot
2. As **admin user**, type: `!shutdown`
   - Should work (show confirmation)
3. As **non-admin user**, type: `!shutdown`
   - Should show permission error

**Expected Result:**
- ✅ Admins can execute commands
- ✅ Non-admins get permission error
- ✅ Error message is clear
- ✅ No security bypass possible

**Status:** ⏳ PENDING

---

### **Test Case 6: Timeout Handling**

**Objective:** Verify confirmation timeout works correctly

**Steps:**
1. Start Discord bot
2. Type: `!shutdown`
3. Bot shows confirmation
4. Wait 30 seconds without clicking
5. Confirmation buttons should timeout
6. No shutdown should occur

**Expected Result:**
- ✅ Timeout after 30 seconds
- ✅ Buttons become unclickable
- ✅ Bot stays running
- ✅ Clear timeout indication

**Status:** ⏳ PENDING

---

## 🚀 TESTING CHECKLIST

**Pre-Testing Setup:**
- [ ] Discord bot token configured in .env
- [ ] Bot invited to test Discord server
- [ ] Bot has admin permissions set up
- [ ] Test user has admin role
- [ ] Test user has non-admin role

**Test Execution:**
- [ ] Test Case 1: Shutdown with confirm
- [ ] Test Case 2: Shutdown with cancel
- [ ] Test Case 3: Restart with confirm
- [ ] Test Case 4: Restart with cancel
- [ ] Test Case 5: Admin permission check
- [ ] Test Case 6: Timeout handling

**Post-Testing:**
- [ ] All logs reviewed for errors
- [ ] Documentation updated with results
- [ ] Any bugs filed and fixed
- [ ] General/Captain notified of completion

---

## 📊 TEST RESULTS (Will Update After Testing)

**Test Case 1:**
- Result: ⏳ PENDING
- Notes:

**Test Case 2:**
- Result: ⏳ PENDING
- Notes:

**Test Case 3:**
- Result: ⏳ PENDING
- Notes:

**Test Case 4:**
- Result: ⏳ PENDING
- Notes:

**Test Case 5:**
- Result: ⏳ PENDING
- Notes:

**Test Case 6:**
- Result: ⏳ PENDING
- Notes:

---

## 🐛 KNOWN ISSUES

**Issue:** None yet (testing pending)

---

## ✅ SIGN-OFF

**Implementation Complete:** Agent-6  
**Testing Complete:** ⏳ PENDING  
**Architecture Review:** Agent-2 (LEAD)  
**Final Approval:** General (Discord commands requestor)  

---

**WE. ARE. SWARM.** 🐝⚡

**#DISCORD_COMMANDS #TESTING #GENERAL_REQUEST #URGENT_PRIORITY**

