# API y Lista de Lectura del Blog de Star Wars

Proyecto full-stack de Star Wars con una API REST en Flask, modelos con SQLAlchemy, Flask Admin, migraciones de base de datos y un frontend React/Vite para la lista de lectura.

La aplicacion permite explorar personajes, planetas y vehiculos, abrir paginas de detalle y agregar o eliminar favoritos. La autenticacion todavia no esta implementada, por eso la API usa un usuario actual fijo (`CURRENT_USER_ID = 1`) y los usuarios se pueden administrar desde Flask Admin.

## Tecnologias

- Backend: Python, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Admin, PostgreSQL/SQLite
- Frontend: React, Vite, React Router, Bootstrap, CSS
- Herramientas: Pipenv, npm, ESLint, pycodestyle, migraciones Alembic

## Estructura del Proyecto

```text
src/                         Codigo fuente de la API Flask
migrations/                  Migraciones de Alembic
Starwars-blog-reading-list/  Frontend React/Vite
```

## Funcionalidades del Backend

- `GET /people`
- `GET /people/<id>`
- `POST /people`
- `PUT /people/<id>`
- `DELETE /people/<id>`
- `GET /planets`
- `GET /planets/<id>`
- `POST /planets`
- `PUT /planets/<id>`
- `DELETE /planets/<id>`
- `GET /vehicles`
- `GET /vehicles/<id>`
- `POST /vehicles`
- `PUT /vehicles/<id>`
- `DELETE /vehicles/<id>`
- `GET /users`
- `GET /users/favorites`
- `POST /favorite/people/<id>`
- `POST /favorite/planet/<id>`
- `POST /favorite/vehicle/<id>`
- `DELETE /favorite/people/<id>`
- `DELETE /favorite/planet/<id>`
- `DELETE /favorite/vehicle/<id>`

Los favoritos tienen una restriccion en la base de datos para que cada fila apunte exactamente a un tipo de entidad: personaje, planeta o vehiculo.

## Funcionalidades del Frontend

- Catalogo responsive de personajes, planetas y vehiculos
- Paginas de detalle para cada tipo de recurso
- Agregar y eliminar favoritos conectados con la API Flask
- Menu de favoritos en la barra de navegacion
- Buscador por nombre en las tres categorias
- Sistema de imagenes con fallback local, imagenes oficiales mapeadas y Star Wars Visual Guide
- URL de API configurable para deploy con `VITE_API_URL`

## Instalacion

Instala las dependencias del backend:

```bash
pipenv install
```

Instala las dependencias del frontend:

```bash
cd Starwars-blog-reading-list
npm install
```

No hace falta descargar nada extra si esas dependencias ya estan instaladas en el workspace.

## Variables de Entorno

El backend usa `DATABASE_URL` si existe. Si no esta definida, usa SQLite en `/tmp/test.db`.

El frontend puede usar el proxy local de Vite o una URL de API desplegada:

```bash
cd Starwars-blog-reading-list
cp .env.example .env
```

Ejemplo:

```bash
VITE_API_URL=http://localhost:3000
```

Para desarrollo local con el proxy de Vite incluido, `VITE_API_URL` tambien puede quedar vacio.

## Ejecutar Localmente

Prepara la base de datos y carga datos de ejemplo:

```bash
pipenv run flask --app src/app.py db upgrade
pipenv run flask --app src/app.py seed
```

Inicia el backend:

```bash
pipenv run start
```

URL del backend:

```text
http://localhost:3000
```

Inicia el frontend en otra terminal:

```bash
cd Starwars-blog-reading-list
npm run dev
```

URL del frontend:

```text
http://localhost:5173
```

## Controles de Calidad

Backend:

```bash
python -m py_compile src/app.py src/models.py src/admin.py src/utils.py src/wsgi.py
pipenv run pycodestyle --config=pycodestyle.cfg src migrations/versions
```

Frontend:

```bash
cd Starwars-blog-reading-list
npm run lint
npm run build
```

## Admin

Flask Admin esta disponible en:

```text
http://localhost:3000/admin
```

Como todavia no hay autenticacion, los usuarios se crean directamente desde Flask Admin o mediante seed de la base de datos.
