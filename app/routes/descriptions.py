from fastapi import APIRouter, HTTPException, Request
from opentelemetry import trace
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
async def breed_description(breed: str, request: Request):
    # Full URL + request/response bodies as span attributes, scoped to this
    # one route as a test of body capture -- not enabled globally, since
    # auto-instrumentation deliberately excludes bodies (size/PII risk).
    span = trace.get_current_span()
    span.set_attribute("http.request.full_url", str(request.url))
    span.set_attribute("http.request.body", (await request.body()).decode("utf-8", errors="replace"))

    description = get_breed_description(breed)

    if not description:
        raise HTTPException(status_code=404, detail=f"Description for breed '{breed}' not found")

    response = success_response(description)
    span.set_attribute("http.response.body", response.model_dump_json())
    return response


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
