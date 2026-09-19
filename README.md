# FastAPI Supabase Authentication API

A REST API built with **FastAPI** and **Supabase Authentication** that demonstrates a complete authentication flow with public and protected endpoints.

The project supports user signup, login, JWT-based authentication, protected routes, logout, and interactive API testing through Swagger UI.

## Features

- User signup with email and password
- User login using Supabase Authentication
- JWT access token authentication
- Protected API endpoints
- User profile retrieval
- Protected dashboard
- User logout
- Public endpoints
- Swagger UI with Bearer token authorization
- Environment variables for secure configuration

## Tech Stack

- Python
- FastAPI
- Supabase
- Uvicorn
- python-dotenv
- JWT / Bearer Authentication
- Swagger UI

## Project Structure

```text
auth_practice/
│
├── main.py
├── auth_routes.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── screenshots/
    └── swagger-ui.png
```

> `.env` and `venv/` should not be committed to GitHub.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd auth_practice
```

Replace the repository URL above with the actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

You can copy the provided example:

```bash
cp .env.example .env
```

Add your own Supabase credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
```

You can find these values in your Supabase project settings.

Do **not** commit your real `.env` file or secret credentials to GitHub.

The `.env.example` file should contain only placeholder values:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Run the API

Start the FastAPI development server:

```bash
uvicorn main:app --reload --port 3000
```

The API will be available at:

```text
http://localhost:3000
```

Swagger UI:

```text
http://localhost:3000/docs
```

## API Reference

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| GET | `/` | No | Check that the API is running |
| POST | `/auth/signup` | No | Create a new user account |
| POST | `/auth/login` | No | Log in and receive access and refresh tokens |
| GET | `/public/info` | No | Access public information |
| GET | `/protected/profile` | Bearer Token | Return authenticated user's profile |
| GET | `/protected/dashboard` | Bearer Token | Access the authenticated user's dashboard |
| POST | `/auth/logout` | Bearer Token | Log out the authenticated user |

## Authentication Flow

After creating an account, log in using:

```http
POST /auth/login
```

Example request body:

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

A successful login returns an access token and refresh token.

Example:

```json
{
  "access token": "YOUR_ACCESS_TOKEN",
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

The access token is used to access protected endpoints.

## Testing Protected Routes with Swagger UI

1. Start the FastAPI server.
2. Open `http://localhost:3000/docs`.
3. Log in using `POST /auth/login`.
4. Copy the returned access token.
5. Click the **Authorize** button at the top of Swagger UI.
6. Paste the access token into the authorization field.
7. Click **Authorize**.
8. Test `/protected/profile` or `/protected/dashboard`.

FastAPI's `HTTPBearer` security scheme automatically adds the authorization controls and lock icons to protected endpoints in Swagger UI.

## Swagger UI

The Swagger interface provides interactive documentation for testing both public and authenticated endpoints.

![Swagger UI](screenshots/swagger-ui.png)

## Authentication Implementation

Protected routes use a reusable FastAPI dependency:

```python
security = HTTPBearer()

async def verify_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return response.user
```

Any endpoint that uses:

```python
Depends(verify_user)
```

requires a valid Bearer access token.

For example:

```python
@app.get("/protected/profile")
async def protected_profile(user = Depends(verify_user)):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }
```

## Security

Sensitive configuration is stored using environment variables rather than hard-coded credentials.

The `.gitignore` file should include:

```gitignore
.env
venv/
__pycache__/
*.pyc
.DS_Store
```

Never commit Supabase keys, access tokens, refresh tokens, passwords, or other private credentials.

## Quick Start

A new developer can run the project with:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd auth_practice

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Add your Supabase credentials to .env

uvicorn main:app --reload --port 3000
```

Then open:

```text
http://localhost:3000/docs
```

The API is now ready for signup, login, and authenticated endpoint testing.