#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import time
import requests
import re
import random
import get_our_email
import publicFun
from bs4 import BeautifulSoup

def get_user_message():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36'
    headers = {
        'User-Agent': ua,
        'Connection': 'close'
    }
    proxy = {
        "http" : "192.168.1.250:7890"
    }
    user_detail = {}
    url = 'https://www.fakeaddressgenerator.com/World_Address/get_us_address1/state/CA'
    response = requests.get(url,headers=headers,proxies=proxy,timeout = 10)
    soup = BeautifulSoup(response.text, "html.parser")
    title_list = []
    value_list = []
    soups = soup.select('body > div.container.index.no-padding > div.row.main > div.col-md-9.col-sm-9.col-xs-12.main-left > div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > table ')
    if soups:
        a = re.findall('<tr>(.*)</tr>',str(soups[0]))
        b = a[0].split("</td><td>")
        for c in b[0:-1]:
            title = c.split("</span>")[0].split('<span>')[-1]
            title_list.append(title)
        for d in b[1:]:
            value = d.split("</strong>")[0].split('<strong>')[-1]
            value_list.append(value)
        for i in range(4, 11):
            soups1 = soup.select(
                'body > div.container.index.no-padding > div.row.main > div.col-md-9.col-sm-9.col-xs-12.main-left > div > div > div:nth-child(2) > div:nth-child({})'.format(
                    i))
            title = str(soups1[0]).split("</span>")[0].split('<span>')[-1]
            title_list.append(title)
            value = str(soups1[0]).split("</strong>")[0].split('<strong>')[-1]
            value = value.split('value="')[-1].split('"/>')[0]
            value_list.append(value)
        user_detail = dict(zip(title_list, value_list))
        email,email_password,email_server = get_our_email.get_email()
        user_detail.update({'email': email,'email_pwd':email_password,'email_server':email_server})
        register_time = time.strftime("%Y-%m-%d %X", time.localtime())
        user_detail.update({'register_time': register_time})
    else:
        print("未取到值")
    #print(user_detail)
    return user_detail


if __name__ == '__main__':
    while True:
        username = ''.join(random.sample("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 13))
        try:
            user_detail = get_user_message()
            if len(user_detail)>=10:
                data = []
                data.append(username)
                for key in user_detail:
                    data.append(user_detail[key])

                print(data)
                publicFun.add_user_detail(data)
        except Exception as e:
            #tb.print_exc()
            print('获取用户信息失败')
            continue
        finally:
            this_time = time.strftime("%Y-%m-%d %X", time.localtime())
            print(this_time)
            time.sleep(60)