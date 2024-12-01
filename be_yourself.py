import os
import yagmail
import schedule
import time
import random
from datetime import datetime


def get_random_time():
    """
    生成 14:00 至 20:00 之间的随机时间
    """
    start_time = datetime.strptime("14:00", "%H:%M").time()
    end_time = datetime.strptime("20:00", "%H:%M").time()

    # 随机选择时间点
    random_hour = random.randint(start_time.hour, end_time.hour)
    random_minute = random.randint(0, 59)

    # 调整时间边界
    if random_hour == start_time.hour and random_minute < start_time.minute:
        random_minute = start_time.minute
    if random_hour == end_time.hour and random_minute > end_time.minute:
        random_minute = end_time.minute

    random_time = f"{random_hour:02}:{random_minute:02}"
    return random_time


def get_contents(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def get_emails(path):
    with open(path, 'r') as f:
        return f.read().splitlines()


def get_one_file(path):
    """
    从 path 目录中随机选择一个文件，返回其完整路径
    """
    files = os.listdir(path)
    return os.path.join(path, random.choice(files))


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
        # 执行邮件发送任务
        p = '/root/be-yourself/data'
        path = get_one_file(p)
        src = '19121220286@163.com'
        tos = get_emails('emails.txt')
        subject = '今日戒色信息流'
        contents = get_contents(path)
        attachments = path

        send_emails(src, tos, subject, contents, attachments)

        # 任务完成后设置下一天的随机时间
        random_time = get_random_time()
        print(f"任务完成。下一个邮件发送时间: {random_time}")
        schedule.clear('daily_task')  # 清除之前的任务
        schedule.every().day.at(random_time).do(daily_task).tag('daily_task')  # 设置新的任务
    except Exception as e:
        print(f"{e} occurred in daily_task")


if __name__ == '__main__':
    try:
        # 初始化第一次的任务
        random_time = get_random_time()
        print(f"首次邮件发送时间: {random_time}")
        schedule.every().day.at(random_time).do(daily_task).tag('daily_task')

        # 启动调度器
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        print(f"{e} occurred~")
