import asyncio
import copy
import difflib
import functools
import logging
import os
import random
import re
import traceback
#----for site bot---
import unicodedata
from functools import wraps
from itertools import product
from typing import Any, Callable
from urllib.parse import urlencode

import boto3
import constants
import decorators
import loguru
import playwright_exceptions as exceptions
import requests
# 環境変数を参照
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright
from playwright._impl._api_structures import ProxySettings
from playwright.async_api import BrowserContext, Page, Response
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

load_dotenv()
IMG_DIR = os.getenv('IMG_DIR')
BUCKET_NAME=os.getenv('BUCKET_NAME')
SMART_PROXY_JP = os.environ.get('SMART_PROXY_JP')
lg = logging.getLogger(__name__)




async def get_element_text(page: Page, xpath: str, replace=True, timeout=None):
    """
    Get the text content of an element using its XPath.

    Args:
        page (Page): The Page object to search for the element.
        xpath (str): The XPath of the element.
        replace (bool, optional): Whether to remove newlines and trailing
        whitespace from the text. Defaults to True.
        timeout (int, optional): The maximum time to wait for the element.
        Defaults to None.

    Returns:
        str: The text content of the element.
    """
    result: str = await page.locator(xpath).text_content(timeout=timeout)
    if replace:
        return result.strip().replace("\n", "")
    else:
        return result


async def fill_form(page: Page, xpath: str, text: str, timeout=None):
    """
    Fill a form field with the given text using its XPath.

    Args:
        page (Page): The Page object containing the form field.
        xpath (str): The XPath of the form field.
        text (str): The text to fill into the form field.
        timeout (int, optional): The maximum time to wait for the form field.
        Defaults to None.

    Returns:
        None
    """
    return await page.locator(xpath).fill(text, timeout=timeout)


async def click_element(page: Page, xpath: str, delay=None, force=None):
    """
    click a element 
    
    Args:
        page (Page): The Page object containing the form field.
        xpath (str): The XPath of the form field.
        delay (int, optional): The maximum time to wait for the form field.
        force(bool)
        Defaults to None.

    Returns:
        None
    """
    return await page.locator(xpath).click(delay=delay, force=force)

@decorators.exception_handler
async def safe_page_wait(page: Page, url: str, wait_until="networkidle", timeout=9.0):
    """
    click a element 
    
    Args:
        page (Page): The Page object containing the form field.
        url (str): "**/target.html"
        wait_until (str): Literal["commit", "domcontentloaded", "load", "networkidle"]
        timeout(int):float
    Returns:
        bool
    """

    res = await page.wait_for_url(url, wait_until=wait_until, timeout=timeout)
    if not res:
        return False
    return True


@decorators.exception_handler
async def safe_click_element(page: Page, xpath: str, delay=None, force=None, wait_load=True):
    """
    Safely get the text content of an element using its XPath.

    Args:
        page (Page): The Page object containing the form field.
        xpath (str): The XPath of the form field.
        delay (int, optional): The maximum time to wait for the form field.
        force(bool):force.
        wait_load(bool): is wait load networkidle after click element.
        
    Returns:
        object: playwright object
    """
    res = await click_element(page, xpath, delay=delay, force=force)
    if wait_load:
        await asyncio.sleep(2)
        await page.wait_for_load_state("networkidle")
    return res


@decorators.exception_handler
async def safe_get_element_text(page: Page, xpath: str, replace=True, timeout=None):
    """
    Safely get the text content of an element using its XPath.

    Args:
        page (Page): The Page object to search for the element.
        xpath (str): The XPath of the element.
        replace (bool, optional): Whether to remove newlines and trailing
        whitespace from the text. Defaults to True.
        timeout (int, optional): The maximum time to wait for the element.
        Defaults to None.

    Returns:
        str: The text content of the element, or an empty string on failure.
    """
    return await get_element_text(page, xpath, replace, timeout=timeout)


@decorators.exception_handler
async def safe_fill_form(page: Page, xpath: str, text: str, timeout=None):
    """
    Safely fill a form field with the given text using its XPath.

    Args:
        page (Page): The Page object containing the form field.
        xpath (str): The XPath of the form field.
        text (str): The text to fill into the form field.
        timeout (int, optional): The maximum time to wait for the form field.
        Defaults to None.

    Returns:
        None
    """
    return await fill_form(page, xpath, text, timeout=timeout)



async def does_element_exist_on_page(page: Page, xpath: str, timeout: int = 10000):
    """
    Check if an element exists on the page using its XPath.
    If the element exists, return True. Otherwise, return False.
    If the element does not exist after the specified timeout, return False.

    Args:
        page (Page): The Page object to search for the element.
        xpath (str): The XPath of the element.
        timeout (int, optional): The maximum time to wait for the element.
        Defaults to 500.

    Returns:
        bool: True if the element exists, False otherwise.
    """
    try:
        await page.locator(xpath).wait_for(timeout=timeout)
        return True
    except PlaywrightTimeoutError:
        return False



def get_random_proxy() -> ProxySettings:
    """
    Get a random proxy from the available proxy list.

    :return: A ProxySettings object with a random proxy's details.
    """
    ip_address,port,username,password = SMART_PROXY_JP.split(':')
    port = random.randint(int(port), (int(port)+1000))
    
    return ProxySettings(
        server=f"http://{ip_address}:{port}",
        username=username, password=password
    )



def moji_hikaku(word_a, word_b):
    clean_word_a = re.sub('\W+', '', word_a)
    clean_word_b = re.sub('\W+', '', word_b)
    normalized_word_a = unicodedata.normalize('NFKC', clean_word_a)
    normalized_word_b = unicodedata.normalize('NFKC', clean_word_b)
    itti = difflib.SequenceMatcher(None, normalized_word_a, normalized_word_b).ratio()
    if 0.8 < itti:
        return True
    else:
        return False

def add_extract(search_txt):
    email_regex = re.compile(r'''(
        [a-zA-Z0-9._%+-]+
        @
        [a-zA-Z0-9.-]+
        (\.[a-zA-Z]{2,4})
        )''', re.VERBOSE)

    email_mae = re.compile(r'''(
        [a-zA-Z0-9._%+-]+
        )''', re.VERBOSE)

    email_usiro = re.compile(r'''(
        @
        [a-zA-Z0-9.-]+
        (\.[a-zA-Z]{2,4})
        )''', re.VERBOSE)

    # メルアドの表現の＠の間に余分な文字が入ってる場合
    b_email_regex = re.compile(r'''(
        [a-zA-Z0-9._%+-]+
        .{,20}
        @
        [a-zA-Z0-9.-]+
        (\.[a-zA-Z]{2,4})
        )''', re.VERBOSE)

    result = re.findall(r'([a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))', search_txt)

    if result:
        domain = result[-1][0]
        atto_domain = "@" + str(domain)
        my_txt = search_txt.replace(domain, atto_domain)
        atto_txt = my_txt.replace(' ', '')
        moi = email_regex.search(atto_txt)
        if moi:
            mailado = moi.group()
            return mailado

    rep_txt = search_txt.replace('yahoo', '@yahoo.co.jp').replace('hotmail', '@hotmail.co.jp')
    rep_txt = rep_txt.replace('docomo', '@docomo.ne.jp').replace('gmail', '@gmail.com')
    rep_txt = rep_txt.replace('i.softbank', '@i.softbank.jp').replace('ezweb', '@ezweb.ne.jp')
    rep_txt = rep_txt.replace('icloud', '@icloud.com').replace('au.com', '@au.com').replace('outlook', '@outlook.jp')

    if 'i.softbank' not in rep_txt:
        rep_txt = rep_txt.replace('softbank', '@softbank.ne.jp')
    rep_txt = rep_txt.replace(' ', '').replace('@@', '@')
    rep_txt = re.sub('[^a-zA-Z0-9_.+-@]+', '', rep_txt)
    moi = email_regex.search(rep_txt)
    if moi:
        mailado = moi.group()
        return mailado
    bmoi = b_email_regex.search(rep_txt)
    if bmoi:
        b_mailado = bmoi.group()
        mail_mae = email_mae.search(b_mailado).group()
        mail_usiro = email_usiro.search(b_mailado).group()
        mailado = mail_mae + mail_usiro
        return mailado

    return None

def add_ifin(search_txt):
    email_regex = re.compile(r'''(
        [a-zA-Z0-9._%+-]+
        @
        [a-zA-Z0-9.-]+
        (\.[a-zA-Z]{2,4})
        )''', re.VERBOSE)
    mo = email_regex.search(search_txt)
    if mo:
        mailado = mo.group()
        return mailado
    if any(map(search_txt.__contains__,("outlook", "au", "icloud", "gmail", "ezweb", "softbank", "yahoo", "hotmail", "docomo"))):
        mailado = add_extract(search_txt)
        return mailado
    return None



def mail_what(list_you, tem_ple, namae, asi_if=True, logname="hp"):
    lg = logging.getLogger(__name__)
    list_a = copy.copy(list_you)
    list_my = [tem_ple["title_mail"], tem_ple["asiato"], tem_ple["meruado"], tem_ple["after_mail"]]
    list_n = ["asiato", "meruado", "after_mail"]

    list_b = copy.copy(list_my)

    for n, l_b in enumerate(list_b):
        if 'namae' in l_b:
            list_b[n] = l_b.replace('namae', '{}'.format(namae))

    kenmei = list_b.pop(0)
    if not asi_if:
        asi_ato = list_b.pop(0)
        asi_get = list_n.pop(0)
    clean_list_a = []
    clean_list_b = []
    list_a.reverse()
    list_b.reverse()
    list_n.reverse()
    for c_la in list(list_a):
        clean_word_a = re.sub('\W+', '', c_la)
        normalized_word_a = unicodedata.normalize('NFKC', clean_word_a)
        clean_list_a.append(normalized_word_a)
    for c_lb in list(list_b):
        clean_word_b = re.sub('\W+', '', c_lb)
        normalized_word_b = unicodedata.normalize('NFKC', clean_word_b)
        clean_list_b.append(normalized_word_b)

    # list_bの最後の要素（tem_ple["after_mail"]）を送っていたら終了
    for c_a in list(clean_list_a):
        itti = difflib.SequenceMatcher(None, c_a, clean_list_b[0]).ratio()
        if 0.8 < itti:
            return None

    # メルアドが落ちていたら送信
    for c_a in list(list_a):
        mailado = add_ifin(c_a)
        if mailado:
            for u in range(3):
                mail_ok = send_gmail(tem_ple, mailado, kenmei)
                # mail_ok = old_smtp_gmail(tem_ple, mailado, kenmei)
                if mail_ok == True:
                    lg.debug("{0}_{1}_gmail".format(tem_ple["cnm"], logname))
                    return list_b[0]

    for n, c_b in enumerate(list(clean_list_b)):

        #
        for c_a in list(clean_list_a):
            itti = difflib.SequenceMatcher(None, c_a, c_b).ratio()
            if 0.8 < itti:
                n = n - 1
                if 0 < n:
                    lg.debug("{0}_{1}_{2}".format(tem_ple["cnm"], logname, list_n[n]))
                    return list_b[n]
                else:
                    return None

            else:
                continue
    else:
        lg.debug("{0}_{1}_{2}".format(tem_ple["cnm"], logname, list_n[-1]))
        return list_b[-1]


def s3_img(bucket_name=BUCKET_NAME, img_dir=IMG_DIR):
    
    # s3のimgフォルダの一覧をゲット
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    img_list = [obj.key for obj in bucket.objects.all() if 'jpg' in obj.key]
    img_name = random.choice(img_list)
    img_dir = os.path.join(os.getcwd(), img_dir)
    img_path = os.path.join(img_dir, img_name)
    bucket.download_file(img_name, img_path)
    bucket.delete_objects(
        Delete={
            "Objects": [
                {"Key": img_name}
            ]
        }
    )
    lg.debug('download and delete' + img_name)
    return img_path



async def get_firefox(use_headless=True):
    firefox = Playwright.devices['Desktop Firefox']
    async with async_playwright() as driver:
        browser = await driver.firefox.launch(
            headless=use_headless,
            args=[
                '--start-maximized',
                '--foreground',
                '--disable-backgrounding-occluded-windows'
            ]
            # firefox_user_prefs=constants.FIREFOX_SETTINGS
            # proxy=helpers.get_random_proxy(),
        )

        context = await browser.new_context(
            **firefox,
            accept_downloads=True,
            ignore_https_errors=True,
        )
        context.set_default_navigation_timeout(60000)
        page = await context.new_page()
        await page.goto("https://gologin.com/ja/check-browser")


@decorators.exception_handler
async def send_gmailsub(formurl, sender_name, money, mailado, kenmei):
    """playwrightで書き直す"""
    #フォームURLが複数あればランダムで１つ選ぶ
    form_urls = formurl.split(',')
    form_url = random.choice(form_urls)
    #送信者名と条件文
    name = sender_name.strip()
    nakami = money.strip()
    async with async_playwright() as driver:
        firefox = driver.devices['Desktop Firefox']
        browser = await driver.firefox.launch(
            headless=False,
            args=[
                '--start-maximized',
                '--foreground',
                '--disable-backgrounding-occluded-windows'
            ],
            slow_mo=2000
            # firefox_user_prefs=constants.FIREFOX_SETTINGS
            # proxy=helpers.get_random_proxy(),
        )

        context = await browser.new_context(
            **firefox,
            accept_downloads=True,
            ignore_https_errors=True,
        )
        context.set_default_navigation_timeout(60000)
        page = await context.new_page()
        await page.goto(form_url)
        await does_element_exist_on_page(page, "//input[@type='email']", timeout=20000)
        await safe_fill_form(page, "//input[@type='email']", mailado)
        inputforms = await page.locator("//input[@type='text']").all()
        await inputforms[0].fill(kenmei)
        if 1 < len(inputforms):
            await inputforms[1].fill(name)
            xpath = "//form[@id='mG61Hd']/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div/div[2]/textarea"
            is_exist = await does_element_exist_on_page(page, xpath, timeout=3000)
            if is_exist:
                await safe_fill_form(page, xpath, nakami)
        
        # submit_xpath = "//form[@id='mG61Hd']/div[2]/div/div[3]/div/div/div/span/span"
        submit_xpath = "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span"
        await safe_click_element(page, submit_xpath, delay=2, force=True, wait_load=True)
        # await page.get_by_text("送信").click(force=True)
        
        await asyncio.sleep(2)
        await page.get_by_text("別の回答を送信").click(force=True)
        await asyncio.sleep(2)
        return True

from playwright.sync_api import Playwright, sync_playwright, expect





def func_send_gmail(playwright: Playwright, formurl: str, sender_name: str, money: str, mailado: str, kenmei: str) -> None:
    #args setting
    form_urls = formurl.split(',')
    form_url = random.choice(form_urls)
    #送信者名と条件文
    name = sender_name.strip()
    nakami = money.strip()
    browser = playwright.firefox.launch(headless=True)
    context = browser.new_context(**playwright.devices["Desktop Firefox"])
    page = context.new_page()
    page.goto(formurl)
    page.wait_for_load_state("networkidle")
    page.get_by_role("textbox", name="メールアドレス").fill(mailado)
    page.get_by_role("textbox", name="お名前").fill(kenmei)
    page.get_by_role("button", name="送信").click()
    with page.expect_navigation():
        page.get_by_role("link", name="別の回答を送信").click()

    # ---------------------
    context.close()
    browser.close()

def send_gmail(formurl, sender_name, money, mailado, kenmei):
    with sync_playwright() as playwright:
        func_send_gmail(playwright, formurl, sender_name, money, mailado, kenmei)
        

@decorators.exception_handler
async def func_send_gmail_async(playwright: Playwright, formurl: str, sender_name: str, money: str, mailado: str, kenmei: str) -> None:
    #args setting
    form_urls = formurl.split(',')
    form_url = random.choice(form_urls)
    #送信者名と条件文
    name = sender_name.strip()
    nakami = money.strip()
    browser = await playwright.firefox.launch(headless=True)
    # firefox = await playwright.devices["Desktop Firefox"]
    context = await browser.new_context(**playwright.devices["Desktop Firefox"])
    page = await context.new_page()
    await page.goto(formurl)
    await page.wait_for_load_state("networkidle")
    await page.get_by_role("textbox", name="メールアドレス").fill(mailado)
    await page.get_by_role("textbox", name="お名前").fill(kenmei)
    await page.get_by_role("button", name="送信").click()
    async with page.expect_navigation():
        await page.get_by_role("link", name="別の回答を送信").click()

    # ---------------------
    await context.close()
    await browser.close()
    return True


async def send_gmail_async(formurl, sender_name, money, mailado, kenmei):
    async with async_playwright() as playwright:
        res = await func_send_gmail_async(playwright, formurl, sender_name, money, mailado, kenmei)
        return res

if __name__ == "__main__":
    """playwright codegen github.com/microsoft/playwright --save-storage=auth.json
    playwright codegen --device="Desktop Firefox" forms.gle/sks
    """
    formurl="https://forms.gle/skdjd"
    sender_name="mimi"
    money="""お金がないので、お金をください。"""
    mailado="ss@gmail.com"
    kenmei="kenmei"
    # send_gmail(formurl, sender_name, money, mailado, kenmei)
    result = asyncio.run(send_gmail_async(formurl, sender_name, money, mailado, kenmei))
    print('result is {}'.format(result))
    
    
