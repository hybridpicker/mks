/* ================================================
   MKS Management JavaScript
   Core functionality for management interface
   ================================================ */

(function() {
    'use strict';

    // Management namespace
    window.MKSManagement = window.MKSManagement || {};

    // Configuration
    const Config = {
        selectors: {
            container: '.mks-manage-container',
            mobileToggle: '#mks-manage-mobile-toggle',
            sidebar: '#mks-manage-sidebar',
            overlay: '#mks-manage-overlay',
            messageClose: '.mks-manage-message-close'
        },
        classes: {
            sidebarOpen: 'mks-manage-open',
            overlayActive: 'mks-manage-active',
            collapsed: 'mks-manage-collapsed',
            loading: 'mks-manage-loading'
        },
        breakpoints: {
            mobile: 768,
            tablet: 1024
        }
    };

    // Utility functions
    const Utils = {
        // Get element by selector
        getElement: function(selector) {
            return document.querySelector(selector);
        },

        // Get all elements by selector
        getElements: function(selector) {
            return document.querySelectorAll(selector);
        },

        // Add event listener with delegation
        on: function(selector, event, handler, parent = document) {
            parent.addEventListener(event, function(e) {
                if (e.target.matches(selector) || e.target.closest(selector)) {
                    handler.call(e.target.closest(selector), e);
                }
            });
        },

        // Toggle class
        toggleClass: function(element, className) {
            if (!element) return;
            element.classList.toggle(className);
        },

        // Add class
        addClass: function(element, className) {
            if (!element) return;
            element.classList.add(className);
        },

        // Remove class
        removeClass: function(element, className) {
            if (!element) return;
            element.classList.remove(className);
        },

        // Check if element has class
        hasClass: function(element, className) {
            if (!element) return false;
            return element.classList.contains(className);
        },

        // Get window width
        getWindowWidth: function() {
            return window.innerWidth || document.documentElement.clientWidth;
        },

        // Debounce function
        debounce: function(func, wait) {
            let timeout;
            return function(...args) {
                clearTimeout(timeout);
                timeout = setTimeout(() => func.apply(this, args), wait);
            };
        },

        // Show loading state
        showLoading: function(element) {
            if (!element) return;
            this.addClass(element, Config.classes.loading);
        },

        // Hide loading state
        hideLoading: function(element) {
            if (!element) return;
            this.removeClass(element, Config.classes.loading);
        },

        // Show notification
        showNotification: function(message, type = 'info', duration = 5000) {
            const notification = document.createElement('div');
            notification.className = `mks-manage-notification mks-manage-notification-${type}`;
            notification.innerHTML = `
                <span class="mks-manage-notification-message">${message}</span>
                <button class="mks-manage-notification-close">&times;</button>
            `;

            // Add to body
            document.body.appendChild(notification);

            // Auto-remove after duration
            if (duration > 0) {
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, duration);
            }

            // Manual close
            const closeBtn = notification.querySelector('.mks-manage-notification-close');
            closeBtn.addEventListener('click', () => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            });

            return notification;
        }
    };

    // Mobile Navigation Controller
    const MobileNav = {
        init: function() {
            this.bindEvents();
            this.handleResize();
        },

        bindEvents: function() {
            const mobileToggle = Utils.getElement(Config.selectors.mobileToggle);
            const overlay = Utils.getElement(Config.selectors.overlay);

            if (mobileToggle) {
                mobileToggle.addEventListener('click', this.toggleSidebar.bind(this));
            }

            if (overlay) {
                overlay.addEventListener('click', this.closeSidebar.bind(this));
            }

            // Handle escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.closeSidebar();
                }
            });

            // Handle window resize
            window.addEventListener('resize', Utils.debounce(this.handleResize.bind(this), 250));
        },

        toggleSidebar: function() {
            const sidebar = Utils.getElement(Config.selectors.sidebar);
            const overlay = Utils.getElement(Config.selectors.overlay);

            if (Utils.hasClass(sidebar, Config.classes.sidebarOpen)) {
                this.closeSidebar();
            } else {
                this.openSidebar();
            }
        },

        openSidebar: function() {
            const sidebar = Utils.getElement(Config.selectors.sidebar);
            const overlay = Utils.getElement(Config.selectors.overlay);

            Utils.addClass(sidebar, Config.classes.sidebarOpen);
            Utils.addClass(overlay, Config.classes.overlayActive);

            // Prevent body scroll
            document.body.style.overflow = 'hidden';
        },

        closeSidebar: function() {
            const sidebar = Utils.getElement(Config.selectors.sidebar);
            const overlay = Utils.getElement(Config.selectors.overlay);

            Utils.removeClass(sidebar, Config.classes.sidebarOpen);
            Utils.removeClass(overlay, Config.classes.overlayActive);

            // Restore body scroll
            document.body.style.overflow = '';
        },

        handleResize: function() {
            // Close sidebar when viewport becomes larger
            if (Utils.getWindowWidth() > Config.breakpoints.mobile) {
                this.closeSidebar();
            }
        }
    };

    // Message Handler
    const MessageHandler = {
        init: function() {
            this.bindEvents();
            this.autoHideMessages();
        },

        bindEvents: function() {
            Utils.on(Config.selectors.messageClose, 'click', this.closeMessage.bind(this));
        },

        closeMessage: function(e) {
            e.preventDefault();
            const message = e.target.closest('.mks-manage-message');
            if (message) {
                this.hideMessage(message);
            }
        },

        hideMessage: function(message) {
            message.style.animation = 'mks-manage-fadeOut 0.3s ease-in-out';
            setTimeout(() => {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            }, 300);
        },

        autoHideMessages: function() {
            const messages = Utils.getElements('.mks-manage-message:not([data-persistent])');
            messages.forEach((message) => {
                setTimeout(() => {
                    this.hideMessage(message);
                }, 5000);
            });
        }
    };

    // CSS Conflict Manager
    const ConflictManager = {
        init: function() {
            this.detectAndNeutralize();
            this.observeChanges();
        },

        // Detect and neutralize problematic CSS classes
        detectAndNeutralize: function() {
            const container = Utils.getElement(Config.selectors.container);
            if (!container) return;

            const problematicSelectors = ['.bs', '.mbs', '.bf'];
            
            problematicSelectors.forEach(selector => {
                const elements = container.querySelectorAll(selector);
                elements.forEach(element => {
                    Utils.addClass(element, 'mks-manage-override');
                    
                    // Log for debugging
                    console.log(`MKS Management: Neutralized problematic class "${selector}" on element:`, element);
                });
            });
        },

        // Observe DOM changes and neutralize new problematic elements
        observeChanges: function() {
            const container = Utils.getElement(Config.selectors.container);
            if (!container || !window.MutationObserver) return;

            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    if (mutation.type === 'childList') {
                        mutation.addedNodes.forEach((node) => {
                            if (node.nodeType === Node.ELEMENT_NODE) {
                                this.neutralizeElement(node);
                            }
                        });
                    }
                });
            });

            observer.observe(container, {
                childList: true,
                subtree: true
            });
        },

        // Neutralize a specific element
        neutralizeElement: function(element) {
            const problematicSelectors = ['.bs', '.mbs', '.bf'];
            
            problematicSelectors.forEach(selector => {
                if (element.matches && element.matches(selector)) {
                    Utils.addClass(element, 'mks-manage-override');
                }
                
                const children = element.querySelectorAll(selector);
                children.forEach(child => {
                    Utils.addClass(child, 'mks-manage-override');
                });
            });
        }
    };

    // AJAX Helper
    const AjaxHelper = {
        // Perform AJAX request
        request: function(options) {
            const defaults = {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            };

            const config = Object.assign(defaults, options);

            // Add CSRF token for non-GET requests
            if (config.method !== 'GET') {
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                if (csrfToken) {
                    config.headers['X-CSRFToken'] = csrfToken.value;
                }
            }

            return fetch(config.url, config)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .catch(error => {
                    console.error('AJAX request failed:', error);
                    Utils.showNotification('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.', 'error');
                    throw error;
                });
        },

        // GET request
        get: function(url, params = {}) {
            const urlParams = new URLSearchParams(params);
            const fullUrl = url + (urlParams.toString() ? '?' + urlParams.toString() : '');
            
            return this.request({
                url: fullUrl,
                method: 'GET'
            });
        },

        // POST request
        post: function(url, data = {}) {
            return this.request({
                url: url,
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        // PUT request
        put: function(url, data = {}) {
            return this.request({
                url: url,
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },

        // DELETE request
        delete: function(url) {
            return this.request({
                url: url,
                method: 'DELETE'
            });
        }
    };

    // Form Handler
    const FormHandler = {
        init: function() {
            this.bindEvents();
        },

        bindEvents: function() {
            // Handle form submissions
            Utils.on('form[data-ajax="true"]', 'submit', this.handleAjaxSubmit.bind(this));
            
            // Handle file inputs
            Utils.on('input[type="file"]', 'change', this.handleFileChange.bind(this));
            
            // Handle form validation
            Utils.on('.mks-manage-form-input', 'blur', this.validateField.bind(this));
        },

        handleAjaxSubmit: function(e) {
            e.preventDefault();
            const form = e.target;
            const submitBtn = form.querySelector('[type="submit"]');
            
            // Show loading state
            Utils.addClass(submitBtn, 'mks-manage-btn-loading');
            Utils.showLoading(form);
            
            const formData = new FormData(form);
            
            fetch(form.action, {
                method: form.method,
                body: formData,
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                Utils.removeClass(submitBtn, 'mks-manage-btn-loading');
                Utils.hideLoading(form);
                
                if (data.success) {
                    Utils.showNotification(data.message || 'Erfolgreich gespeichert!', 'success');
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                } else {
                    Utils.showNotification(data.message || 'Ein Fehler ist aufgetreten.', 'error');
                    this.displayFormErrors(form, data.errors || {});
                }
            })
            .catch(error => {
                Utils.removeClass(submitBtn, 'mks-manage-btn-loading');
                Utils.hideLoading(form);
                Utils.showNotification('Ein unerwarteter Fehler ist aufgetreten.', 'error');
                console.error('Form submission error:', error);
            });
        },

        handleFileChange: function(e) {
            const input = e.target;
            const label = input.nextElementSibling;
            
            if (input.files && input.files.length > 0) {
                const fileName = input.files[0].name;
                const fileText = label.querySelector('.mks-manage-form-file-text');
                if (fileText) {
                    fileText.textContent = fileName;
                }
            }
        },

        validateField: function(e) {
            const field = e.target;
            const value = field.value.trim();
            const required = field.hasAttribute('required');
            const type = field.getAttribute('type');
            
            this.clearFieldErrors(field);
            
            if (required && !value) {
                this.showFieldError(field, 'Dieses Feld ist erforderlich.');
                return false;
            }
            
            if (type === 'email' && value && !this.isValidEmail(value)) {
                this.showFieldError(field, 'Bitte geben Sie eine gültige E-Mail-Adresse ein.');
                return false;
            }
            
            return true;
        },

        clearFieldErrors: function(field) {
            const group = field.closest('.mks-manage-form-group');
            if (group) {
                group.classList.remove('mks-manage-error');
                const errorMsg = group.querySelector('.mks-manage-form-error');
                if (errorMsg) {
                    errorMsg.remove();
                }
            }
        },

        showFieldError: function(field, message) {
            const group = field.closest('.mks-manage-form-group');
            if (group) {
                group.classList.add('mks-manage-error');
                const errorMsg = document.createElement('span');
                errorMsg.className = 'mks-manage-form-error';
                errorMsg.textContent = message;
                field.parentNode.insertBefore(errorMsg, field.nextSibling);
            }
        },

        displayFormErrors: function(form, errors) {
            Object.keys(errors).forEach(fieldName => {
                const field = form.querySelector(`[name="${fieldName}"]`);
                if (field && errors[fieldName].length > 0) {
                    this.showFieldError(field, errors[fieldName][0]);
                }
            });
        },

        isValidEmail: function(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }
    };

    // Keyboard Shortcuts
    const KeyboardShortcuts = {
        init: function() {
            this.bindEvents();
        },

        bindEvents: function() {
            document.addEventListener('keydown', this.handleKeydown.bind(this));
        },

        handleKeydown: function(e) {
            // Only handle shortcuts when not in an input/textarea
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }

            // Ctrl/Cmd + S: Save form
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                const form = document.querySelector('form');
                if (form) {
                    form.dispatchEvent(new Event('submit', { cancelable: true }));
                }
            }

            // Escape: Close modals/sidebars
            if (e.key === 'Escape') {
                MobileNav.closeSidebar();
            }
        }
    };

    // Accessibility Enhancements
    const Accessibility = {
        init: function() {
            this.setupSkipLinks();
            this.enhanceFocusManagement();
            this.setupLiveRegions();
        },

        setupSkipLinks: function() {
            const skipLink = document.createElement('a');
            skipLink.href = '#mks-manage-main-content';
            skipLink.className = 'mks-manage-skip-link';
            skipLink.textContent = 'Zum Hauptinhalt springen';
            skipLink.style.cssText = `
                position: absolute;
                top: -40px;
                left: 6px;
                background: var(--mks-manage-primary);
                color: white;
                padding: 8px;
                text-decoration: none;
                z-index: 1000;
                border-radius: 4px;
            `;
            
            skipLink.addEventListener('focus', () => {
                skipLink.style.top = '6px';
            });
            
            skipLink.addEventListener('blur', () => {
                skipLink.style.top = '-40px';
            });
            
            document.body.insertBefore(skipLink, document.body.firstChild);
        },

        enhanceFocusManagement: function() {
            // Trap focus in modals
            Utils.on('.mks-manage-modal', 'keydown', (e) => {
                if (e.key === 'Tab') {
                    this.trapFocus(e, e.target);
                }
            });
        },

        trapFocus: function(e, container) {
            const focusableElements = container.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];
            
            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        },

        setupLiveRegions: function() {
            // Create live region for dynamic announcements
            const liveRegion = document.createElement('div');
            liveRegion.id = 'mks-manage-live-region';
            liveRegion.setAttribute('aria-live', 'polite');
            liveRegion.style.cssText = `
                position: absolute;
                left: -10000px;
                width: 1px;
                height: 1px;
                overflow: hidden;
            `;
            document.body.appendChild(liveRegion);
        },

        announce: function(message) {
            const liveRegion = document.getElementById('mks-manage-live-region');
            if (liveRegion) {
                liveRegion.textContent = message;
            }
        }
    };

    // Main Management Controller
    const Management = {
        init: function() {
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', this.setup.bind(this));
            } else {
                this.setup();
            }
        },

        setup: function() {
            // Initialize all modules
            MobileNav.init();
            MessageHandler.init();
            ConflictManager.init();
            FormHandler.init();
            KeyboardShortcuts.init();
            Accessibility.init();

            // Create global reference
            window.MKSManagement = {
                Utils: Utils,
                AjaxHelper: AjaxHelper,
                MobileNav: MobileNav,
                MessageHandler: MessageHandler,
                ConflictManager: ConflictManager,
                FormHandler: FormHandler,
                Accessibility: Accessibility
            };

            console.log('MKS Management System initialized successfully');
        }
    };

    // Initialize when script loads
    Management.init();

})();

// CSS animations for notifications and other dynamic elements
const style = document.createElement('style');
style.textContent = `
    @keyframes mks-manage-fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-10px); }
    }
    
    @keyframes mks-manage-fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .mks-manage-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 20px;
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        z-index: 1050;
        max-width: 400px;
        animation: mks-manage-fadeIn 0.3s ease-in-out;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .mks-manage-notification-success {
        border-left: 4px solid var(--mks-manage-success, #00a32a);
        background: #f0f9ff;
    }
    
    .mks-manage-notification-error {
        border-left: 4px solid var(--mks-manage-error, #d63638);
        background: #fffafa;
    }
    
    .mks-manage-notification-warning {
        border-left: 4px solid var(--mks-manage-warning, #dba617);
        background: #fffbf0;
    }
    
    .mks-manage-notification-close {
        margin-left: auto;
        background: none;
        border: none;
        font-size: 18px;
        cursor: pointer;
        opacity: 0.6;
        transition: opacity 0.2s;
    }
    
    .mks-manage-notification-close:hover {
        opacity: 1;
    }
    
    @media (max-width: 768px) {
        .mks-manage-notification {
            left: 20px;
            right: 20px;
            max-width: none;
        }
    }
`;
document.head.appendChild(style);
