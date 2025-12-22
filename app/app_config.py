from typing import Dict, Any

def get_fastapi_config(root_path: str = "") -> Dict[str, Any]:
    config = {
        "title": "dog-api",
        "description": "API for accessing dog breed images and information",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json"
    }
    if root_path:
        config["root_path"] = root_path
    return config

