"""
Application entry point.

This module serves as the entry point for running the Flask application.
It creates an application instance using the factory pattern and runs
the development server.

Usage:
    python run.py

Author: Equipo 46
Date: 2024
"""

import os
from app import create_app

# Create application instance
app = create_app()

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    print("=" * 70)
    print("🚀 Planificador de Horarios con IA - Backend API")
    print("=" * 70)
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Running on: http://localhost:{port}")
    print(f"Debug mode: {'ON' if debug else 'OFF'}")
    print("=" * 70)
    print("\nPress CTRL+C to quit\n")

    # Run the application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
