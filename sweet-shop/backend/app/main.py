from fastapi import FastAPI
from .auth import router as auth_router
from .sweets import router as sweets_router

app = FastAPI(title="Sweet Shop API")

app.include_router(auth_router)
app.include_router(sweets_router)

@app.get("/")
async def root():
    return {"message": "Sweet Shop API"}
