# Live Demo Deployment

Use this setup for the live demo:

- Frontend: Vercel
- Backend API: Render
- Database: Supabase PostgreSQL

## 1. Supabase

Create a Supabase project and copy the PostgreSQL connection string.

Use the URI format that starts with:

```text
postgresql://...
```

If Supabase gives you a URI that starts with `postgres://`, the backend also handles it, but `postgresql://` is preferred.

## 2. Render Backend

Create a Render Blueprint from this repository or connect the repo as a Python web service.

The service config is in `render.yaml`.

Set this Render environment variable manually:

```text
DATABASE_URL=<your Supabase PostgreSQL connection string>
```

The build command runs migrations and seeds the demo data automatically:

```bash
./render_build.sh
```

Expected backend URL:

```text
https://starwars-blog-api.onrender.com
```

If Render gives you a different URL, update the destinations in `frontend/vercel.json`.

## 3. Vercel Frontend

Import the same GitHub repository in Vercel.

Set the Vercel root directory to:

```text
frontend
```

Vercel will build the React app from `frontend/package.json`.

The `frontend/vercel.json` file proxies API calls such as `/people`, `/planets`, `/vehicles`, `/users`, and `/favorite/...` to the Render backend, then falls back to `index.html` for React routes.

## 4. Smoke Test

After both deploys finish, check:

```text
https://starwars-blog-api.onrender.com/people
```

Then open the Vercel URL and verify that people, planets, vehicles, and favorites load.
