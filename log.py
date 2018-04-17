import logging
import logging.config
import sys


def init(config=None, verbose=None):
    if config:
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            stream=sys.stderr,
            format="%(asctime)s %(levelname) %(process)d %(name)s: %(message)s",
            level=logging.DEBUG if verbose else logging.INFO
        )
