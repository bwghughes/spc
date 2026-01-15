# spcchart Examples

This directory contains practical examples demonstrating various use cases for spcchart.

## Running the Examples

All examples are standalone Python scripts. Run them with:

```bash
# Using uv (recommended)
uv run python examples/demo.py

# Or with standard Python
python examples/demo.py
```

## Available Examples

### 1. demo.py - Quick Start Demo

**Purpose:** Introduction to both SVG and interactive Plotly charts.

**What it demonstrates:**
- Creating static SVG charts (Pygal)
- Creating interactive HTML charts (Plotly)
- Getting statistics
- Detecting violations

**Run:**
```bash
uv run python examples/demo.py
```

**Output:**
- SVG chart file
- Interactive HTML chart file
- Statistics printed to console
- Violation detection

---

### 2. manufacturing_example.py - Quality Control

**Purpose:** Monitor manufacturing process quality for widget dimensions.

**What it demonstrates:**
- X-mR chart for individual measurements
- Using Nelson rules for sensitive detection
- Process capability analysis
- Specification limit checking
- Control limit interpretation

**Use case:** Manufacturing quality control for dimensional measurements

**Run:**
```bash
uv run python examples/manufacturing_example.py
```

**Key concepts:**
- Target values vs. specification limits
- Process capability
- When to stop production
- Root cause investigation

**Output:**
- Control chart analysis
- Capability metrics
- Recommendations
- Interactive chart: `widget_width_control.html`

---

### 3. service_monitoring.py - Service Level Monitoring

**Purpose:** Monitor customer service response times.

**What it demonstrates:**
- X-mR chart for service metrics
- SLA compliance tracking
- Performance rating system
- Trend analysis
- Process stability assessment

**Use case:** Service level monitoring, customer support metrics, response time tracking

**Run:**
```bash
uv run python examples/service_monitoring.py
```

**Key concepts:**
- Average response time
- SLA compliance rate
- Performance benchmarking
- Process stability

**Output:**
- Response time statistics
- SLA compliance metrics
- Performance rating
- Interactive chart: `service_response_times.html`

---

### 4. defect_tracking.py - Defect Monitoring

**Purpose:** Track production defects using count data.

**What it demonstrates:**
- c-chart for count data
- Defect rate calculation (PPM)
- Six Sigma level assessment
- Trend analysis
- Quality metrics

**Use case:** Production defect tracking, quality improvement, Six Sigma projects

**Run:**
```bash
uv run python examples/defect_tracking.py
```

**Key concepts:**
- Count data vs. measurement data
- Parts Per Million (PPM)
- Six Sigma quality levels
- Process improvement tracking

**Output:**
- Defect statistics
- Quality metrics
- Six Sigma level
- Trend analysis
- Interactive chart: `defect_tracking.html`

---

## Example Data

### Manufacturing Data (manufacturing_example.py)
```python
widget_widths = [
    10.2, 10.3, 10.1, 10.4, 10.2, 10.3, 10.2, 10.5,
    10.1, 10.3, 10.4, 10.2, 10.3, 10.1, 10.2, 10.3,
    # ... 24 measurements in mm
]
```

### Service Data (service_monitoring.py)
```python
response_times = [
    5.2, 4.8, 5.1, 5.3, 4.9, 5.0, 5.2, 4.7,
    # ... 30 response times in minutes
]
```

### Defect Data (defect_tracking.py)
```python
daily_defects = [
    5, 3, 4, 6, 5, 4, 3, 7, 2, 5,
    # ... 30 daily defect counts
]
```

## Creating Your Own Examples

### Template Structure

```python
#!/usr/bin/env python3
"""
Your Example Title

Brief description of what this example demonstrates.
"""

from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import CHART_X_MR_X

# Your data
data = [1, 2, 3, 4, 5]

print("=" * 60)
print("Your Analysis Title")
print("=" * 60)
print()

# Create chart
chart = PlotlySpcChart(data, title="Your Chart Title")

# Get statistics
center = chart.center
lcl = chart.lcl
ucl = chart.ucl

# Display results
print(f"Center Line: {center:.2f}")
print(f"LCL: {lcl:.2f}")
print(f"UCL: {ucl:.2f}")

# Check violations
violations = chart.violations
if violations:
    print("\n⚠️ Process out of control")
    for rule, points in violations.items():
        print(f"  {rule}: {points}")
else:
    print("\n✓ Process in control")

# Save chart
filename = chart.render_to_file()
print(f"\nChart saved to: {filename}")
```

## Common Patterns

### Pattern 1: Basic Analysis

```python
from spcchart.plotly_chart import PlotlySpcChart

data = [your_data_here]
chart = PlotlySpcChart(data, title="Analysis")

# Quick check
if chart.violations:
    print("Action needed!")
else:
    print("All good!")
```

### Pattern 2: Detailed Analysis

```python
from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import RULES_NELSON

data = [your_data_here]
chart = PlotlySpcChart(data, title="Detailed Analysis")

# Use stricter rules
chart.spc.rules = RULES_NELSON

# Get detailed stats
center, lcl, ucl = chart.center, chart.lcl, chart.ucl

# Check each rule
violations = chart.spc.get_violating_points()
for rule, points in violations.items():
    print(f"{rule}: {points}")
```

### Pattern 3: Comparison Analysis

```python
from spcchart.plotly_chart import PlotlySpcChart

before_data = [old_measurements]
after_data = [new_measurements]

before_chart = PlotlySpcChart(before_data, title="Before")
after_chart = PlotlySpcChart(after_data, title="After")

# Compare
improvement = before_chart.center - after_chart.center
print(f"Improvement: {improvement:.2f}")
```

## Tips for Using Examples

1. **Modify the data:** Replace example data with your own
2. **Adjust thresholds:** Change specification limits to match your requirements
3. **Customize charts:** Use `get_figure()` to customize Plotly charts
4. **Add logging:** Track results over time
5. **Integrate with systems:** Use examples as templates for automation

## Understanding the Output

### Console Output

Each example prints:
- **Statistics**: Center line, control limits
- **Analysis**: Interpretation of results
- **Recommendations**: Action items
- **File location**: Where charts are saved

### Chart Files

Generated HTML files contain:
- Interactive Plotly charts
- Zoom and pan capabilities
- Hover tooltips with exact values
- Export options (PNG, SVG)

### Reading the Charts

- **Blue line**: Your data points
- **Green line**: Center line (average)
- **Red dashed lines**: Control limits
- **Orange X marks**: Violations (out of control points)

## Troubleshooting Examples

### "No module named 'spcchart'"

**Solution:** Install the package first:
```bash
uv pip install -e .
```

### "Permission denied"

**Solution:** Make scripts executable:
```bash
chmod +x examples/*.py
```

### "Not enough data points"

**Solution:** Most charts need at least 2 data points. Add more data to your list.

### Charts look wrong

**Solution:** Ensure you're using the right chart type:
- **X-mR**: Individual measurements
- **c-chart**: Count data
- **Xbar-R**: Subgrouped data

## Next Steps

After exploring these examples:

1. Read the [User Guide](../USER_GUIDE.md) for detailed explanations
2. Check the [API Reference](../API_REFERENCE.md) for all options
3. Try the [Web Application](../app.py) for interactive chart generation
4. Create your own examples based on these templates

## Contributing Examples

Have a great example? Consider contributing:

1. Fork the repository
2. Add your example to this directory
3. Update this README
4. Submit a pull request

Make sure your example:
- Is well-commented
- Demonstrates a clear use case
- Includes sample output
- Follows the existing style

---

For questions or issues, visit: https://github.com/bwghughes/spc/issues
