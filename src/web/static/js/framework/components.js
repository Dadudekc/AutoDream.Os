import { layoutUtils } from './layout.js';
import { events } from './events.js';
import { config } from './config.js';

export const components = {};

components.Navigation = {
    init() {
        this.setupMobileToggle();
        this.setupDropdowns();
        this.setupScrollSpy();
    },

    setupMobileToggle() {
        const toggleButtons = document.querySelectorAll('[data-bs-toggle="collapse"]');

        toggleButtons.forEach(button => {
            button.addEventListener('click', e => {
                e.preventDefault();
                const target = document.querySelector(button.getAttribute('data-bs-target'));

                if (target) {
                    layoutUtils.toggleClass(target, 'show', 'animate-slideInDown');
                    layoutUtils.toggleClass(button, 'collapsed');
                }
            });
        });
    },

    setupDropdowns() {
        const dropdowns = document.querySelectorAll('.dropdown');

        dropdowns.forEach(dropdown => {
            const toggle = dropdown.querySelector('.dropdown-toggle');
            const menu = dropdown.querySelector('.dropdown-menu');

            if (toggle && menu) {
                toggle.addEventListener('click', e => {
                    e.preventDefault();
                    this.toggleDropdown(dropdown);
                });

                document.addEventListener('click', e => {
                    if (!dropdown.contains(e.target)) {
                        this.closeDropdown(dropdown);
                    }
                });
            }
        });
    },

    toggleDropdown(dropdown) {
        const menu = dropdown.querySelector('.dropdown-menu');
        layoutUtils.toggleClass(dropdown, 'show');
        layoutUtils.toggleClass(menu, 'show', 'animate-slideInDown');
    },

    closeDropdown(dropdown) {
        const menu = dropdown.querySelector('.dropdown-menu');
        layoutUtils.removeClass(dropdown, 'show');
        layoutUtils.removeClass(menu, 'show');
    },

    setupScrollSpy() {
        if (!config.enableScrollSpy) return;

        const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
        const sections = Array.from(navLinks)
            .map(link => {
                const href = link.getAttribute('href');
                return href !== '#' ? document.querySelector(href) : null;
            })
            .filter(section => section);

        const handleScroll = layoutUtils.throttle(() => {
            const scrollTop = window.pageYOffset;

            sections.forEach((section, index) => {
                const offset = layoutUtils.getElementOffset(section);
                const link = navLinks[index];

                if (
                    scrollTop >= offset.top - 100 &&
                    scrollTop < offset.top + section.offsetHeight - 100
                ) {
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            });
        }, 100);

        window.addEventListener('scroll', handleScroll);
    }
};

components.Modal = {
    init() {
        this.setupModalTriggers();
        this.setupKeyboardHandlers();
    },

    setupModalTriggers() {
        const modalTriggers = document.querySelectorAll('[data-bs-toggle="modal"]');

        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', e => {
                e.preventDefault();
                const target = document.querySelector(trigger.getAttribute('data-bs-target'));

                if (target) {
                    this.showModal(target);
                }
            });
        });

        const closeButtons = document.querySelectorAll('[data-bs-dismiss="modal"]');
        closeButtons.forEach(button => {
            button.addEventListener('click', e => {
                e.preventDefault();
                const modal = button.closest('.modal');
                if (modal) {
                    this.hideModal(modal);
                }
            });
        });

        document.addEventListener('click', e => {
            if (e.target.classList.contains('modal')) {
                this.hideModal(e.target);
            }
        });
    },

    showModal(modal) {
        const backdrop = document.createElement('div');
        backdrop.className = 'modal-backdrop';
        backdrop.setAttribute('data-modal-id', modal.id);
        document.body.appendChild(backdrop);

        modal.style.display = 'block';
        document.body.classList.add('modal-open');

        setTimeout(() => {
            modal.classList.add('show');
            backdrop.classList.add('show');
        }, 10);

        const firstFocusable = modal.querySelector(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"]')
        );
        if (firstFocusable) {
            firstFocusable.focus();
        }

        events.trigger('modal.show', { modal });
    },

    hideModal(modal) {
        const backdrop = document.querySelector(`[data-modal-id="${modal.id}"]`);

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

        events.trigger('modal.hide', { modal });
    },

    setupKeyboardHandlers() {
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape') {
                const openModal = document.querySelector('.modal.show');
                if (openModal) {
                    this.hideModal(openModal);
                }
            }
        });
    }
};

components.Accordion = {
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

components.LazyLoading = {
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

components.TouchSupport = {
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

components.BreakpointHandler = {
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

components.FormEnhancement = {
    init() {
        this.setupValidation();
        this.setupFloatingLabels();
        this.setupFileInputs();
    },

    setupValidation() {
        const forms = document.querySelectorAll('.needs-validation');

        forms.forEach(form => {
            form.addEventListener('submit', e => {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }

                form.classList.add('was-validated');
            });
        });
    },

    setupFloatingLabels() {
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

            updateLabel();
        });
    },

    setupFileInputs() {
        const fileInputs = document.querySelectorAll('input[type="file"]');

        fileInputs.forEach(input => {
            input.addEventListener('change', e => {
                const files = e.target.files;
                const label = input.nextElementSibling;

                if (files.length > 0) {
                    const fileName =
                        files.length === 1 ? files[0].name : `${files.length} files selected`;
                    if (label) {
                        label.textContent = fileName;
                    }
                }
            });
        });
    }
};

export function initializeComponents() {
    Object.keys(components).forEach(name => {
        const component = components[name];
        if (component && typeof component.init === 'function') {
            component.init();
        }
    });
}

