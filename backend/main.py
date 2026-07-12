from fastapi import FastAPI

from app.api.upload import router as upload_router

app = FastAPI(title="JobSearcherChatGPT")

app.include_router(upload_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to JobSearcherChatGPT!"
    }