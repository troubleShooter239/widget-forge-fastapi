from fastapi import FastAPI
from uvicorn import run


app = FastAPI()


if __name__ == "__main__":
    run("main:app", reload=True, workers=9)
