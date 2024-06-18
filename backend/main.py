from fastapi import FastAPI
from uvicorn import run

from api import auth


app = FastAPI()
app.include_router(auth.router)


if __name__ == "__main__":
    run("main:app", reload=True, workers=9)
