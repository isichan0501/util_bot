"""Exapmle:
def run(playwright: Playwright) -> None:

    pixel_2 = playwright.devices['Pixel 2']
    browser = playwright.chromium.launch(
        args=[
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-blink-features=AutomationControlled',
            '--disable-infobars',
            '--allow-running-insecure-content',
        ],
        headless=False,
        devtools=True,
        proxy={
            "server": "103.0.128.70:45785",
            "username": "user",
            "password": "pass",
        },
        chromium_sandbox=False,
    )
    
    context = browser.new_context(
        **pixel_2,
        locale='ja-JP',
        timezone_id='Asia/Tokyo',
        geolocation={"longitude": 136.881694, "latitude": 35.1706431},
        permissions=["geolocation"],
        java_script_enabled=True,
        ignore_https_errors=True,
        
    )
    page = context.new_page()
    stealth_sync(page)
    

    
    # ---------------------
    context.close()
    browser.close()
"""

from xmlrpc.client import Boolean
from playwright.sync_api import Playwright, ProxySettings, sync_playwright
from playwright_stealth import stealth_sync
from playwright._impl._api_types import TimeoutError
from typing import Union, List, Set, Tuple, Dict, Optional, Callable, Generator

from util_proxy import random_proxy, format_proxy
from util_device import random_device
from util_region import GetMap, convert_region_dict
from util_sheet import Temple


import os
import sys

import loguru
from loguru import logger
import pysnooper
from importlib import reload
import time
import random
import constants
import asyncio
from playwright.async_api import async_playwright, BrowserContext, Page, Response, TimeoutError as PlaywrightTimeoutError
from dotenv import load_dotenv
import pysnooper

# 環境変数を参照
load_dotenv()
SMART_PROXY_JP = os.environ.get('SMART_PROXY_JP')


@pysnooper.snoop()
def get_android_browser(playwright: Playwright, proxy_info: Optional[str] = None):

    browser = playwright.chromium.launch(
        args=constants.BROWSER_OPTIONS_PCMAX,
        headless=False,
        devtools=True,
        proxy=format_proxy(proxy_info),
        chromium_sandbox=False,
    )
    return browser

@pysnooper.snoop()
def get_android_context(browser, browser_device, region_name):
    
    context = browser.new_context(
        **browser_device,
        locale='ja-JP',
        timezone_id='Asia/Tokyo',
        geolocation=convert_region_dict(region_name),
        permissions=["geolocation"],
        java_script_enabled=True,
        ignore_https_errors=True,
    )
    return context

@pysnooper.snoop()
def get_android_device(playwright, device_name):
    device_name = device_name if device_name else random_device(os_name='android')
    return playwright.devices[device_name]


def generate_device_specs():
    """
    Generate random RAM/Hardware Concurrency.

    Returns:
        Tuple[int, int]: A tuple containing a random RAM and hardware
        concurrency.
    """
    random_ram = random.choice([1, 2, 4, 8, 16, 32, 64])
    max_hw_concurrency = random_ram * 2 if random_ram < 64 else 64
    random_hw_concurrency = random.choice([1, 2, 4, max_hw_concurrency])
    return (random_ram, random_hw_concurrency)

###-----firefox-----###
async def setup_firefox():
    try:
        firefox = Playwright.devices['Desktop Firefox']
        async with async_playwright() as driver:
            browser = await driver.firefox.launch(
                headless=False,
                args=[
                    '--start-maximized',
                    '--foreground',
                    '--disable-backgrounding-occluded-windows'
                ],
                firefox_user_prefs=constants.FIREFOX_SETTINGS
                # proxy=helpers.get_random_proxy(),
            )

            context = await browser.new_context(
                # **firefox,
                timezone_id='Asia/Tokyo',
                accept_downloads=True,
                is_mobile=False,
                has_touch=False,
                ignore_https_errors=True,
                # proxy=helpers.get_random_proxy()
            )

            page = await context.new_page()
            await page.bring_to_front()
            await page.set_viewport_size(
                {
                    "width": 1280,
                    "height": 720
                }
            )

            await page.add_init_script(
                script=constants.SPOOF_FINGERPRINT % generate_device_specs()
            )
            await page.goto("https://gologin.com/ja/check-browser")

            
            import pdb;pdb.set_trace()
            await asyncio.sleep(1)
            
    except (PlaywrightTimeoutError, Exception) as e:
        print(e)