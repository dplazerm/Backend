"""
Authentication routes module.

This module provides authentication-related endpoints, specifically
user login functionality using Backendless as the authentication provider.

Following REST best practices and the Single Responsibility Principle,
this module only handles HTTP request/response logic, delegating business
logic to the service layer (BackendlessClient).

Author: Equipo 46
Date: 2024
"""

from typing import Any, Dict, Tuple
from flask import Blueprint, request, Response, current_app
from pydantic import ValidationError

from app.config import get_config
from app.services.backendless_client import BackendlessClient, BackendlessClientError
from app.models.schemas import UserLoginRequest, UserLoginResponse
from app.utils.response_builder import success_response, bad_request_response


# Create authentication blueprint
# URL prefix '/auth' means all routes in this blueprint will be prefixed with /auth
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login() -> Tuple[Response, int]:
    """
    Authenticates a user and returns an authentication token.

    This endpoint handles user login by validating credentials against
    Backendless authentication service. On successful authentication,
    it returns a user token that must be included in subsequent requests
    as the 'user-token' header.

    Request Body (JSON):
        {
            "login": "user@example.com",  // Email or username
            "password": "userpassword"     // User password
        }

    Response (200 OK):
        {
            "user-token": "abc123xyz...",  // Authentication token
            "objectId": "USER123",         // User's unique identifier
            "email": "user@example.com"    // User's email address
        }

    Error Responses:
        400 Bad Request:
            - Missing or invalid request body
            - Missing required fields (login or password)

        401 Unauthorized:
            - Invalid credentials
            - User not found
            - Authentication failed

        500 Internal Server Error:
            - Backendless service unavailable
            - Network error

    Returns:
        Tuple[Response, int]: JSON response and HTTP status code.

    Note:
        All errors are handled by the global error handler middleware,
        which ensures consistent error response format across the API.

    Example:
        >>> # Successful login
        >>> POST /auth/login
        >>> {
        >>>     "login": "user@example.com",
        >>>     "password": "password123"
        >>> }
        >>> # Response: 200 OK
        >>> {
        >>>     "user-token": "abc123...",
        >>>     "objectId": "USER123",
        >>>     "email": "user@example.com"
        >>> }

        >>> # Invalid credentials
        >>> POST /auth/login
        >>> {
        >>>     "login": "wrong@example.com",
        >>>     "password": "wrongpass"
        >>> }
        >>> # Response: 401 Unauthorized
        >>> {
        >>>     "message": "Token inválido o expirado",
        >>>     "code": 401,
        >>>     "details": "Invalid login or password"
        >>> }
    """
    # Log incoming login attempt (without sensitive data)
    current_app.logger.info("Login attempt received")

    # Step 1: Extract and validate request body
    request_data = request.get_json()

    if request_data is None:
        # Request body is missing or not valid JSON
        current_app.logger.warning("Login attempt with missing or invalid JSON body")
        return bad_request_response(
            message="Solicitud inválida",
            details="Request body must be valid JSON"
        )

    # Step 2: Validate request data with Pydantic schema
    # ValidationError will be caught by global error handler if validation fails
    try:
        validated_request = UserLoginRequest(**request_data)
        current_app.logger.debug(f"Login request validated for user: {validated_request.login}")
    except ValidationError as e:
        # Log validation error
        current_app.logger.warning(f"Login request validation failed: {e}")
        # Re-raise to let global error handler format the response
        raise

    # Step 3: Get application configuration
    config = get_config()

    # Step 4: Create Backendless client instance
    # Following Dependency Injection principle - config is injected
    backendless_client = BackendlessClient(config)

    # Step 5: Attempt authentication with Backendless
    # BackendlessClientError will be caught by global error handler if authentication fails
    try:
        # Call Backendless authentication service
        auth_response = backendless_client.login(
            login=validated_request.login,
            password=validated_request.password
        )
        current_app.logger.info(f"User authenticated successfully: {validated_request.login}")
    except BackendlessClientError as e:
        # Log authentication failure
        current_app.logger.warning(f"Authentication failed for user {validated_request.login}: {e.message}")
        # Re-raise to let global error handler format the response
        raise

    # Step 6: Validate Backendless response with response schema
    # This ensures the response from Backendless matches our expected format
    try:
        validated_response = UserLoginResponse(**auth_response)
    except ValidationError as e:
        # This should rarely happen, but we handle it for robustness
        current_app.logger.error(f"Backendless response validation failed: {e}")
        # Re-raise to let global error handler format the response
        raise

    # Step 7: Return successful response
    # Use model_dump with by_alias=True to ensure 'user-token' is used instead of 'user_token'
    response_data = validated_response.model_dump(by_alias=True)

    current_app.logger.info(f"Login successful for user: {validated_response.email}")

    return success_response(response_data, status=200)


# Additional authentication endpoints can be added here in the future
# Examples:
# - POST /auth/logout - Logout user
# - POST /auth/register - Register new user
# - POST /auth/reset-password - Password reset
# - GET /auth/validate - Validate current token

# NOTE: These are for future implementation and are not part of Phase 2
