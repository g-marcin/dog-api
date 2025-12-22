import re
from typing import List, Union, Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import config

allowed_origins_patterns: List[Union[str, re.Pattern]] = []

for origin in config.CORS_ORIGINS.split(","):
    origin = origin.strip()
    if not origin:
        continue
    if origin.startswith("/") and origin.endswith("/") and len(origin) > 2:
        regex_pattern = origin[1:-1]
        try:
            compiled_pattern = re.compile(regex_pattern)
            allowed_origins_patterns.append(compiled_pattern)
            print(f"CORS: Added regex pattern: {regex_pattern}")
        except re.error as e:
            print(f"Warning: Invalid regex pattern '{regex_pattern}': {e}")
    elif "*" in origin:
        escaped = re.escape(origin)
        pattern = escaped.replace(r"\*", ".*")
        compiled_pattern = re.compile(f"^{pattern}$")
        allowed_origins_patterns.append(compiled_pattern)
        print(f"CORS: Added wildcard pattern '{origin}' -> regex: ^{pattern}$")
    else:
        allowed_origins_patterns.append(origin)
        print(f"CORS: Added plain origin: {origin}")

def is_origin_allowed(origin: str) -> bool:
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
    async def dispatch(self, request: Request, call_next: Callable):
        origin = request.headers.get("origin")
        
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
        
        response = await call_next(request)
        
        if origin and is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
            response.headers["Access-Control-Allow-Headers"] = "*"
        
        return response

