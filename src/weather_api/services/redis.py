from redis.asyncio import Redis
import json


class RedisCache:
    def __init__(self, host: str, port: int, db: int):
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)

    async def get_or_set(self, key: str, ttl: int, fetch_fn):
        value = await self.redis.get(key)
        if value is not None:
            return json.loads(value)

        result = await fetch_fn()

        if result is None:
            return None

        await self.redis.set(key, json.dumps(result), ex=ttl)
        return result
