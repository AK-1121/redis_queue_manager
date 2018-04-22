import random
import redis
import time

import log
log.init()


class RedisQueue:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.StrictRedis(host=host, port=port, db=db)

    def enqueue(self, task_name: str, config_str: str):
        ts = str(time.time())
        rand_int = random.randint(1000, 9999)
        task_id = u"{name}_{ts}_{rand_int}".format(name=task_name, ts=ts, rand_int=rand_int)
        task_names_queue = u"{}_queue".format(task_name)
        self.r.lpush(task_names_queue, task_id)
        self.r.set(task_id, config_str)
