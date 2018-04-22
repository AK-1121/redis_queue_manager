import json
import logging

import click

from redis_queue import RedisQueue
import log

logger = logging.getLogger(__name__)
log.init()


DEFAULT_TASK_CONFIG = {
    'url': "http://fullhdwallpapers.ru/image/nature/4051/magicheskie-gory.jpg",
    'local_path': "downloads"
}


@click.command()
@click.option('-t', '--task_name', default="task_download_file_by_url", help='Give name of task')
@click.option('-c', '--config', default=DEFAULT_TASK_CONFIG, help='Give local path (absolute or relative)')
@click.option('--host', default='localhost', help='Redis queue host name')
@click.option('--port', default=6379, help='Redis queue port')
@click.option('--db', default=0, help='Redis db number')
def main(task_name, config, host, port, db):
    rq = RedisQueue(host=host, port=port, db=db)
    config_json_str = json.dumps(config)
    rq.enqueue(task_name, config_json_str)


if __name__ == '__main__':
    main()
