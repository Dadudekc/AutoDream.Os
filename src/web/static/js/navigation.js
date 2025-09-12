import { layoutUtils } from './layout.js';
import { events } from './events.js';
import { config } from './config.js';

export const Navigation = {
    mobileMenuOpen: false,
    currentScrollPosition: 0,

    init() {
        this.setupMobileNavigation();
        this.setupDropdowns();
        this.setupScrollSpy();
        this.setupEventListeners();
    },

    setupMobileNavigation() {
        const hamburger = document.querySelector('.hamburger-menu');
        const mobileMenu = document.querySelector('.mobile-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');

        if (hamburger && mobileMenu) {
            hamburger.addEventListener('click', () => {
                this.toggleMobileMenu();
            });
        }

        if (overlay) {
            overlay.addEventListener('click', () => {
                this.closeMobileMenu();
            });
        }

        // Close mobile menu on window resize
        window.addEventListener('resize', layoutUtils.debounce(() => {
            if (window.innerWidth > 768 && this.mobileMenuOpen) {
                this.closeMobileMenu();
            }
        }, 250));
    },

    toggleMobileMenu() {
        const mobileMenu = document.querySelector('.mobile-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');
        const hamburger = document.querySelector('.hamburger-menu');

        if (!mobileMenu) return;

        this.mobileMenuOpen = !this.mobileMenuOpen;

        if (this.mobileMenuOpen) {
            layoutUtils.addClass(mobileMenu, 'active', 'animate-slideInRight');
            layoutUtils.addClass(overlay, 'active');
            layoutUtils.addClass(hamburger, 'active');
            document.body.style.overflow = 'hidden';
        } else {
            this.closeMobileMenu();
        }
    },

    closeMobileMenu() {
        const mobileMenu = document.querySelector('.mobile-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');
        const hamburger = document.querySelector('.hamburger-menu');

        if (mobileMenu) {
            layoutUtils.removeClass(mobileMenu, 'active');
        }
        if (overlay) {
            layoutUtils.removeClass(overlay, 'active');
        }
        if (hamburger) {
            layoutUtils.removeClass(hamburger, 'active');
        }

        this.mobileMenuOpen = false;
        document.body.style.overflow = '';
    },

    setupDropdowns() {
        const dropdowns = document.querySelectorAll('.dropdown-toggle');

        dropdowns.forEach(dropdown => {
            dropdown.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleDropdown(dropdown);
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
                if (!dropdown.parentElement.contains(e.target)) {
                    this.closeDropdown(dropdown);
                }
            });

            // Handle keyboard navigation
            dropdown.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggleDropdown(dropdown);
                } else if (e.key === 'Escape') {
                    this.closeDropdown(dropdown);
                }
            });
        });
    },

    toggleDropdown(dropdown) {
        const menu = dropdown.nextElementSibling;
        const isOpen = dropdown.getAttribute('aria-expanded') === 'true';

        if (isOpen) {
            this.closeDropdown(dropdown);
        } else {
            this.openDropdown(dropdown);
        }
    },

    openDropdown(dropdown) {
        const menu = dropdown.nextElementSibling;
        if (!menu) return;

        dropdown.setAttribute('aria-expanded', 'true');
        layoutUtils.addClass(menu, 'show', 'animate-fadeInDown');
        menu.style.display = 'block';

        // Focus management
        const firstItem = menu.querySelector('a, button');
        if (firstItem) {
            firstItem.focus();
        }
    },

    closeDropdown(dropdown) {
        const menu = dropdown.nextElementSibling;
        if (!menu) return;

        dropdown.setAttribute('aria-expanded', 'false');
        layoutUtils.removeClass(menu, 'show');
        setTimeout(() => {
            menu.style.display = 'none';
        }, 150);
    },

    setupScrollSpy() {
        if (!config.enableScrollSpy) return;

        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

        if (sections.length === 0 || navLinks.length === 0) return;

        const updateActiveLink = layoutUtils.throttle(() => {
            const scrollPosition = window.scrollY + 100;

            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.offsetHeight;
                const sectionId = section.getAttribute('id');

                if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                    navLinks.forEach(link => {
                        link.classList.remove('active');
                        if (link.getAttribute('href') === `#${sectionId}`) {
                            link.classList.add('active');
                        }
                    });
                }
            });
        }, 100);

        window.addEventListener('scroll', updateActiveLink);
        updateActiveLink(); // Initial call
    },

    setupEventListeners() {
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                const targetId = anchor.getAttribute('href');
                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    e.preventDefault();
                    this.smoothScrollTo(targetElement);
                }
            });
        });

        // Handle back/forward navigation
        window.addEventListener('popstate', () => {
            const hash = window.location.hash;
            if (hash) {
                const targetElement = document.querySelector(hash);
                if (targetElement) {
                    this.smoothScrollTo(targetElement);
                }
            }
        });
    },

    smoothScrollTo(element) {
        const headerOffset = 80;
        const elementPosition = element.offsetTop;
        const offsetPosition = elementPosition - headerOffset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    },

    // Public API methods
    goToSection(sectionId) {
        const element = document.getElementById(sectionId);
        if (element) {
            this.smoothScrollTo(element);
        }
    },

    isMobileMenuOpen() {
        return this.mobileMenuOpen;
    }
};
