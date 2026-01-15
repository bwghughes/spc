#!/usr/bin/env python3
"""
Service Level Monitoring Example

Monitor customer service response times using SPC charts.
"""

from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import CHART_X_MR_X
import statistics

# Customer service response times (in minutes)
response_times = [
    5.2, 4.8, 5.1, 5.3, 4.9, 5.0, 5.2, 4.7,
    5.1, 5.0, 4.9, 5.2, 5.3, 5.1, 5.0, 4.8,
    5.2, 5.1, 4.9, 5.3, 5.0, 5.1, 4.8, 5.2,
    5.4, 5.0, 5.1, 4.9, 5.2, 5.0
]

print("=" * 70)
print("Customer Service Response Time Analysis")
print("=" * 70)
print()

# Create control chart
chart = PlotlySpcChart(
    response_times,
    title="Customer Service Response Time Control Chart",
    chart_type=CHART_X_MR_X
)

# Get statistics
center = chart.center
lcl = chart.lcl
ucl = chart.ucl
violations = chart.violations

print("Response Time Statistics:")
print(f"  Average Response Time: {center:.2f} minutes")
print(f"  Lower Control Limit:   {lcl:.2f} minutes")
print(f"  Upper Control Limit:   {ucl:.2f} minutes")
print()

# Service Level Agreement (SLA) target
sla_target = 6.0  # 6 minutes maximum
print(f"Service Level Agreement (SLA):")
print(f"  Target: Respond within {sla_target} minutes")
print()

# Check SLA compliance
over_sla = [t for t in response_times if t > sla_target]
compliance_rate = (len(response_times) - len(over_sla)) / len(response_times) * 100

print(f"SLA Compliance:")
print(f"  Responses meeting SLA: {len(response_times) - len(over_sla)}/{len(response_times)}")
print(f"  Compliance Rate:       {compliance_rate:.1f}%")

if over_sla:
    print(f"  ⚠️ {len(over_sla)} responses exceeded SLA")
else:
    print(f"  ✓ All responses met SLA target")
print()

# Check for process stability
if violations:
    print("⚠️ SERVICE LEVEL IS UNSTABLE")
    print()
    print("Statistical violations detected:")
    for rule, points in violations.items():
        print(f"  • {rule}")
        print(f"    Occurred at measurements: {points}")
        print(f"    Response times: {[f'{response_times[i]:.2f}' for i in points]} min")
    print()
    print("Recommendations:")
    print("  1. Investigate root causes of variation")
    print("  2. Review staffing levels during peak times")
    print("  3. Check for system performance issues")
    print("  4. Provide additional training if needed")
else:
    print("✓ SERVICE LEVEL IS STABLE")
    print()
    print("The process is in statistical control.")
    print("Response times are consistent and predictable.")

print()

# Performance metrics
median_time = statistics.median(response_times)
stdev = statistics.stdev(response_times)
min_time = min(response_times)
max_time = max(response_times)

print("Detailed Metrics:")
print(f"  Median Response Time:  {median_time:.2f} minutes")
print(f"  Standard Deviation:    {stdev:.2f} minutes")
print(f"  Fastest Response:      {min_time:.2f} minutes")
print(f"  Slowest Response:      {max_time:.2f} minutes")
print(f"  Range:                 {max_time - min_time:.2f} minutes")
print()

# Performance rating
if center < 4.0:
    rating = "Excellent"
elif center < 5.0:
    rating = "Good"
elif center < 6.0:
    rating = "Acceptable"
else:
    rating = "Needs Improvement"

print(f"Performance Rating: {rating}")
print(f"  Based on average response time of {center:.2f} minutes")
print()

# Save chart
filename = chart.render_to_file("service_response_times.html")
print(f"Interactive chart saved to: {filename}")
print()
print("=" * 70)
