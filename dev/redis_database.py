import redis

def create_redis_instance():
    r = redis.Redis(
    host='',
    port=17203,
    password='')

    return r 
