#!/usr/bin/env python3
"""
Script para crear usuario de prueba en Backendless.

Uso:
    python create_test_user.py
"""

import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

APP_ID = os.getenv('BACKENDLESS_APP_ID')
REST_API_KEY = os.getenv('BACKENDLESS_REST_API_KEY')
BASE_URL = os.getenv('BACKENDLESS_BASE_URL', 'https://api.backendless.com')

# Usuario de prueba
TEST_USER = {
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User"
}

def create_user():
    """Crea un usuario de prueba en Backendless."""
    url = f"{BASE_URL}/{APP_ID}/{REST_API_KEY}/users/register"

    print("🔄 Creando usuario de prueba en Backendless...")
    print(f"   Email: {TEST_USER['email']}")

    try:
        response = requests.post(
            url,
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code in [200, 201]:
            print("✅ Usuario creado exitosamente!")
            print(f"   ObjectId: {response.json().get('objectId')}")
            print(f"\nPuedes usar estas credenciales para el login:")
            print(f"   Email: {TEST_USER['email']}")
            print(f"   Password: {TEST_USER['password']}")
        elif response.status_code == 400:
            error_data = response.json()
            if 'already registered' in error_data.get('message', '').lower():
                print("ℹ️  El usuario ya existe en Backendless")
                print(f"   Puedes usarlo para el login:")
                print(f"   Email: {TEST_USER['email']}")
                print(f"   Password: {TEST_USER['password']}")
            else:
                print(f"❌ Error: {error_data.get('message', 'Error desconocido')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if not APP_ID or not REST_API_KEY:
        print("❌ Error: Variables de entorno no configuradas")
        print("   Asegúrate de que .env contenga:")
        print("   - BACKENDLESS_APP_ID")
        print("   - BACKENDLESS_REST_API_KEY")
    else:
        create_user()
