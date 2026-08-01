from fastapi import APIRouter, HTTPException
from app.model.models import APIResponse, success_response
from app.model.responses import PerformanceMessage
from app.services.health_service import check_system_performance, check_health

import os

router = APIRouter()

# @deprecated @redundant: OS-level cpu/memory/disk stats duplicate what
# node_exporter already exposes for this machine (node_cpu_seconds_total,
# node_memory_*, node_filesystem_*) and are scraped into Grafana Cloud already.
# Kept for now for any existing consumers; do not build new monitoring on this.
@router.get(
    "/performance",
    response_model=APIResponse[PerformanceMessage],
    tags=["health"],
    summary="check api os performance",
    description="check api os performance cpu, memory, disk"
)
def system_performance():
    system_performance_metrics = check_system_performance()
    return success_response(system_performance_metrics)

@router.get(
    "/healthcheck",
    response_model=APIResponse[str],
    tags=["health"],
    summary="check api health",
    description="check api health, returns ok 200 if healthy"
)
def system_health():
    is_healthy = check_health()
    return success_response(is_healthy)
