"""
Pytest configuration and shared fixtures.

This module provides fixtures that are shared across all test files.
Following pytest best practices for test organization and reusability.

Author: Equipo 46
Date: 2024
"""

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app


@pytest.fixture(scope='function')
def app() -> Flask:
    """
    Creates a Flask application instance configured for testing.

    This fixture creates a new app instance for each test function,
    ensuring test isolation. Uses the 'testing' configuration which
    enables TEST mode and debug mode.

    Yields:
        Flask: Configured Flask application instance.

    Example:
        def test_something(app):
            assert app.testing is True
    """
    app = create_app('testing')
    yield app


@pytest.fixture(scope='function')
def client(app: Flask) -> FlaskClient:
    """
    Creates a Flask test client for making requests to the app.

    The test client allows making HTTP requests to the application
    without running a server. Each test gets a fresh client instance.

    Args:
        app: Flask application instance from app fixture.

    Yields:
        FlaskClient: Test client for making requests.

    Example:
        def test_endpoint(client):
            response = client.get('/subjects')
            assert response.status_code == 401
    """
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='function')
def auth_headers() -> dict:
    """
    Provides authentication headers with a fake user-token.

    This fixture returns headers that can be used for authenticated
    requests in tests. The token is fake and should be mocked when
    testing endpoints that validate tokens with Backendless.

    Returns:
        dict: Headers dictionary with user-token.

    Example:
        def test_authenticated_endpoint(client, auth_headers):
            response = client.get('/subjects', headers=auth_headers)
            # Remember to mock BackendlessClient responses
    """
    return {
        'user-token': 'fake-test-token-12345',
        'Content-Type': 'application/json'
    }


@pytest.fixture(scope='function')
def sample_subject_data() -> dict:
    """
    Provides sample subject data for testing create/update operations.

    Returns a dictionary with valid subject data that can be used
    for POST and PUT requests in tests.

    Returns:
        dict: Valid subject data.

    Example:
        def test_create_subject(client, auth_headers, sample_subject_data):
            response = client.post('/subjects',
                                   json=sample_subject_data,
                                   headers=auth_headers)
    """
    return {
        'name': 'Cálculo I',
        'code': 'CALC1',
        'kind': 'class',
        'weeklyLoadHours': 4
    }


@pytest.fixture(scope='function')
def sample_subject_response() -> dict:
    """
    Provides sample subject response from Backendless.

    Returns a dictionary mimicking what Backendless would return
    when creating or fetching a subject. Useful for mocking
    BackendlessClient responses.

    Returns:
        dict: Subject data as returned by Backendless.

    Example:
        def test_something(mocker, sample_subject_response):
            mock_create = mocker.patch('app.services.backendless_client.BackendlessClient.create')
            mock_create.return_value = sample_subject_response
    """
    return {
        'objectId': 'TEST123',
        'name': 'Cálculo I',
        'code': 'CALC1',
        'kind': 'class',
        'weeklyLoadHours': 4,
        'created': 1699564800000,
        'updated': 1699564800000
    }


@pytest.fixture(scope='function')
def sample_login_response() -> dict:
    """
    Provides sample login response from Backendless.

    Returns a dictionary mimicking what Backendless would return
    on successful login. Useful for mocking BackendlessClient.login().

    Returns:
        dict: Login response data as returned by Backendless.

    Example:
        def test_login(mocker, sample_login_response):
            mock_login = mocker.patch('app.services.backendless_client.BackendlessClient.login')
            mock_login.return_value = sample_login_response
    """
    return {
        'user-token': 'mock-token-abc123xyz',
        'objectId': 'USER123',
        'email': 'test@example.com'
    }


@pytest.fixture(scope='function')
def sample_subjects_list() -> list:
    """
    Provides a sample list of subjects for testing list endpoints.

    Returns a list of subject dictionaries as would be returned by
    Backendless list operation. Useful for mocking paginated responses.

    Returns:
        list: List of subject dictionaries.

    Example:
        def test_list_subjects(mocker, sample_subjects_list):
            mock_list = mocker.patch('app.services.backendless_client.BackendlessClient.list')
            mock_list.return_value = sample_subjects_list
    """
    return [
        {
            'objectId': 'SUBJ1',
            'name': 'Cálculo I',
            'code': 'CALC1',
            'kind': 'class',
            'weeklyLoadHours': 4,
            'created': 1699564800000,
            'updated': 1699564800000
        },
        {
            'objectId': 'SUBJ2',
            'name': 'Física I',
            'code': 'FIS1',
            'kind': 'class',
            'weeklyLoadHours': 5,
            'created': 1699564800000,
            'updated': 1699564800000
        }
    ]
