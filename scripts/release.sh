#!/usr/bin/env bash
#
# Full release script for spcchart
# Handles version bumping, changelog, git tagging, building, and deployment
#

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navigate to project root
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

# Check if version argument is provided
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: Version number required${NC}"
    echo "Usage: $0 <version> [--skip-tests] [--skip-tag]"
    echo "Example: $0 0.24.1"
    exit 1
fi

NEW_VERSION="$1"
SKIP_TESTS=false
SKIP_TAG=false

# Parse optional arguments
shift
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --skip-tag)
            SKIP_TAG=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Release Process for spcchart v${NEW_VERSION}${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Get current version
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo -e "${YELLOW}Current version: ${CURRENT_VERSION}${NC}"
echo -e "${YELLOW}New version: ${NEW_VERSION}${NC}"
echo

# Confirm release
read -p "Continue with release? (yes/no): " -r
echo
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo -e "${RED}Release cancelled${NC}"
    exit 1
fi

# Step 1: Run tests (unless skipped)
if [ "$SKIP_TESTS" = false ]; then
    echo -e "${YELLOW}Step 1: Running tests...${NC}"
    if uv run pytest -q; then
        echo -e "${GREEN}✓ All tests passed${NC}"
    else
        echo -e "${RED}✗ Tests failed - aborting release${NC}"
        exit 1
    fi
    echo
else
    echo -e "${YELLOW}Step 1: Skipping tests${NC}"
    echo
fi

# Step 2: Update version files
echo -e "${YELLOW}Step 2: Updating version files...${NC}"

# Update pyproject.toml
sed -i "s/^version = .*/version = \"${NEW_VERSION}\"/" pyproject.toml
echo -e "${GREEN}✓ Updated pyproject.toml${NC}"

# Update version file
echo "${NEW_VERSION}" > version
echo -e "${GREEN}✓ Updated version file${NC}"
echo

# Step 3: Update CHANGELOG
echo -e "${YELLOW}Step 3: Updating CHANGELOG.md...${NC}"
DATE=$(date +%Y-%m-%d)

# Check if version already exists in CHANGELOG
if grep -q "\[${NEW_VERSION}\]" CHANGELOG.md; then
    echo -e "${GREEN}✓ Version ${NEW_VERSION} already in CHANGELOG${NC}"
else
    echo -e "${YELLOW}Please update CHANGELOG.md with changes for version ${NEW_VERSION}${NC}"
    echo -e "${YELLOW}Press Enter when ready to continue...${NC}"
    read
fi
echo

# Step 4: Git commit and tag (unless skipped)
if [ "$SKIP_TAG" = false ]; then
    echo -e "${YELLOW}Step 4: Creating git commit and tag...${NC}"

    # Check for uncommitted changes
    if [[ -n $(git status -s) ]]; then
        git add pyproject.toml version CHANGELOG.md
        git commit -m "Bump version to ${NEW_VERSION}"
        echo -e "${GREEN}✓ Created commit${NC}"
    fi

    # Create git tag
    git tag -a "v${NEW_VERSION}" -m "Release version ${NEW_VERSION}"
    echo -e "${GREEN}✓ Created tag v${NEW_VERSION}${NC}"
    echo
else
    echo -e "${YELLOW}Step 4: Skipping git tag${NC}"
    echo
fi

# Step 5: Build package
echo -e "${YELLOW}Step 5: Building package...${NC}"
./scripts/build.sh
echo

# Step 6: Deploy to PyPI
echo -e "${YELLOW}Step 6: Deploy to PyPI${NC}"
echo -e "${BLUE}Choose deployment target:${NC}"
echo "  1) TestPyPI (recommended for testing)"
echo "  2) Production PyPI"
echo "  3) Skip deployment"
echo
read -p "Enter choice (1/2/3): " -r DEPLOY_CHOICE
echo

case $DEPLOY_CHOICE in
    1)
        ./scripts/deploy.sh testpypi
        ;;
    2)
        ./scripts/deploy.sh pypi
        ;;
    3)
        echo -e "${YELLOW}Skipping deployment${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

# Step 7: Summary
echo
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Release ${NEW_VERSION} complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo

if [ "$SKIP_TAG" = false ]; then
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Push commits: git push"
    echo "  2. Push tags: git push --tags"
    echo "  3. Create GitHub release at: https://github.com/bwghughes/spc/releases/new"
fi
