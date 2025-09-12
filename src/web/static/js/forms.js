import { layoutUtils } from './layout.js';

export const FormEnhancement = {
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
