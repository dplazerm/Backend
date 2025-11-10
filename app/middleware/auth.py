"""
Authentication middleware module.

This module provides decorators and utilities for handling authentication
in Flask routes. It implements authentication as a cross-cutting concern,
following the Aspect-Oriented Programming principle.

Author: Equipo 46
Date: 2024
"""

from functools import wraps
from typing import Callable, Any
from flask import request, g

from app.utils.response_builder import unauthorized_response


def require_auth(f: Callable) -> Callable:
    """
    Decorator to require authentication for a route.

    This decorator checks for the presence and validity of the 'user-token'
    header in the request. If the token is missing, it returns a 401 error.

    The token is stored in Flask's g object for use within the request context.

    Args:
        f: The Flask route function to decorate.

    Returns:
        Callable: The decorated function.

    Usage:
        @app.route('/protected')
        @require_auth
        def protected_route():
            user_token = g.user_token
            # ... use token for Backendless operations

    Note:
        This decorator does NOT validate the token with Backendless.
        Token validation happens implicitly when making Backendless API calls.
        If the token is invalid, Backendless will return an error.
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        # Extract user-token from headers
        user_token = request.headers.get('user-token')

        if not user_token:
            return unauthorized_response(
                message="Token inválido o expirado"
            )

        # Store token in Flask's g object for use in the route
        g.user_token = user_token

        return f(*args, **kwargs)

    return decorated_function


def get_user_token() -> str:
    """
    Retrieves the user token from the current request context.

    This is a convenience function to access the user token stored
    by the @require_auth decorator.

    Returns:
        str: The user token from the current request.

    Raises:
        RuntimeError: If called outside a request context or before
                     authentication middleware has run.

    Example:
        @app.route('/subjects')
        @require_auth
        def list_subjects():
            token = get_user_token()
            # Use token for Backendless operations
    """
    if not hasattr(g, 'user_token'):
        raise RuntimeError(
            "User token not available. "
            "Ensure @require_auth decorator is applied to the route."
        )

    return g.user_token


def optional_auth(f: Callable) -> Callable:
    """
    Decorator for routes where authentication is optional.

    This decorator extracts the user-token if present, but does not
    require it. Useful for endpoints that can work with or without
    authentication.

    Args:
        f: The Flask route function to decorate.

    Returns:
        Callable: The decorated function.

    Usage:
        @app.route('/public-or-private')
        @optional_auth
        def flexible_route():
            token = getattr(g, 'user_token', None)
            if token:
                # Authenticated behavior
            else:
                # Anonymous behavior
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        # Extract user-token from headers (optional)
        user_token = request.headers.get('user-token')

        if user_token:
            g.user_token = user_token
        else:
            g.user_token = None

        return f(*args, **kwargs)

    return decorated_function
