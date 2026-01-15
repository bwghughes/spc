# User Guide for spcchart

Complete guide to using spcchart for Statistical Process Control.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Chart Types](#chart-types)
5. [Using the Library](#using-the-library)
6. [Web Application](#web-application)
7. [Advanced Usage](#advanced-usage)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

## Introduction

spcchart is a Python library for creating Statistical Process Control (SPC) charts, also known as control charts. These charts help you monitor process behavior over time and identify when a process is out of statistical control.

### What are Control Charts?

Control charts display process data over time with:
- **Center Line (CL)**: The average or target value
- **Upper Control Limit (UCL)**: Three standard deviations above the center
- **Lower Control Limit (LCL)**: Three standard deviations below the center

Points outside these limits or following certain patterns indicate the process may be out of control.

## Installation

### Using pip (from PyPI)

```bash
pip install spcchart
```

### Using uv (recommended for development)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install spcchart
uv pip install spcchart

# Or install with dev dependencies
uv pip install -e ".[dev]"
```

### From source

```bash
git clone https://github.com/bwghughes/spc.git
cd spc
uv pip install -e .
```

## Quick Start

### Command Line

```bash
# Generate a simple chart
spcchart --data=98.6,98.7,98.5,98.8,98.6,98.7,98.6,98.5 --title="Temperature"
```

### Python - Static SVG Chart

```python
from spcchart import SpcChart

data = [98.6, 98.7, 98.5, 98.8, 98.6, 98.7, 98.6, 98.5]
chart = SpcChart(data, title="Temperature Monitoring")
chart.render_to_file()  # Creates an SVG file
```

### Python - Interactive Plotly Chart

```python
from spcchart.plotly_chart import PlotlySpcChart

data = [98.6, 98.7, 98.5, 98.8, 98.6, 98.7, 98.6, 98.5]
chart = PlotlySpcChart(data, title="Temperature Monitoring")
chart.render_to_file()  # Creates an interactive HTML file
```

### Web Application

```bash
python app.py
# Open http://localhost:5000 in your browser
```

## Chart Types

### X-mR Chart (Individual and Moving Range)

Best for: **Individual measurements** where you have one data point at a time.

**Use cases:**
- Temperature readings
- Process times
- Measurement data
- Any continuous data without subgroups

**Example:**
```python
from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import CHART_X_MR_X

data = [10.2, 10.5, 10.1, 10.4, 10.3, 10.6, 10.2, 10.3]
chart = PlotlySpcChart(data, title="Widget Width (mm)", chart_type=CHART_X_MR_X)
chart.render_to_file("widget_width.html")
```

**Requirements:**
- At least 2 data points
- Individual measurements (not grouped)

### c-Chart (Count of Defects)

Best for: **Count data** where you're counting defects or events.

**Use cases:**
- Number of defects per unit
- Number of errors per report
- Number of customer complaints
- Any count data with constant sample size

**Example:**
```python
from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import CHART_C

# Number of defects found in 10 inspections
data = [5, 3, 4, 6, 5, 4, 3, 7, 2, 5]
chart = PlotlySpcChart(data, title="Defects Per Unit", chart_type=CHART_C)
chart.render_to_file("defects.html")
```

**Requirements:**
- Count data (integers)
- At least 2 data points

### Other Chart Types (Advanced)

For advanced users, additional chart types are available through the `spcchart.spc` module:

- **Xbar-R**: X-bar and Range charts for subgrouped data
- **Xbar-S**: X-bar and Standard Deviation charts
- **p-chart**: Proportion defective
- **np-chart**: Number defective
- **u-chart**: Defects per unit (variable sample size)

See the [API Reference](API_REFERENCE.md) for details.

## Using the Library

### Basic Workflow

1. **Collect your data** as a list of numbers
2. **Choose the appropriate chart type** based on your data
3. **Create the chart** using `PlotlySpcChart` or `SpcChart`
4. **Analyze the results** - check statistics and violations

### Example: Complete Workflow

```python
from spcchart.plotly_chart import PlotlySpcChart

# Step 1: Your data
temperature_readings = [
    98.6, 98.7, 98.5, 98.8, 98.6, 98.7, 98.6, 98.5,
    98.9, 98.7, 98.8, 98.6, 98.5, 98.7, 98.6
]

# Step 2: Create chart
chart = PlotlySpcChart(
    data=temperature_readings,
    title="Body Temperature Monitoring"
)

# Step 3: Get statistics
center, lcl, ucl = chart.center, chart.lcl, chart.ucl
print(f"Center Line: {center:.2f}°F")
print(f"LCL: {lcl:.2f}°F")
print(f"UCL: {ucl:.2f}°F")

# Step 4: Check for violations
violations = chart.violations
if violations:
    print(f"\n⚠️ Violations detected:")
    for rule, points in violations.items():
        print(f"  {rule}: Points {points}")
else:
    print("\n✓ Process is in control")

# Step 5: Save the chart
filename = chart.render_to_file("temperature_chart.html")
print(f"\nChart saved to: {filename}")
```

### Getting Chart Statistics

```python
from spcchart.plotly_chart import PlotlySpcChart

data = [10, 11, 10, 12, 11, 10, 11, 10]
chart = PlotlySpcChart(data, title="Example")

# Get control limits
center = chart.center      # Center line (mean)
lcl = chart.lcl           # Lower control limit
ucl = chart.ucl           # Upper control limit

print(f"Center: {center:.4f}")
print(f"LCL: {lcl:.4f}")
print(f"UCL: {ucl:.4f}")

# Get violations
violations = chart.violations
for rule, point_indices in violations.items():
    print(f"Rule '{rule}' violated at points: {point_indices}")
```

### Customizing Charts

```python
from spcchart.plotly_chart import PlotlySpcChart

data = [1, 2, 3, 4, 5, 6, 7, 8]
chart = PlotlySpcChart(data, title="Custom Chart")

# Get the Plotly figure for customization
fig = chart.get_figure()

# Customize the figure
fig.update_layout(
    title_font_size=24,
    height=800,
    template='plotly_dark'
)

# Save with customizations
fig.write_html("custom_chart.html")
```

## Web Application

### Starting the Server

```bash
python app.py
```

The web application will start at http://localhost:5000

### Using the Web Interface

1. **Enter your data**: Comma-separated numbers in the text area
   ```
   98.6, 98.7, 98.5, 98.8, 98.6, 98.7
   ```

2. **Choose chart type**: Select from dropdown
   - X-mR Chart: For individual measurements
   - c-Chart: For count data

3. **Set a title**: Descriptive name for your chart

4. **Click "Generate Chart"**: View your interactive chart

### API Endpoint

The web app provides a JSON API:

```python
import requests

# Send data to the API
response = requests.post('http://localhost:5000/api/generate', json={
    'title': 'Temperature',
    'data': '98.6, 98.7, 98.5, 98.8',
    'chart_type': 'X mR - X'
})

result = response.json()
html_chart = result['html']
```

### Health Check

```bash
curl http://localhost:5000/health
# {"status": "ok"}
```

## Advanced Usage

### Working with SPC Objects Directly

```python
from spcchart.spc import Spc, CHART_X_MR_X, RULES_NELSON

data = [10, 11, 10, 12, 11, 10, 11, 10]

# Create SPC object with specific rules
spc = Spc(data, CHART_X_MR_X, rules=RULES_NELSON)

# Get statistics
center, lcl, ucl = spc.get_stats()

# Get violations using Nelson rules
violations = spc.get_violating_points()

print(f"Statistics: Center={center}, LCL={lcl}, UCL={ucl}")
print(f"Violations: {violations}")
```

### Control Chart Rules

Different rule sets for detecting out-of-control conditions:

```python
from spcchart.spc import (
    RULES_BASIC,   # Basic rules (beyond 3σ, 7 on one side)
    RULES_WECO,    # Western Electric rules
    RULES_NELSON,  # Nelson rules
    RULES_ALL      # All available rules
)

from spcchart.plotly_chart import PlotlySpcChart

# Use specific rules
chart = PlotlySpcChart(data, title="With Nelson Rules")
chart.spc.rules = RULES_NELSON
violations = chart.spc.get_violating_points()
```

### Batch Processing

```python
from spcchart.plotly_chart import PlotlySpcChart
import pandas as pd

# Read data from CSV
df = pd.read_csv('measurements.csv')

# Process each column
for column in df.columns:
    data = df[column].dropna().tolist()

    chart = PlotlySpcChart(data, title=f"Control Chart: {column}")
    chart.render_to_file(f"chart_{column}.html")

    # Log statistics
    print(f"{column}: Center={chart.center:.2f}, "
          f"LCL={chart.lcl:.2f}, UCL={chart.ucl:.2f}")
```

## Examples

### Example 1: Manufacturing Quality Control

Monitor widget dimensions:

```python
from spcchart.plotly_chart import PlotlySpcChart

# Widget width measurements (mm)
widths = [
    10.2, 10.3, 10.1, 10.4, 10.2, 10.3, 10.2, 10.5,
    10.1, 10.3, 10.4, 10.2, 10.3, 10.1, 10.2, 10.3
]

chart = PlotlySpcChart(widths, title="Widget Width Control Chart")
chart.render_to_file("widget_quality.html")

# Check if process is in control
if chart.violations:
    print("⚠️ Process out of control - investigate!")
else:
    print("✓ Process is stable")
```

### Example 2: Service Time Monitoring

Track customer service response times:

```python
from spcchart.plotly_chart import PlotlySpcChart

# Response times in minutes
response_times = [
    5.2, 4.8, 5.1, 5.3, 4.9, 5.0, 5.2, 4.7,
    5.1, 5.0, 4.9, 5.2, 5.3, 5.1, 5.0
]

chart = PlotlySpcChart(
    response_times,
    title="Customer Service Response Time"
)

center, lcl, ucl = chart.center, chart.lcl, chart.ucl
print(f"Target time: {center:.1f} minutes")
print(f"Warning if below: {lcl:.1f} or above: {ucl:.1f}")

chart.render_to_file("service_times.html")
```

### Example 3: Defect Tracking

Monitor defects in production:

```python
from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import CHART_C

# Defects found per day
daily_defects = [5, 3, 4, 6, 5, 4, 3, 7, 2, 5, 4, 6]

chart = PlotlySpcChart(
    daily_defects,
    title="Daily Defect Count",
    chart_type=CHART_C
)

# Analyze trend
if len(chart.violations) > 0:
    print("Action needed: Defect rate is unstable")
else:
    print(f"Stable defect rate: ~{chart.center:.1f} per day")

chart.render_to_file("defects.html")
```

### Example 4: Comparing Static and Interactive Charts

```python
from spcchart import SpcChart
from spcchart.plotly_chart import PlotlySpcChart

data = [10, 11, 10, 12, 11, 10, 11, 10, 12, 11]

# Create static SVG chart
svg_chart = SpcChart(data, title="Static Chart")
svg_file = svg_chart.render_to_file()
print(f"SVG chart: {svg_file}")

# Create interactive HTML chart
plotly_chart = PlotlySpcChart(data, title="Interactive Chart")
html_file = plotly_chart.render_to_file()
print(f"Interactive chart: {html_file}")

# Both charts show the same statistics
print(f"\nStatistics are identical:")
print(f"Center: {plotly_chart.center:.4f}")
```

## Troubleshooting

### Common Issues

#### "At least 2 data points are required"

**Problem**: Not enough data for statistical analysis.

**Solution**: Provide at least 2 data points.

```python
# Wrong
data = [42]

# Correct
data = [42, 43]
```

#### "Invalid data format"

**Problem**: Data contains non-numeric values.

**Solution**: Ensure all values are numbers.

```python
# Wrong
data = [1, 2, "three", 4]

# Correct
data = [1, 2, 3, 4]
```

#### Charts look wrong or have no violations

**Problem**: May be using the wrong chart type for your data.

**Solution**: Review [Chart Types](#chart-types) section and choose the appropriate chart.

#### Web app returns 500 error

**Problem**: Using unsupported chart type or invalid data.

**Solution**:
- Use only X-mR or c-chart in the web app
- Ensure data is comma-separated numbers
- Check browser console for detailed errors

### Getting Help

1. **Check the documentation**: [API Reference](API_REFERENCE.md)
2. **Run examples**: Try the examples in `examples/` directory
3. **Enable debug mode**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```
4. **Report issues**: https://github.com/bwghughes/spc/issues

## Best Practices

1. **Collect enough data**: At least 20-25 points for reliable control limits
2. **Use the right chart**: Match chart type to your data type
3. **Investigate violations**: Don't ignore out-of-control signals
4. **Regular monitoring**: Update charts regularly with new data
5. **Document changes**: Note when process changes are made

## Further Reading

- [API Reference](API_REFERENCE.md) - Complete API documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - How to deploy to PyPI
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [Statistical Process Control on Wikipedia](https://en.wikipedia.org/wiki/Statistical_process_control)
