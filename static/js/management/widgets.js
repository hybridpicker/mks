/* ================================================
   MKS Management Widget JavaScript
   Handles widget interactions and functionality
   ================================================ */

(function() {
    'use strict';

    // Widget Controller
    const WidgetController = {
        init: function() {
            this.bindEvents();
            this.loadWidgetStates();
            this.initWidgetFeatures();
        },

        bindEvents: function() {
            // Widget collapse/expand
            document.addEventListener('click', (e) => {
                const toggleBtn = e.target.closest('.mks-manage-widget-toggle');
                if (toggleBtn) {
                    e.preventDefault();
                    this.toggleWidget(toggleBtn);
                }
            });

            // Widget dragging (for future reordering feature)
            document.addEventListener('dragstart', this.handleDragStart.bind(this));
            document.addEventListener('dragover', this.handleDragOver.bind(this));
            document.addEventListener('drop', this.handleDrop.bind(this));

            // Widget refresh
            document.addEventListener('click', (e) => {
                const refreshBtn = e.target.closest('.mks-manage-widget-refresh');
                if (refreshBtn) {
                    e.preventDefault();
                    this.refreshWidget(refreshBtn);
                }
            });

            // Widget settings
            document.addEventListener('click', (e) => {
                const settingsBtn = e.target.closest('.mks-manage-widget-settings');
                if (settingsBtn) {
                    e.preventDefault();
                    this.openWidgetSettings(settingsBtn);
                }
            });

            // Auto-save widget states
            window.addEventListener('beforeunload', this.saveWidgetStates.bind(this));
        },

        toggleWidget: function(toggleBtn) {
            const widget = toggleBtn.closest('.mks-manage-widget');
            if (!widget) return;

            const content = widget.querySelector('.mks-manage-widget-content');
            const isCollapsed = widget.classList.contains('mks-manage-collapsed');
            const widgetId = widget.getAttribute('data-widget-id') || widget.id;

            if (isCollapsed) {
                this.expandWidget(widget, content);
            } else {
                this.collapseWidget(widget, content);
            }

            // Update ARIA state
            toggleBtn.setAttribute('aria-expanded', (!isCollapsed).toString());
            widget.setAttribute('aria-expanded', (!isCollapsed).toString());

            // Save state
            if (widgetId) {
                this.saveWidgetState(widgetId, !isCollapsed);
            }

            // Announce to screen readers
            const title = widget.querySelector('.mks-manage-widget-title').textContent;
            const state = isCollapsed ? 'eingeblendet' : 'ausgeblendet';
            this.announceToScreenReader(`${title} ${state}`);
        },

        expandWidget: function(widget, content) {
            widget.classList.remove('mks-manage-collapsed');
            content.style.maxHeight = content.scrollHeight + 'px';
            
            // Remove max-height after transition
            setTimeout(() => {
                if (!widget.classList.contains('mks-manage-collapsed')) {
                    content.style.maxHeight = 'none';
                }
            }, 300);

            // Focus management for accessibility
            const focusableElement = content.querySelector('input, button, a, [tabindex]:not([tabindex="-1"])');
            if (focusableElement) {
                focusableElement.focus();
            }
        },

        collapseWidget: function(widget, content) {
            content.style.maxHeight = content.scrollHeight + 'px';
            
            // Force reflow
            content.offsetHeight;
            
            content.style.maxHeight = '0';
            widget.classList.add('mks-manage-collapsed');
        },

        refreshWidget: function(refreshBtn) {
            const widget = refreshBtn.closest('.mks-manage-widget');
            if (!widget) return;

            const widgetId = widget.getAttribute('data-widget-id');
            const refreshUrl = refreshBtn.getAttribute('data-refresh-url');

            if (!refreshUrl) {
                console.warn('No refresh URL specified for widget');
                return;
            }

            // Show loading state
            widget.classList.add('mks-manage-loading');
            refreshBtn.disabled = true;

            // Perform AJAX request
            fetch(refreshUrl, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken()
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                const content = widget.querySelector('.mks-manage-widget-content');
                if (content) {
                    content.innerHTML = html;
                    this.initWidgetFeatures(widget);
                }
                this.showNotification('Widget erfolgreich aktualisiert', 'success');
            })
            .catch(error => {
                console.error('Widget refresh failed:', error);
                this.showNotification('Fehler beim Aktualisieren des Widgets', 'error');
            })
            .finally(() => {
                widget.classList.remove('mks-manage-loading');
                refreshBtn.disabled = false;
            });
        },

        openWidgetSettings: function(settingsBtn) {
            const widget = settingsBtn.closest('.mks-manage-widget');
            const settingsUrl = settingsBtn.getAttribute('data-settings-url');
            
            if (settingsUrl) {
                // Open settings in modal or new window
                this.openModal(settingsUrl);
            } else {
                // Toggle inline settings
                this.toggleInlineSettings(widget);
            }
        },

        toggleInlineSettings: function(widget) {
            const existingSettings = widget.querySelector('.mks-manage-widget-inline-settings');
            
            if (existingSettings) {
                existingSettings.remove();
                return;
            }

            const settings = document.createElement('div');
            settings.className = 'mks-manage-widget-inline-settings';
            settings.innerHTML = `
                <div class="mks-manage-widget-settings-content">
                    <h4>Widget-Einstellungen</h4>
                    <form class="mks-manage-widget-settings-form">
                        <div class="mks-manage-form-group">
                            <label class="mks-manage-form-label">
                                <input type="checkbox" class="mks-manage-form-checkbox" name="auto-refresh">
                                Automatische Aktualisierung
                            </label>
                        </div>
                        <div class="mks-manage-form-group">
                            <label class="mks-manage-form-label">Aktualisierungsintervall</label>
                            <select class="mks-manage-form-select" name="refresh-interval">
                                <option value="0">Nie</option>
                                <option value="30">30 Sekunden</option>
                                <option value="60">1 Minute</option>
                                <option value="300">5 Minuten</option>
                                <option value="600">10 Minuten</option>
                            </select>
                        </div>
                        <div class="mks-manage-form-actions">
                            <button type="submit" class="mks-manage-btn mks-manage-btn-primary mks-manage-btn-sm">
                                Speichern
                            </button>
                            <button type="button" class="mks-manage-btn mks-manage-btn-secondary mks-manage-btn-sm mks-manage-widget-settings-cancel">
                                Abbrechen
                            </button>
                        </div>
                    </form>
                </div>
            `;

            const content = widget.querySelector('.mks-manage-widget-content');
            content.appendChild(settings);

            // Bind events
            const form = settings.querySelector('.mks-manage-widget-settings-form');
            const cancelBtn = settings.querySelector('.mks-manage-widget-settings-cancel');

            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.saveWidgetSettings(widget, new FormData(form));
                settings.remove();
            });

            cancelBtn.addEventListener('click', () => {
                settings.remove();
            });
        },

        saveWidgetSettings: function(widget, formData) {
            const widgetId = widget.getAttribute('data-widget-id');
            const settings = {};
            
            for (let [key, value] of formData.entries()) {
                settings[key] = value;
            }

            // Save to localStorage
            const allSettings = JSON.parse(localStorage.getItem('mks-widget-settings') || '{}');
            allSettings[widgetId] = settings;
            localStorage.setItem('mks-widget-settings', JSON.stringify(allSettings));

            // Apply settings
            this.applyWidgetSettings(widget, settings);

            this.showNotification('Widget-Einstellungen gespeichert', 'success');
        },

        applyWidgetSettings: function(widget, settings) {
            const widgetId = widget.getAttribute('data-widget-id');
            
            // Auto-refresh functionality
            if (settings['auto-refresh'] === 'on' && settings['refresh-interval'] > 0) {
                this.setupAutoRefresh(widget, parseInt(settings['refresh-interval']) * 1000);
            } else {
                this.clearAutoRefresh(widget);
            }
        },

        setupAutoRefresh: function(widget, interval) {
            const widgetId = widget.getAttribute('data-widget-id');
            
            // Clear existing interval
            this.clearAutoRefresh(widget);
            
            // Set new interval
            const intervalId = setInterval(() => {
                const refreshBtn = widget.querySelector('.mks-manage-widget-refresh');
                if (refreshBtn && !widget.classList.contains('mks-manage-loading')) {
                    this.refreshWidget(refreshBtn);
                }
            }, interval);
            
            // Store interval ID
            widget.setAttribute('data-refresh-interval-id', intervalId);
        },

        clearAutoRefresh: function(widget) {
            const intervalId = widget.getAttribute('data-refresh-interval-id');
            if (intervalId) {
                clearInterval(parseInt(intervalId));
                widget.removeAttribute('data-refresh-interval-id');
            }
        },

        // Widget drag and drop
        handleDragStart: function(e) {
            const widget = e.target.closest('.mks-manage-widget[draggable="true"]');
            if (!widget) return;

            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/html', widget.outerHTML);
            e.dataTransfer.setData('text/plain', widget.getAttribute('data-widget-id'));
            
            widget.classList.add('mks-manage-dragging');
        },

        handleDragOver: function(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            
            const widget = e.target.closest('.mks-manage-widget');
            if (widget) {
                widget.classList.add('mks-manage-drop-target');
            }
        },

        handleDrop: function(e) {
            e.preventDefault();
            
            const targetWidget = e.target.closest('.mks-manage-widget');
            const draggedWidget = document.querySelector('.mks-manage-widget.mks-manage-dragging');
            
            if (targetWidget && draggedWidget && targetWidget !== draggedWidget) {
                const container = targetWidget.parentNode;
                const targetRect = targetWidget.getBoundingClientRect();
                const mouseY = e.clientY;
                const insertAfter = mouseY > targetRect.top + targetRect.height / 2;
                
                if (insertAfter) {
                    container.insertBefore(draggedWidget, targetWidget.nextSibling);
                } else {
                    container.insertBefore(draggedWidget, targetWidget);
                }
                
                this.saveWidgetOrder();
            }
            
            // Clean up
            document.querySelectorAll('.mks-manage-dragging, .mks-manage-drop-target').forEach(el => {
                el.classList.remove('mks-manage-dragging', 'mks-manage-drop-target');
            });
        },

        saveWidgetOrder: function() {
            const containers = document.querySelectorAll('.mks-manage-widgets-container');
            const order = {};
            
            containers.forEach((container, containerIndex) => {
                const widgets = container.querySelectorAll('.mks-manage-widget[data-widget-id]');
                order[containerIndex] = Array.from(widgets).map(widget => 
                    widget.getAttribute('data-widget-id')
                );
            });
            
            localStorage.setItem('mks-widget-order', JSON.stringify(order));
        },

        loadWidgetStates: function() {
            const states = JSON.parse(localStorage.getItem('mks-widget-states') || '{}');
            const settings = JSON.parse(localStorage.getItem('mks-widget-settings') || '{}');
            
            Object.keys(states).forEach(widgetId => {
                const widget = document.querySelector(`[data-widget-id="${widgetId}"]`);
                if (widget) {
                    const isExpanded = states[widgetId];
                    if (!isExpanded) {
                        const content = widget.querySelector('.mks-manage-widget-content');
                        this.collapseWidget(widget, content);
                    }
                }
            });
            
            // Apply widget settings
            Object.keys(settings).forEach(widgetId => {
                const widget = document.querySelector(`[data-widget-id="${widgetId}"]`);
                if (widget) {
                    this.applyWidgetSettings(widget, settings[widgetId]);
                }
            });
        },

        saveWidgetStates: function() {
            const states = {};
            const widgets = document.querySelectorAll('.mks-manage-widget[data-widget-id]');
            
            widgets.forEach(widget => {
                const widgetId = widget.getAttribute('data-widget-id');
                const isExpanded = !widget.classList.contains('mks-manage-collapsed');
                states[widgetId] = isExpanded;
            });
            
            localStorage.setItem('mks-widget-states', JSON.stringify(states));
        },

        saveWidgetState: function(widgetId, isExpanded) {
            const states = JSON.parse(localStorage.getItem('mks-widget-states') || '{}');
            states[widgetId] = isExpanded;
            localStorage.setItem('mks-widget-states', JSON.stringify(states));
        },

        initWidgetFeatures: function(context = document) {
            // Initialize charts in widgets
            this.initCharts(context);
            
            // Initialize data tables
            this.initDataTables(context);
            
            // Initialize widget-specific components
            this.initWidgetComponents(context);
        },

        initCharts: function(context) {
            const chartContainers = context.querySelectorAll('[data-chart-type]');
            
            chartContainers.forEach(container => {
                const chartType = container.getAttribute('data-chart-type');
                const chartData = JSON.parse(container.getAttribute('data-chart-data') || '{}');
                
                switch (chartType) {
                    case 'line':
                        this.renderLineChart(container, chartData);
                        break;
                    case 'bar':
                        this.renderBarChart(container, chartData);
                        break;
                    case 'pie':
                        this.renderPieChart(container, chartData);
                        break;
                    case 'doughnut':
                        this.renderDoughnutChart(container, chartData);
                        break;
                }
            });
        },

        renderLineChart: function(container, data) {
            // Simple line chart implementation
            // In a real implementation, you'd use Chart.js or similar
            container.innerHTML = '<p>Line Chart (Chart.js integration required)</p>';
        },

        renderBarChart: function(container, data) {
            // Simple bar chart implementation
            container.innerHTML = '<p>Bar Chart (Chart.js integration required)</p>';
        },

        renderPieChart: function(container, data) {
            // Simple pie chart implementation
            container.innerHTML = '<p>Pie Chart (Chart.js integration required)</p>';
        },

        renderDoughnutChart: function(container, data) {
            // Simple doughnut chart implementation
            container.innerHTML = '<p>Doughnut Chart (Chart.js integration required)</p>';
        },

        initDataTables: function(context) {
            const tables = context.querySelectorAll('.mks-manage-data-table');
            
            tables.forEach(table => {
                this.enhanceTable(table);
            });
        },

        enhanceTable: function(table) {
            // Add sorting functionality
            const headers = table.querySelectorAll('th[data-sortable="true"]');
            headers.forEach(header => {
                header.style.cursor = 'pointer';
                header.addEventListener('click', () => {
                    this.sortTable(table, header);
                });
            });
            
            // Add search functionality if search input exists
            const searchInput = table.parentElement.querySelector('.mks-manage-table-search');
            if (searchInput) {
                searchInput.addEventListener('input', (e) => {
                    this.filterTable(table, e.target.value);
                });
            }
        },

        sortTable: function(table, header) {
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const columnIndex = Array.from(header.parentElement.children).indexOf(header);
            const currentOrder = header.getAttribute('data-sort-order') || 'asc';
            const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
            
            rows.sort((a, b) => {
                const aText = a.children[columnIndex].textContent.trim();
                const bText = b.children[columnIndex].textContent.trim();
                
                // Try to parse as numbers
                const aNum = parseFloat(aText);
                const bNum = parseFloat(bText);
                
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return newOrder === 'asc' ? aNum - bNum : bNum - aNum;
                }
                
                // Compare as strings
                return newOrder === 'asc' 
                    ? aText.localeCompare(bText)
                    : bText.localeCompare(aText);
            });
            
            // Update DOM
            rows.forEach(row => tbody.appendChild(row));
            
            // Update header
            headers.forEach(h => h.removeAttribute('data-sort-order'));
            header.setAttribute('data-sort-order', newOrder);
            
            // Update visual indicator
            headers.forEach(h => h.classList.remove('mks-manage-sorted-asc', 'mks-manage-sorted-desc'));
            header.classList.add(`mks-manage-sorted-${newOrder}`);
        },

        filterTable: function(table, searchTerm) {
            const tbody = table.querySelector('tbody');
            const rows = tbody.querySelectorAll('tr');
            const regex = new RegExp(searchTerm, 'i');
            
            rows.forEach(row => {
                const text = row.textContent;
                if (regex.test(text)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        },

        initWidgetComponents: function(context) {
            // Initialize progress bars
            const progressBars = context.querySelectorAll('.mks-manage-progress-bar');
            progressBars.forEach(bar => {
                this.animateProgressBar(bar);
            });
            
            // Initialize counters
            const counters = context.querySelectorAll('.mks-manage-counter');
            counters.forEach(counter => {
                this.animateCounter(counter);
            });
            
            // Initialize tooltips
            const tooltips = context.querySelectorAll('[data-tooltip]');
            tooltips.forEach(element => {
                this.initTooltip(element);
            });
        },

        animateProgressBar: function(bar) {
            const targetWidth = bar.getAttribute('data-progress') + '%';
            const fill = bar.querySelector('.mks-manage-progress-fill');
            
            if (fill) {
                setTimeout(() => {
                    fill.style.width = targetWidth;
                }, 100);
            }
        },

        animateCounter: function(counter) {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = 2000; // 2 seconds
            const increment = target / (duration / 16); // 60fps
            let current = 0;
            
            const updateCounter = () => {
                current += increment;
                if (current >= target) {
                    counter.textContent = target.toLocaleString();
                } else {
                    counter.textContent = Math.floor(current).toLocaleString();
                    requestAnimationFrame(updateCounter);
                }
            };
            
            updateCounter();
        },

        initTooltip: function(element) {
            const tooltipText = element.getAttribute('data-tooltip');
            
            element.addEventListener('mouseenter', () => {
                this.showTooltip(element, tooltipText);
            });
            
            element.addEventListener('mouseleave', () => {
                this.hideTooltip();
            });
        },

        showTooltip: function(element, text) {
            const existingTooltip = document.querySelector('.mks-manage-tooltip');
            if (existingTooltip) {
                existingTooltip.remove();
            }
            
            const tooltip = document.createElement('div');
            tooltip.className = 'mks-manage-tooltip';
            tooltip.textContent = text;
            
            document.body.appendChild(tooltip);
            
            const rect = element.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
        },

        hideTooltip: function() {
            const tooltip = document.querySelector('.mks-manage-tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        },

        // Utility methods
        getCSRFToken: function() {
            const token = document.querySelector('[name=csrfmiddlewaretoken]');
            return token ? token.value : '';
        },

        showNotification: function(message, type) {
            // Use the main notification system
            if (window.MKSManagement && window.MKSManagement.Utils) {
                window.MKSManagement.Utils.showNotification(message, type);
            } else {
                console.log(`${type.toUpperCase()}: ${message}`);
            }
        },

        announceToScreenReader: function(message) {
            if (window.MKSManagement && window.MKSManagement.Accessibility) {
                window.MKSManagement.Accessibility.announce(message);
            }
        },

        openModal: function(url) {
            // Simple modal implementation - would be enhanced in production
            window.open(url, 'widget-settings', 'width=600,height=400,scrollbars=yes');
        }
    };

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        WidgetController.init();
        console.log('MKS Management Widget Controller initialized');
    });

    // Export for use by other scripts
    if (typeof window !== 'undefined') {
        window.MKSManagement = window.MKSManagement || {};
        window.MKSManagement.WidgetController = WidgetController;
    }

})();

// Add CSS for widget enhancements
const widgetStyles = document.createElement('style');
widgetStyles.textContent = `
    .mks-manage-widget-inline-settings {
        margin-top: 16px;
        padding: 16px;
        background: #f8f9fa;
        border-radius: 6px;
        border: 1px solid #e9ecef;
    }
    
    .mks-manage-widget-settings-content h4 {
        margin: 0 0 16px 0;
        color: #495057;
        font-size: 14px;
        font-weight: 600;
    }
    
    .mks-manage-widget.mks-manage-dragging {
        opacity: 0.5;
        transform: scale(0.95);
    }
    
    .mks-manage-widget.mks-manage-drop-target {
        border: 2px dashed var(--mks-manage-primary, #2271b1);
        background: rgba(34, 113, 177, 0.05);
    }
    
    .mks-manage-progress-bar {
        width: 100%;
        height: 8px;
        background: #e9ecef;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .mks-manage-progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--mks-manage-primary, #2271b1), var(--mks-manage-primary-light, #4f94d4));
        width: 0;
        transition: width 0.6s ease;
        border-radius: 4px;
    }
    
    .mks-manage-counter {
        font-size: 2rem;
        font-weight: 700;
        color: var(--mks-manage-primary, #2271b1);
    }
    
    .mks-manage-tooltip {
        position: absolute;
        background: #333;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 1000;
        pointer-events: none;
    }
    
    .mks-manage-tooltip::after {
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 5px solid transparent;
        border-top-color: #333;
    }
    
    .mks-manage-sorted-asc::after {
        content: ' ↑';
        color: var(--mks-manage-primary, #2271b1);
    }
    
    .mks-manage-sorted-desc::after {
        content: ' ↓';
        color: var(--mks-manage-primary, #2271b1);
    }
    
    .mks-manage-data-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .mks-manage-data-table th,
    .mks-manage-data-table td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #e9ecef;
    }
    
    .mks-manage-data-table th {
        background: #f8f9fa;
        font-weight: 600;
        color: #495057;
    }
    
    .mks-manage-data-table tr:hover {
        background: #f8f9fa;
    }
    
    .mks-manage-table-search {
        width: 100%;
        padding: 8px 12px;
        border: 1px solid #ced4da;
        border-radius: 4px;
        margin-bottom: 16px;
    }
`;
document.head.appendChild(widgetStyles);
