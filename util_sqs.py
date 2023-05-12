# -*- coding: utf-8 -*-
"""使い方

import util_sqs

#queue_nameが存在しなければ作成してメッセージのリストを送信
res_list = util_sqs.send_msg(queue_name, msg_list)
#queueに入ってるmessageをmax_num個数分ゲット（max_num=10まで）
#ついでにqueueのメッセージを消去
msg_list = util_sqs.get_msg(queue_name, max_num=5)


"""
import boto3
import json

#---debug--------------------------------
import pysnooper
import loguru
from loguru import logger
import functools
import time

def logger_wraps(*, entry=True, exit=True, level="DEBUG"):

    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            try:
                start_time = time.time()
                if entry:
                    logger_.log(level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs)
                result = func(*args, **kwargs)
                if exit:
                    logger_.log(level, "Exiting '{}' (result={})", name, result)
                end_time = time.time() - start_time
                if (entry==True) and (entry==exit):
                    logger_.log(level, "'{} time is ' ()", name, end_time)
                return result
            except Exception as e:
                logger_.exception(e)
                raise
        return wrapped

    return wrapper

#---debug--------------------------------


#@pysnooper.snoop()
def split_list(l, n):
    """
    リストをサブリストに分割する
    :param l: リスト
    :param n: サブリストの要素数
    :return:
    """
    for idx in range(0, len(l), n):
        yield l[idx:idx + n]

#@pysnooper.snoop()
def get_queue(queue_name: str):
    sqs = boto3.resource('sqs')
    try:
        # キューの名前を指定してインスタンスを取得
        queue = sqs.get_queue_by_name(QueueName=queue_name)
        logger.debug('get queue. name={}'.format(queue_name))
        return queue
    except:
        # 指定したキューがない場合はexceptionが返るので、キューを作成
        queue = sqs.create_queue(QueueName=queue_name)
        logger.debug('not queue. create queue name={}'.format(queue_name))
        return queue

#@pysnooper.snoop()
def send_msg(queue_name: str, msg_list: list):
    """
    Args:
        queue_name(str): 送信先のキューの名前
        msg_list (list): [list of dict(message)]
    Return:
        メッセージのDict
    """
    # メッセージキューに送信
    queue = get_queue(queue_name)
    #msg_list = [json.dumps(msg) for msg in msg_list]
    msg_list = [{'Id' : '{}'.format(i+1), 'MessageBody' : json.dumps(msg_list[i])} for i in range(len(msg_list))]
    res_list = []
    for msg_l in split_list(msg_list,10):
        response = queue.send_messages(Entries=msg_l)
        logger.debug('queue_name={} sent message={}'.format(queue_name, msg_l))
        res_list.append(response)
    return res_list

#@pysnooper.snoop()
def get_msg(queue_name: str, get_num=1):
    queue = get_queue(queue_name)
    msg_list = queue.receive_messages(MaxNumberOfMessages=get_num)
    msg_dict_list = []
    for message in msg_list:
        msg_dict_list.append(json.loads(message.body))
        message.delete()
        logger.debug('queue_name={} get & delete message={}'.format(queue_name, message))
    return msg_dict_list

if __name__ == "__main__":

    #queue = get_queue(queue_name)
    ##msg_list = queue.receive_messages(MaxNumberOfMessages=5)

    queue_name = 'activate-accounts'
    queue = get_queue(queue_name)

    msgs = get_msg(queue_name)


    # msg_list = [ac1, ac2, ac3]
    # # import pdb;pdb.set_trace()
    # res_list = send_msg(queue_name, msg_list)
    #msg_list = get_msg(queue_name, get_num=5)
    import pdb;pdb.set_trace()
    msg_list = get_msg(queue_name)
    print('sqs')
