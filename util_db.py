# -*- coding: utf-8 -*-
"""使い方- token/にsheetのjson

from util_db import Temple
tm = Temple(cnm='ruru')
tem_ple = tm._get('Temple)

tm.del_id(site='pc')

-------------

from util_db import UserModel, LogModel

user = UserModel(user_id, cnm)
user.profile = EMAIL
#user.keys() =  [user_id, cnm, name, profile, email, message, hajime, asiato, meruado_otosi, view]

log = LogModel()
log(login_id, time=datetime.datetime.now())
#lgm.keys() = [login_id, time, user_id, act]
"""
import sys

# sys.path.append(r'/home/ec2-user/.local/lib/python3.7/site-packages/')
import datetime
import json
import os
import pdb
import pickle
from collections import defaultdict

import boto3
import gspread
import pynamodb
import pandas as pd
#from dynamo_pandas import put_df, get_df, keys
import pysnooper
from boto3.dynamodb.conditions import Attr, Key
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from pynamodb.attributes import (JSONAttribute, ListAttribute, NumberAttribute,
                                DynamicMapAttribute, UnicodeAttribute,
                                UTCDateTimeAttribute, BooleanAttribute)
from pynamodb.models import Model
from pynamodb_utils import DynamicMapAttribute, AsDictModel, JSONQueryModel, TimestampedModel
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection, LocalSecondaryIndex
from datetime import timezone, datetime
from pynamodb_utils.utils import get_timestamp, parse_attrs_to_dict
from tinydb import Query, TinyDB, operations, where
import random
from glob import glob
import loguru
from loguru import logger






from dotenv import load_dotenv
# 環境変数を参照
load_dotenv()
SHEET_JSON_FILE = os.getenv('TEMPLE_JSON_FILE')
SHEET_KEY = os.getenv('TEMPLE_SHEET_KEY')

class MySheet:

    def __init__(self, file_path, worksheet, sheetname):
        gc = gspread.service_account(file_path)
        self.sh = gc.open(worksheet)
        self.wks = self.sh.worksheet(sheetname)

    def get_df(self):
        df = get_as_dataframe(self.wks, skiprows=0, header=0)
        df.dropna(how='all', inplace=True)
        return df

    def set_df(self, df):
        set_with_dataframe(self.wks, df)

    def set_df_new(self, sheetname, df):
        worksheet = self.sh.add_worksheet(title=sheetname)
        set_with_dataframe(worksheet, df)

class Temple:

    def __init__(self, cnm):
        self.cnm = cnm
        self.sh = Temple.get_sheet()
        #self.tem_ple = self._get('Temple')

    @classmethod
    def get_sheet(cls):
        # token_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'token'))
        # tokens = glob('{}/*sheet.json'.format(token_dir))
        # file_path = random.choice(tokens)
        gc = gspread.service_account(SHEET_JSON_FILE)
        return gc.open_by_key(SHEET_KEY)

    #@pysnooper.snoop()
    def _get(self, sheetname):
        cnm = self.cnm
        wks = self.sh.worksheet(sheetname)
        df = get_as_dataframe(wks, skiprows=0, header=0)
        df.dropna(subset=['cnm'], inplace=True)
        df = df.set_index('cnm', drop=False)
        d_dict = df.T.to_dict()
        return d_dict[cnm]

    #@pysnooper.snoop()
    def del_id(self, site):
        """
        site名指定でID削除

        Args:
            site (str): pc,hp,ik,jm
        """
        cnm = self.cnm
        logger.debug(cnm, site)
        wks = self.sh.worksheet('Temple')
        df = get_as_dataframe(wks, index='cnm', skiprows=0, header=0)
        df = pd.DataFrame(df)
        df.dropna(how='all', inplace=True)
        df = df.set_index('cnm', drop=False)
        df.at[cnm, site] = ""

        set_with_dataframe(wks, df)

    #cell_valで検索してwrite_valで置き換え
    #@pysnooper.snoop()
    def change_cell(self, sheetname, cell_val, write_val):
        """
        site名指定でID削除

        Args:
            site (str): pc,hp,ik,jm
        """
        #ワークシート選択
        wks = self.sh.worksheet(sheetname)
        #cell.value, cell.row, cell.col
        cell = wks.find(cell_val)
        wks.update_cell(cell.row, cell.col, write_val)

    #row_val = pc,hp などサイト名, col_val = cnm('mika','eri'...etc)
    #@pysnooper.snoop()
    @classmethod
    def write_cell(cls, sheetname, row_val, col_val, write_val):
        #ワークシート選択
        sh = Temple.get_sheet()
        wks = sh.worksheet(sheetname)
        #row,colのリストを取得してindex+1のrow & col valueを取得
        # [補足]第2引数が2の場合、値ではなく数式を格納する - worksheet.row_values(1,2)
        row_list = wks.row_values(1)
        col_list = wks.col_values(1)
        cell_col = row_list.index(row_val) + 1
        cell_row = col_list.index(col_val) + 1
        #書き込み
        wks.update_cell(cell_row, cell_col, write_val)
        logger.debug(f'chagne cell sheetname:{sheetname}-{row_val}:{col_val}={write_val}')

    @classmethod
    def add_row(cls, sheetname, row_vals):
        #ワークシート選択
        sh = Temple.get_sheet()
        wks = sh.worksheet(sheetname)
        #書き込み
        wks.append_row(row_vals, value_input_option='USER_ENTERED')
        logger.debug('append row: {}'.format(row_vals))


def get_cnm_list(ec2_name="happy1", site_name="pc"):
    """
    シートのec2行をチェックしてサーバー毎に動かすアカウントをチェックする
    """
    #変数
    sh = Temple.get_sheet()
    wks = sh.worksheet("Temple")
    df = get_as_dataframe(wks, skiprows=0, header=0)
    #df.dropna(subset=['cnm'], inplace=True)
    #df = df.set_index('cnm', drop=False)
    df = df[df['ec2'] == ec2_name]
    if site_name == "pc":
        df = df[df[site_name].str.startswith('1')]
    else:
        df = df[df[site_name].str.startswith('0')]
    return df['cnm'].to_list()


#cnmlist = get_cnm_list(ec2_name="happy1", site_name="pc")

class MyDB:

    def __init__(self, table_name):
        self.tablename = table_name
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(table_name)


    @classmethod
    def tables(cls):
        dynamodb = boto3.resource('dynamodb')
        table_list = dynamodb.tables.all()
        for table in table_list:
            logger.debug(table.table_name)

    def rm(self, key_dict):
        self.table.delete_item(Key=key_dict)

    def put(self, item_dict):
        res = self.table.put_item(
            Item=item_dict
        )
        return res

    def get(self, key_dict):
        items = self.table.get_item(
                    Key=key_dict
                )
        return items['Item'] if 'Item' in items else None

    # Partition Key（SerialNumber）での絞込検索
    def query(self, key, val):
        response = self.table.query(
            KeyConditionExpression=Key(key).eq(val)
        )
        return response['Items']

    def get_records(self, **kwargs):
        while True:
            response = self.table.scan()
            for item in response['Items']:
                yield item
            if 'LastEvaluatedKey' not in response:
                break
            kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])

    def scan(self):
        records = self.get_records(self.table)
        return records

    def update_item(self, key_dict, update_key, update_val):

        res = self.table.update_item(
            Key = key_dict,
            AttributeUpdates = {'flag':{'Action': 'PUT', update_key: update_val}},
            ReturnValues = 'UPDATED_NEW'
        )
        return res


def value2none(item_dict):
    for k, v in item_dict.items():
        if not v:
            item_dict[k] = None
            logger.debug("{0} change None".format(k))

    return item_dict

class IdTimeIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    index_name = 'pc-user-index'
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'LoginId_UpdatedAt_Index'
        region = 'ap-northeast-1'
        TZINFO = timezone.utc
        read_capacity_units = 5
        write_capacity_units = 5
        # All attributes are projected
        projection = AllProjection()
    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    login_id = UnicodeAttribute(default="0", hash_key=True)
    updated_at = UTCDateTimeAttribute(default=get_timestamp, range_key=True)


class TimeIndex(LocalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'time_index'
        region = 'ap-northeast-1'
        TZINFO = timezone.utc
        read_capacity_units = 5
        write_capacity_units = 5
        # All attributes are projected
        projection = AllProjection()
    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    user_id = UnicodeAttribute(hash_key=True)
    updated_at = UTCDateTimeAttribute(default=get_timestamp, range_key=True)

#user_id と gmailで検索
class GmailIndex(LocalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'gmail_index'
        region = 'ap-northeast-1'
        TZINFO = timezone.utc
        read_capacity_units = 5
        write_capacity_units = 5
        # All attributes are projected
        projection = AllProjection()
    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    user_id = UnicodeAttribute(hash_key=True)
    gmail = BooleanAttribute(null=False, default=False, range_key=True)


class EmailIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    index_name = 'pc-user-index'
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'email-index'
        region = 'ap-northeast-1'
        TZINFO = timezone.utc
        read_capacity_units = 2
        write_capacity_units = 2
        # All attributes are projected
        projection = AllProjection()
    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    email = UnicodeAttribute(default="", hash_key=True)
    

class UserModel(AsDictModel, JSONQueryModel, TimestampedModel):
    """pcmax user data.
    TimestampedModelを引数に入れると
    created_at,updated_at,deleted_atが key に追加"""

    class Meta:
        table_name = "pcmax_user"
        region = 'ap-northeast-1'
        TZINFO = timezone.utc
    user_id = UnicodeAttribute(hash_key=True)
    cnm = UnicodeAttribute(range_key=True)
    
    login_id = UnicodeAttribute(default="0")
    updated_at = UTCDateTimeAttribute(default=get_timestamp)
    time_index = TimeIndex()
    
    profile = DynamicMapAttribute(default=dict)
    # email_index = EmailIndex()
    email = UnicodeAttribute(default="")
    name = UnicodeAttribute(null=True)
    url = UnicodeAttribute(null=True)
    
    hajime = BooleanAttribute(null=False, default=False)
    asiato = BooleanAttribute(null=False, default=False)
    meruado = BooleanAttribute(null=False, default=False)
    gmail = BooleanAttribute(null=False, default=False)
    
    message = ListAttribute(default=list)
    
    view = NumberAttribute(default=0)



class AccountModel(AsDictModel, TimestampedModel):
    """アカウントの状態をチェック"""
    class Meta:
        table_name = "Account"
        region = 'ap-northeast-1'
        TZINFO = timezone.utc
    
    user_id = UnicodeAttribute(hash_key=True)
    cnm = UnicodeAttribute(range_key=True)
    #idx,key,valのdict の list
    message = ListAttribute(default=list)
    time = UTCDateTimeAttribute(default=datetime.now())


class LogModel(Model):
    """
    lg = LogModel(login_id, time, user_id=user_id, act=act, cnm=cnm)
    lg.save()
    """
    class Meta:
        table_name = "log"
        region = 'ap-northeast-1'
        #read_capacity_units = 5
        #write_capacity_units = 5
        TZINFO = timezone.utc

    login_id = UnicodeAttribute(hash_key=True)
    time = UTCDateTimeAttribute(range_key=True, default=datetime.now())
    user_id = UnicodeAttribute(null=True)
    cnm = UnicodeAttribute(null=True)
    act = UnicodeAttribute(null=True)
    


from pprint import pprint

if __name__ == '__main__':

    user_id = '18384941'
    cnm = 'miho'
    email='@gmail.com'
    # user = UserModel.get(user_id, cnm)
    # import pdb;pdb.set_trace()

    users = UserModel.email_index.query(email)
    user = users.next()
    pprint(user.as_dict())
    
        
    # user = UserModel.get(user_id, cnm)
    import pdb;pdb.set_trace()
    cnm = 'mika'
    site = 'pc'
    tm = Temple(cnm)
    sheetname = 'Temple'
    tm = Temple(cnm)
    tem_ple = tm._get(sheetname)
    cell_val = tem_ple['pc']
    write_val = "{0}-{1}".format('15', cell_val)

    tm.write_cell(sheetname, site, cnm, write_val)


    import pdb;pdb.set_trace()
    #df_dict = [dd for k, y in df_dict_list.items() if dd['cnm'] == cnm]
    #tm.del_id(site)
    #logger.debug(tem_ple)


