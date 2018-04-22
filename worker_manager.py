import json
import logging
import multiprocessing
import random
import time

import click

import log
from worker import run_worker


logger = logging.getLogger(__name__)


@click.command()
@click.option('--config', default=None, help="Config in JSON format")
@click.option('--host', default='localhost', help="Link to host with Redis")
@click.option('-p', '--port', default=6379, help="Redis port")
@click.option('-d', '--db', default=0, help="Database number in Redis")
@click.option('-n', '--worker_number', default=1, help="Number of workers")
@click.option('--task_types', default='', help="Comma-separated list of types of tasks to execute")
@click.option('--sleep_time', default=0.5, help="Sleep time in secs between re-doing cyclic actions")
@click.option('-v', '--is_verbose', is_flag=False, help='Enables verbose mode')
def main(config, host, port, db, worker_number, task_types, sleep_time, is_verbose):
    log.init(config, is_verbose)
    logger.debug(u"Input params: confg: {}; host: {}; port: {}; db: {}; "
                 u"worker_number: {}; task_types: {}; sleep_time: {}; is_verbose: "
                 u"{}".format(config, host, port, db, worker_number,
                              task_types, sleep_time, is_verbose))
    if config:
        kwargs = _get_params_from_config(config)
    else:
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


def _get_params_from_config(config_str):
    config = json.loads(config_str)
    params = dict()
    params['host'] = config.get('host', 'localhost')
    params['port'] = config.get('port', 6379)
    params['db'] = config.get('db', 0)
    params['serving_task_types'] = config.get('task_types', '')
    params['sleep_time'] = config.get('sleep_time', 0.5)
    return params


def run_workers(worker_number, kwargs):
    workers_list = []
    for i in range(worker_number):
        logger.debug(u"i: {}".format(i))
        worker_process_name = "worker_" + str(int(time.time())) + "_" + str(random.randint(1000, 9999))
        worker = multiprocessing.Process(
            target=run_worker, kwargs=kwargs, name=worker_process_name
        )
        worker.start()
        workers_list.append(worker)
    return workers_list


def filter_not_working_workers(worker_list):
    return [w for w in worker_list if w.is_alive]


if __name__ == '__main__':
    main()
