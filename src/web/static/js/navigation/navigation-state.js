/**
 * Navigation State Module - V2 Compliant
 * Manages navigation state and current view tracking
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class NavigationState {
    constructor(initialView = 'overview') {
        this.currentView = initialView;
        this.previousView = null;
        this.viewHistory = [initialView];
        this.maxHistorySize = 10;
        this.viewMetadata = new Map();
        this.stateListeners = new Set();
    }

    /**
     * Set current view
     */
    setCurrentView(view, metadata = {}) {
        try {
            if (this.currentView === view) {
                console.log(`Navigation: View '${view}' is already current`);
                return false;
            }

            this.previousView = this.currentView;
            this.currentView = view;

            // Add to history
            this.addToHistory(view);

            // Store metadata
            if (Object.keys(metadata).length > 0) {
                this.viewMetadata.set(view, {
                    ...metadata,
                    timestamp: Date.now()
                });
            }

            // Notify listeners
            this.notifyStateChange();

            console.log(`Navigation: Changed to view '${view}'`);
            return true;
        } catch (error) {
            console.error('Failed to set current view:', error);
            return false;
        }
    }

    /**
     * Get current view
     */
    getCurrentView() {
        return this.currentView;
    }

    /**
     * Get previous view
     */
    getPreviousView() {
        return this.previousView;
    }

    /**
     * Check if view exists in history
     */
    hasViewInHistory(view) {
        return this.viewHistory.includes(view);
    }

    /**
     * Get view history
     */
    getViewHistory() {
        return [...this.viewHistory];
    }

    /**
     * Get view metadata
     */
    getViewMetadata(view) {
        return this.viewMetadata.get(view) || {};
    }

    /**
     * Clear view history
     */
    clearHistory() {
        try {
            this.viewHistory = [this.currentView];
            this.previousView = null;
            this.viewMetadata.clear();
            console.log('Navigation history cleared');
            return true;
        } catch (error) {
            console.error('Failed to clear navigation history:', error);
            return false;
        }
    }

    /**
     * Go back to previous view
     */
    goBack() {
        try {
            if (!this.previousView) {
                console.warn('No previous view available');
                return false;
            }

            const targetView = this.previousView;
            this.previousView = this.viewHistory[this.viewHistory.length - 2] || null;

            // Remove current from history and add target
            this.viewHistory.pop();
            this.currentView = targetView;

            this.notifyStateChange();

            console.log(`Navigation: Went back to view '${targetView}'`);
            return true;
        } catch (error) {
            console.error('Failed to go back:', error);
            return false;
        }
    }

    /**
     * Add view to history
     */
    addToHistory(view) {
        try {
            // Remove if already exists (move to end)
            const existingIndex = this.viewHistory.indexOf(view);
            if (existingIndex > -1) {
                this.viewHistory.splice(existingIndex, 1);
            }

            // Add to end
            this.viewHistory.push(view);

            // Maintain max history size
            if (this.viewHistory.length > this.maxHistorySize) {
                const removedView = this.viewHistory.shift();
                this.viewMetadata.delete(removedView);
            }
        } catch (error) {
            console.error('Failed to add view to history:', error);
        }
    }

    /**
     * Add state change listener
     */
    addStateListener(listener) {
        this.stateListeners.add(listener);
    }

    /**
     * Remove state change listener
     */
    removeStateListener(listener) {
        this.stateListeners.delete(listener);
    }

    /**
     * Notify state change listeners
     */
    notifyStateChange() {
        const event = {
            currentView: this.currentView,
            previousView: this.previousView,
            history: this.getViewHistory(),
            timestamp: Date.now()
        };

        this.stateListeners.forEach(listener => {
            try {
                listener(event);
            } catch (error) {
                console.error('State listener error:', error);
            }
        });
    }

    /**
     * Get navigation statistics
     */
    getStats() {
        return {
            currentView: this.currentView,
            previousView: this.previousView,
            historySize: this.viewHistory.length,
            maxHistorySize: this.maxHistorySize,
            metadataEntries: this.viewMetadata.size,
            listenersCount: this.stateListeners.size
        };
    }

    /**
     * Export state
     */
    exportState() {
        return {
            currentView: this.currentView,
            previousView: this.previousView,
            viewHistory: this.viewHistory,
            viewMetadata: Object.fromEntries(this.viewMetadata),
            maxHistorySize: this.maxHistorySize
        };
    }

    /**
     * Import state
     */
    importState(state) {
        try {
            if (state.currentView) this.currentView = state.currentView;
            if (state.previousView) this.previousView = state.previousView;
            if (state.viewHistory) this.viewHistory = [...state.viewHistory];
            if (state.viewMetadata) {
                this.viewMetadata = new Map(Object.entries(state.viewMetadata));
            }
            if (state.maxHistorySize) this.maxHistorySize = state.maxHistorySize;

            console.log('Navigation state imported successfully');
            return true;
        } catch (error) {
            console.error('Failed to import navigation state:', error);
            return false;
        }
    }
}

// Factory function for creating navigation state
export function createNavigationState(initialView = 'overview') {
    return new NavigationState(initialView);
}
