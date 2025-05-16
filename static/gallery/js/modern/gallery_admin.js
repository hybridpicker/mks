/**
 * Enhanced Gallery Admin Functionality
 * Provides improved drag and drop image upload and management
 */

// Configuration
const MAX_FILE_SIZE = 3 * 1024 * 1024; // 3MB (erhöht von 2MB)
const MAX_FILES = 100; // Maximum files per upload
const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
const ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];

// State management
let selectedFiles = [];
let uploadQueue = [];
let isUploading = false;
let uploadIndex = 0;
let successCount = 0;
let errorCount = 0;

// DOM elements
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the admin interface
    initGalleryAdmin();
});

/**
 * Initialize gallery admin interface
 */
function initGalleryAdmin() {
    // Setup drag and drop for single upload
    setupSingleUpload();
    
    // Setup enhanced drag and drop for multiple uploads
    setupMultiUpload();
    
    // Setup UI tabs
    setupUploadTabs();
    
    // Initialize sortable functionality
    initSortable();
    
    // Setup modals
    setupModals();
    
    // Setup category tabs
    setupCategoryTabs();
    
    // Setup photo actions
    setupPhotoActions();
    
    // Setup category actions
    setupCategoryActions();
}

/**
 * Setup drag and drop for single image upload
 */
function setupSingleUpload() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadForm = document.getElementById('upload-form');
    const selectedFileInfo = document.getElementById('selected-file');
    
    if (!dropZone || !fileInput || !uploadForm) return;
    
    // Prevent default drag behaviors on document for this drop zone
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.addEventListener(eventName, function(e) {
            // Only prevent if it's related to the upload zone
            if (e.target === dropZone || dropZone.contains(e.target)) {
                e.preventDefault();
                e.stopPropagation();
            }
        }, false);
    });
    
    // Also prevent directly on the drop zone to be 100% sure
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, function(e) {
            e.preventDefault();
            e.stopPropagation();
        }, false);
    });
    
    // Highlight drop zone when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        }, false);
    });
    
    // Handle dropped files
    dropZone.addEventListener('drop', e => {
        console.log('Single file dropped');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleSingleFile(files[0]);
        }
    });
    
    // Handle file input change
    fileInput.addEventListener('change', e => {
        if (e.target.files.length > 0) {
            handleSingleFile(e.target.files[0]);
        }
    });
    
    // Handle the button click to trigger file input
    document.getElementById('select-file-btn')?.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Handle form submission
    uploadForm.addEventListener('submit', handleSingleFormSubmit);
}

/**
 * Handle single file selection
 */
function handleSingleFile(file) {
    const fileInput = document.getElementById('file-input');
    const selectedFileInfo = document.getElementById('selected-file');
    
    // Get file extension
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    
    // Check file type by MIME type OR extension (more permissive)
    const validMimeType = ALLOWED_MIME_TYPES.includes(file.type);
    const validExtension = ALLOWED_EXTENSIONS.includes(fileExt);
    
    console.log(`Checking file ${file.name} - type: ${file.type}, extension: ${fileExt}`);
    console.log(`Valid MIME: ${validMimeType}, Valid extension: ${validExtension}`);
    
    if (!validMimeType && !validExtension) {
        showMessage('error', 'Ungültiger Dateityp. Erlaubte Typen: JPG, PNG, GIF, WEBP');
        return;
    }
    
    // Zeigen Sie eine Ladeanzeige an, während das Bild komprimiert wird
    selectedFileInfo.innerHTML = `
        <div class="compression-indicator">
            <div class="spinner"></div>
            <p>Bild wird für Upload optimiert...</p>
        </div>
    `;
    selectedFileInfo.style.display = 'flex';
    
    // Überprüfen Sie die Dateigröße und komprimieren Sie bei Bedarf
    if (file.size > MAX_FILE_SIZE) {
        console.log(`Komprimiere großes Bild: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)}MB)`);
        
        // Komprimierungsoptionen
        const options = {
            maxWidth: 1920,
            maxHeight: 1080,
            quality: 0.7,
            maxSizeMB: MAX_FILE_SIZE / (1024 * 1024)
        };
        
        // Komprimieren Sie das Bild
        compressImage(file, options)
            .then(compressedFile => {
                console.log(`Komprimierung abgeschlossen: ${file.name}`);
                console.log(`Original: ${(file.size / 1024 / 1024).toFixed(2)}MB → Komprimiert: ${(compressedFile.size / 1024 / 1024).toFixed(2)}MB`);
                
                // Aktualisieren Sie das Datei-Input mit der komprimierten Datei
                updateFileInput(compressedFile);
                
                // Zeigen Sie die komprimierte Dateiinformation an
                showFileInfo(compressedFile, true);
                
                // Zeigen Sie eine Erfolgsmeldung an
                showMessage('success', `Bild wurde für Upload optimiert (${(file.size / 1024 / 1024).toFixed(2)}MB → ${(compressedFile.size / 1024 / 1024).toFixed(2)}MB)`);
            })
            .catch(error => {
                console.error('Fehler bei der Komprimierung:', error);
                
                // Wenn die Komprimierung fehlschlägt, versuchen Sie es mit der Originaldatei
                if (file.size <= MAX_FILE_SIZE) {
                    updateFileInput(file);
                    showFileInfo(file);
                } else {
                    showMessage('error', `Die Datei ist zu groß und konnte nicht komprimiert werden. Maximale Größe: ${(MAX_FILE_SIZE / 1024 / 1024).toFixed(0)}MB`);
                    selectedFileInfo.style.display = 'none';
                }
            });
    } else {
        // Datei ist bereits klein genug
        updateFileInput(file);
        showFileInfo(file);
    }
    
    // Funktion zum Aktualisieren des Datei-Inputs
    function updateFileInput(newFile) {
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(newFile);
        fileInput.files = dataTransfer.files;
        
        // Extrahieren Sie den Dateinamen für den Titel, wenn er leer ist
        const titleInput = document.getElementById('title');
        if (titleInput && titleInput.value === '') {
            const fileName = newFile.name.substring(0, newFile.name.lastIndexOf('.'));
            titleInput.value = fileName.substring(0, 50); // Limit to 50 chars
        }
    }
    
    // Funktion zum Anzeigen der Dateiinformationen
    function showFileInfo(newFile, wasCompressed = false) {
        selectedFileInfo.innerHTML = `
            <div class="selected-file-preview">
                <img src="${URL.createObjectURL(newFile)}" alt="${newFile.name}">
                ${wasCompressed ? '<span class="compressed-badge">Optimiert</span>' : ''}
            </div>
            <div class="selected-file-info">
                <div class="selected-file-name">${newFile.name}</div>
                <div class="selected-file-size">${formatFileSize(newFile.size)}</div>
            </div>
            <button type="button" class="remove-file-btn" onclick="clearSelectedFile()">×</button>
        `;
    }
}

/**
 * Clear the selected single file
 */
function clearSelectedFile() {
    const fileInput = document.getElementById('file-input');
    const selectedFileInfo = document.getElementById('selected-file');
    
    fileInput.value = '';
    selectedFileInfo.innerHTML = '';
    selectedFileInfo.style.display = 'none';
}

/**
 * Handle single file upload form submission
 */
function handleSingleFormSubmit(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const fileInput = document.getElementById('file-input');
    const uploadForm = document.getElementById('upload-form');
    const progressBar = document.getElementById('progress-bar');
    const progressContainer = document.getElementById('upload-progress');
    const progressText = document.getElementById('progress-text');
    
    if (!fileInput.files.length) {
        showMessage('error', 'Bitte wählen Sie eine Datei aus.');
        return;
    }
    
    // Create FormData
    const formData = new FormData(uploadForm);
    
    // Ensure CSRF token is included
    const csrfToken = getCsrfToken();
    if (!formData.has('csrfmiddlewaretoken')) {
        formData.append('csrfmiddlewaretoken', csrfToken);
    }
    
    // Log what we're uploading
    console.log('Uploading single file:', fileInput.files[0].name);
    console.log('Form data keys:', [...formData.keys()]);
    
    // Show progress container
    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';
    progressText.textContent = '0%';
    
    // Disable the submit button
    const submitBtn = uploadForm.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Wird hochgeladen...';
    }
    
    // Submit using XMLHttpRequest for better compatibility
    const xhr = new XMLHttpRequest();
    xhr.open('POST', uploadForm.action, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    
    // Setup progress tracking
    xhr.upload.addEventListener('progress', e => {
        if (e.lengthComputable) {
            const percent = Math.round((e.loaded / e.total) * 100);
            progressBar.style.width = `${percent}%`;
            progressText.textContent = `${percent}%`;
        }
    });
    
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
            try {
                const data = JSON.parse(xhr.responseText);
                
                if (data.status === 'success') {
                    showMessage('success', 'Bild erfolgreich hochgeladen.');
                    
                    // Reset form
                    uploadForm.reset();
                    clearSelectedFile();
                    
                    // Add the photo to the grid
                    if (data.photo) {
                        addPhotoToGrid(data.photo);
                    } else {
                        // Reload the page if we don't have the photo data
                        window.location.reload();
                    }
                } else {
                    showMessage('error', data.message || 'Fehler beim Hochladen des Bildes.');
                }
            } catch (e) {
                console.error('Error parsing response:', e);
                showMessage('error', 'Fehler beim Verarbeiten der Serverantwort.');
            }
        } else {
            showMessage('error', `HTTP-Fehler beim Hochladen: ${xhr.status}`);
        }
        
        // Hide progress after a delay
        setTimeout(() => {
            progressContainer.style.display = 'none';
        }, 1000);
        
        // Re-enable the submit button
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Hochladen';
        }
    };
    
    xhr.onerror = function() {
        console.error('Network error during upload');
        showMessage('error', 'Netzwerkfehler beim Hochladen des Bildes.');
        
        progressContainer.style.display = 'none';
        
        // Re-enable the submit button
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Hochladen';
        }
    };
    
    // Send the form data
    xhr.send(formData);
}

/**
 * Setup enhanced multi-file upload with drag and drop
 */
function setupMultiUpload() {
    const multiDropZone = document.getElementById('multi-drop-zone');
    const multiFileInput = document.getElementById('multi-file-input');
    const multiUploadForm = document.getElementById('multi-upload-form');
    const selectedFilesContainer = document.querySelector('.selected-files-container');
    const selectedFilesList = document.getElementById('selected-files-list');
    const selectedFilesCount = document.getElementById('selected-files-count');
    const uploadFilesBtn = document.getElementById('upload-files-btn');
    
    if (!multiDropZone || !multiFileInput || !multiUploadForm) return;
    
    // CRITICAL: Prevent default drag behaviors on entire document
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.addEventListener(eventName, function(e) {
            // Only prevent if it's related to the upload zone
            if (e.target === multiDropZone || multiDropZone.contains(e.target)) {
                e.preventDefault();
                e.stopPropagation();
            }
        }, false);
    });
    
    // Also prevent directly on the drop zone to be 100% sure
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        multiDropZone.addEventListener(eventName, function(e) {
            e.preventDefault();
            e.stopPropagation();
        }, false);
    });
    
    // Highlight drop zone when items are dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        multiDropZone.addEventListener(eventName, () => {
            multiDropZone.classList.add('dragover');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        multiDropZone.addEventListener(eventName, () => {
            multiDropZone.classList.remove('dragover');
        }, false);
    });
    
    // Handle dropped files with improved validation
    multiDropZone.addEventListener('drop', e => {
        const files = e.dataTransfer.files;
        console.log('Files dropped:', files.length);
        if (files.length > 0) {
            handleMultipleFiles(files);
        }
    });
    
    // Handle file input change
    multiFileInput.addEventListener('change', e => {
        if (e.target.files.length > 0) {
            handleMultipleFiles(e.target.files);
        }
    });
    
    // Handle the button click to trigger file input
    document.getElementById('select-files-btn')?.addEventListener('click', () => {
        multiFileInput.click();
    });
    
    // Handle click on drop zone
    multiDropZone.addEventListener('click', () => {
        multiFileInput.click();
    });
    
    // Handle form submission with improved queue processing
    multiUploadForm.addEventListener('submit', handleMultiFormSubmit);
}

/**
 * Process multiple files for upload
 */
function handleMultipleFiles(files) {
    // Convert FileList to Array
    const fileArray = Array.from(files);
    
    // Log all files and their types for debugging
    console.log('Files to process:', fileArray.map(f => ({ name: f.name, type: f.type, size: f.size })));
    
    // Check if too many files
    if (fileArray.length > MAX_FILES) {
        showMessage('error', `Zu viele Dateien ausgewählt. Maximal ${MAX_FILES} Bilder erlaubt.`);
        return;
    }
    
    // Filter valid files with improved feedback
    let validFiles = [];
    let invalidFiles = [];
    
    fileArray.forEach(file => {
        // Get file extension
        const fileExt = '.' + file.name.split('.').pop().toLowerCase();
        
        // Check file type by MIME type OR extension (more permissive)
        const validMimeType = ALLOWED_MIME_TYPES.includes(file.type);
        const validExtension = ALLOWED_EXTENSIONS.includes(fileExt);
        
        if (!validMimeType && !validExtension) {
            console.log(`Rejected file ${file.name} - type: ${file.type}, extension: ${fileExt}`);
            invalidFiles.push({
                file: file,
                error: `Ungültiger Dateityp: ${file.type || 'unbekannt'} (nur JPG, PNG, GIF, WEBP erlaubt)`
            });
            return;
        }
        
        // Dateigrößenprüfung erfolgt später, da wir große Dateien komprimieren werden
        
        // File is valid by type
        console.log(`Valid file type: ${file.name} - type: ${file.type}, extension: ${fileExt}, size: ${(file.size / 1024 / 1024).toFixed(2)}MB`);
        validFiles.push(file);
    });
    
    // Show error messages for invalid files
    if (invalidFiles.length > 0) {
        // Group by error type for better feedback
        const errorsByType = {};
        invalidFiles.forEach(item => {
            if (!errorsByType[item.error]) {
                errorsByType[item.error] = [];
            }
            errorsByType[item.error].push(item.file.name);
        });
        
        // Show consolidated error messages
        for (const [error, fileNames] of Object.entries(errorsByType)) {
            if (fileNames.length <= 3) {
                showMessage('error', `${error}: ${fileNames.join(', ')}`);
            } else {
                showMessage('error', `${error}: ${fileNames.slice(0, 3).join(', ')} und ${fileNames.length - 3} weitere`);
            }
        }
    }
    
    if (validFiles.length === 0) {
        if (invalidFiles.length === 0) {
            showMessage('error', 'Keine Bilder ausgewählt.');
        } else {
            showMessage('error', 'Keine gültigen Bilder unter den ausgewählten Dateien.');
        }
        return;
    }
    
    // Komprimieren Sie große Dateien
    const selectedFilesContainer = document.querySelector('.selected-files-container');
    const selectedFilesList = document.getElementById('selected-files-list');
    const selectedFilesCount = document.getElementById('selected-files-count');
    
    // Zeigen Sie eine Ladeanimation während der Komprimierung an
    selectedFilesContainer.style.display = 'block';
    selectedFilesCount.textContent = `Optimiere ${validFiles.length} Bilder...`;
    selectedFilesList.innerHTML = `
        <div class="compression-indicator">
            <div class="spinner"></div>
            <p>Bilder werden für Upload optimiert...</p>
        </div>
    `;
    
    // Komprimierungsoptionen
    const compressOptions = {
        maxWidth: 1920,
        maxHeight: 1080,
        quality: 0.7,
        maxSizeMB: MAX_FILE_SIZE / (1024 * 1024)
    };
    
    // Komprimieren Sie die Dateien
    compressImageFiles(validFiles, compressOptions)
        .then(compressedFiles => {
            console.log(`Komprimierung abgeschlossen: ${compressedFiles.length} Dateien`);
            
            // Ersetzen Sie die ausgewählten Dateien durch die komprimierten
            selectedFiles = compressedFiles;
            
            // Aktualisieren Sie die UI
            updateSelectedFilesUI(compressedFiles.some(f => f.wasCompressed));
            
            // Enable upload button if we have files
            const uploadFilesBtn = document.getElementById('upload-files-btn');
            if (uploadFilesBtn) {
                uploadFilesBtn.disabled = selectedFiles.length === 0;
            }
            
            // Zeigen Sie eine Erfolgsmeldung an, wenn Dateien komprimiert wurden
            const compressedCount = compressedFiles.filter(f => f.wasCompressed).length;
            if (compressedCount > 0) {
                showMessage('success', `${compressedCount} von ${compressedFiles.length} Bildern wurden für den Upload optimiert.`);
            }
        })
        .catch(error => {
            console.error('Fehler bei der Komprimierung:', error);
            
            // Falls die Komprimierung fehlschlägt, versuchen Sie es mit den Originaldateien
            // aber filtern Sie zu große Dateien heraus
            const filteredFiles = validFiles.filter(file => file.size <= MAX_FILE_SIZE);
            const tooLargeFiles = validFiles.filter(file => file.size > MAX_FILE_SIZE);
            
            if (tooLargeFiles.length > 0) {
                showMessage('error', `${tooLargeFiles.length} Dateien sind zu groß und konnten nicht komprimiert werden.`);
            }
            
            if (filteredFiles.length === 0) {
                selectedFilesContainer.style.display = 'none';
                showMessage('error', 'Keine gültigen Bilder zum Hochladen.');
                return;
            }
            
            // Merge with existing selection (optional)
            const mergeWithExisting = true;
            if (mergeWithExisting && selectedFiles.length > 0) {
                // Check for duplicates by filename
                const existingFileNames = selectedFiles.map(f => f.name);
                const newFiles = filteredFiles.filter(file => !existingFileNames.includes(file.name));
                
                // Add to existing selection
                selectedFiles = [...selectedFiles, ...newFiles];
            } else {
                // Replace existing selection
                selectedFiles = filteredFiles;
            }
            
            // Aktualisieren Sie die UI
            updateSelectedFilesUI();
            
            // Enable upload button if we have files
            const uploadFilesBtn = document.getElementById('upload-files-btn');
            if (uploadFilesBtn) {
                uploadFilesBtn.disabled = selectedFiles.length === 0;
            }
        });
}

/**
 * Update the UI to show selected files
 */
function updateSelectedFilesUI(hasCompressedFiles = false) {
    const selectedFilesContainer = document.querySelector('.selected-files-container');
    const selectedFilesList = document.getElementById('selected-files-list');
    const selectedFilesCount = document.getElementById('selected-files-count');
    
    if (!selectedFilesContainer || !selectedFilesList || !selectedFilesCount) return;
    
    // Update count
    selectedFilesCount.textContent = `${selectedFiles.length} Bilder ausgewählt${hasCompressedFiles ? ' (optimiert)' : ''}`;
    
    // Clear list
    selectedFilesList.innerHTML = '';
    
    // Create preview for each file
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'selected-file-item';
        fileItem.dataset.index = index;
        
        // Create file preview
        const reader = new FileReader();
        reader.onload = function(e) {
            const previewContainer = document.createElement('div');
            previewContainer.className = 'selected-file-preview-container';
            
            const preview = document.createElement('img');
            preview.src = e.target.result;
            preview.className = 'selected-file-preview';
            preview.alt = file.name;
            previewContainer.appendChild(preview);
            
            // Add compression badge if this file was compressed
            if (file.wasCompressed) {
                const badge = document.createElement('span');
                badge.className = 'compressed-badge';
                badge.textContent = 'Optimiert';
                previewContainer.appendChild(badge);
            }
            
            fileItem.prepend(previewContainer);
        };
        reader.readAsDataURL(file);
        
        // File info
        const fileInfo = document.createElement('div');
        fileInfo.className = 'selected-file-info';
        
        const fileName = document.createElement('div');
        fileName.className = 'selected-file-name';
        fileName.textContent = file.name;
        
        const fileSize = document.createElement('div');
        fileSize.className = 'selected-file-size';
        fileSize.textContent = formatFileSize(file.size);
        
        // If we have the original size, show the comparison
        if (file.originalSize) {
            const sizeDiff = document.createElement('div');
            sizeDiff.className = 'selected-file-size-diff';
            const savingsPercent = Math.round(100 - (file.size / file.originalSize * 100));
            sizeDiff.textContent = `${savingsPercent}% kleiner`;
            fileInfo.appendChild(sizeDiff);
        }
        
        fileInfo.appendChild(fileName);
        fileInfo.appendChild(fileSize);
        
        // Remove button
        const removeButton = document.createElement('div');
        removeButton.className = 'remove-file';
        removeButton.textContent = '×';
        removeButton.addEventListener('click', e => {
            e.stopPropagation();
            removeFileFromSelection(index);
        });
        
        fileItem.appendChild(fileInfo);
        fileItem.appendChild(removeButton);
        
        selectedFilesList.appendChild(fileItem);
    });
    
    // Show container if we have files
    selectedFilesContainer.style.display = selectedFiles.length > 0 ? 'block' : 'none';
}

/**
 * Remove a file from the selection
 */
function removeFileFromSelection(index) {
    selectedFiles.splice(index, 1);
    updateSelectedFilesUI();
    
    // Enable/disable upload button
    const uploadFilesBtn = document.getElementById('upload-files-btn');
    if (uploadFilesBtn) {
        uploadFilesBtn.disabled = selectedFiles.length === 0;
    }
}

/**
 * Handle multi-file upload form submission with improved queue processing
 */
function handleMultiFormSubmit(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const multiUploadForm = document.getElementById('multi-upload-form');
    const multiProgressBar = document.getElementById('multi-progress-bar');
    const multiProgressContainer = document.getElementById('multi-upload-progress');
    const multiProgressText = document.getElementById('multi-progress-text');
    
    if (selectedFiles.length === 0) {
        showMessage('error', 'Bitte wählen Sie mindestens ein Bild aus.');
        return;
    }
    
    if (isUploading) {
        showMessage('error', 'Ein Upload ist bereits im Gange. Bitte warten Sie.');
        return;
    }
    
    // Reset upload stats
    isUploading = true;
    uploadIndex = 0;
    successCount = 0;
    errorCount = 0;
    uploadQueue = [...selectedFiles];
    
    // Show progress container
    multiProgressContainer.style.display = 'block';
    multiProgressBar.style.width = '0%';
    multiProgressText.textContent = '0%';
    
    // Disable upload button
    const uploadFilesBtn = document.getElementById('upload-files-btn');
    if (uploadFilesBtn) {
        uploadFilesBtn.disabled = true;
        uploadFilesBtn.textContent = 'Upload läuft...';
    }
    
    // Log the number of files to upload
    console.log('Starting upload of', selectedFiles.length, 'files');
    
    // Start the upload queue
    processUploadQueue();
}

/**
 * Process the upload queue with improved parallelism
 */
function processUploadQueue() {
    const multiUploadForm = document.getElementById('multi-upload-form');
    const multiProgressBar = document.getElementById('multi-progress-bar');
    const multiProgressText = document.getElementById('multi-progress-text');
    
    if (!isUploading || uploadQueue.length === 0) {
        finishMultiUpload();
        return;
    }
    
    // Calculate progress
    const totalFiles = selectedFiles.length;
    const processedFiles = successCount + errorCount;
    const progressPercent = Math.round((processedFiles / totalFiles) * 100);
    
    // Update progress UI
    multiProgressBar.style.width = `${progressPercent}%`;
    multiProgressText.textContent = `${progressPercent}% (${processedFiles}/${totalFiles})`;
    
    // Take the next file from the queue
    const file = uploadQueue.shift();
    console.log('Uploading file:', file.name);
    
    // Create form data for this file
    const formData = new FormData();
    formData.append('images', file);
    formData.append('category_id', document.querySelector('input[name="category_id"]').value);
    formData.append('is_multiple', 'true');
    
    // Add CSRF token
    const csrfToken = getCsrfToken();
    formData.append('csrfmiddlewaretoken', csrfToken);
    
    // Log the form data
    console.log('Form data keys:', [...formData.keys()]);
    
    // Upload the file using XMLHttpRequest for better compatibility
    const xhr = new XMLHttpRequest();
    xhr.open('POST', multiUploadForm.action, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
            try {
                const data = JSON.parse(xhr.responseText);
                if (data.status === 'success') {
                    successCount++;
                    console.log(`Successfully uploaded ${file.name}`);
                    
                    // Add the photo to the grid
                    if (data.photos && data.photos.length > 0) {
                        data.photos.forEach(photo => {
                            addPhotoToGrid(photo);
                        });
                    }
                } else {
                    errorCount++;
                    console.error(`Error uploading ${file.name}: ${data.message}`);
                    showMessage('error', `Fehler beim Hochladen von ${file.name}: ${data.message}`);
                }
            } catch (e) {
                errorCount++;
                console.error(`Error parsing response for ${file.name}:`, e);
                showMessage('error', `Fehler beim Verarbeiten der Antwort für ${file.name}`);
            }
        } else {
            errorCount++;
            console.error(`HTTP error uploading ${file.name}: ${xhr.status}`);
            showMessage('error', `HTTP-Fehler beim Hochladen von ${file.name}: ${xhr.status}`);
        }
        
        // Process the next file in the queue
        processUploadQueue();
    };
    
    xhr.onerror = function() {
        errorCount++;
        console.error(`Network error uploading ${file.name}`);
        showMessage('error', `Netzwerkfehler beim Hochladen von ${file.name}`);
        
        // Continue with next file
        processUploadQueue();
    };
    
    // Send the form data
    xhr.send(formData);
}

/**
 * Finish multi-file upload process
 */
function finishMultiUpload() {
    const multiProgressContainer = document.getElementById('multi-upload-progress');
    
    isUploading = false;
    
    // Show final results
    if (successCount > 0) {
        showMessage('success', `${successCount} von ${selectedFiles.length} Bildern erfolgreich hochgeladen${errorCount > 0 ? ` (${errorCount} Fehler)` : ''}.`);
        
        // Clear selection if all successful
        if (errorCount === 0) {
            selectedFiles = [];
            updateSelectedFilesUI();
            
            // Reset form
            const multiUploadForm = document.getElementById('multi-upload-form');
            if (multiUploadForm) {
                multiUploadForm.reset();
            }
        } else {
            // Remove successful files from selection
            // (This would require tracking which files were successfully uploaded)
        }
    } else if (errorCount > 0) {
        showMessage('error', `Keine Bilder konnten hochgeladen werden (${errorCount} Fehler).`);
    }
    
    // Hide progress after a delay
    setTimeout(() => {
        if (multiProgressContainer) {
            multiProgressContainer.style.display = 'none';
        }
    }, 1000);
    
    // Re-enable upload button if files remain
    const uploadFilesBtn = document.getElementById('upload-files-btn');
    if (uploadFilesBtn) {
        uploadFilesBtn.disabled = selectedFiles.length === 0;
    }
}

/**
 * Setup upload tabs
 */
function setupUploadTabs() {
    const tabs = document.querySelectorAll('.upload-tab');
    const tabContents = document.querySelectorAll('.upload-tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabId = this.dataset.tab;
            
            // Set active tab
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Show active content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tabId) {
                    content.classList.add('active');
                }
            });
        });
    });
}

/**
 * Initialize sortable functionality
 */
function initSortable() {
    if (window.jQuery && jQuery.ui) {
        const photoGrid = document.getElementById('photo-grid');
        if (photoGrid) {
            jQuery(photoGrid).sortable({
                items: '.photo-item',
                cursor: 'move',
                opacity: 0.7,
                update: savePhotoOrder
            });
        }
    }
}

/**
 * Save the photo order after drag and drop
 */
function savePhotoOrder() {
    const photoGrid = document.getElementById('photo-grid');
    if (!photoGrid) return;
    
    const photoIds = Array.from(photoGrid.querySelectorAll('.photo-item')).map(item => {
        return parseInt(item.dataset.id, 10);
    });
    
    if (photoIds.length === 0) return;
    
    // Show loading indicator
    showMessage('info', 'Reihenfolge wird aktualisiert...');
    
    // Send the new order to the server
    fetch('/galerie/admin/order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ photos: photoIds })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            showMessage('success', 'Reihenfolge aktualisiert.');
        } else {
            showMessage('error', data.message || 'Fehler beim Aktualisieren der Reihenfolge.');
        }
    })
    .catch(error => {
        console.error('Error saving order:', error);
        showMessage('error', 'Netzwerkfehler beim Aktualisieren der Reihenfolge.');
    });
}

/**
 * Show message in the message container
 */
function showMessage(type, text) {
    const messageContainer = document.getElementById('message-container');
    if (!messageContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    
    // Clear previous messages
    messageContainer.innerHTML = '';
    messageContainer.appendChild(messageDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode === messageContainer) {
            messageDiv.remove();
        }
    }, 5000);
}

/**
 * Add a new photo to the grid
 */
function addPhotoToGrid(photo) {
    const photoGrid = document.getElementById('photo-grid');
    if (!photoGrid) return;
    
    // Create photo item
    const photoItem = document.createElement('div');
    photoItem.className = 'photo-item';
    photoItem.dataset.id = photo.id;
    
    // Create image with lazy loading
    const img = document.createElement('img');
    img.src = photo.image_url;
    img.alt = photo.title || 'Gallery Image';
    img.loading = 'lazy';
    photoItem.appendChild(img);
    
    // Create info section
    const infoDiv = document.createElement('div');
    infoDiv.className = 'photo-info';
    
    // Create title
    const title = document.createElement('h3');
    title.className = 'photo-title';
    title.textContent = photo.title || `Bild ${photo.id}`;
    infoDiv.appendChild(title);
    
    // Create actions
    const actionsDiv = document.createElement('div');
    actionsDiv.className = 'photo-actions';
    
    // Edit button
    const editBtn = document.createElement('button');
    editBtn.className = 'btn btn-sm photo-edit-btn';
    editBtn.textContent = 'Bearbeiten';
    editBtn.addEventListener('click', () => {
        openEditPhotoModal(photo.id);
    });
    actionsDiv.appendChild(editBtn);
    
    // Delete button
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'btn btn-sm btn-secondary photo-delete-btn';
    deleteBtn.textContent = 'Löschen';
    deleteBtn.addEventListener('click', () => {
        deletePhoto(photo.id);
    });
    actionsDiv.appendChild(deleteBtn);
    
    infoDiv.appendChild(actionsDiv);
    photoItem.appendChild(infoDiv);
    
    // Add to the beginning of the grid
    if (photoGrid.firstChild) {
        photoGrid.insertBefore(photoItem, photoGrid.firstChild);
    } else {
        photoGrid.appendChild(photoItem);
    }
    
    // Animate new photo
    photoItem.style.opacity = '0';
    photoItem.style.transform = 'translateY(10px)';
    
    setTimeout(() => {
        photoItem.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        photoItem.style.opacity = '1';
        photoItem.style.transform = 'translateY(0)';
    }, 10);
    
    // Refresh sortable
    if (window.jQuery && jQuery.ui) {
        jQuery(photoGrid).sortable('refresh');
    }
}

/**
 * Set up modal functionality
 */
function setupModals() {
    // Get all close buttons
    document.querySelectorAll('.close-modal').forEach(button => {
        const modalId = button.closest('.modal').id;
        button.addEventListener('click', () => {
            closeModal(modalId);
        });
    });
    
    // Close when clicking outside
    window.addEventListener('click', e => {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
    
    // Setup form submissions
    const editPhotoForm = document.getElementById('edit-photo-form');
    if (editPhotoForm) {
        editPhotoForm.addEventListener('submit', submitEditPhotoForm);
    }
    
    const newCategoryForm = document.getElementById('new-category-form');
    if (newCategoryForm) {
        newCategoryForm.addEventListener('submit', submitNewCategoryForm);
    }
    
    const editCategoryForm = document.getElementById('edit-category-form');
    if (editCategoryForm) {
        editCategoryForm.addEventListener('submit', submitEditCategoryForm);
    }
}

/**
 * Set up category tab click handlers
 */
function setupCategoryTabs() {
    document.querySelectorAll('.category-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            const categoryId = this.dataset.categoryId;
            window.location.href = `/galerie/admin/?category=${categoryId}`;
        });
    });
}

/**
 * Setup photo action handlers
 */
function setupPhotoActions() {
    // Edit buttons
    document.querySelectorAll('.photo-edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const photoId = this.closest('.photo-item').dataset.id;
            openEditPhotoModal(photoId);
        });
    });
    
    // Delete buttons
    document.querySelectorAll('.photo-delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const photoId = this.closest('.photo-item').dataset.id;
            deletePhoto(photoId);
        });
    });
}

/**
 * Setup category action handlers
 */
function setupCategoryActions() {
    // New category button
    const newCategoryBtn = document.getElementById('new-category-btn');
    if (newCategoryBtn) {
        newCategoryBtn.addEventListener('click', function() {
            openModal('new-category-modal');
        });
    }
    
    // Edit category button
    const editCategoryBtn = document.getElementById('edit-category-btn');
    if (editCategoryBtn) {
        editCategoryBtn.addEventListener('click', function() {
            const activeTab = document.querySelector('.category-tab.active');
            if (!activeTab) return;
            
            const categoryId = activeTab.dataset.categoryId;
            const categoryTitle = activeTab.textContent.trim();
            
            document.getElementById('edit-category-id').value = categoryId;
            document.getElementById('edit-category-title').value = categoryTitle;
            
            openModal('edit-category-modal');
        });
    }
    
    // Delete category button
    const deleteCategoryBtn = document.getElementById('delete-category-btn');
    if (deleteCategoryBtn) {
        deleteCategoryBtn.addEventListener('click', function() {
            const activeTab = document.querySelector('.category-tab.active');
            if (!activeTab) return;
            
            const categoryId = activeTab.dataset.categoryId;
            
            if (confirm('Sind Sie sicher, dass Sie diese Kategorie löschen möchten? Alle zugehörigen Bilder werden ebenfalls gelöscht!')) {
                deleteCategory(categoryId);
            }
        });
    }
}

/**
 * Open a modal by ID
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        
        // Add animation class
        modal.classList.add('modal-open');
        
        // Focus first input if present
        setTimeout(() => {
            const firstInput = modal.querySelector('input[type="text"]');
            if (firstInput) {
                firstInput.focus();
            }
        }, 100);
    }
}

/**
 * Close a modal by ID
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('modal-open');
        modal.classList.add('modal-closing');
        
        setTimeout(() => {
            modal.style.display = 'none';
            modal.classList.remove('modal-closing');
        }, 300);
    }
}

/**
 * Open edit photo modal
 */
function openEditPhotoModal(photoId) {
    const photoItem = document.querySelector(`.photo-item[data-id="${photoId}"]`);
    if (!photoItem) return;
    
    // Get existing data from the DOM
    const title = photoItem.querySelector('.photo-title').textContent;
    
    // Set form values
    document.getElementById('edit-photo-id').value = photoId;
    document.getElementById('edit-photo-title').value = title;
    
    // Clear previous data
    document.getElementById('edit-photo-description').value = '';
    document.getElementById('edit-photo-copyright').value = '';
    
    // Show loading state
    const modalTitle = document.querySelector('#edit-photo-modal .modal-title');
    if (modalTitle) {
        modalTitle.innerHTML = 'Bild wird geladen...';
    }
    
    // Try to get additional data from the server
    fetch(`/galerie/admin/edit/${photoId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success' && data.photo) {
            document.getElementById('edit-photo-description').value = data.photo.description || '';
            document.getElementById('edit-photo-copyright').value = data.photo.copyright_by || '';
            
            // Update modal title
            if (modalTitle) {
                modalTitle.innerHTML = 'Bild bearbeiten';
            }
        }
    })
    .catch(error => {
        console.error('Error fetching photo data:', error);
        showMessage('error', 'Fehler beim Laden der Bilddaten.');
    })
    .finally(() => {
        // Open modal
        openModal('edit-photo-modal');
    });
}

/**
 * Submit edit photo form
 */
function submitEditPhotoForm(e) {
    e.preventDefault();
    
    const photoId = document.getElementById('edit-photo-id').value;
    const title = document.getElementById('edit-photo-title').value;
    const description = document.getElementById('edit-photo-description').value;
    const copyright = document.getElementById('edit-photo-copyright').value;
    
    // Show loading state
    const submitBtn = this.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Wird gespeichert...';
    }
    
    fetch(`/galerie/admin/edit/${photoId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            title: title,
            description: description,
            copyright_by: copyright
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            // Update title in the DOM
            const photoItem = document.querySelector(`.photo-item[data-id="${photoId}"]`);
            if (photoItem) {
                photoItem.querySelector('.photo-title').textContent = title || `Bild ${photoId}`;
            }
            
            showMessage('success', 'Bild aktualisiert.');
            closeModal('edit-photo-modal');
        } else {
            showMessage('error', data.message || 'Fehler beim Aktualisieren des Bildes.');
        }
    })
    .catch(error => {
        console.error('Error updating photo:', error);
        showMessage('error', 'Netzwerkfehler beim Aktualisieren des Bildes.');
    })
    .finally(() => {
        // Reset button state
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Speichern';
        }
    });
}

/**
 * Delete a photo with confirmation
 */
function deletePhoto(photoId) {
    if (!confirm('Sind Sie sicher, dass Sie dieses Bild löschen möchten?')) {
        return;
    }
    
    // Find photo item
    const photoItem = document.querySelector(`.photo-item[data-id="${photoId}"]`);
    if (photoItem) {
        // Add deleting state
        photoItem.classList.add('deleting');
    }
    
    fetch(`/galerie/admin/delete/${photoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            // Animate removal
            if (photoItem) {
                photoItem.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                photoItem.style.opacity = '0';
                photoItem.style.transform = 'scale(0.9)';
                
                setTimeout(() => {
                    photoItem.remove();
                }, 300);
            }
            
            showMessage('success', 'Bild gelöscht.');
        } else {
            if (photoItem) {
                photoItem.classList.remove('deleting');
            }
            showMessage('error', data.message || 'Fehler beim Löschen des Bildes.');
        }
    })
    .catch(error => {
        console.error('Error deleting photo:', error);
        if (photoItem) {
            photoItem.classList.remove('deleting');
        }
        showMessage('error', 'Netzwerkfehler beim Löschen des Bildes.');
    });
}

/**
 * Submit new category form
 */
function submitNewCategoryForm(e) {
    e.preventDefault();
    
    const title = document.getElementById('new-category-title').value;
    
    if (!title.trim()) {
        showMessage('error', 'Bitte geben Sie einen Kategorietitel ein.');
        return;
    }
    
    // Disable submit button
    const submitBtn = this.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Wird gespeichert...';
    }
    
    fetch('/galerie/admin/category/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            title: title
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            showMessage('success', 'Kategorie erstellt.');
            closeModal('new-category-modal');
            
            // Redirect to the new category
            window.location.href = `/galerie/admin/?category=${data.category.id}`;
        } else {
            showMessage('error', data.message || 'Fehler beim Erstellen der Kategorie.');
        }
    })
    .catch(error => {
        console.error('Error creating category:', error);
        showMessage('error', 'Netzwerkfehler beim Erstellen der Kategorie.');
    })
    .finally(() => {
        // Reset button state
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Speichern';
        }
    });
}

/**
 * Submit edit category form
 */
function submitEditCategoryForm(e) {
    e.preventDefault();
    
    const categoryId = document.getElementById('edit-category-id').value;
    const title = document.getElementById('edit-category-title').value;
    
    if (!title.trim()) {
        showMessage('error', 'Bitte geben Sie einen Kategorietitel ein.');
        return;
    }
    
    // Disable submit button
    const submitBtn = this.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Wird gespeichert...';
    }
    
    fetch(`/galerie/admin/category/edit/${categoryId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            title: title
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            // Update title in the DOM
            const categoryTab = document.querySelector(`.category-tab[data-category-id="${categoryId}"]`);
            if (categoryTab) {
                categoryTab.textContent = title;
            }
            
            showMessage('success', 'Kategorie aktualisiert.');
            closeModal('edit-category-modal');
        } else {
            showMessage('error', data.message || 'Fehler beim Aktualisieren der Kategorie.');
        }
    })
    .catch(error => {
        console.error('Error updating category:', error);
        showMessage('error', 'Netzwerkfehler beim Aktualisieren der Kategorie.');
    })
    .finally(() => {
        // Reset button state
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Speichern';
        }
    });
}

/**
 * Delete a category with confirmation
 */
function deleteCategory(categoryId) {
    fetch(`/galerie/admin/category/delete/${categoryId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            showMessage('success', 'Kategorie gelöscht.');
            
            // Redirect to the first available category
            window.location.href = '/galerie/admin/';
        } else {
            showMessage('error', data.message || 'Fehler beim Löschen der Kategorie.');
        }
    })
    .catch(error => {
        console.error('Error deleting category:', error);
        showMessage('error', 'Netzwerkfehler beim Löschen der Kategorie.');
    });
}

/**
 * Format file size in human-readable format
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
 * Get CSRF token from cookies
 */
function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    
    return cookieValue;
}

/**
 * Prevent default event behavior
 */
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}
