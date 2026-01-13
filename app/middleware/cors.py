import re
from typing import List, Tuple
import config

def parse_cors_origins() -> Tuple[List[str], List[re.Pattern]]:
    plain_origins = []
    regex_patterns = []
    
    for origin in config.CORS_ORIGINS.split(","):
        origin = origin.strip()
        if not origin:
            continue
        if origin.startswith("/") and origin.endswith("/") and len(origin) > 2:
            regex_pattern = origin[1:-1]
            try:
                compiled_pattern = re.compile(regex_pattern)
                regex_patterns.append(compiled_pattern)
                print(f"CORS: Added regex pattern: {regex_pattern}")
            except re.error as e:
                print(f"Warning: Invalid regex pattern '{regex_pattern}': {e}")
        elif "*" in origin:
            escaped = re.escape(origin)
            pattern = escaped.replace(r"\*", ".*")
            compiled_pattern = re.compile(f"^{pattern}$")
            regex_patterns.append(compiled_pattern)
            print(f"CORS: Added wildcard pattern '{origin}' -> regex: ^{pattern}$")
        else:
            plain_origins.append(origin)
            print(f"CORS: Added plain origin: {origin}")
    
    return plain_origins, regex_patterns

plain_origins, regex_patterns = parse_cors_origins()

def is_origin_allowed(origin: str) -> bool:
    if not origin:
        return False
    if origin in plain_origins:
        return True
    for pattern in regex_patterns:
        if pattern.match(origin):
            return True
    return False
