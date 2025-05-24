/**
 * MKS Overlay Menu JavaScript - Neues Design
 * Version: 3.0
 * Vereinfacht und optimiert für die neue Layout-Struktur
 */

'use strict';

class MKSOverlayMenu {
    constructor() {
        // DOM Elements
        this.overlay = document.getElementById('overlayMenu');
        this.trigger = document.querySelector('.mks-overlay-trigger');
        this.closeBtn = document.querySelector('.mks-overlay-close');
        this.content = document.querySelector('.mks-overlay-content');
        
        // State
        this.isOpen = false;
        this.isAnimating = false;
        this.lastFocusedElement = null;
        
        // Configuration
        this.config = {
            animationDuration: 300,
            enableEscapeKey: true,
            enableClickOutside: true,
            preventBodyScroll: true
        };
        
        // Initialize
        this.init();
    }
    
    /**
     * Initialize the overlay menu
     */
    init() {
        if (!this.overlay || !this.trigger) {
            console.warn('[MKS Overlay Menu] Required elements not found');
            return;
        }
        
        this.bindEvents();
        this.setupAccessibility();
        this.setupStatistics();
        
        console.info('[MKS Overlay Menu] Initialized successfully');
    }
    
    /**
     * Bind all event listeners
     */
    bindEvents() {
        // Trigger button
        this.trigger.addEventListener('click', this.handleTriggerClick.bind(this));
        
        // Close button
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', this.handleCloseClick.bind(this));
        }
        
        // Backdrop click (outside content)
        if (this.config.enableClickOutside) {
            this.overlay.addEventListener('click', this.handleBackdropClick.bind(this));
        }
        
        // Keyboard events
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
        
        // Window resize
        window.addEventListener('resize', this.handleResize.bind(this));
        
        // Loading states for navigation items
        this.setupLoadingStates();
        
        // Form submissions
        this.setupFormHandlers();
    }
    
    /**
     * Setup accessibility features
     */
    setupAccessibility() {
        // ARIA attributes
        this.trigger.setAttribute('aria-controls', 'overlayMenu');
        this.trigger.setAttribute('aria-expanded', 'false');
        this.overlay.setAttribute('role', 'dialog');
        this.overlay.setAttribute('aria-modal', 'true');
        this.overlay.setAttribute('aria-hidden', 'true');
        this.overlay.setAttribute('aria-labelledby', 'overlay-title');
        
        // Focus management
        this.updateFocusableElements();
    }
    
    /**
     * Setup statistics functionality
     */
    setupStatistics() {
        const statCards = document.querySelectorAll('.mks-overlay-stat-card');
        
        statCards.forEach(card => {
            // Skip disabled cards
            if (card.classList.contains('disabled-stat')) {
                return;
            }
            
            // Click handlers
            card.addEventListener('click', this.handleStatCardClick.bind(this));
            
            // Keyboard handlers for accessibility
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.handleStatCardClick(e);
                }
            });
        });
    }
    
    /**
     * Setup loading states for navigation items
     */
    setupLoadingStates() {
        const navItems = document.querySelectorAll('.mks-overlay-nav-item');
        
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                // Skip for external links or hash links
                const href = item.getAttribute('href');
                if (!href || href.startsWith('#') || item.target === '_blank') return;
                
                // Add loading state
                item.classList.add('loading');
                
                // Remove loading state after navigation
                setTimeout(() => {
                    item.classList.remove('loading');
                }, 600);
            });
        });
    }
    
    /**
     * Setup form handlers
     */
    setupFormHandlers() {
        const forms = this.overlay.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.classList.add('loading');
                    submitBtn.disabled = true;
                }
            });
        });
    }
    
    /**
     * Handle trigger button click
     */
    handleTriggerClick(e) {
        e.preventDefault();
        e.stopPropagation();
        
        if (this.isAnimating) return;
        
        this.toggle();
    }
    
    /**
     * Handle close button click
     */
    handleCloseClick(e) {
        e.preventDefault();
        e.stopPropagation();
        
        if (this.isAnimating) return;
        
        this.close();
    }
    
    /**
     * Handle backdrop click (outside content area)
     */
    handleBackdropClick(e) {
        // Only close if clicking the overlay background, not the content
        if (e.target === this.overlay) {
            this.close();
        }
    }
    
    /**
     * Handle keyboard events
     */
    handleKeyDown(e) {
        if (!this.isOpen) return;
        
        switch (e.key) {
            case 'Escape':
                if (this.config.enableEscapeKey) {
                    e.preventDefault();
                    this.close();
                }
                break;
                
            case 'Tab':
                this.handleTabNavigation(e);
                break;
        }
    }
    
    /**
     * Handle tab navigation for focus trapping
     */
    handleTabNavigation(e) {
        if (!this.focusableElements || this.focusableElements.length === 0) return;
        
        const firstFocusable = this.focusableElements[0];
        const lastFocusable = this.focusableElements[this.focusableElements.length - 1];
        
        if (e.shiftKey) {
            // Shift + Tab (backward)
            if (document.activeElement === firstFocusable) {
                e.preventDefault();
                lastFocusable.focus();
            }
        } else {
            // Tab (forward)
            if (document.activeElement === lastFocusable) {
                e.preventDefault();
                firstFocusable.focus();
            }
        }
    }
    
    /**
     * Handle window resize
     */
    handleResize() {
        if (this.isOpen) {
            this.updateFocusableElements();
        }
    }
    
    /**
     * Update focusable elements for focus trapping
     */
    updateFocusableElements() {
        if (!this.overlay) return;
        
        const focusableSelector = [
            'button:not([disabled]):not([inert])',
            '[href]:not([disabled]):not([inert])',
            'input:not([disabled]):not([inert])',
            'select:not([disabled]):not([inert])',
            'textarea:not([disabled]):not([inert])',
            '[tabindex]:not([tabindex="-1"]):not([disabled]):not([inert])',
            '[contenteditable]:not([disabled]):not([inert])'
        ].join(', ');
        
        this.focusableElements = Array.from(
            this.overlay.querySelectorAll(focusableSelector)
        ).filter(el => {
            // Check visibility
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && rect.height > 0 && 
                   window.getComputedStyle(el).visibility !== 'hidden';
        });
    }
    
    /**
     * Handle stat card clicks
     */
    handleStatCardClick(e) {
        const card = e.currentTarget;
        const cardId = card.id;
        
        // Prevent multiple clicks during loading
        if (card.classList.contains('loading')) return;
        
        // Add loading state
        card.classList.add('loading');
        
        // Analytics tracking (if available)
        if (typeof gtag !== 'undefined') {
            gtag('event', 'stat_card_clicked', {
                'event_category': 'dashboard',
                'event_label': cardId
            });
        }
        
        // Remove loading state after a delay
        setTimeout(() => {
            card.classList.remove('loading');
        }, 800);
        
        // Navigate based on card type
        let targetUrl = '';
        
        switch (cardId) {
            case 'new-registrations':
                targetUrl = this.getUrlByName('get_controlling_students') || '/controlling/students';
                break;
            case 'recent-blogs':
                targetUrl = this.getUrlByName('show_blogs_editing') || '/blogedit/summary';
                break;
            case 'gallery-images':
                targetUrl = this.getUrlByName('gallery_admin') || '/galerie/admin/';
                break;
            case 'website-visits':
                // Show info modal
                this.showInfoModal('Website-Statistiken', 
                    'Detaillierte Analytics sind über das Dashboard verfügbar.');
                return;
        }
        
        if (targetUrl) {
            setTimeout(() => {
                this.close(() => {
                    window.location.href = targetUrl;
                });
            }, 200);
        }
    }
    
    /**
     * Get URL by Django URL name (fallback approach)
     */
    getUrlByName(urlName) {
        // This is a simple fallback - in a real implementation,
        // you might want to expose Django URLs to JavaScript
        const urlMap = {
            'get_controlling_students': '/controlling/students',
            'show_blogs_editing': '/blogedit/summary',
            'gallery_admin': '/galerie/admin/',
            'event_managing_view': '/team/events'
        };
        return urlMap[urlName];
    }
    
    /**
     * Show info modal for stats that don't have direct links
     */
    showInfoModal(title, content) {
        // Create a simple modal
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10001;
            backdrop-filter: blur(4px);
        `;
        
        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background: white;
            padding: 2rem;
            border-radius: 12px;
            max-width: 400px;
            width: 90%;
            text-align: center;
            box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1);
        `;
        
        modalContent.innerHTML = `
            <h4 style="margin: 0 0 1rem 0; color: #111827; font-family: var(--mks-font-family);">${this.escapeHtml(title)}</h4>
            <p style="margin: 0 0 1.5rem 0; color: #4b5563; font-size: 0.875rem;">${this.escapeHtml(content)}</p>
            <button style="
                background: #d11317; 
                color: white; 
                border: none; 
                padding: 0.75rem 2rem; 
                border-radius: 8px; 
                cursor: pointer; 
                font-weight: 600;
                font-size: 0.875rem;
                transition: all 0.2s ease-in-out;
            ">Schließen</button>
        `;
        
        modal.appendChild(modalContent);
        document.body.appendChild(modal);
        
        // Close handlers
        const closeBtn = modalContent.querySelector('button');
        const closeModal = () => {
            modal.remove();
        };
        
        closeBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
        
        // Auto-close after 5 seconds
        setTimeout(closeModal, 5000);
        
        // Focus the close button
        closeBtn.focus();
    }
    
    /**
     * Open the overlay menu
     */
    open(callback) {
        if (this.isOpen || this.isAnimating) return;
        
        this.isAnimating = true;
        this.isOpen = true;
        this.lastFocusedElement = document.activeElement;
        
        // Update DOM
        this.overlay.classList.add('is-open');
        this.overlay.setAttribute('aria-hidden', 'false');
        this.trigger.setAttribute('aria-expanded', 'true');
        
        // Prevent body scroll
        if (this.config.preventBodyScroll) {
            document.body.style.overflow = 'hidden';
        }
        
        // Update focusable elements
        this.updateFocusableElements();
        
        // Focus management - focus the close button
        setTimeout(() => {
            if (this.closeBtn) {
                this.closeBtn.focus();
            }
        }, 50);
        
        // Animation complete
        setTimeout(() => {
            this.isAnimating = false;
            if (callback) callback();
        }, this.config.animationDuration);
        
        // Custom event
        this.dispatchEvent('mksOverlayOpened');
    }
    
    /**
     * Close the overlay menu
     */
    close(callback) {
        if (!this.isOpen || this.isAnimating) return;
        
        this.isAnimating = true;
        this.isOpen = false;
        
        // Update DOM
        this.overlay.classList.remove('is-open');
        this.overlay.setAttribute('aria-hidden', 'true');
        this.trigger.setAttribute('aria-expanded', 'false');
        
        // Restore body scroll
        if (this.config.preventBodyScroll) {
            document.body.style.overflow = '';
        }
        
        // Animation complete
        setTimeout(() => {
            this.isAnimating = false;
            
            // Restore focus to trigger element
            if (this.lastFocusedElement && this.lastFocusedElement.focus) {
                this.lastFocusedElement.focus();
            }
            
            if (callback) callback();
        }, this.config.animationDuration);
        
        // Custom event
        this.dispatchEvent('mksOverlayClosed');
    }
    
    /**
     * Toggle the overlay menu
     */
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    /**
     * Dispatch custom event
     */
    dispatchEvent(eventName, detail = {}) {
        const event = new CustomEvent(eventName, {
            detail: { overlay: this, ...detail },
            bubbles: true,
            cancelable: true
        });
        document.dispatchEvent(event);
    }
    
    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    /**
     * Destroy the overlay menu instance
     */
    destroy() {
        // Remove event listeners
        this.trigger?.removeEventListener('click', this.handleTriggerClick);
        this.closeBtn?.removeEventListener('click', this.handleCloseClick);
        this.overlay?.removeEventListener('click', this.handleBackdropClick);
        document.removeEventListener('keydown', this.handleKeyDown);
        window.removeEventListener('resize', this.handleResize);
        
        // Reset states
        this.isOpen = false;
        this.isAnimating = false;
        
        // Restore body scroll
        document.body.style.overflow = '';
        
        console.info('[MKS Overlay Menu] Destroyed');
    }
}

// Auto-initialization
function initMKSOverlayMenu() {
    // Check if already initialized
    if (window.mksOverlayMenu) {
        window.mksOverlayMenu.destroy();
    }
    
    // Initialize new instance
    window.mksOverlayMenu = new MKSOverlayMenu();
    
    // Setup global API
    window.MKS = window.MKS || {};
    window.MKS.OverlayMenu = {
        open: () => window.mksOverlayMenu.open(),
        close: () => window.mksOverlayMenu.close(),
        toggle: () => window.mksOverlayMenu.toggle(),
        isOpen: () => window.mksOverlayMenu.isOpen
    };
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMKSOverlayMenu);
} else {
    initMKSOverlayMenu();
}

// Re-initialize on navigation (SPA support)
window.addEventListener('popstate', initMKSOverlayMenu);

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.mksOverlayMenu) {
        window.mksOverlayMenu.destroy();
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MKSOverlayMenu;
} else if (typeof define === 'function' && define.amd) {
    define([], () => MKSOverlayMenu);
}
