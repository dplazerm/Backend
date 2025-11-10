"""
Configuration module for the Flask application.

This module implements the Single Responsibility Principle by handling
only application configuration. It provides different configuration
classes for different environments (development, testing, production).

Author: Equipo 46
Date: 2024
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Base configuration class.

    Contains common configuration settings shared across all environments.
    Uses environment variables for sensitive data to follow security best practices.
    """

    # Flask Configuration
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG: bool = False
    TESTING: bool = False

    # Server Configuration
    PORT: int = int(os.getenv('PORT', 8000))

    # Backendless Configuration
    BACKENDLESS_APP_ID: Optional[str] = os.getenv('BACKENDLESS_APP_ID')
    BACKENDLESS_REST_API_KEY: Optional[str] = os.getenv('BACKENDLESS_REST_API_KEY')
    BACKENDLESS_BASE_URL: str = os.getenv('BACKENDLESS_BASE_URL', 'https://api.backendless.com')

    # CORS Configuration
    CORS_ORIGINS: list = ['http://localhost:3000', 'http://localhost:8000']

    @classmethod
    def validate(cls) -> None:
        """
        Validates that all required configuration variables are set.

        Raises:
            ValueError: If any required configuration variable is missing.
        """
        required_vars = [
            ('BACKENDLESS_APP_ID', cls.BACKENDLESS_APP_ID),
            ('BACKENDLESS_REST_API_KEY', cls.BACKENDLESS_REST_API_KEY),
        ]

        missing_vars = [var_name for var_name, var_value in required_vars if not var_value]

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                f"Please check your .env file."
            )

    @property
    def backendless_base_path(self) -> str:
        """
        Constructs the base path for Backendless API calls.

        Returns:
            str: The complete base URL for Backendless API operations.
        """
        return f"{self.BACKENDLESS_BASE_URL}/{self.BACKENDLESS_APP_ID}/{self.BACKENDLESS_REST_API_KEY}"


class DevelopmentConfig(Config):
    """
    Development environment configuration.

    Enables debug mode and verbose logging for development purposes.
    """
    DEBUG: bool = True
    FLASK_ENV: str = 'development'


class TestingConfig(Config):
    """
    Testing environment configuration.

    Enables testing mode and uses in-memory databases when applicable.
    """
    TESTING: bool = True
    DEBUG: bool = True


class ProductionConfig(Config):
    """
    Production environment configuration.

    Disables debug mode and enforces strict security settings.
    """
    DEBUG: bool = False
    FLASK_ENV: str = 'production'

    # Override CORS for production (should be configured with actual frontend URL)
    # TODO: Update with actual production frontend URL
    CORS_ORIGINS: list = ['https://your-production-frontend.com']


# Configuration dictionary for easy access
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: Optional[str] = None) -> Config:
    """
    Factory function to get the appropriate configuration object.

    Args:
        config_name: Name of the configuration to use. If None, uses FLASK_ENV
                    environment variable or defaults to 'development'.

    Returns:
        Config: The appropriate configuration object.
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    config_class = config_by_name.get(config_name, DevelopmentConfig)
    config = config_class()
    config.validate()

    return config
