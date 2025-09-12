import { layoutUtils } from './layout.js';
import { events } from './events.js';
import { config } from './config.js';

export const Accordion = {
    init() {
        const accordions = document.querySelectorAll('.accordion');

        accordions.forEach(accordion => {
            this.setupAccordion(accordion);
        });
    },

    setupAccordion(accordion) {
        const items = accordion.querySelectorAll('.accordion-item');

        items.forEach(item => {
            const button = item.querySelector('.accordion-button');
            const collapse = item.querySelector('.accordion-collapse');

            if (button && collapse) {
                button.addEventListener('click', e => {
                    e.preventDefault();
                    this.toggleItem(item, accordion);
                });
            }
        });
    },

    toggleItem(item, accordion) {
        const button = item.querySelector('.accordion-button');
        const collapse = item.querySelector('.accordion-collapse');
        const isExpanded = collapse.classList.contains('show');

        if (!accordion.hasAttribute('data-bs-allow-multiple')) {
            const openItems = accordion.querySelectorAll('.accordion-collapse.show');
            openItems.forEach(openItem => {
                if (openItem !== collapse) {
                    this.closeItem(openItem.closest('.accordion-item'));
                }
            });
        }

        if (isExpanded) {
            this.closeItem(item);
        } else {
            this.openItem(item);
        }
    },

    openItem(item) {
        const button = item.querySelector('.accordion-button');
        const collapse = item.querySelector('.accordion-collapse');

        button.classList.remove('collapsed');
        button.setAttribute('aria-expanded', 'true');
        layoutUtils.addClass(collapse, 'show', 'animate-slideInDown');
    },

    closeItem(item) {
        const button = item.querySelector('.accordion-button');
        const collapse = item.querySelector('.accordion-collapse');

        button.classList.add('collapsed');
        button.setAttribute('aria-expanded', 'false');
        layoutUtils.removeClass(collapse, 'show');
    }
};

export const LazyLoading = {
    init() {
        if (!config.enableLazyLoading) return;

        this.setupIntersectionObserver();
    },

    setupIntersectionObserver() {
        if ('IntersectionObserver' in window) {
            const images = document.querySelectorAll('img[data-src]');

            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        } else {
            this.fallbackLazyLoading();
        }
    },

    fallbackLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');

        const loadImages = layoutUtils.throttle(() => {
            images.forEach(img => {
                if (layoutUtils.isInViewport(img)) {
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                }
            });
        }, 200);

        window.addEventListener('scroll', loadImages);
        window.addEventListener('resize', loadImages);
        loadImages();
    }
};

export const TouchSupport = {
    init() {
        if (!config.enableTouchSupport) return;

        this.setupTouchEvents();
    },

    setupTouchEvents() {
        let touchStartX = 0;
        let touchStartY = 0;

        const handleTouchStart = e => {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        };

        const handleTouchMove = e => {
            const touchEndX = e.touches[0].clientX;
            const touchEndY = e.touches[0].clientY;

            const diffX = touchEndX - touchStartX;
            const diffY = touchEndY - touchStartY;

            if (Math.abs(diffX) > Math.abs(diffY)) {
                if (Math.abs(diffX) > 30) {
                    const direction = diffX > 0 ? 'right' : 'left';
                    events.trigger('swipe', { direction });
                }
            }
        };

        document.addEventListener('touchstart', handleTouchStart, { passive: true });
        document.addEventListener('touchmove', handleTouchMove, { passive: true });
    }
};

export const BreakpointHandler = {
    currentBreakpoint: null,

    init() {
        this.currentBreakpoint = layoutUtils.getCurrentBreakpoint();
        this.setupResizeHandler();
        this.triggerBreakpointChange();
    },

    setupResizeHandler() {
        const handleResize = layoutUtils.debounce(() => {
            const newBreakpoint = layoutUtils.getCurrentBreakpoint();

            if (newBreakpoint !== this.currentBreakpoint) {
                const oldBreakpoint = this.currentBreakpoint;
                this.currentBreakpoint = newBreakpoint;

                events.trigger('breakpoint.change', {
                    oldBreakpoint,
                    newBreakpoint,
                    viewport: {
                        width: layoutUtils.getViewportWidth(),
                        height: layoutUtils.getViewportHeight()
                    }
                });
            }
        }, 250);

        window.addEventListener('resize', handleResize);
    },

    triggerBreakpointChange() {
        events.trigger('breakpoint.change', {
            oldBreakpoint: null,
            newBreakpoint: this.currentBreakpoint,
            viewport: {
                width: layoutUtils.getViewportWidth(),
                height: layoutUtils.getViewportHeight()
            }
        });
    }
};
