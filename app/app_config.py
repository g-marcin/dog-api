from typing import Dict, Any
from fastapi.routing import APIRoute


def operation_id_from_route_name(route: APIRoute) -> str:
    return route.name


def get_fastapi_config(root_path: str = "") -> Dict[str, Any]:
    config = {
        "title": "dog-api",
        "description": "API for accessing dog breed images and information",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json",
        "generate_unique_id_function": operation_id_from_route_name,
    }
    config["root_path"] = root_path or ""
    return config

