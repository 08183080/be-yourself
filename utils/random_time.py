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
    return random_time

if __name__ == "__main__":
    for i in range(20):
        r = get_random_time()
        print(r) #print(r, type(r))