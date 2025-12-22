from fastapi import APIRouter, HTTPException
from app.models import APIResponse, success_response
from app.services.breed_service import scan_breeds

router = APIRouter()

@router.get(
    "/breeds/list/all",
    response_model=APIResponse,
    tags=["Breeds"],
    summary="List all breeds",
    description="Returns a list of all available dog breeds and their sub-breeds"
)
async def list_all_breeds():
    breeds = scan_breeds()
    return success_response(breeds)

@router.get(
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
    
    return success_response(breeds[breed])

