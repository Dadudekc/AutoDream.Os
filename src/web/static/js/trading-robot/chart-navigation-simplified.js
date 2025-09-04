/**
 * Chart Navigation Simplified - V2 Compliant
 * Simplified orchestrator for chart navigation functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE SIMPLIFICATION
 * @license MIT
 */

import { createChartNavigationModule } from './chart-navigation-module.js';

// ================================
// CHART NAVIGATION SIMPLIFIED ORCHESTRATOR
// ================================

/**
 * Simplified orchestrator for chart navigation functionality
 */
export class ChartNavigationSimplified {
    constructor() {
        this.logger = console;
        this.navigationModule = createChartNavigationModule();
        this.callbacks = {};
    }

    /**
     * Initialize simplified chart navigation
     */
    initialize(canvas) {
        this.logger.log('🧭 Initializing Chart Navigation Simplified...');

        // Setup callbacks
        const navigationCallbacks = {
            onZoom: (zoomLevel) => this.handleZoom(zoomLevel),
            onPan: (panOffset) => this.handlePan(panOffset),
            onReset: () => this.handleReset(),
            onResize: (width, height) => this.handleResize(width, height),
            onFullscreenToggle: (isFullscreen) => this.handleFullscreenToggle(isFullscreen),
            onCrosshairMove: (x, y) => this.handleCrosshairMove(x, y)
        };

        this.navigationModule.initialize(canvas, navigationCallbacks);
        this.logger.log('✅ Chart Navigation Simplified initialized');
    }

    /**
     * Handle zoom events
     */
    handleZoom(zoomLevel) {
        if (this.callbacks.onZoom) {
            this.callbacks.onZoom(zoomLevel);
        }
    }

    /**
     * Handle pan events
     */
    handlePan(panOffset) {
        if (this.callbacks.onPan) {
            this.callbacks.onPan(panOffset);
        }
    }

    /**
     * Handle reset events
     */
    handleReset() {
        if (this.callbacks.onReset) {
            this.callbacks.onReset();
        }
    }

    /**
     * Handle resize events
     */
    handleResize(width, height) {
        if (this.callbacks.onResize) {
            this.callbacks.onResize(width, height);
        }
    }

    /**
     * Handle fullscreen toggle events
     */
    handleFullscreenToggle(isFullscreen) {
        if (this.callbacks.onFullscreenToggle) {
            this.callbacks.onFullscreenToggle(isFullscreen);
        }
    }

    /**
     * Handle crosshair move events
     */
    handleCrosshairMove(x, y) {
        if (this.callbacks.onCrosshairMove) {
            this.callbacks.onCrosshairMove(x, y);
        }
    }

    // ================================
    // NAVIGATION METHODS - DELEGATED
    // ================================

    zoomChart(delta) {
        return this.navigationModule.zoomChart(delta);
    }

    panChart(deltaX) {
        return this.navigationModule.panChart(deltaX);
    }

    resetChart() {
        return this.navigationModule.resetChart();
    }

    toggleFullscreen() {
        return this.navigationModule.toggleFullscreen();
    }

    toggleCrosshair() {
        return this.navigationModule.toggleCrosshair();
    }

    navigateToTimeRange(startTime, endTime) {
        return this.navigationModule.navigateToTimeRange(startTime, endTime);
    }

    centerOnDataPoint(dataPoint) {
        return this.navigationModule.centerOnDataPoint(dataPoint);
    }

    // ================================
    // GETTER METHODS
    // ================================

    getZoomLevel() {
        return this.navigationModule.getZoomLevel();
    }

    getPanOffset() {
        return this.navigationModule.getPanOffset();
    }

    isFullscreenMode() {
        return this.navigationModule.isFullscreenMode();
    }

    isCrosshairEnabled() {
        return this.navigationModule.isCrosshairEnabled();
    }

    getNavigationState() {
        return this.navigationModule.getNavigationState();
    }

    setNavigationState(state) {
        return this.navigationModule.setNavigationState(state);
    }

    setNavigationEnabled(enabled) {
        return this.navigationModule.setNavigationEnabled(enabled);
    }

    // ================================
    // CALLBACK SETUP
    // ================================

    setCallbacks(callbacks) {
        this.callbacks = { ...this.callbacks, ...callbacks };
    }

    addCallback(event, callback) {
        this.callbacks[event] = callback;
    }

    removeCallback(event) {
        delete this.callbacks[event];
    }

    // ================================
    // CLEANUP
    // ================================

    cleanup() {
        if (this.navigationModule) {
            this.navigationModule.cleanup();
        }
        this.callbacks = {};
        this.logger.log('🧹 Chart Navigation Simplified cleanup complete');
    }

    // ================================
    // STATUS METHODS
    // ================================

    getStatus() {
        return {
            initialized: true,
            zoomLevel: this.getZoomLevel(),
            panOffset: this.getPanOffset(),
            isFullscreen: this.isFullscreenMode(),
            crosshairEnabled: this.isCrosshairEnabled(),
            callbacksConfigured: Object.keys(this.callbacks).length,
            timestamp: new Date().toISOString()
        };
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy ChartNavigationModule class for backward compatibility
 * @deprecated Use ChartNavigationSimplified instead
 */
export class ChartNavigationModule extends ChartNavigationSimplified {
    constructor() {
        super();
        console.warn('[DEPRECATED] ChartNavigationModule is deprecated. Use ChartNavigationSimplified instead.');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create simplified chart navigation instance
 */
export function createChartNavigationSimplified(canvas) {
    const navigation = new ChartNavigationSimplified();
    if (canvas) {
        navigation.initialize(canvas);
    }
    return navigation;
}

/**
 * Create legacy chart navigation module (backward compatibility)
 */
export function createChartNavigationModule() {
    return new ChartNavigationModule();
}

