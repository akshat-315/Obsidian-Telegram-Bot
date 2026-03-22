from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from services.logger import setup_logger
from services.telegram import start_bot

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    await start_bot()
    yield
    


app = FastAPI(title="Obsidian Workflow Bot", description="A bot to automate workflows in Obsidian", version="1.0.0", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}