# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.24] - 2025-01-11

### Added
- **Interactive Plotly Charts**: New `PlotlySpcChart` class for modern, interactive web charts
  - Zoom, pan, and interactive exploration
  - Hover tooltips showing exact values
  - Range slider for data navigation
  - Export to PNG directly from browser
  - Automatic violation highlighting with color coding
- **Flask Web Application**: Browser-based interface (`app.py`)
  - Beautiful, responsive UI with gradient design
  - Web form for data input
  - Chart type selection (X-mR, X-bar R, p, c)
  - Real-time statistics display (center, LCL, UCL)
  - Violation detection with visual indicators
  - JSON API endpoint at `/api/generate`
  - Health check endpoint at `/health`
- **Modern Testing**: Comprehensive pytest test suite
  - 41 tests total (14 new tests for PlotlySpcChart)
  - All tests passing
  - Coverage for chart creation, rendering, statistics, violations, and edge cases
- **Package Management**: Migration to `uv` for fast, reliable dependency management
  - `pyproject.toml` with PEP 621 metadata
  - `uv.lock` for reproducible builds
- **Example Scripts**: Demo script in `examples/demo.py`

### Changed
- **Removed numpy dependency**: Replaced with Python stdlib (`math`, `statistics`)
  - All SPC calculations now use pure Python
  - Added helper functions for 2D array operations
  - Significantly reduced installation size and complexity
- **Modernized Python**: Full migration from Python 2 to Python 3
  - Updated all print statements to functions
  - Replaced `xrange` with `range`
  - Fixed relative imports
- **Updated Dependencies**:
  - Added: `plotly>=5.0.0`, `flask>=2.0.0`
  - Updated: `pygal>=3.0.0`, `shortuuid>=1.0.0`
  - Removed: `numpy`, `wsgiref`
- **Version bump**: 0.23 → 0.24

### Maintained
- Full backward compatibility with existing `SpcChart` (Pygal) implementation
- All original functionality preserved
- Existing code continues to work unchanged

## [0.23] - Previous Release

### Added
- pytest testing infrastructure
- Modern package structure

### Changed
- Updated to Python 3 syntax
- Modernized dependency management

## [0.22 and earlier]

See git history for older changes.
