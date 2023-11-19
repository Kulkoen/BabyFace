import redis

def create_redis_instance():
    r = redis.Redis(
    host='redis-17203.c259.us-central1-2.gce.cloud.redislabs.com',
    port=17203,
    password='kWFTLkM3O10DSUeCC1sjhKxtrGdJpvyf',
    decode_responses=True)

    return r 