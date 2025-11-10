"""
Global error handling middleware.

This module provides centralized error handling for the Flask application.
It ensures consistent error responses across all endpoints and proper
logging of errors for debugging.

Author: Equipo 46
Date: 2024
"""

import logging
from typing import Union, Tuple
from flask import Flask, Response
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from app.utils.response_builder import error_response
from app.services.backendless_client import BackendlessClientError

# Configure logging
logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """
    Registers global error handlers for the Flask application.

    This function should be called during application initialization
    to set up consistent error handling across all routes.

    Args:
        app: The Flask application instance.

    Example:
        app = Flask(__name__)
        register_error_handlers(app)
    """

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError) -> Tuple[Response, int]:
        """
        Handles Pydantic validation errors.

        When request data fails Pydantic validation, this handler
        formats the validation errors into a user-friendly response.

        Args:
            error: The Pydantic ValidationError instance.

        Returns:
            Tuple: Error response and 400 status code.
        """
        logger.warning(f"Validation error: {error}")

        # Extract first error message for simplicity
        errors = error.errors()
        first_error = errors[0] if errors else {}
        field = first_error.get('loc', ['unknown'])[0]
        message = first_error.get('msg', 'Validation error')

        return error_response(
            message="Parámetros inválidos",
            code=400,
            details=f"Campo '{field}': {message}"
        )

    @app.errorhandler(BackendlessClientError)
    def handle_backendless_error(error: BackendlessClientError) -> Tuple[Response, int]:
        """
        Handles errors from Backendless API calls.

        Maps Backendless errors to appropriate HTTP status codes
        and user-friendly messages.

        Args:
            error: The BackendlessClientError instance.

        Returns:
            Tuple: Error response and appropriate status code.
        """
        status_code = error.status_code or 500

        # Log error for debugging
        if status_code >= 500:
            logger.error(f"Backendless server error: {error.message} - {error.details}")
        else:
            logger.warning(f"Backendless client error: {error.message}")

        # Map common Backendless error codes
        if status_code == 404 or "not found" in error.message.lower():
            return error_response(
                message="No encontrado",
                code=404,
                details=error.message
            )
        elif status_code == 401 or "invalid" in error.message.lower():
            return error_response(
                message="Token inválido o expirado",
                code=401,
                details=error.message
            )
        elif status_code == 403:
            return error_response(
                message="Acceso denegado",
                code=403,
                details=error.message
            )
        else:
            return error_response(
                message=error.message or "Error en el servidor",
                code=status_code,
                details=error.details
            )

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException) -> Tuple[Response, int]:
        """
        Handles standard HTTP exceptions from Flask/Werkzeug.

        Args:
            error: The HTTPException instance.

        Returns:
            Tuple: Error response and status code from exception.
        """
        logger.warning(f"HTTP exception: {error.code} - {error.description}")

        return error_response(
            message=error.description or "Error en la solicitud",
            code=error.code or 500
        )

    @app.errorhandler(ValueError)
    def handle_value_error(error: ValueError) -> Tuple[Response, int]:
        """
        Handles ValueError exceptions.

        These typically occur from invalid input data or configuration issues.

        Args:
            error: The ValueError instance.

        Returns:
            Tuple: Error response and 400 status code.
        """
        logger.warning(f"Value error: {str(error)}")

        return error_response(
            message="Parámetros inválidos",
            code=400,
            details=str(error)
        )

    @app.errorhandler(KeyError)
    def handle_key_error(error: KeyError) -> Tuple[Response, int]:
        """
        Handles KeyError exceptions.

        These typically occur when required data is missing from requests
        or responses.

        Args:
            error: The KeyError instance.

        Returns:
            Tuple: Error response and 400 status code.
        """
        logger.warning(f"Key error: {str(error)}")

        return error_response(
            message="Datos faltantes",
            code=400,
            details=f"Campo requerido faltante: {str(error)}"
        )

    @app.errorhandler(404)
    def handle_not_found(error: Union[HTTPException, Exception]) -> Tuple[Response, int]:
        """
        Handles 404 Not Found errors.

        Args:
            error: The error instance.

        Returns:
            Tuple: Error response and 404 status code.
        """
        return error_response(
            message="No encontrado",
            code=404,
            details="El recurso solicitado no existe"
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error: Union[HTTPException, Exception]) -> Tuple[Response, int]:
        """
        Handles 405 Method Not Allowed errors.

        Args:
            error: The error instance.

        Returns:
            Tuple: Error response and 405 status code.
        """
        return error_response(
            message="Método no permitido",
            code=405,
            details="El método HTTP usado no está permitido para este endpoint"
        )

    @app.errorhandler(500)
    def handle_internal_error(error: Exception) -> Tuple[Response, int]:
        """
        Handles 500 Internal Server Error.

        This is a catch-all for unexpected errors. Logs the full error
        for debugging but returns a generic message to the client.

        Args:
            error: The exception instance.

        Returns:
            Tuple: Error response and 500 status code.
        """
        logger.error(f"Internal server error: {str(error)}", exc_info=True)

        return error_response(
            message="Error interno del servidor",
            code=500,
            details="Ha ocurrido un error inesperado. Por favor, intente más tarde."
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> Tuple[Response, int]:
        """
        Catch-all handler for any unhandled exceptions.

        Args:
            error: The exception instance.

        Returns:
            Tuple: Error response and 500 status code.
        """
        logger.error(f"Unexpected error: {str(error)}", exc_info=True)

        return error_response(
            message="Error inesperado",
            code=500,
            details="Ha ocurrido un error inesperado. Por favor, contacte al administrador."
        )
