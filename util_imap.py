
from imbox import Imbox
import datetime
from urlextract import URLExtract
import re


# SSL Context docs https://docs.python.org/3/library/ssl.html#ssl.create_default_context
# outlook_host = 'imap-mail.outlook.com'
# hotmail = 'outlook.office365.com'

outlook_host = 'imap-mail.outlook.com'
hotmail_host = 'outlook.office365.com'
gmail_host = 'imap.gmail.com'


def find_url(content):
    extractor = URLExtract()
    urls = extractor.find_urls(content)
    print(urls)
    return urls


#hotmail用
def get_verify_link(email, email_pw, sent_from="verify@twitter.com"):

    if 'outlook' in email:
        host = 'imap-mail.outlook.com'
    elif 'hotmail' in email:
        host = 'outlook.office365.com'
    else:
        host = 'outlook.office365.com'

    msglist = []
    with Imbox(host,
            username=email,
            password=email_pw,
            ssl=True,
            ssl_context=None,
            starttls=False) as imbox:

        # Messages sent FROM
        inbox_messages = imbox.messages(sent_from=sent_from)
        for uid, message in inbox_messages:
            # emaildict = dict(**message.sent_from[0], **{"plain": message.body.get('plain')[0]})
            msglist.append(dict(**message.sent_from[0], **{"plain": message.body.get('plain')[0], "date": message.date}))

    return msglist


from urlextract import URLExtract

def find_url(content):
    extractor = URLExtract()
    urls = extractor.find_urls(content)
    # print(urls)
    return urls



def get_twitter_pin_code(msg_list):
    mail_from_twitter = [k for k in msg_list if 'info@twitter.com' in k['sent_from'][0]['email']][0]['subject']
    result = re.findall(r"\d+", mail_from_twitter)
    return result[0]


def check_host(email):
    if 'hotmail' in email:
        return hotmail_host
    elif 'outlook' in email:
        return outlook_host
    elif 'gmail' in email:
        return gmail_host
    else:
        return hotmail_host


def get_all_msg(email, email_pw):
    msg_list = []
    with Imbox(check_host(email),
            username=email,
            password=email_pw,
            ssl=True,
            ssl_context=None,
            starttls=False) as imbox:

        # Get all folders
        status, folders_with_additional_info = imbox.folders()

        # Gets all messages from the inbox
        all_inbox_messages = imbox.messages()
        
        
        for uid, message in all_inbox_messages:
            # Every message is an object with the following keys
            msg_list.append(
                {
                    'sent_from': message.sent_from,
                    'sent_to': message.sent_to,
                    'subject': message.subject,
                    'headers': message.headers,
                    'plain': message.body.get('plain'),
                    'message_id': message.message_id,
                    'sent_from': message.date,
                    'sent_from': message.sent_from,
                    'sent_from': message.sent_from,
                    'sent_from': message.sent_from,
                    'sent_from': message.sent_from
                }
            )
        
    return msg_list


outlook_host = 'imap-mail.outlook.com'
hotmail_host = 'outlook.office365.com'
gmail_host = 'imap.gmail.com'

    
if __name__ == "__main__":

    email = "exaple@hotmail.com"
    email_pw = "pw"
    msg_list = get_all_msg(email, email_pw)
    
    # import pdb;pdb.set_trace()
    # with Imbox(hotmail_host,
    #         username=email,
    #         password=email_pw,
    #         ssl=True,
    #         ssl_context=None,
    #         starttls=False) as imbox:

    #     all_inbox_messages = imbox.messages()

    import pdb;pdb.set_trace()
    pin_code = get_twitter_pin_code(msg_list)
    
    # import pdb;pdb.set_trace()
    print(pin_code)
    # msgs = get_verify_link(email, email_pw, sent_from="verify@twitter.com")
    # import pdb;pdb.set_trace()
    # print(msgs)

    

