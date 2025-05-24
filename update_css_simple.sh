#!/bin/bash

# CSS Version Update Script - Simple Version
# ==========================================
# Updates all CSS files and references to a specific version
# Usage: ./update_css_simple.sh 3.0.0

set -e

VERSION="$1"
PROJECT_ROOT="$(pwd)"
BACKUP_DIR="css_backup_$(date +%Y%m%d_%H%M%S)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Validate input
if [ -z "$VERSION" ]; then
    log_error "Usage: $0 <version>"
    log_error "Example: $0 3.0.0"
    exit 1
fi

if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    log_error "Version must be in format X.Y.Z (e.g., 3.0.0)"
    exit 1
fi

log_info "CSS Version Update Script"
log_info "========================="
log_info "Project Root: $PROJECT_ROOT"
log_info "Target Version: $VERSION"
echo

# Create backup directory
log_info "Creating backup directory: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Find and process CSS files
log_info "Finding CSS files..."
declare -a CSS_FILES
while IFS= read -r -d $'\0' file; do
    CSS_FILES+=("$file")
done < <(find . -name "*.css" -type f -print0)

log_info "Found ${#CSS_FILES[@]} CSS files"

if [ ${#CSS_FILES[@]} -eq 0 ]; then
    log_warning "No CSS files found!"
    exit 0
fi

# Process each CSS file
log_info "Processing CSS files..."
declare -A CSS_CHANGES

for css_file in "${CSS_FILES[@]}"; do
    # Create backup
    backup_path="$BACKUP_DIR/${css_file#./}"
    mkdir -p "$(dirname "$backup_path")"
    cp "$css_file" "$backup_path"
    
    # Get filename without path and extension
    filename=$(basename "$css_file" .css)
    dirname=$(dirname "$css_file")
    
    # Remove existing version if present
    filename_clean=$(echo "$filename" | sed 's/\.[0-9]\+\.[0-9]\+\.[0-9]\+$//')
    
    # Create new filename
    new_filename="${filename_clean}.${VERSION}.css"
    new_path="${dirname}/${new_filename}"
    
    # Rename file
    mv "$css_file" "$new_path"
    
    # Store change for template updates
    CSS_CHANGES["$(basename "$css_file")"]="$new_filename"
    
    log_success "Renamed: $css_file -> $new_path"
done

log_success "CSS version update completed successfully!"
echo "Backup created in: $BACKUP_DIR"