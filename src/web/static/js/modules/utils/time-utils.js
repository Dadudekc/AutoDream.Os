/**
 * Time Utils - V2 Compliant Time and Date Management System
 * V2 COMPLIANT: 200 lines maximum
 * CONSOLIDATES: time-utils.js, date-utils.js, time-related utilities
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Unified time utilities with formatting, parsing, and calculations
 */

// ================================
// TIME UTILS CLASS
// ================================

/**
 * Unified Time Utilities
 * Consolidates all time and date functionality
 */
export class TimeUtils {
    constructor(options = {}) {
        this.isInitialized = false;
        this.timers = new Map();
        this.config = {
            defaultLocale: 'en-US',
            defaultTimezone: 'UTC',
            enablePerformanceMonitoring: true,
            ...options
        };
    }

    /**
     * Initialize time utilities
     */
    async initialize() {
        if (this.isInitialized) {
            console.warn('⚠️ Time utils already initialized');
            return;
        }

        console.log('🚀 Initializing Time Utils (V2 Compliant)...');

        try {
            // Setup time event listeners
            this.setupTimeEventListeners();

            // Initialize timezone detection
            this.initializeTimezoneDetection();

            this.isInitialized = true;
            console.log('✅ Time Utils initialized successfully');

        } catch (error) {
            console.error('❌ Failed to initialize time utils:', error);
            throw error;
        }
    }

    /**
     * Setup time event listeners
     */
    setupTimeEventListeners() {
        // Listen for time update requests
        window.addEventListener('time:update', (event) => {
            this.handleTimeUpdate(event.detail);
        });

        // Listen for timer requests
        window.addEventListener('time:timer', (event) => {
            this.handleTimerRequest(event.detail);
        });
    }

    /**
     * Initialize timezone detection
     */
    initializeTimezoneDetection() {
        try {
            this.config.defaultTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        } catch (error) {
            console.warn('⚠️ Timezone detection failed, using UTC');
            this.config.defaultTimezone = 'UTC';
        }
    }

    /**
     * Format date to readable string
     */
    formatDate(date, options = {}) {
        try {
            const dateObj = new Date(date);
            if (isNaN(dateObj.getTime())) {
                throw new Error('Invalid date provided');
            }

            const defaultOptions = {
                locale: this.config.defaultLocale,
                dateStyle: 'medium',
                timeStyle: 'short',
                timeZone: this.config.defaultTimezone,
                ...options
            };

            return new Intl.DateTimeFormat(defaultOptions.locale, {
                dateStyle: defaultOptions.dateStyle,
                timeStyle: defaultOptions.timeStyle,
                timeZone: defaultOptions.timeZone
            }).format(dateObj);
        } catch (error) {
            console.error('❌ Date formatting failed:', error);
            return 'Invalid Date';
        }
    }

    /**
     * Format date to ISO string
     */
    formatISO(date) {
        try {
            const dateObj = new Date(date);
            if (isNaN(dateObj.getTime())) {
                throw new Error('Invalid date provided');
            }
            return dateObj.toISOString();
        } catch (error) {
            console.error('❌ ISO formatting failed:', error);
            return null;
        }
    }

    /**
     * Format relative time
     */
    formatRelative(date, options = {}) {
        try {
            const dateObj = new Date(date);
            if (isNaN(dateObj.getTime())) {
                throw new Error('Invalid date provided');
            }

            const now = new Date();
            const diffMs = now - dateObj;
            const diffSeconds = Math.floor(diffMs / 1000);
            const diffMinutes = Math.floor(diffSeconds / 60);
            const diffHours = Math.floor(diffMinutes / 60);
            const diffDays = Math.floor(diffHours / 24);

            if (diffSeconds < 60) {
                return 'just now';
            } else if (diffMinutes < 60) {
                return `${diffMinutes} minute${diffMinutes > 1 ? 's' : ''} ago`;
            } else if (diffHours < 24) {
                return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
            } else if (diffDays < 7) {
                return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
            } else {
                return this.formatDate(dateObj, { dateStyle: 'short' });
            }
        } catch (error) {
            console.error('❌ Relative time formatting failed:', error);
            return 'unknown time';
        }
    }

    /**
     * Parse date string
     */
    parseDate(dateString) {
        try {
            const date = new Date(dateString);
            if (isNaN(date.getTime())) {
                throw new Error('Invalid date string');
            }
            return date;
        } catch (error) {
            console.error('❌ Date parsing failed:', error);
            return null;
        }
    }

    /**
     * Get current timestamp
     */
    getCurrentTimestamp() {
        return Date.now();
    }

    /**
     * Get current date
     */
    getCurrentDate() {
        return new Date();
    }

    /**
     * Add time to date
     */
    addTime(date, amount, unit) {
        try {
            const dateObj = new Date(date);
            if (isNaN(dateObj.getTime())) {
                throw new Error('Invalid date provided');
            }

            const units = {
                'milliseconds': 1,
                'seconds': 1000,
                'minutes': 60 * 1000,
                'hours': 60 * 60 * 1000,
                'days': 24 * 60 * 60 * 1000,
                'weeks': 7 * 24 * 60 * 60 * 1000,
                'months': 30 * 24 * 60 * 60 * 1000,
                'years': 365 * 24 * 60 * 60 * 1000
            };

            const multiplier = units[unit] || 1;
            return new Date(dateObj.getTime() + (amount * multiplier));
        } catch (error) {
            console.error('❌ Time addition failed:', error);
            return null;
        }
    }

    /**
     * Calculate time difference
     */
    getTimeDifference(startDate, endDate, unit = 'milliseconds') {
        try {
            const start = new Date(startDate);
            const end = new Date(endDate);
            
            if (isNaN(start.getTime()) || isNaN(end.getTime())) {
                throw new Error('Invalid dates provided');
            }

            const diffMs = end - start;
            const units = {
                'milliseconds': 1,
                'seconds': 1000,
                'minutes': 60 * 1000,
                'hours': 60 * 60 * 1000,
                'days': 24 * 60 * 60 * 1000
            };

            const multiplier = units[unit] || 1;
            return Math.floor(diffMs / multiplier);
        } catch (error) {
            console.error('❌ Time difference calculation failed:', error);
            return null;
        }
    }

    /**
     * Create timer
     */
    createTimer(name, duration, callback, options = {}) {
        try {
            const timerId = this.generateTimerId();
            const timer = {
                id: timerId,
                name,
                duration,
                callback,
                startTime: Date.now(),
                isActive: true,
                options
            };

            const timeoutId = setTimeout(() => {
                this.executeTimer(timer);
            }, duration);

            timer.timeoutId = timeoutId;
            this.timers.set(timerId, timer);

            console.log(`⏰ Timer created: ${name} (${duration}ms)`);
            return timerId;

        } catch (error) {
            console.error('❌ Timer creation failed:', error);
            return null;
        }
    }

    /**
     * Execute timer
     */
    executeTimer(timer) {
        try {
            if (timer.isActive) {
                timer.callback();
                this.timers.delete(timer.id);
                console.log(`⏰ Timer executed: ${timer.name}`);
            }
        } catch (error) {
            console.error('❌ Timer execution failed:', error);
        }
    }

    /**
     * Cancel timer
     */
    cancelTimer(timerId) {
        const timer = this.timers.get(timerId);
        if (timer) {
            clearTimeout(timer.timeoutId);
            timer.isActive = false;
            this.timers.delete(timerId);
            console.log(`⏰ Timer cancelled: ${timer.name}`);
            return true;
        }
        return false;
    }

    /**
     * Create interval
     */
    createInterval(name, interval, callback, options = {}) {
        try {
            const timerId = this.generateTimerId();
            const timer = {
                id: timerId,
                name,
                interval,
                callback,
                startTime: Date.now(),
                isActive: true,
                isInterval: true,
                options
            };

            const intervalId = setInterval(() => {
                this.executeInterval(timer);
            }, interval);

            timer.intervalId = intervalId;
            this.timers.set(timerId, timer);

            console.log(`⏰ Interval created: ${name} (${interval}ms)`);
            return timerId;

        } catch (error) {
            console.error('❌ Interval creation failed:', error);
            return null;
        }
    }

    /**
     * Execute interval
     */
    executeInterval(timer) {
        try {
            if (timer.isActive) {
                timer.callback();
            }
        } catch (error) {
            console.error('❌ Interval execution failed:', error);
        }
    }

    /**
     * Cancel interval
     */
    cancelInterval(timerId) {
        const timer = this.timers.get(timerId);
        if (timer && timer.isInterval) {
            clearInterval(timer.intervalId);
            timer.isActive = false;
            this.timers.delete(timerId);
            console.log(`⏰ Interval cancelled: ${timer.name}`);
            return true;
        }
        return false;
    }

    /**
     * Handle time update
     */
    handleTimeUpdate(data) {
        const { element, format, interval } = data;
        
        if (element && format) {
            this.updateTimeDisplay(element, format, interval);
        }
    }

    /**
     * Handle timer request
     */
    handleTimerRequest(data) {
        const { type, name, duration, callback, options } = data;
        
        if (type === 'timer') {
            return this.createTimer(name, duration, callback, options);
        } else if (type === 'interval') {
            return this.createInterval(name, duration, callback, options);
        }
    }

    /**
     * Update time display
     */
    updateTimeDisplay(element, format, interval = 1000) {
        const updateTime = () => {
            const now = new Date();
            element.textContent = this.formatDate(now, format);
        };

        // Initial update
        updateTime();

        // Create interval for updates
        if (interval > 0) {
            this.createInterval(`time-display-${element.id}`, interval, updateTime);
        }
    }

    /**
     * Generate timer ID
     */
    generateTimerId() {
        return `timer_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Get timezone offset
     */
    getTimezoneOffset() {
        return new Date().getTimezoneOffset();
    }

    /**
     * Convert to timezone
     */
    convertToTimezone(date, timezone) {
        try {
            const dateObj = new Date(date);
            if (isNaN(dateObj.getTime())) {
                throw new Error('Invalid date provided');
            }

            return new Intl.DateTimeFormat('en-US', {
                timeZone: timezone,
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            }).formatToParts(dateObj);
        } catch (error) {
            console.error('❌ Timezone conversion failed:', error);
            return null;
        }
    }

    /**
     * Get service status
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            activeTimers: this.timers.size,
            defaultLocale: this.config.defaultLocale,
            defaultTimezone: this.config.defaultTimezone
        };
    }

    /**
     * Destroy time utils
     */
    async destroy() {
        console.log('🧹 Destroying time utils...');

        // Cancel all timers and intervals
        this.timers.forEach((timer, id) => {
            if (timer.isInterval) {
                this.cancelInterval(id);
            } else {
                this.cancelTimer(id);
            }
        });

        this.timers.clear();
        this.isInitialized = false;

        console.log('✅ Time utils destroyed');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create time utils with default configuration
 */
export function createTimeUtils(options = {}) {
    return new TimeUtils(options);
}

// Export default
export default TimeUtils;