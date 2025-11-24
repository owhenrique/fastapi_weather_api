from fastapi import APIRouter, HTTPException
from http import HTTPStatus

from weather_api.settings import Settings
from weather_api.services.redis import RedisCache
from weather_api.services.get_weather import get_weather

settings = Settings()  # type: ignore
host = settings.REDIS_HOST
port = settings.REDIS_PORT
db = settings.REDIS_DB

router = APIRouter(prefix="/weathers")


@router.get("/", status_code=HTTPStatus.OK)
async def read_location_weather(location: str):

    try:
        cache = RedisCache(host, port, db)
        return await cache.get_or_set(
            f"weather:{location}",
            ttl=60,
            fetch_fn=lambda: get_weather(location),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
