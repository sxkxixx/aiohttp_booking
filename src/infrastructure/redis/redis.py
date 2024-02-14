from aioredis import Redis

from config import RedisConfig

redis = Redis(
    host=RedisConfig.HOST,
    port=RedisConfig.PORT,
    username=RedisConfig.USERNAME,
    password=RedisConfig.PASSWORD
)
