#!/usr/bin/env python3
"""
Demo script showing the new features of spcchart v0.24

This demonstrates:
1. No numpy dependency (using Python stdlib)
2. Interactive Plotly charts
3. Traditional Pygal charts (still supported)
"""

from spcchart import SpcChart, PlotlySpcChart

# Sample data - widget quality measurements
data = [
    98.6, 98.7, 98.5, 98.8, 98.6, 98.7, 98.6, 98.5,
    98.9, 98.7, 98.8, 98.6, 98.5, 98.7, 98.6, 101.2  # Last point is out of spec
]

print("=" * 60)
print("SPC Chart Demo - Version 0.24")
print("=" * 60)
print()

# Traditional SVG chart (Pygal)
print("1. Creating traditional SVG chart...")
svg_chart = SpcChart(data, title="Temperature Monitoring (SVG)")
svg_file = svg_chart.render_to_file()
print(f"   ✓ Created: {svg_file}")
print()

# New Interactive Plotly chart
print("2. Creating interactive HTML chart...")
plotly_chart = PlotlySpcChart(data, title="Temperature Monitoring (Interactive)")
html_file = plotly_chart.render_to_file()
print(f"   ✓ Created: {html_file}")
print()

# Display statistics
print("3. Chart Statistics:")
center, lcl, ucl = plotly_chart.center, plotly_chart.lcl, plotly_chart.ucl
print(f"   Center Line: {center:.4f}")
print(f"   Lower Control Limit (LCL): {lcl:.4f}")
print(f"   Upper Control Limit (UCL): {ucl:.4f}")
print()

# Display violations
violations = plotly_chart.violations
if violations:
    print("4. ⚠️  Violations Detected:")
    for rule, points in violations.items():
        print(f"   Rule: {rule}")
        print(f"   Points: {points}")
else:
    print("4. ✓ No violations detected")

print()
print("=" * 60)
print("Demo complete! Open the HTML file in your browser to see")
print("the interactive chart with zoom, pan, and export features.")
print("=" * 60)
