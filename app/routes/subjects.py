"""
Subjects (Materias) routes module.

This module provides CRUD endpoints for managing academic subjects/courses.
It follows the Blueprint pattern for modular organization and delegates
all business logic to the service layer (BackendlessClient).

Following REST best practices and SOLID principles:
- Single Responsibility: Each route handler manages only HTTP logic
- Open/Closed: Extensible without modifying existing code
- Dependency Inversion: Depends on abstractions (Config, BackendlessClient)

Author: Equipo 46
Date: 2024
"""

from typing import Any, Dict, Tuple
from flask import Blueprint, request, Response, current_app
from pydantic import ValidationError

from app.config import get_config
from app.services.backendless_client import BackendlessClient, BackendlessClientError
from app.models.schemas import SubjectCreate, SubjectUpdate, Subject, PaginatedSubjects
from app.utils.response_builder import (
    success_response,
    created_response,
    no_content_response,
    paginated_response,
    not_found_response,
    bad_request_response
)
from app.middleware.auth import require_auth, get_user_token


# Create subjects blueprint
# URL prefix '/subjects' means all routes will be prefixed with /subjects
subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects')


@subjects_bp.route('', methods=['GET'])
@require_auth
def list_subjects() -> Tuple[Response, int]:
    """
    Lists all subjects with pagination and optional filtering.

    This endpoint retrieves a paginated list of subjects from Backendless.
    Supports filtering by code and standard pagination parameters.

    Query Parameters:
        pageSize (int, optional): Number of items per page (1-100, default: 50)
        offset (int, optional): Number of items to skip (default: 0)
        code (str, optional): Filter by exact subject code (e.g., "CALC1")

    Response (200 OK):
        {
            "total": 124,           // Total number of subjects
            "count": 10,            // Number of subjects in this page
            "offset": 0,            // Offset used for this page
            "results": [
                {
                    "objectId": "ABC123",
                    "name": "Cálculo I",
                    "code": "CALC1",
                    "kind": "class",
                    "weeklyLoadHours": 4,
                    "created": 1699564800000,
                    "updated": 1699564800000
                },
                // ... more subjects
            ]
        }

    Error Responses:
        401 Unauthorized:
            - Missing or invalid user-token header

        403 Forbidden:
            - Valid token but insufficient permissions (handled by Backendless)

        500 Internal Server Error:
            - Backendless service unavailable
            - Network error

    Returns:
        Tuple[Response, int]: JSON response with paginated subjects and 200 status.

    Note:
        - Requires authentication (user-token header)
        - pageSize is capped at 100 (Backendless limit)
        - All errors are handled by global error handler middleware

    Example:
        >>> # List first 10 subjects
        >>> GET /subjects?pageSize=10&offset=0
        >>> Headers: { "user-token": "abc123..." }

        >>> # Filter by code
        >>> GET /subjects?code=CALC1
        >>> Headers: { "user-token": "abc123..." }
    """
    # Log request
    current_app.logger.info("List subjects request received")

    # Step 1: Extract query parameters
    page_size = request.args.get('pageSize', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    code_filter = request.args.get('code', None, type=str)

    current_app.logger.debug(
        f"Pagination params - pageSize: {page_size}, offset: {offset}, code: {code_filter}"
    )

    # Step 2: Build where clause for filtering
    where_clause = None
    if code_filter:
        # Backendless uses SQL-like syntax for where clauses
        # Note: Single quotes around string values
        where_clause = f"code='{code_filter}'"
        current_app.logger.debug(f"Applying filter: {where_clause}")

    # Step 3: Get user token from context (set by @require_auth)
    user_token = get_user_token()

    # Step 4: Get configuration and create Backendless client
    config = get_config()
    backendless_client = BackendlessClient(config)

    # Step 5: Get total count of subjects (for pagination)
    total = backendless_client.count(
        table='Subjects',
        where_clause=where_clause,
        user_token=user_token
    )
    current_app.logger.debug(f"Total subjects count: {total}")

    # Step 6: Fetch subjects list from Backendless
    subjects_data = backendless_client.list(
        table='Subjects',
        page_size=page_size,
        offset=offset,
        where_clause=where_clause,
        user_token=user_token
    )

    # Step 7: Validate each subject with Pydantic schema
    # This ensures data consistency and type safety
    validated_subjects = [Subject(**subject) for subject in subjects_data]

    # Step 8: Convert to dict for JSON serialization (with aliases)
    results = [subject.model_dump(by_alias=True) for subject in validated_subjects]

    # Step 9: Return paginated response
    current_app.logger.info(
        f"Successfully retrieved {len(results)} subjects (total: {total})"
    )

    return paginated_response(
        results=results,
        total=total,
        count=len(results),
        offset=offset
    )


@subjects_bp.route('', methods=['POST'])
@require_auth
def create_subject() -> Tuple[Response, int]:
    """
    Creates a new subject.

    This endpoint creates a new subject in Backendless with the provided data.
    All fields are validated using Pydantic before creation.

    Request Body (JSON):
        {
            "name": "Cálculo I",           // Required, min length 1
            "code": "CALC1",               // Required, min length 1, must be unique
            "kind": "class",               // Required, one of: class, exam, task, project, other
            "weeklyLoadHours": 4           // Optional, integer >= 0, default: 4
        }

    Response (201 Created):
        {
            "objectId": "ABC123",          // Generated by Backendless
            "name": "Cálculo I",
            "code": "CALC1",
            "kind": "class",
            "weeklyLoadHours": 4,
            "created": 1699564800000,      // Unix timestamp in milliseconds
            "updated": 1699564800000
        }

    Error Responses:
        400 Bad Request:
            - Missing or invalid request body
            - Missing required fields (name, code)
            - Invalid field types or values
            - code already exists (unique constraint)

        401 Unauthorized:
            - Missing or invalid user-token header

        403 Forbidden:
            - Valid token but insufficient permissions

        500 Internal Server Error:
            - Backendless service unavailable
            - Network error

    Returns:
        Tuple[Response, int]: JSON response with created subject and 201 status.

    Note:
        - Requires authentication (user-token header)
        - code must be unique across all subjects
        - Validation errors return detailed field-level error messages
        - All errors are handled by global error handler middleware

    Example:
        >>> POST /subjects
        >>> Headers: { "user-token": "abc123...", "Content-Type": "application/json" }
        >>> Body: {
        >>>     "name": "Cálculo I",
        >>>     "code": "CALC1",
        >>>     "kind": "class",
        >>>     "weeklyLoadHours": 4
        >>> }
    """
    # Log request
    current_app.logger.info("Create subject request received")

    # Step 1: Extract and validate request body
    request_data = request.get_json()
    if request_data is None:
        current_app.logger.warning("Invalid request body: not valid JSON")
        return bad_request_response(
            message="Solicitud inválida",
            details="Request body must be valid JSON"
        )

    # Step 2: Validate with Pydantic schema
    # ValidationError will be caught by global error handler
    validated_request = SubjectCreate(**request_data)
    current_app.logger.debug(
        f"Creating subject with code: {validated_request.code}"
    )

    # Step 3: Get user token from context
    user_token = get_user_token()

    # Step 4: Get configuration and create Backendless client
    config = get_config()
    backendless_client = BackendlessClient(config)

    # Step 5: Create subject in Backendless
    # Convert Pydantic model to dict for Backendless
    subject_data = validated_request.model_dump()

    created_subject = backendless_client.create(
        table='Subjects',
        data=subject_data,
        user_token=user_token
    )

    # Step 6: Validate response from Backendless
    validated_response = Subject(**created_subject)

    # Step 7: Return created response (201)
    response_data = validated_response.model_dump(by_alias=True)

    current_app.logger.info(
        f"Subject created successfully with objectId: {validated_response.objectId}"
    )

    return created_response(response_data)


@subjects_bp.route('/<string:id>', methods=['GET'])
@require_auth
def get_subject(id: str) -> Tuple[Response, int]:
    """
    Retrieves a single subject by its objectId.

    This endpoint fetches a specific subject from Backendless using its
    unique objectId.

    Path Parameters:
        id (str): The objectId of the subject to retrieve

    Response (200 OK):
        {
            "objectId": "ABC123",
            "name": "Cálculo I",
            "code": "CALC1",
            "kind": "class",
            "weeklyLoadHours": 4,
            "created": 1699564800000,
            "updated": 1699564800000
        }

    Error Responses:
        404 Not Found:
            - Subject with the given objectId does not exist

        401 Unauthorized:
            - Missing or invalid user-token header

        403 Forbidden:
            - Valid token but insufficient permissions

        500 Internal Server Error:
            - Backendless service unavailable
            - Network error

    Returns:
        Tuple[Response, int]: JSON response with subject data and 200 status.

    Note:
        - Requires authentication (user-token header)
        - objectId must be a valid Backendless object identifier
        - 404 error is automatically handled by Backendless/error handler

    Example:
        >>> GET /subjects/ABC123
        >>> Headers: { "user-token": "abc123..." }
    """
    # Log request
    current_app.logger.info(f"Get subject request received for objectId: {id}")

    # Step 1: Get user token from context
    user_token = get_user_token()

    # Step 2: Get configuration and create Backendless client
    config = get_config()
    backendless_client = BackendlessClient(config)

    # Step 3: Fetch subject from Backendless
    # BackendlessClientError with 404 will be caught by global error handler
    subject_data = backendless_client.get_by_id(
        table='Subjects',
        object_id=id,
        user_token=user_token
    )

    # Step 4: Validate response with Pydantic schema
    validated_subject = Subject(**subject_data)

    # Step 5: Return success response
    response_data = validated_subject.model_dump(by_alias=True)

    current_app.logger.info(f"Subject retrieved successfully: {validated_subject.code}")

    return success_response(response_data, status=200)


@subjects_bp.route('/<string:id>', methods=['PUT'])
@require_auth
def update_subject(id: str) -> Tuple[Response, int]:
    """
    Updates an existing subject.

    This endpoint updates a subject in Backendless with the provided data.
    All fields are optional (partial update supported). Only provided fields
    will be updated.

    Path Parameters:
        id (str): The objectId of the subject to update

    Request Body (JSON):
        {
            "name": "Cálculo Avanzado I",  // Optional
            "code": "CALC1-ADV",           // Optional
            "kind": "exam",                // Optional
            "weeklyLoadHours": 6           // Optional
        }

    Note: At least one field should be provided for update.

    Response (200 OK):
        {
            "objectId": "ABC123",
            "name": "Cálculo Avanzado I",  // Updated fields
            "code": "CALC1-ADV",
            "kind": "exam",
            "weeklyLoadHours": 6,
            "created": 1699564800000,
            "updated": 1699578000000       // Updated timestamp
        }

    Error Responses:
        400 Bad Request:
            - Invalid request body
            - Invalid field types or values
            - code already exists (if updating code to existing one)

        404 Not Found:
            - Subject with the given objectId does not exist

        401 Unauthorized:
            - Missing or invalid user-token header

        403 Forbidden:
            - Valid token but insufficient permissions

        500 Internal Server Error:
            - Backendless service unavailable
            - Network error

    Returns:
        Tuple[Response, int]: JSON response with updated subject and 200 status.

    Note:
        - Requires authentication (user-token header)
        - Partial updates supported (only send fields to update)
        - Empty update body is technically valid but does nothing
        - All errors are handled by global error handler middleware

    Example:
        >>> PUT /subjects/ABC123
        >>> Headers: { "user-token": "abc123...", "Content-Type": "application/json" }
        >>> Body: {
        >>>     "name": "Cálculo Avanzado I",
        >>>     "weeklyLoadHours": 6
        >>> }
    """
    # Log request
    current_app.logger.info(f"Update subject request received for objectId: {id}")

    # Step 1: Extract and validate request body
    request_data = request.get_json()
    if request_data is None:
        current_app.logger.warning("Invalid request body: not valid JSON")
        return bad_request_response(
            message="Solicitud inválida",
            details="Request body must be valid JSON"
        )

    # Step 2: Validate with Pydantic schema (allows partial updates)
    # ValidationError will be caught by global error handler
    validated_request = SubjectUpdate(**request_data)
    current_app.logger.debug(f"Updating subject {id} with data: {request_data}")

    # Step 3: Get user token from context
    user_token = get_user_token()

    # Step 4: Get configuration and create Backendless client
    config = get_config()
    backendless_client = BackendlessClient(config)

    # Step 5: Update subject in Backendless
    # Only send fields that were provided (exclude None values)
    update_data = validated_request.model_dump(exclude_none=True)

    updated_subject = backendless_client.update(
        table='Subjects',
        object_id=id,
        data=update_data,
        user_token=user_token
    )

    # Step 6: Validate response from Backendless
    validated_response = Subject(**updated_subject)

    # Step 7: Return success response
    response_data = validated_response.model_dump(by_alias=True)

    current_app.logger.info(f"Subject updated successfully: {validated_response.code}")

    return success_response(response_data, status=200)


@subjects_bp.route('/<string:id>', methods=['DELETE'])
@require_auth
def delete_subject(id: str) -> Tuple[str, int]:
    """
    Deletes a subject by its objectId.

    This endpoint permanently removes a subject from Backendless.
    The operation is irreversible.

    Path Parameters:
        id (str): The objectId of the subject to delete

    Response (204 No Content):
        No response body. Status code 204 indicates successful deletion.

    Error Responses:
        404 Not Found:
            - Subject with the given objectId does not exist

        401 Unauthorized:
            - Missing or invalid user-token header

        403 Forbidden:
            - Valid token but insufficient permissions

        500 Internal Server Error:
            - Backendless service unavailable
            - Network error

    Returns:
        Tuple[str, int]: Empty response with 204 status.

    Note:
        - Requires authentication (user-token header)
        - Operation is irreversible
        - Returns 204 even if subject was already deleted (idempotent)
        - All errors are handled by global error handler middleware

    Warning:
        This operation permanently deletes the subject. Consider implementing
        soft delete (marking as inactive) if you need to maintain history.

    Example:
        >>> DELETE /subjects/ABC123
        >>> Headers: { "user-token": "abc123..." }
        >>> Response: 204 No Content (empty body)
    """
    # Log request
    current_app.logger.info(f"Delete subject request received for objectId: {id}")

    # Step 1: Get user token from context
    user_token = get_user_token()

    # Step 2: Get configuration and create Backendless client
    config = get_config()
    backendless_client = BackendlessClient(config)

    # Step 3: Delete subject from Backendless
    # BackendlessClientError with 404 will be caught by global error handler
    backendless_client.delete(
        table='Subjects',
        object_id=id,
        user_token=user_token
    )

    # Step 4: Return no content response (204)
    current_app.logger.info(f"Subject deleted successfully: {id}")

    return no_content_response()
