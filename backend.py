import uvicorn

from care_on_live_app import app


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
