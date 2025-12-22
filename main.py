import uvicorn
from config import PORT, ROOT_PATH
from app.main import app

def main():
    uvicorn.run(app, host="localhost", port=PORT, root_path=ROOT_PATH if ROOT_PATH else None)

if __name__ == "__main__":
    main()

