"""
Backendless API client service.

This module provides a clean interface to interact with Backendless REST API.
It implements the Single Responsibility Principle by focusing only on
API communication, and Dependency Inversion by abstracting the external service.

Author: Equipo 46
Date: 2024
"""

import requests
from typing import Any, Dict, Optional, List
from requests.exceptions import RequestException, Timeout, ConnectionError

from app.config import Config


class BackendlessClientError(Exception):
    """Custom exception for Backendless client errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, details: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class BackendlessClient:
    """
    Client for interacting with Backendless REST API.

    This client provides methods for authentication and CRUD operations
    on Backendless data tables, abstracting away the HTTP details.

    Attributes:
        config: Application configuration object containing Backendless credentials.
        base_url: Base URL for all Backendless API calls.
        timeout: Timeout in seconds for HTTP requests.
    """

    def __init__(self, config: Config, timeout: int = 30):
        """
        Initializes the Backendless client.

        Args:
            config: Application configuration object.
            timeout: Request timeout in seconds (default: 30).

        Raises:
            ValueError: If required configuration is missing.
        """
        self.config = config
        self.base_url = config.backendless_base_path
        self.timeout = timeout
        self._validate_config()

    def _validate_config(self) -> None:
        """
        Validates that required configuration is present.

        Raises:
            ValueError: If APP_ID or REST_API_KEY is missing.
        """
        if not self.config.BACKENDLESS_APP_ID or not self.config.BACKENDLESS_REST_API_KEY:
            raise ValueError("Backendless APP_ID and REST_API_KEY are required")

    def _build_headers(self, user_token: Optional[str] = None) -> Dict[str, str]:
        """
        Builds HTTP headers for Backendless requests.

        Args:
            user_token: Optional authentication token for authenticated requests.

        Returns:
            Dict: HTTP headers dictionary.
        """
        headers = {
            "Content-Type": "application/json"
        }

        if user_token:
            headers["user-token"] = user_token

        return headers

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handles HTTP response and error cases.

        Args:
            response: The HTTP response object.

        Returns:
            Any: Parsed JSON response data.

        Raises:
            BackendlessClientError: If the response indicates an error.
        """
        try:
            response_data = response.json() if response.content else {}
        except ValueError:
            response_data = {}

        if response.status_code >= 400:
            error_message = response_data.get('message', 'Unknown error occurred')
            error_code = response_data.get('code', response.status_code)
            raise BackendlessClientError(
                message=error_message,
                status_code=error_code,
                details=str(response_data)
            )

        return response_data

    # ========================================================================
    # Authentication Methods
    # ========================================================================

    def login(self, login: str, password: str) -> Dict[str, Any]:
        """
        Authenticates a user with Backendless.

        Args:
            login: User email or username.
            password: User password.

        Returns:
            Dict: User data including user-token, objectId, and email.

        Raises:
            BackendlessClientError: If authentication fails.

        Example:
            >>> client.login("user@example.com", "password123")
            {'user-token': 'abc123', 'objectId': '123', 'email': 'user@example.com'}
        """
        url = f"{self.base_url}/users/login"
        payload = {
            "login": login,
            "password": password
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self._build_headers(),
                timeout=self.timeout
            )
            return self._handle_response(response)
        except (Timeout, ConnectionError) as e:
            raise BackendlessClientError(
                message="Failed to connect to Backendless",
                details=str(e)
            )
        except RequestException as e:
            raise BackendlessClientError(
                message="Error during authentication",
                details=str(e)
            )

    # ========================================================================
    # CRUD Methods
    # ========================================================================

    def create(self, table: str, data: Dict[str, Any], user_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Creates a new object in a Backendless table.

        Args:
            table: Name of the table.
            data: Object data to create.
            user_token: Optional authentication token.

        Returns:
            Dict: Created object with objectId assigned.

        Raises:
            BackendlessClientError: If creation fails.

        Example:
            >>> client.create("Subjects", {"name": "Math", "code": "MATH101"}, token)
            {'objectId': '123', 'name': 'Math', 'code': 'MATH101'}
        """
        url = f"{self.base_url}/data/{table}"

        try:
            response = requests.post(
                url,
                json=data,
                headers=self._build_headers(user_token),
                timeout=self.timeout
            )
            return self._handle_response(response)
        except (Timeout, ConnectionError) as e:
            raise BackendlessClientError(
                message="Failed to connect to Backendless",
                details=str(e)
            )
        except RequestException as e:
            raise BackendlessClientError(
                message=f"Error creating object in {table}",
                details=str(e)
            )

    def get_by_id(self, table: str, object_id: str, user_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves a single object by its objectId.

        Args:
            table: Name of the table.
            object_id: The objectId of the object to retrieve.
            user_token: Optional authentication token.

        Returns:
            Dict: The retrieved object.

        Raises:
            BackendlessClientError: If retrieval fails or object not found.

        Example:
            >>> client.get_by_id("Subjects", "ABC123", token)
            {'objectId': 'ABC123', 'name': 'Math', 'code': 'MATH101'}
        """
        url = f"{self.base_url}/data/{table}/{object_id}"

        try:
            response = requests.get(
                url,
                headers=self._build_headers(user_token),
                timeout=self.timeout
            )
            return self._handle_response(response)
        except (Timeout, ConnectionError) as e:
            raise BackendlessClientError(
                message="Failed to connect to Backendless",
                details=str(e)
            )
        except RequestException as e:
            raise BackendlessClientError(
                message=f"Error retrieving object from {table}",
                details=str(e)
            )

    def list(
        self,
        table: str,
        page_size: int = 50,
        offset: int = 0,
        where_clause: Optional[str] = None,
        user_token: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Lists objects from a Backendless table with pagination.

        Args:
            table: Name of the table.
            page_size: Number of items per page (max 100).
            offset: Number of items to skip.
            where_clause: Optional SQL-like where clause for filtering.
            user_token: Optional authentication token.

        Returns:
            List: List of objects from the table.

        Raises:
            BackendlessClientError: If listing fails.

        Example:
            >>> client.list("Subjects", page_size=10, offset=0, token)
            [{'objectId': '1', 'name': 'Math'}, {'objectId': '2', 'name': 'Physics'}]
        """
        # Validate page_size (Backendless max is 100)
        page_size = min(max(1, page_size), 100)
        offset = max(0, offset)

        url = f"{self.base_url}/data/{table}"
        params = {
            "pageSize": page_size,
            "offset": offset
        }

        if where_clause:
            params["where"] = where_clause

        try:
            response = requests.get(
                url,
                params=params,
                headers=self._build_headers(user_token),
                timeout=self.timeout
            )
            return self._handle_response(response)
        except (Timeout, ConnectionError) as e:
            raise BackendlessClientError(
                message="Failed to connect to Backendless",
                details=str(e)
            )
        except RequestException as e:
            raise BackendlessClientError(
                message=f"Error listing objects from {table}",
                details=str(e)
            )

    def update(
        self,
        table: str,
        object_id: str,
        data: Dict[str, Any],
        user_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Updates an existing object in a Backendless table.

        Args:
            table: Name of the table.
            object_id: The objectId of the object to update.
            data: Updated object data.
            user_token: Optional authentication token.

        Returns:
            Dict: Updated object.

        Raises:
            BackendlessClientError: If update fails.

        Example:
            >>> client.update("Subjects", "ABC123", {"name": "Advanced Math"}, token)
            {'objectId': 'ABC123', 'name': 'Advanced Math', 'code': 'MATH101'}
        """
        url = f"{self.base_url}/data/{table}/{object_id}"

        try:
            response = requests.put(
                url,
                json=data,
                headers=self._build_headers(user_token),
                timeout=self.timeout
            )
            return self._handle_response(response)
        except (Timeout, ConnectionError) as e:
            raise BackendlessClientError(
                message="Failed to connect to Backendless",
                details=str(e)
            )
        except RequestException as e:
            raise BackendlessClientError(
                message=f"Error updating object in {table}",
                details=str(e)
            )

    def delete(self, table: str, object_id: str, user_token: Optional[str] = None) -> None:
        """
        Deletes an object from a Backendless table.

        Args:
            table: Name of the table.
            object_id: The objectId of the object to delete.
            user_token: Optional authentication token.

        Raises:
            BackendlessClientError: If deletion fails.

        Example:
            >>> client.delete("Subjects", "ABC123", token)
        """
        url = f"{self.base_url}/data/{table}/{object_id}"

        try:
            response = requests.delete(
                url,
                headers=self._build_headers(user_token),
                timeout=self.timeout
            )
            # For delete, we don't expect a response body
            if response.status_code >= 400:
                self._handle_response(response)
        except (Timeout, ConnectionError) as e:
            raise BackendlessClientError(
                message="Failed to connect to Backendless",
                details=str(e)
            )
        except RequestException as e:
            raise BackendlessClientError(
                message=f"Error deleting object from {table}",
                details=str(e)
            )

    def count(self, table: str, where_clause: Optional[str] = None, user_token: Optional[str] = None) -> int:
        """
        Counts objects in a Backendless table.

        Args:
            table: Name of the table.
            where_clause: Optional SQL-like where clause for filtering.
            user_token: Optional authentication token.

        Returns:
            int: Count of objects.

        Raises:
            BackendlessClientError: If count operation fails.

        Example:
            >>> client.count("Subjects", token)
            42
        """
        url = f"{self.base_url}/data/{table}/count"
        params = {}

        if where_clause:
            params["where"] = where_clause

        try:
            response = requests.get(
                url,
                params=params,
                headers=self._build_headers(user_token),
                timeout=self.timeout
            )
            return self._handle_response(response)
        except (Timeout, ConnectionError) as e:
            raise BackendlessClientError(
                message="Failed to connect to Backendless",
                details=str(e)
            )
        except RequestException as e:
            raise BackendlessClientError(
                message=f"Error counting objects in {table}",
                details=str(e)
            )
