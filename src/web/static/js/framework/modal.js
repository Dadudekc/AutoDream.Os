import { layoutUtils } from './layout.js';
import { events } from './events.js';

export const Modal = {
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

