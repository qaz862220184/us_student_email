#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import re
import publicFun
import time
import get_our_email

def get_edu_email(email,email_passwor,email_server):
    email_msg = get_our_email.get_email_msg(email,email_passwor,email_server)
    #print(email_msg)
    if email_msg['header'].get('send_address') == 'NO_Reply@mccd.edu':
        #print('就是这条邮件')
        body = email_msg['body']
        #print(body,type(body))
        # 这边是取出学生ID
        stu_id = re.findall('Your student ID number at Merced College is:.*',body)
        stu_id = re.search('\d{7}', stu_id[0]).group()
        #print(stu_id)
        # 这里是获取学生邮箱地址
        stu_email = re.findall('Your Merced College e-mail address is.*', body)
        stu_email = re.search('\w+.\w+@campus.mccd.edu', stu_email[0]).group()
        #print(stu_email)

    else:
        print('不是这封邮件')
        print(email_msg['header'].get('send_address'))

    return stu_id,stu_email


def change_date(date):
    m, d, y = date.split('/')
    m = m.zfill(2)
    d = d.zfill(2)
    y = y[-2:]
    edu_pwd = m + d + y
    return edu_pwd


def main():
    stu_register = publicFun.get_user_detail(2)
    if stu_register:
        email = stu_register['email']
        email_password = stu_register['email_pwd']
        email_server = stu_register['email_server']
        Birthday = stu_register['birthday']
        print(email, email_password, email_server, Birthday)
        global stu_id, edu_email
        stu_id, edu_email = '', ''
        edu_pwd = change_date(Birthday)

        try:
            stu_id, edu_email = get_edu_email(email,email_password,email_server)
        except Exception as e:
            #publicFun.update_user_tag(email, 5)
            publicFun.logger.info('%s获取邮箱信息失败'%email)
            print('获取邮箱信息失败')
        print(stu_id, edu_email, edu_pwd)
        if stu_id and edu_email and edu_pwd:
            collect_time = time.strftime("%Y-%m-%d %X", time.localtime())
            publicFun.add_email_detail([stu_id, edu_email, edu_pwd,collect_time,531])
            publicFun.delete_user_detail_succeed(email)
        else:
            publicFun.logger.info('%s未获得完整学生邮箱信息'%email)
            print('未获得完整学生邮箱信息')
    else:
        time.sleep(300)
    return stu_register

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            break
            #time.sleep(300)
