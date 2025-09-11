/**
 * Dashboard Date Utils Module - V2 Compliant
 * Date and time formatting utilities
 *
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

export const DateUtils = {
    formatDate(date, options = {}) {
        if (!date) return 'N/A';
        const dateObj = new Date(date);
        if (isNaN(dateObj.getTime())) return 'Invalid Date';

        const defaultOptions = {
            locale: 'en-US',
            dateStyle: 'medium',
            timeStyle: options.includeTime ? 'short' : undefined,
            ...options
        };

        return new Intl.DateTimeFormat(defaultOptions.locale, {
            dateStyle: defaultOptions.dateStyle,
            timeStyle: defaultOptions.timeStyle
        }).format(dateObj);
    },

    getRelativeTime(date) {
        if (!date) return 'N/A';
        const dateObj = new Date(date);
        if (isNaN(dateObj.getTime())) return 'Invalid Date';

        const now = new Date();
        const diffInSeconds = Math.floor((now - dateObj) / 1000);
        const diffInMinutes = Math.floor(diffInSeconds / 60);
        const diffInHours = Math.floor(diffInMinutes / 60);
        const diffInDays = Math.floor(diffInHours / 24);

        const rtf = new Intl.RelativeTimeFormat('en-US', { numeric: 'auto' });

        if (Math.abs(diffInSeconds) < 60) {
            return rtf.format(-diffInSeconds, 'second');
        } else if (Math.abs(diffInMinutes) < 60) {
            return rtf.format(-diffInMinutes, 'minute');
        } else if (Math.abs(diffInHours) < 24) {
            return rtf.format(-diffInHours, 'hour');
        } else if (Math.abs(diffInDays) < 7) {
            return rtf.format(-diffInDays, 'day');
        } else {
            return this.formatDate(dateObj, { dateStyle: 'short' });
        }
    },

    isToday(date) {
        if (!date) return false;
        const dateObj = new Date(date);
        if (isNaN(dateObj.getTime())) return false;
        const today = new Date();
        return dateObj.toDateString() === today.toDateString();
    },

    isYesterday(date) {
        if (!date) return false;
        const dateObj = new Date(date);
        if (isNaN(dateObj.getTime())) return false;
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        return dateObj.toDateString() === yesterday.toDateString();
    },

    getStartOfDay(date) {
        if (!date) return null;
        const dateObj = new Date(date);
        if (isNaN(dateObj.getTime())) return null;
        dateObj.setHours(0, 0, 0, 0);
        return dateObj;
    },

    getEndOfDay(date) {
        if (!date) return null;
        const dateObj = new Date(date);
        if (isNaN(dateObj.getTime())) return null;
        dateObj.setHours(23, 59, 59, 999);
        return dateObj;
    },

    formatDateRange(startDate, endDate) {
        if (!startDate || !endDate) return 'N/A';
        const start = this.formatDate(startDate, { dateStyle: 'short' });
        const end = this.formatDate(endDate, { dateStyle: 'short' });
        if (start === end) return start;
        return `${start} - ${end}`;
    }
};
