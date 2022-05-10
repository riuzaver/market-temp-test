from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, RedirectResponse

from db import get_session

root_router = APIRouter()


@root_router.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")


@root_router.get("/healthcheck", tags=["healthcheck"])
async def healthcheck(db: AsyncSession = Depends(get_session)):
    try:
        result = await db.execute("SELECT 1")
        if result:
            status_code = status.HTTP_200_OK
            text = "ok"
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            text = "error"
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        text = str(e)

    return JSONResponse({"status": text}, status_code)
