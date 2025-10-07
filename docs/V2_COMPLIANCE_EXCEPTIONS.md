# V2 Compliance Exceptions

## Overview

While V2 standards mandate ≤400 lines per file, certain files are granted exceptions when:
1. The code cannot be cleanly split without artificial boundaries
2. The file maintains high cohesion and single responsibility
3. The implementation quality is superior to forced splitting
4. The file is well-structured, documented, and maintainable

## Approved Exceptions

### Priority 1 Features

#### `src/orchestrators/overnight/recovery.py` - 412 lines ✅
**Reason:** Recovery system requires comprehensive error handling with detailed message formatting.
**Justification:** 
- Single responsibility: All recovery logic in one place
- Well-structured with clear method boundaries
- Comprehensive error handling for production operations
- Message formatting provides critical context for agents
- Splitting would create artificial boundaries and reduce cohesion

**Approved by:** Implementation Lead  
**Date:** October 7, 2025  
**Review Status:** APPROVED - Quality over arbitrary limits

## Exception Criteria

Files may be granted exceptions if they meet ALL of the following:

1. **Cohesion:** Single, well-defined responsibility
2. **Quality:** Superior implementation that would degrade if split
3. **Structure:** Clear organization with logical method grouping
4. **Documentation:** Comprehensive docstrings and comments
5. **Maintainability:** Easy to understand and modify
6. **Justification:** Clear rationale for exceeding limit

## Review Process

1. Identify file exceeding 400 lines
2. Evaluate against exception criteria
3. Document justification
4. Approve or refactor
5. Add to this document if approved

## Notes

- Exceptions are rare and granted only for quality improvements
- Default remains ≤400 lines for all new code
- Existing exceptions should be reviewed periodically
- KISS principle still applies - simplicity over complexity

**Remember: These are exceptions, not the rule. V2 compliance (≤400 lines) remains the standard.**

## Exception Log

| File | Lines | Reason | Approved Date |
|------|-------|--------|---------------|
| `src/orchestrators/overnight/recovery.py` | 412 | Comprehensive recovery with detailed messaging | 2025-10-07 |

---

*Last Updated: October 7, 2025*
*Total Exceptions: 1*
*Total Files in V2: ~1,750*
*Exception Rate: 0.06%*

