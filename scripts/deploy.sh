#!/usr/bin/env bash
#
# Deployment script for spcchart package to PyPI
# Uses uv for publishing
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

# Default to production PyPI
REPOSITORY="${1:-pypi}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Deploying spcchart to ${REPOSITORY}${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv is not installed${NC}"
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if dist/ exists
if [ ! -d "dist" ]; then
    echo -e "${YELLOW}No dist/ folder found. Building package first...${NC}"
    ./scripts/build.sh
fi

# Check for distribution files
if [ -z "$(ls -A dist 2>/dev/null)" ]; then
    echo -e "${RED}Error: No distribution files found in dist/${NC}"
    echo "Run ./scripts/build.sh first"
    exit 1
fi

# Show what will be uploaded
echo -e "${YELLOW}Distribution files to upload:${NC}"
ls -lh dist/
echo

# Confirm deployment
if [ "$REPOSITORY" = "pypi" ]; then
    echo -e "${YELLOW}⚠️  You are about to deploy to PRODUCTION PyPI!${NC}"
    echo -e "${YELLOW}This action cannot be undone.${NC}"
    echo
    read -p "Are you sure you want to continue? (yes/no): " -r
    echo
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo -e "${RED}Deployment cancelled${NC}"
        exit 1
    fi
fi

# Deploy using uv
echo -e "${YELLOW}Uploading to ${REPOSITORY}...${NC}"

if [ "$REPOSITORY" = "testpypi" ]; then
    # TestPyPI deployment
    uv publish --publish-url https://test.pypi.org/legacy/
else
    # Production PyPI deployment
    uv publish
fi

if [ $? -eq 0 ]; then
    echo
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Deployment successful!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo

    VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

    if [ "$REPOSITORY" = "testpypi" ]; then
        echo -e "${BLUE}Package uploaded to TestPyPI${NC}"
        echo -e "${BLUE}View at: https://test.pypi.org/project/spcchart/${VERSION}/${NC}"
        echo
        echo -e "${YELLOW}To install from TestPyPI:${NC}"
        echo "  pip install --index-url https://test.pypi.org/simple/ spcchart"
    else
        echo -e "${BLUE}Package uploaded to PyPI${NC}"
        echo -e "${BLUE}View at: https://pypi.org/project/spcchart/${VERSION}/${NC}"
        echo
        echo -e "${YELLOW}To install:${NC}"
        echo "  pip install spcchart"
    fi
else
    echo -e "${RED}✗ Deployment failed${NC}"
    exit 1
fi
