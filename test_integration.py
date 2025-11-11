#!/usr/bin/env python3
"""
Script de pruebas de integración para la API.

Este script prueba todos los endpoints de la API con datos reales
de Backendless. Requiere que el servidor esté corriendo en localhost:8000
y que las credenciales de Backendless estén configuradas.

Uso:
    python test_integration.py

Requisitos:
    - Servidor corriendo en http://localhost:8000
    - Usuario de prueba creado en Backendless
    - Tabla Subjects configurada en Backendless
"""

import requests
import json
from typing import Dict, Optional

# Configuración
BASE_URL = "http://localhost:8000"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "Test123!"

# Colores para la terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_step(step: str):
    """Imprime un paso de prueba."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{step}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")


def print_success(message: str):
    """Imprime un mensaje de éxito."""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")


def print_error(message: str):
    """Imprime un mensaje de error."""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")


def print_info(message: str):
    """Imprime información."""
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.RESET}")


def print_json(data: dict):
    """Imprime JSON formateado."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def test_root_endpoint():
    """Prueba el endpoint raíz."""
    print_step("1. Probando endpoint raíz (GET /)")

    try:
        response = requests.get(f"{BASE_URL}/")

        if response.status_code == 200:
            print_success(f"Servidor respondió con 200 OK")
            data = response.json()
            print_json(data)

            if data.get('status') == 'online':
                print_success("API está online")
            return True
        else:
            print_error(f"Error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar al servidor")
        print_info("Asegúrate de que el servidor esté corriendo: python run.py")
        return False
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return False


def test_login() -> Optional[str]:
    """Prueba el endpoint de login y retorna el token."""
    print_step("2. Probando autenticación (POST /auth/login)")

    try:
        payload = {
            "login": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }

        print_info(f"Intentando login con: {TEST_USER_EMAIL}")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print_success("Login exitoso")
            print_json(data)

            token = data.get('user-token')
            if token:
                print_success(f"Token obtenido: {token[:20]}...")
                return token
            else:
                print_error("No se recibió token")
                return None
        else:
            print_error(f"Error en login: {response.status_code}")
            print_info("Respuesta:")
            print_json(response.json())
            print_info("\nVerifica que:")
            print_info("1. El usuario exista en Backendless")
            print_info("2. Las credenciales sean correctas")
            print_info("3. BACKENDLESS_APP_ID y BACKENDLESS_REST_API_KEY estén en .env")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None


def test_create_subject(token: str) -> Optional[str]:
    """Crea una materia de prueba y retorna su ID."""
    print_step("3. Probando creación de materia (POST /subjects)")

    try:
        payload = {
            "name": "Matemáticas I - Test",
            "code": f"MAT-TEST-{hash(token) % 10000}",
            "kind": "class",
            "weeklyLoadHours": 4
        }

        print_info(f"Creando materia: {payload['name']}")
        response = requests.post(
            f"{BASE_URL}/subjects",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "user-token": token
            }
        )

        if response.status_code == 201:
            data = response.json()
            print_success("Materia creada exitosamente")
            print_json(data)

            subject_id = data.get('objectId')
            if subject_id:
                print_success(f"ID de materia: {subject_id}")
                return subject_id
            return None
        else:
            print_error(f"Error al crear materia: {response.status_code}")
            print_json(response.json())
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None


def test_list_subjects(token: str):
    """Lista todas las materias."""
    print_step("4. Probando listado de materias (GET /subjects)")

    try:
        response = requests.get(
            f"{BASE_URL}/subjects",
            headers={"user-token": token}
        )

        if response.status_code == 200:
            data = response.json()
            print_success(f"Materias listadas exitosamente")
            print_info(f"Total de materias: {data.get('total', 0)}")
            print_info(f"Materias en esta página: {data.get('count', 0)}")

            if data.get('results'):
                print_info("\nPrimeras materias:")
                for subject in data['results'][:3]:
                    print(f"  - {subject.get('name')} ({subject.get('code')})")
            return True
        else:
            print_error(f"Error: {response.status_code}")
            print_json(response.json())
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_get_subject(token: str, subject_id: str):
    """Obtiene una materia por ID."""
    print_step(f"5. Probando obtener materia por ID (GET /subjects/{subject_id})")

    try:
        response = requests.get(
            f"{BASE_URL}/subjects/{subject_id}",
            headers={"user-token": token}
        )

        if response.status_code == 200:
            data = response.json()
            print_success("Materia obtenida exitosamente")
            print_json(data)
            return True
        else:
            print_error(f"Error: {response.status_code}")
            print_json(response.json())
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_update_subject(token: str, subject_id: str):
    """Actualiza una materia."""
    print_step(f"6. Probando actualización de materia (PUT /subjects/{subject_id})")

    try:
        payload = {
            "name": "Matemáticas I - Test (Actualizado)",
            "weeklyLoadHours": 6
        }

        print_info("Actualizando materia con:")
        print_json(payload)

        response = requests.put(
            f"{BASE_URL}/subjects/{subject_id}",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "user-token": token
            }
        )

        if response.status_code == 200:
            data = response.json()
            print_success("Materia actualizada exitosamente")
            print_json(data)
            return True
        else:
            print_error(f"Error: {response.status_code}")
            print_json(response.json())
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_delete_subject(token: str, subject_id: str):
    """Elimina una materia."""
    print_step(f"7. Probando eliminación de materia (DELETE /subjects/{subject_id})")

    try:
        response = requests.delete(
            f"{BASE_URL}/subjects/{subject_id}",
            headers={"user-token": token}
        )

        if response.status_code == 204:
            print_success("Materia eliminada exitosamente")
            return True
        else:
            print_error(f"Error: {response.status_code}")
            if response.text:
                print_json(response.json())
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def main():
    """Ejecuta todas las pruebas de integración."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     PRUEBAS DE INTEGRACIÓN - Planificador de Horarios     ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Colors.RESET)

    results = {
        'total': 0,
        'passed': 0,
        'failed': 0
    }

    # Test 1: Root endpoint
    results['total'] += 1
    if test_root_endpoint():
        results['passed'] += 1
    else:
        results['failed'] += 1
        print_error("\nNo se puede continuar sin conexión al servidor")
        return

    # Test 2: Login
    results['total'] += 1
    token = test_login()
    if token:
        results['passed'] += 1
    else:
        results['failed'] += 1
        print_error("\nNo se puede continuar sin autenticación")
        return

    # Test 3: Create subject
    results['total'] += 1
    subject_id = test_create_subject(token)
    if subject_id:
        results['passed'] += 1
    else:
        results['failed'] += 1
        print_info("\nContinuando con pruebas de lectura...")

    # Test 4: List subjects
    results['total'] += 1
    if test_list_subjects(token):
        results['passed'] += 1
    else:
        results['failed'] += 1

    # Solo continuar con update/delete si creamos una materia
    if subject_id:
        # Test 5: Get subject
        results['total'] += 1
        if test_get_subject(token, subject_id):
            results['passed'] += 1
        else:
            results['failed'] += 1

        # Test 6: Update subject
        results['total'] += 1
        if test_update_subject(token, subject_id):
            results['passed'] += 1
        else:
            results['failed'] += 1

        # Test 7: Delete subject
        results['total'] += 1
        if test_delete_subject(token, subject_id):
            results['passed'] += 1
        else:
            results['failed'] += 1

    # Resumen
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                    RESUMEN DE PRUEBAS                      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Colors.RESET)

    print(f"\nTotal de pruebas: {results['total']}")
    print(f"{Colors.GREEN}Pasaron: {results['passed']}{Colors.RESET}")
    print(f"{Colors.RED}Fallaron: {results['failed']}{Colors.RESET}")

    if results['failed'] == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ¡TODAS LAS PRUEBAS PASARON!{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}⚠️  Algunas pruebas fallaron. Revisa los errores arriba.{Colors.RESET}")


if __name__ == "__main__":
    main()
