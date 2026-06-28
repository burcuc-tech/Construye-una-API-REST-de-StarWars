# Lista de Lectura del Blog de Star Wars

Frontend React/Vite para consumir la API Flask del StarWars Blog. Permite explorar personajes, planetas y vehiculos, abrir detalles, buscar recursos y administrar favoritos.

## Funcionalidades

- Listado de `people`, `planets` y `vehicles` desde la API local.
- Vista detallada para cada recurso.
- Favoritos conectados con `/users/favorites` y `/favorite/...`.
- Buscador en la barra de navegacion.
- Cache local de recursos con `localStorage`.
- Imagenes con fallback local, imagenes oficiales mapeadas y Star Wars Visual Guide.
- Diseno responsive con Bootstrap y CSS personalizado.

## Configuracion

Copia `.env.example` y ajusta la URL del backend si hace falta:

```bash
VITE_API_URL=http://localhost:3000
```

En desarrollo tambien puedes dejar `VITE_API_URL` vacio y usar el proxy definido en `vite.config.js`.

## Comandos

```bash
npm install
npm run dev
npm run lint
npm run build
```

La aplicacion Vite se ejecuta por defecto en:

```text
http://localhost:5173
```

El backend Flask debe estar disponible en:

```text
http://localhost:3000
```

## Imagenes

La aplicacion busca imagenes en este orden:

1. Archivo local, por ejemplo `public/images/people/1.jpg`.
2. Imagen oficial mapeada desde StarWars.com Databank.
3. Star Wars Visual Guide como respaldo.
4. Fallback visual interno si ninguna imagen carga.
