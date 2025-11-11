"""
Tests for authentication endpoints.

This module tests the authentication endpoints, specifically the login
functionality. Uses mocking to avoid dependency on Backendless service.

Author: Equipo 46
Date: 2024
"""

import pytest
from flask.testing import FlaskClient
from pydantic import ValidationError

from app.services.backendless_client import BackendlessClientError


@pytest.mark.unit
class TestAuthLogin:
    """Test suite for POST /auth/login endpoint."""

    def test_login_success(self, client: FlaskClient, mocker, sample_login_response):
        """
        Test successful login with valid credentials.

        Mocks BackendlessClient.login() to return a successful response
        and verifies that the endpoint returns 200 with correct data structure.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            sample_login_response: Sample login response fixture.
        """
        # Mock BackendlessClient.login() to return successful response
        mock_login = mocker.patch(
            'app.services.backendless_client.BackendlessClient.login'
        )
        mock_login.return_value = sample_login_response

        # Make request
        response = client.post(
            '/auth/login',
            json={
                'login': 'test@example.com',
                'password': 'Test123!'
            }
        )

        # Assertions
        assert response.status_code == 200, "Should return 200 on successful login"

        data = response.get_json()
        assert data is not None, "Response should contain JSON data"
        assert 'user-token' in data, "Response should include user-token"
        assert 'objectId' in data, "Response should include objectId"
        assert 'email' in data, "Response should include email"
        assert data['user-token'] == sample_login_response['user-token']
        assert data['objectId'] == sample_login_response['objectId']
        assert data['email'] == sample_login_response['email']

        # Verify mock was called with correct parameters
        mock_login.assert_called_once_with(
            login='test@example.com',
            password='Test123!'
        )

    def test_login_invalid_credentials(self, client: FlaskClient, mocker):
        """
        Test login with invalid credentials returns 401.

        Mocks BackendlessClient.login() to raise BackendlessClientError
        simulating invalid credentials from Backendless.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
        """
        # Mock BackendlessClient.login() to raise error (invalid credentials)
        mock_login = mocker.patch(
            'app.services.backendless_client.BackendlessClient.login'
        )
        mock_login.side_effect = BackendlessClientError(
            message="Invalid login or password",
            status_code=401
        )

        # Make request
        response = client.post(
            '/auth/login',
            json={
                'login': 'wrong@example.com',
                'password': 'WrongPassword'
            }
        )

        # Assertions
        assert response.status_code == 401, "Should return 401 for invalid credentials"

        data = response.get_json()
        assert data is not None, "Response should contain JSON data"
        assert 'message' in data, "Error response should include message"
        assert 'code' in data, "Error response should include code"
        assert data['code'] == 401

    def test_login_missing_login_field(self, client: FlaskClient):
        """
        Test login with missing 'login' field returns 400.

        Verifies that Pydantic validation catches missing required fields
        and the error handler returns appropriate 400 response.

        Args:
            client: Flask test client fixture.
        """
        # Make request with missing 'login' field
        response = client.post(
            '/auth/login',
            json={
                'password': 'Test123!'
                # 'login' field is missing
            }
        )

        # Assertions
        assert response.status_code == 400, "Should return 400 for missing required field"

        data = response.get_json()
        assert data is not None, "Response should contain JSON data"
        assert 'message' in data, "Error response should include message"
        assert 'code' in data, "Error response should include code"
        assert data['code'] == 400

    def test_login_missing_password_field(self, client: FlaskClient):
        """
        Test login with missing 'password' field returns 400.

        Verifies that Pydantic validation catches missing required fields.

        Args:
            client: Flask test client fixture.
        """
        # Make request with missing 'password' field
        response = client.post(
            '/auth/login',
            json={
                'login': 'test@example.com'
                # 'password' field is missing
            }
        )

        # Assertions
        assert response.status_code == 400, "Should return 400 for missing required field"

        data = response.get_json()
        assert data is not None, "Response should contain JSON data"
        assert 'message' in data
        assert 'code' in data
        assert data['code'] == 400

    def test_login_empty_login_field(self, client: FlaskClient):
        """
        Test login with empty 'login' field returns 400.

        Verifies that Pydantic min_length validation works.

        Args:
            client: Flask test client fixture.
        """
        # Make request with empty 'login' field
        response = client.post(
            '/auth/login',
            json={
                'login': '',
                'password': 'Test123!'
            }
        )

        # Assertions
        assert response.status_code == 400, "Should return 400 for empty login"

        data = response.get_json()
        assert data is not None
        assert data['code'] == 400

    def test_login_invalid_json(self, client: FlaskClient):
        """
        Test login with invalid JSON returns 400.

        Verifies that the endpoint handles malformed JSON properly.

        Args:
            client: Flask test client fixture.
        """
        # Make request with invalid JSON
        response = client.post(
            '/auth/login',
            data='{"login": "test", invalid json',  # Malformed JSON
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 400, "Should return 400 for invalid JSON"

        data = response.get_json()
        assert data is not None
        assert 'message' in data

    def test_login_no_json_body(self, client: FlaskClient):
        """
        Test login with no request body returns 415.

        Verifies that the endpoint requires Content-Type: application/json.
        Flask returns 415 (Unsupported Media Type) when Content-Type is not set.

        Args:
            client: Flask test client fixture.
        """
        # Make request without JSON body
        response = client.post('/auth/login')

        # Assertions
        # Flask returns 415 when Content-Type is not 'application/json'
        assert response.status_code == 415, "Should return 415 for missing Content-Type"

        data = response.get_json()
        assert data is not None
        assert 'message' in data

    def test_login_response_structure(self, client: FlaskClient, mocker, sample_login_response):
        """
        Test that login response has correct structure and field types.

        Verifies that the response matches the UserLoginResponse schema.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            sample_login_response: Sample login response fixture.
        """
        # Mock successful login
        mock_login = mocker.patch(
            'app.services.backendless_client.BackendlessClient.login'
        )
        mock_login.return_value = sample_login_response

        # Make request
        response = client.post(
            '/auth/login',
            json={
                'login': 'test@example.com',
                'password': 'Test123!'
            }
        )

        # Assertions
        assert response.status_code == 200

        data = response.get_json()

        # Verify all required fields are present
        required_fields = ['user-token', 'objectId', 'email']
        for field in required_fields:
            assert field in data, f"Response should include {field}"

        # Verify field types
        assert isinstance(data['user-token'], str), "user-token should be string"
        assert isinstance(data['objectId'], str), "objectId should be string"
        assert isinstance(data['email'], str), "email should be string"

        # Verify no extra fields (only the expected ones)
        assert len(data) == 3, "Response should only contain user-token, objectId, and email"

    def test_login_backendless_connection_error(self, client: FlaskClient, mocker):
        """
        Test login when Backendless service is unavailable.

        Simulates network error or Backendless downtime.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
        """
        # Mock BackendlessClient.login() to raise connection error
        mock_login = mocker.patch(
            'app.services.backendless_client.BackendlessClient.login'
        )
        mock_login.side_effect = BackendlessClientError(
            message="Failed to connect to Backendless",
            status_code=None
        )

        # Make request
        response = client.post(
            '/auth/login',
            json={
                'login': 'test@example.com',
                'password': 'Test123!'
            }
        )

        # Assertions
        # Should return 500 for server errors
        assert response.status_code == 500, "Should return 500 for connection errors"

        data = response.get_json()
        assert data is not None
        assert 'message' in data
