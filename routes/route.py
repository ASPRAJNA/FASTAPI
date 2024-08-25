from fastapi import APIRouter
from src.endpoints import tasks, users

router = APIRouter()
router.include_router(tasks.router)
router.include_router(users.router)
