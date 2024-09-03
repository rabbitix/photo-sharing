from fastapi import FastAPI

from src.services.router import router

app = FastAPI()

app.include_router(router)
