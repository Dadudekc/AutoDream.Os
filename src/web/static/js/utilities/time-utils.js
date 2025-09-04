/**
 * Time Utilities Module - V2 Compliant
 * Date and time manipulation functions
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class TimeUtils {
    constructor(logger = console) {
        this.logger = logger;
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
                locale: 'en-US',
                dateStyle: 'medium',
                timeStyle: 'short',
                ...options
            };

            return new Intl.DateTimeFormat(defaultOptions.locale, {
                dateStyle: defaultOptions.dateStyle,
                timeStyle: defaultOptions.timeStyle
            }).format(dateObj);
        } catch (error) {
            this.logger.error('Date formatting failed', error);
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
            this.logger.error('ISO formatting failed', error);
            return null;
        }
    }

    /**
     * Get relative time (e.g., "2 hours ago")
     */
    getRelativeTime(date, locale = 'en-US') {
        try {
            const dateObj = new Date(date);
            if (isNaN(dateObj.getTime())) {
                throw new Error('Invalid date provided');
            }

            const now = new Date();
            const diffInSeconds = Math.floor((now - dateObj) / 1000);
            const diffInMinutes = Math.floor(diffInSeconds / 60);
            const diffInHours = Math.floor(diffInMinutes / 60);
            const diffInDays = Math.floor(diffInHours / 24);

            const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

            if (Math.abs(diffInSeconds) < 60) {
                return rtf.format(-diffInSeconds, 'second');
            } else if (Math.abs(diffInMinutes) < 60) {
                return rtf.format(-diffInMinutes, 'minute');
            } else if (Math.abs(diffInHours) < 24) {
                return rtf.format(-diffInHours, 'hour');
            } else if (Math.abs(diffInDays) < 7) {
                return rtf.format(-diffInDays, 'day');
            } else {
                return this.formatDate(dateObj, { dateStyle: 'medium' });
            }
        } catch (error) {
            this.logger.error('Relative time calculation failed', error);
            return 'Unknown time';
        }
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

            switch (unit.toLowerCase()) {
                case 'seconds':
                case 'second':
                    dateObj.setSeconds(dateObj.getSeconds() + amount);
                    break;
                case 'minutes':
                case 'minute':
                    dateObj.setMinutes(dateObj.getMinutes() + amount);
                    break;
                case 'hours':
                case 'hour':
                    dateObj.setHours(dateObj.getHours() + amount);
                    break;
                case 'days':
                case 'day':
                    dateObj.setDate(dateObj.getDate() + amount);
                    break;
                case 'weeks':
                case 'week':
                    dateObj.setDate(dateObj.getDate() + (amount * 7));
                    break;
                case 'months':
                case 'month':
                    dateObj.setMonth(dateObj.getMonth() + amount);
                    break;
                case 'years':
                case 'year':
                    dateObj.setFullYear(dateObj.getFullYear() + amount);
                    break;
                default:
                    throw new Error(`Invalid time unit: ${unit}`);
            }

            return dateObj;
        } catch (error) {
            this.logger.error('Time addition failed', error);
            return null;
        }
    }

    /**
     * Check if date is in the past
     */
    isPast(date) {
        try {
            const dateObj = new Date(date);
            if (isNaN(dateObj.getTime())) {
                return false;
            }
            return dateObj < new Date();
        } catch (error) {
            this.logger.error('Past date check failed', error);
            return false;
        }
    }

    /**
     * Check if date is in the future
     */
    isFuture(date) {
        try {
            const dateObj = new Date(date);
            if (isNaN(dateObj.getTime())) {
                return false;
            }
            return dateObj > new Date();
        } catch (error) {
            this.logger.error('Future date check failed', error);
            return false;
        }
    }

    /**
     * Get start of day
     */
    getStartOfDay(date) {
        try {
            const dateObj = new Date(date);
            if (isNaN(dateObj.getTime())) {
                throw new Error('Invalid date provided');
            }
            dateObj.setHours(0, 0, 0, 0);
            return dateObj;
        } catch (error) {
            this.logger.error('Start of day calculation failed', error);
            return null;
        }
    }

    /**
     * Get end of day
     */
    getEndOfDay(date) {
        try {
            const dateObj = new Date(date);
            if (isNaN(dateObj.getTime())) {
                throw new Error('Invalid date provided');
            }
            dateObj.setHours(23, 59, 59, 999);
            return dateObj;
        } catch (error) {
            this.logger.error('End of day calculation failed', error);
            return null;
        }
    }

    /**
     * Format duration in milliseconds
     */
    formatDuration(milliseconds) {
        try {
            if (typeof milliseconds !== 'number' || milliseconds < 0) {
                throw new Error('Invalid duration provided');
            }

            const seconds = Math.floor(milliseconds / 1000);
            const minutes = Math.floor(seconds / 60);
            const hours = Math.floor(minutes / 60);
            const days = Math.floor(hours / 24);

            if (days > 0) {
                return `${days}d ${hours % 24}h ${minutes % 60}m`;
            } else if (hours > 0) {
                return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
            } else if (minutes > 0) {
                return `${minutes}m ${seconds % 60}s`;
            } else {
                return `${seconds}s`;
            }
        } catch (error) {
            this.logger.error('Duration formatting failed', error);
            return '0s';
        }
    }
}

// Factory function for creating time utils instance
export function createTimeUtils(logger = console) {
    return new TimeUtils(logger);
}


