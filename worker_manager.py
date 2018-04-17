import logging
import multiprocessing
import time

import click

import log
from worker import run_worker


logger = logging.getLogger(__name__)


# class WorkerManager:
#     def __init__(self, host='localhost', port=6379, db=0,
#                  worker_number=1, serving_task_types=''):
#         self.host = host
#         self.port = port
#         self.db = db
#         self.worker_number = worker_number
#         self.serving_task_types = serving_task_types
#
#     def __call__(self):
#         for i in range(self.worker_number):
#             logger.debug(u"i: {}".format(i))
#             kwargs = {
#                 'host': self.host, 'port': self.port, 'db': self.db,
#                 'serving_task_types': self.serving_task_types
#             }
#             process = multiprocessing.Process(
#                 target=run_worker, kwargs=kwargs
#             )
#             process.start()
            # process.join()


@click.command()
@click.option('--config', default=None, help="Config in JSON format")
@click.option('--host', default='localhost', help="Link to host with Redis")
@click.option('-p', '--port', default=6379, help="Redis port")
@click.option('-d', '--db', default=0, help="Database number in Redis")
@click.option('-n', '--worker_number', default=1, help="Number of workers")
@click.option('--task_types', default='', help="Comma-separated list of types of tasks to execute")
@click.option('--sleep_time', default=0.5, help="Sleep time in secs between re-doing cyclic actions")
@click.option('-v', '--is_verbose', is_flag=True, help='Enables verbose mode')
def main(config, host, port, db, worker_number, task_types, sleep_time, is_verbose):
    log.init(config, is_verbose)
    logger.debug(u"Input params: confg: {}; host: {}; port: {}; db: {}; "
                 u"worker_number: {}; task_types: {}; sleep_time: {}; is_verbose: "
                 u"{}".format(config, host, port, db, worker_number,
                              task_types, sleep_time, is_verbose))
    # worker_manager = WorkerManager(
    #     host=host, port=port, db=db, worker_number=worker_number,
    #     serving_task_types=task_types, sleep_time=sleep_time
    # )
    # worker_manager()
    kwargs = {
        'host': host, 'port': port, 'db': db,
        'serving_task_types': task_types,
        "sleep_time": sleep_time
    }
    workers_list = run_workers(worker_number, kwargs)
    while True:
        time.sleep(sleep_time)
        live_workers = filter_not_working_workers(workers_list)
        new_workers = run_workers(worker_number - len(live_workers), kwargs)
        workers_list = live_workers + new_workers


def run_workers(worker_number, kwargs):
    workers_list = []
    for i in range(worker_number):
        logger.debug(u"i: {}".format(i))
        worker = multiprocessing.Process(target=run_worker, kwargs=kwargs)
        worker.start()
        workers_list.append()
    return workers_list


def filter_not_working_workers(worker_list):
    return [w for w in worker_list if w.is_alive]


if __name__ == '__main__':
    main()
