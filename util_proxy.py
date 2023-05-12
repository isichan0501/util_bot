# -*- coding: utf-8 -*-
"""web automation utils


random_proxy:
    proxy_info = random_proxy()

Todo:
    -set proxy.txt
    
How to Use

proxies = get_proxies()
proxy = get_random_proxy(proxies, is_requests=True)


get_proxies(): download and return proxylist
get_random_proxy(proxies, is_requests=True): 
is_requests=True : return proxies = {'http': f'http://{proxy}','https': f'http://{proxy}'}


"""
import requests
import random
import time
import csv
import os
import random
import pysnooper
import json
from pprint import pprint


def format_proxy(proxy_info):
    """proxy format= 'ip:port:user:pass'"""

    if not proxy_info:
        return False
    if not isinstance(proxy_info, str):
        return proxy_info

    if 'random' == proxy_info:
        prox = random_proxy().split(':')
    else:
        prox = proxy_info.split(':')
    return {
        "server": "http://{}:{}".format(prox[0], prox[1]),
        "username": prox[2],
        "password": prox[3],
    }

def download_proxies(filepath='http.txt'):
    """
    Downloads a list of proxies and saves it to a file named 'http.txt'.
    """
    response = requests.get('https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt')

    with open(filepath, 'wb') as f:
        f.write(response.content)

def get_proxies(filepath='http.txt'):
    """fix proxies.
    raw proxies are in the format of 'ip:port' and we need to fix for acyncio and aiohttp of each proxy.
    """
    download_proxies(filepath='http.txt')
    time.sleep(2)
    with open(filepath, 'r') as f:
        proxylist = [px.strip() for px in f.readlines()]
        
    return proxylist
    # fixed_proxies = []
    # for proxy in proxies:
    #     fixed_proxy = 'http://' + proxy
    #     fixed_proxies.append(fixed_proxy)
    # return fixed_proxies

def get_random_proxy(proxies, is_requests=True):
    proxy = proxies[random.randint(0, len(proxies) - 1)]
    if not is_requests:
        return proxy
    
    return {'http': f'http://{proxy}','https': f'http://{proxy}'}


def random_proxy():
    """get random proxy info dict from proxy.txt

    Returns:
        proxy dict (dict): key : host, port, user, pass
    """
    
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "proxy.txt"))
    with open(file_path, 'r') as f:
        proxys = [pr.strip() for pr in f.readlines()]

    return random.choice(proxys)

    prox = random.choice(proxys).split(':')
    proxy_info = {
        'host': prox[0], 
        'port': prox[1],
        'user': prox[2],
        'pass': prox[3],
    }
    return proxy_info