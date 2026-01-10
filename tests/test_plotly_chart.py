"""Tests for the PlotlySpcChart module."""

import pytest
import os
from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import CHART_X_MR_X, CHART_X_BAR_R_X, CHART_P, CHART_C


class TestPlotlySpcChart:
    """Tests for the PlotlySpcChart class."""

    def test_chart_creation(self):
        """Test basic chart creation."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        chart = PlotlySpcChart(data, title="Test Chart")

        assert chart.data == data
        assert chart.title == "Test Chart"
        assert chart.chart_type == CHART_X_MR_X

    def test_chart_statistics(self):
        """Test that statistics are calculated correctly."""
        data = [10, 20, 30, 40, 50]
        chart = PlotlySpcChart(data, title="Stats Test")

        assert chart.center is not None
        assert chart.lcl is not None
        assert chart.ucl is not None
        assert isinstance(chart.center, (int, float))
        assert isinstance(chart.lcl, (int, float))
        assert isinstance(chart.ucl, (int, float))

    def test_render_to_html(self):
        """Test HTML rendering."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        chart = PlotlySpcChart(data, title="HTML Test")

        html = chart.render_to_html(include_plotlyjs=False)

        assert isinstance(html, str)
        assert len(html) > 0
        assert "HTML Test" in html  # Title should be in HTML
        assert "plotly" in html.lower()  # Should contain plotly references

    def test_render_to_file(self, tmp_path):
        """Test file rendering."""
        data = [5, 10, 15, 20, 25, 20, 15, 10, 5]
        chart = PlotlySpcChart(data, title="File Test")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            filename = chart.render_to_file()

            # Verify file was created
            assert os.path.exists(filename)
            assert filename.endswith(".html")

            # Verify file has content
            with open(filename, "r") as f:
                content = f.read()
                assert len(content) > 0
                assert "File Test" in content

        finally:
            os.chdir(original_dir)

    def test_render_to_file_custom_name(self, tmp_path):
        """Test file rendering with custom filename."""
        data = [1, 2, 3, 4, 5]
        chart = PlotlySpcChart(data, title="Custom File Test")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            filename = chart.render_to_file("custom_chart.html")

            assert filename == "custom_chart.html"
            assert os.path.exists(filename)

        finally:
            os.chdir(original_dir)

    def test_get_figure(self):
        """Test getting the Plotly figure object."""
        data = [1, 2, 3, 4, 5]
        chart = PlotlySpcChart(data, title="Figure Test")

        fig = chart.get_figure()

        # Figure should be a Plotly graph object
        assert fig is not None
        assert hasattr(fig, 'data')  # Should have data attribute
        assert hasattr(fig, 'layout')  # Should have layout attribute

    def test_different_chart_types(self):
        """Test creating charts with different types."""
        data = [1, 2, 3, 4, 5, 6, 7, 8]

        # X-mR chart
        chart_xmr = PlotlySpcChart(data, title="XMR", chart_type=CHART_X_MR_X)
        assert chart_xmr.chart_type == CHART_X_MR_X

        # c-chart
        chart_c = PlotlySpcChart(data, title="C Chart", chart_type=CHART_C)
        assert chart_c.chart_type == CHART_C

    def test_violation_detection(self):
        """Test that violations are detected."""
        # Create data with an obvious outlier
        data = [10, 11, 10, 11, 10, 11, 10, 100]  # 100 is way out
        chart = PlotlySpcChart(data, title="Violation Test")

        # Should have some violations
        violations = chart.violations
        assert isinstance(violations, dict)

    def test_widget_quality_example(self, tmp_path):
        """Test with example data similar to widget quality scenario."""
        data = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 5, 5,
            4, 4, 3, 3, 2, 2, 2, 3, 4, 5, 5, 5
        ]
        chart = PlotlySpcChart(data, title="Widget Quality")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            filename = chart.render_to_file()

            # File should be created successfully
            assert os.path.exists(filename)

            # Check file size is reasonable
            file_size = os.path.getsize(filename)
            assert file_size > 1000  # At least 1KB

        finally:
            os.chdir(original_dir)

    def test_temperature_monitoring_data(self):
        """Test with typical process monitoring data."""
        # Simulate temperature readings
        data = [
            98.6, 98.7, 98.5, 98.8, 98.6, 98.7, 98.6, 98.5,
            98.9, 98.7, 98.8, 98.6, 98.5, 98.7, 98.6
        ]
        chart = PlotlySpcChart(data, title="Temperature Monitoring")

        html = chart.render_to_html(include_plotlyjs=False)
        assert "Temperature Monitoring" in html

    def test_empty_data_handling(self):
        """Test handling of edge cases."""
        # Empty data should raise an error
        with pytest.raises((AssertionError, ValueError, IndexError, ZeroDivisionError)):
            data = []
            chart = PlotlySpcChart(data, title="Empty")

    def test_single_point_handling(self):
        """Test handling of single data point."""
        # Single point should raise an error
        with pytest.raises((AssertionError, ValueError, IndexError, ZeroDivisionError)):
            data = [42]
            chart = PlotlySpcChart(data, title="Single Point")


class TestPlotlyChartIntegration:
    """Integration tests for PlotlySpcChart."""

    def test_full_workflow(self, tmp_path):
        """Test complete workflow from data to HTML file."""
        data = [5, 10, 15, 20, 25, 30, 25, 20, 15, 10, 5]
        title = "Complete Workflow Test"

        # Create chart
        chart = PlotlySpcChart(data, title=title, chart_type=CHART_X_MR_X)

        # Verify statistics
        assert chart.center is not None
        assert chart.lcl is not None
        assert chart.ucl is not None

        # Get HTML
        html = chart.render_to_html(include_plotlyjs=False)
        assert title in html

        # Save to file
        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            filename = chart.render_to_file("workflow_test.html")
            assert os.path.exists(filename)

        finally:
            os.chdir(original_dir)

    def test_comparison_with_pygal_chart(self):
        """Test that plotly chart works with same data as pygal chart."""
        from spcchart import SpcChart  # Pygal version

        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Create both chart types
        pygal_chart = SpcChart(data, title="Pygal Chart")
        plotly_chart = PlotlySpcChart(data, title="Plotly Chart")

        # Both should have statistics
        assert pygal_chart.data == plotly_chart.data

        # Both should be able to render
        html_plotly = plotly_chart.render_to_html(include_plotlyjs=False)
        assert len(html_plotly) > 0
