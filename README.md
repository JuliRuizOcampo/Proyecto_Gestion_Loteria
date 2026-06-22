# Lotería CU-DS

Proyecto Django de ejemplo para gestionar números ganadores de lotería con un dashboard personalizado.

## Credenciales de prueba

Este proyecto incluye un backend de autenticación de desarrollo con credenciales fijas.

- Usuario: `admin`
- Contraseña: `admin123`

## Cómo acceder

- Raíz pública: `http://127.0.0.1:8000/` → redirige a `http://127.0.0.1:8000/loteria/`
- Login: `http://127.0.0.1:8000/loteria/login/`
- Dashboard protegido: `http://127.0.0.1:8000/loteria/dashboard/`
- Crear registro: `http://127.0.0.1:8000/loteria/registrar/`
- Editar registro: `http://127.0.0.1:8000/loteria/editar/<id>/`
- Eliminar registro: `http://127.0.0.1:8000/loteria/eliminar/<id>/` (POST con confirmación)
- Cerrar sesión: `http://127.0.0.1:8000/loteria/logout/`

## Qué incluye

- Login personalizado con backend hardcodeado en `loteria/auth_backends.py`.
- Dashboard privado para crear, editar y eliminar registros de sorteos.
- Página pública de consulta con listado, filtro por fecha y paginación.
- Formulario de registro con validación de número y fecha única.
- Edición de sorteos con validación de duplicados por fecha.
- Eliminación segura con confirmación previa.

## Consideraciones importantes

- Este backend de prueba es solo para desarrollo local.
- No usar en producción.
- Para producción, elimina `loteria.auth_backends.HardcodedTestUserBackend` de `AUTHENTICATION_BACKENDS` y crea usuarios reales con `python3 manage.py createsuperuser`.
- `DEBUG` está activado en `loteria_project/settings.py` y debe desactivarse en producción.
- La base de datos predeterminada es SQLite (`db.sqlite3`).
- El `SECRET_KEY` también es de desarrollo.

## Uso rápido

1. Activa el entorno virtual.
2. Ejecuta:
   ```bash
   python3 manage.py migrate
   python3 manage.py runserver
   ```
3. Abre `http://127.0.0.1:8000/loteria/login/`.
4. Ingresa con las credenciales de prueba.

## Archivos clave

- `loteria/auth_backends.py` — backend de autenticación hardcodeado.
- `loteria_project/settings.py` — configuración de Django y autenticación.
- `loteria/urls.py` — rutas de la app.
- `loteria/views.py` — lógica de registro, edición, eliminación y consulta.
- `loteria/templates/loteria/` — plantillas personalizadas de la aplicación.
