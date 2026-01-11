#!/usr/bin/env bash
#
# Build script for spcchart package
# Uses uv for building the distribution packages
#

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Building spcchart package${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Navigate to project root
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv is not installed${NC}"
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -rf dist/ build/ *.egg-info
echo -e "${GREEN}✓ Cleaned${NC}"
echo

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
if uv run pytest -q; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${RED}✗ Tests failed${NC}"
    exit 1
fi
echo

# Build the package
echo -e "${YELLOW}Building distribution packages...${NC}"
uv build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Build successful${NC}"
    echo
    echo -e "${BLUE}Distribution packages created:${NC}"
    ls -lh dist/
    echo
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Build completed successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi
