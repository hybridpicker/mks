/**
 * Bildkompressor-Funktion für die Galerie
 * Verkleinert Bilder auf Clientseite bevor sie hochgeladen werden
 */

/**
 * Komprimiert ein Bild, um die Dateigröße zu reduzieren
 * @param {File} file - Die ursprüngliche Bilddatei
 * @param {Object} options - Optionen für die Komprimierung
 * @param {Number} options.maxWidth - Maximale Breite des Bildes
 * @param {Number} options.maxHeight - Maximale Höhe des Bildes
 * @param {Number} options.quality - JPEG-Qualität (0-1)
 * @param {Number} options.maxSizeMB - Maximale Dateigröße in MB
 * @returns {Promise<File>} Die komprimierte Bilddatei
 */
function compressImage(file, options = {}) {
    // Standardwerte
    const maxWidth = options.maxWidth || 1920; // Standardmäßig auf 1920px maximale Breite
    const maxHeight = options.maxHeight || 1080; // Standardmäßig auf 1080px maximale Höhe
    const quality = options.quality || 0.7; // Standard-Qualität von 70%
    const maxSizeMB = options.maxSizeMB || 2; // Standard 2MB
    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    
    return new Promise((resolve, reject) => {
        // Erstellen Sie ein Image-Element
        const img = new Image();
        img.onload = function() {
            // Bestimmen Sie die neuen Dimensionen unter Beibehaltung des Seitenverhältnisses
            let width = img.width;
            let height = img.height;
            
            // Skalieren Sie das Bild, wenn es größer als die maximalen Dimensionen ist
            if (width > maxWidth || height > maxHeight) {
                if (width / height > maxWidth / maxHeight) {
                    // Bild ist breiter als hoch im Verhältnis
                    height = height * (maxWidth / width);
                    width = maxWidth;
                } else {
                    // Bild ist höher als breit im Verhältnis
                    width = width * (maxHeight / height);
                    height = maxHeight;
                }
            }
            
            // Erstellen Sie eine Canvas zum Zeichnen des skalierten Bildes
            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            
            // Zeichnen Sie das Bild auf die Canvas
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);
            
            // Konvertieren Sie die Canvas zu einer Datei mit der angegebenen Qualität
            let compressQuality = quality;
            let iteration = 0;
            const maxIterations = 10;
            
            // Rekursive Funktion zum Komprimieren mit reduzierter Qualität, falls nötig
            function compressWithQuality() {
                canvas.toBlob(blob => {
                    if (blob.size > maxSizeBytes && iteration < maxIterations) {
                        // Wenn die Dateigröße immer noch zu groß ist, reduzieren Sie die Qualität und versuchen Sie es erneut
                        iteration++;
                        compressQuality -= 0.1;
                        if (compressQuality < 0.3) compressQuality = 0.3; // Keine niedrigere Qualität als 30%
                        console.log(`Komprimierung mit Qualität ${compressQuality.toFixed(2)}, Iteration ${iteration}`);
                        compressWithQuality();
                    } else {
                        // Dateigröße ist akzeptabel oder wir haben die maximale Anzahl von Iterationen erreicht
                        // Erstellen Sie eine neue Datei mit dem ursprünglichen Namen und Typ
                        const compressedFile = new File([blob], file.name, {
                            type: file.type,
                            lastModified: new Date().getTime()
                        });
                        
                        console.log(`Komprimiert: ${file.name} von ${formatFileSize(file.size)} auf ${formatFileSize(compressedFile.size)}`);
                        console.log(`Qualität: ${compressQuality.toFixed(2)}, Neue Dimensionen: ${width}x${height}`);
                        
                        // Wenn die komprimierte Datei immer noch größer als das Maximum ist, warnen Sie,
                        // aber lösen Sie das Versprechen mit der komprimierten Datei auf
                        if (compressedFile.size > maxSizeBytes) {
                            console.warn(`Die Datei konnte nicht unter ${maxSizeMB}MB komprimiert werden`);
                        }
                        
                        resolve(compressedFile);
                    }
                }, file.type, compressQuality);
            }
            
            // Starten Sie die Komprimierung
            compressWithQuality();
        };
        
        img.onerror = function() {
            reject(new Error('Fehler beim Laden des Bildes für die Komprimierung'));
        };
        
        // Laden Sie das Bild
        img.src = URL.createObjectURL(file);
    });
}

/**
 * Formatiert Dateigröße in menschenlesbarer Form
 * @param {Number} bytes - Dateigröße in Bytes
 * @returns {String} Formatierte Größe
 */
function formatFileSize(bytes) {
    if (bytes < 1024) {
        return bytes + ' B';
    } else if (bytes < 1024 * 1024) {
        return (bytes / 1024).toFixed(2) + ' KB';
    } else {
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    }
}

/**
 * Komprimiert ein Array von Dateien
 * @param {File[]} files - Array von Dateien
 * @param {Object} options - Komprimierungsoptionen
 * @returns {Promise<File[]>} Array von komprimierten Dateien
 */
async function compressImageFiles(files, options = {}) {
    const maxSizeMB = options.maxSizeMB || 2.5;
    const compressedFiles = [];
    
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        
        // Nur Bilder komprimieren und nur wenn sie größer als das Limit sind
        if (file.type.startsWith('image/') && file.size > maxSizeMB * 1024 * 1024) {
            try {
                const compressedFile = await compressImage(file, options);
                
                // Speichern Sie die ursprüngliche Größe für Vergleichszwecke
                compressedFile.originalSize = file.size;
                compressedFile.wasCompressed = true;
                
                compressedFiles.push(compressedFile);
            } catch (error) {
                console.error(`Fehler beim Komprimieren von ${file.name}:`, error);
                compressedFiles.push(file); // Verwenden Sie die Originaldatei, wenn die Komprimierung fehlschlägt
            }
        } else {
            // Keine Komprimierung notwendig
            compressedFiles.push(file);
        }
    }
    
    return compressedFiles;
}
