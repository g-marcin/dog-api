from fastapi import APIRouter, HTTPException
from app.model.models import APIResponse, success_response
from app.services.breed_service import get_breeds

router = APIRouter()


@router.get(
    "/breeds/list/all",
    response_model=APIResponse,
    tags=["Breeds"],
    summary="List all breeds",
    description="Returns a list of all available dog breeds and their sub-breeds"
)
async def list_all_breeds():
    breeds = get_breeds()
    return success_response(breeds)


@router.get(
    "/breed/{breed}/list",
    response_model=APIResponse,
    tags=["Breeds"],
    summary="Get breed sub-breeds",
    description="Returns a list of sub-breeds for a specific breed -"
)
async def breed_subbreeds(breed: str):
    breeds = get_breeds()

    if breed not in breeds:
        raise HTTPException(status_code=404, detail=f"Breed '{breed}' not found")

    return success_response(breeds[breed])

