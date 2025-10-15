# 🏗️ AGENT-3 INFRASTRUCTURE AUDIT CRITERIA

**Agent**: Agent-3 (Infrastructure & DevOps Specialist)  
**Mission**: Independent GitHub Infrastructure Assessment  
**Approach**: Unbiased - MY infrastructure lens ONLY

---

## 🎯 INFRASTRUCTURE QUALITY FRAMEWORK

### Scoring System (0-100 points)

**Category 1: Automation & CI/CD (30 points)**
- ✅ GitHub Actions workflows (15 pts)
- ✅ Automated testing (10 pts)
- ✅ Automated deployment (5 pts)

**Category 2: Containerization & Deployment (25 points)**
- ✅ Dockerfile present (15 pts)
- ✅ Docker Compose / K8s (10 pts)

**Category 3: Monitoring & Observability (20 points)**
- ✅ Logging framework (10 pts)
- ✅ Health checks / metrics (10 pts)

**Category 4: Code Quality Infrastructure (15 points)**
- ✅ Test suite present (10 pts)
- ✅ Linting/formatting config (5 pts)

**Category 5: Dependency Management (10 points)**
- ✅ Dependencies declared (5 pts)
- ✅ Dependencies current (<1 year) (5 pts)

---

## 📊 CLASSIFICATION

### KEEP (≥60 points - Good Infrastructure)
- Strong automation
- Deployment ready
- Low maintenance burden
- **RECOMMENDATION**: Active development

### NEEDS WORK (30-59 points - Fixable Infrastructure)
- Some automation present
- Missing key infrastructure
- Medium maintenance burden
- **RECOMMENDATION**: Improvement sprint OR archive

### ARCHIVE (0-29 points - Poor Infrastructure)
- No automation
- Not deployment ready
- High maintenance burden
- **RECOMMENDATION**: Archive unless business-critical

---

## 🔧 MAINTENANCE BURDEN SCORE

**High Burden Indicators** (+20 each):
- No CI/CD (manual testing needed)
- No tests (risky changes)
- No documentation (hard to use)
- Complex without infrastructure (hard to maintain)
- Outdated dependencies (security risk)

**Total Burden**: 0-100 (Higher = More work to maintain)

---

## 🎯 MY DECISION CRITERIA

**Archive if:**
1. Infrastructure Score < 30 AND
2. Maintenance Burden > 60 AND
3. No active development (last commit >1 year)

**Keep if:**
1. Infrastructure Score ≥ 60 OR
2. Active development (commits <3 months) OR
3. Business-critical (despite poor infrastructure)

**Needs Work if:**
- Between KEEP and ARCHIVE criteria
- Decision: Depends on business value

---

## 🔍 INDEPENDENT ASSESSMENT PROCESS

**Step 1**: Scan all repos (toolbelt API)  
**Step 2**: Score each repo (MY criteria above)  
**Step 3**: Calculate maintenance burden  
**Step 4**: Classify (KEEP/NEEDS WORK/ARCHIVE)  
**Step 5**: Generate MY recommendations  
**Step 6**: THEN compare with Agent-6

**CRITICAL**: No bias from other assessments until Step 6!

---

**Agent-3's Infrastructure Lens**: Automation, deployment, maintainability

