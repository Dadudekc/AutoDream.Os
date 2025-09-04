/**
 * Chart State Orchestrator - V2 Compliant
 * Main orchestrator for chart state management
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

import { createChartStateCoreModule } from './chart-state-core-module.js';
import { createChartStateCallbacksModule } from './chart-state-callbacks-module.js';
import { createChartStateValidationModule } from './chart-state-validation-module.js';

// ================================
// CHART STATE ORCHESTRATOR
// ================================

/**
 * Main orchestrator for chart state management
 */
export class ChartStateOrchestrator {
    constructor() {
        this.logger = console;

        // Initialize modules
        this.coreModule = createChartStateCoreModule();
        this.callbacksModule = createChartStateCallbacksModule();
        this.validationModule = createChartStateValidationModule();
    }

    /**
     * Initialize orchestrator
     */
    initialize() {
        this.logger.log('📊 Initializing Chart State Orchestrator...');
        this.coreModule.initialize();
        this.logger.log('✅ Chart State Orchestrator initialized');
    }

    // ================================
    // STATE MANAGEMENT METHODS
    // ================================

    updateState(property, value) {
        // Validate value
        const validation = this.validationModule.validateProperty(property, value);
        if (!validation.valid) {
            this.logger.error(`State update validation failed: ${validation.error}`);
            return false;
        }

        // Sanitize value
        const sanitizedValue = this.validationModule.sanitizeValue(property, value);

        // Update state
        const oldState = this.coreModule.getState();
        const updated = this.coreModule.updateState(property, sanitizedValue);

        if (updated) {
            // Validate state transition
            const newState = this.coreModule.getState();
            const transitionValidation = this.validationModule.validateStateTransition(oldState, newState);

            if (!transitionValidation.valid) {
                // Rollback if transition is invalid
                this.coreModule.setState(oldState);
                this.logger.error(`State transition validation failed: ${transitionValidation.errors.join(', ')}`);
                return false;
            }

            // Trigger callbacks
            this.callbacksModule.triggerCallbacks('stateChange', {
                property,
                oldValue: oldState[property],
                newValue: sanitizedValue,
                fullState: newState
            });
        }

        return updated;
    }

    getState(property) {
        return this.coreModule.getState(property);
    }

    setState(newState) {
        // Validate new state
        const validation = this.validationModule.validateState(newState);
        if (!validation.valid) {
            this.logger.error(`State validation failed: ${validation.errors.join(', ')}`);
            return false;
        }

        // Sanitize state values
        const sanitizedState = {};
        for (const [key, value] of Object.entries(newState)) {
            sanitizedState[key] = this.validationModule.sanitizeValue(key, value);
        }

        const oldState = this.coreModule.getState();
        const updated = this.coreModule.setState(sanitizedState);

        if (updated) {
            // Validate state transition
            const transitionValidation = this.validationModule.validateStateTransition(oldState, sanitizedState);

            if (!transitionValidation.valid) {
                // Rollback if transition is invalid
                this.coreModule.setState(oldState);
                this.logger.error(`State transition validation failed: ${transitionValidation.errors.join(', ')}`);
                return false;
            }

            // Trigger callbacks
            this.callbacksModule.triggerCallbacks('stateChange', {
                oldState,
                newState: sanitizedState,
                transition: transitionValidation.transition
            });
        }

        return updated;
    }

    resetState() {
        const oldState = this.coreModule.getState();
        const reset = this.coreModule.resetState();

        if (reset) {
            this.callbacksModule.triggerCallbacks('stateReset', {
                oldState,
                newState: this.coreModule.getState()
            });
        }

        return reset;
    }

    // ================================
    // CALLBACK METHODS
    // ================================

    addCallback(event, callback) {
        return this.callbacksModule.addCallbackValidated(event, callback);
    }

    removeCallback(event, callback) {
        return this.callbacksModule.removeCallback(event, callback);
    }

    removeCallbackById(id) {
        return this.callbacksModule.removeCallbackById(id);
    }

    triggerCallbacks(event, data) {
        return this.callbacksModule.triggerCallbacks(event, data);
    }

    getCallbacksForEvent(event) {
        return this.callbacksModule.getCallbacksForEvent(event);
    }

    getAllCallbacks() {
        return this.callbacksModule.getAllCallbacks();
    }

    clearAllCallbacks() {
        return this.callbacksModule.clearAllCallbacks();
    }

    getCallbackStatistics() {
        return this.callbacksModule.getCallbackStatistics();
    }

    // ================================
    // VALIDATION METHODS
    // ================================

    validateProperty(property, value) {
        return this.validationModule.validateProperty(property, value);
    }

    validateState(state) {
        return this.validationModule.validateState(state || this.coreModule.getState());
    }

    validateStateTransition(oldState, newState) {
        return this.validationModule.validateStateTransition(
            oldState || this.coreModule.getState(),
            newState || this.coreModule.getState()
        );
    }

    sanitizeValue(property, value) {
        return this.validationModule.sanitizeValue(property, value);
    }

    addValidationRule(property, rule) {
        return this.validationModule.addValidationRule(property, rule);
    }

    removeValidationRule(property) {
        return this.validationModule.removeValidationRule(property);
    }

    getValidationRules() {
        return this.validationModule.getValidationRules();
    }

    // ================================
    // UTILITY METHODS
    // ================================

    getStateSummary() {
        return this.coreModule.getStateSummary();
    }

    validateStateIntegrity() {
        return this.coreModule.validateStateIntegrity();
    }

    // Convenience getters
    getChartData() { return this.coreModule.getChartData(); }
    setChartData(data) { return this.updateState('chartData', data); }
    getCurrentSymbol() { return this.coreModule.getCurrentSymbol(); }
    setCurrentSymbol(symbol) { return this.updateState('currentSymbol', symbol); }
    getCurrentTimeframe() { return this.coreModule.getCurrentTimeframe(); }
    setCurrentTimeframe(timeframe) { return this.updateState('currentTimeframe', timeframe); }
    getActiveIndicators() { return this.coreModule.getActiveIndicators(); }
    setActiveIndicators(indicators) { return this.updateState('indicators', indicators); }

    // ================================
    // STATISTICS METHODS
    // ================================

    getStatistics() {
        return {
            state: this.getStateSummary(),
            callbacks: this.getCallbackStatistics(),
            validation: this.validationModule.getValidationStatistics(),
            integrity: this.validateStateIntegrity(),
            timestamp: new Date().toISOString()
        };
    }

    getComprehensiveStatistics() {
        return {
            core: this.coreModule.getState(),
            callbacks: this.callbacksModule.getCallbackStatistics(),
            validation: this.validationModule.getValidationStatistics(),
            stateValidation: this.validateState(this.coreModule.getState()),
            timestamp: new Date().toISOString()
        };
    }

    // ================================
    // CLEANUP
    // ================================

    cleanup() {
        this.callbacksModule.cleanup();
        this.validationModule.cleanup();
        this.coreModule.cleanup();
        this.logger.log('💥 Chart State Orchestrator cleanup complete');
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy ChartStateModule class for backward compatibility
 * @deprecated Use ChartStateOrchestrator instead
 */
export class ChartStateModule extends ChartStateOrchestrator {
    constructor() {
        super();
        console.warn('[DEPRECATED] ChartStateModule is deprecated. Use ChartStateOrchestrator instead.');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create chart state orchestrator instance
 */
export function createChartStateOrchestrator() {
    const orchestrator = new ChartStateOrchestrator();
    orchestrator.initialize();
    return orchestrator;
}

/**
 * Create legacy chart state module (backward compatibility)
 */
export function createChartStateModule() {
    const module = new ChartStateModule();
    module.initialize();
    return module;
}

