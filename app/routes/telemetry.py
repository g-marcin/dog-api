import os

import grpc
from fastapi import APIRouter, Request, Response
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceRequest
from opentelemetry.proto.collector.trace.v1.trace_service_pb2_grpc import TraceServiceStub

from app.telemetry import grpc_headers, grpc_target

router = APIRouter()


@router.post("/telemetry/traces", include_in_schema=False)
async def relay_traces(request: Request):
    body = await request.body()

    otlp_request = ExportTraceServiceRequest()
    try:
        otlp_request.ParseFromString(body)
    except Exception:
        return Response(status_code=400)

    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    headers_env = os.environ.get("OTEL_EXPORTER_OTLP_HEADERS")
    if not endpoint or not headers_env:
        return Response(status_code=503)

    channel = grpc.secure_channel(grpc_target(endpoint), grpc.ssl_channel_credentials())
    try:
        stub = TraceServiceStub(channel)
        otlp_response = stub.Export(otlp_request, metadata=grpc_headers(headers_env), timeout=10)
    except grpc.RpcError as exc:
        return Response(status_code=502, content=str(exc.details()).encode())
    finally:
        channel.close()

    return Response(content=otlp_response.SerializeToString(), media_type="application/x-protobuf")
