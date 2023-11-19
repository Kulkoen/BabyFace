# Task: Create library to use in other files to create the same redis instance

# Libraries
import redis


# Create a Redis Database Instance
def create_redis_instance():
    r = redis.Redis(
    host='redis-17203.c259.us-central1-2.gce.cloud.redislabs.com',
    port=17203,
    password='kWFTLkM3O10DSUeCC1sjhKxtrGdJpvyf',
    decode_responses=True)

    return r 