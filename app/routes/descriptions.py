from fastapi import APIRouter, HTTPException
from app.model.models import APIResponse, success_response
from app.model.responses import DescriptionMessage
from app.services.description_service import get_breed_description, get_variant_description

router = APIRouter()


@router.get(
    "/breed/{breed}/description",
    response_model=APIResponse[DescriptionMessage],
    tags=["Descriptions"],
    summary="Get breed description",
    description="Returns the description for a specific breed in multiple languages",
)
async def breed_description(breed: str):
    description = get_breed_description(breed)

    if not description:
        raise HTTPException(status_code=404, detail=f"Description for breed '{breed}' not found")

    return success_response(description)


@router.get(
    "/breed/{breed}/{variant}/description",
    response_model=APIResponse[DescriptionMessage],
    tags=["Descriptions"],
    summary="Get variant description",
    description="Returns the description for a specific breed variant in multiple languages",
)
async def variant_description(breed: str, variant: str):
    description = get_variant_description(breed, variant)

    if not description:
        raise HTTPException(
            status_code=404,
            detail=f"Description for variant '{variant}' of breed '{breed}' not found",
        )

    return success_response(description)
