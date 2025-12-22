import random
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models import APIResponse, success_response
from app.services.breed_service import get_breed_images, get_image_url, get_all_images
import config

router = APIRouter()

@router.get(
    "/breeds/image/random",
    response_model=APIResponse,
    tags=["Images"],
    summary="Get random image",
    description="Returns a random dog image URL from all available breeds"
)
async def random_image():
    all_images = get_all_images()
    
    if not all_images:
        raise HTTPException(status_code=404, detail="No images found")
    
    random_image = random.choice(all_images)
    return success_response(get_image_url(random_image))

@router.get(
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
    return success_response(image_urls)

@router.get(
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
    return success_response(get_image_url(random_image))

@router.get(
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
    return success_response(image_urls)

@router.get(
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
    return success_response(get_image_url(random_image))

@router.get(
    "/images/{file_path:path}",
    tags=["Images"],
    summary="Serve image file",
    description="Serves the actual image file by path"
)
async def serve_image(file_path: str):
    image_path = config.ASSETS_DIR / file_path
    
    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path)

