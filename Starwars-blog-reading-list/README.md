# Lista de Lectura del Blog de Star Wars

Aplicacion React creada con Vite para explorar la API local del StarWars Blog. Permite consultar personajes, planetas y vehiculos, abrir una vista detallada y guardar elementos en favoritos.

## Funcionalidades

- Listado de personajes, planetas y vehiculos desde la API Flask del proyecto.
- Vista detallada para `people`, `planets` y `vehicles`.
- Favoritos globales conectados con los endpoints `/users/favorites` y `/favorite/...`.
- Buscador rapido por nombre en las tres categorias.
- Cache local de recursos con `localStorage` para reducir llamadas repetidas.
- Tarjetas con imagen local, imagen oficial mapeada y fallback visual.
- Diseno responsive con Bootstrap y CSS personalizado.

## Configuracion

Copia `.env.example` y ajusta la URL del backend si hace falta:

```bash
VITE_API_URL=http://localhost:3000
```

En desarrollo tambien puedes dejar `VITE_API_URL` vacio y usar el proxy de Vite definido en `vite.config.js`.

## Comandos

```bash
npm install
npm run dev
npm run lint
npm run build
```

La aplicacion Vite se ejecuta por defecto en `http://localhost:5173/`. El backend Flask debe estar disponible en `http://localhost:3000/` o en la URL configurada con `VITE_API_URL`.

## Imagenes

La aplicacion busca imagenes en este orden:

1. Archivo local, por ejemplo `public/images/people/1.jpg`.
2. Imagen oficial mapeada desde StarWars.com Databank.
3. Star Wars Visual Guide como respaldo.
4. Fallback visual interno si ninguna imagen carga.
