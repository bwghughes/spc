#!/usr/bin/env python3
"""
Manufacturing Quality Control Example

This example demonstrates using spcchart for monitoring
manufacturing process quality.
"""

from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import CHART_X_MR_X, RULES_NELSON

# Widget dimension measurements (in mm)
widget_widths = [
    10.2, 10.3, 10.1, 10.4, 10.2, 10.3, 10.2, 10.5,
    10.1, 10.3, 10.4, 10.2, 10.3, 10.1, 10.2, 10.3,
    10.4, 10.2, 10.3, 10.1, 10.5, 10.2, 10.3, 10.4
]

print("=" * 60)
print("Manufacturing Quality Control Analysis")
print("=" * 60)
print()

# Create control chart with strict rules
chart = PlotlySpcChart(
    widget_widths,
    title="Widget Width Control Chart",
    chart_type=CHART_X_MR_X
)

# Use Nelson rules for more sensitive detection
chart.spc.rules = RULES_NELSON
violations = chart.spc.get_violating_points()

# Display statistics
center = chart.center
lcl = chart.lcl
ucl = chart.ucl

print("Control Chart Statistics:")
print(f"  Target (Center Line): {center:.3f} mm")
print(f"  Lower Control Limit:  {lcl:.3f} mm")
print(f"  Upper Control Limit:  {ucl:.3f} mm")
print(f"  Control Range:        {ucl - lcl:.3f} mm")
print()

# Calculate process capability metrics
specification_target = 10.25
specification_tolerance = 0.30  # ±0.15 mm

lsl = specification_target - specification_tolerance  # Lower Spec Limit
usl = specification_target + specification_tolerance  # Upper Spec Limit

print("Specification Limits:")
print(f"  Target:               {specification_target:.3f} mm")
print(f"  Lower Spec Limit:     {lsl:.3f} mm")
print(f"  Upper Spec Limit:     {usl:.3f} mm")
print()

# Check if process is within specifications
if lcl >= lsl and ucl <= usl:
    print("✓ Process is capable (control limits within spec limits)")
else:
    print("⚠️ Process may not be capable")
    if lcl < lsl:
        print(f"  LCL is {lsl - lcl:.3f} mm below lower spec")
    if ucl > usl:
        print(f"  UCL is {ucl - usl:.3f} mm above upper spec")
print()

# Check for violations
if violations:
    print("⚠️ PROCESS OUT OF CONTROL")
    print("Violations detected:")
    for rule, points in violations.items():
        print(f"  • {rule}:")
        print(f"    Points: {points}")
        print(f"    Values: {[f'{widget_widths[i]:.3f}' for i in points]}")
    print()
    print("Recommended Actions:")
    print("  1. Stop production and investigate")
    print("  2. Check equipment calibration")
    print("  3. Review operator procedures")
    print("  4. Inspect raw materials")
else:
    print("✓ PROCESS IS IN STATISTICAL CONTROL")
    print()
    print("Process is stable and predictable.")
    print("Continue monitoring with regular measurements.")

print()

# Save the chart
filename = chart.render_to_file("widget_width_control.html")
print(f"Interactive chart saved to: {filename}")
print()

# Calculate process statistics
import statistics
mean = statistics.mean(widget_widths)
stdev = statistics.stdev(widget_widths)

print("Process Statistics:")
print(f"  Mean:                 {mean:.3f} mm")
print(f"  Standard Deviation:   {stdev:.3f} mm")
print(f"  Min Value:            {min(widget_widths):.3f} mm")
print(f"  Max Value:            {max(widget_widths):.3f} mm")
print(f"  Range:                {max(widget_widths) - min(widget_widths):.3f} mm")

print()
print("=" * 60)
