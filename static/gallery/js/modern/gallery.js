/**
 * Modern Gallery JavaScript
 * Handles gallery functionality with improved image viewing and interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the gallery
    initGallery();
    
    // Setup lazy loading
    setupLazyLoading();
});

/**
 * Initialize gallery functionality
 */
function initGallery() {
    // Setup image overlay
    setupImageOverlay();
    
    // Setup keyboard navigation
    setupKeyboardNavigation();
    
    // Apply modern styling classes
    modernizeGalleryLayout();
}

/**
 * Modernize the gallery layout
 */
function modernizeGalleryLayout() {
    // Add container class to gallery
    const galleryContainer = document.querySelector('.container.gallery');
    if (galleryContainer) {
        galleryContainer.classList.add('gallery-container');
    }
    
    // Add header class
    const galleryHeader = document.querySelector('.gallery h1');
    if (galleryHeader) {
        const headerDiv = document.createElement('div');
        headerDiv.className = 'gallery-header';
        galleryHeader.parentNode.insertBefore(headerDiv, galleryHeader);
        headerDiv.appendChild(galleryHeader);
    }
    
    // Add classes to empty message if exists
    const emptyGalleryMessage = document.querySelector('.gallery-show > div');
    if (emptyGalleryMessage && !emptyGalleryMessage.classList.contains('picture')) {
        emptyGalleryMessage.className = 'empty-gallery-message';
    }
    
    // Add class to no categories message if exists
    const noCategoriesMessage = document.querySelector('.gallery > div[style*="text-align: center"]');
    if (noCategoriesMessage) {
        noCategoriesMessage.className = 'no-categories-message';
    }
    
    // Ensure overlay has active class for proper styling
    const overlay = document.getElementById('overlay-image-section');
    if (overlay) {
        if (overlay.style.display === 'block') {
            overlay.classList.add('active');
        }
    }
}

/**
 * Setup image overlay with improved interaction
 */
function setupImageOverlay() {
    const pictures = document.querySelectorAll('.gallery-show picture');
    const overlay = document.getElementById('overlay-image-section');
    const overlayImg = document.getElementById('overlay-show-img');
    const overlayText = document.getElementById('gallery-text-overlay');
    const closeBtn = document.getElementById('closebtn-gallery');
    
    // Set up gallery photos for overlay
    pictures.forEach(picture => {
        picture.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get photo ID from the onclick attribute
            const onClickAttr = this.getAttribute('onclick');
            if (onClickAttr) {
                const photoIdMatch = onClickAttr.match(/showImg\((\d+)\)/);
                if (photoIdMatch && photoIdMatch[1]) {
                    showImage(parseInt(photoIdMatch[1]));
                }
            }
        });
    });
    
    // Enhanced close button
    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            hideOverlay();
        });
    }
    
    // Click outside image to close
    if (overlay) {
        overlay.addEventListener('click', function(e) {
            if (e.target === this) {
                hideOverlay();
            }
        });
    }
}

/**
 * Show image in overlay with smooth transition
 */
function showImage(id) {
    if (!photo_data || !photo_data[id]) return;
    
    const overlay = document.getElementById('overlay-image-section');
    const overlayImg = document.getElementById('overlay-show-img');
    const overlayText = document.getElementById('gallery-text-overlay');
    
    // Get image data
    const photoData = photo_data[id];
    
    // Set image source
    overlayImg.src = photoData.image;
    
    // Create and set caption
    let caption = '';
    if (photoData.description) {
        caption = photoData.description;
    }
    
    if (photoData.copyright_by) {
        if (caption) {
            caption += ' | © ' + photoData.copyright_by;
        } else {
            caption = '© ' + photoData.copyright_by;
        }
    }
    
    // Update caption text
    if (document.getElementById('gallery-text-overlay')) {
        document.getElementById('gallery-text-overlay').innerHTML = caption;
    }
    
    // Display overlay with animation
    overlay.style.display = 'flex';
    setTimeout(() => {
        overlay.classList.add('active');
    }, 10);
    
    // Hide header
    if (document.querySelector('header')) {
        document.querySelector('header').style.zIndex = '0';
    }
    
    // Track current image for navigation
    overlay.dataset.currentId = id;
    
    // Check if we have previous and next images
    updateNavigationAvailability();
}

/**
 * Hide overlay with smooth transition
 */
function hideOverlay() {
    const overlay = document.getElementById('overlay-image-section');
    
    overlay.classList.remove('active');
    setTimeout(() => {
        overlay.style.display = 'none';
        
        // Restore header
        if (document.querySelector('header')) {
            document.querySelector('header').style.zIndex = '99';
        }
    }, 300);
}

/**
 * Update navigation availability based on current image
 */
function updateNavigationAvailability() {
    const overlay = document.getElementById('overlay-image-section');
    const currentId = parseInt(overlay.dataset.currentId);
    
    // Get all available photo IDs
    const photoIds = Object.keys(photo_data).map(id => parseInt(id));
    
    // Find current index
    const currentIndex = photoIds.indexOf(currentId);
    
    // Determine if we have previous and next
    const hasPrev = currentIndex > 0;
    const hasNext = currentIndex < photoIds.length - 1;
    
    // Update navigation
    const prevNav = document.querySelector('.gallery-prev-nav');
    const nextNav = document.querySelector('.gallery-next-nav');
    
    if (prevNav) {
        prevNav.style.display = hasPrev ? 'flex' : 'none';
    }
    
    if (nextNav) {
        nextNav.style.display = hasNext ? 'flex' : 'none';
    }
}

/**
 * Setup keyboard navigation
 */
function setupKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        const overlay = document.getElementById('overlay-image-section');
        
        // Only process if overlay is active
        if (overlay && overlay.style.display === 'block') {
            if (e.key === 'Escape') {
                hideOverlay();
            } else if (e.key === 'ArrowRight') {
                navigateGallery('next');
            } else if (e.key === 'ArrowLeft') {
                navigateGallery('prev');
            }
        }
    });
}

/**
 * Navigate to previous or next image
 */
function navigateGallery(direction) {
    const overlay = document.getElementById('overlay-image-section');
    const currentId = parseInt(overlay.dataset.currentId);
    
    // Get all available photo IDs
    const photoIds = Object.keys(photo_data).map(id => parseInt(id));
    
    // Find current index
    const currentIndex = photoIds.indexOf(currentId);
    
    // Determine target index
    let targetIndex;
    if (direction === 'next' && currentIndex < photoIds.length - 1) {
        targetIndex = currentIndex + 1;
    } else if (direction === 'prev' && currentIndex > 0) {
        targetIndex = currentIndex - 1;
    } else {
        return; // Can't navigate further
    }
    
    // Show the target image
    showImage(photoIds[targetIndex]);
}

/**
 * Setup lazy loading for images
 */
function setupLazyLoading() {
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img.lazy');
        
        const imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    
                    lazyImage.addEventListener('load', () => {
                        lazyImage.classList.add('loaded');
                    });
                    
                    imageObserver.unobserve(lazyImage);
                }
            });
        });
        
        lazyImages.forEach(function(lazyImage) {
            imageObserver.observe(lazyImage);
        });
    } else {
        // Fallback for browsers without IntersectionObserver
        const lazyLoad = function() {
            const lazyImages = document.querySelectorAll('img.lazy');
            
            lazyImages.forEach(function(lazyImage) {
                if (isInViewport(lazyImage)) {
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.classList.remove('lazy');
                }
            });
        };
        
        // Initial load
        lazyLoad();
        
        // Add scroll event
        let lazyLoadThrottleTimeout;
        window.addEventListener('scroll', function() {
            if (lazyLoadThrottleTimeout) {
                clearTimeout(lazyLoadThrottleTimeout);
            }
            
            lazyLoadThrottleTimeout = setTimeout(lazyLoad, 200);
        });
    }
}

/**
 * Check if element is in viewport
 */
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.bottom >= 0 &&
        rect.right >= 0 &&
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.left <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Backward compatibility
function showImg(id) {
    showImage(id);
}

function blockImg() {
    hideOverlay();
}
