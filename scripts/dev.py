#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from config import PORT
from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=True)

