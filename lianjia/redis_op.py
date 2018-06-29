import redis
from lianjia.settings import REDIS_HOST, REDIS_PORT

class RedisOp(object):
    def __init__(self, *args, **kwargs):
        self.pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
        self.redis = redis.Redis(connection_pool=self.pool)
    
    def sadd(self, name, values):
        self.redis.sadd(name, values)
    
    def sismember(self, name, value):
        return self.redis.sismember(name,value)