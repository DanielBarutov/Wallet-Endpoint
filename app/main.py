from fastapi import FastAPI
from app.api.api_route import router

app = FastAPI()
app.include_router(router)
