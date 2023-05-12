# -*- coding: utf-8 -*-
"""web automation utils


random_device:
    device = random_device(os_name='android')
    os_name: 'android' or 'iphone' or 'pc'



Todo:
    -set devices.json
    

"""

import csv
import os
import random
import pysnooper
import json
from pprint import pprint
import requests

def get_device_list():
    """JSON ファイルを読み込んで Python オブジェクトとして返します。"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "devices.json"))
    with open(file_path, encoding='utf-8') as f:
        return list(json.load(f).keys())
    

def download_devices(filepath='devices.json'):
    """
    Downloads a list of proxies and saves it to a file named 'http.txt'.
    """
    response = requests.get('https://raw.githubusercontent.com/microsoft/playwright/main/packages/playwright-core/src/server/deviceDescriptorsSource.json')

    with open(filepath, 'wb') as f:
        f.write(response.content)



def random_device(os_name='android'):
    device_list = get_device_list()
    iphones = [device for device in device_list if device.startswith('iP')]
    desktops = [device for device in device_list if device.startswith('Desktop')]
    androids = list(set(device_list) - set(iphones) - set(desktops))
    if 'iphone' == os_name:
        return random.choice(iphones)
    elif 'pc' == os_name:
        return random.choice(desktops)
    else:
        return random.choice(androids)


if __name__ == '__main__':
    # device_list = get_device_list()
    download_devices(filepath='devices.json')
    import pdb;pdb.set_trace()
    