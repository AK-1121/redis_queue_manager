import json
import time

import requests


# ============ Download file by url job ==============
def download_file_by_url(params):
    """
    Expecting params:
    url - str - url of file
    local_path - str - local path where to save file
    :param dict params:
    :return:
    """
    url = params["url"]
    local_path = params["local_path"]
    while True:
        resp = requests.get(url, stream=True)
        if resp.status_code != 200:
            time.sleep(1)
            continue
        _save_file(local_path, resp)
        break


def _save_file(local_path, resp_obj):
    with open(local_path, 'wb') as f:
        for chunk in resp_obj.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


