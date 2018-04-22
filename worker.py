import json
import logging
import time

import redis

import tasks as tasks_storage

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, host='localhost', port=6379, db=0, serving_task_types='', sleep_time=0.5):
        self.r = redis.StrictRedis(host=host, port=port, db=db)
        logger.info(u"Redis credentials: host: {}; port: {}; db: {}".format(host, port, db))
        if serving_task_types:
            self.serving_tasks_types = serving_task_types.split(',')
        else:
            logger.debug(u"dir(tasks_storage): {}".format(dir(tasks_storage)))
            self.serving_tasks_types = [t for t in dir(tasks_storage) if t.startswith("task_")]
        logger.info(u"Serving tasks types: {}".format(self.serving_tasks_types))
        self.is_continue = True
        self.sleep_time =sleep_time

    def run(self):
        while self.is_continue:
            for task_type in self.serving_tasks_types:
                logger.debug(u"task_type: {}".format(task_type))
                task_id = self.r.rpop(task_type + "_queue")
                logger.debug(u"RPop task id: {}".format(task_id))
                if not task_id:
                    continue
                config_str = self.r.get(task_id)
                config = json.loads(config_str)
                task_body = getattr(tasks_storage, task_type)
                task_body(config)
            time.sleep(self.sleep_time)


def run_worker(**kwargs):
    worker = Worker(**kwargs)
    worker.run()




