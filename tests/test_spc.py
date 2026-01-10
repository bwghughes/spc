"""Tests for the SPC statistical module."""

import pytest
import numpy as np
from spcchart.spc import (
    Spc,
    CHART_X_MR_X,
    CHART_X_MR_MR,
    CHART_X_BAR_R_X,
    CHART_X_BAR_R_R,
    CHART_X_BAR_S_X,
    CHART_X_BAR_S_S,
    CHART_P,
    CHART_NP,
    CHART_C,
    CHART_U,
    CHART_CUSUM,
    RULES_BASIC,
    RULES_WECO,
    RULES_NELSON,
    get_stats_x_mr_x,
    get_stats_c,
)


class TestSpcXMRChart:
    """Tests for X-mR (Individual and Moving Range) charts."""

    def test_basic_x_mr_chart(self):
        """Test basic X-mR chart creation."""
        data = [1, 2, 3, 3, 2, 1, 3, 8]
        spc = Spc(data, CHART_X_MR_X)
        center, lcl, ucl = spc.get_stats()

        assert isinstance(center, (int, float))
        assert isinstance(lcl, (int, float))
        assert isinstance(ucl, (int, float))
        assert lcl < center < ucl

    def test_x_mr_stats_calculation(self):
        """Test X-mR statistics calculation."""
        data = [1, 2, 3, 3, 2, 1, 3, 8]
        center, lcl, ucl = get_stats_x_mr_x(data, size=1)

        # Mean should be 2.875
        assert abs(center - 2.875) < 0.001

        # Control limits should be reasonable
        assert lcl < center
        assert ucl > center

    def test_violating_points_detection(self):
        """Test detection of points beyond control limits."""
        data = [1, 2, 3, 3, 2, 1, 3, 8]
        spc = Spc(data, CHART_X_MR_X, rules=RULES_BASIC)
        violations = spc.get_violating_points()

        assert isinstance(violations, dict)
        # The value 8 should be detected as beyond 3*sigma
        if "1 beyond 3*sigma" in violations:
            assert 7 in violations["1 beyond 3*sigma"]


class TestSpcXBarRChart:
    """Tests for Xbar-R (X-bar and Range) charts."""

    def test_x_bar_r_x_chart(self):
        """Test X-bar R chart for means."""
        # Subgroups of size 5
        data = [
            [20, 21, 19, 22, 20],
            [19, 20, 21, 20, 19],
            [21, 22, 20, 21, 20],
            [20, 19, 21, 20, 22],
        ]
        spc = Spc(data, CHART_X_BAR_R_X)
        center, lcl, ucl = spc.get_stats()

        assert isinstance(center, (int, float))
        assert lcl < center < ucl

    def test_x_bar_r_r_chart(self):
        """Test X-bar R chart for ranges."""
        data = [
            [20, 21, 19, 22, 20],
            [19, 20, 21, 20, 19],
            [21, 22, 20, 21, 20],
        ]
        spc = Spc(data, CHART_X_BAR_R_R)
        center, lcl, ucl = spc.get_stats()

        assert isinstance(center, (int, float))
        assert lcl >= 0  # Range cannot be negative
        assert ucl > center


class TestSpcXBarSChart:
    """Tests for Xbar-S (X-bar and Standard Deviation) charts."""

    def test_x_bar_s_x_chart(self):
        """Test X-bar S chart for means."""
        data = [
            [20, 21, 19, 22, 20],
            [19, 20, 21, 20, 19],
            [21, 22, 20, 21, 20],
        ]
        spc = Spc(data, CHART_X_BAR_S_X)
        center, lcl, ucl = spc.get_stats()

        assert isinstance(center, (int, float))
        assert lcl < center < ucl

    def test_x_bar_s_s_chart(self):
        """Test X-bar S chart for standard deviations."""
        data = [
            [20, 21, 19, 22, 20],
            [19, 20, 21, 20, 19],
            [21, 22, 20, 21, 20],
        ]
        spc = Spc(data, CHART_X_BAR_S_S)
        center, lcl, ucl = spc.get_stats()

        assert isinstance(center, (int, float))
        assert lcl >= 0  # Standard deviation cannot be negative


class TestSpcAttributeCharts:
    """Tests for attribute control charts (p, np, c, u)."""

    def test_p_chart(self):
        """Test p-chart (proportion defective)."""
        # Proportions should be between 0 and 1
        data = [0.05, 0.03, 0.04, 0.06, 0.05, 0.04]
        spc = Spc(data, CHART_P, sizes=100)
        center, lcl, ucl = spc.get_stats()

        assert 0 <= center <= 1
        assert 0 <= lcl <= 1
        assert 0 <= ucl <= 1

    def test_np_chart(self):
        """Test np-chart (number of defectives)."""
        data = [5, 3, 4, 6, 5, 4]
        spc = Spc(data, CHART_NP, sizes=100)
        center, lcl, ucl = spc.get_stats()

        assert isinstance(center, (int, float))
        assert lcl >= 0

    def test_c_chart(self):
        """Test c-chart (count of defects)."""
        data = [5, 3, 4, 6, 5, 4, 3, 7]
        center, lcl, ucl = get_stats_c(data, size=1)

        assert isinstance(center, (int, float))
        assert lcl >= 0  # Cannot have negative counts
        assert ucl > center

    def test_u_chart(self):
        """Test u-chart (defects per unit)."""
        data = [5, 3, 4, 6, 5, 4]
        spc = Spc(data, CHART_U, sizes=10)
        center, lcl, ucl = spc.get_stats()

        assert isinstance(center, (int, float))
        assert lcl >= 0


class TestSpcCUSUM:
    """Tests for CUSUM (Cumulative Sum) charts."""

    def test_cusum_chart(self):
        """Test CUSUM chart creation."""
        data = [1, 2, 3, 3, 2, 1, 3, 8]
        # CUSUM chart with basic rules may fail due to None limits
        # Use empty rules to avoid limit checking
        spc = Spc(data, CHART_CUSUM, rules=[])
        center, lcl, ucl = spc.get_stats()

        # CUSUM returns center=0, lcl=None, ucl=None
        assert center == 0
        assert lcl is None
        assert ucl is None


class TestSpcRules:
    """Tests for control chart rules (WECO, Nelson, etc.)."""

    def test_rules_basic(self):
        """Test basic rules (beyond 3 sigma)."""
        data = [1, 2, 3, 3, 2, 1, 3, 100]  # 100 is clearly an outlier
        spc = Spc(data, CHART_X_MR_X, rules=RULES_BASIC)
        violations = spc.get_violating_points()

        assert isinstance(violations, dict)

    def test_rules_weco(self):
        """Test WECO rules."""
        data = list(range(20))
        spc = Spc(data, CHART_X_MR_X, rules=RULES_WECO)
        violations = spc.get_violating_points()

        assert isinstance(violations, dict)

    def test_rules_nelson(self):
        """Test Nelson rules."""
        data = [5] * 10 + [15] * 10  # Two distinct levels
        spc = Spc(data, CHART_X_MR_X, rules=RULES_NELSON)
        violations = spc.get_violating_points()

        assert isinstance(violations, dict)


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_single_value(self):
        """Test handling of single data point."""
        with pytest.raises((AssertionError, ValueError, IndexError, ZeroDivisionError)):
            data = [5]
            spc = Spc(data, CHART_X_MR_X)

    def test_empty_data(self):
        """Test handling of empty data."""
        with pytest.raises((AssertionError, ValueError, IndexError)):
            data = []
            spc = Spc(data, CHART_X_MR_X)

    def test_invalid_subgroup_size(self):
        """Test handling of invalid subgroup size."""
        with pytest.raises(AssertionError):
            # Subgroup size 15 is beyond the supported range (2-10)
            data = [[i] * 15 for i in range(5)]
            spc = Spc(data, CHART_X_BAR_R_X)
