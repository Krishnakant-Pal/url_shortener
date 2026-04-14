# URL Shortener API

A production-ready URL Shortener REST API built with Django REST Framework.

## Features

- JWT Authentication (register, login, refresh token)
- Shorten any URL with auto-generated short code
- Custom short codes (e.g. `/r/myresume`)
- URL expiration — links auto-expire after set date
- Redis caching on redirects for fast response
- Async click tracking via Celery
- Analytics per URL and summary across all URLs
- Rate limiting on URL creation
- Swagger UI at `/swagger/`
- Fully Dockerized

## Tech Stack

- **Backend** — Django + Django REST Framework
- **Database** — PostgreSQL
- **Cache/Broker** — Redis
- **Async Tasks** — Celery
- **Auth** — SimpleJWT
- **Docs** — drf-yasg (Swagger)
- **Deployment** — Railway

## Getting Started

### Prerequisites
- Docker Desktop

### Run Locally

1. Clone the repo
```bash
   git clone https://github.com/yourusername/url_shortener.git
   cd url_shortener
```

2. Create `.env` file
```bash
   cp .env.example .env
```

3. Start all services
```bash
   docker-compose up --build
```

4. Run migrations
```bash
   docker-compose exec web python manage.py migrate
```

5. Visit `http://localhost:8000/swagger/`

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login, get JWT token | No |
| POST | `/api/auth/refresh/` | Refresh access token | No |
| GET | `/api/urls/` | List all your URLs | Yes |
| POST | `/api/urls/` | Create short URL | Yes |
| GET | `/api/urls/{id}/` | Get single URL | Yes |
| PUT | `/api/urls/{id}/` | Update URL | Yes |
| DELETE | `/api/urls/{id}/` | Delete URL | Yes |
| GET | `/api/urls/r/{short_code}/` | Redirect to original | No |
| GET | `/api/urls/analytics/{short_code}/` | URL analytics | Yes |
| GET | `/api/urls/summary/` | Total URLs and clicks | Yes |

## Environment Variables

See `.env.example` for all required variables.
