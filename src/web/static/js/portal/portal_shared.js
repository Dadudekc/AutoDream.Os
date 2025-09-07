/**
 * Shared Portal Utilities
 * Provides common helper functions for both PortalFramework and PortalComponents.
 */
(function() {
    'use strict';

    window.PortalShared = {
        utils: {
            // DOM utilities
            dom: {
                ready: function(callback) {
                    if (document.readyState === 'loading') {
                        document.addEventListener('DOMContentLoaded', callback);
                    } else {
                        callback();
                    }
                },
                createElement: function(tag, attributes, content) {
                    const element = document.createElement(tag);
                    if (attributes) {
                        Object.keys(attributes).forEach(function(key) {
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
                            content.forEach(function(item) {
                                element.appendChild(item);
                            });
                        }
                    }
                    return element;
                },
                addClass: function(element, className) {
                    if (element.classList) {
                        element.classList.add(className);
                    } else {
                        element.className += ' ' + className;
                    }
                },
                removeClass: function(element, className) {
                    if (element.classList) {
                        element.classList.remove(className);
                    } else {
                        element.className = element.className.replace(
                            new RegExp('(^|\\b)' + className.split(' ').join('|') + '(\\b|$)', 'gi'), ' '
                        );
                    }
                },
                hasClass: function(element, className) {
                    if (element.classList) {
                        return element.classList.contains(className);
                    } else {
                        return new RegExp('(^| )' + className + '( |$)', 'gi').test(element.className);
                    }
                },
                toggleClass: function(element, className) {
                    if (this.hasClass(element, className)) {
                        this.removeClass(element, className);
                    } else {
                        this.addClass(element, className);
                    }
                }
            },

            // Storage utilities
            storage: {
                set: function(key, value) {
                    try {
                        localStorage.setItem(key, JSON.stringify(value));
                    } catch (error) {
                        console.warn('Could not save to localStorage:', error);
                    }
                },
                get: function(key, defaultValue) {
                    try {
                        const item = localStorage.getItem(key);
                        return item ? JSON.parse(item) : defaultValue;
                    } catch (error) {
                        console.warn('Could not read from localStorage:', error);
                        return defaultValue;
                    }
                },
                remove: function(key) {
                    try {
                        localStorage.removeItem(key);
                    } catch (error) {
                        console.warn('Could not remove from localStorage:', error);
                    }
                }
            },

            // HTTP utilities
            http: {
                get: function(url, options) {
                    return this.request('GET', url, options);
                },
                post: function(url, data, options) {
                    return this.request('POST', url, { ...options, data });
                },
                put: function(url, data, options) {
                    return this.request('PUT', url, { ...options, data });
                },
                delete: function(url, options) {
                    return this.request('DELETE', url, options);
                },
                request: function(method, url, options = {}) {
                    return new Promise(function(resolve, reject) {
                        const xhr = new XMLHttpRequest();
                        xhr.open(method, url);
                        if (options.headers) {
                            Object.keys(options.headers).forEach(function(key) {
                                xhr.setRequestHeader(key, options.headers[key]);
                            });
                        }
                        if (options.responseType) {
                            xhr.responseType = options.responseType;
                        }
                        xhr.onload = function() {
                            if (xhr.status >= 200 && xhr.status < 300) {
                                try {
                                    const response = xhr.responseType === 'json' ? xhr.response : JSON.parse(xhr.response);
                                    resolve(response);
                                } catch (error) {
                                    resolve(xhr.response);
                                }
                            } else {
                                reject(new Error(`HTTP ${xhr.status}: ${xhr.statusText}`));
                            }
                        };
                        xhr.onerror = function() {
                            reject(new Error('Network error'));
                        };
                        if (options.timeout) {
                            xhr.timeout = options.timeout;
                            xhr.ontimeout = function() {
                                reject(new Error('Request timeout'));
                            };
                        }
                        if (options.data && method !== 'GET') {
                            xhr.send(JSON.stringify(options.data));
                        } else {
                            xhr.send();
                        }
                    });
                }
            },

            // Time utilities
            time: {
                formatRelative: function(timestamp) {
                    const now = new Date();
                    const date = new Date(timestamp);
                    const diff = now - date;
                    const seconds = Math.floor(diff / 1000);
                    const minutes = Math.floor(seconds / 60);
                    const hours = Math.floor(minutes / 60);
                    const days = Math.floor(hours / 24);
                    if (days > 0) {
                        return days === 1 ? '1 day ago' : `${days} days ago`;
                    } else if (hours > 0) {
                        return hours === 1 ? '1 hour ago' : `${hours} hours ago`;
                    } else if (minutes > 0) {
                        return minutes === 1 ? '1 minute ago' : `${minutes} minutes ago`;
                    } else {
                        return 'Just now';
                    }
                },
                formatDate: function(timestamp, format = 'YYYY-MM-DD HH:mm:ss') {
                    const date = new Date(timestamp);
                    const year = date.getFullYear();
                    const month = String(date.getMonth() + 1).padStart(2, '0');
                    const day = String(date.getDate()).padStart(2, '0');
                    const hours = String(date.getHours()).padStart(2, '0');
                    const minutes = String(date.getMinutes()).padStart(2, '0');
                    const seconds = String(date.getSeconds()).padStart(2, '0');
                    return format
                        .replace('YYYY', year)
                        .replace('MM', month)
                        .replace('DD', day)
                        .replace('HH', hours)
                        .replace('mm', minutes)
                        .replace('ss', seconds);
                }
            },

            // Validation utilities
            validation: {
                isEmail: function(email) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    return emailRegex.test(email);
                },
                isUrl: function(url) {
                    try {
                        new URL(url);
                        return true;
                    } catch {
                        return false;
                    }
                },
                isRequired: function(value) {
                    return value !== null && value !== undefined && value !== '';
                },
                minLength: function(value, min) {
                    return value && value.length >= min;
                },
                maxLength: function(value, max) {
                    return value && value.length <= max;
                }
            },

            // Formatting utilities
            formatNumber: function(number, decimals = 2) {
                if (number >= 1000000) {
                    return (number / 1000000).toFixed(decimals) + 'M';
                } else if (number >= 1000) {
                    return (number / 1000).toFixed(decimals) + 'K';
                } else {
                    return number.toString();
                }
            },
            formatFileSize: function(bytes) {
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
            },
            formatDuration: function(seconds) {
                if (seconds < 60) {
                    return seconds + 's';
                } else if (seconds < 3600) {
                    const minutes = Math.floor(seconds / 60);
                    const remainingSeconds = seconds % 60;
                    return minutes + 'm ' + remainingSeconds + 's';
                } else {
                    const hours = Math.floor(seconds / 3600);
                    const remainingMinutes = Math.floor((seconds % 3600) / 60);
                    return hours + 'h ' + remainingMinutes + 'm';
                }
            },

            // Helper functions
            debounce: function(func, wait) {
                let timeout;
                return function executedFunction(...args) {
                    const later = function() {
                        clearTimeout(timeout);
                        func(...args);
                    };
                    clearTimeout(timeout);
                    timeout = setTimeout(later, wait);
                };
            },
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
            }
        }
    };
})();
