/**
 * Responsive Framework JavaScript
 * Agent_Cellphone_V2_Repository TDD Integration Project
 * 
 * A comprehensive JavaScript framework for responsive design and UI interactions:
 * - Responsive breakpoint detection
 * - Component interaction handlers
 * - Mobile-first utilities
 * - Event management system
 * - Touch and gesture support
 * 
 * Author: Web Development & UI Framework Specialist
 * License: MIT
 */

(function(window, document) {
    'use strict';

    // Framework namespace
    const ResponsiveFramework = {
        version: '1.0.0',
        breakpoints: {
            xs: 0,
            sm: 576,
            md: 768,
            lg: 992,
            xl: 1200,
            xxl: 1400
        },
        components: {},
        events: {},
        utils: {},
        config: {
            enableTouchSupport: true,
            enableScrollSpy: true,
            enableLazyLoading: true,
            enableAnimations: true
        }
    };

    /**
     * Utility Functions
     */
    ResponsiveFramework.utils = {
        /**
         * Get current viewport width
         */
        getViewportWidth: function() {
            return Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
        },

        /**
         * Get current viewport height
         */
        getViewportHeight: function() {
            return Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
        },

        /**
         * Get current breakpoint
         */
        getCurrentBreakpoint: function() {
            const width = this.getViewportWidth();
            const breakpoints = ResponsiveFramework.breakpoints;
            
            if (width >= breakpoints.xxl) return 'xxl';
            if (width >= breakpoints.xl) return 'xl';
            if (width >= breakpoints.lg) return 'lg';
            if (width >= breakpoints.md) return 'md';
            if (width >= breakpoints.sm) return 'sm';
            return 'xs';
        },

        /**
         * Check if viewport matches breakpoint
         */
        matchesBreakpoint: function(breakpoint) {
            const width = this.getViewportWidth();
            return width >= ResponsiveFramework.breakpoints[breakpoint];
        },

        /**
         * Debounce function
         */
        debounce: function(func, wait, immediate) {
            let timeout;
            return function executedFunction() {
                const context = this;
                const args = arguments;
                const later = function() {
                    timeout = null;
                    if (!immediate) func.apply(context, args);
                };
                const callNow = immediate && !timeout;
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
                if (callNow) func.apply(context, args);
            };
        },

        /**
         * Throttle function
         */
        throttle: function(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },

        /**
         * Check if element is in viewport
         */
        isInViewport: function(element) {
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

        /**
         * Get element offset from top of page
         */
        getElementOffset: function(element) {
            let top = 0;
            let left = 0;
            
            while (element) {
                top += element.offsetTop;
                left += element.offsetLeft;
                element = element.offsetParent;
            }
            
            return { top, left };
        },

        /**
         * Add class with animation support
         */
        addClass: function(element, className, animationClass = null) {
            if (!element.classList.contains(className)) {
                element.classList.add(className);
                
                if (animationClass && ResponsiveFramework.config.enableAnimations) {
                    element.classList.add(animationClass);
                    setTimeout(() => {
                        element.classList.remove(animationClass);
                    }, 300);
                }
            }
        },

        /**
         * Remove class with animation support
         */
        removeClass: function(element, className, animationClass = null) {
            if (element.classList.contains(className)) {
                if (animationClass && ResponsiveFramework.config.enableAnimations) {
                    element.classList.add(animationClass);
                    setTimeout(() => {
                        element.classList.remove(className, animationClass);
                    }, 300);
                } else {
                    element.classList.remove(className);
                }
            }
        },

        /**
         * Toggle class with animation support
         */
        toggleClass: function(element, className, animationClass = null) {
            if (element.classList.contains(className)) {
                this.removeClass(element, className, animationClass);
            } else {
                this.addClass(element, className, animationClass);
            }
        }
    };

    /**
     * Event Management System
     */
    ResponsiveFramework.events = {
        listeners: {},

        /**
         * Add event listener
         */
        on: function(event, callback) {
            if (!this.listeners[event]) {
                this.listeners[event] = [];
            }
            this.listeners[event].push(callback);
        },

        /**
         * Remove event listener
         */
        off: function(event, callback) {
            if (this.listeners[event]) {
                const index = this.listeners[event].indexOf(callback);
                if (index > -1) {
                    this.listeners[event].splice(index, 1);
                }
            }
        },

        /**
         * Trigger event
         */
        trigger: function(event, data = null) {
            if (this.listeners[event]) {
                this.listeners[event].forEach(callback => {
                    try {
                        callback(data);
                    } catch (error) {
                        console.error('Error in event callback:', error);
                    }
                });
            }
        }
    };

    /**
     * Responsive Navigation Component
     */
    ResponsiveFramework.components.Navigation = {
        init: function() {
            this.setupMobileToggle();
            this.setupDropdowns();
            this.setupScrollSpy();
        },

        setupMobileToggle: function() {
            const toggleButtons = document.querySelectorAll('[data-bs-toggle="collapse"]');
            
            toggleButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    e.preventDefault();
                    const target = document.querySelector(button.getAttribute('data-bs-target'));
                    
                    if (target) {
                        ResponsiveFramework.utils.toggleClass(target, 'show', 'animate-slideInDown');
                        ResponsiveFramework.utils.toggleClass(button, 'collapsed');
                    }
                });
            });
        },

        setupDropdowns: function() {
            const dropdowns = document.querySelectorAll('.dropdown');
            
            dropdowns.forEach(dropdown => {
                const toggle = dropdown.querySelector('.dropdown-toggle');
                const menu = dropdown.querySelector('.dropdown-menu');
                
                if (toggle && menu) {
                    toggle.addEventListener('click', (e) => {
                        e.preventDefault();
                        this.toggleDropdown(dropdown);
                    });
                    
                    // Close on outside click
                    document.addEventListener('click', (e) => {
                        if (!dropdown.contains(e.target)) {
                            this.closeDropdown(dropdown);
                        }
                    });
                }
            });
        },

        toggleDropdown: function(dropdown) {
            const menu = dropdown.querySelector('.dropdown-menu');
            ResponsiveFramework.utils.toggleClass(dropdown, 'show');
            ResponsiveFramework.utils.toggleClass(menu, 'show', 'animate-slideInDown');
        },

        closeDropdown: function(dropdown) {
            const menu = dropdown.querySelector('.dropdown-menu');
            ResponsiveFramework.utils.removeClass(dropdown, 'show');
            ResponsiveFramework.utils.removeClass(menu, 'show');
        },

        setupScrollSpy: function() {
            if (!ResponsiveFramework.config.enableScrollSpy) return;
            
            const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
            const sections = Array.from(navLinks).map(link => {
                const href = link.getAttribute('href');
                return href !== '#' ? document.querySelector(href) : null;
            }).filter(section => section);
            
            const handleScroll = ResponsiveFramework.utils.throttle(() => {
                const scrollTop = window.pageYOffset;
                
                sections.forEach((section, index) => {
                    const offset = ResponsiveFramework.utils.getElementOffset(section);
                    const link = navLinks[index];
                    
                    if (scrollTop >= offset.top - 100 && 
                        scrollTop < offset.top + section.offsetHeight - 100) {
                        link.classList.add('active');
                    } else {
                        link.classList.remove('active');
                    }
                });
            }, 100);
            
            window.addEventListener('scroll', handleScroll);
        }
    };

    /**
     * Modal Component
     */
    ResponsiveFramework.components.Modal = {
        init: function() {
            this.setupModalTriggers();
            this.setupKeyboardHandlers();
        },

        setupModalTriggers: function() {
            const modalTriggers = document.querySelectorAll('[data-bs-toggle="modal"]');
            
            modalTriggers.forEach(trigger => {
                trigger.addEventListener('click', (e) => {
                    e.preventDefault();
                    const target = document.querySelector(trigger.getAttribute('data-bs-target'));
                    
                    if (target) {
                        this.showModal(target);
                    }
                });
            });
            
            // Close button handlers
            const closeButtons = document.querySelectorAll('[data-bs-dismiss="modal"]');
            closeButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    e.preventDefault();
                    const modal = button.closest('.modal');
                    if (modal) {
                        this.hideModal(modal);
                    }
                });
            });
            
            // Backdrop click handler
            document.addEventListener('click', (e) => {
                if (e.target.classList.contains('modal')) {
                    this.hideModal(e.target);
                }
            });
        },

        showModal: function(modal) {
            // Create backdrop
            const backdrop = document.createElement('div');
            backdrop.className = 'modal-backdrop';
            backdrop.setAttribute('data-modal-id', modal.id);
            document.body.appendChild(backdrop);
            
            // Show modal
            modal.style.display = 'block';
            document.body.classList.add('modal-open');
            
            // Animate in
            setTimeout(() => {
                modal.classList.add('show');
                backdrop.classList.add('show');
            }, 10);
            
            // Focus management
            const firstFocusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            if (firstFocusable) {
                firstFocusable.focus();
            }
            
            ResponsiveFramework.events.trigger('modal.show', { modal });
        },

        hideModal: function(modal) {
            const backdrop = document.querySelector(`[data-modal-id="${modal.id}"]`);
            
            // Animate out
            modal.classList.remove('show');
            if (backdrop) {
                backdrop.classList.remove('show');
            }
            
            setTimeout(() => {
                modal.style.display = 'none';
                if (backdrop) {
                    backdrop.remove();
                }
                document.body.classList.remove('modal-open');
            }, 300);
            
            ResponsiveFramework.events.trigger('modal.hide', { modal });
        },

        setupKeyboardHandlers: function() {
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    const openModal = document.querySelector('.modal.show');
                    if (openModal) {
                        this.hideModal(openModal);
                    }
                }
            });
        }
    };

    /**
     * Accordion Component
     */
    ResponsiveFramework.components.Accordion = {
        init: function() {
            const accordions = document.querySelectorAll('.accordion');
            
            accordions.forEach(accordion => {
                this.setupAccordion(accordion);
            });
        },

        setupAccordion: function(accordion) {
            const items = accordion.querySelectorAll('.accordion-item');
            
            items.forEach(item => {
                const button = item.querySelector('.accordion-button');
                const collapse = item.querySelector('.accordion-collapse');
                
                if (button && collapse) {
                    button.addEventListener('click', (e) => {
                        e.preventDefault();
                        this.toggleItem(item, accordion);
                    });
                }
            });
        },

        toggleItem: function(item, accordion) {
            const button = item.querySelector('.accordion-button');
            const collapse = item.querySelector('.accordion-collapse');
            const isExpanded = collapse.classList.contains('show');
            
            // Close other items if not multi-collapse
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

        openItem: function(item) {
            const button = item.querySelector('.accordion-button');
            const collapse = item.querySelector('.accordion-collapse');
            
            button.classList.remove('collapsed');
            button.setAttribute('aria-expanded', 'true');
            ResponsiveFramework.utils.addClass(collapse, 'show', 'animate-slideInDown');
        },

        closeItem: function(item) {
            const button = item.querySelector('.accordion-button');
            const collapse = item.querySelector('.accordion-collapse');
            
            button.classList.add('collapsed');
            button.setAttribute('aria-expanded', 'false');
            ResponsiveFramework.utils.removeClass(collapse, 'show');
        }
    };

    /**
     * Lazy Loading Component
     */
    ResponsiveFramework.components.LazyLoading = {
        init: function() {
            if (!ResponsiveFramework.config.enableLazyLoading) return;
            
            this.setupIntersectionObserver();
        },

        setupIntersectionObserver: function() {
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
                // Fallback for older browsers
                this.fallbackLazyLoading();
            }
        },

        fallbackLazyLoading: function() {
            const images = document.querySelectorAll('img[data-src]');
            
            const loadImages = ResponsiveFramework.utils.throttle(() => {
                images.forEach(img => {
                    if (ResponsiveFramework.utils.isInViewport(img)) {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                    }
                });
            }, 200);
            
            window.addEventListener('scroll', loadImages);
            window.addEventListener('resize', loadImages);
            loadImages(); // Initial load
        }
    };

    /**
     * Touch Support
     */
    ResponsiveFramework.components.TouchSupport = {
        init: function() {
            if (!ResponsiveFramework.config.enableTouchSupport) return;
            
            this.setupSwipeDetection();
            this.setupTouchFeedback();
        },

        setupSwipeDetection: function() {
            let startX, startY, endX, endY;
            
            document.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
            });
            
            document.addEventListener('touchend', (e) => {
                endX = e.changedTouches[0].clientX;
                endY = e.changedTouches[0].clientY;
                
                this.handleSwipe(startX, startY, endX, endY, e.target);
            });
        },

        handleSwipe: function(startX, startY, endX, endY, target) {
            const deltaX = endX - startX;
            const deltaY = endY - startY;
            const threshold = 50;
            
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > threshold) {
                // Horizontal swipe
                const direction = deltaX > 0 ? 'right' : 'left';
                ResponsiveFramework.events.trigger('swipe', {
                    direction,
                    target,
                    deltaX,
                    deltaY
                });
            } else if (Math.abs(deltaY) > threshold) {
                // Vertical swipe
                const direction = deltaY > 0 ? 'down' : 'up';
                ResponsiveFramework.events.trigger('swipe', {
                    direction,
                    target,
                    deltaX,
                    deltaY
                });
            }
        },

        setupTouchFeedback: function() {
            const interactiveElements = document.querySelectorAll('button, .btn, a, [role="button"]');
            
            interactiveElements.forEach(element => {
                element.addEventListener('touchstart', () => {
                    element.classList.add('touch-active');
                });
                
                element.addEventListener('touchend', () => {
                    setTimeout(() => {
                        element.classList.remove('touch-active');
                    }, 150);
                });
            });
        }
    };

    /**
     * Responsive Breakpoint Handler
     */
    ResponsiveFramework.components.BreakpointHandler = {
        currentBreakpoint: null,
        
        init: function() {
            this.currentBreakpoint = ResponsiveFramework.utils.getCurrentBreakpoint();
            this.setupResizeHandler();
            this.triggerBreakpointChange();
        },

        setupResizeHandler: function() {
            const handleResize = ResponsiveFramework.utils.debounce(() => {
                const newBreakpoint = ResponsiveFramework.utils.getCurrentBreakpoint();
                
                if (newBreakpoint !== this.currentBreakpoint) {
                    const oldBreakpoint = this.currentBreakpoint;
                    this.currentBreakpoint = newBreakpoint;
                    
                    ResponsiveFramework.events.trigger('breakpoint.change', {
                        oldBreakpoint,
                        newBreakpoint,
                        viewport: {
                            width: ResponsiveFramework.utils.getViewportWidth(),
                            height: ResponsiveFramework.utils.getViewportHeight()
                        }
                    });
                }
            }, 250);
            
            window.addEventListener('resize', handleResize);
        },

        triggerBreakpointChange: function() {
            ResponsiveFramework.events.trigger('breakpoint.change', {
                oldBreakpoint: null,
                newBreakpoint: this.currentBreakpoint,
                viewport: {
                    width: ResponsiveFramework.utils.getViewportWidth(),
                    height: ResponsiveFramework.utils.getViewportHeight()
                }
            });
        }
    };

    /**
     * Form Enhancement
     */
    ResponsiveFramework.components.FormEnhancement = {
        init: function() {
            this.setupValidation();
            this.setupFloatingLabels();
            this.setupFileInputs();
        },

        setupValidation: function() {
            const forms = document.querySelectorAll('.needs-validation');
            
            forms.forEach(form => {
                form.addEventListener('submit', (e) => {
                    if (!form.checkValidity()) {
                        e.preventDefault();
                        e.stopPropagation();
                    }
                    
                    form.classList.add('was-validated');
                });
            });
        },

        setupFloatingLabels: function() {
            const floatingInputs = document.querySelectorAll('.form-floating input, .form-floating textarea');
            
            floatingInputs.forEach(input => {
                const updateLabel = () => {
                    const label = input.nextElementSibling;
                    if (label && label.classList.contains('form-label')) {
                        if (input.value || input === document.activeElement) {
                            label.classList.add('active');
                        } else {
                            label.classList.remove('active');
                        }
                    }
                };
                
                input.addEventListener('focus', updateLabel);
                input.addEventListener('blur', updateLabel);
                input.addEventListener('input', updateLabel);
                
                // Initial state
                updateLabel();
            });
        },

        setupFileInputs: function() {
            const fileInputs = document.querySelectorAll('input[type="file"]');
            
            fileInputs.forEach(input => {
                input.addEventListener('change', (e) => {
                    const files = e.target.files;
                    const label = input.nextElementSibling;
                    
                    if (files.length > 0) {
                        const fileName = files.length === 1 ? files[0].name : `${files.length} files selected`;
                        if (label) {
                            label.textContent = fileName;
                        }
                    }
                });
            });
        }
    };

    /**
     * Initialize Framework
     */
    ResponsiveFramework.init = function() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.initializeComponents();
            });
        } else {
            this.initializeComponents();
        }
    };

    ResponsiveFramework.initializeComponents = function() {
        try {
            // Initialize all components
            Object.keys(this.components).forEach(componentName => {
                const component = this.components[componentName];
                if (component && typeof component.init === 'function') {
                    component.init();
                }
            });
            
            // Trigger framework ready event
            this.events.trigger('framework.ready');
            
            console.log('ResponsiveFramework initialized successfully');
        } catch (error) {
            console.error('Error initializing ResponsiveFramework:', error);
        }
    };

    // Add CSS for touch feedback
    const style = document.createElement('style');
    style.textContent = `
        .touch-active {
            transform: scale(0.95);
            opacity: 0.8;
            transition: all 0.1s ease;
        }
        
        .lazy {
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .lazy.loaded {
            opacity: 1;
        }
    `;
    document.head.appendChild(style);

    // Expose framework globally
    window.ResponsiveFramework = ResponsiveFramework;
    window.RF = ResponsiveFramework; // Short alias

    // Auto-initialize
    ResponsiveFramework.init();

})(window, document);
