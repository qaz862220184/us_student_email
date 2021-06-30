#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import requests




def get_email():
    get_email_api = '*********************'
    response = requests.get(get_email_api)
    ret = response.json()
    #print(ret)
    email = ret['data'].get('email')
    email_password = ret['data'].get('email_psw')
    email_server = ret['data'].get('mail_server')
    #print(email,email_password,email_server)
    return email,email_password,email_server

#get_email()

def get_email_msg(email,email_password,email_server):
    get_email_msg_api = '***********'
    data = {
    "email":email,
    "email_psw":email_password,
    "mail_server":email_server,
    "mail_port":110,
    "mail_ssl":False,
    "email_num":"1",
    "mail_service":"pop3",
    "email_port":110
    }
    response = requests.post(get_email_msg_api, json=data)
    ret = response.json()
    #print(ret['data'])
    return ret['data'][0]

if __name__ == '__main__':

    get_email_msg('3ec7f83ba1@ppvpnplus.com','3590a266cd','pop.ppvpnplus.com')
