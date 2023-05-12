# -*- coding:utf-8 -*-
# ------------------------------------------------------------------
import sys
from random import choice, uniform
import time
import pathlib
import logging
import logging.config
from contextlib import contextmanager, suppress
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import socket
import pysnooper
from importlib import reload
import os
import re
import emoji
#from pyvirtualdisplay import Display
import undetected_chromedriver as uc
from selenium.webdriver.common.proxy import Proxy, ProxyType
import random
import unicodedata, difflib
import boto3
import subprocess
import platform
from dotenv import load_dotenv
lg = logging.getLogger(__name__)
import copy


# 環境変数を参照
load_dotenv()
IMG_DIR = os.getenv('IMG_DIR')
BUCKET_NAME=os.getenv('BUCKET_NAME')

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

#@pysnooper.snoop()
def add_exact(search_txt):
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


#@pysnooper.snoop()
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
        mailado = add_exact(search_txt)
        return mailado
    return None


def get_driver(headless=False, use_ua=False, use_proxy=False, use_profile=False, use_eager_mode=False):
    from webdriver_manager.chrome import ChromeDriverManager
    #prof_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cookies')
    co = Options()
    if headless:
        co.add_argument("--headless")
    if use_ua:
        co.add_argument('--user-agent={0}'.format(use_ua))
    else:
        co.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36')
    if use_proxy:
        co.add_argument(f'--proxy-server=http://{use_proxy}')

    if use_profile:
        userdata_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'UserData')
        lg.debug('user-data-dir={}. profile=Profile {}'.format(userdata_dir, use_profile))
        #userdata_dir = 'UserData'  # カレントディレクトリの直下に作る場合
        os.makedirs(userdata_dir, exist_ok=True)
        co.add_argument('--user-data-dir={}'.format(userdata_dir))
        co.add_argument('--profile-directory=Profile {}'.format(use_profile))

    if use_eager_mode:
        co.set_capability("pageLoadStrategy", "eager")

    co.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    co.add_argument('--disable-blink-features=AutomationControlled')
    co.add_argument('--disable-gpu')
    co.add_argument("--disable-infobars")
    co.add_argument("--hide-scrollbars")
    co.add_argument('--ignore-certificate-errors')
    co.add_argument('--allow-running-insecure-content')
    co.add_argument('--disable-web-security')
    co.add_argument('--lang=ja')
    co.add_argument("--enable-javascript")
    co.add_argument("--window-size=375,812")
    co.add_argument("--start-maximized")
    co.add_argument('--log-level=3')
    co.add_argument('--no-sandbox')
    co.add_argument("--disable-application-cache")
    co.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=co)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    #driver.set_window_size('375', '812')
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(60)
    return driver


def page_load(driver, myurl):
    waitTime = 5
    for ww in range(1, 4):
        mywait = waitTime * ww
        try:
            driver.get(myurl)
            WebDriverWait(driver, mywait).until(
                EC.presence_of_all_elements_located)
            break
        except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
            print(e)
            lg.exception(e)


def myClick(driver, by, desc):
    waitn = WebDriverWait(driver, 5)
    try:
        by = by.upper()
        if by == 'XPATH':
            waitn.until(EC.element_to_be_clickable((By.XPATH, desc))).click()
        if by == 'ID':
            waitn.until(EC.element_to_be_clickable((By.ID, desc))).click()
        if by == 'LINK_TEXT':
            waitn.until(EC.element_to_be_clickable(
                (By.LINK_TEXT, desc))).click()
        if by == "NAME":
            waitn.until(EC.element_to_be_clickable((By.NAME, desc))).click()
        if by == "CSS":
            waitn.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, desc))).click()
        if by == "OK":
            waitn.until(EC.presence_of_all_elements_located)
            desc.click()

    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as ex:
        print(ex)


def action_click(driver, elem):
    # elemは(By.XPATH, 'xpath')のようなタプル
    waitn = WebDriverWait(driver, 5)
    try:
        elem = waitn.until(EC.element_to_be_clickable(elem))
        webdriver.ActionChains(driver).move_to_element(elem).click().perform()
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as ex:
        print(ex)


def slowClick(driver, by, desc):
    waitn = WebDriverWait(driver, 10)
    try:
        by = by.upper()
        if by == 'XPATH':
            waitn.until(EC.element_to_be_clickable((By.XPATH, desc))).click()
        if by == 'ID':
            waitn.until(EC.element_to_be_clickable((By.ID, desc))).click()
        if by == 'LINK_TEXT':
            waitn.until(EC.element_to_be_clickable(
                (By.LINK_TEXT, desc))).click()
        if by == "NAME":
            waitn.until(EC.element_to_be_clickable((By.NAME, desc))).click()
        if by == "CSS":
            waitn.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, desc))).click()
        if by == "OK":
            waitn.until(EC.presence_of_all_elements_located)
            desc.click()
        waitn.until(EC.presence_of_all_elements_located)

    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as ex:
        print(ex)
        raise


def mySendkey(driver, by, desc, my_word):
    waitn = WebDriverWait(driver, 10)
    time.sleep(1)
    try:
        by = by.upper()
        if by == 'XPATH':
            waitn.until(EC.element_to_be_clickable((By.XPATH, desc))).clear()
            waitn.until(EC.element_to_be_clickable(
                (By.XPATH, desc))).send_keys(my_word)
        if by == 'ID':
            waitn.until(EC.element_to_be_clickable((By.ID, desc))).clear()
            waitn.until(EC.element_to_be_clickable(
                (By.ID, desc))).send_keys(my_word)
        if by == 'LINK_TEXT':
            waitn.until(EC.element_to_be_clickable(
                (By.LINK_TEXT, desc))).clear()
            waitn.until(EC.element_to_be_clickable(
                (By.LINK_TEXT, desc))).send_keys(my_word)
        if by == "NAME":
            waitn.until(EC.element_to_be_clickable((By.NAME, desc))).clear()
            waitn.until(EC.element_to_be_clickable(
                (By.NAME, desc))).send_keys(my_word)
        if by == "CSS":
            waitn.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, desc))).clear()
            waitn.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, desc))).send_keys(my_word)
        if by == "OK":
            waitn.until(EC.presence_of_all_elements_located)
            desc.clear()
            desc.send_keys(my_word)

        waitn.until(EC.presence_of_all_elements_located)
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as ex:
        print(ex)
        raise


def exe_click(driver, by, desc):
    waitn = WebDriverWait(driver, 10)
    try:
        by = by.upper()
        if by == 'XPATH':
            waitn.until(EC.presence_of_element_located((By.XPATH, desc)))
            driver.execute_script(
                "arguments[0].click();", driver.find_element(By.XPATH, desc))
        if by == 'ID':
            waitn.until(EC.presence_of_element_located((By.ID, desc)))
            driver.execute_script(
                "arguments[0].click();", driver.find_element(By.ID, desc))
        if by == 'LINK_TEXT':
            waitn.until(EC.presence_of_element_located((By.LINK_TEXT, desc)))
            driver.execute_script(
                "arguments[0].click();", driver.find_element(By.LINK_TEXT, desc))
        if by == "NAME":
            waitn.until(EC.presence_of_element_located((By.NAME, desc)))
            driver.execute_script(
                "arguments[0].click();", driver.find_element(By.NAME, desc))
        if by == "CSS":
            waitn.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, desc)))
            driver.execute_script(
                "arguments[0].click();", driver.find_element(By.CSS_SELECTOR, desc))
        if by == "OK":
            waitn.until(EC.presence_of_all_elements_located)
            driver.execute_script("arguments[0].click();", desc)
        waitn.until(EC.presence_of_all_elements_located)

    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as ex:
        print(ex)
        raise


def waiting_for_element(driver, element, wait_time):
    try:
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(
            element))
    except Exception as e:
        print(e)


def send_keys(driver, element, key):
    action = webdriver.ActionChains(driver)
    action.send_keys_to_element(element, key).pause(uniform(.1, .5)) \
        .send_keys_to_element(element, Keys.ENTER).perform()


# @pysnooper.snoop()
def emoji_convert(texts):
    mytxt = texts
    for ppn in range(20):
        if re.search(r':[a-z]+[^:]+[a-z]:', mytxt):
            emj = re.search(r':[a-z]+[^:]+[a-z]:', mytxt).group()
            mytxt = mytxt.replace(emj, emoji.emojize(emj, use_aliases=True))
            continue
        else:
            return mytxt


# @pysnooper.snoop()
def emoji_send(driver, x_elem, texts):
    JS_ADD_TEXT_TO_INPUT = """
    console.log( "start" );
    try {
        var elm = arguments[0], txt = arguments[1];
        elm.value += txt;

        elm.dispatchEvent(new Event('change'));
    } catch(e) {
        console.log( e.message );
    }
    """
    elem = driver.find_element(By.XPATH, x_elem)
    mytext = emoji_convert(texts)
    try:
        driver.execute_script(JS_ADD_TEXT_TO_INPUT, elem, mytext)
        driver.find_element(By.XPATH, x_elem).send_keys(" ")
        # driver.find_element(By.XPATH, x_elem).send_keys(Keys.RETURN)
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
        print(e)


# @pysnooper.snoop()
def my_emojiSend(driver, by, desc, my_word):
    wait = WebDriverWait(driver, 10)
    time.sleep(1)
    INPUT_EMOJI = """
    arguments[0].value += arguments[1];
    arguments[0].dispatchEvent(new Event('change'));
    """

    try:
        by = by.upper()
        if by == 'XPATH':
            wait.until(EC.element_to_be_clickable((By.XPATH, desc))).clear()
            element = driver.find_element(By.XPATH, desc)
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")

        if by == 'ID':
            wait.until(EC.element_to_be_clickable((By.ID, desc))).clear()
            element = driver.find_element(By.ID, desc)
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")
        if by == 'LINK_TEXT':
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, desc))).clear()
            element = driver.find_element(By.LINK_TEXT,  desc)
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")
        if by == "NAME":
            wait.until(EC.element_to_be_clickable((By.NAME, desc))).clear()
            element = driver.find_element(By.NAME,  desc)
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")
        if by == "CSS":
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, desc))).clear()
            element = driver.find_element(By.CSS_SELECTOR,   desc)
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")
        if by == 'OK':
            element = desc
            element.clear()
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")

    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as ex:
        print(ex)
        

# @pysnooper.snoop()
def send_gmail(formurl, sender_name, money, mailado, kenmei):
    #フォームURLが複数あればランダムで１つ選ぶ
    form_urls = formurl.split(',')
    form_url = random.choice(form_urls)
    #送信者名と条件文
    name = sender_name.strip()
    nakami = money.strip()
    try:
        driver = get_driver(headless=True, use_ua=False, use_proxy=False)
        wait = WebDriverWait(driver, 10)
        driver.get(form_url)
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        driver.find_element(By.XPATH,"//input[@type='email']").send_keys(mailado)
        inputforms = driver.find_elements(By.XPATH,"//input[@type='text']")
        inputforms[0].send_keys(kenmei)
        if 1 < len(inputforms):
            inputforms[1].send_keys(name)
            driver.implicitly_wait(3)
            elem = driver.find_elements(By.XPATH,"//form[@id='mG61Hd']/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div/div[2]/textarea")
            if len(elem) != 0:
                elem[0].send_keys(nakami)
        myClick(driver, "xpath", "//form[@id='mG61Hd']/div[2]/div/div[3]/div/div/div/span/span")
        time.sleep(2)
        myClick(driver, "link_text", "別の回答を送信")
        time.sleep(1)
        driver.quit()
        return True
    except(socket.timeout, NoSuchElementException, TimeoutException, Exception):
        driver.quit()
        return False



# list_you = 会話履歴,namaeは客の名前,asi_if=falseで足跡テンプレは送らない
# @pysnooper.snoop()
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



def check_element(driver, element_data, el_max_wait_time=10):
    """check if an element exists on the page"""
    element = element_data[0]
    text = element_data[1]
    try:
        wait = WebDriverWait(driver, el_max_wait_time)
        wait.until(EC.presence_of_element_located(element))
        if text and text not in driver.find_element(*element).text:
            return False
    except Exception as e:
        print(e)
        return False
    return True


def submit_bt_click(driver, submit):
    try:
        driver.switch_to.default_content()
        time.sleep(uniform(1.0, 5.0))
        element = driver.find_element(*submit)
        webdriver.ActionChains(driver).move_to_element(
            element).click().perform()
    except Exception as e:
        print(e)


def smartproxy(host, port):
    DRIVER = 'CHROME'

    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL

    prox.http_proxy = '{hostname}:{port}'.format(hostname=host, port=port)
    prox.ssl_proxy = '{hostname}:{port}'.format(hostname=host, port=port)

    if DRIVER == 'FIREFOX':
        capabilities = webdriver.DesiredCapabilities.FIREFOX
    elif DRIVER == 'CHROME':
        capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    return capabilities


@contextmanager
def driver_set(use_proxy=False, use_profile=None, user_agent=None):
    co = Options()
    if use_proxy:
        co.add_argument('--proxy-server={0}'.format(use_proxy))
    if use_profile:
        userdir = pathlib.Path.cwd() / "UserData"
        os.makedirs(userdir, exist_ok=True)
        co.add_argument('--user-data-dir={0}'.format(userdir))
        co.add_argument('--profile-directory={}'.format(use_profile))
    if user_agent:
        co.add_argument('--user-agent={}'.format(user_agent))

    # co.add_argument('--start-maximized')
    co.add_argument('--window-size=1440,920')
    co.add_experimental_option("excludeSwitches", ['enable-automation'])
    co.add_argument('--disable-blink-features=AutomationControlled')
    co.add_argument('--disable-gpu')
    co.add_argument('--ignore-certificate-errors')
    co.add_argument('--allow-file-access-from-files')
    co.add_argument('--disable-web-security')
    co.add_argument('--lang=ja')
    ch_r = [os.path.join(os.path.abspath(
        os.path.dirname(__file__))), 'chromedriver']
    chrome_driver = os.path.join(*ch_r)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=co)
    driver.implicitly_wait(15)
    driver.set_page_load_timeout(60)
    try:
        yield driver
    finally:
        driver.quit()


@pysnooper.snoop()
def compose_driver(proxy_info=None, userdata_dir=None, use_profile=None, use_ua=None):
    co = uc.ChromeOptions()
    co.add_argument(
        '--no-first-run --no-service-autorun --password-store=basic')
    if proxy_info:
        co.add_argument('--proxy-server={}'.format(proxy_info))
    co.add_argument('--no-default-browser-check')
    co.add_argument('--lang=ja-JP')
    co.add_argument("--proxy-bypass-list:localhost,127.0.0.1")
    if userdata_dir:
        userdata_dir = os.path.join(os.getcwd(), userdata_dir)
        #userdata_path = pathlib.Path('./ChromeProfile')
        co.add_argument('--user-data-dir={}'.format(userdata_dir))
    if use_profile:
        co.add_argument('--profile-directory={}'.format(use_profile))
    if use_ua:
        co.add_argument('--user-agent={0}'.format(use_ua))
        co.add_argument("--window-size=393,851")

    #linuxだとchromeの最新バージョンいれれないので、ChromeDriverManagerを使うかの分岐
    #amazonlinuxで使うときはchromedriverを同じディレクトリに
    ch_r = [os.path.join(os.path.abspath(
        os.path.dirname(__file__))), 'chromedriver']
    chrome_driver = os.path.join(*ch_r)
    is_driver = os.path.exists(chrome_driver)
    if is_driver:
        driver = uc.Chrome(driver_executable_path=chrome_driver,options=co)
    else:
        driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install(),options=co)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(60)
    return driver

@pysnooper.snoop()
def http_check(driver):
    time.sleep(20)
    for i in range(100):
        try:
            driver.get("https://www.cman.jp/network/support/go_access.cgi")
            time.sleep(6)
            if driver.title == "アクセス情報【使用中のIPアドレス確認】":
                print('再起動OK')
                return True
        except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
            print('wait 20sec')
            time.sleep(20)


@pysnooper.snoop()
def check_ip(driver):
    for i in range(5):
        try:
            driver.get('http://ip.smartproxy.com/')
            time.sleep(4)
            body_text = driver.find_element_by_tag_name('body').text
            print('myip is {}'.format(body_text))
            return body_text
        except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
            print(e)
    return False


@pysnooper.snoop()
def wifi_reboot(driver):
    try:
        page_load(driver, "http://web.setting/html/home.html")
        myClick(driver, "css", "#settings > span")
        time.sleep(2)
        # import pdb; pdb.set_trace()
        myClick(driver, "id", "password")
        time.sleep(1)
        mySendkey(driver, "id", "password", "admin")
        time.sleep(1)
        myClick(driver, "link_text", "ログイン")
        time.sleep(2)
        driver.refresh()
        myClick(driver, "id", "system")
        myClick(driver, "link_text", "再起動")
        time.sleep(2)
        myClick(driver, "css", ".button_center")
        time.sleep(2)
        myClick(driver, "link_text", "はい")
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
        print(e)


def ouath_twitter(driver, myurl, twitter_id, twitter_pw, twitter_mail):
    wait = WebDriverWait(driver, 15)
    try:
        page_load(driver, myurl)
        # Twitterでログインボタンを押す
        action_click(driver, (By.XPATH, "/html/body/div/button"))
        time.sleep(4)
        # 最初のログインページ
        send_keys(driver, (By.ID, "username_or_email"), twitter_id)
        mySendkey(driver, "id", "username_or_email", twitter_id)
        mySendkey(driver, "id", "password", twitter_pw)
        action_click(driver, (By.ID, "allow"))
        time.sleep(2)
        wait.until(EC.presence_of_all_elements_located)
        # メルアド認証を求められるので
        mySendkey(driver, "id", "challenge_response", twitter_mail)
        exe_click(driver, "id", "email_challenge_submit")
        time.sleep(2)
        wait.until(EC.presence_of_all_elements_located)
        # 最後に認証ボタンを押す
        exe_click(driver, "id", "allow")
        time.sleep(5)
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
        print(e)


@pysnooper.snoop()
def ouath_twitter_not_login(driver, myurl):
    wait = WebDriverWait(driver, 15)
    try:
        page_load(driver, myurl)
        # Twitterでログインボタンを押す
        action_click(driver, (By.XPATH, "/html/body/div/button"))
        time.sleep(4)
        wait.until(EC.presence_of_all_elements_located)
        # 最後に認証ボタンを押す
        action_click(driver, (By.ID, "allow"))
        time.sleep(5)
        wait.until(EC.presence_of_all_elements_located)
        apikey_str = driver.find_elements(By.XPATH, "/html/body/div[2]/div/p")
        api_list = [a.text for a in apikey_str]
        # 辞書型にする
        api_dict = {}
        for ak in api_list:
            key_val = ak.split(':')
            k, v = key_val[0], key_val[1]
            api_dict[k] = v
        return api_dict

    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
        print(e)


@pysnooper.snoop()
def twitter_login(driver, twitter_id, twitter_pw, twitter_email):
    """
    Returns:
        True: ログイン成功
        False: 認証が必要
        None: ログイン失敗
    """
    wait_second = 20
    try:
        page_load(driver, 'https://twitter.com')
        # login button
        waiting_for_element(
            driver, (By.XPATH, '//a[@href="/login"]'), wait_second)
        login_bt = driver.find_element(
            By.XPATH, '//a[@href="/login"]')
        webdriver.ActionChains(driver).move_to_element(
            login_bt).click().perform()
        time.sleep(6)
        # login input
        waiting_for_element(
            driver,
            (By.CSS_SELECTOR, '#react-root input'), wait_second)
        inp = driver.find_element(
            By.CSS_SELECTOR,
            '#react-root input')
        send_keys(driver, inp, twitter_id)
        time.sleep(6)
        # password input
        waiting_for_element(
            driver,
            (By.CSS_SELECTOR, '#layers > div:nth-child(2) input'), wait_second)
        inp = driver.find_elements(
            By.CSS_SELECTOR,
            '#layers > div:nth-child(2) input')[1]
        send_keys(driver, inp, twitter_pw)
        time.sleep(6)
        # inputタグが１つでtype=emailのページだったらメルアド認証　or コード認証
        WebDriverWait(driver, wait_second).until(
            EC.presence_of_all_elements_located)
        # inputフォームが１つのページ
        input_tag = driver.find_elements(By.TAG_NAME, "input")
        if len(input_tag) == 1:
            if input_tag[0].get_attribute('type') == 'email':
                inp = input_tag[0]
                send_keys(driver, inp, twitter_email)
            elif input_tag[0].get_attribute('type') == 'text':
                print('認証必要あり')
            time.sleep(6)

        WebDriverWait(driver, wait_second).until(
            EC.presence_of_all_elements_located)
        if driver.current_url == "https://twitter.com/home":
            print('{}, login success'.format())
            return True
        else:
            print('{}, login error'.format(twitter_id))
            return False
    except Exception as e:
        print(e)
        return None






@pysnooper.snoop()
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

def http_check(driver):
    time.sleep(20)
    for i in range(100):
        try:
            driver.get("https://www.cman.jp/network/support/go_access.cgi")
            time.sleep(6)
            if driver.title == "アクセス情報【使用中のIPアドレス確認】":
                print('再起動OK')
                myip = driver.find_element(By.CLASS_NAME, "outIp").text
                print('myip: %s' % myip)
                return myip
        except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
            print('wait 20sec')
            time.sleep(20)


def wifi_reboot(driver, passwd='admin'):
    try:
        page_load(driver,"http://web.setting/html/home.html")
        myClick(driver, "id", "settings")
        time.sleep(2)
        # import pdb; pdb.set_trace()
        myClick(driver, "id", "password")
        time.sleep(1)
        mySendkey(driver,"id","password",passwd)
        time.sleep(1)
        exe_click(driver, "link_text", "ログイン")
        time.sleep(2)
        if driver.current_url != "http://web.setting/html/quicksetup.html":
            exe_click(driver, "link_text", "ログイン")
            time.sleep(2)
        driver.refresh()
        time.sleep(3)
        myClick(driver, "id", "system")
        myClick(driver, "link_text", "再起動")
        time.sleep(2)
        exe_click(driver, "id", "button_reboot")
        # myClick(driver, "css", ".button_center")
        time.sleep(2)
        exe_click(driver, "link_text", "はい")
        time.sleep(3)
        wait_str = driver.find_element(By.ID, "wait_table").text
        print(wait_str)
        time.sleep(5)
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
        print(e)

def check_ip(driver):
    for i in range(5):
        try:
            driver.get('http://ip.smartproxy.com/')
            time.sleep(4)
            body_text = driver.find_element_by_tag_name('body').text
            print('myip is {}'.format(body_text))
            return body_text
        except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
            print(e)
    return False


def change_ip_with_galaxy_web_settings(driver, password):
    try:
        page_load(driver, "http://galaxy.mobilewifi")
        time.sleep(5)
        exe_click(driver, "id", "details-button")
        time.sleep(5)
        exe_click(driver, "id", "proceed-link")
        time.sleep(5)
        driver.refresh()
        time.sleep(5)
        mySendkey(driver, "xpath", "//input[@type='password']", password)
        #サインインボタン
        exe_click(driver, "xpath", "//*[@id=\"app\"]//button[contains(text(), 'サインイン')]")
        #通信設定メニュー
        exe_click(driver, "xpath", "//*[@id=\"app\"]/div/div[1]/ul/li[3]/div[1]/span[1]")
        #通信設定
        exe_click(driver, "xpath", "//a[@href=\"/communication-settings/setting\"]")
        #ドロップダウンのアイコン
        myClick(driver, "xpath", "//img[@class=\"ic_dropdown_arrow open-indicator\"]")

        
        #ドロップダウン
        dropdown = driver.find_elements(By.XPATH, "//ul[@class=\"dropdown-menu\"]/li")
        btn_element = dropdown[0] if dropdown[0].get_attribute("class") == "select-option" else dropdown[1]
        btn_element.click()
        #選択されていない方をチェック
        # for i in range(len(dropdown)):
        #     if dropdown[i].get_attribute("class") == "select-option":
        #         dropdown[i].click()
        #         break
        
        #保存ボタン
        exe_click(driver, "xpath", "//img[@class=\"btn_primary_arrow column\"]")
        time.sleep(5)
        #確認OKボタン
        exe_click(driver, "xpath", "//button[contains(text(), 'OK')]")
        time.sleep(5)
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
        print(e)

if __name__ == "__main__":
    password = "098951"
    
    driver = compose_driver()
    old_ip = http_check(driver)
    change_ip_with_galaxy_web_settings(driver, password)
    new_ip = http_check(driver)

    #---galacy ip change---
    # password = "098951"
    import pdb;pdb.set_trace()
