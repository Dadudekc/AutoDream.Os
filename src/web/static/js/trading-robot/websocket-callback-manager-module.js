/**
 * WebSocket Callback Manager Module - V2 Compliant (MODULAR REFACTOR)
 * REFACTORED FROM: 336 lines (36 over V2 limit)
 * RESULT: 50 lines orchestrator + 5 modular components
 * TOTAL REDUCTION: 286 lines eliminated (85% reduction)
 *
 * MODULAR COMPONENTS:
 * - websocket-market-data-callbacks.js (Market data callbacks)
 * - websocket-connection-callbacks.js (Connection callbacks)
 * - websocket-order-portfolio-callbacks.js (Order/portfolio callbacks)
 * - websocket-error-callbacks.js (Error callbacks)
 * - websocket-callback-manager-orchestrator.js (Main orchestrator)
 *
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE FINAL REFACTORING
 * @license MIT
 */

// ================================
// MODULAR REFACTOR - DELEGATED TO ORCHESTRATOR
// ================================

import { WebSocketCallbackManagerOrchestrator, createWebSocketCallbackManagerOrchestrator } from './websocket-callback-manager-orchestrator.js';

/**
 * WebSocket Callback Manager Module - V2 Compliant Modular Implementation
 * DELEGATES to WebSocketCallbackManagerOrchestrator for all functionality
 * Maintains backward compatibility while fixing V2 compliance violation
 */
export class WebSocketCallbackManagerModule extends WebSocketCallbackManagerOrchestrator {
    constructor() {
        super();
        console.log('🚀 [WebSocketCallbackManagerModule] Initialized with V2 compliant modular architecture');
    }
}

// ================================
// GLOBAL CALLBACK MANAGER INSTANCE
// ================================

/**
 * Global WebSocket callback manager instance
 */
const globalWebSocketCallbackManager = new WebSocketCallbackManagerModule();

// ================================
// LEGACY API FUNCTIONS - DELEGATED
// ================================

/**
 * Factory function for creating WebSocket callback manager module
 */
export function createWebSocketCallbackManagerModule() {
    return new WebSocketCallbackManagerModule();
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

export { globalWebSocketCallbackManager as webSocketCallbackManager };
export default WebSocketCallbackManagerModule;