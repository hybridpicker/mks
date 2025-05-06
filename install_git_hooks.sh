#!/bin/bash

# Skript zum Installieren der Git-Hooks für das MKS-Projekt

# Pfad zum Git-Hooks-Verzeichnis
HOOKS_DIR=".git/hooks"

# Kopieren des pre-push-Hooks
cat > $HOOKS_DIR/pre-push << 'EOF'
#!/bin/bash

# Define colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running Django tests before push...${NC}"

# Get current branch name
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "Current branch: ${YELLOW}$BRANCH${NC}"

# Path to python interpreter (adjust if using virtualenv/conda)
PYTHON_CMD="python"
if command -v conda &> /dev/null; then
    # Check if mks conda environment exists and use it
    if conda env list | grep -q "mks"; then
        echo -e "${YELLOW}Using conda mks environment${NC}"
        source "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate mks
        PYTHON_CMD="python"
    fi
fi

# Save current git stash
STASH_NAME="pre-push-tests-$(date +%s)"
git stash push -q --keep-index --include-untracked --message "$STASH_NAME"
STASH_RESULT=$?

# Function to restore stashed changes
restore_stash() {
    if [ $STASH_RESULT -eq 0 ]; then
        STASH_ID=$(git stash list | grep "$STASH_NAME" | cut -d: -f1)
        if [ -n "$STASH_ID" ]; then
            echo -e "${YELLOW}Restoring your working directory changes...${NC}"
            git stash pop -q "$STASH_ID"
        fi
    fi
}

# Note: Fixture generation has been removed to preserve manual updates

# Execute django tests
cd "$(git rev-parse --show-toplevel)"
echo -e "${YELLOW}Running tests...${NC}"
$PYTHON_CMD manage.py test

TESTS_EXIT_CODE=$?

# Check test results
if [ $TESTS_EXIT_CODE -ne 0 ]; then
    echo -e "${RED}Tests failed! Push aborted.${NC}"
    echo -e "${YELLOW}Please fix the failing tests before pushing.${NC}"
    restore_stash
    exit 1
fi

echo -e "${GREEN}All tests passed. Proceeding with push...${NC}"
restore_stash
exit 0
EOF

# Hook ausführbar machen
chmod +x $HOOKS_DIR/pre-push

echo "Git hooks erfolgreich installiert!"
echo "Der pre-push Hook wurde eingerichtet. Er führt die Tests vor dem Push aus, überschreibt aber nicht die Dance-App-Fixtures."
