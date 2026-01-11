"""Tests for the Flask web application."""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestFlaskApp:
    """Tests for Flask web application endpoints."""

    def test_index_route(self, client):
        """Test that the main page loads."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'SPC Chart Generator' in response.data
        assert b'chart-form' in response.data

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'

    def test_generate_xmr_chart(self, client):
        """Test generating an X-mR chart."""
        data = {
            'title': 'Test X-mR Chart',
            'data': '98.6, 98.7, 98.5, 98.8, 98.6, 98.7',
            'chart_type': 'X mR - X'
        }

        response = client.post('/api/generate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = response.get_json()
        assert 'html' in result
        assert 'Center Line:' in result['html']
        assert 'plotly' in result['html'].lower()

    def test_generate_c_chart(self, client):
        """Test generating a c-chart."""
        data = {
            'title': 'Defect Count',
            'data': '5, 3, 4, 6, 5, 4, 3, 7',
            'chart_type': 'c'
        }

        response = client.post('/api/generate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = response.get_json()
        assert 'html' in result
        assert 'Defect Count' in result['html']

    def test_invalid_data_format(self, client):
        """Test error handling for invalid data format."""
        data = {
            'title': 'Invalid Test',
            'data': 'abc, def, ghi',
            'chart_type': 'X mR - X'
        }

        response = client.post('/api/generate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400
        result = response.get_json()
        assert 'error' in result
        assert 'Invalid data format' in result['error']

    def test_empty_data(self, client):
        """Test error handling for empty data."""
        data = {
            'title': 'Empty Test',
            'data': '',
            'chart_type': 'X mR - X'
        }

        response = client.post('/api/generate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400
        result = response.get_json()
        assert 'error' in result

    def test_insufficient_data(self, client):
        """Test error handling for insufficient data points."""
        data = {
            'title': 'Single Point',
            'data': '42',
            'chart_type': 'X mR - X'
        }

        response = client.post('/api/generate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400
        result = response.get_json()
        assert 'error' in result

    def test_violation_detection(self, client):
        """Test that violations are detected and displayed."""
        # Data with an obvious outlier
        data = {
            'title': 'Violation Test',
            'data': '10, 11, 10, 11, 10, 11, 10, 100',
            'chart_type': 'X mR - X'
        }

        response = client.post('/api/generate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = response.get_json()
        # Should mention violations
        assert 'Violation' in result['html'] or 'violation' in result['html']

    def test_statistics_display(self, client):
        """Test that statistics are properly displayed."""
        data = {
            'title': 'Stats Test',
            'data': '1, 2, 3, 4, 5',
            'chart_type': 'X mR - X'
        }

        response = client.post('/api/generate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = response.get_json()
        html = result['html']

        # Check for all required statistics
        assert 'Center Line:' in html
        assert 'Lower Control Limit (LCL):' in html
        assert 'Upper Control Limit (UCL):' in html

    def test_whitespace_in_data(self, client):
        """Test that whitespace in data is handled correctly."""
        data = {
            'title': 'Whitespace Test',
            'data': '  1  ,  2  ,  3  ,  4  ,  5  ',
            'chart_type': 'X mR - X'
        }

        response = client.post('/api/generate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
