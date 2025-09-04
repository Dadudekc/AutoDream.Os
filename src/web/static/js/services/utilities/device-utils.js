/**
 * Device & Browser Utilities - V2 Compliant Module
 * Device and browser detection utilities
 * MODULAR: ~85 lines (V2 compliant)
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE MODULAR EXTRACTION
 * @license MIT
 */

export class DeviceUtils {
    constructor() {
        this.logger = new UnifiedLoggingSystem("DeviceUtils");
    }

    /**
     * Check if running on mobile device
     */
    isMobileDevice() {
        if (typeof window === 'undefined') return false;

        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
            window.navigator.userAgent
        );
    }

    /**
     * Get browser information
     */
    getBrowserInfo() {
        if (typeof window === 'undefined') {
            return { name: 'unknown', version: 'unknown' };
        }

        const userAgent = window.navigator.userAgent;
        let browser = { name: 'unknown', version: 'unknown' };

        // Chrome
        if (userAgent.includes('Chrome')) {
            const match = userAgent.match(/Chrome\/(\d+)/);
            browser = { name: 'Chrome', version: match ? match[1] : 'unknown' };
        }
        // Firefox
        else if (userAgent.includes('Firefox')) {
            const match = userAgent.match(/Firefox\/(\d+)/);
            browser = { name: 'Firefox', version: match ? match[1] : 'unknown' };
        }
        // Safari
        else if (userAgent.includes('Safari') && !userAgent.includes('Chrome')) {
            const match = userAgent.match(/Version\/(\d+)/);
            browser = { name: 'Safari', version: match ? match[1] : 'unknown' };
        }
        // Edge
        else if (userAgent.includes('Edg')) {
            const match = userAgent.match(/Edg\/(\d+)/);
            browser = { name: 'Edge', version: match ? match[1] : 'unknown' };
        }

        return browser;
    }

    /**
     * Get device type
     */
    getDeviceType() {
        if (typeof window === 'undefined') return 'server';

        if (this.isMobileDevice()) {
            return window.innerWidth < 768 ? 'mobile' : 'tablet';
        }

        return 'desktop';
    }
}


