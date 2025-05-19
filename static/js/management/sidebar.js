/* ================================================
   MKS Management Sidebar JavaScript
   Handles sidebar navigation and interactions
   ================================================ */

(function() {
    'use strict';

    // Sidebar Controller
    const SidebarController = {
        init: function() {
            this.bindEvents();
            this.setActiveStates();
            this.handleSubmenus();
        },

        bindEvents: function() {
            // Handle submenu toggles
            document.addEventListener('click', (e) => {
                const submenuTrigger = e.target.closest('[data-submenu]');
                if (submenuTrigger) {
                    e.preventDefault();
                    this.toggleSubmenu(submenuTrigger);
                }
            });

            // Handle sidebar collapse (future feature)
            const collapseBtn = document.querySelector('.mks-manage-sidebar-collapse');
            if (collapseBtn) {
                collapseBtn.addEventListener('click', this.toggleSidebarCollapse.bind(this));
            }

            // Handle window resize for responsive behavior
            window.addEventListener('resize', this.handleResize.bind(this));

            // Handle keyboard navigation
            document.addEventListener('keydown', this.handleKeyboardNav.bind(this));
        },

        toggleSubmenu: function(trigger) {
            const submenuId = trigger.getAttribute('data-submenu');
            const submenu = document.getElementById(`submenu-${submenuId}`);
            const arrow = trigger.querySelector('.mks-manage-nav-arrow');
            
            if (!submenu) return;

            const isOpen = submenu.classList.contains('mks-manage-open');
            
            // Close all other submenus (accordion behavior)
            this.closeAllSubmenus();
            
            if (!isOpen) {
                // Open this submenu
                submenu.classList.add('mks-manage-open');
                trigger.setAttribute('aria-expanded', 'true');
                
                if (arrow) {
                    arrow.style.transform = 'rotate(90deg)';
                }
                
                // Animate opening
                submenu.style.maxHeight = submenu.scrollHeight + 'px';
                
                // Focus first link in submenu
                const firstLink = submenu.querySelector('a');
                if (firstLink) {
                    firstLink.focus();
                }
            } else {
                // Close submenu
                this.closeSubmenu(submenu, trigger);
            }
        },

        closeSubmenu: function(submenu, trigger) {
            submenu.classList.remove('mks-manage-open');
            trigger.setAttribute('aria-expanded', 'false');
            
            const arrow = trigger.querySelector('.mks-manage-nav-arrow');
            if (arrow) {
                arrow.style.transform = '';
            }
            
            // Animate closing
            submenu.style.maxHeight = '0';
        },

        closeAllSubmenus: function() {
            const openSubmenus = document.querySelectorAll('.mks-manage-nav-submenu.mks-manage-open');
            openSubmenus.forEach(submenu => {
                const trigger = document.querySelector(`[data-submenu="${submenu.id.replace('submenu-', '')}"]`);
                if (trigger) {
                    this.closeSubmenu(submenu, trigger);
                }
            });
        },

        setActiveStates: function() {
            const currentPath = window.location.pathname;
            const navLinks = document.querySelectorAll('.mks-manage-nav-link, .mks-manage-nav-sublink');
            
            navLinks.forEach(link => {
                const href = link.getAttribute('href');
                if (href && (href === currentPath || currentPath.startsWith(href))) {
                    link.classList.add('mks-manage-active');
                    
                    // If it's a sublink, also open the parent submenu
                    if (link.classList.contains('mks-manage-nav-sublink')) {
                        const submenu = link.closest('.mks-manage-nav-submenu');
                        if (submenu) {
                            const submenuId = submenu.id.replace('submenu-', '');
                            const trigger = document.querySelector(`[data-submenu="${submenuId}"]`);
                            if (trigger) {
                                submenu.classList.add('mks-manage-open');
                                trigger.setAttribute('aria-expanded', 'true');
                                submenu.style.maxHeight = submenu.scrollHeight + 'px';
                                
                                const arrow = trigger.querySelector('.mks-manage-nav-arrow');
                                if (arrow) {
                                    arrow.style.transform = 'rotate(90deg)';
                                }
                            }
                        }
                    }
                }
            });
        },

        toggleSidebarCollapse: function() {
            const sidebar = document.querySelector('.mks-manage-sidebar');
            const main = document.querySelector('.mks-manage-main');
            
            if (!sidebar || !main) return;
            
            const isCollapsed = sidebar.classList.contains('mks-manage-collapsed');
            
            if (isCollapsed) {
                sidebar.classList.remove('mks-manage-collapsed');
                localStorage.setItem('mks-sidebar-collapsed', 'false');
            } else {
                sidebar.classList.add('mks-manage-collapsed');
                localStorage.setItem('mks-sidebar-collapsed', 'true');
                
                // Close all submenus when collapsing
                this.closeAllSubmenus();
            }
        },

        handleResize: function() {
            const windowWidth = window.innerWidth;
            const sidebar = document.querySelector('.mks-manage-sidebar');
            
            // Auto-collapse on smaller screens
            if (windowWidth <= 768) {
                if (sidebar && !sidebar.classList.contains('mks-manage-open')) {
                    // Mobile view - sidebar starts hidden
                }
            } else if (windowWidth > 768) {
                // Desktop view - restore collapsed state from localStorage
                const wasCollapsed = localStorage.getItem('mks-sidebar-collapsed') === 'true';
                if (sidebar) {
                    if (wasCollapsed) {
                        sidebar.classList.add('mks-manage-collapsed');
                    } else {
                        sidebar.classList.remove('mks-manage-collapsed');
                    }
                }
            }
        },

        handleKeyboardNav: function(e) {
            const activeElement = document.activeElement;
            
            // Handle arrow key navigation in sidebar
            if (activeElement && activeElement.closest('.mks-manage-sidebar')) {
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    this.focusNext(activeElement);
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    this.focusPrevious(activeElement);
                } else if (e.key === 'ArrowRight') {
                    // Open submenu if on parent item
                    const trigger = activeElement.closest('[data-submenu]');
                    if (trigger && trigger.getAttribute('aria-expanded') === 'false') {
                        this.toggleSubmenu(trigger);
                    }
                } else if (e.key === 'ArrowLeft') {
                    // Close submenu or go to parent
                    const sublink = activeElement.closest('.mks-manage-nav-sublink');
                    if (sublink) {
                        const submenu = sublink.closest('.mks-manage-nav-submenu');
                        if (submenu) {
                            const submenuId = submenu.id.replace('submenu-', '');
                            const trigger = document.querySelector(`[data-submenu="${submenuId}"]`);
                            if (trigger) {
                                this.closeSubmenu(submenu, trigger);
                                trigger.focus();
                            }
                        }
                    }
                }
            }
        },

        focusNext: function(currentElement) {
            const focusableElements = this.getFocusableElements();
            const currentIndex = focusableElements.indexOf(currentElement);
            const nextIndex = (currentIndex + 1) % focusableElements.length;
            focusableElements[nextIndex].focus();
        },

        focusPrevious: function(currentElement) {
            const focusableElements = this.getFocusableElements();
            const currentIndex = focusableElements.indexOf(currentElement);
            const prevIndex = currentIndex === 0 ? focusableElements.length - 1 : currentIndex - 1;
            focusableElements[prevIndex].focus();
        },

        getFocusableElements: function() {
            const sidebar = document.querySelector('.mks-manage-sidebar');
            if (!sidebar) return [];
            
            const selector = '.mks-manage-nav-link:not([aria-expanded="false"] + .mks-manage-nav-submenu .mks-manage-nav-sublink), .mks-manage-nav-sublink';
            return Array.from(sidebar.querySelectorAll(selector)).filter(el => {
                // Only include visible elements
                return el.offsetHeight > 0;
            });
        },

        // Highlight search results
        highlightSearchResults: function(searchTerm) {
            if (!searchTerm) {
                this.clearHighlights();
                return;
            }
            
            const navLinks = document.querySelectorAll('.mks-manage-nav-link span, .mks-manage-nav-sublink span');
            navLinks.forEach(span => {
                const text = span.textContent;
                const regex = new RegExp(`(${searchTerm})`, 'gi');
                const highlightedText = text.replace(regex, '<mark>$1</mark>');
                span.innerHTML = highlightedText;
            });
        },

        clearHighlights: function() {
            const highlightedElements = document.querySelectorAll('.mks-manage-sidebar mark');
            highlightedElements.forEach(mark => {
                const parent = mark.parentNode;
                parent.replaceChild(document.createTextNode(mark.textContent), mark);
                parent.normalize();
            });
        }
    };

    // Quick Navigation Search
    const QuickSearch = {
        init: function() {
            this.createSearchBox();
            this.bindEvents();
        },

        createSearchBox: function() {
            const sidebarHeader = document.querySelector('.mks-manage-sidebar-header');
            if (!sidebarHeader) return;

            const searchContainer = document.createElement('div');
            searchContainer.className = 'mks-manage-sidebar-search';
            searchContainer.innerHTML = `
                <div class="mks-manage-search-wrapper">
                    <input type="text" 
                           class="mks-manage-search-input" 
                           placeholder="Navigation durchsuchen..." 
                           aria-label="Navigation durchsuchen">
                    <button class="mks-manage-search-clear" 
                            type="button" 
                            aria-label="Suche löschen" 
                            style="display: none;">×</button>
                </div>
            `;

            sidebarHeader.appendChild(searchContainer);

            // Add CSS styles
            const style = document.createElement('style');
            style.textContent = `
                .mks-manage-sidebar-search {
                    padding: 16px 16px 0;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    margin-bottom: 8px;
                }
                
                .mks-manage-search-wrapper {
                    position: relative;
                    display: flex;
                    align-items: center;
                }
                
                .mks-manage-search-input {
                    width: 100%;
                    padding: 8px 12px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 4px;
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                    font-size: 14px;
                    outline: none;
                    transition: all 0.2s ease;
                }
                
                .mks-manage-search-input::placeholder {
                    color: rgba(255, 255, 255, 0.6);
                }
                
                .mks-manage-search-input:focus {
                    border-color: var(--mks-manage-primary-light, #4f94d4);
                    background: rgba(255, 255, 255, 0.15);
                }
                
                .mks-manage-search-clear {
                    position: absolute;
                    right: 8px;
                    background: none;
                    border: none;
                    color: rgba(255, 255, 255, 0.7);
                    cursor: pointer;
                    font-size: 16px;
                    padding: 4px;
                    border-radius: 2px;
                    transition: background-color 0.2s ease;
                }
                
                .mks-manage-search-clear:hover {
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                }
                
                .mks-manage-sidebar mark {
                    background: rgba(255, 193, 7, 0.4);
                    color: inherit;
                    padding: 0 2px;
                    border-radius: 2px;
                }
            `;
            document.head.appendChild(style);
        },

        bindEvents: function() {
            const searchInput = document.querySelector('.mks-manage-search-input');
            const clearButton = document.querySelector('.mks-manage-search-clear');

            if (searchInput) {
                searchInput.addEventListener('input', this.handleSearch.bind(this));
                searchInput.addEventListener('keydown', this.handleKeydown.bind(this));
            }

            if (clearButton) {
                clearButton.addEventListener('click', this.clearSearch.bind(this));
            }
        },

        handleSearch: function(e) {
            const searchTerm = e.target.value.trim();
            const clearButton = document.querySelector('.mks-manage-search-clear');

            if (searchTerm) {
                clearButton.style.display = 'block';
                this.performSearch(searchTerm);
            } else {
                clearButton.style.display = 'none';
                this.clearSearch();
            }
        },

        handleKeydown: function(e) {
            if (e.key === 'Escape') {
                this.clearSearch();
                e.target.blur();
            } else if (e.key === 'Enter') {
                // Focus first visible result
                const firstResult = document.querySelector('.mks-manage-nav-link:not(.mks-manage-hidden), .mks-manage-nav-sublink:not(.mks-manage-hidden)');
                if (firstResult) {
                    firstResult.click();
                }
            }
        },

        performSearch: function(searchTerm) {
            const allItems = document.querySelectorAll('.mks-manage-nav-item');
            const regex = new RegExp(searchTerm, 'i');
            
            SidebarController.highlightSearchResults(searchTerm);
            
            allItems.forEach(item => {
                const text = item.textContent;
                const isMatch = regex.test(text);
                
                if (isMatch) {
                    item.style.display = 'block';
                    item.classList.remove('mks-manage-hidden');
                    
                    // Show parent submenu if this is a subitem
                    const submenu = item.closest('.mks-manage-nav-submenu');
                    if (submenu) {
                        submenu.classList.add('mks-manage-open');
                        submenu.style.maxHeight = submenu.scrollHeight + 'px';
                        
                        const submenuId = submenu.id.replace('submenu-', '');
                        const trigger = document.querySelector(`[data-submenu="${submenuId}"]`);
                        if (trigger) {
                            trigger.setAttribute('aria-expanded', 'true');
                            const arrow = trigger.querySelector('.mks-manage-nav-arrow');
                            if (arrow) {
                                arrow.style.transform = 'rotate(90deg)';
                            }
                        }
                    }
                } else {
                    item.style.display = 'none';
                    item.classList.add('mks-manage-hidden');
                }
            });
        },

        clearSearch: function() {
            const searchInput = document.querySelector('.mks-manage-search-input');
            const clearButton = document.querySelector('.mks-manage-search-clear');
            const allItems = document.querySelectorAll('.mks-manage-nav-item');

            if (searchInput) {
                searchInput.value = '';
            }
            
            if (clearButton) {
                clearButton.style.display = 'none';
            }

            // Show all items
            allItems.forEach(item => {
                item.style.display = 'block';
                item.classList.remove('mks-manage-hidden');
            });

            // Clear highlights
            SidebarController.clearHighlights();

            // Close all submenus
            SidebarController.closeAllSubmenus();
        }
    };

    // User Profile Card Enhancement
    const UserProfile = {
        init: function() {
            this.enhanceUserCard();
        },

        enhanceUserCard: function() {
            const userCard = document.querySelector('.mks-manage-user-card');
            if (!userCard) return;

            // Add click handler for potential profile dropdown
            userCard.addEventListener('click', this.toggleUserMenu.bind(this));
            
            // Add tooltip for truncated user names
            const userName = userCard.querySelector('.mks-manage-user-name');
            if (userName && userName.scrollWidth > userName.clientWidth) {
                userName.setAttribute('title', userName.textContent);
            }
        },

        toggleUserMenu: function(e) {
            e.preventDefault();
            
            // Future enhancement: Add dropdown menu with user options
            console.log('User menu toggle - to be implemented');
        }
    };

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        SidebarController.init();
        QuickSearch.init();
        UserProfile.init();
        
        // Restore sidebar state on page load
        const wasCollapsed = localStorage.getItem('mks-sidebar-collapsed') === 'true';
        const sidebar = document.querySelector('.mks-manage-sidebar');
        if (wasCollapsed && sidebar && window.innerWidth > 768) {
            sidebar.classList.add('mks-manage-collapsed');
        }
        
        console.log('MKS Management Sidebar initialized');
    });

    // Export for use by other scripts
    if (typeof window !== 'undefined') {
        window.MKSManagement = window.MKSManagement || {};
        window.MKSManagement.SidebarController = SidebarController;
        window.MKSManagement.QuickSearch = QuickSearch;
        window.MKSManagement.UserProfile = UserProfile;
    }

})();
