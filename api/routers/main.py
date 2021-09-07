from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def main_handler():
    return "OK"
