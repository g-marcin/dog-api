# Dog API

API for accessing dog breed images and information.

## Project Structure

```
dog-api/
├── app/                          # Application code
│   ├── __init__.py
│   ├── main.py                  # FastAPI app instance
│   ├── models.py                # Domain models (Status, APIResponse)
│   ├── app_config.py            # FastAPI configuration
│   ├── openapi.py               # OpenAPI documentation setup
│   ├── middleware/              # Middleware
│   │   ├── __init__.py
│   │   └── cors.py              # CORS middleware
│   ├── routes/                  # API routes
│   │   ├── __init__.py
│   │   ├── breeds.py            # Breed endpoints
│   │   └── images.py            # Image endpoints
│   └── services/                # Business logic
│       ├── __init__.py
│       └── breed_service.py     # Breed/image operations
├── config.py                    # Environment configuration
├── main.py                      # Entry point (runs uvicorn)
├── server.py                    # Legacy file (deprecated)
├── requirements.txt             # Python dependencies
├── env.example                  # Environment variables template
├── nginx.conf                   # Nginx configuration
└── reload-nginx.sh              # Nginx reload script
```

## Structure Overview

- **Root level**: Configuration files, entry point, deployment files
- **`app/`**: All application code (similar to `src/` in JavaScript projects)
  - **`models.py`**: Pydantic models and response utilities
  - **`routes/`**: API endpoint handlers
  - **`services/`**: Business logic layer
  - **`middleware/`**: HTTP middleware (CORS, etc.)
  - **`openapi.py`**: OpenAPI/Swagger documentation configuration
  - **`app_config.py`**: FastAPI application configuration
  - **`main.py`**: FastAPI app instance creation

## Running the Application

### Using Makefile

```bash
make dev          # Run development server
make start        # Run with auto-reload
make install      # Install dependencies
make test         # Run tests
make lint         # Lint code
make format       # Format code
make clean        # Clean cache files
```

### Using Python directly

```bash
python main.py                    # Run development server
uvicorn app.main:app --reload    # Run with auto-reload
```

The application will start on `http://localhost:8000` (or the port specified in `config.py`).

