# Planificador de Horarios con IA - Backend API

Backend RESTful para el sistema de Planificador de Horarios con IA. Implementado con Python/Flask y Backendless como BaaS.

**Equipo 46:**
- Gabriel Sareñana Labra - A01795507
- David Plazer Medrano - A01796849
- Daniel Nuñez Constantino - A01379717
- Didier Gamboa Angulo - A01795710

## Estado del Proyecto

🚧 **En Desarrollo - Fase 0 Completada**

### Fase Actual: Fase 0 - Preparación y Configuración del Entorno

**Completado:**
- ✅ Estructura de carpetas creada
- ✅ Archivos de configuración (.env, requirements.txt)
- ✅ Configuración de Git (.gitignore)
- ✅ Archivos base de la aplicación (config, schemas, services, middleware)
- ✅ Documentación de configuración de Backendless

**Próximos pasos:** Fase 1 - Core de la aplicación y configuración base

---

## Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Backendless (gratuita)
- Git

---

## Instalación

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd Backend
```

### 2. Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita el archivo `.env` con tus credenciales de Backendless:
   ```env
   BACKENDLESS_APP_ID=tu-app-id-aqui
   BACKENDLESS_REST_API_KEY=tu-rest-api-key-aqui
   ```

3. **Consulta la guía completa:** [BACKENDLESS_SETUP.md](BACKENDLESS_SETUP.md)

---

## Configuración de Backendless

⚠️ **IMPORTANTE:** Antes de ejecutar la aplicación, debes configurar Backendless.

Sigue la guía detallada en [BACKENDLESS_SETUP.md](BACKENDLESS_SETUP.md) para:
- Crear tu cuenta de Backendless
- Obtener tus credenciales (APP_ID y REST_API_KEY)
- Configurar la tabla `Subjects`
- Crear usuarios de prueba
- Configurar permisos

---

## Ejecutar la Aplicación

```bash
python run.py
```

La aplicación estará disponible en: `http://localhost:8000`

---

## Estructura del Proyecto

```
Backend/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config.py             # Configuration classes
│   ├── routes/               # API route blueprints
│   │   └── __init__.py
│   ├── services/             # Business logic services
│   │   ├── __init__.py
│   │   └── backendless_client.py
│   ├── models/               # Pydantic schemas
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── middleware/           # Request/response middleware
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── error_handler.py
│   └── utils/                # Utility functions
│       ├── __init__.py
│       └── response_builder.py
├── tests/                    # Test suite
│   └── __init__.py
├── .env                      # Environment variables (not in git)
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
├── PLAN_DE_TRABAJO.md        # Development plan
├── BACKENDLESS_SETUP.md      # Backendless setup guide
└── README.md                 # This file
```

---

## Tecnologías Utilizadas

- **Python 3.9+** - Lenguaje de programación
- **Flask 3.0** - Framework web
- **Pydantic 2.5** - Validación de datos
- **Backendless** - Backend as a Service (BaaS)
- **pytest** - Framework de testing
- **Flask-CORS** - Manejo de CORS

---

## Principios de Desarrollo

Este proyecto sigue las mejores prácticas de desarrollo:

- ✅ **Clean Code** - Código limpio y legible
- ✅ **SOLID Principles** - Principios de diseño orientado a objetos
- ✅ **Type Hints** - Tipado estático para mejor mantenibilidad
- ✅ **Comprehensive Documentation** - Documentación exhaustiva con docstrings
- ✅ **Error Handling** - Manejo robusto de errores
- ✅ **Logging** - Sistema de logging configurable
- ✅ **Security Best Practices** - Variables de entorno para secretos

---

## Endpoints Disponibles

> 📝 **Nota:** Los endpoints se implementarán en las siguientes fases.
> Esta sección se actualizará conforme se completen las fases de desarrollo.

### Fase 2: Autenticación
- `POST /auth/login` - Autenticación de usuarios

### Fase 3: Materias (Subjects)
- `GET /subjects` - Listar materias
- `POST /subjects` - Crear materia
- `GET /subjects/{id}` - Obtener materia por ID
- `PUT /subjects/{id}` - Actualizar materia
- `DELETE /subjects/{id}` - Eliminar materia

---

## Desarrollo

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con cobertura
pytest --cov=app tests/

# Ejecutar tests específicos
pytest tests/test_auth.py
```

### Linting

```bash
# Verificar estilo de código
flake8 app/

# Formatear código automáticamente
black app/
```

### Type Checking

```bash
# Verificar tipos estáticos
mypy app/
```

---

## Documentación Adicional

- [Plan de Trabajo](PLAN_DE_TRABAJO.md) - Plan detallado de desarrollo por fases
- [Configuración de Backendless](BACKENDLESS_SETUP.md) - Guía de configuración de Backendless
- [Contrato OpenAPI](planificador-horarios-prod.yaml) - Especificación completa de la API

---

## Troubleshooting

### Error: "Missing required environment variables"

**Solución:** Asegúrate de haber configurado correctamente el archivo `.env` con tus credenciales de Backendless.

```bash
cp .env.example .env
# Edita .env con tus credenciales reales
```

### Error: "Module not found"

**Solución:** Asegúrate de haber activado el entorno virtual e instalado las dependencias.

```bash
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

### Error al conectar con Backendless

**Solución:** Verifica que:
1. Tus credenciales sean correctas
2. Tengas conexión a internet
3. La tabla `Subjects` esté creada en Backendless

Consulta [BACKENDLESS_SETUP.md](BACKENDLESS_SETUP.md) para más detalles.

---

## Contacto

Para preguntas o soporte, contacta al equipo:

**Email:** equipo46@example.com

---

## Licencia

Este proyecto es parte de un proyecto académico del TEC.

---

**Última actualización:** Fase 0 completada - Estructura base del proyecto
