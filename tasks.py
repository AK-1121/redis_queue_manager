import json
import logging
import os
import time

import requests

logger = logging.getLogger(__name__)


# ============ Download file by url job ==============
def task_download_file_by_url(params):
    """
    Expecting params:
    url - str - url of file
    local_path - str - local path where to save file
    :param dict params:
    :return:
    """
    try:
        url = params["url"]
        local_path_from_conf = params["local_path"]
        logger.debug(u"config. url: {}; local_path: {}".format(url, local_path_from_conf))
        local_path = _find_local_path(url, local_path_from_conf)
        logger.debug(u"local path: {}".format(local_path))
        _prepare_local_path(local_path)
        while True:
            resp = requests.get(url, stream=True)
            if resp.status_code != 200:
                logger.info(u"Cannot get file: {}".format(url))
                time.sleep(1)
                continue
            _save_file(local_path, resp)
            break
        result_msg = "Job successfully done"
    except Exception as e:
        result_msg = "Job got error: " + str(e)
    logger.info(result_msg)


def _prepare_local_path(local_file_path):
    dir_name = os.path.dirname(local_file_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if os.path.exists(local_file_path):  # clear way for saving file
        os.remove(local_file_path)


def _find_local_path(url, local_path_from_conf):
    if not os.path.isabs(local_path_from_conf):
        home_dir = os.path.expanduser("~")
        local_path = os.path.join(home_dir, local_path_from_conf)
    else:
        local_path = local_path_from_conf
    if os.path.isdir(local_path):
        original_file_name = os.path.basename(url)
        local_path = os.path.join(local_path, original_file_name)
    return local_path


def _save_file(local_path, resp_obj):
    with open(local_path, 'wb') as f:
        for chunk in resp_obj.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


