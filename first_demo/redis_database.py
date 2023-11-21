# Task: Create library to use in other files to create the same redis instance

# Libraries
import redis


# Create a Redis Database Instance
def create_redis_instance():
    r = redis.Redis(
    host='',
    port=17203,
    password='',
    decode_responses=True)

    return r 