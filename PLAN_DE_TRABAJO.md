# Plan de Trabajo - Backend Planificador de Horarios con IA
## Fase 1: Login y CRUD de Materias

**Proyecto:** Planificador Académico con IA
**Equipo:** 46
**Stack:** Python + Flask + Backendless
**Versión API:** 1.1.0
**Alcance:** Implementación de Login + CRUD Materias (6 endpoints)

---

## Resumen Ejecutivo

Este documento define el plan de trabajo para desarrollar la **primera fase del backend** del Planificador de Horarios con IA. Esta fase incluye únicamente:

1. **POST /auth/login** - Autenticación de usuarios
2. **GET /subjects** - Listar materias
3. **POST /subjects** - Crear materia
4. **GET /subjects/{id}** - Obtener materia por ID
5. **PUT /subjects/{id}** - Actualizar materia
6. **DELETE /subjects/{id}** - Eliminar materia

El sistema constará de una API RESTful en Python/Flask que actúa como proxy hacia Backendless (BaaS).

---

## Fase 0: Preparación y Configuración del Entorno ✅

**Duración estimada:** 1-2 días
**Estado:** ✅ COMPLETADA

### Objetivos
- ✅ Configurar el entorno de desarrollo
- ✅ Establecer la estructura del proyecto
- ✅ Configurar Backendless

### Tareas

#### 0.1 Configuración de Entorno Local
- [x] Crear entorno virtual Python (venv o conda)
- [x] Instalar dependencias base:
  - Flask
  - Flask-CORS
  - python-dotenv
  - requests (para llamadas a Backendless)
  - pydantic (validación de datos)
  - pytest (testing)
  - pytest-cov (cobertura)
  - python-dateutil (manejo de fechas)

#### 0.2 Estructura del Proyecto
```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── subjects.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── backendless_client.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── error_handler.py
│   └── utils/
│       ├── __init__.py
│       └── response_builder.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_subjects.py
├── .env.example
├── .env
├── requirements.txt
├── run.py
└── README.md
```

#### 0.3 Configuración de Backendless
- [x] Crear/verificar cuenta en Backendless
- [x] Obtener APP_ID y REST_API_KEY
- [x] Crear tabla en Backendless:
  - `Subjects` (con campos: objectId, name, code, kind, weeklyLoadHours, created, updated)
- [x] Configurar permisos de acceso y autenticación de usuarios
- [x] Probar conexión con API de Backendless
- [x] **CREADO:** Guía detallada de configuración en `BACKENDLESS_SETUP.md`

#### 0.4 Variables de Entorno
Crear archivo `.env`:
```env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=8000
BACKENDLESS_APP_ID=E6AC194E-095F-44F0-BF76-223C12EF6337
BACKENDLESS_REST_API_KEY=557AD802-52D8-422D-90EF-BDF931195F97
BACKENDLESS_BASE_URL=https://api.backendless.com
```

#### 0.5 Configuración de Git
- [x] Inicializar repositorio (si no existe)
- [x] Crear `.gitignore` (excluir .env, __pycache__, venv/)
- [x] Commit inicial de estructura

**Entregables:**
- ✅ Entorno Python configurado
- ✅ Estructura de carpetas creada
- ✅ Conexión con Backendless verificada (guía documentada)
- ✅ Repositorio Git inicializado
- ✅ **EXTRA:** Archivos base de aplicación creados (config, services, middleware, schemas)
- ✅ **EXTRA:** README actualizado con instrucciones de instalación
- ✅ **EXTRA:** Guía completa de Backendless (`BACKENDLESS_SETUP.md`)

---

## Fase 1: Core de la Aplicación y Configuración Base

**Duración estimada:** 2-3 días

### Objetivos
- Implementar el core de Flask
- Configurar middleware y manejo de errores
- Implementar cliente de Backendless

### Tareas

#### 1.1 Configuración de Flask (`app/__init__.py`)
- [ ] Crear factory de aplicación Flask
- [ ] Configurar CORS
- [ ] Registrar blueprints
- [ ] Configurar logging

#### 1.2 Configuración (`app/config.py`)
- [ ] Clase de configuración base
- [ ] Configuraciones por entorno (dev, test, prod)
- [ ] Validación de variables requeridas

#### 1.3 Cliente de Backendless (`app/services/backendless_client.py`)
- [ ] Clase `BackendlessClient`
- [ ] Métodos CRUD genéricos:
  - `get(table, object_id)`
  - `list(table, page_size, offset, where_clause)`
  - `create(table, data)`
  - `update(table, object_id, data)`
  - `delete(table, object_id)`
- [ ] Manejo de autenticación con user-token
- [ ] Manejo de errores de Backendless
- [ ] Transformación de respuestas

#### 1.4 Middleware de Autenticación (`app/middleware/auth.py`)
- [ ] Decorador `@require_auth`
- [ ] Extracción y validación de `user-token`
- [ ] Manejo de respuestas 401

#### 1.5 Manejo Global de Errores (`app/middleware/error_handler.py`)
- [ ] Handler para errores 400, 401, 403, 404, 500
- [ ] Formato estandarizado de respuestas de error
- [ ] Logging de errores

#### 1.6 Utilidades (`app/utils/`)
- [ ] `response_builder.py`: funciones para respuestas JSON consistentes
  - Función `success_response(data, status=200)`
  - Función `error_response(message, code, details=None)`
  - Función `paginated_response(results, total, count, offset)`

#### 1.7 Esquemas Pydantic (`app/models/schemas.py`)
- [ ] Definir modelos para validación:
  - `UserLoginRequest`, `UserLoginResponse`
  - `SubjectCreate`, `SubjectUpdate`, `Subject`
  - `PaginatedSubjects`

**Entregables:**
- Aplicación Flask funcional
- Cliente de Backendless operativo
- Middleware de autenticación
- Sistema de manejo de errores
- Modelos de validación

---

## Fase 2: Endpoint de Autenticación

**Duración estimada:** 1 día

### Objetivos
- Implementar autenticación con Backendless
- Probar flujo de login completo

### Tareas

#### 2.1 Autenticación (`app/routes/auth.py`)
- [ ] `POST /auth/login`
  - Validar request body (login, password) usando `UserLoginRequest`
  - Llamar a Backendless Users login endpoint
  - Retornar user-token, objectId, email en formato `UserLoginResponse`
  - Manejo de error 401 (credenciales inválidas)
  - Manejo de error 400 (datos faltantes)

#### 2.2 Pruebas Manuales
- [ ] Probar login con credenciales válidas
- [ ] Probar login con credenciales inválidas
- [ ] Verificar formato de respuesta
- [ ] Guardar user-token de prueba para siguiente fase

**Entregables:**
- Endpoint `/auth/login` funcional
- Respuestas correctas para casos exitosos y de error
- user-token obtenido para pruebas de Subjects

---

## Fase 3: CRUD de Subjects (Materias)

**Duración estimada:** 2-3 días

### Objetivos
- Implementar endpoints completos de Subjects
- Establecer patrón para otros recursos

### Tareas

#### 3.1 Rutas de Subjects (`app/routes/subjects.py`)
- [ ] `GET /subjects`
  - Paginación (pageSize, offset)
  - Filtro por `code` (opcional)
  - Autenticación requerida
  - Retornar `PaginatedSubjects`

- [ ] `POST /subjects`
  - Validar `SubjectCreate`
  - Crear en Backendless
  - Retornar Subject creado (201)

- [ ] `GET /subjects/{id}`
  - Obtener por objectId
  - Manejo de 404

- [ ] `PUT /subjects/{id}`
  - Validar `SubjectUpdate`
  - Actualizar en Backendless
  - Retornar Subject actualizado

- [ ] `DELETE /subjects/{id}`
  - Eliminar de Backendless
  - Retornar 204 (no content)

#### 3.2 Validaciones
- [ ] `name` y `code` requeridos en creación
- [ ] `kind` debe ser uno de: class, exam, task, project, other
- [ ] `weeklyLoadHours` debe ser >= 0
- [ ] `code` único (manejar error de Backendless)

#### 3.3 Tests (`tests/test_subjects.py`)
- [ ] Test GET list con paginación
- [ ] Test GET list con filtro por code
- [ ] Test POST crear materia válida
- [ ] Test POST con datos inválidos (400)
- [ ] Test GET by ID existente
- [ ] Test GET by ID no existente (404)
- [ ] Test PUT actualizar materia
- [ ] Test DELETE materia
- [ ] Test autenticación requerida (401)

**Entregables:**
- CRUD completo de Subjects
- Suite de tests unitarios
- Documentación de uso

---

## Fase 4: Testing y Documentación

**Duración estimada:** 1-2 días

### Objetivos
- Asegurar calidad del código con tests
- Documentar endpoints implementados
- Preparar entrega

### Tareas

#### 4.1 Testing de Autenticación (`tests/test_auth.py`)
- [ ] Test POST /auth/login con credenciales válidas
- [ ] Test POST /auth/login con credenciales inválidas (401)
- [ ] Test POST /auth/login con datos faltantes (400)
- [ ] Test formato de respuesta (user-token, objectId, email)

#### 4.2 Testing de Subjects (completar `tests/test_subjects.py`)
- [ ] Test GET /subjects con paginación
- [ ] Test GET /subjects con filtro por code
- [ ] Test POST /subjects con datos válidos (201)
- [ ] Test POST /subjects con datos inválidos (400)
- [ ] Test POST /subjects sin autenticación (401)
- [ ] Test GET /subjects/{id} existente (200)
- [ ] Test GET /subjects/{id} no existente (404)
- [ ] Test PUT /subjects/{id} actualización exitosa
- [ ] Test PUT /subjects/{id} no existente (404)
- [ ] Test DELETE /subjects/{id} exitoso (204)
- [ ] Test DELETE /subjects/{id} no existente (404)

#### 4.3 Tests de Integración
- [ ] Test flujo completo: login → crear materia → listar materias
- [ ] Test flujo completo: login → crear materia → actualizar → obtener por ID → eliminar
- [ ] Test validación de token en todos los endpoints de subjects

#### 4.4 Cobertura de Tests
- [ ] Ejecutar `pytest --cov=app tests/`
- [ ] Verificar cobertura mínima de 70%
- [ ] Agregar tests adicionales si es necesario

#### 4.5 Documentación README.md
- [ ] Descripción del proyecto
- [ ] Tecnologías utilizadas (Python, Flask, Backendless)
- [ ] Requisitos previos
- [ ] Instrucciones de instalación paso a paso
- [ ] Configuración de variables de entorno
- [ ] Comandos para ejecutar el servidor
- [ ] Comandos para ejecutar tests
- [ ] Estructura del proyecto
- [ ] Documentación de endpoints implementados:
  - POST /auth/login
  - GET /subjects
  - POST /subjects
  - GET /subjects/{id}
  - PUT /subjects/{id}
  - DELETE /subjects/{id}
- [ ] Ejemplos de uso (curl o Postman)

#### 4.6 Colección de Postman/Insomnia
- [ ] Crear colección con los 6 endpoints
- [ ] Incluir ejemplos de request/response
- [ ] Configurar variables de entorno (base_url, user_token)
- [ ] Exportar colección JSON

#### 4.7 Validación Final
- [ ] Todos los tests pasan
- [ ] Sin errores de linting (flake8)
- [ ] Código comentado adecuadamente
- [ ] Variables de entorno documentadas
- [ ] Verificar que el servidor inicia sin errores

**Entregables:**
- Suite completa de tests (>70% cobertura)
- README.md completo
- Colección Postman/Insomnia
- Código limpio y documentado
- Reporte de cobertura

---

## Cronograma Estimado

| Fase | Descripción | Duración | Acumulado |
|------|-------------|----------|-----------|
| 0 | Preparación y configuración | 1-2 días | 2 días |
| 1 | Core de la aplicación | 2-3 días | 5 días |
| 2 | Endpoint de Login | 1 día | 6 días |
| 3 | CRUD de Materias (Subjects) | 2-3 días | 9 días |
| 4 | Testing y Documentación | 1-2 días | **11 días** |

**Duración total estimada: 11 días laborables (aproximadamente 2 semanas)**

### Desglose de Tiempo por Endpoint

| Endpoint | Método | Tiempo Estimado |
|----------|--------|-----------------|
| /auth/login | POST | 1 día (incluye pruebas) |
| /subjects | GET | 0.5 días |
| /subjects | POST | 0.5 días |
| /subjects/{id} | GET | 0.3 días |
| /subjects/{id} | PUT | 0.5 días |
| /subjects/{id} | DELETE | 0.3 días |

**Total desarrollo de endpoints: 3.1 días**
**Testing y documentación: 1-2 días**

---

## Criterios de Éxito

### Funcionales
- ✅ Endpoint de login implementado y funcional
- ✅ Autenticación funcional con Backendless mediante user-token
- ✅ CRUD completo de Materias (Subjects) implementado:
  - GET /subjects (con paginación y filtro por code)
  - POST /subjects
  - GET /subjects/{id}
  - PUT /subjects/{id}
  - DELETE /subjects/{id}
- ✅ Todas las validaciones de datos funcionando correctamente
- ✅ Manejo correcto de errores (400, 401, 403, 404)

### Técnicos
- ✅ Cobertura de tests >70%
- ✅ Todos los tests pasando (pytest)
- ✅ Tiempo de respuesta <500ms para operaciones CRUD
- ✅ Código limpio (sin errores de flake8)
- ✅ Uso correcto de Pydantic para validación
- ✅ Integración exitosa con Backendless

### Documentación
- ✅ README completo con:
  - Instrucciones de instalación
  - Configuración de variables de entorno
  - Ejemplos de uso de cada endpoint
  - Comandos para ejecutar y testear
- ✅ Código documentado con docstrings
- ✅ Colección de Postman/Insomnia exportada
- ✅ Estructura del proyecto clara

### Ejecución
- ✅ Servidor Flask inicia sin errores
- ✅ Todas las dependencias instalables vía requirements.txt
- ✅ Variables de entorno correctamente configuradas
- ✅ Conexión con Backendless verificada

---

## Riesgos y Mitigación

### Riesgo 1: Problemas de Conexión con Backendless
**Probabilidad:** Media
**Impacto:** Alto
**Mitigación:**
- Verificar credenciales (APP_ID y REST_API_KEY) en fase 0
- Probar conexión antes de comenzar desarrollo
- Tener documentación de Backendless API a mano
- Implementar manejo robusto de errores de red

### Riesgo 2: Autenticación con Backendless
**Probabilidad:** Media
**Impacto:** Alto
**Mitigación:**
- Estudiar documentación de autenticación de Backendless
- Crear usuarios de prueba en Backendless
- Implementar manejo correcto de tokens
- Testear exhaustivamente el flujo de login

### Riesgo 3: Validaciones de Datos Inconsistentes
**Probabilidad:** Baja
**Impacto:** Medio
**Mitigación:**
- Usar Pydantic para validaciones centralizadas
- Definir esquemas claros desde el inicio
- Testear casos edge (datos faltantes, tipos incorrectos)
- Revisar contrato OpenAPI constantemente

### Riesgo 4: Retrasos en Configuración del Entorno
**Probabilidad:** Media
**Impacto:** Bajo
**Mitigación:**
- Documentar proceso de instalación detalladamente
- Usar requirements.txt específicos con versiones fijas
- Tener backup de Python 3.9+ instalado
- Preparar entorno virtual desde el día 1

---

## Dependencias del Proyecto

### Dependencias Principales
```txt
Flask==3.0.0
Flask-CORS==4.0.0
python-dotenv==1.0.0
requests==2.31.0
pydantic==2.5.0
python-dateutil==2.8.2
```

### Dependencias de Desarrollo
```txt
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
black==23.12.0
flake8==6.1.0
mypy==1.7.1
```

---

## Contacto y Equipo

**Equipo 46**
- Gabriel Sareñana Labra - A01795507
- David Plazer Medrano - A01796849
- Daniel Nuñez Constantino - A01379717
- Didier Gamboa Angulo - A01795710

**Email:** equipo46@example.com
**Repositorio:** https://github.com/example/planificador-ia

---

## Notas Finales

Este plan está diseñado para ser ejecutado de manera iterativa. Se recomienda:

1. **Commits frecuentes**: Hacer commits después de cada tarea completada
2. **Code reviews**: Revisión de código entre miembros del equipo
3. **Tests desde el inicio**: Implementar tests en paralelo con el desarrollo, no al final
4. **Documentar mientras desarrollas**: Agregar docstrings y comentarios conforme escribes código
5. **Probar constantemente**: Ejecutar el servidor frecuentemente para detectar errores temprano
6. **Usar Postman/Insomnia**: Probar cada endpoint manualmente además de los tests automatizados
7. **Consultar el contrato OpenAPI**: Verificar constantemente que tu implementación coincida con el YAML

### Siguientes Pasos (Fases Futuras)

Esta es la **Fase 1** del proyecto completo. Una vez completada, las siguientes fases incluirán:
- **Fase 2**: CRUD de Events (Eventos)
- **Fase 3**: Gestión de Notificaciones y Preferencias
- **Fase 4**: Detección de Conflictos (algoritmo de traslapes)
- **Fase 5**: Sistema de Sugerencias con IA (scoring inteligente)
- **Fase 6**: Deployment a producción

El conocimiento y estructura creados en esta fase servirán como base sólida para todas las funcionalidades futuras.

**¡Éxito en el desarrollo! 🚀**
