export const dom = {
    ready(callback) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', callback);
        } else {
            callback();
        }
    },

    createElement(tag, attributes, content) {
        const element = document.createElement(tag);

        if (attributes) {
            Object.keys(attributes).forEach(key => {
                if (key === 'className') {
                    element.className = attributes[key];
                } else if (key === 'textContent') {
                    element.textContent = attributes[key];
                } else {
                    element.setAttribute(key, attributes[key]);
                }
            });
        }

        if (content) {
            if (typeof content === 'string') {
                element.textContent = content;
            } else if (content instanceof HTMLElement) {
                element.appendChild(content);
            } else if (Array.isArray(content)) {
                content.forEach(item => element.appendChild(item));
            }
        }

        return element;
    },

    addClass(element, className, animationClass = null) {
        if (element.classList) {
            if (!element.classList.contains(className)) {
                element.classList.add(className);
                if (animationClass) {
                    element.classList.add(animationClass);
                    setTimeout(() => element.classList.remove(animationClass), 300);
                }
            }
        } else {
            element.className += ' ' + className;
        }
    },

    removeClass(element, className, animationClass = null) {
        if (element.classList) {
            if (element.classList.contains(className)) {
                if (animationClass) {
                    element.classList.add(animationClass);
                    setTimeout(() => {
                        element.classList.remove(className);
                        element.classList.remove(animationClass);
                    }, 300);
                } else {
                    element.classList.remove(className);
                }
            }
        } else {
            element.className = element.className.replace(
                new RegExp('(^|\b)' + className.split(' ').join('|') + '(\b|$)', 'gi'),
                ' '
            );
        }
    },

    hasClass(element, className) {
        if (element.classList) {
            return element.classList.contains(className);
        }
        return new RegExp('(^| )' + className + '( |$)', 'gi').test(element.className);
    },

    toggleClass(element, className, animationClass = null) {
        if (this.hasClass(element, className)) {
            this.removeClass(element, className, animationClass);
        } else {
            this.addClass(element, className, animationClass);
        }
    }
};

export function createEventBus() {
    const listeners = {};
    return {
        on(event, callback) {
            if (!listeners[event]) {
                listeners[event] = [];
            }
            listeners[event].push(callback);
        },
        off(event, callback) {
            if (!listeners[event]) return;
            const index = listeners[event].indexOf(callback);
            if (index > -1) {
                listeners[event].splice(index, 1);
            }
        },
        emit(event, data) {
            if (listeners[event]) {
                listeners[event].forEach(callback => {
                    try {
                        callback(data);
                    } catch (error) {
                        console.error('Error in event listener:', error);
                    }
                });
            }
        },
        trigger(event, data) {
            this.emit(event, data);
        }
    };
}
