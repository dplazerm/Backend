# Guía de Configuración de Backendless

Esta guía proporciona instrucciones paso a paso para configurar Backendless como backend de la aplicación.

## Tabla de Contenidos

1. [Crear Cuenta en Backendless](#1-crear-cuenta-en-backendless)
2. [Obtener Credenciales de API](#2-obtener-credenciales-de-api)
3. [Configurar Tabla Subjects](#3-configurar-tabla-subjects)
4. [Configurar Autenticación de Usuarios](#4-configurar-autenticación-de-usuarios)
5. [Configurar Permisos y Seguridad](#5-configurar-permisos-y-seguridad)
6. [Probar la Conexión](#6-probar-la-conexión)

---

## 1. Crear Cuenta en Backendless

1. Visita [https://backendless.com/](https://backendless.com/)
2. Haz clic en "Get Started for Free"
3. Registra una cuenta usando tu email
4. Verifica tu email
5. Inicia sesión en el dashboard de Backendless

---

## 2. Obtener Credenciales de API

### Paso 1: Crear una Nueva Aplicación

1. En el dashboard, haz clic en "Create New App"
2. Asigna un nombre a tu aplicación (ej: "Planificador-Horarios")
3. Selecciona el plan gratuito (Cloud 99)
4. Haz clic en "Create App"

### Paso 2: Obtener APP_ID y REST_API_KEY

1. Una vez creada la app, haz clic en ella para entrar
2. Ve a la sección **"App Settings"** (icono de engranaje en el menú lateral)
3. Haz clic en **"Manage > App Settings"**
4. Encontrarás dos valores importantes:
   - **Application ID** (APP_ID)
   - **REST API Key** (REST_API_KEY)
5. Copia estos valores y guárdalos de forma segura

### Paso 3: Actualizar Variables de Entorno

Edita el archivo `.env` en la raíz del proyecto:

```env
BACKENDLESS_APP_ID=tu-app-id-aqui
BACKENDLESS_REST_API_KEY=tu-rest-api-key-aqui
BACKENDLESS_BASE_URL=https://api.backendless.com
```

---

## 3. Configurar Tabla Subjects

### Paso 1: Crear la Tabla

1. En el dashboard de Backendless, ve a **"Database"** en el menú lateral (icono de base de datos)
2. Haz clic en **"Create New Table"**
3. Nombra la tabla: `Subjects`
4. Haz clic en "Create"

### Paso 2: Configurar Columnas

Backendless crea automáticamente las columnas:
- `objectId` (STRING) - Identificador único (automático)
- `created` (DATETIME) - Fecha de creación (automático)
- `updated` (DATETIME) - Fecha de actualización (automático)

Ahora agrega las siguientes columnas manualmente:

#### Columna: name
- Haz clic en "+" para agregar columna
- **Column Name:** `name`
- **Type:** `STRING`
- **Required:** ✅ Sí
- **Unique:** ❌ No
- Haz clic en "Save"

#### Columna: code
- Haz clic en "+" para agregar columna
- **Column Name:** `code`
- **Type:** `STRING`
- **Required:** ✅ Sí
- **Unique:** ✅ Sí (para evitar códigos duplicados)
- Haz clic en "Save"

#### Columna: kind
- Haz clic en "+" para agregar columna
- **Column Name:** `kind`
- **Type:** `STRING`
- **Required:** ❌ No
- **Default Value:** `class`
- Haz clic en "Save"

#### Columna: weeklyLoadHours
- Haz clic en "+" para agregar columna
- **Column Name:** `weeklyLoadHours`
- **Type:** `INT`
- **Required:** ❌ No
- **Default Value:** `4`
- Haz clic en "Save"

### Paso 3: Verificar Estructura de la Tabla

Tu tabla `Subjects` debe tener las siguientes columnas:

| Column Name       | Type     | Required | Unique | Default | Auto |
|-------------------|----------|----------|--------|---------|------|
| objectId          | STRING   | ✅       | ✅     | -       | ✅   |
| name              | STRING   | ✅       | ❌     | -       | ❌   |
| code              | STRING   | ✅       | ✅     | -       | ❌   |
| kind              | STRING   | ❌       | ❌     | "class" | ❌   |
| weeklyLoadHours   | INT      | ❌       | ❌     | 4       | ❌   |
| created           | DATETIME | ✅       | ❌     | -       | ✅   |
| updated           | DATETIME | ✅       | ❌     | -       | ✅   |

---

## 4. Configurar Autenticación de Usuarios

### Paso 1: Habilitar User Registration

1. Ve a **"Users"** en el menú lateral
2. Haz clic en **"User Registration"**
3. Asegúrate de que esté habilitado: **"Enable User Registration"** ✅

### Paso 2: Configurar Identity Properties

1. En la sección "User Registration", verifica que **Email** esté configurado como **User Identity**
2. Esto permite que los usuarios inicien sesión con su email

### Paso 3: Crear Usuario de Prueba

Para facilitar el desarrollo, crea un usuario de prueba:

1. Ve a **"Users"** > **"Data"**
2. Haz clic en "+" para agregar un nuevo usuario
3. Completa los campos:
   - **email:** `test@example.com`
   - **password:** `Test123!`
   - **name:** `Test User` (opcional)
4. Haz clic en "Save"

**Guarda estas credenciales** para usarlas en las pruebas del endpoint `/auth/login`.

---

## 5. Configurar Permisos y Seguridad

### Paso 1: Configurar Permisos de la Tabla Subjects

1. Ve a **"Database"** > Selecciona la tabla **"Subjects"**
2. Haz clic en la pestaña **"Permissions"**

#### Para Desarrollo (Más Permisivo):

Configure los siguientes permisos para facilitar el desarrollo:

| Operation | Role              | Permission |
|-----------|-------------------|------------|
| FIND      | AuthenticatedUser | ✅ GRANT   |
| CREATE    | AuthenticatedUser | ✅ GRANT   |
| UPDATE    | AuthenticatedUser | ✅ GRANT   |
| DELETE    | AuthenticatedUser | ✅ GRANT   |

Esto permite que cualquier usuario autenticado pueda realizar operaciones CRUD en Subjects.

#### Para Producción (Recomendado):

En producción, considera restricciones más estrictas:

- **FIND:** Permitir a todos los usuarios autenticados
- **CREATE:** Solo administradores o roles específicos
- **UPDATE:** Solo el creador del objeto o administradores
- **DELETE:** Solo administradores

### Paso 2: Configurar API Keys Security

1. Ve a **"App Settings"** > **"Security"**
2. Asegúrate de que **REST API Key** esté activo
3. Para producción, considera rotar las keys periódicamente

---

## 6. Probar la Conexión

### Opción 1: Usar cURL

Prueba el login con el usuario de prueba:

```bash
curl -H "Content-Type: application/json" \
  -X POST \
  'https://api.backendless.com/{TU-APP-ID}/{TU-REST-API-KEY}/users/login' \
  -d '{"login":"test@example.com", "password":"Test123!"}'
```

Deberías recibir una respuesta similar a:

```json
{
  "user-token": "ABC123XYZ...",
  "objectId": "USER-ID-123",
  "email": "test@example.com"
}
```

### Opción 2: Usar Backendless Console

1. Ve a **"Database"** > **"Subjects"**
2. Haz clic en "+" para agregar un registro de prueba manualmente
3. Completa los campos:
   - **name:** `Matemáticas I`
   - **code:** `MAT101`
   - **kind:** `class`
   - **weeklyLoadHours:** `4`
4. Haz clic en "Save"
5. Verifica que el registro aparezca en la tabla

### Opción 3: Usar Postman/Insomnia

Importa la siguiente request para probar:

**Login Request:**
- **Method:** POST
- **URL:** `https://api.backendless.com/{APP-ID}/{REST-API-KEY}/users/login`
- **Headers:** `Content-Type: application/json`
- **Body:**
  ```json
  {
    "login": "test@example.com",
    "password": "Test123!"
  }
  ```

**Create Subject Request:**
- **Method:** POST
- **URL:** `https://api.backendless.com/{APP-ID}/{REST-API-KEY}/data/Subjects`
- **Headers:**
  - `Content-Type: application/json`
  - `user-token: {TOKEN-FROM-LOGIN}`
- **Body:**
  ```json
  {
    "name": "Cálculo I",
    "code": "CALC101",
    "kind": "class",
    "weeklyLoadHours": 4
  }
  ```

---

## Troubleshooting

### Error: "Invalid application id or secret key"

- Verifica que `BACKENDLESS_APP_ID` y `BACKENDLESS_REST_API_KEY` estén correctos en el archivo `.env`
- Asegúrate de no tener espacios extra o comillas en los valores

### Error: "User token is not valid"

- El token puede haber expirado
- Realiza un nuevo login para obtener un token fresco
- Verifica que estás enviando el header `user-token` correctamente

### Error: "Table 'Subjects' not found"

- Verifica que la tabla se llame exactamente `Subjects` (con mayúscula inicial)
- Backendless es case-sensitive

### Error: "Column 'code' must be unique"

- Ya existe un Subject con ese código
- Usa un código diferente o elimina el registro existente

### No puedo crear usuarios

- Verifica que "User Registration" esté habilitado en Settings > Users
- Asegúrate de que el email tenga un formato válido

---

## Recursos Adicionales

- [Documentación oficial de Backendless](https://backendless.com/docs/)
- [Backendless REST API Reference](https://backendless.com/docs/rest/)
- [Backendless User Management](https://backendless.com/docs/rest/users_overview.html)
- [Backendless Data Service](https://backendless.com/docs/rest/data_overview.html)

---

## Checklist de Configuración

Usa este checklist para verificar que todo esté configurado correctamente:

- [ ] Cuenta de Backendless creada
- [ ] Aplicación creada en Backendless
- [ ] APP_ID y REST_API_KEY obtenidos
- [ ] Variables de entorno actualizadas en `.env`
- [ ] Tabla `Subjects` creada con todas las columnas
- [ ] Columna `code` configurada como UNIQUE
- [ ] User Registration habilitado
- [ ] Usuario de prueba creado
- [ ] Permisos de la tabla configurados
- [ ] Conexión probada exitosamente

---

**¡Listo!** Backendless está configurado y listo para usar con la aplicación.
