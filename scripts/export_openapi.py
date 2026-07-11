import json
from pathlib import Path

from app.main import app

ROOT = Path(__file__).parent.parent
OUTPUT_PATH = ROOT / "openapi.json"
PACKAGE_OUTPUT_PATH = ROOT / "packages" / "api-types" / "openapi.json"

if __name__ == "__main__":
    schema = app.openapi()
    content = json.dumps(schema, indent=2)
    PACKAGE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(content)
    PACKAGE_OUTPUT_PATH.write_text(content)
    print(f"Wrote OpenAPI schema to {OUTPUT_PATH} and {PACKAGE_OUTPUT_PATH}")
