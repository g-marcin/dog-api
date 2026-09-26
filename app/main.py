from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.base import BaseHTTPMiddleware

from app.app_config import get_fastapi_config
from app.middleware.cors import plain_origins
from app.model.database import engine
from app.openapi import setup_custom_openapi
from app.routes import breeds, descriptions, health, images, telemetry
from app.telemetry import setup_telemetry
from config import ROOT_PATH


class RootPathFixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.scope.get("root_path") is None:
            request.scope["root_path"] = ""
        return await call_next(request)


app = FastAPI(**get_fastapi_config(ROOT_PATH))
app.add_middleware(RootPathFixMiddleware)
setup_custom_openapi(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=plain_origins,
    allow_origin_regex=r"https://woof-app-ff670.*\.web\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)
setup_telemetry(app, engine)


@app.get("/", include_in_schema=False)
async def root(request: Request):
    return RedirectResponse(url=f"{request.scope.get('root_path', '').rstrip('/')}/docs")


app.include_router(breeds.router)
app.include_router(images.router)
app.include_router(health.router)
app.include_router(descriptions.router)
app.include_router(telemetry.router)
