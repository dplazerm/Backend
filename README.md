# Planificador de Horarios con IA - Backend API

> Backend RESTful para sistema académico de planificación de horarios inteligente

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Pydantic](https://img.shields.io/badge/pydantic-2.10-red.svg)](https://docs.pydantic.dev/)
[![Tests](https://img.shields.io/badge/tests-32%20passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-75%25-yellowgreen.svg)](htmlcov/)
[![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Quick Start](#-quick-start)
- [Instalación](#-instalación)
- [Configuración](#️-configuración)
- [Uso](#-uso)
- [API Reference](#-api-reference)
- [Tests](#-tests)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías](#️-tecnologías)
- [Troubleshooting](#-troubleshooting)
- [Equipo](#-equipo)
- [Licencia](#-licencia)

## ✨ Características

- 🔐 **Autenticación JWT** - Sistema de autenticación con tokens seguros
- 📚 **CRUD Completo** - Gestión completa de materias académicas
- 🔍 **Paginación y Filtrado** - Búsqueda eficiente con filtros personalizados
- ✅ **Validación Robusta** - Validación de datos con Pydantic
- 🛡️ **Manejo de Errores** - Sistema centralizado de manejo de errores
- 🧪 **Testing Completo** - 29 tests unitarios con 75% de cobertura
- 📖 **Documentación OpenAPI** - Especificación completa de la API
- 🎯 **Clean Code** - Siguiendo principios SOLID y mejores prácticas

## 🚀 Quick Start

```bash
# Clonar repositorio
git clone <repository-url>
cd Backend

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de Backendless

# Ejecutar servidor
python run.py
```

El servidor estará disponible en `http://localhost:8000`

## 📦 Instalación

### Requisitos Previos

- Python 3.13 o superior (recomendado 3.13+)
- pip (gestor de paquetes)
- Cuenta de Backendless (gratuita)

### Paso a Paso

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd Backend
   ```

2. **Crear entorno virtual**
   ```bash
   python3 -m venv venv

   # Activar en macOS/Linux
   source venv/bin/activate

   # Activar en Windows
   venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Backendless**

   Consulta la [guía de configuración de Backendless](BACKENDLESS_SETUP.md) para:
   - Crear cuenta y obtener credenciales
   - Configurar tabla Subjects
   - Crear usuarios de prueba

5. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   ```

   Edita `.env` con tus credenciales:
   ```env
   BACKENDLESS_APP_ID=tu-app-id
   BACKENDLESS_REST_API_KEY=tu-api-key
   FLASK_ENV=development
   PORT=8000
   ```

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Requerido | Default |
|----------|-------------|-----------|---------|
| `BACKENDLESS_APP_ID` | ID de aplicación Backendless | Sí | - |
| `BACKENDLESS_REST_API_KEY` | API Key de Backendless | Sí | - |
| `BACKENDLESS_BASE_URL` | URL base de Backendless | No | `https://api.backendless.com` |
| `FLASK_ENV` | Entorno de Flask | No | `development` |
| `FLASK_DEBUG` | Modo debug | No | `True` |
| `PORT` | Puerto del servidor | No | `8000` |

### Configuración de Backendless

Para configurar Backendless correctamente, sigue la [guía detallada](BACKENDLESS_SETUP.md).

## 💻 Uso

### Iniciar el Servidor

```bash
python run.py
```

El servidor iniciará en `http://localhost:8000`

### Verificar que el Servidor está Funcionando

Abre tu navegador o usa curl para acceder a la raíz de la API:

```bash
curl http://localhost:8000/
```

**Respuesta:**
```json
{
  "name": "Planificador de Horarios - Backend API",
  "version": "1.0.0",
  "description": "Backend RESTful para sistema académico de planificación de horarios inteligente",
  "status": "online",
  "endpoints": {
    "auth": {
      "login": "POST /auth/login"
    },
    "subjects": {
      "list": "GET /subjects",
      "create": "POST /subjects",
      "get": "GET /subjects/{id}",
      "update": "PUT /subjects/{id}",
      "delete": "DELETE /subjects/{id}"
    }
  }
}
```

### Ejemplos de Uso

#### 1. Autenticación

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "login": "user@example.com",
    "password": "your-password"
  }'
```

**Respuesta:**
```json
{
  "user-token": "abc123...",
  "objectId": "USER123",
  "email": "user@example.com"
}
```

#### 2. Listar Materias

```bash
curl -X GET "http://localhost:8000/subjects?pageSize=10&offset=0" \
  -H "user-token: your-token-here"
```

**Respuesta:**
```json
{
  "total": 50,
  "count": 10,
  "offset": 0,
  "results": [
    {
      "objectId": "SUBJ123",
      "name": "Cálculo I",
      "code": "CALC1",
      "kind": "class",
      "weeklyLoadHours": 4
    }
  ]
}
```

#### 3. Crear Materia

```bash
curl -X POST http://localhost:8000/subjects \
  -H "Content-Type: application/json" \
  -H "user-token: your-token-here" \
  -d '{
    "name": "Cálculo I",
    "code": "CALC1",
    "kind": "class",
    "weeklyLoadHours": 4
  }'
```

#### 4. Actualizar Materia

```bash
curl -X PUT http://localhost:8000/subjects/SUBJ123 \
  -H "Content-Type: application/json" \
  -H "user-token: your-token-here" \
  -d '{
    "name": "Cálculo Avanzado I",
    "weeklyLoadHours": 6
  }'
```

#### 5. Eliminar Materia

```bash
curl -X DELETE http://localhost:8000/subjects/SUBJ123 \
  -H "user-token: your-token-here"
```

## 📚 API Reference

### Información General

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/` | Información de la API y endpoints disponibles | No |

### Autenticación

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | Iniciar sesión | No |

### Subjects (Materias)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/subjects` | Listar todas las materias | Sí |
| POST | `/subjects` | Crear nueva materia | Sí |
| GET | `/subjects/{id}` | Obtener materia por ID | Sí |
| PUT | `/subjects/{id}` | Actualizar materia | Sí |
| DELETE | `/subjects/{id}` | Eliminar materia | Sí |

### Parámetros de Paginación

| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `pageSize` | integer | Número de resultados por página | 50 |
| `offset` | integer | Número de resultados a saltar | 0 |

### Filtros Disponibles

| Parámetro | Endpoint | Descripción |
|-----------|----------|-------------|
| `code` | GET /subjects | Filtrar por código exacto de materia |

### Códigos de Respuesta

| Código | Descripción |
|--------|-------------|
| 200 | Operación exitosa |
| 201 | Recurso creado exitosamente |
| 204 | Operación exitosa sin contenido |
| 400 | Solicitud inválida (validación fallida) |
| 401 | No autenticado (token faltante o inválido) |
| 403 | Acceso denegado |
| 404 | Recurso no encontrado |
| 415 | Tipo de contenido no soportado |
| 500 | Error interno del servidor |

Para la especificación completa de la API, consulta [planificador-horarios-prod.yaml](planificador-horarios-prod.yaml).

## 🧪 Tests

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con output verbose
pytest -v

# Ejecutar tests específicos
pytest tests/test_auth.py
pytest tests/test_subjects.py

# Ejecutar solo tests unitarios
pytest -m unit
```

### Cobertura de Código

```bash
# Generar reporte de cobertura
pytest --cov=app tests/

# Generar reporte HTML
pytest --cov=app --cov-report=html tests/

# Ver reporte HTML
open htmlcov/index.html
```

### Resultados Actuales

- **Tests totales:** 32
- **Tests pasando:** 32 (100%)
- **Cobertura de código:** 75%

### Linting y Formateo

```bash
# Verificar estilo de código
flake8 app/ tests/

# Formatear código automáticamente
black app/ tests/

# Verificar tipos estáticos
mypy app/
```

## 📁 Estructura del Proyecto

```
Backend/
├── app/                          # Código fuente de la aplicación
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuración por entornos
│   ├── routes/                  # Blueprints de endpoints
│   │   ├── auth.py             # Autenticación
│   │   └── subjects.py         # CRUD de materias
│   ├── services/               # Lógica de negocio
│   │   └── backendless_client.py
│   ├── models/                 # Schemas de validación
│   │   └── schemas.py
│   ├── middleware/             # Middleware personalizado
│   │   ├── auth.py            # Autenticación
│   │   └── error_handler.py   # Manejo de errores
│   └── utils/                  # Utilidades
│       └── response_builder.py
├── tests/                       # Suite de tests
│   ├── conftest.py             # Fixtures compartidos
│   ├── test_auth.py            # Tests de autenticación
│   └── test_subjects.py        # Tests de subjects
├── htmlcov/                     # Reporte de cobertura HTML
├── .env.example                 # Template de variables de entorno
├── .gitignore                   # Archivos ignorados por git
├── pytest.ini                   # Configuración de pytest
├── requirements.txt             # Dependencias Python
├── run.py                       # Punto de entrada
├── BACKENDLESS_SETUP.md        # Guía de Backendless
└── README.md                    # Este archivo
```

## 🛠️ Tecnologías

### Backend Framework
- [Flask 3.0](https://flask.palletsprojects.com/) - Micro web framework
- [Flask-CORS](https://flask-cors.readthedocs.io/) - Manejo de CORS

### Validación y Serialización
- [Pydantic 2.10](https://docs.pydantic.dev/) - Validación de datos con type hints

### Backend as a Service
- [Backendless](https://backendless.com/) - BaaS para persistencia y autenticación

### Testing
- [pytest](https://pytest.org/) - Framework de testing
- [pytest-cov](https://pytest-cov.readthedocs.io/) - Plugin de cobertura
- [pytest-mock](https://pytest-mock.readthedocs.io/) - Mocking para pytest

### Desarrollo
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Variables de entorno
- [black](https://black.readthedocs.io/) - Formateador de código
- [flake8](https://flake8.pycqa.org/) - Linter
- [mypy](https://mypy.readthedocs.io/) - Type checker

## 🔧 Troubleshooting

### Error: "Missing required environment variables"

**Problema:** La aplicación no puede iniciar sin las credenciales de Backendless.

**Solución:**
```bash
cp .env.example .env
# Edita .env con tus credenciales de Backendless
```

### Error: "Module not found"

**Problema:** Dependencias no instaladas o entorno virtual no activado.

**Solución:**
```bash
# Activar entorno virtual
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Error: "Connection refused" o "Backendless timeout"

**Problema:** No se puede conectar con Backendless.

**Solución:**
1. Verifica tu conexión a internet
2. Confirma que las credenciales en `.env` sean correctas
3. Revisa que la tabla `Subjects` exista en Backendless
4. Consulta [BACKENDLESS_SETUP.md](BACKENDLESS_SETUP.md)

### Error 401: "Token inválido o expirado"

**Problema:** El token de autenticación no es válido.

**Solución:**
1. Realiza login nuevamente para obtener un token fresco
2. Verifica que estés incluyendo el header `user-token` en tus requests
3. Confirma que el token no haya expirado

### Tests fallan localmente

**Problema:** Los tests no pasan en tu máquina.

**Solución:**
```bash
# Asegúrate de tener las dependencias de testing instaladas
pip install -r requirements.txt

# Ejecuta pytest con modo verbose para ver detalles
pytest -v

# Limpia cache de pytest
rm -rf .pytest_cache __pycache__
```

## 👥 Equipo

**Equipo 46 - TEC**

- Gabriel Sareñana Labra - A01795507
- David Plazer Medrano - A01796849
- Daniel Nuñez Constantino - A01379717
- Didier Gamboa Angulo - A01795710

## 📧 Contacto

Para preguntas, soporte o reportar issues:

**Email:** equipo46@example.com

## 📄 Licencia

Este proyecto es parte de un proyecto académico del Tecnológico de Monterrey (TEC).

---

## 📚 Documentación Adicional

- [Plan de Trabajo](PLAN_DE_TRABAJO.md) - Documentación del proceso de desarrollo
- [Configuración de Backendless](BACKENDLESS_SETUP.md) - Guía detallada de configuración
- [Especificación OpenAPI](planificador-horarios-prod.yaml) - Contrato completo de la API

---

<div align="center">

**Planificador de Horarios con IA** - Sistema académico inteligente

Hecho con ❤️ por Equipo 46

</div>
