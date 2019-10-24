from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from starlette.responses import JSONResponse
import tortoise.exceptions

from db import Status
from errors import DoesNoExist, ValidationError, UserAlreadyExists

router = APIRouter()


@router.get("/{_id}")
async def get_status_by_id(_id):
    try:
        obj = await Status.get(id=_id)
        data = await obj.to_json()
        return JSONResponse(status_code = HTTP_201_CREATED, content=json)
    except tortoise.exceptions.DoesNotExist:
        return DoesNoExist()

@router.post("/")
async def create_status()
