from fastapi import HTTPException
import httpx

from weather_api.settings import Settings

settings = Settings()  # type: ignore
api_url = settings.WEATHER_API_URL
api_key = settings.WEATHER_API_KEY


async def get_weather(location: str):
    try:
        url = f"{api_url}/{location}"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={
                    "unitGroup": "us",
                    "elements": (
                        "remove:cloudcover,"
                        "remove:datetimeEpoch,"
                        "remove:dew,"
                        "remove:feelslikemax,"
                        "remove:feelslikemin,"
                        "remove:moonphase,"
                        "remove:precipcover,"
                        "remove:preciptype,"
                        "remove:pressure,"
                        "remove:snow,"
                        "remove:snowdepth,"
                        "remove:solarenergy,"
                        "remove:solarradiation,"
                        "remove:uvindex,"
                        "remove:visibility,"
                        "remove:winddir,"
                        "remove:windgust"
                    ),
                    "include": "current,alerts",
                    "key": api_key,
                    "contentType": "json",
                },
                timeout=20,
            )

            response.raise_for_status()
            data = response.json()
            result = {
                "status_code": response.status_code,
                "location": data["resolvedAddress"],
                "timezone": data["timezone"],
                "alerts": data["alerts"],
                "currentConditions": data["currentConditions"],
            }

            return result

    except httpx.HTTPStatusError as exc:
        resp = exc.response

        try:
            data = resp.json()
            msg = (
                data.get("response")
                or data.get("message")
                or "Weather API error"
            )
        except Exception:
            msg = resp.text or "Weather API returned invalid response"

        raise HTTPException(
            status_code=resp.status_code,
            detail=msg,
        )
