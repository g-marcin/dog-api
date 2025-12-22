from fastapi import FastAPI
from config import ROOT_PATH
from app.app_config import get_fastapi_config
from app.openapi import setup_custom_openapi
from app.middleware.cors import CustomCORSMiddleware
from app.routes import breeds, images

app = FastAPI(**get_fastapi_config(ROOT_PATH))
setup_custom_openapi(app)

app.add_middleware(CustomCORSMiddleware)

app.include_router(breeds.router)
app.include_router(images.router)

