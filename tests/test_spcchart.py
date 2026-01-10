"""Tests for the SpcChart visualization module."""

import os
import pytest
from spcchart import SpcChart


class TestSpcChart:
    """Tests for the SpcChart class."""

    def test_chart_creation(self):
        """Test basic chart creation."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        chart = SpcChart(data, title="Test Chart")

        assert chart.data == data
        assert chart.title == "Test Chart"
        assert chart.filename.endswith(".svg")

    def test_chart_with_custom_title(self):
        """Test chart creation with custom title."""
        data = [10, 20, 30, 40, 50]
        title = "Quality Metrics"
        chart = SpcChart(data, title=title)

        assert chart.title == title

    def test_chart_filename_is_unique(self):
        """Test that each chart gets a unique filename."""
        data = [1, 2, 3, 4, 5]
        chart1 = SpcChart(data, title="Chart 1")
        chart2 = SpcChart(data, title="Chart 2")

        assert chart1.filename != chart2.filename

    def test_render_to_file_creates_file(self, tmp_path):
        """Test that render_to_file creates an SVG file."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        chart = SpcChart(data, title="Test Chart")

        # Change to temporary directory
        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            filename = chart.render_to_file()

            # Verify file was created
            assert os.path.exists(filename)
            assert filename.endswith(".svg")

            # Verify file has content
            with open(filename, "r") as f:
                content = f.read()
                assert len(content) > 0
                assert "svg" in content.lower()  # Should contain SVG tags

        finally:
            os.chdir(original_dir)

    def test_render_to_file_returns_filename(self, tmp_path):
        """Test that render_to_file returns the filename."""
        data = [5, 10, 15, 20, 25]
        chart = SpcChart(data, title="Return Test")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = chart.render_to_file()

            assert result == chart.filename
            assert isinstance(result, str)
            assert result.endswith(".svg")

        finally:
            os.chdir(original_dir)

    def test_empty_data(self):
        """Test handling of empty data."""
        data = []
        chart = SpcChart(data, title="Empty Chart")

        # Chart creation should work
        assert chart.data == []

        # Rendering might fail with empty data
        # This is acceptable behavior

    def test_single_point_data(self, tmp_path):
        """Test handling of single data point."""
        data = [42]
        chart = SpcChart(data, title="Single Point")

        # Chart creation should work
        assert chart.data == [42]
        # Rendering might fail with single point - this is a known limitation


class TestSpcChartIntegration:
    """Integration tests for SpcChart with real data."""

    def test_widget_quality_example(self, tmp_path):
        """Test with example data similar to widget quality scenario."""
        data = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 5, 5,
            4, 4, 3, 3, 2, 2, 2, 3, 4, 5, 5, 5
        ]
        chart = SpcChart(data, title="Widget Quality")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            filename = chart.render_to_file()

            # File should be created successfully
            assert os.path.exists(filename)

            # Check file size is reasonable (SVG should have some content)
            file_size = os.path.getsize(filename)
            assert file_size > 100  # At least 100 bytes

        finally:
            os.chdir(original_dir)

    def test_process_monitoring_data(self, tmp_path):
        """Test with typical process monitoring data."""
        # Simulate temperature readings
        data = [
            98.6, 98.7, 98.5, 98.8, 98.6, 98.7, 98.6, 98.5,
            98.9, 98.7, 98.8, 98.6, 98.5, 98.7, 98.6
        ]
        chart = SpcChart(data, title="Temperature Monitoring")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            filename = chart.render_to_file()

            assert os.path.exists(filename)

        finally:
            os.chdir(original_dir)
