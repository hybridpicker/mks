/**
 * MKS Overlay Menu JavaScript - Optimiert für das MKS Design System
 * Version: 2.0
 * Entwickelt für: Musikschule Klagenfurt
 * 
 * Features:
 * - Vollständige Accessibility-Unterstützung
 * - Keyboard Navigation
 * - Focus Management
 * - Loading States
 * - Statistics Animation
 * - Touch/Gesture Support
 * - Performance Optimiert
 */

'use strict';

class MKSOverlayMenu {
    constructor() {
        // DOM Elements
        this.overlay = document.getElementById('overlayMenu');
        this.trigger = document.querySelector('.mks-overlay-trigger');
        this.closeBtn = document.querySelector('.mks-overlay-close');
        this.backdrop = document.querySelector('.mks-overlay-backdrop');
        this.content = document.querySelector('.mks-overlay-content');
        
        // State Management
        this.isOpen = false;
        this.isAnimating = false;
        this.focusableElements = [];
        this.lastFocusedElement = null;
        this.touchStartX = 0;
        this.touchStartY = 0;
        
        // Configuration
        this.config = {
            animationDuration: 400,
            swipeThreshold: 100,
            enableSwipeToClose: true,
            enableClickOutside: true,
            enableEscapeKey: true,
            autoCloseDelay: null, // Set to number for auto-close
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
            this.logWarning('MKS Overlay menu elements not found');
            return;
        }
        
        this.bindEvents();
        this.setupAccessibility();
        this.setupStatistics();
        this.setupTouchGestures();
        this.preloadResources();
        
        this.logInfo('MKS Overlay Menu initialized successfully');
    }
    
    /**
     * Bind all event listeners
     */
    bindEvents() {
        // Primary trigger
        this.trigger.addEventListener('click', this.handleTriggerClick.bind(this));
        
        // Close button
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', this.handleCloseClick.bind(this));
        }
        
        // Backdrop click
        if (this.backdrop && this.config.enableClickOutside) {
            this.backdrop.addEventListener('click', this.handleBackdropClick.bind(this));
        }
        
        // Keyboard events
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
        
        // Window events
        window.addEventListener('resize', this.handleResize.bind(this));
        window.addEventListener('orientationchange', this.handleOrientationChange.bind(this));
        
        // Prevent scroll propagation
        if (this.content) {
            this.content.addEventListener('wheel', this.handleContentScroll.bind(this));
            this.content.addEventListener('touchstart', this.handleContentTouchStart.bind(this), { passive: true });
        }
        
        // Loading states for navigation items
        this.setupLoadingStates();
        
        // Form submissions
        this.setupFormHandlers();
        
        // Custom events
        this.setupCustomEvents();
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
        
        // Live region for announcements
        this.createLiveRegion();
        
        // Update focusable elements
        this.updateFocusableElements();
        
        // Screen reader support
        this.setupScreenReaderSupport();
    }
    
    /**
     * Create live region for screen reader announcements
     */
    createLiveRegion() {
        this.liveRegion = document.createElement('div');
        this.liveRegion.setAttribute('aria-live', 'polite');
        this.liveRegion.setAttribute('aria-atomic', 'true');
        this.liveRegion.className = 'sr-only mks-overlay-live-region';
        this.liveRegion.style.cssText = `
            position: absolute !important;
            left: -10000px !important;
            width: 1px !important;
            height: 1px !important;
            overflow: hidden !important;
            clip: rect(1px, 1px, 1px, 1px) !important;
        `;
        document.body.appendChild(this.liveRegion);
    }
    
    /**
     * Setup statistics functionality
     */
    setupStatistics() {
        const statCards = document.querySelectorAll('.mks-overlay-stat-card');
        
        statCards.forEach(card => {
            // Click handlers
            card.addEventListener('click', this.handleStatCardClick.bind(this));
            
            // Keyboard handlers
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.handleStatCardClick(e);
                }
            });
        });
        
        // Auto-update stats when menu opens
        document.addEventListener('mksOverlayOpened', () => {
            this.updateStatistics();
        });
    }
    
    /**
     * Setup touch gesture support
     */
    setupTouchGestures() {
        if (!this.config.enableSwipeToClose || !this.content) return;
        
        let touchStartX = 0;
        let touchStartY = 0;
        let touchStartTime = 0;
        
        this.content.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
            touchStartTime = Date.now();
        }, { passive: true });
        
        this.content.addEventListener('touchmove', (e) => {
            if (!this.isOpen) return;
            
            const touchX = e.touches[0].clientX;
            const touchY = e.touches[0].clientY;
            const diffX = touchStartX - touchX;
            const diffY = Math.abs(touchStartY - touchY);
            
            // Only handle horizontal swipes to the left
            if (diffX > 50 && diffY < 100) {
                const progress = Math.min(diffX / this.config.swipeThreshold, 1);
                this.content.style.transform = `translateX(-${progress * 100}%)`;
            }
        }, { passive: true });
        
        this.content.addEventListener('touchend', (e) => {
            if (!this.isOpen) return;
            
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndTime = Date.now();
            const diffX = touchStartX - touchEndX;
            const swipeSpeed = Math.abs(diffX) / (touchEndTime - touchStartTime);
            
            if (diffX > this.config.swipeThreshold || swipeSpeed > 0.5) {
                this.close();
            } else {
                // Reset transform
                this.content.style.transform = '';
            }
        }, { passive: true });
    }
    
    /**
     * Preload resources for better performance
     */
    preloadResources() {
        // Preload any critical images or fonts if needed
        // This is a placeholder for future optimizations
        
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => {
                this.preloadImages();
            });
        }
    }
    
    /**
     * Preload images used in the overlay
     */
    preloadImages() {
        const images = this.overlay.querySelectorAll('img[data-src]');
        images.forEach(img => {
            const src = img.getAttribute('data-src');
            if (src) {
                const preloadImg = new Image();
                preloadImg.src = src;
                preloadImg.onload = () => {
                    img.src = src;
                    img.removeAttribute('data-src');
                };
            }
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
     * Handle backdrop click
     */
    handleBackdropClick(e) {
        if (e.target === this.backdrop) {
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
                
            case 'Home':
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    this.focusFirstElement();
                }
                break;
                
            case 'End':
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    this.focusLastElement();
                }
                break;
        }
    }
    
    /**
     * Handle tab navigation for focus trapping
     */
    handleTabNavigation(e) {
        if (this.focusableElements.length === 0) return;
        
        const firstFocusable = this.focusableElements[0];
        const lastFocusable = this.focusableElements[this.focusableElements.length - 1];
        
        if (e.shiftKey) {
            // Shift + Tab
            if (document.activeElement === firstFocusable) {
                e.preventDefault();
                lastFocusable.focus();
            }
        } else {
            // Tab
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
            this.adjustLayoutForViewport();
        }
    }
    
    /**
     * Handle orientation change
     */
    handleOrientationChange() {
        setTimeout(() => {
            this.handleResize();
        }, 100);
    }
    
    /**
     * Handle content scroll to prevent propagation
     */
    handleContentScroll(e) {
        e.stopPropagation();
    }
    
    /**
     * Handle content touch start
     */
    handleContentTouchStart(e) {
        // Store initial touch position
        this.touchStartX = e.touches[0].clientX;
        this.touchStartY = e.touches[0].clientY;
    }
    
    /**
     * Update focusable elements
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
            // Additional checks for visibility
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && rect.height > 0 && 
                   window.getComputedStyle(el).visibility !== 'hidden';
        });
    }
    
    /**
     * Setup loading states for navigation items
     */
    setupLoadingStates() {
        const navItems = document.querySelectorAll('.mks-overlay-nav-item');
        
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                // Don't add loading state for links that open in new window
                if (item.target === '_blank') return;
                
                // Don't add loading state for hash links
                const href = item.getAttribute('href');
                if (href && href.startsWith('#')) return;
                
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
     * Setup custom event handlers
     */
    setupCustomEvents() {
        document.addEventListener('mksOverlayOpened', this.handleOverlayOpened.bind(this));
        document.addEventListener('mksOverlayClosed', this.handleOverlayClosed.bind(this));
        
        // External API for opening/closing
        window.addEventListener('mksOpenOverlay', () => this.open());
        window.addEventListener('mksCloseOverlay', () => this.close());
    }
    
    /**
     * Handle overlay opened event
     */
    handleOverlayOpened() {
        // Custom logic when overlay opens
        this.logInfo('Overlay opened');
        
        // Analytics tracking (if available)
        if (typeof gtag !== 'undefined') {
            gtag('event', 'overlay_opened', {
                'event_category': 'navigation',
                'event_label': 'mks_admin_overlay'
            });
        }
    }
    
    /**
     * Handle overlay closed event
     */
    handleOverlayClosed() {
        // Custom logic when overlay closes
        this.logInfo('Overlay closed');
        
        // Analytics tracking (if available)
        if (typeof gtag !== 'undefined') {
            gtag('event', 'overlay_closed', {
                'event_category': 'navigation',
                'event_label': 'mks_admin_overlay'
            });
        }
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
        
        // Analytics tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'stat_card_clicked', {
                'event_category': 'dashboard',
                'event_label': cardId
            });
        }
        
        // Remove loading state
        setTimeout(() => {
            card.classList.remove('loading');
        }, 800);
        
        // Navigation logic
        let targetUrl = '';
        let shouldCloseOverlay = true;
        
        switch (cardId) {
            case 'new-registrations':
                targetUrl = this.getUrlFromElement('get_controlling_students');
                break;
            case 'recent-blogs':
                targetUrl = this.getUrlFromElement('show_blogs_editing');
                break;
            case 'gallery-images':
                targetUrl = this.getUrlFromElement('gallery_admin');
                break;
            case 'website-visits':
                this.showStatsModal('Website-Statistiken', 
                    'Detaillierte Analytics sind über das Dashboard verfügbar. Diese Daten werden aus verschiedenen Quellen zusammengestellt.');
                shouldCloseOverlay = false;
                break;
        }
        
        if (targetUrl) {
            setTimeout(() => {
                if (shouldCloseOverlay) {
                    this.close(() => {
                        window.location.href = targetUrl;
                    });
                } else {
                    window.location.href = targetUrl;
                }
            }, 400);
        }
    }
    
    /**
     * Get URL from Django template tags
     */
    getUrlFromElement(urlName) {
        // This would ideally get the URL from a data attribute set by Django
        // For now, we use a fallback approach
        const urlMap = {
            'get_controlling_students': '/team/controlling/students/',
            'show_blogs_editing': '/blog/manage/',
            'gallery_admin': '/gallery/admin/',
            'event_managing_view': '/events/manage/'
        };
        return urlMap[urlName] || '#';
    }
    
    /**
     * Show stats modal
     */
    showStatsModal(title, content) {
        const modal = this.createStatsModal(title, content);
        document.body.appendChild(modal);
        
        // Focus management
        const closeBtn = modal.querySelector('button');
        if (closeBtn) {
            closeBtn.focus();
        }
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (modal.parentElement) {
                modal.remove();
            }
        }, 10000);
    }
    
    /**
     * Create stats modal element
     */
    createStatsModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'mks-overlay-stats-modal';
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');
        modal.setAttribute('aria-labelledby', 'stats-modal-title');
        
        modal.innerHTML = `
            <div class="mks-overlay-stats-modal-content">
                <h4 id="stats-modal-title">${this.escapeHtml(title)}</h4>
                <p>${this.escapeHtml(content)}</p>
                <button type="button" class="mks-overlay-stats-modal-close">
                    Schließen
                </button>
            </div>
        `;
        
        // Add styles if not already present
        this.ensureStatsModalStyles();
        
        // Bind close event
        const closeBtn = modal.querySelector('.mks-overlay-stats-modal-close');
        closeBtn.addEventListener('click', () => modal.remove());
        
        // Close on backdrop click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
        
        // Close on Escape key
        const handleKeyDown = (e) => {
            if (e.key === 'Escape') {
                modal.remove();
                document.removeEventListener('keydown', handleKeyDown);
            }
        };
        document.addEventListener('keydown', handleKeyDown);
        
        return modal;
    }
    
    /**
     * Ensure stats modal styles are loaded
     */
    ensureStatsModalStyles() {
        if (document.getElementById('mks-stats-modal-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'mks-stats-modal-styles';
        styles.textContent = `
            .mks-overlay-stats-modal {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.6);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10001;
                backdrop-filter: blur(4px);
                animation: mks-modal-fade-in 0.3s ease;
            }
            .mks-overlay-stats-modal-content {
                background: var(--mks-white, #fdfdfd);
                padding: 2rem;
                border-radius: 12px;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
                text-align: center;
                animation: mks-modal-slide-up 0.3s ease;
            }
            .mks-overlay-stats-modal-content h4 {
                color: var(--mks-secondary, #333333);
                font-family: var(--mks-font-family, sans-serif);
                font-size: 1.25rem;
                font-weight: 700;
                margin: 0 0 1rem 0;
            }
            .mks-overlay-stats-modal-content p {
                color: var(--mks-dark-gray, #555555);
                font-family: var(--mks-font-family, sans-serif);
                font-size: 0.875rem;
                line-height: 1.5;
                margin: 0 0 1.5rem 0;
            }
            .mks-overlay-stats-modal-close {
                background: var(--mks-primary, #d11317);
                color: white;
                border: none;
                padding: 0.75rem 2rem;
                border-radius: 8px;
                cursor: pointer;
                font-family: var(--mks-font-family, sans-serif);
                font-weight: 600;
                font-size: 0.875rem;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .mks-overlay-stats-modal-close:hover {
                background: var(--mks-primary-hover, #b01115);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(209, 19, 23, 0.3);
            }
            .mks-overlay-stats-modal-close:focus {
                outline: 3px solid var(--mks-primary, #d11317);
                outline-offset: 2px;
            }
            @keyframes mks-modal-fade-in {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes mks-modal-slide-up {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
        `;
        document.head.appendChild(styles);
    }
    
    /**
     * Update statistics with animation
     */
    updateStatistics() {
        const statCards = document.querySelectorAll('.mks-overlay-stat-card');
        
        statCards.forEach((card, index) => {
            setTimeout(() => {
                this.animateStatCard(card);
            }, index * 150); // Stagger animations
        });
    }
    
    /**
     * Animate individual stat card
     */
    animateStatCard(card) {
        const numberElement = card.querySelector('.mks-overlay-stat-number');
        if (!numberElement) return;
        
        const finalText = numberElement.textContent;
        const finalNumber = parseInt(finalText.replace(/\D/g, ''));
        
        if (isNaN(finalNumber)) return;
        
        // Add loading state
        card.classList.add('loading');
        
        // Animate from 0 to final number
        let current = 0;
        const increment = finalNumber / 50; // 50 steps
        const startTime = Date.now();
        const duration = 1000; // 1 second
        
        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Use easing function for smooth animation
            const easedProgress = this.easeOutCubic(progress);
            current = Math.floor(finalNumber * easedProgress);
            
            // Format number with original formatting
            const formatted = this.formatStatNumber(current, finalText);
            numberElement.textContent = formatted;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                numberElement.textContent = finalText;
                card.classList.remove('loading');
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    /**
     * Format stat number maintaining original formatting
     */
    formatStatNumber(number, originalText) {
        // Check if original had specific formatting
        if (originalText.includes('&nbsp;')) {
            return number.toLocaleString('de-DE').replace(/ /g, '&nbsp;');
        }
        return number.toLocaleString('de-DE');
    }
    
    /**
     * Easing function for animations
     */
    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }
    
    /**
     * Setup screen reader support
     */
    setupScreenReaderSupport() {
        // Add descriptions for complex interactive elements
        const statCards = document.querySelectorAll('.mks-overlay-stat-card');
        statCards.forEach(card => {
            if (!card.getAttribute('aria-describedby')) {
                const description = this.createScreenReaderDescription(card);
                if (description) {
                    const descId = 'desc-' + Math.random().toString(36).substr(2, 9);
                    const descElement = document.createElement('span');
                    descElement.id = descId;
                    descElement.className = 'sr-only';
                    descElement.textContent = description;
                    card.appendChild(descElement);
                    card.setAttribute('aria-describedby', descId);
                }
            }
        });
    }
    
    /**
     * Create screen reader description for stat cards
     */
    createScreenReaderDescription(card) {
        const label = card.querySelector('.mks-overlay-stat-label');
        if (label) {
            return `Klicken Sie hier, um weitere Details zu ${label.textContent} anzuzeigen`;
        }
        return null;
    }
    
    /**
     * Adjust layout for current viewport
     */
    adjustLayoutForViewport() {
        // Add viewport-specific classes
        const viewport = this.getViewportSize();
        this.overlay.className = this.overlay.className.replace(/mks-viewport-\w+/g, '');
        this.overlay.classList.add(`mks-viewport-${viewport}`);
    }
    
    /**
     * Get current viewport size category
     */
    getViewportSize() {
        const width = window.innerWidth;
        if (width < 480) return 'mobile';
        if (width < 768) return 'tablet';
        if (width < 1024) return 'desktop';
        return 'large';
    }
    
    /**
     * Focus first focusable element
     */
    focusFirstElement() {
        if (this.focusableElements.length > 0) {
            this.focusableElements[0].focus();
        }
    }
    
    /**
     * Focus last focusable element
     */
    focusLastElement() {
        if (this.focusableElements.length > 0) {
            this.focusableElements[this.focusableElements.length - 1].focus();
        }
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
            document.body.classList.add('mks-overlay-open');
        }
        
        // Update focusable elements
        this.updateFocusableElements();
        
        // Focus management
        setTimeout(() => {
            if (this.closeBtn) {
                this.closeBtn.focus();
            } else if (this.focusableElements.length > 0) {
                this.focusableElements[0].focus();
            }
        }, 100);
        
        // Adjust layout
        this.adjustLayoutForViewport();
        
        // Animation complete
        setTimeout(() => {
            this.isAnimating = false;
            if (callback) callback();
        }, this.config.animationDuration);
        
        // Screen reader announcement
        this.announceToScreenReader('Verwaltungsmenü geöffnet');
        
        // Custom event
        this.dispatchEvent('mksOverlayOpened');
        
        // Auto-close timer
        if (this.config.autoCloseDelay) {
            this.autoCloseTimer = setTimeout(() => {
                this.close();
            }, this.config.autoCloseDelay);
        }
    }
    
    /**
     * Close the overlay menu
     */
    close(callback) {
        if (!this.isOpen || this.isAnimating) return;
        
        this.isAnimating = true;
        this.isOpen = false;
        
        // Clear auto-close timer
        if (this.autoCloseTimer) {
            clearTimeout(this.autoCloseTimer);
            this.autoCloseTimer = null;
        }
        
        // Update DOM
        this.overlay.classList.remove('is-open');
        this.overlay.setAttribute('aria-hidden', 'true');
        this.trigger.setAttribute('aria-expanded', 'false');
        
        // Restore body scroll
        if (this.config.preventBodyScroll) {
            document.body.style.overflow = '';
            document.body.classList.remove('mks-overlay-open');
        }
        
        // Reset content transform (in case it was modified by touch)
        if (this.content) {
            this.content.style.transform = '';
        }
        
        // Animation complete
        setTimeout(() => {
            this.isAnimating = false;
            
            // Restore focus
            if (this.lastFocusedElement && this.lastFocusedElement.focus) {
                this.lastFocusedElement.focus();
            }
            
            if (callback) callback();
        }, this.config.animationDuration);
        
        // Screen reader announcement
        this.announceToScreenReader('Verwaltungsmenü geschlossen');
        
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
     * Announce to screen readers
     */
    announceToScreenReader(message) {
        if (!this.liveRegion) return;
        
        // Clear previous content
        this.liveRegion.textContent = '';
        
        // Set new content after a small delay
        setTimeout(() => {
            this.liveRegion.textContent = message;
        }, 100);
        
        // Clear content after announcement
        setTimeout(() => {
            this.liveRegion.textContent = '';
        }, 1000);
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
     * Logging utilities
     */
    logInfo(message) {
        if (console && console.info) {
            console.info(`[MKS Overlay Menu] ${message}`);
        }
    }
    
    logWarning(message) {
        if (console && console.warn) {
            console.warn(`[MKS Overlay Menu] ${message}`);
        }
    }
    
    logError(message, error) {
        if (console && console.error) {
            console.error(`[MKS Overlay Menu] ${message}`, error);
        }
    }
    
    /**
     * Destroy the overlay menu instance
     */
    destroy() {
        // Remove event listeners
        this.trigger?.removeEventListener('click', this.handleTriggerClick);
        this.closeBtn?.removeEventListener('click', this.handleCloseClick);
        this.backdrop?.removeEventListener('click', this.handleBackdropClick);
        document.removeEventListener('keydown', this.handleKeyDown);
        window.removeEventListener('resize', this.handleResize);
        window.removeEventListener('orientationchange', this.handleOrientationChange);
        
        // Remove live region
        if (this.liveRegion && this.liveRegion.parentElement) {
            this.liveRegion.parentElement.removeChild(this.liveRegion);
        }
        
        // Clear timers
        if (this.autoCloseTimer) {
            clearTimeout(this.autoCloseTimer);
        }
        
        // Reset states
        this.isOpen = false;
        this.isAnimating = false;
        
        this.logInfo('Overlay menu destroyed');
    }
}

// Auto-initialization when DOM is ready
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

// Re-initialize on page transitions (for SPA-like behavior)
window.addEventListener('popstate', initMKSOverlayMenu);

// Prevent memory leaks on page unload
window.addEventListener('beforeunload', () => {
    if (window.mksOverlayMenu) {
        window.mksOverlayMenu.destroy();
    }
});

// Performance monitoring (optional)
if ('performance' in window && 'measure' in window.performance) {
    document.addEventListener('mksOverlayOpened', () => {
        performance.mark('mks-overlay-opened');
    });
    
    document.addEventListener('mksOverlayClosed', () => {
        performance.mark('mks-overlay-closed');
        performance.measure('mks-overlay-duration', 'mks-overlay-opened', 'mks-overlay-closed');
    });
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MKSOverlayMenu;
} else if (typeof define === 'function' && define.amd) {
    define([], () => MKSOverlayMenu);
}
