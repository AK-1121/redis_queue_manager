import json

import redis

import tasks as tasks_storage


class Worker:
    def __init__(self, host='localhost', port=6379, db=0, serving_task_types=tuple()):
        self.r = redis.StrictRedis(host=host, port=port, db=db)
        self.serving_tasks_entities = serving_task_types
        # if task_type_name:
        #     serving_tasks_names = [task_type_name.split(',')]
        # else:
        #     serving_tasks_names = [t for t in dir(tasks_storage) if t.startswith("task_")]
        # for name in serving_tasks_names:
        #     task_triada = (name, name + "_queue", name + "_conf")
        #     self.serving_tasks_entities.append(task_triada)
        self.is_continue = True

    def run(self):
        while self.is_continue:
            for task_type in self.serving_tasks_entities:
                task_id = self.r.rpop(task_type + "_queue")
                config_str = self.r.get(task_id)
                config = json.loads(config_str)
                task_body = getattr(tasks_storage, task_type)
                task_body(config)






