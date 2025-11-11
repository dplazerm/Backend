"""
Tests for subjects CRUD endpoints.

This module tests all CRUD operations for subjects: list, create, get,
update, and delete. Uses mocking to avoid dependency on Backendless.

Author: Equipo 46
Date: 2024
"""

import pytest
from flask.testing import FlaskClient

from app.services.backendless_client import BackendlessClientError


@pytest.mark.unit
class TestListSubjects:
    """Test suite for GET /subjects endpoint."""

    def test_list_subjects_success(self, client: FlaskClient, mocker, auth_headers, sample_subjects_list):
        """
        Test successful listing of subjects with pagination.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            auth_headers: Authentication headers fixture.
            sample_subjects_list: Sample subjects list fixture.
        """
        # Mock count and list methods
        mock_count = mocker.patch(
            'app.services.backendless_client.BackendlessClient.count'
        )
        mock_count.return_value = 2

        mock_list = mocker.patch(
            'app.services.backendless_client.BackendlessClient.list'
        )
        mock_list.return_value = sample_subjects_list

        # Make request
        response = client.get('/subjects', headers=auth_headers)

        # Assertions
        assert response.status_code == 200

        data = response.get_json()
        assert data is not None
        assert 'total' in data
        assert 'count' in data
        assert 'offset' in data
        assert 'results' in data
        assert data['total'] == 2
        assert data['count'] == 2
        assert data['offset'] == 0
        assert len(data['results']) == 2

    def test_list_subjects_with_pagination(self, client: FlaskClient, mocker, auth_headers, sample_subjects_list):
        """
        Test listing subjects with custom pagination parameters.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            auth_headers: Authentication headers fixture.
            sample_subjects_list: Sample subjects list fixture.
        """
        mock_count = mocker.patch(
            'app.services.backendless_client.BackendlessClient.count'
        )
        mock_count.return_value = 10

        mock_list = mocker.patch(
            'app.services.backendless_client.BackendlessClient.list'
        )
        mock_list.return_value = sample_subjects_list

        # Make request with pagination params
        response = client.get(
            '/subjects?pageSize=2&offset=4',
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 200

        data = response.get_json()
        assert data['offset'] == 4
        assert data['count'] == 2

        # Verify mock was called with correct pagination params
        mock_list.assert_called_once()
        call_kwargs = mock_list.call_args.kwargs
        assert call_kwargs['page_size'] == 2
        assert call_kwargs['offset'] == 4

    def test_list_subjects_with_code_filter(self, client: FlaskClient, mocker, auth_headers):
        """
        Test listing subjects filtered by code.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            auth_headers: Authentication headers fixture.
        """
        filtered_subject = [{
            'objectId': 'SUBJ1',
            'name': 'Cálculo I',
            'code': 'CALC1',
            'kind': 'class',
            'weeklyLoadHours': 4
        }]

        mock_count = mocker.patch(
            'app.services.backendless_client.BackendlessClient.count'
        )
        mock_count.return_value = 1

        mock_list = mocker.patch(
            'app.services.backendless_client.BackendlessClient.list'
        )
        mock_list.return_value = filtered_subject

        # Make request with code filter
        response = client.get(
            '/subjects?code=CALC1',
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 200

        data = response.get_json()
        assert data['total'] == 1
        assert data['count'] == 1

        # Verify where_clause was constructed correctly
        mock_list.assert_called_once()
        call_kwargs = mock_list.call_args.kwargs
        assert call_kwargs['where_clause'] == "code='CALC1'"

    def test_list_subjects_unauthorized(self, client: FlaskClient):
        """
        Test that listing subjects without auth token returns 401.

        Args:
            client: Flask test client fixture.
        """
        # Make request without auth headers
        response = client.get('/subjects')

        # Assertions
        assert response.status_code == 401

        data = response.get_json()
        assert data is not None
        assert 'message' in data
        assert data['code'] == 401


@pytest.mark.unit
class TestCreateSubject:
    """Test suite for POST /subjects endpoint."""

    def test_create_subject_success(self, client: FlaskClient, mocker, auth_headers, sample_subject_data, sample_subject_response):
        """
        Test successful subject creation.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            auth_headers: Authentication headers fixture.
            sample_subject_data: Sample subject input data fixture.
            sample_subject_response: Sample subject response fixture.
        """
        # Mock create method
        mock_create = mocker.patch(
            'app.services.backendless_client.BackendlessClient.create'
        )
        mock_create.return_value = sample_subject_response

        # Make request
        response = client.post(
            '/subjects',
            json=sample_subject_data,
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 201

        data = response.get_json()
        assert data is not None
        assert 'objectId' in data
        assert 'name' in data
        assert 'code' in data
        assert data['name'] == sample_subject_data['name']
        assert data['code'] == sample_subject_data['code']

    def test_create_subject_missing_required_field(self, client: FlaskClient, auth_headers):
        """
        Test creating subject with missing required field returns 400.

        Args:
            client: Flask test client fixture.
            auth_headers: Authentication headers fixture.
        """
        # Request missing 'code' field
        invalid_data = {
            'name': 'Cálculo I',
            # 'code' is missing
            'kind': 'class'
        }

        response = client.post(
            '/subjects',
            json=invalid_data,
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 400

        data = response.get_json()
        assert data is not None
        assert data['code'] == 400

    def test_create_subject_invalid_kind(self, client: FlaskClient, auth_headers):
        """
        Test creating subject with invalid 'kind' value returns 400.

        Args:
            client: Flask test client fixture.
            auth_headers: Authentication headers fixture.
        """
        invalid_data = {
            'name': 'Cálculo I',
            'code': 'CALC1',
            'kind': 'invalid_kind',  # Not in allowed values
            'weeklyLoadHours': 4
        }

        response = client.post(
            '/subjects',
            json=invalid_data,
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 400

        data = response.get_json()
        assert data is not None
        assert data['code'] == 400

    def test_create_subject_negative_hours(self, client: FlaskClient, auth_headers):
        """
        Test creating subject with negative weeklyLoadHours returns 400.

        Args:
            client: Flask test client fixture.
            auth_headers: Authentication headers fixture.
        """
        invalid_data = {
            'name': 'Cálculo I',
            'code': 'CALC1',
            'kind': 'class',
            'weeklyLoadHours': -5  # Invalid: must be >= 0
        }

        response = client.post(
            '/subjects',
            json=invalid_data,
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 400

        data = response.get_json()
        assert data is not None
        assert data['code'] == 400

    def test_create_subject_unauthorized(self, client: FlaskClient, sample_subject_data):
        """
        Test creating subject without auth token returns 401.

        Args:
            client: Flask test client fixture.
            sample_subject_data: Sample subject input data fixture.
        """
        # Make request without auth headers
        response = client.post(
            '/subjects',
            json=sample_subject_data
        )

        # Assertions
        assert response.status_code == 401

        data = response.get_json()
        assert data is not None
        assert data['code'] == 401


@pytest.mark.unit
class TestGetSubjectById:
    """Test suite for GET /subjects/{id} endpoint."""

    def test_get_subject_success(self, client: FlaskClient, mocker, auth_headers, sample_subject_response):
        """
        Test successfully retrieving a subject by ID.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            auth_headers: Authentication headers fixture.
            sample_subject_response: Sample subject response fixture.
        """
        # Mock get_by_id method
        mock_get = mocker.patch(
            'app.services.backendless_client.BackendlessClient.get_by_id'
        )
        mock_get.return_value = sample_subject_response

        # Make request
        response = client.get(
            '/subjects/TEST123',
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 200

        data = response.get_json()
        assert data is not None
        assert data['objectId'] == 'TEST123'
        assert 'name' in data
        assert 'code' in data

        # Verify mock was called with correct ID
        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs['object_id'] == 'TEST123'

    def test_get_subject_not_found(self, client: FlaskClient, mocker, auth_headers):
        """
        Test getting non-existent subject returns 404.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            auth_headers: Authentication headers fixture.
        """
        # Mock get_by_id to raise not found error
        mock_get = mocker.patch(
            'app.services.backendless_client.BackendlessClient.get_by_id'
        )
        mock_get.side_effect = BackendlessClientError(
            message="Entity not found",
            status_code=404
        )

        # Make request
        response = client.get(
            '/subjects/NONEXISTENT',
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 404

        data = response.get_json()
        assert data is not None
        assert data['code'] == 404

    def test_get_subject_unauthorized(self, client: FlaskClient):
        """
        Test getting subject without auth token returns 401.

        Args:
            client: Flask test client fixture.
        """
        # Make request without auth headers
        response = client.get('/subjects/TEST123')

        # Assertions
        assert response.status_code == 401

        data = response.get_json()
        assert data is not None
        assert data['code'] == 401


@pytest.mark.unit
class TestUpdateSubject:
    """Test suite for PUT /subjects/{id} endpoint."""

    def test_update_subject_success(self, client: FlaskClient, mocker, auth_headers, sample_subject_response):
        """
        Test successfully updating a subject.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            auth_headers: Authentication headers fixture.
            sample_subject_response: Sample subject response fixture.
        """
        # Mock update method
        updated_response = {**sample_subject_response, 'name': 'Cálculo Avanzado I'}
        mock_update = mocker.patch(
            'app.services.backendless_client.BackendlessClient.update'
        )
        mock_update.return_value = updated_response

        # Update data
        update_data = {
            'name': 'Cálculo Avanzado I'
        }

        # Make request
        response = client.put(
            '/subjects/TEST123',
            json=update_data,
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 200

        data = response.get_json()
        assert data is not None
        assert data['objectId'] == 'TEST123'
        assert data['name'] == 'Cálculo Avanzado I'

        # Verify mock was called with correct params
        mock_update.assert_called_once()
        call_kwargs = mock_update.call_args.kwargs
        assert call_kwargs['object_id'] == 'TEST123'
        assert call_kwargs['data'] == update_data

    def test_update_subject_partial_update(self, client: FlaskClient, mocker, auth_headers, sample_subject_response):
        """
        Test partial update (only updating one field).

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            auth_headers: Authentication headers fixture.
            sample_subject_response: Sample subject response fixture.
        """
        # Mock update method
        updated_response = {**sample_subject_response, 'weeklyLoadHours': 6}
        mock_update = mocker.patch(
            'app.services.backendless_client.BackendlessClient.update'
        )
        mock_update.return_value = updated_response

        # Update only weeklyLoadHours
        update_data = {
            'weeklyLoadHours': 6
        }

        # Make request
        response = client.put(
            '/subjects/TEST123',
            json=update_data,
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 200

        data = response.get_json()
        assert data['weeklyLoadHours'] == 6

        # Verify only the updated field was sent to Backendless
        call_kwargs = mock_update.call_args.kwargs
        assert call_kwargs['data'] == {'weeklyLoadHours': 6}

    def test_update_subject_not_found(self, client: FlaskClient, mocker, auth_headers):
        """
        Test updating non-existent subject returns 404.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            auth_headers: Authentication headers fixture.
        """
        # Mock update to raise not found error
        mock_update = mocker.patch(
            'app.services.backendless_client.BackendlessClient.update'
        )
        mock_update.side_effect = BackendlessClientError(
            message="Entity not found",
            status_code=404
        )

        # Make request
        response = client.put(
            '/subjects/NONEXISTENT',
            json={'name': 'Updated Name'},
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 404

        data = response.get_json()
        assert data is not None
        assert data['code'] == 404

    def test_update_subject_invalid_data(self, client: FlaskClient, auth_headers):
        """
        Test updating subject with invalid data returns 400.

        Args:
            client: Flask test client fixture.
            auth_headers: Authentication headers fixture.
        """
        # Invalid kind value
        invalid_update = {
            'kind': 'invalid_kind'
        }

        response = client.put(
            '/subjects/TEST123',
            json=invalid_update,
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 400

        data = response.get_json()
        assert data is not None
        assert data['code'] == 400

    def test_update_subject_unauthorized(self, client: FlaskClient):
        """
        Test updating subject without auth token returns 401.

        Args:
            client: Flask test client fixture.
        """
        # Make request without auth headers
        response = client.put(
            '/subjects/TEST123',
            json={'name': 'Updated Name'}
        )

        # Assertions
        assert response.status_code == 401

        data = response.get_json()
        assert data is not None
        assert data['code'] == 401


@pytest.mark.unit
class TestDeleteSubject:
    """Test suite for DELETE /subjects/{id} endpoint."""

    def test_delete_subject_success(self, client: FlaskClient, mocker, auth_headers):
        """
        Test successfully deleting a subject.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            auth_headers: Authentication headers fixture.
        """
        # Mock delete method
        mock_delete = mocker.patch(
            'app.services.backendless_client.BackendlessClient.delete'
        )
        mock_delete.return_value = None  # Delete returns nothing

        # Make request
        response = client.delete(
            '/subjects/TEST123',
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 204

        # 204 No Content should have empty body
        assert response.data == b''

        # Verify mock was called with correct ID
        mock_delete.assert_called_once()
        call_kwargs = mock_delete.call_args.kwargs
        assert call_kwargs['object_id'] == 'TEST123'

    def test_delete_subject_not_found(self, client: FlaskClient, mocker, auth_headers):
        """
        Test deleting non-existent subject returns 404.

        Args:
            client: Flask test client fixture.
            mocker: pytest-mock mocker fixture.
            auth_headers: Authentication headers fixture.
        """
        # Mock delete to raise not found error
        mock_delete = mocker.patch(
            'app.services.backendless_client.BackendlessClient.delete'
        )
        mock_delete.side_effect = BackendlessClientError(
            message="Entity not found",
            status_code=404
        )

        # Make request
        response = client.delete(
            '/subjects/NONEXISTENT',
            headers=auth_headers
        )

        # Assertions
        assert response.status_code == 404

        data = response.get_json()
        assert data is not None
        assert data['code'] == 404

    def test_delete_subject_unauthorized(self, client: FlaskClient):
        """
        Test deleting subject without auth token returns 401.

        Args:
            client: Flask test client fixture.
        """
        # Make request without auth headers
        response = client.delete('/subjects/TEST123')

        # Assertions
        assert response.status_code == 401

        data = response.get_json()
        assert data is not None
        assert data['code'] == 401
