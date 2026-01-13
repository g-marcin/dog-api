from fastapi import APIRouter, HTTPException
from app.models import APIResponse, success_response
from app.services.health_service import check_system_performance, check_health

import os

router = APIRouter()

@router.get(
    "/performance",
    response_model=APIResponse,
    tags=["health"],
    summary="check api os performance",
    description="check api os performance cpu, memory, disk"
)
def system_performance():
    system_performance_metrics = check_system_performance()
    return success_response(system_performance_metrics)

@router.get(
    "/healthcheck",
    response_model=APIResponse,
    tags=["health"],
    summary="check api health",
    description="check api health, returns ok 200 if healthy"
)
def system_health():
    is_healthy = check_health()
    return success_response(is_healthy)
