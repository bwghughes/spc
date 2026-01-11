#!/usr/bin/env bash
#
# Deploy to TestPyPI for testing before production release
#

set -e

# Colors
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Deploying to TestPyPI...${NC}"
echo

# Call main deploy script with testpypi argument
"$(dirname "$0")/deploy.sh" testpypi
