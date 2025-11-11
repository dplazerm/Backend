"""
Tests for root endpoint.

This module tests the root endpoint that provides API information.

Author: Equipo 46
Date: 2024
"""

import pytest
from flask.testing import FlaskClient


@pytest.mark.unit
class TestRootEndpoint:
    """Test suite for GET / endpoint."""

    def test_root_endpoint_success(self, client: FlaskClient):
        """
        Test root endpoint returns API information.

        Verifies that accessing the root URL returns 200 and includes
        API metadata and available endpoints.

        Args:
            client: Flask test client fixture.
        """
        # Make request to root endpoint
        response = client.get('/')

        # Assertions
        assert response.status_code == 200, "Should return 200 for root endpoint"

        data = response.get_json()
        assert data is not None, "Response should contain JSON data"

        # Verify required fields
        assert 'name' in data, "Response should include name"
        assert 'version' in data, "Response should include version"
        assert 'description' in data, "Response should include description"
        assert 'status' in data, "Response should include status"
        assert 'endpoints' in data, "Response should include endpoints"

        # Verify status
        assert data['status'] == 'online', "API status should be 'online'"

        # Verify endpoints structure
        assert 'auth' in data['endpoints'], "Should include auth endpoints"
        assert 'subjects' in data['endpoints'], "Should include subjects endpoints"

    def test_root_endpoint_structure(self, client: FlaskClient):
        """
        Test root endpoint response structure.

        Verifies detailed structure of the API information response.

        Args:
            client: Flask test client fixture.
        """
        response = client.get('/')
        data = response.get_json()

        # Verify auth endpoints
        assert 'login' in data['endpoints']['auth'], "Should include login endpoint"

        # Verify subjects endpoints
        subjects_endpoints = data['endpoints']['subjects']
        assert 'list' in subjects_endpoints, "Should include list endpoint"
        assert 'create' in subjects_endpoints, "Should include create endpoint"
        assert 'get' in subjects_endpoints, "Should include get endpoint"
        assert 'update' in subjects_endpoints, "Should include update endpoint"
        assert 'delete' in subjects_endpoints, "Should include delete endpoint"

    def test_root_endpoint_field_types(self, client: FlaskClient):
        """
        Test root endpoint field types are correct.

        Verifies that all fields have the expected data types.

        Args:
            client: Flask test client fixture.
        """
        response = client.get('/')
        data = response.get_json()

        # Verify field types
        assert isinstance(data['name'], str), "name should be string"
        assert isinstance(data['version'], str), "version should be string"
        assert isinstance(data['description'], str), "description should be string"
        assert isinstance(data['status'], str), "status should be string"
        assert isinstance(data['endpoints'], dict), "endpoints should be dict"
