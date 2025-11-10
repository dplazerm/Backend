"""
Response builder utility module.

This module provides utility functions to build standardized JSON responses
following the DRY (Don't Repeat Yourself) principle. All API responses
should use these builders to ensure consistency.

Author: Equipo 46
Date: 2024
"""

from typing import Any, Dict, Optional
from flask import jsonify, Response


def success_response(data: Any, status: int = 200) -> tuple[Response, int]:
    """
    Builds a successful JSON response.

    Args:
        data: The data to include in the response body.
        status: HTTP status code (default: 200).

    Returns:
        tuple: A tuple containing the JSON response and status code.

    Example:
        >>> success_response({"name": "John"}, 200)
        ({'name': 'John'}, 200)
    """
    return jsonify(data), status


def error_response(
    message: str,
    code: int,
    details: Optional[str] = None
) -> tuple[Response, int]:
    """
    Builds an error JSON response following the OpenAPI contract.

    Args:
        message: A human-readable error message.
        code: HTTP status code.
        details: Optional additional details about the error.

    Returns:
        tuple: A tuple containing the JSON response and status code.

    Example:
        >>> error_response("Invalid request", 400, "Missing 'name' field")
        ({'message': 'Invalid request', 'code': 400, 'details': "Missing 'name' field"}, 400)
    """
    error_body: Dict[str, Any] = {
        "message": message,
        "code": code
    }

    if details:
        error_body["details"] = details

    return jsonify(error_body), code


def paginated_response(
    results: list,
    total: int,
    count: int,
    offset: int,
    status: int = 200
) -> tuple[Response, int]:
    """
    Builds a paginated JSON response following the OpenAPI contract.

    This response format is used for list operations that support pagination.

    Args:
        results: List of items for the current page.
        total: Total number of items available.
        count: Number of items in the current page.
        offset: Offset used for this page.
        status: HTTP status code (default: 200).

    Returns:
        tuple: A tuple containing the JSON response and status code.

    Example:
        >>> paginated_response([{"id": 1}, {"id": 2}], 100, 2, 0)
        ({'total': 100, 'count': 2, 'offset': 0, 'results': [...]}, 200)
    """
    response_body = {
        "total": total,
        "count": count,
        "offset": offset,
        "results": results
    }

    return jsonify(response_body), status


def created_response(data: Any) -> tuple[Response, int]:
    """
    Builds a response for successful resource creation (201).

    Args:
        data: The created resource data.

    Returns:
        tuple: A tuple containing the JSON response and 201 status code.

    Example:
        >>> created_response({"id": 1, "name": "New Item"})
        ({'id': 1, 'name': 'New Item'}, 201)
    """
    return success_response(data, status=201)


def no_content_response() -> tuple[str, int]:
    """
    Builds a response for successful operations with no content (204).

    Commonly used for DELETE operations.

    Returns:
        tuple: An empty response with 204 status code.

    Example:
        >>> no_content_response()
        ('', 204)
    """
    return '', 204


def unauthorized_response(message: str = "Token inválido o expirado") -> tuple[Response, int]:
    """
    Builds an unauthorized error response (401).

    Args:
        message: Custom error message (default: "Token inválido o expirado").

    Returns:
        tuple: A tuple containing the JSON response and 401 status code.
    """
    return error_response(message, 401)


def forbidden_response(message: str = "Acceso denegado") -> tuple[Response, int]:
    """
    Builds a forbidden error response (403).

    Args:
        message: Custom error message (default: "Acceso denegado").

    Returns:
        tuple: A tuple containing the JSON response and 403 status code.
    """
    return error_response(message, 403)


def not_found_response(message: str = "No encontrado") -> tuple[Response, int]:
    """
    Builds a not found error response (404).

    Args:
        message: Custom error message (default: "No encontrado").

    Returns:
        tuple: A tuple containing the JSON response and 404 status code.
    """
    return error_response(message, 404)


def bad_request_response(
    message: str = "Solicitud inválida",
    details: Optional[str] = None
) -> tuple[Response, int]:
    """
    Builds a bad request error response (400).

    Args:
        message: Custom error message (default: "Solicitud inválida").
        details: Optional additional details about what's wrong.

    Returns:
        tuple: A tuple containing the JSON response and 400 status code.
    """
    return error_response(message, 400, details)
