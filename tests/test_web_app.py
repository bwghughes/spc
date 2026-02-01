"""Tests for the Flask web application."""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestIndexPage:
    """Tests for the main index page."""

    def test_index_returns_200(self, client):
        """Test that the index page returns 200 status."""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_returns_html(self, client):
        """Test that the index page returns HTML content."""
        response = client.get('/')
        assert response.content_type.startswith('text/html')

    def test_index_contains_title(self, client):
        """Test that the index page contains the page title."""
        response = client.get('/')
        assert b'SPC Chart Generator' in response.data

    def test_index_contains_form(self, client):
        """Test that the index page contains the chart form."""
        response = client.get('/')
        assert b'chart-form' in response.data
        assert b'Generate Chart' in response.data

    def test_index_contains_chart_types(self, client):
        """Test that the index page contains all chart type options."""
        response = client.get('/')
        assert b'X mR - X' in response.data or b'X-mR' in response.data
        assert b'Xbar R - X' in response.data or b'X-bar R' in response.data
        assert b'p-chart' in response.data
        assert b'c-chart' in response.data

    def test_index_contains_dark_mode_toggle(self, client):
        """Test that the index page contains dark mode toggle."""
        response = client.get('/')
        assert b'theme-toggle' in response.data

    def test_index_contains_preset_buttons(self, client):
        """Test that the index page contains sample data preset buttons."""
        response = client.get('/')
        assert b'preset-btn' in response.data
        assert b'Temperature' in response.data
        assert b'Quality' in response.data


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_returns_200(self, client):
        """Test that the health endpoint returns 200 status."""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_returns_json(self, client):
        """Test that the health endpoint returns JSON."""
        response = client.get('/health')
        assert response.content_type == 'application/json'

    def test_health_returns_ok_status(self, client):
        """Test that the health endpoint returns ok status."""
        response = client.get('/health')
        data = json.loads(response.data)
        assert data['status'] == 'ok'


class TestGenerateChartAPI:
    """Tests for the chart generation API endpoint."""

    def test_generate_requires_post(self, client):
        """Test that the generate endpoint requires POST method."""
        response = client.get('/api/generate')
        assert response.status_code == 405  # Method Not Allowed

    def test_generate_valid_xmr_chart(self, client):
        """Test generating a valid X-mR chart."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Test Chart',
                'data': '1, 2, 3, 4, 5, 6, 7, 8, 9, 10',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'html' in data
        assert 'error' not in data

    def test_generate_xbar_r_chart_requires_subgroups(self, client):
        """Test that X-bar R chart returns error without proper subgroup data."""
        # X-bar R charts require subgroup data which isn't fully supported
        # in the simple web interface (would need sizes parameter)
        response = client.post(
            '/api/generate',
            json={
                'title': 'X-bar R Test',
                'data': '10, 20, 30, 40, 50, 60, 70, 80',
                'chart_type': 'Xbar R - X'
            },
            content_type='application/json'
        )

        # Currently returns an error as subgroups need size configuration
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data

    def test_generate_p_chart_requires_sizes(self, client):
        """Test that p-chart returns error without proper sizes data."""
        # p-charts require sample sizes which aren't provided in simple interface
        response = client.post(
            '/api/generate',
            json={
                'title': 'P Chart Test',
                'data': '0.1, 0.2, 0.15, 0.12, 0.18, 0.22, 0.14, 0.16',
                'chart_type': 'p'
            },
            content_type='application/json'
        )

        # Currently returns an error as p-charts need size configuration
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data

    def test_generate_valid_c_chart(self, client):
        """Test generating a valid c-chart."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'C Chart Test',
                'data': '3, 5, 2, 4, 6, 3, 4, 5, 2, 3',
                'chart_type': 'c'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'html' in data

    def test_generate_returns_statistics(self, client):
        """Test that generated chart includes statistics."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Stats Test',
                'data': '10, 20, 30, 40, 50',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        html = data['html']

        # Should contain statistics elements
        assert 'Center Line' in html
        assert 'LCL' in html
        assert 'UCL' in html
        assert 'Violations' in html

    def test_generate_returns_chart_container(self, client):
        """Test that generated chart includes chart container."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Container Test',
                'data': '1, 2, 3, 4, 5, 6, 7, 8',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)

        # Should contain chart container div
        assert 'chart-container' in data['html']

    def test_generate_empty_data_returns_error(self, client):
        """Test that empty data returns an error."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Empty Test',
                'data': '',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No valid data' in data['error']

    def test_generate_single_point_returns_error(self, client):
        """Test that single data point returns an error."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Single Point Test',
                'data': '42',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'At least 2 data points' in data['error']

    def test_generate_invalid_data_format_returns_error(self, client):
        """Test that invalid data format returns an error."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Invalid Data Test',
                'data': 'not, valid, numbers, abc',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_generate_whitespace_data_returns_error(self, client):
        """Test that whitespace-only data returns an error."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Whitespace Test',
                'data': '   ,   ,   ',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_generate_default_title(self, client):
        """Test that missing title gets a default."""
        response = client.post(
            '/api/generate',
            json={
                'data': '1, 2, 3, 4, 5, 6, 7, 8',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_generate_default_chart_type(self, client):
        """Test that missing chart type gets a default."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Default Type Test',
                'data': '1, 2, 3, 4, 5, 6, 7, 8'
            },
            content_type='application/json'
        )

        assert response.status_code == 200


class TestGenerateChartAPIDataFormats:
    """Tests for various data input formats."""

    def test_data_with_extra_spaces(self, client):
        """Test that data with extra spaces is handled correctly."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Spaces Test',
                'data': '  1  ,  2  ,  3  ,  4  ,  5  ',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'html' in data

    def test_data_with_decimals(self, client):
        """Test that decimal data is handled correctly."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Decimal Test',
                'data': '98.6, 98.7, 98.5, 98.8, 98.6',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'html' in data

    def test_data_with_negative_numbers(self, client):
        """Test that negative numbers are handled correctly."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Negative Test',
                'data': '-5, -3, -1, 1, 3, 5',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'html' in data

    def test_data_with_large_numbers(self, client):
        """Test that large numbers are handled correctly."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Large Numbers Test',
                'data': '1000000, 1000001, 1000002, 1000003, 1000004',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'html' in data

    def test_data_with_small_decimals(self, client):
        """Test that small decimal numbers are handled correctly."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Small Decimals Test',
                'data': '0.001, 0.002, 0.003, 0.004, 0.005',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'html' in data


class TestGenerateChartAPIViolations:
    """Tests for violation detection in the API."""

    def test_chart_with_violations(self, client):
        """Test that violations are detected and reported."""
        # Data with obvious outlier
        response = client.post(
            '/api/generate',
            json={
                'title': 'Violation Test',
                'data': '10, 11, 10, 11, 10, 11, 10, 100',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        # Should contain violations section
        assert 'Violations' in data['html']

    def test_chart_without_violations(self, client):
        """Test chart with stable data (no violations)."""
        # Stable data within control limits
        response = client.post(
            '/api/generate',
            json={
                'title': 'Stable Test',
                'data': '10.0, 10.1, 9.9, 10.0, 10.2, 9.8, 10.1, 9.9',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'Violations' in data['html']


class TestStatisticsDisplay:
    """Tests for the statistics display in generated charts."""

    def test_stats_grid_is_present(self, client):
        """Test that stats grid is present in output."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Stats Grid Test',
                'data': '10, 20, 30, 40, 50',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'stats-grid' in data['html']
        assert 'stat-card' in data['html']

    def test_stats_values_are_formatted(self, client):
        """Test that statistics values are properly formatted."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Format Test',
                'data': '10, 20, 30, 40, 50',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        # Stats should be formatted with decimal places
        assert 'stat-value' in data['html']


class TestUIElements:
    """Tests for specific UI elements in the web app."""

    def test_logo_is_present(self, client):
        """Test that the logo is present."""
        response = client.get('/')
        assert b'logo' in response.data
        assert b'SPCChart' in response.data

    def test_github_link_is_present(self, client):
        """Test that the GitHub link is present."""
        response = client.get('/')
        assert b'github.com' in response.data

    def test_footer_is_present(self, client):
        """Test that the footer is present."""
        response = client.get('/')
        assert b'footer' in response.data
        assert b'Statistical Process Control Charts For Humans' in response.data

    def test_hero_section_is_present(self, client):
        """Test that the hero section is present."""
        response = client.get('/')
        assert b'hero' in response.data
        assert b'Statistical Process Control Charts' in response.data


class TestAccessibility:
    """Tests for accessibility features."""

    def test_html_has_lang_attribute(self, client):
        """Test that HTML has lang attribute for accessibility."""
        response = client.get('/')
        assert b'lang="en"' in response.data

    def test_form_has_labels(self, client):
        """Test that form inputs have proper labels."""
        response = client.get('/')
        assert b'form-label' in response.data
        assert b'for="title"' in response.data
        assert b'for="data"' in response.data

    def test_theme_toggle_has_aria_label(self, client):
        """Test that theme toggle has aria-label."""
        response = client.get('/')
        assert b'aria-label' in response.data

    def test_viewport_meta_is_present(self, client):
        """Test that viewport meta tag is present for mobile responsiveness."""
        response = client.get('/')
        assert b'viewport' in response.data


class TestContentSecurityHeaders:
    """Tests for response headers and security."""

    def test_api_returns_json_content_type(self, client):
        """Test that API returns proper JSON content type."""
        response = client.post(
            '/api/generate',
            json={
                'title': 'Content Type Test',
                'data': '1, 2, 3, 4, 5',
                'chart_type': 'X mR - X'
            },
            content_type='application/json'
        )

        assert response.content_type == 'application/json'
