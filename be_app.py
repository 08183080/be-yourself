import os
import yagmail
import schedule
import time
import random
from datetime import datetime

def get_random_time():
    # 计算14:00到20:00之间的时间范围
    start_time = datetime.strptime("14:00", "%H:%M").time()
    end_time = datetime.strptime("20:00", "%H:%M").time()
    
    # 随机选择一个时间点
    random_hour = random.randint(start_time.hour, end_time.hour)
    random_minute = random.randint(0, 59)
    
    # 如果随机时间在14:00之前，调整为14:00
    if random_hour == start_time.hour and random_minute < start_time.minute:
        random_minute = start_time.minute
    
    # 如果随机时间在20:00之后，调整为19:59
    if random_hour == end_time.hour and random_minute > end_time.minute:
        random_minute = end_time.minute
    
    random_time = f"{random_hour:02}:{random_minute:02}"
    # print('随机发送时间: ',random_time)
    return random_time


def get_contents(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_emails(path):
    with open(path, 'r') as f:
        return f.read().splitlines()


def get_one_file(path):
    '''
    在path目录中随便选择个文件，返回路径+文件名的绝对路径
    '''
    files = os.listdir(path)
    return path + '/' + random.choice(files)

def send_email(src, dst, subject, contents, attachments):
    pwd = os.environ.get('wangyi_emai_auth')

    yag = yagmail.SMTP(user=src, password=pwd, host='smtp.163.com', port='465')
    yag.send(to=dst, subject=subject, contents=contents, attachments=attachments)
    yag.close()

def send_emails(src, tos, subject, contents, attachments):
    for to in tos:
        send_email(src, to, subject, contents, attachments)  

def daily_task():
    try:
        p = '/root/be-yourself/data' # if windows another path
        path = get_one_file(p)
        src = '19121220286@163.com'
        tos = get_emails('emails.txt') 
        subject = '今日戒色信息流'
        contents = get_contents(path)
        attachments = path
        
        send_emails(src, tos, subject, contents, attachments)
    except Exception as e:
        print(f"{e} occured in daily_task")

if __name__ == '__main__':
    try:
        schedule.every().day.at(get_random_time()).do(daily_task)

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        print(f"{e} occured~")

    # p = r'/root/be-yourself/data'
    # path = get_one_file(p)
    # print(path)