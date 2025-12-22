from typing import Dict, Any
from fastapi import FastAPI

def get_openapi_schema() -> Dict[str, Any]:
    return {
        "openapi": "3.0.2",
        "info": {
            "title": "Dog CEO API",
            "description": "API for accessing dog breed images and information",
            "version": "1.0.0",
            "contact": {
                "name": "API Support"
            }
        },
        "tags": [
            {
                "name": "Breeds",
                "description": "Operations related to dog breeds and sub-breeds"
            },
            {
                "name": "Images",
                "description": "Operations related to dog images"
            }
        ],
        "servers": [
            {
                "url": "http://localhost:8000",
                "description": "Local development server"
            }
        ]
    }

def setup_custom_openapi(app: FastAPI):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        from fastapi.openapi.utils import get_openapi
        import os
        custom_spec = get_openapi_schema()
        root_path = os.getenv("ROOT_PATH", "")
        
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        if "tags" in custom_spec:
            openapi_schema["tags"] = custom_spec["tags"]
        if "servers" in custom_spec:
            if root_path:
                custom_spec["servers"][0]["url"] = root_path
            openapi_schema["servers"] = custom_spec["servers"]
        if "info" in custom_spec:
            openapi_schema["info"].update(custom_spec["info"])
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi
