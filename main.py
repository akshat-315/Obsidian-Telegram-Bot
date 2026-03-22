from fastapi import FastAPI

app = FastAPI(title="Obsidian Workflow Bot", description="A bot to automate workflows in Obsidian", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World"}