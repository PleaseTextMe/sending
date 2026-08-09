from fastapi import APIRouter

from src.api.v1.endpoints.messages import router as messages_router

router = APIRouter(prefix="/v1")

router.include_router(messages_router)
