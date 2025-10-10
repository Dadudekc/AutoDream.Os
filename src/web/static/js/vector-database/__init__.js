/**
 * Vector Database Web Interface - V2 Compliant Modular Architecture
 * ================================================================
 *
 * Modular vector database web interface with clean separation of concerns.
 * Each module handles a specific aspect of the interface.
 *
 * V2 Compliance: < 300 lines per module, single responsibility.
 *
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export { VectorDatabaseCore } from './core.js';
export { VectorDatabaseUIOptimized as VectorDatabaseUI } from './ui-optimized.js';
export { VectorDatabaseSearch } from './search.js';
export { VectorDatabaseAnalytics } from './analytics.js';
export { VectorDatabaseManager } from './manager.js';
export {
    setupSearchInterface,
    setupDocumentManagement,
    showError,
    showSuccess,
    escapeHtml
} from './ui-common.js';
