import requests
import typing as tp
import time
from twocaptcha import TwoCaptcha
from twocaptcha import *


class TwoCaptchaService:
    
    _SURL = 'https://client-api.arkoselabs.com'
    # _USER_AGENT         = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    

    def __init__(self, api_key, proxy_http=None, useragent=None):
        self.api_key = api_key
        self.solver = TwoCaptcha(api_key, defaultTimeout=180, pollingInterval=15)
        self.proxy_captcha = None
        if proxy_http:
            self.proxy_captcha = self.get_proxy_captcha(proxy=proxy_http)
        self._user_agent = self.set_user_agent(useragent=useragent)

    def get_proxy_captcha(self, proxy):
        if not proxy:
            return None
        proxy = proxy.replace('http://','')
        return {
            'type': 'HTTP',
            'uri': proxy,
            }

    def set_user_agent(self, useragent):
        if not useragent:
            return None
        return useragent


    def get_balance(self):
        return self.solver.balance()

    def create_task(self, public_key, page_url, task_name):
        try:
            #send & get_resultでやる
            task_id = self.solver.send(publickey=public_key,
                            url=page_url,
                            method=task_name,
                            surl=self._SURL,
                            userAgent=self._user_agent,
                            proxy=self.proxy_captcha)
            return task_id
        except Exception as e:
            print('captcha id miss')
            return None

    def get_task_result(self, task_id, sleep_time=10):
        try:
            code = self.solver.get_result(task_id)
            return code
        except (TimeoutException, ValidationException, NetworkException, ApiException, Exception) as e:
            print(e)
            time.sleep(sleep_time)
            return None

    def send_task_report(self, task_id, is_report=True):
        try:
            self.solver.report(task_id, is_report) # captcha solved correctly
        except (TimeoutException, ValidationException, NetworkException, ApiException, Exception) as e:
            print(e)
            




