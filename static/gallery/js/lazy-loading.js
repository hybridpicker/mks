// Lazy Loading for Gallery Images
document.addEventListener('DOMContentLoaded', function() {
    console.log("Lazy Loading für Galerie initialisiert");
    
    // Optionen für Intersection Observer
    const imageObserverOptions = {
        rootMargin: '50px 0px', // Lade Bilder 50px bevor sie sichtbar werden
        threshold: 0.01
    };
    
    // Intersection Observer erstellen
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                const galleryItem = img.closest('.gallery-item');
                
                // Temporäres Bild zum Vorabladen
                const tempImg = new Image();
                
                tempImg.onload = function() {
                    // Ersetze src mit data-src
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    img.classList.add('loaded');
                    
                    // Entferne Loading-Animation
                    if (galleryItem) {
                        galleryItem.classList.remove('loading');
                    }
                    
                    // Beobachtung beenden
                    observer.unobserve(img);
                };
                
                tempImg.onerror = function() {
                    console.error('Fehler beim Laden des Bildes:', img.dataset.src);
                    if (galleryItem) {
                        galleryItem.classList.remove('loading');
                    }
                    observer.unobserve(img);
                };
                
                // Starte das Laden
                tempImg.src = img.dataset.src;
            }
        });
    }, imageObserverOptions);
    
    // Alle Bilder mit data-src finden und beobachten
    const lazyImages = document.querySelectorAll('img[data-src]');
    lazyImages.forEach(img => {
        img.classList.add('lazy');
        imageObserver.observe(img);
    });
    
    // Fallback für Browser ohne Intersection Observer
    if (!('IntersectionObserver' in window)) {
        console.log('Intersection Observer nicht unterstützt - lade alle Bilder sofort');
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            img.classList.add('loaded');
            const galleryItem = img.closest('.gallery-item');
            if (galleryItem) {
                galleryItem.classList.remove('loading');
            }
        });
    }
});