from taskiq_redis import RedisAsyncResultBackend, ListQueueBroker

from src.config import settings

result_backend = RedisAsyncResultBackend(settings.REDIS_URL)
broker = ListQueueBroker(settings.REDIS_URL).with_result_backend(result_backend)
