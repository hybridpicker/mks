#!/bin/bash

# MKS Claude Cleanup Script
# Erkennt und entfernt unwichtige Markdown-Dateien, die typischerweise von Claude generiert werden

# Define colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Helper functions
print_section() {
    echo -e "\n${BOLD}${BLUE}$1${NC}"
    echo -e "${BLUE}$(printf '─%.0s' {1..50})${NC}"
}

print_info() {
    echo -e "${BLUE}  ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}  ✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}  ⚠️  $1${NC}"
}

print_cleanup() {
    echo -e "${PURPLE}  🧹 $1${NC}"
}

# Patterns that indicate Claude-generated documentation
CLAUDE_PATTERNS=(
    "# MKS Project"
    "# Test.*Structure"
    "# Git Hooks Integration"
    "# Problem.*Resolved"
    "# Migrations.*Anweisungen"
    "Diese Django-App"
    "Diese organisierte.*struktur"
    "Bitte lege hier.*ab"
    "# Placeholder für"
    "Das originale Bild sollte"
    "# Event Default Image"
    "CLAUDE CLEANUP"
    "Comprehensive Test Suite"
)

# Files and patterns to NEVER delete (whitelist)
PROTECTED_PATTERNS=(
    "README.md$"  # Main project README
    "LICENSE.*md$"
    "CHANGELOG.*md$"
    "CONTRIBUTING.*md$"
    "/vendor/"
    "/node_modules/"
    "animate.*README"
    "tinymce.*README"
    "select2.*LICENSE"
)
# Function to check if file is protected
is_protected_file() {
    local file="$1"
    
    # Check against protected patterns
    for pattern in "${PROTECTED_PATTERNS[@]}"; do
        if [[ "$file" =~ $pattern ]]; then
            return 0  # Protected
        fi
    done
    
    return 1  # Not protected
}

# Function to check if file contains Claude-generated content
is_claude_generated() {
    local file="$1"
    
    if [[ ! -f "$file" ]]; then
        return 1
    fi
    
    # Read first 10 lines of file
    local content=$(head -n 10 "$file" 2>/dev/null)
    
    # Check against Claude patterns
    for pattern in "${CLAUDE_PATTERNS[@]}"; do
        if echo "$content" | grep -qi "$pattern"; then
            return 0  # Is Claude-generated
        fi
    done
    
    return 1  # Not Claude-generated
}

# Main cleanup function
cleanup_claude_files() {
    local project_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
    cd "$project_root"
    
    print_section "🤖 Claude Markdown Cleanup"
    print_info "Scanning for Claude-generated .md files..."
    
    # Find all .md files
    local md_files=()
    while IFS= read -r -d '' file; do
        md_files+=("$file")
    done < <(find . -name "*.md" -type f -print0 2>/dev/null)
    
    if [[ ${#md_files[@]} -eq 0 ]]; then
        print_info "No .md files found"
        return 0
    fi
    
    print_info "Found ${#md_files[@]} .md files"    
    local cleaned_count=0
    local protected_count=0
    local kept_count=0
    
    for file in "${md_files[@]}"; do
        # Skip if protected
        if is_protected_file "$file"; then
            print_info "Protected: $file"
            ((protected_count++))
            continue
        fi
        
        # Check if Claude-generated
        if is_claude_generated "$file"; then
            print_cleanup "Removing Claude-generated file: $file"
            if rm "$file" 2>/dev/null; then
                print_success "Deleted: $file"
                ((cleaned_count++))
            else
                print_warning "Failed to delete: $file"
            fi
        else
            print_info "Keeping: $file"
            ((kept_count++))
        fi
    done
    
    # Summary
    print_section "📊 Cleanup Summary"
    echo -e "${GREEN}  🗑️  Removed: ${cleaned_count} Claude-generated files${NC}"
    echo -e "${BLUE}  🛡️  Protected: ${protected_count} files${NC}"
    echo -e "${YELLOW}  📄 Kept: ${kept_count} other files${NC}"
    
    if [[ $cleaned_count -gt 0 ]]; then
        print_success "Cleanup completed - removed $cleaned_count unwanted files"
        return 0
    else
        print_info "No cleanup needed - all files are legitimate"
        return 0
    fi
}

# Run cleanup
cleanup_claude_files