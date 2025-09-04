import { layoutUtils } from './layout.js';
import { events } from './events.js';
import { config } from './config.js';

export const Navigation = {
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

