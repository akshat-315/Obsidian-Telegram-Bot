from fastapi import FastAPI
from contextlib import asynccontextmanager

from services.logger import setup_logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    yield


app = FastAPI(title="Obsidian Workflow Bot", description="A bot to automate workflows in Obsidian", version="1.0.0", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}