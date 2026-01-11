# Deployment Scripts

This directory contains scripts for building and deploying the spcchart package to PyPI using uv.

## Scripts Overview

### `build.sh`
Build distribution packages (wheel and source distribution).

**Usage:**
```bash
./scripts/build.sh
```

**What it does:**
- Cleans previous build artifacts
- Runs all tests
- Builds wheel (`.whl`) and source distribution (`.tar.gz`)
- Outputs packages to `dist/` directory

### `deploy.sh`
Deploy to PyPI or TestPyPI.

**Usage:**
```bash
# Deploy to TestPyPI
./scripts/deploy.sh testpypi

# Deploy to production PyPI
./scripts/deploy.sh pypi

# Default (PyPI)
./scripts/deploy.sh
```

**What it does:**
- Checks for distribution files (builds if needed)
- Confirms deployment (for production PyPI)
- Uploads packages using uv publish
- Shows package URL and installation instructions

### `deploy-test.sh`
Shortcut for deploying to TestPyPI.

**Usage:**
```bash
./scripts/deploy-test.sh
```

**Equivalent to:**
```bash
./scripts/deploy.sh testpypi
```

### `release.sh`
Complete release workflow with version management.

**Usage:**
```bash
# Standard release
./scripts/release.sh 0.24.1

# Skip tests (if already run)
./scripts/release.sh 0.24.1 --skip-tests

# Skip git tagging
./scripts/release.sh 0.24.1 --skip-tag
```

**What it does:**
1. Runs all tests (unless `--skip-tests`)
2. Updates version in `pyproject.toml` and `version` file
3. Prompts to update `CHANGELOG.md`
4. Creates git commit and tag (unless `--skip-tag`)
5. Builds distribution packages
6. Interactively asks where to deploy:
   - TestPyPI (recommended first)
   - Production PyPI
   - Skip deployment
7. Shows next steps

## Quick Workflows

### Testing a Release

Before deploying to production, always test on TestPyPI:

```bash
# Build and deploy to TestPyPI
./scripts/build.sh
./scripts/deploy-test.sh

# Test installation
pip install --index-url https://test.pypi.org/simple/ spcchart

# Run quick test
python -c "from spcchart import SpcChart; print('Works!')"
```

### Full Production Release

```bash
# One command for everything
./scripts/release.sh 0.25.0

# Or manually:
./scripts/build.sh
./scripts/deploy.sh pypi
git push && git push --tags
```

### Build Only (No Deployment)

```bash
./scripts/build.sh
```

The distribution files will be in `dist/`:
- `spcchart-X.Y.Z-py3-none-any.whl` - Wheel package
- `spcchart-X.Y.Z.tar.gz` - Source distribution

## Prerequisites

1. **uv installed:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **PyPI credentials configured:**

   Option A - Using `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = pypi-YourTokenHere

   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-YourTestTokenHere
   ```

   Option B - Environment variables:
   ```bash
   export UV_PUBLISH_USERNAME=__token__
   export UV_PUBLISH_PASSWORD=pypi-YourTokenHere
   ```

## Notes

- All scripts should be run from the project root or the scripts directory
- Scripts automatically navigate to project root
- Build artifacts are placed in `dist/` directory
- Scripts use colored output for better readability
- All scripts exit on error (`set -e`)

## Troubleshooting

**Permission denied:**
```bash
chmod +x scripts/*.sh
```

**uv not found:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or check PATH
which uv
```

**Tests failing:**
```bash
# Run tests manually to see errors
uv run pytest -v
```

**Version already exists on PyPI:**
- You cannot overwrite a published version
- Increment the version number and rebuild
- Use TestPyPI for testing before production

For detailed deployment instructions, see [DEPLOYMENT.md](../DEPLOYMENT.md).
