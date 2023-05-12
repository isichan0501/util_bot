
# -*- coding: utf-8 -*-

import pdb

import boto
import boto3
import botocore
import paramiko
import pysnooper
import time
import os
import configparser
import loguru
from loguru import logger
import sys
from contextlib import contextmanager
import subprocess
import asyncio




from dotenv import load_dotenv
# 環境変数を参照
load_dotenv()
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')
REGION_NAME = os.getenv('AWS_REGION_NAME')
PEM_KEY = os.getenv('AWS_PEM_KEY')

#paramiko log
os.makedirs('logs', exist_ok=True)
LOG_FILE='logs/p_log.txt'


paramiko.util.log_to_file(LOG_FILE)


# #@pysnooper.snoop()
def get_ec2_client(region=REGION_NAME):
    ec2 = boto3.session.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY).client('ec2', region)
    return ec2

#@pysnooper.snoop()
def get_ec2_resouce(region=REGION_NAME):
    ec2 = boto3.resource(
        service_name='ec2',
        region_name=region,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY)
    return ec2


# parse tags lists
def parse_sets(tags):
    result = {}
    for tag in tags:
        key = tag['Key']
        val = tag['Value']
        result[key] = val
    return result


#find instance with instance name
def find_ec2_instanceid(instance_name):
    ec2 = get_ec2_client()
    instances = ec2.describe_instances()
    instance_list = []
    for reservations in instances['Reservations']:
        for instance in reservations['Instances']:
            tags = parse_sets(instance['Tags'])
            if tags['Name'] == instance_name:
                return instance['InstanceId']


def ec2_return_public_ip(instance_name):
    instance_id = find_ec2_instanceid(instance_name)
    ec2 = get_ec2_resouce()
    instance = ec2.Instance(instance_id)
    ip = instance.public_ip_address
    logger.debug(f"IPアドレス: {ip}")
    return ip


def show_alive_instances():
    ec2 = get_ec2_resouce()
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    i = 0
    for instance in instances:
        logger.debug(instance.id, instance.instance_type)
        i += 1


#startかstopした場合だけreturn True
def ec2_start_from_name(instance_name, is_stop=False):
    try:
        instance_id = find_ec2_instanceid(instance_name)
        ec2 = get_ec2_resouce()
        instance = ec2.Instance(instance_id)
        #commandがstartで起動中じゃなければ
        if is_stop == False:
            if instance.state['Name'] == 'running':
                logger.debug("instance is running.")
            else:
                logger.debug("instance is not running. start instance")
                instance.start()
                instance.wait_until_running()
                logger.debug("instance is start!")
                return True
        else:
            if instance.state['Name'] == 'stopped':
                logger.debug("instance is stopped.")
            else:
                logger.debug("instance is running. stopping instance")
                instance.stop()
                instance.wait_until_stopped()
                logger.debug("instance is stop!")
                return True
        return False
    except (botocore.exceptions.ClientError, Exception) as e:
        logger.exception(e)

#sshclientをyield
@contextmanager
def yield_ssh_client(instance_name):
    instance_id = find_ec2_instanceid(instance_name)
    ec2 = get_ec2_resouce()
    instance = ec2.Instance(instance_id)
    try:
        client = paramiko.SSHClient()
        client.known_hosts = None
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        privkey = paramiko.RSAKey.from_private_key_file(PEM_KEY)
        client.connect(instance.public_dns_name,username='ec2-user', pkey=privkey, timeout=60)
        yield client
    finally:
        client.close()

#戻り値をutf8でデコードしてLISTでリターン
##@pysnooper.snoop()
def exec_ec2(instance_name, exec_cmd):
    try:
        cmd_result = ''
        with yield_ssh_client(instance_name) as client:
            stdin, stdout, stderr = client.exec_command(exec_cmd, get_pty=True)
            #シェルに入力するばあい
            #stdin.write("write")
            stdin.flush()
            #time.sleep(3)
            #print('\x03', file=stdin, end='')
            #stdin.channel.shutdown_write()  # <--- これが必要
            #stdin.close()
            data = stdout.read().splitlines()
            for line in data:
                add_line = line.decode('utf-8') + '\n'
                cmd_result += add_line
                logger.debug(line.decode())
        return cmd_result
    except KeyboardInterrupt:
        logger.debug('press ctrl + c. end')
        #print('\x03', file=stdin, end='')
        sys.exit()
    except Exception as e:
        logger.exception(e)


#instance_dict- key= id, type, state, name　のlistをreturn
def get_all_instance():
    ec2 = boto3.client('ec2')
    ec2_data = ec2.describe_instances()
    instance_list = []
    for ec2_reservation in ec2_data['Reservations']:
        for ec2_instance in ec2_reservation['Instances']:
            tags = parse_sets(ec2_instance['Tags'])
            instance_dict = {
                'id': ec2_instance['InstanceId'],
                'type': ec2_instance['InstanceType'],
                'state': ec2_instance['State']['Name'],
                'name': tags['Name'],
            }
            instance_list.append(instance_dict)
            #pprint(instance_dict)

    return instance_list


#task = 実行する関数名
##@pysnooper.snoop()
def fire_and_forget(task, *args, **kwargs):
    loop = asyncio.get_event_loop()
    if callable(task):
        return loop.run_in_executor(None, task, *args, **kwargs)
    else:   
        raise TypeError('Task must be a callable')

def exec_subprocess(task, exec_cmd):
    if callable(task):
        p = subprocess.Popen("exec " + exec_cmd, shell=True)       # execで実行
        p.kill()
    else:
        raise TypeError('Task must be a callable')

def get_public_ip():
    cmd = ["curl", "inet-ip.info"]
    try:
        result = subprocess.check_output(' '.join(cmd), shell=True)
        public_ip = result.decode('utf-8').strip()
        return public_ip
    except subprocess.CalledProcessError as e:
        logger.exception(e)
        return False

##@pysnooper.snoop()
def get_pid_from_filename(file_name):
    #変数
    cmd = ["ps", "-ax", "|", "grep", file_name]
    try:
        result = subprocess.check_output(' '.join(cmd), shell=True)
        #要素に 'bash' or 'python' などがあるプロセス
        pid_line = [line for line in result.decode('utf-8').splitlines() if ('ps' not in line.split()) and ('grep' not in line.split())]
        #pid_line = [line for line in result.decode('utf-8').splitlines() if program_code in line.split()]
        #ps -axの戻り値を空白で分割した最初の要素がpidなので
        if len(pid_line) != 0:
            pid_line[0].split()
            pid = pid_line[0].strip().split()[0]
            return int(pid)
        else:
            return False
    except subprocess.CalledProcessError as e:
        logger.exception(e)
        return False

#instanceのNameタグとfilenameを指定してreturn pid. else return False
##@pysnooper.snoop()
def get_pid_from_instance(instance_name, file_name):
    logger.debug('instance_name = {}. file_name = {}'.format(instance_name, file_name))
    exec_cmd = "ps -ax | grep {}".format(file_name)
    exec_output = exec_ec2(instance_name, exec_cmd)
    #is_pid = exec_output.strip().split()
    pid_line = [line for line in exec_output.splitlines() if ('ps' not in line.strip().split()) and ('grep' not in line.strip().split())]
    logger.debug("pid_line={}".format(pid_line))
    if len(pid_line) != 0:
        pid_str = pid_line[0].strip().split()[0]
        logger.debug('pid = {} is exist!'.format(pid_str))
        return int(pid_str)
    else:
        logger.debug('file_name={} is not exist!'.format(file_name))
        return False

##@pysnooper.snoop()
def kill_process(kill_instance, kill_file):
    pid_int = get_pid_from_instance(kill_instance, kill_file)
    if pid_int:
        logger.debug('instance_name = {}. file_name = {}.kill {}'.format(kill_instance, kill_file, pid_int))
        exec_cmd = "kill {}".format(pid_int)
        exec_output = exec_ec2(kill_instance, exec_cmd)
        logger.debug(exec_output)

@pysnooper.snoop()
def run_if_not_exist(instance_name, file_name, *args):
    pid_int = get_pid_from_instance(instance_name, file_name)
    #引数があればexec_cmdに追加する
    if args:
        args = " " + " ".join(list(args))
    else:
        args = ""
    #プロセスが存在しなければ
    if not pid_int:
        if file_name.split('.')[-1] == 'py':
            exec_cmd = "python {}".format(file_name)
            exec_cmd+=args
            logger.debug('instance_name = {}.file_name = {} is not running. exec {}'.format(instance_name, file_name, exec_cmd))
            #exec_output = exec_ec2(instance_name, exec_cmd)
            #exec_ec2(instance_name, exec_cmd)
            fire_and_forget(exec_ec2, instance_name, exec_cmd)
        else:
            exec_cmd = "bash {}".format(file_name)
            exec_cmd+=args
            logger.debug('instance_name = {}.file_name = {} is not running. exec {}'.format(instance_name, file_name, exec_cmd))
            fire_and_forget(exec_ec2, instance_name, exec_cmd)
            #exec_ec2(instance_name, exec_cmd)
    else:
        logger.debug('process is exist. pid = {}'.format(pid_int))


def get_instance_state(instance_name):
    instances = get_all_instance()
    instance_info = [d for d in instances if d.get('name') == instance_name]
    print('{} is {}'.format(instance_name, instance_info[0]['state']))
    if instance_info[0]['state'] == 'stopped':
        return False
    else:
        return


#アクティブな状態ならreturn 'ok'
def get_instance_status(instance_name):
    ec2 = boto3.client('ec2')
    instance_id = find_ec2_instanceid(instance_name)
    response = ec2.describe_instance_status(InstanceIds=[instance_id])
    if not response['InstanceStatuses']:
        print(f'{instance_name} is stopped')
        return False

    instance_status = response['InstanceStatuses'][0]['InstanceStatus']['Status']
    print(f'{instance_name} is active')
    if instance_status == 'ok':
        return True
    else:
        return False



@pysnooper.snoop()
def ec2_send_command(instance_name, exec_cmd):
    instance_id = find_ec2_instanceid(instance_name)
    ssm = boto3.client('ssm')
    ssm_client = boto3.client('ssm')
    response = ssm_client.send_command(
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': exec_cmd},
        InstanceIds=[instance_id],
    )

    time.sleep(5.0)

    command_id = response['Command']['CommandId']

    output = ssm_client.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id,
    )
    print("Output = \n{}\n".format(output['StandardOutputContent']))
    print("Error  = \n{}\n".format(output['StandardErrorContent']))



#ec2起動→pcmax/main.py→再起動（IP変える）を繰り返す
def main():
    from util_db import get_cnm_list
    instance_name = 'happy2'
    file_name = "RunPcmax.sh"
    cnm_list = get_cnm_list(ec2_name=instance_name, site_name="pc")
    print(cnm_list)

    for cnm in cnm_list:
        while True:
            is_state = get_instance_state(instance_name)
            print(f'instance = {instance_name} is {is_state}. cnm = {cnm}')
            if not is_state:
                is_status = get_instance_status(instance_name)
                if not is_status:
                    ec2_start_from_name(instance_name, is_stop=False)
                    time.sleep(10)
                    is_status = get_instance_status(instance_name)
                    if not is_status:
                        continue
                    run_if_not_exist(instance_name, file_name, cnm)
                    time.sleep(10)
                    break
                    
            time.sleep(60)
        
    # pcpid = get_pid_from_instance(instance_name, file_name)
    # commands = "pgrep -a python3.7 | grep pc_main.py".split()
    # exec_cmd = ["pgrep -a python3.7 | grep pc_main.py"]
    
#ec2を停止→起動してpublic ipを返す
def ec2_restart_from_name(instance_name):
    nowip = ec2_return_public_ip(instance_name=instance_name)
    #まず停止
    ec2_start_from_name(instance_name=instance_name, is_stop=True)
    #起動
    ec2_start_from_name(instance_name=instance_name, is_stop=False)
    return ec2_return_public_ip(instance_name=instance_name)


if __name__ == '__main__':
    """ec2-proxyで構築したプロキシ用のEC2インスタンスを再起動してIP変更。
    ※インスタンスのIPは構築時に取得済み
    インスタンスのnameは Proxy Node 1 ~ Proxy Node 19
    1.インスタンス一覧を取得してプロキシ用だけ抽出
    2.インスタンスの起動状態を確認
    3.再起動
    """
    from pprint import pprint

    #インスタンス全ての情報
    instances = get_all_instance()
    #プロキシ用だけ
    instances_proxy = [i for i in instances if i['name'].startswith('Proxy Node')]
    iplist = []
    for ins in instances_proxy:
        ip = fire_and_forget(ec2_restart_from_name, ins['name'])
        iplist.append(ip)
        
    

    """ {'id': 'i-0fb1aa46d47e274b1',
    'name': 'Proxy Node 3',
    'state': 'running',
    'type': 't2.micro'}]
    """
    import pdb;pdb.set_trace()
        
    

    
    
    
    # pcpid = get_pid_from_instance(instance_name, file_name)
    # commands = "pgrep -a python3.7 | grep pc_main.py".split()
    # exec_cmd = ["pgrep -a python3.7 | grep pc_main.py"]
    
    
    
    
    # is_state = get_instance_state(instance_name)


    # exec_cmd = "pgrep -a python3.7 | grep pc_main.py"

    # ec2_send_command(instance_name, [exec_cmd])
    
    # exec_ec2(instance_name, exec_cmd)
    
    # instance_id = find_ec2_instanceid(instance_name)
    
    # ec2 = get_ec2_resouce(region=REGION_NAME)
    # #ec2 = boto3.resource('ec2')
    # instance = ec2.Instance(instance_id)
    # pdb.set_trace()
    # print("インスタンス停止開始")
    # instance.stop()
    # instance.wait_until_stopped()
    # print("インスタンス停止完了")
    # pdb.set_trace()
    # instance_name = "twurl4"
    # exec_cmd = "python3 hello.py"
    # exec_ec2(instance_name, exec_cmd)
    # pdb.set_trace()
