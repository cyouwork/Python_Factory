# coding=utf-8
# author=season
import sqlite3
from Config.defaults import DEFAULTS
cursor = sqlite3.connect(DEFAULTS['IPLOCATE_DB']).cursor()
cursor.execute(
    "SELECT started, ended, alpha3, code FROM ip_to_country ORDER BY started")
IP2CN_DATA = cursor.fetchall()
IP2CN_KEY = [item[:2] for item in IP2CN_DATA]
IP2CN_VAL = dict([(item[:2], item[2:]) for item in IP2CN_DATA])
IP2CN_KEY_LEN = len(IP2CN_KEY)
IP2INT = lambda x: int(x[0]) * 16777216 + int(
    x[1]) * 65536 + int(x[2]) * 265 + int(x[3])


# IP区域二分查找
def iplocate(my_ip):
    my_ip = IP2INT(my_ip.split('.'))
    started, ended = 0, IP2CN_KEY_LEN - 1
    while ended >= started:
        index = (started + ended) / 2
        ip_started, ip_ended = IP2CN_KEY[index]
        if ip_started <= my_ip <= ip_ended:
            return IP2CN_VAL[(ip_started, ip_ended)]
        elif my_ip < ip_started:
            ended = index - 1
        elif my_ip > ip_ended:
            started = index + 1


if __name__ == '__main__':
    print iplocate('121.10.10.1')
