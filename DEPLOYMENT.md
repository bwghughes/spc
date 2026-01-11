# Deployment Guide for spcchart

This guide covers building and deploying the spcchart package to PyPI using uv.

## Prerequisites

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **PyPI Account**: Create accounts on:
   - [TestPyPI](https://test.pypi.org/account/register/) (for testing)
   - [PyPI](https://pypi.org/account/register/) (for production)

3. **API Tokens**: Generate API tokens:
   - TestPyPI: https://test.pypi.org/manage/account/token/
   - PyPI: https://pypi.org/manage/account/token/

4. **Configure API Tokens**:

   Create or edit `~/.pypirc`:
   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-YourPyPITokenHere

   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-YourTestPyPITokenHere
   ```

   Or set environment variables:
   ```bash
   export UV_PUBLISH_USERNAME=__token__
   export UV_PUBLISH_PASSWORD=pypi-YourTokenHere
   ```

## Quick Start

### Build Only

To build distribution packages without deploying:

```bash
./scripts/build.sh
```

This will:
- Clean previous builds
- Run all tests
- Build wheel and source distribution
- Output packages to `dist/` directory

### Deploy to TestPyPI (Recommended First)

Test the deployment process on TestPyPI before going to production:

```bash
./scripts/deploy-test.sh
```

Or manually:
```bash
./scripts/deploy.sh testpypi
```

Then test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ spcchart
```

### Deploy to Production PyPI

After testing on TestPyPI, deploy to production:

```bash
./scripts/deploy.sh pypi
```

**WARNING**: This cannot be undone! You cannot re-upload the same version.

## Full Release Process

For a complete release with version bumping, tagging, and deployment:

```bash
./scripts/release.sh 0.24.1
```

This interactive script will:
1. Run all tests
2. Update version in `pyproject.toml` and `version` file
3. Prompt you to update `CHANGELOG.md`
4. Create git commit and tag
5. Build distribution packages
6. Ask which deployment target (TestPyPI, PyPI, or skip)
7. Deploy to selected target

### Release Script Options

```bash
# Full release
./scripts/release.sh 0.24.1

# Skip tests (if already run)
./scripts/release.sh 0.24.1 --skip-tests

# Skip git tagging
./scripts/release.sh 0.24.1 --skip-tag

# Both
./scripts/release.sh 0.24.1 --skip-tests --skip-tag
```

## Manual Deployment Steps

If you prefer manual control:

### 1. Update Version

Edit `pyproject.toml` and `version`:
```toml
version = "0.24.1"
```

### 2. Update CHANGELOG.md

Add release notes for the new version.

### 3. Commit Changes

```bash
git add pyproject.toml version CHANGELOG.md
git commit -m "Bump version to 0.24.1"
git tag -a v0.24.1 -m "Release version 0.24.1"
```

### 4. Run Tests

```bash
uv run pytest
```

### 5. Build Package

```bash
uv build
```

### 6. Upload to TestPyPI

```bash
uv publish --publish-url https://test.pypi.org/legacy/
```

### 7. Test Installation from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ spcchart==0.24.1
```

### 8. Upload to PyPI

```bash
uv publish
```

### 9. Push to GitHub

```bash
git push
git push --tags
```

### 10. Create GitHub Release

Go to https://github.com/bwghughes/spc/releases/new and create a new release.

## Troubleshooting

### Build Failures

If the build fails:

1. Check that all tests pass: `uv run pytest`
2. Verify pyproject.toml syntax
3. Check MANIFEST.in includes all necessary files
4. Clean and rebuild: `rm -rf dist/ build/ *.egg-info && ./scripts/build.sh`

### Upload Failures

**Version already exists**:
- PyPI doesn't allow re-uploading the same version
- Increment version and rebuild

**Authentication failed**:
- Check API token is correct
- Verify `~/.pypirc` or environment variables
- Regenerate token if needed

**Package size too large**:
- Check for accidentally included files
- Review MANIFEST.in exclusions

### Testing Installation

After deployment, test in a clean environment:

```bash
# Create fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # or test_env\Scripts\activate on Windows

# Install from PyPI
pip install spcchart

# Test import and basic functionality
python -c "from spcchart import SpcChart, PlotlySpcChart; print('Success!')"

# Test CLI
spcchart --help

# Deactivate and clean up
deactivate
rm -rf test_env
```

## Verification Checklist

Before deploying to production PyPI:

- [ ] All tests pass (`uv run pytest`)
- [ ] Version number updated in `pyproject.toml` and `version`
- [ ] CHANGELOG.md updated with release notes
- [ ] README.md reflects current features
- [ ] Git commit created and tagged
- [ ] Built successfully (`./scripts/build.sh`)
- [ ] Tested on TestPyPI
- [ ] Installation from TestPyPI works
- [ ] Example code runs correctly

## Post-Deployment

After successful deployment:

1. **Push to GitHub**:
   ```bash
   git push
   git push --tags
   ```

2. **Create GitHub Release**:
   - Go to https://github.com/bwghughes/spc/releases/new
   - Select the tag you just created
   - Copy changelog entries for this version
   - Attach distribution files from `dist/` (optional)
   - Publish release

3. **Verify on PyPI**:
   - Check package page: https://pypi.org/project/spcchart/
   - Verify description renders correctly
   - Check that all links work

4. **Announce** (optional):
   - Social media
   - Mailing lists
   - Project changelog/blog

## Links

- PyPI Package: https://pypi.org/project/spcchart/
- TestPyPI Package: https://test.pypi.org/project/spcchart/
- GitHub Repository: https://github.com/bwghughes/spc
- Documentation: https://statistical-process-control-charts.readthedocs.org/

## Support

For issues or questions:
- GitHub Issues: https://github.com/bwghughes/spc/issues
- PyPI Help: https://pypi.org/help/
