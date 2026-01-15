# API Reference

Complete API documentation for spcchart library.

## Table of Contents

1. [spcchart.plotly_chart](#spcchartplotly_chart)
2. [spcchart.spcchart](#spcchartspcchart)
3. [spcchart.spc](#spcchartspc)
4. [Flask Web App](#flask-web-app)

---

## spcchart.plotly_chart

Interactive Plotly-based SPC charts.

### PlotlySpcChart

Create interactive, web-ready SPC charts using Plotly.

```python
class PlotlySpcChart(data, title=None, chart_type=CHART_X_MR_X, sizes=None)
```

#### Parameters

- **data** (`list`): List of numerical values or list of lists for subgrouped data
- **title** (`str`, optional): Chart title. Default: "SPC Chart"
- **chart_type** (`str`, optional): Type of SPC chart. Default: `CHART_X_MR_X`
- **sizes** (`int`, optional): Subgroup size for charts requiring it

#### Attributes

- **data** (`list`): The input data
- **title** (`str`): Chart title
- **chart_type** (`str`): Chart type identifier
- **spc** (`Spc`): Underlying SPC calculation object
- **center** (`float`): Center line value
- **lcl** (`float`): Lower control limit
- **ucl** (`float`): Upper control limit
- **violations** (`dict`): Dictionary of rule violations

#### Methods

##### render_to_html()

```python
render_to_html(include_plotlyjs=True) -> str
```

Render the chart to HTML string.

**Parameters:**
- `include_plotlyjs` (bool|str): Include Plotly.js library. Options:
  - `True`: Include full library (default)
  - `False`: Don't include library
  - `'cdn'`: Use CDN link

**Returns:** HTML string containing the chart

**Example:**
```python
chart = PlotlySpcChart([1,2,3,4,5], title="Example")
html = chart.render_to_html(include_plotlyjs='cdn')
```

##### render_to_file()

```python
render_to_file(filename=None) -> str
```

Render the chart to an HTML file.

**Parameters:**
- `filename` (str, optional): Output filename. Auto-generated if not provided.

**Returns:** Path to the created file

**Example:**
```python
chart = PlotlySpcChart([1,2,3,4,5], title="Example")
filepath = chart.render_to_file("my_chart.html")
```

##### get_figure()

```python
get_figure() -> plotly.graph_objects.Figure
```

Get the Plotly figure object for further customization.

**Returns:** Plotly Figure object

**Example:**
```python
chart = PlotlySpcChart([1,2,3,4,5], title="Example")
fig = chart.get_figure()
fig.update_layout(template='plotly_dark')
fig.write_html("custom_chart.html")
```

#### Complete Example

```python
from spcchart.plotly_chart import PlotlySpcChart

# Create chart
data = [98.6, 98.7, 98.5, 98.8, 98.6, 98.7]
chart = PlotlySpcChart(data, title="Temperature Monitoring")

# Get statistics
print(f"Center: {chart.center:.2f}")
print(f"LCL: {chart.lcl:.2f}")
print(f"UCL: {chart.ucl:.2f}")

# Check violations
if chart.violations:
    for rule, points in chart.violations.items():
        print(f"Violation: {rule} at points {points}")

# Save chart
chart.render_to_file("temperature.html")
```

---

## spcchart.spcchart

Traditional static SVG charts using Pygal (backward compatibility).

### SpcChart

Create static SVG charts.

```python
class SpcChart(data, title=None, filename=None)
```

#### Parameters

- **data** (`list`): List of numerical values
- **title** (`str`, optional): Chart title
- **filename** (`str`, optional): Output filename

#### Methods

##### render_to_file()

```python
render_to_file() -> str
```

Render chart to SVG file.

**Returns:** Path to the created SVG file

**Example:**
```python
from spcchart import SpcChart

chart = SpcChart([1,2,3,4,5], title="Example")
filename = chart.render_to_file()
print(f"Chart saved to: {filename}")
```

---

## spcchart.spc

Core SPC statistical calculations and chart type definitions.

### Spc

Main SPC analysis class for calculating control limits and detecting violations.

```python
class Spc(data, chart_type, rules=RULES_BASIC, newdata=[], sizes=None)
```

#### Parameters

- **data** (`list`): Input data (flat list or list of lists for subgrouped data)
- **chart_type** (`str`): Type of control chart (see [Chart Types](#chart-types))
- **rules** (`list`, optional): List of rules to check. Default: `RULES_BASIC`
- **newdata** (`list`, optional): Additional new data points
- **sizes** (`int`, optional): Subgroup size

#### Attributes

- **orig_data** (`list`): Original input data
- **chart_type** (`str`): Chart type identifier
- **center** (`float`): Center line (mean)
- **lcl** (`float`): Lower control limit
- **ucl** (`float`): Upper control limit
- **violating_points** (`dict`): Dictionary of rule violations

#### Methods

##### get_stats()

```python
get_stats() -> tuple
```

Get control chart statistics.

**Returns:** Tuple of (center, lcl, ucl)

**Example:**
```python
from spcchart.spc import Spc, CHART_X_MR_X

data = [10, 11, 10, 12, 11, 10]
spc = Spc(data, CHART_X_MR_X)
center, lcl, ucl = spc.get_stats()
```

##### get_violating_points()

```python
get_violating_points(rules=[]) -> dict
```

Get points that violate control chart rules.

**Parameters:**
- `rules` (list, optional): Override default rules

**Returns:** Dictionary mapping rule names to lists of violating point indices

**Example:**
```python
from spcchart.spc import Spc, CHART_X_MR_X, RULES_NELSON

spc = Spc([1,2,3,4,5,100], CHART_X_MR_X, rules=RULES_NELSON)
violations = spc.get_violating_points()

for rule, points in violations.items():
    print(f"{rule}: {points}")
```

### Chart Types

Constants defining available chart types:

#### Individual/Variable Charts

- **CHART_X_MR_X**: X and Moving Range chart (for X values)
- **CHART_X_MR_MR**: X and Moving Range chart (for mR values)

**Usage:**
```python
from spcchart.spc import CHART_X_MR_X

data = [10.1, 10.2, 10.3, 10.1, 10.2]
spc = Spc(data, CHART_X_MR_X)
```

#### Subgrouped Charts

- **CHART_X_BAR_R_X**: X-bar and R chart (for means)
- **CHART_X_BAR_R_R**: X-bar and R chart (for ranges)
- **CHART_X_BAR_S_X**: X-bar and S chart (for means)
- **CHART_X_BAR_S_S**: X-bar and S chart (for standard deviations)

**Usage:**
```python
from spcchart.spc import CHART_X_BAR_R_X

# Subgrouped data (5 measurements per subgroup)
data = [
    [10, 11, 10, 12, 11],
    [10, 10, 11, 10, 11],
    [11, 10, 10, 11, 10]
]
spc = Spc(data, CHART_X_BAR_R_X)
```

#### Attribute Charts

- **CHART_P**: p-chart (proportion defective)
- **CHART_NP**: np-chart (number defective)
- **CHART_C**: c-chart (count of defects)
- **CHART_U**: u-chart (defects per unit)

**Usage:**
```python
from spcchart.spc import CHART_C

# Count of defects per inspection
data = [5, 3, 4, 6, 5, 4, 3, 7]
spc = Spc(data, CHART_C)
```

#### Special Charts

- **CHART_CUSUM**: Cumulative Sum chart
- **CHART_EWMA**: Exponentially Weighted Moving Average
- **CHART_THREE_WAY**: Three-way chart
- **CHART_TIME_SERIES**: Time series chart

### Control Chart Rules

Rule sets for detecting out-of-control conditions:

#### RULES_BASIC

Basic rules (most commonly used):
- 1 point beyond 3σ
- 7 consecutive points on one side of center

```python
from spcchart.spc import RULES_BASIC
```

#### RULES_WECO

Western Electric rules:
- 1 point beyond 3σ
- 2 of 3 points beyond 2σ
- 4 of 5 points beyond 1σ
- 8 consecutive points on one side
- 6 points trending
- 14 points alternating up/down

```python
from spcchart.spc import RULES_WECO
```

#### RULES_NELSON

Nelson rules (comprehensive):
- 1 point beyond 3σ
- 9 consecutive points on one side
- 6 points trending
- 14 points alternating up/down
- 2 of 3 points beyond 2σ
- 4 of 5 points beyond 1σ
- 15 consecutive points within 1σ
- 8 consecutive points beyond 1σ on both sides

```python
from spcchart.spc import RULES_NELSON
```

#### RULES_ALL

All available rules combined.

```python
from spcchart.spc import RULES_ALL
```

### Example: Custom Rules

```python
from spcchart.spc import Spc, CHART_X_MR_X, RULES_NELSON

data = [10, 11, 10, 12, 11, 10, 11, 10, 12, 11]

# Use Nelson rules
spc = Spc(data, CHART_X_MR_X, rules=RULES_NELSON)

# Get violations
violations = spc.get_violating_points()

if violations:
    print("Process is out of control!")
    for rule, points in violations.items():
        print(f"  {rule}: {points}")
else:
    print("Process is in statistical control")
```

---

## Flask Web App

REST API for chart generation.

### Endpoints

#### GET /

Main web interface.

**Response:** HTML page with chart generation form

**Example:**
```bash
curl http://localhost:5000/
```

#### POST /api/generate

Generate SPC chart via API.

**Request Body:**
```json
{
  "title": "Chart Title",
  "data": "1,2,3,4,5,6,7,8",
  "chart_type": "X mR - X"
}
```

**Parameters:**
- `title` (string): Chart title
- `data` (string): Comma-separated numbers
- `chart_type` (string): Chart type
  - `"X mR - X"`: X-mR chart
  - `"c"`: c-chart

**Response:**
```json
{
  "html": "<div>...</div>"
}
```

**Error Response:**
```json
{
  "error": "Error message"
}
```

**HTTP Status Codes:**
- `200`: Success
- `400`: Invalid data format
- `500`: Server error

**Example:**
```python
import requests

response = requests.post('http://localhost:5000/api/generate', json={
    'title': 'Temperature',
    'data': '98.6, 98.7, 98.5, 98.8, 98.6',
    'chart_type': 'X mR - X'
})

if response.status_code == 200:
    result = response.json()
    print(result['html'])
else:
    print(f"Error: {response.json()['error']}")
```

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

**Example:**
```bash
curl http://localhost:5000/health
```

### Running the Web App

```python
# In your code
from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Or from command line:
```bash
python app.py
```

Configuration options:
```python
app.config['DEBUG'] = True  # Enable debug mode
app.config['TESTING'] = True  # Enable testing mode
```

---

## Type Hints

For type checking with mypy or similar tools:

```python
from typing import List, Tuple, Dict, Optional, Union
from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import Spc

def create_chart(data: List[float], title: str) -> PlotlySpcChart:
    return PlotlySpcChart(data, title=title)

def get_statistics(data: List[float]) -> Tuple[float, float, float]:
    spc = Spc(data, "X mR - X")
    return spc.get_stats()

def check_violations(data: List[float]) -> Dict[str, List[int]]:
    spc = Spc(data, "X mR - X")
    return spc.get_violating_points()
```

---

## Error Handling

### Common Exceptions

#### AssertionError

Raised when data doesn't meet chart type requirements.

**Example:**
```python
from spcchart.spc import Spc, CHART_X_BAR_R_X

# This will raise AssertionError - needs subgrouped data
try:
    spc = Spc([1, 2, 3], CHART_X_BAR_R_X)
except AssertionError as e:
    print("Invalid data for chart type")
```

#### ValueError

Raised when data contains non-numeric values.

**Example:**
```python
try:
    data = [float(x) for x in ["1", "2", "abc"]]
except ValueError:
    print("Data must be numeric")
```

#### ZeroDivisionError

Raised when insufficient data for calculations.

**Example:**
```python
from spcchart.spc import Spc, CHART_X_MR_X

try:
    spc = Spc([42], CHART_X_MR_X)  # Needs at least 2 points
except ZeroDivisionError:
    print("Need more data points")
```

### Recommended Error Handling

```python
from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import CHART_X_MR_X

def safe_chart_creation(data, title):
    try:
        if len(data) < 2:
            raise ValueError("Need at least 2 data points")

        # Ensure all values are numeric
        data = [float(x) for x in data]

        chart = PlotlySpcChart(data, title=title, chart_type=CHART_X_MR_X)
        return chart

    except ValueError as e:
        print(f"Data error: {e}")
        return None
    except AssertionError as e:
        print(f"Chart type error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

---

## Performance Considerations

### Memory Usage

For large datasets (>10,000 points):

```python
# Good: Process in chunks
def process_large_dataset(data, chunk_size=1000):
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        chart = PlotlySpcChart(chunk, title=f"Chunk {i//chunk_size}")
        chart.render_to_file(f"chunk_{i}.html")
```

### Rendering Speed

For faster rendering:

```python
# Use CDN for Plotly.js (smaller file size)
chart.render_to_html(include_plotlyjs='cdn')

# Or exclude if you'll include it separately
chart.render_to_html(include_plotlyjs=False)
```

---

## Complete Example

Putting it all together:

```python
from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import CHART_X_MR_X, RULES_NELSON

def analyze_process_data(measurements, title="Process Data"):
    """
    Complete SPC analysis workflow.

    Args:
        measurements: List of numerical measurements
        title: Chart title

    Returns:
        Dictionary with analysis results
    """
    # Create chart with Nelson rules
    chart = PlotlySpcChart(
        measurements,
        title=title,
        chart_type=CHART_X_MR_X
    )

    # Apply stricter rules
    chart.spc.rules = RULES_NELSON
    violations = chart.spc.get_violating_points()

    # Get statistics
    center, lcl, ucl = chart.center, chart.lcl, chart.ucl

    # Save chart
    filename = chart.render_to_file(f"{title.replace(' ', '_')}.html")

    # Return results
    return {
        'center': center,
        'lcl': lcl,
        'ucl': ucl,
        'violations': violations,
        'in_control': len(violations) == 0,
        'chart_file': filename
    }

# Use it
if __name__ == '__main__':
    data = [98.6, 98.7, 98.5, 98.8, 98.6, 98.7, 98.6, 98.5,
            98.9, 98.7, 98.8, 98.6, 98.5, 98.7, 98.6]

    results = analyze_process_data(data, "Temperature Monitoring")

    print(f"Center: {results['center']:.2f}")
    print(f"Control limits: {results['lcl']:.2f} - {results['ucl']:.2f}")
    print(f"In control: {results['in_control']}")
    print(f"Chart saved: {results['chart_file']}")

    if results['violations']:
        print("\n⚠️ Violations detected:")
        for rule, points in results['violations'].items():
            print(f"  {rule}: {points}")
```

---

## See Also

- [User Guide](USER_GUIDE.md) - Complete user guide with examples
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment documentation
- [CHANGELOG.md](CHANGELOG.md) - Version history
