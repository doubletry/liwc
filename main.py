# -*- coding: UTF-8 -*-

import random
import requests
import math
import time
import json


class CampusNet:

    def __init__(self):
        with open('./conf.json', 'r') as f:
            text = json.load(f)

        self.username = text['username']
        self.password = text['password']
        self.status = False
        self.cookies = None
        self.ip = None

    def login(self):

        d = 'action=login&ac_id=1&user_ip=&nas_ip=&user_mac=&url=&username={}&password={}'.format(self.username,
                                                                                                  self.password)

        h = {
            'Host': '10.255.44.33',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://10.255.44.33',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'http://10.255.44.33/srun_portal_pc.php?ac_id=1&',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        if self.cookies is not None:
            h['Cookie'] = 'login=' + self.cookies
        h['Content-Length'] = str(len(d))

        r = requests.post(url='http://10.255.44.33/srun_portal_pc.php', headers=h, data=d)
        self.cookies = requests.utils.dict_from_cookiejar(r.cookies)['login']

    def logout(self):

        d = 'action=auto_logout&info=&user_ip={}&username={}'.format(self.ip, self.username)

        h = {
            'Host': '10.255.44.33',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://10.255.44.33',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'http://10.255.44.33/srun_portal_pc.php?ac_id=1&',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        if self.cookies is not None:
            h['Cookie'] = 'login=' + self.cookies

        r = requests.post(url='http://10.255.44.33/srun_portal_pc.php', headers=h, data=d)
        self.cookies = None
        self.ip = None

    def update_ip(self):

        k = math.floor(random.random() * (100000 + 1))
        d = 'action=get_online_info&key=' + str(k)

        h = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': '10.255.44.33',
            'Origin': 'http://10.255.44.33',
            'Referer': 'http://10.255.44.33/srun_portal_pc.php',
            'X-Requested-With': 'XMLHttpRequest'
        }

        if self.cookies is not None:
            h['Cookie'] = 'login=' + self.cookies
        h['Content-Length'] = str(len(d))

        r = requests.post(url='http://10.255.44.33/include/auth_action.php', params={'k': str(k)}, headers=h, data=d)
        self.ip = r.text.split(',')[-1]



if __name__ == '__main__':
    net = CampusNet()

    net.login()
    print('Login')
    net.update_ip()
    print('Ip: {}'.format(net.ip))
    time.sleep(10)
    net.logout()
    print('Logout')
