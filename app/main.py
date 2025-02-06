from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import image_routes

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの追加
app.include_router(
    image_routes.router,
    prefix=f"{settings.API_V1_STR}/images",
    tags=["images"]
)

@app.get("/")
async def root():
    return {"message": "Welcome to LGTM Image Service"}