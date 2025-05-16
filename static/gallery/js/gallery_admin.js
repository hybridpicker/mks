/**
 * Gallery admin functionality with drag and drop support.
 * Provides image upload, reordering, editing, and deletion for gallery management.
 */

// Constants
const MAX_FILE_SIZE = 2 * 1024 * 1024; // 2MB
const MAX_FILES = 100; // Maximum number of files allowed
const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

// DOM elements
let dropZone;
let fileInput;
let uploadForm;
let progressBar;
let progressContainer;
let progressText;
let messageContainer;
let photoGrid;
let selectedFileInfo;

// Multiple upload elements
let multiDropZone;
let multiFileInput;
let multiUploadForm;
let multiProgressBar;
let multiProgressContainer;
let multiProgressText;
let selectedFilesContainer;
let selectedFilesList;
let selectedFilesCount;
let uploadFilesBtn;

// File list for multiple uploads
let selectedFiles = [];

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Find elements
    dropZone = document.getElementById('drop-zone');
    fileInput = document.getElementById('file-input');
    uploadForm = document.getElementById('upload-form');
    progressBar = document.getElementById('progress-bar');
    progressContainer = document.getElementById('upload-progress');
    progressText = document.getElementById('progress-text');
    messageContainer = document.getElementById('message-container');
    photoGrid = document.getElementById('photo-grid');
    selectedFileInfo = document.getElementById('selected-file');
    
    // Multiple upload elements
    multiDropZone = document.getElementById('multi-drop-zone');
    multiFileInput = document.getElementById('multi-file-input');
    multiUploadForm = document.getElementById('multi-upload-form');
    multiProgressBar = document.getElementById('multi-progress-bar');
    multiProgressContainer = document.getElementById('multi-upload-progress');
    multiProgressText = document.getElementById('multi-progress-text');
    selectedFilesContainer = document.querySelector('.selected-files-container');
    selectedFilesList = document.getElementById('selected-files-list');
    selectedFilesCount = document.getElementById('selected-files-count');
    uploadFilesBtn = document.getElementById('upload-files-btn');
    
    // Setup upload tabs
    setupUploadTabs();
    
    // Setup drag and drop for single uploads
    if (dropZone && fileInput) {
        setupDragAndDrop();
    }
    
    // Setup drag and drop for multiple uploads
    if (multiDropZone && multiFileInput) {
        setupMultiDragAndDrop();
    }
    
    // Setup form submissions
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleFormSubmit);
    }
    
    if (multiUploadForm) {
        multiUploadForm.addEventListener('submit', handleMultiFormSubmit);
    }
    
    // Setup sortable functionality
    initSortable();
    
    // Setup modal handlers
    setupModals();
    
    // Setup category tab click handlers
    setupCategoryTabs();
    
    // Setup photo action handlers
    setupPhotoActions();
    
    // Setup category action handlers
    setupCategoryActions();
});

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
 * Setup multiple files drag and drop
 */
function setupMultiDragAndDrop() {
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        multiDropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    // Highlight drop zone when items are dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        multiDropZone.addEventListener(eventName, function() {
            multiDropZone.classList.add('dragover');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        multiDropZone.addEventListener(eventName, function() {
            multiDropZone.classList.remove('dragover');
        }, false);
    });
    
    // Handle dropped files
    multiDropZone.addEventListener('drop', handleMultiDrop, false);
    
    // Handle file input change
    multiFileInput.addEventListener('change', handleMultiFilesSelected);
    
    // Handle the click to trigger file input
    document.getElementById('select-files-btn').addEventListener('click', function() {
        multiFileInput.click();
    });
    
    // Handle click on drop zone
    multiDropZone.addEventListener('click', function() {
        multiFileInput.click();
    });
}

/**
 * Handle drop for multiple files
 */
function handleMultiDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    console.log(`Drag and drop detected ${files.length} files`);
    
    // Ensure we handle multiple files
    if (files.length > 0) {
        handleMultipleFiles(files);
    }
}

/**
 * Handle multiple files selection
 */
function handleMultiFilesSelected(e) {
    if (e.target.files.length > 0) {
        handleMultipleFiles(e.target.files);
    }
}

/**
 * Process multiple files for upload
 */
function handleMultipleFiles(files) {
    // Convert FileList to Array
    const fileArray = Array.from(files);
    
    console.log(`Processing ${fileArray.length} files for upload`);
    
    // Check if too many files
    if (fileArray.length > MAX_FILES) {
        showMessage('error', `Zu viele Dateien ausgewählt. Maximal ${MAX_FILES} Bilder erlaubt.`);
        return;
    }
    
    // Filter valid files
    let validFiles = [];
    let invalidFilesCount = 0;
    
    fileArray.forEach(file => {
        // Check file type
        if (!ALLOWED_MIME_TYPES.includes(file.type)) {
            showMessage('error', `"${file.name}" hat einen ungültigen Dateityp.`);
            invalidFilesCount++;
            return;
        }
        
        // Check file size
        if (file.size > MAX_FILE_SIZE) {
            showMessage('error', `"${file.name}" ist zu groß (${(file.size / 1024 / 1024).toFixed(2)}MB). Maximale Größe ist 2MB.`);
            invalidFilesCount++;
            return;
        }
        
        validFiles.push(file);
    });
    
    console.log(`Found ${validFiles.length} valid files and ${invalidFilesCount} invalid files`);
    
    if (validFiles.length === 0) {
        showMessage('error', 'Keine gültigen Bilder ausgewählt.');
        return;
    }
    
    // Add files to the list
    selectedFiles = validFiles;
    
    // Display selected files
    showSelectedFiles();
    
    // Create a DataTransfer object to update the file input
    // Note: This might not work in all browsers, but is used as a backup
    try {
        const dataTransfer = new DataTransfer();
        selectedFiles.forEach(file => {
            dataTransfer.items.add(file);
        });
        
        // Update file input
        multiFileInput.files = dataTransfer.files;
    } catch (e) {
        console.error('Error updating file input:', e);
        // We can still proceed without this, as we store the files in selectedFiles
    }
    
    // Enable upload button
    uploadFilesBtn.disabled = selectedFiles.length === 0;
}

/**
 * Display selected files in the UI
 */
function showSelectedFiles() {
    // Update count
    selectedFilesCount.textContent = `${selectedFiles.length} Bilder ausgewählt`;
    
    // Clear list
    selectedFilesList.innerHTML = '';
    
    // Create preview for each file
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'selected-file-item';
        fileItem.dataset.index = index;
        
        // Create file preview if possible
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.createElement('img');
            preview.src = e.target.result;
            preview.className = 'selected-file-preview';
            preview.alt = file.name;
            fileItem.prepend(preview);
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
        
        fileInfo.appendChild(fileName);
        fileInfo.appendChild(fileSize);
        
        // Remove button
        const removeButton = document.createElement('div');
        removeButton.className = 'remove-file';
        removeButton.textContent = '×';
        removeButton.addEventListener('click', function(e) {
            e.stopPropagation();
            removeFile(index);
        });
        
        fileItem.appendChild(fileInfo);
        fileItem.appendChild(removeButton);
        
        selectedFilesList.appendChild(fileItem);
    });
    
    // Show container if we have files
    if (selectedFiles.length > 0) {
        selectedFilesContainer.style.display = 'block';
    } else {
        selectedFilesContainer.style.display = 'none';
    }
}

/**
 * Remove a file from the selection
 */
function removeFile(index) {
    selectedFiles.splice(index, 1);
    
    // Create a DataTransfer object to update the file input
    const dataTransfer = new DataTransfer();
    selectedFiles.forEach(file => {
        dataTransfer.items.add(file);
    });
    
    // Update file input
    multiFileInput.files = dataTransfer.files;
    
    // Update UI
    showSelectedFiles();
    
    // Enable/disable upload button
    uploadFilesBtn.disabled = selectedFiles.length === 0;
}

/**
 * Handle form submission for multiple photos
 */
function handleMultiFormSubmit(e) {
    e.preventDefault();
    
    if (selectedFiles.length === 0) {
        showMessage('error', 'Bitte wählen Sie mindestens ein Bild aus.');
        return;
    }
    
    console.log(`Submitting ${selectedFiles.length} files for upload`);
    
    // Create FormData
    const formData = new FormData(multiUploadForm);
    
    // Remove any existing 'images' fields
    formData.delete('images');
    
    // Add all files
    for (let i = 0; i < selectedFiles.length; i++) {
        formData.append('images', selectedFiles[i]);
    }
    
    // Show progress container
    multiProgressContainer.style.display = 'block';
    multiProgressBar.style.width = '0%';
    multiProgressText.textContent = '0%';
    
    // Submit using AJAX
    const xhr = new XMLHttpRequest();
    
    // Handle progress
    xhr.upload.addEventListener('progress', e => {
        if (e.lengthComputable) {
            const percent = Math.round((e.loaded / e.total) * 100);
            multiProgressBar.style.width = percent + '%';
            multiProgressText.textContent = percent + '%';
        }
    });
    
    // Handle completion
    xhr.addEventListener('load', function() {
        try {
            const response = JSON.parse(xhr.responseText);
            
            if (xhr.status === 200 && response.status === 'success') {
                const fileCount = selectedFiles.length;
                showMessage('success', `${response.photos.length} von ${fileCount} Bildern erfolgreich hochgeladen.`);
                
                // Add the photos to the grid
                if (response.photos && response.photos.length > 0) {
                    response.photos.forEach(photo => {
                        addPhotoToGrid(photo);
                    });
                }
                
                // Show errors if any
                if (response.errors && response.errors.length > 0) {
                    response.errors.forEach(error => {
                        showMessage('error', error);
                    });
                }
                
                // Reset form
                multiUploadForm.reset();
                selectedFiles = [];
                selectedFilesContainer.style.display = 'none';
                uploadFilesBtn.disabled = true;
            } else {
                showMessage('error', response.message || 'Fehler beim Hochladen der Bilder.');
                
                // Show errors if any
                if (response.errors && response.errors.length > 0) {
                    response.errors.forEach(error => {
                        showMessage('error', error);
                    });
                }
            }
        } catch (e) {
            console.error('Error parsing response:', e);
            showMessage('error', 'Fehler beim Verarbeiten der Serverantwort.');
        }
        
        // Hide progress after a delay
        setTimeout(() => {
            multiProgressContainer.style.display = 'none';
        }, 1000);
    });
    
    // Handle errors
    xhr.addEventListener('error', function() {
        showMessage('error', 'Netzwerkfehler beim Hochladen der Bilder.');
        multiProgressContainer.style.display = 'none';
    });
    
    // Send request
    xhr.open('POST', multiUploadForm.action, true);
    xhr.send(formData);
}

/**
 * Sets up drag and drop functionality for the upload zone
 */
function setupDragAndDrop() {
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    // Highlight drop zone when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });
    
    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);
    
    // Handle file input change
    fileInput.addEventListener('change', handleFileSelected);
    
    // Handle the button click to trigger file input
    document.getElementById('select-file-btn').addEventListener('click', function() {
        fileInput.click();
    });
}

/**
 * Handles file input selection
 */
function handleFileSelected(e) {
    if (e.target.files.length > 0) {
        handleFiles(e.target.files);
    }
}

/**
 * Process files for upload
 */
function handleFiles(files) {
    const file = files[0]; // Only process the first file
    
    // Validate file type
    if (!ALLOWED_MIME_TYPES.includes(file.type)) {
        showMessage('error', 'Ungültiger Dateityp. Erlaubte Typen: JPG, PNG, GIF, WEBP');
        return;
    }
    
    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
        showMessage('error', `Die Datei ist zu groß (max. 2MB). Ihre Datei ist ${(file.size / 1024 / 1024).toFixed(2)}MB.`);
        return;
    }
    
    // Update file input
    fileInput.files = files;
    
    // Show selected file info
    selectedFileInfo.textContent = `Ausgewählte Datei: ${file.name} (${formatFileSize(file.size)})`;
    selectedFileInfo.style.display = 'block';
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
 * Handle form submission for photo upload
 */
function handleFormSubmit(e) {
    e.preventDefault();
    
    if (!fileInput.files.length) {
        showMessage('error', 'Bitte wählen Sie eine Datei aus.');
        return;
    }
    
    // Create FormData
    const formData = new FormData(uploadForm);
    
    // Show progress container
    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';
    progressText.textContent = '0%';
    
    // Submit using AJAX
    const xhr = new XMLHttpRequest();
    
    // Handle progress
    xhr.upload.addEventListener('progress', e => {
        if (e.lengthComputable) {
            const percent = Math.round((e.loaded / e.total) * 100);
            progressBar.style.width = percent + '%';
            progressText.textContent = percent + '%';
        }
    });
    
    // Handle completion
    xhr.addEventListener('load', function() {
        try {
            const response = JSON.parse(xhr.responseText);
            
            if (xhr.status === 200 && response.status === 'success') {
                showMessage('success', 'Bild erfolgreich hochgeladen.');
                
                // Reset form
                uploadForm.reset();
                selectedFileInfo.style.display = 'none';
                
                // Add the photo to the grid
                if (response.photo) {
                    addPhotoToGrid(response.photo);
                }
                
                // Reload the page if we don't have the photo data
                if (!response.photo) {
                    window.location.reload();
                }
            } else {
                showMessage('error', response.message || 'Fehler beim Hochladen des Bildes.');
            }
        } catch (e) {
            showMessage('error', 'Fehler beim Verarbeiten der Serverantwort.');
        }
        
        // Hide progress after a delay
        setTimeout(() => {
            progressContainer.style.display = 'none';
        }, 1000);
    });
    
    // Handle errors
    xhr.addEventListener('error', function() {
        showMessage('error', 'Netzwerkfehler beim Hochladen des Bildes.');
        progressContainer.style.display = 'none';
    });
    
    // Send request
    xhr.open('POST', uploadForm.action, true);
    xhr.send(formData);
}

/**
 * Show message in the message container
 */
function showMessage(type, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    
    // Clear previous messages
    messageContainer.innerHTML = '';
    messageContainer.appendChild(messageDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

/**
 * Initialize sortable functionality for photos
 */
function initSortable() {
    if (window.jQuery && jQuery.ui && photoGrid) {
        jQuery(photoGrid).sortable({
            items: '.photo-item',
            cursor: 'move',
            opacity: 0.7,
            update: function() {
                savePhotoOrder();
            }
        });
    }
}

/**
 * Save the new order of photos
 */
function savePhotoOrder() {
    const photoIds = Array.from(photoGrid.querySelectorAll('.photo-item')).map(item => {
        return parseInt(item.dataset.id, 10);
    });
    
    if (photoIds.length === 0) return;
    
    // Send the new order to the server
    fetch('/galerie/admin/order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ photos: photoIds })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showMessage('success', 'Reihenfolge aktualisiert.');
        } else {
            showMessage('error', data.message || 'Fehler beim Aktualisieren der Reihenfolge.');
        }
    })
    .catch(error => {
        showMessage('error', 'Netzwerkfehler beim Aktualisieren der Reihenfolge.');
    });
}

/**
 * Get CSRF token from cookies
 */
function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length);
        }
    }
    return '';
}

/**
 * Add a new photo to the grid
 */
function addPhotoToGrid(photo) {
    if (!photoGrid) return;
    
    // Create photo item
    const photoItem = document.createElement('div');
    photoItem.className = 'photo-item';
    photoItem.dataset.id = photo.id;
    
    // Create image
    const img = document.createElement('img');
    img.src = photo.image_url;
    img.alt = photo.title || 'Gallery Image';
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
    editBtn.className = 'btn btn-sm';
    editBtn.textContent = 'Bearbeiten';
    editBtn.addEventListener('click', function() {
        openEditPhotoModal(photo.id);
    });
    actionsDiv.appendChild(editBtn);
    
    // Delete button
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'btn btn-sm btn-secondary';
    deleteBtn.textContent = 'Löschen';
    deleteBtn.addEventListener('click', function() {
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
    
    // Setup form submission for edit photo modal
    const editPhotoForm = document.getElementById('edit-photo-form');
    if (editPhotoForm) {
        editPhotoForm.addEventListener('submit', submitEditPhotoForm);
    }
    
    // Setup form submission for category modals
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
 * Open a modal by ID
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    }
}

/**
 * Close a modal by ID
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
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
            const categoryId = document.querySelector('.category-tab.active').dataset.categoryId;
            const categoryTitle = document.querySelector('.category-tab.active').textContent.trim();
            
            document.getElementById('edit-category-id').value = categoryId;
            document.getElementById('edit-category-title').value = categoryTitle;
            
            openModal('edit-category-modal');
        });
    }
    
    // Delete category button
    const deleteCategoryBtn = document.getElementById('delete-category-btn');
    if (deleteCategoryBtn) {
        deleteCategoryBtn.addEventListener('click', function() {
            const categoryId = document.querySelector('.category-tab.active').dataset.categoryId;
            if (confirm('Sind Sie sicher, dass Sie diese Kategorie löschen möchten? Alle zugehörigen Bilder werden ebenfalls gelöscht!')) {
                deleteCategory(categoryId);
            }
        });
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
    
    // Try to get additional data from the server if needed
    fetch(`/galerie/admin/edit/${photoId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success' && data.photo) {
            document.getElementById('edit-photo-description').value = data.photo.description || '';
            document.getElementById('edit-photo-copyright').value = data.photo.copyright_by || '';
        }
    })
    .catch(error => {
        console.error('Error fetching photo data:', error);
    });
    
    // Open modal
    openModal('edit-photo-modal');
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
    
    fetch(`/galerie/admin/edit/${photoId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            title: title,
            description: description,
            copyright_by: copyright
        })
    })
    .then(response => response.json())
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
        showMessage('error', 'Netzwerkfehler beim Aktualisieren des Bildes.');
    });
}

/**
 * Delete a photo
 */
function deletePhoto(photoId) {
    if (!confirm('Sind Sie sicher, dass Sie dieses Bild löschen möchten?')) {
        return;
    }
    
    fetch(`/galerie/admin/delete/${photoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Remove from DOM
            const photoItem = document.querySelector(`.photo-item[data-id="${photoId}"]`);
            if (photoItem) {
                photoItem.remove();
            }
            
            showMessage('success', 'Bild gelöscht.');
        } else {
            showMessage('error', data.message || 'Fehler beim Löschen des Bildes.');
        }
    })
    .catch(error => {
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
    
    fetch('/galerie/admin/category/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            title: title
        })
    })
    .then(response => response.json())
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
        showMessage('error', 'Netzwerkfehler beim Erstellen der Kategorie.');
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
    
    fetch(`/galerie/admin/category/edit/${categoryId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            title: title
        })
    })
    .then(response => response.json())
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
        showMessage('error', 'Netzwerkfehler beim Aktualisieren der Kategorie.');
    });
}

/**
 * Delete a category
 */
function deleteCategory(categoryId) {
    fetch(`/galerie/admin/category/delete/${categoryId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
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
        showMessage('error', 'Netzwerkfehler beim Löschen der Kategorie.');
    });
}
