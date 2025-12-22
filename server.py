from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from pathlib import Path
import random
import os
import re
from typing import Dict, List, Union, Callable

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

os.environ.setdefault("ROOT_PATH", "/dog-api")
os.environ.setdefault("BASE_URL_API", "http://localhost:8000")
os.environ.setdefault("BASE_URL_IMG", "https://mgrzmil.dev")
os.environ.setdefault("PORT", "8000")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost:5174,https://mgrzmil.dev,https://woof-app-ff670*.web.app")

try:
    from .openapi import APIResponse, get_fastapi_config, setup_custom_openapi
except ImportError:
    from openapi import APIResponse, get_fastapi_config, setup_custom_openapi

ROOT_PATH = os.getenv("ROOT_PATH", "")
app = FastAPI(**get_fastapi_config(ROOT_PATH))
setup_custom_openapi(app)

cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost:5174,https://mgrzmil.dev,https://woof-app-ff670*.web.app")
allowed_origins_patterns: List[Union[str, re.Pattern]] = []

for origin in cors_origins_str.split(","):
    origin = origin.strip()
    if not origin:
        continue
    # Check if it's a regex pattern (wrapped in /pattern/)
    if origin.startswith("/") and origin.endswith("/") and len(origin) > 2:
        # Extract regex pattern and compile it
        regex_pattern = origin[1:-1]
        try:
            compiled_pattern = re.compile(regex_pattern)
            allowed_origins_patterns.append(compiled_pattern)
            print(f"CORS: Added regex pattern: {regex_pattern}")
        except re.error as e:
            # If regex is invalid, log error and skip
            print(f"Warning: Invalid regex pattern '{regex_pattern}': {e}")
    elif "*" in origin:
        # Convert wildcard pattern to regex
        # Escape all special regex characters first, then replace escaped * with .*
        # Use re.escape to escape everything, then unescape the * wildcards
        escaped = re.escape(origin)
        # Replace escaped asterisks (\*) with regex wildcard (.*)
        pattern = escaped.replace(r"\*", ".*")
        compiled_pattern = re.compile(f"^{pattern}$")
        allowed_origins_patterns.append(compiled_pattern)
        print(f"CORS: Added wildcard pattern '{origin}' -> regex: ^{pattern}$")
    else:
        # Plain string origin
        allowed_origins_patterns.append(origin)
        print(f"CORS: Added plain origin: {origin}")

def is_origin_allowed(origin: str) -> bool:
    """Check if an origin is allowed based on our patterns."""
    if not origin:
        return False
    for pattern in allowed_origins_patterns:
        if isinstance(pattern, re.Pattern):
            if pattern.match(origin):
                print(f"CORS: Origin '{origin}' matched pattern '{pattern.pattern}'")
                return True
        elif pattern == origin:
            print(f"CORS: Origin '{origin}' matched exact string '{pattern}'")
            return True
    print(f"CORS: Origin '{origin}' not allowed")
    return False

class CustomCORSMiddleware(BaseHTTPMiddleware):
    """Custom CORS middleware that handles both plain strings and regex patterns."""
    async def dispatch(self, request: Request, call_next: Callable):
        origin = request.headers.get("origin")
        
        # Handle preflight OPTIONS request
        if request.method == "OPTIONS":
            if origin and is_origin_allowed(origin):
                response = Response()
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
                response.headers["Access-Control-Allow-Headers"] = "*"
                response.headers["Access-Control-Allow-Credentials"] = "true"
                response.headers["Access-Control-Max-Age"] = "3600"
                return response
            else:
                return Response(status_code=403)
        
        # Process the request
        response = await call_next(request)
        
        # Add CORS headers to response if origin is allowed
        if origin and is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
            response.headers["Access-Control-Allow-Headers"] = "*"
        
        return response

# Use custom middleware that handles both plain strings and regex patterns
app.add_middleware(CustomCORSMiddleware)

ASSETS_DIR = Path(__file__).parent.parent / "dog-assets"
BASE_URL_API = os.getenv("BASE_URL_API", "http://localhost:8000")
BASE_URL_IMG = os.getenv("BASE_URL_IMG", "https://mgrzmil.dev")
if ROOT_PATH:
    BASE_URL_API = BASE_URL_API.rstrip("/") + ROOT_PATH
    BASE_URL_IMG = BASE_URL_IMG.rstrip("/") + ROOT_PATH

def scan_breeds() -> Dict[str, List[str]]:
    breeds = {}
    if not ASSETS_DIR.exists():
        return breeds
    
    for breed_dir in ASSETS_DIR.iterdir():
        if not breed_dir.is_dir():
            continue
        
        breed_name = breed_dir.name
        sub_breeds = []
        
        for item in breed_dir.iterdir():
            if item.is_dir():
                sub_breeds.append(item.name)
        
        breeds[breed_name] = sub_breeds if sub_breeds else []
    
    return breeds

def get_breed_images(breed: str, sub_breed: str = None) -> List[Path]:
    breed_path = ASSETS_DIR / breed
    
    if not breed_path.exists():
        return []
    
    images = []
    
    if sub_breed:
        sub_breed_path = breed_path / sub_breed
        if sub_breed_path.exists() and sub_breed_path.is_dir():
            images.extend([item for item in sub_breed_path.iterdir() if item.suffix.lower() in ['.jpg', '.jpeg', '.png']])
    else:
        for item in breed_path.iterdir():
            if item.is_file() and item.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                images.append(item)
            elif item.is_dir():
                for img in item.rglob('*'):
                    if img.is_file() and img.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        images.append(img)
    
    return images

def get_image_url(image_path: Path) -> str:
    relative_path = image_path.relative_to(ASSETS_DIR)
    return f"{BASE_URL_IMG}/images/{relative_path.as_posix()}"

@app.get(
    "/breeds/list/all",
    response_model=APIResponse,
    tags=["Breeds"],
    summary="List all breeds",
    description="Returns a list of all available dog breeds and their sub-breeds"
)
async def list_all_breeds():
    breeds = scan_breeds()
    return {"status": "success", "message": breeds}

@app.get(
    "/breeds/image/random",
    response_model=APIResponse,
    tags=["Images"],
    summary="Get random image",
    description="Returns a random dog image URL from all available breeds"
)
async def random_image():
    all_images = []
    
    for breed_dir in ASSETS_DIR.iterdir():
        if not breed_dir.is_dir():
            continue
        
        images = get_breed_images(breed_dir.name)
        all_images.extend(images)
    
    if not all_images:
        raise HTTPException(status_code=404, detail="No images found")
    
    random_image = random.choice(all_images)
    return {"status": "success", "message": get_image_url(random_image)}

@app.get(
    "/breed/{breed}/images",
    response_model=APIResponse,
    tags=["Images"],
    summary="Get breed images",
    description="Returns all image URLs for a specific breed"
)
async def breed_images(breed: str):
    images = get_breed_images(breed)
    
    if not images:
        raise HTTPException(status_code=404, detail=f"Breed '{breed}' not found or has no images")
    
    image_urls = [get_image_url(img) for img in images]
    return {"status": "success", "message": image_urls}

@app.get(
    "/breed/{breed}/list",
    response_model=APIResponse,
    tags=["Breeds"],
    summary="Get breed sub-breeds",
    description="Returns a list of sub-breeds for a specific breed"
)
async def breed_subbreeds(breed: str):
    breeds = scan_breeds()
    
    if breed not in breeds:
        raise HTTPException(status_code=404, detail=f"Breed '{breed}' not found")
    
    return {"status": "success", "message": breeds[breed]}

@app.get(
    "/breed/{breed}/images/random",
    response_model=APIResponse,
    tags=["Images"],
    summary="Get random breed image",
    description="Returns a random image URL for a specific breed"
)
async def random_breed_image(breed: str):
    images = get_breed_images(breed)
    
    if not images:
        raise HTTPException(status_code=404, detail=f"Breed '{breed}' not found or has no images")
    
    random_image = random.choice(images)
    return {"status": "success", "message": get_image_url(random_image)}

@app.get(
    "/breed/{breed}/{subbreed}/images",
    response_model=APIResponse,
    tags=["Images"],
    summary="Get sub-breed images",
    description="Returns all image URLs for a specific sub-breed"
)
async def subbreed_images(breed: str, subbreed: str):
    images = get_breed_images(breed, subbreed)
    
    if not images:
        raise HTTPException(status_code=404, detail=f"Sub-breed '{breed}/{subbreed}' not found or has no images")
    
    image_urls = [get_image_url(img) for img in images]
    return {"status": "success", "message": image_urls}

@app.get(
    "/breed/{breed}/{subbreed}/images/random",
    response_model=APIResponse,
    tags=["Images"],
    summary="Get random sub-breed image",
    description="Returns a random image URL for a specific sub-breed"
)
async def random_subbreed_image(breed: str, subbreed: str):
    images = get_breed_images(breed, subbreed)
    
    if not images:
        raise HTTPException(status_code=404, detail=f"Sub-breed '{breed}/{subbreed}' not found or has no images")
    
    random_image = random.choice(images)
    return {"status": "success", "message": get_image_url(random_image)}

@app.get(
    "/images/{file_path:path}",
    tags=["Images"],
    summary="Serve image file",
    description="Serves the actual image file by path"
)
async def serve_image(file_path: str):
    image_path = ASSETS_DIR / file_path
    
    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

