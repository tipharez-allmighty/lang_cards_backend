from taskiq_redis import RedisAsyncResultBackend, ListQueueBroker

redis_url = "redis://localhost:6379"

result_backend = RedisAsyncResultBackend(redis_url)
broker = ListQueueBroker(redis_url).with_result_backend(result_backend)
