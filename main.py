import uvicorn

from app.main import app
from config import PORT, ROOT_PATH


def main():
    uvicorn.run(app, host="localhost", port=PORT, root_path=ROOT_PATH if ROOT_PATH else None)


if __name__ == "__main__":
    main()
