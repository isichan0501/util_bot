import os
import requests
import time
import random
import json


from dotenv import load_dotenv

# 環境変数を参照
load_dotenv()
SMSHUB_API_KEY = os.getenv('SMSHUB_API_KEY')
IPROYAL_API_TOKEN = os.getenv('IPROYAL_API_TOKEN')





if __name__ == "__main__":

    

    headers = {
        'X-Access-Token': IPROYAL_API_TOKEN,
    }

    response = requests.get('https://dashboard.iproyal.com/api/residential/royal/reseller/access/countries', headers=headers)

    import pdb;pdb.set_trace()
    print(response)