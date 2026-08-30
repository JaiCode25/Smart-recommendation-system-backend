# Nexus — Smart Recommendation System UI

A standalone HTML, CSS, and JavaScript frontend for the Smart Recommendation System backend. It reads the backend API directly and remains presentable using built-in demo content when the API is offline.

## Run it

1. Start the FastAPI backend first. From this frontend folder, run:

   ```powershell
   powershell -ExecutionPolicy Bypass -File ..\start-backend.ps1
   ```

2. Confirm that [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health) opens successfully.
3. Open `index.html` in a browser. The top-right label will change from **Demo mode** to **Live connection**.

The default API location is `http://127.0.0.1:8000/api`. Change the `API` value at the beginning of `script.js` if your backend is at a different address.

The FastAPI CORS configuration must permit the origin from which you serve the page.

## Current connection check

The frontend expects the backend at `http://127.0.0.1:8000`. If the top-right label says **Demo mode**, either the FastAPI server is not running or it is using a different address. Start it using the command above, or update the `API` value in `script.js` to match the server address.

## Backend integration

- Register: `POST /api/auth/register` with `username`, `email`, and `password`
- Sign in: `POST /api/auth/login` with `username` and `password`
- Feed: `GET /api/recommendations?user_id=1&limit=12`
- Explore: `GET /api/items?limit=50`
- Interactions: `POST /api/interactions` with `user_id`, `item_id`, and `interaction_type`
- Interest profile: `GET /api/users/1/expanded-interests`

The Tag Graph view is deliberately designed as a clear visual explanation of the weighted tag graph. It can be upgraded to load `GET /api/graph` when the backend graph response is finalized.

## Sign-in

Use **New here? Create an account** on the login page to register once. Passwords are stored as salted PBKDF2 hashes in the SQLite database, never as plain text. The original seeded `alex_dev` account does not have a password, so create your own account before signing in.
