"""
Flask application factory.

This module implements the Application Factory pattern for creating
Flask application instances. This pattern provides flexibility for
testing, multiple environments, and better code organization.

Author: Equipo 46
Date: 2024
"""

import logging
from flask import Flask
from flask_cors import CORS

from app.config import get_config, Config
from app.middleware.error_handler import register_error_handlers


def create_app(config_name: str = None) -> Flask:
    """
    Application factory function.

    Creates and configures a Flask application instance using the
    Factory pattern. This allows for better testability and the
    ability to create multiple application instances with different
    configurations.

    Args:
        config_name: Name of the configuration to use ('development',
                    'testing', 'production'). If None, uses FLASK_ENV
                    environment variable.

    Returns:
        Flask: Configured Flask application instance.

    Example:
        # Create development app
        app = create_app('development')

        # Create testing app
        test_app = create_app('testing')

    Raises:
        ValueError: If required configuration is missing.
    """
    # Create Flask app instance
    app = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)

    # Configure logging
    _configure_logging(app, config)

    # Initialize CORS
    CORS(app, origins=config.CORS_ORIGINS, supports_credentials=True)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    _register_blueprints(app)

    # Log successful initialization
    app.logger.info(f"Application initialized with {config.__class__.__name__}")

    return app


def _configure_logging(app: Flask, config: Config) -> None:
    """
    Configures application logging.

    Sets up logging format, level, and handlers based on the
    application configuration.

    Args:
        app: Flask application instance.
        config: Application configuration object.
    """
    # Set logging level based on debug mode
    log_level = logging.DEBUG if config.DEBUG else logging.INFO

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Set Flask app logger level
    app.logger.setLevel(log_level)

    # Log configuration loaded
    app.logger.info(f"Logging configured at {logging.getLevelName(log_level)} level")


def _register_blueprints(app: Flask) -> None:
    """
    Registers all application blueprints.

    Blueprints organize the application into modular components,
    following the Separation of Concerns principle.

    Args:
        app: Flask application instance.

    Note:
        Import blueprints inside this function to avoid circular imports.
        This is a common pattern in Flask applications.
    """
    # Import blueprints here to avoid circular imports
    # TODO: Uncomment as routes are implemented
    # from app.routes.auth import auth_bp
    # from app.routes.subjects import subjects_bp

    # Register blueprints
    # TODO: Uncomment as routes are implemented
    # app.register_blueprint(auth_bp)
    # app.register_blueprint(subjects_bp)

    app.logger.info("Blueprints registered successfully")


# NOTE: The actual route blueprints (auth, subjects) will be created
# in the next phase. The TODO comments above indicate where they will
# be imported and registered once implemented.
