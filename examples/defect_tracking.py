#!/usr/bin/env python3
"""
Defect Tracking Example

Monitor defects using c-charts for count data.
"""

from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import CHART_C
import statistics

# Number of defects found per day in production
daily_defects = [
    5, 3, 4, 6, 5, 4, 3, 7, 2, 5,
    4, 6, 3, 5, 4, 6, 5, 3, 4, 5,
    6, 4, 5, 3, 4, 7, 5, 6, 4, 5
]

days = len(daily_defects)

print("=" * 70)
print("Production Defect Tracking Analysis")
print("=" * 70)
print()

# Create c-chart for count data
chart = PlotlySpcChart(
    daily_defects,
    title="Daily Defect Count - c-Chart",
    chart_type=CHART_C
)

# Get statistics
center = chart.center
lcl = chart.lcl
ucl = chart.ucl
violations = chart.violations

print(f"Defect Statistics ({days} days):")
print(f"  Average Defects/Day:    {center:.2f}")
print(f"  Lower Control Limit:    {lcl:.2f}")
print(f"  Upper Control Limit:    {ucl:.2f}")
print()

# Calculate totals
total_defects = sum(daily_defects)
min_defects = min(daily_defects)
max_defects = max(daily_defects)

print(f"Total Defects Found:      {total_defects}")
print(f"  Best Day:               {min_defects} defects")
print(f"  Worst Day:              {max_defects} defects")
print(f"  Range:                  {max_defects - min_defects} defects")
print()

# Quality metrics
units_produced_per_day = 1000
defect_rate_ppm = (total_defects / (units_produced_per_day * days)) * 1_000_000

print("Quality Metrics:")
print(f"  Units Produced/Day:     {units_produced_per_day}")
print(f"  Total Units Produced:   {units_produced_per_day * days:,}")
print(f"  Defect Rate:            {defect_rate_ppm:.0f} PPM")
print(f"  Quality Rate:           {100 - (total_defects/(units_produced_per_day*days)*100):.3f}%")
print()

# Check process stability
if violations:
    print("⚠️ DEFECT RATE IS UNSTABLE")
    print()
    print("Detected variations:")
    for rule, points in violations.items():
        print(f"  • {rule}")
        days_affected = [f"Day {p+1}" for p in points]
        defects_affected = [daily_defects[p] for p in points]
        print(f"    Days: {', '.join(days_affected)}")
        print(f"    Defects: {defects_affected}")
    print()
    print("Action Items:")
    print("  1. Investigate days with unusual defect counts")
    print("  2. Review production logs for those dates")
    print("  3. Check for equipment issues or maintenance")
    print("  4. Interview operators about any problems")
    print("  5. Inspect raw material quality for those batches")
else:
    print("✓ DEFECT RATE IS STABLE")
    print()
    print("The defect rate shows normal variation.")
    print("Focus on long-term process improvement.")

print()

# Trend analysis
first_half = daily_defects[:days//2]
second_half = daily_defects[days//2:]

avg_first_half = statistics.mean(first_half)
avg_second_half = statistics.mean(second_half)

print("Trend Analysis:")
print(f"  First Half Average:     {avg_first_half:.2f} defects/day")
print(f"  Second Half Average:    {avg_second_half:.2f} defects/day")

if avg_second_half < avg_first_half:
    improvement = ((avg_first_half - avg_second_half) / avg_first_half) * 100
    print(f"  ✓ Improvement:          {improvement:.1f}% reduction")
    print("  Quality is improving over time!")
elif avg_second_half > avg_first_half:
    deterioration = ((avg_second_half - avg_first_half) / avg_first_half) * 100
    print(f"  ⚠️ Deterioration:        {deterioration:.1f}% increase")
    print("  Quality is declining - investigate causes")
else:
    print("  No significant trend detected")

print()

# Six Sigma comparison
sigma_level = None
if defect_rate_ppm < 3.4:
    sigma_level = "Six Sigma (6σ)"
elif defect_rate_ppm < 233:
    sigma_level = "Five Sigma (5σ)"
elif defect_rate_ppm < 6210:
    sigma_level = "Four Sigma (4σ)"
elif defect_rate_ppm < 66807:
    sigma_level = "Three Sigma (3σ)"
else:
    sigma_level = "Below Three Sigma"

print(f"Process Capability Level: {sigma_level}")
print(f"  Current: {defect_rate_ppm:.0f} PPM")

target_levels = {
    "Six Sigma": 3.4,
    "Five Sigma": 233,
    "Four Sigma": 6210,
    "Three Sigma": 66807
}

print()
print("Quality Level Targets:")
for level, ppm in target_levels.items():
    if defect_rate_ppm > ppm:
        reduction_needed = defect_rate_ppm - ppm
        print(f"  {level}: {ppm:.0f} PPM (need to reduce by {reduction_needed:.0f} PPM)")
    else:
        print(f"  {level}: {ppm:.0f} PPM ✓ Achieved!")

print()

# Save chart
filename = chart.render_to_file("defect_tracking.html")
print(f"Interactive chart saved to: {filename}")
print()
print("=" * 70)
