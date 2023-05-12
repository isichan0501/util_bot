import smtplib, ssl
from email.mime.text import MIMEText
import email.utils
from email.mime.multipart import MIMEMultipart

#-----temp email----
import pyperclip
import requests
import random
import string
import time
import sys
import re
import os
from urlextract import URLExtract
import hashlib

from dotenv import load_dotenv
load_dotenv()
TEMP_MAIL_API_KEY = os.getenv('TEMP_MAIL_API_KEY')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')


#-----------temp mail------------------

def find_url(content):
    extractor = URLExtract()
    urls = extractor.find_urls(content)
    # print(urls)
    return urls


def generateUserName():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    return username


def get_domains():

    url = "https://api.apilayer.com/temp_mail/domains"

    payload = {}
    headers= {
    "apikey": TEMP_MAIL_API_KEY
    }

    response = requests.request("GET", url, headers=headers, data = payload, timeout=20)

    status_code = response.status_code
    result = response.json()
    
    return result


def get_domains2():

    url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/domains/"

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "privatix-temp-mail-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, timeout=20)
    status_code = response.status_code
    result = response.json()
    
    return result


def hash_to_md5(dat):
    # MD5のハッシュ値
    hs = hashlib.md5(dat.encode()).hexdigest()
    print(hs)
    return hs


#メールボックスの確認もこの関数
def get_mail_box(email):
    hashed_email_address = hash_to_md5(email)

    url = "https://api.apilayer.com/temp_mail/mail/id/{}".format(hashed_email_address)

    payload = {}
    headers= {
        "apikey": TEMP_MAIL_API_KEY
    }

    response = requests.request("GET", url, headers=headers, data = payload, timeout=20)

    status_code = response.status_code
    result = response.json()
    print(status_code)
    return result


#メールボックスの確認もこの関数
def get_mail_box2(email):
    
    hashed_email_address = hash_to_md5(email)

    url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id/{}/".format(hashed_email_address)

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "privatix-temp-mail-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    status_code = response.status_code
    result = response.json()
    print(status_code)
    return result

#ランダムなアドレス文字列を作成
def create_email(domain=None):
    if not domain:
        domains = get_domains2()
        domain = random.choice(domains)
    email = generateUserName() + domain
    print(email)
    return email


#get_mail_boxで取得したメール辞書のリストからnoteのアクティベーションURLを取得
def extract_note_url(mail_list):

    mail_from_note = [m for m in mail_list if 'noreply@note.com' in m['mail_from']][-1]['mail_text']
    urls = find_url(mail_from_note)
    activate_url = [u for u in urls if 'https://note.com/activate?' in u][0]
    return activate_url
    
def extract_discord_url(mail_list):
    mail_from_discord = [m for m in mail_list if 'noreply@discord.com' in m['mail_from']][-1]['mail_text']
    urls = find_url(mail_from_discord)
    return urls[0]

def extract_twitter_code(mail_list):
    mail_from_twitter = [m for m in mail_list if 'info@twitter.com' in m['mail_from']][-1]['mail_subject']
    result = re.findall(r"\d+", mail_from_twitter)
    return result[0]


#------------smtp------------

def check_server(email_address):
    if 'outlook' in email_address:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        return server
    elif 'yahoo' in email_address:
        server = smtplib.SMTP_SSL("smtp.mail.yahoo.co.jp", 465)
        return server
    elif 'gmail' in email_address:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        return server
    else:
        print('not find smtp server')
        return None
    
def send_smtp_mail(my_account, my_password, msg):
    """
    引数msgをOutlookで送信
    """

    server = check_server(my_account)
    # ログインしてメール送信
    server.login(my_account, my_password)
    server.send_message(msg)
    server.quit()


def make_mime(to_mail, subject, body, from_mail, sender_name=None):
    """
    引数をMIME形式に変換
    """
    msg = MIMEText(body, 'html') #メッセージ本文
    msg['Subject'] = subject #件名
    msg['To'] = to_mail #宛先
    if not sender_name:
        msg['From'] = from_mail #送信元
    else:
        msg["From"] = email.utils.formataddr((sender_name, from_mail))
    return msg

def send_my_message(recipient, title, content, my_account, my_password, my_name):
    """
    メイン処理
    """
    # MIME形式に変換
    msg = make_mime(
        to_mail=recipient, #送信したい宛先を指定
        subject=title,
        body=content,
        from_mail=my_account,
        sender_name=my_name)

    
    # gmailに送信
    send_smtp_mail(my_account, my_password, msg)





if __name__ == '__main__':

    #-------temp email---
    domains_discord = ['@amozix.com','@tgvis.com','@tenvil.com','@mocvn.com','@anypsd.com','@maxric.com']
    email = create_email(domain=random.choice(domains_discord))
    
    # email = "3bjfyw2ixm@maxric.com"
    mail_list = get_mail_box2(email)
    
    

    import pdb;pdb.set_trace()
    auth_code = extract_twitter_code(mail_list)
    print(auth_code)
    # activate_url = extract_note_url(mail_list)


    
    #----smtp--------------
    recipient = '@gmail.com'
    title = 'まほーー！'
    content = 'みおみお！'
    # Outlook設定
    my_name = "あいな"
    my_account = '@outlook.com'
    my_password = ''
    send_my_message(recipient, title, content, my_account, my_password, my_name)
