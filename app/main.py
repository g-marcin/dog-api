from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import ROOT_PATH
from app.app_config import get_fastapi_config
from app.openapi import setup_custom_openapi
from app.middleware.cors import plain_origins, is_origin_allowed
from app.routes import breeds, images, health

app = FastAPI(**get_fastapi_config(ROOT_PATH))
setup_custom_openapi(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=plain_origins,
    allow_origin_regex=r"https://woof-app-ff670.*\.web\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(breeds.router)
app.include_router(images.router)
app.include_router(health.router)

