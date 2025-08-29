import { debounce, throttle } from '../portal/utils.js';
import { breakpoints } from './config.js';

export const layoutUtils = {
    getViewportWidth() {
        return Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    },

    getViewportHeight() {
        return Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
    },

    getCurrentBreakpoint() {
        const width = this.getViewportWidth();

        if (width >= breakpoints.xxl) return 'xxl';
        if (width >= breakpoints.xl) return 'xl';
        if (width >= breakpoints.lg) return 'lg';
        if (width >= breakpoints.md) return 'md';
        if (width >= breakpoints.sm) return 'sm';
        return 'xs';
    },

    matchesBreakpoint(breakpoint) {
        const width = this.getViewportWidth();
        return width >= breakpoints[breakpoint];
    },

    debounce,
    throttle,

    isInViewport(element) {
        const rect = element.getBoundingClientRect();
        const viewportHeight = this.getViewportHeight();
        const viewportWidth = this.getViewportWidth();

        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= viewportHeight &&
            rect.right <= viewportWidth
        );
    },

    getElementOffset(element) {
        let top = 0;
        let left = 0;

        while (element) {
            top += element.offsetTop;
            left += element.offsetLeft;
            element = element.offsetParent;
        }

        return { top, left };
    },

    addClass(element, className, animationClass = null) {
        if (!element.classList.contains(className)) {
            element.classList.add(className);

            if (animationClass) {
                element.classList.add(animationClass);
                setTimeout(() => {
                    element.classList.remove(animationClass);
                }, 300);
            }
        }
    },

    removeClass(element, className) {
        if (element.classList.contains(className)) {
            element.classList.remove(className);
        }
    },

    toggleClass(element, className, animationClass = null) {
        if (element.classList.contains(className)) {
            this.removeClass(element, className);
        } else {
            this.addClass(element, className, animationClass);
        }
    }
};

