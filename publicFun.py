#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
import pymysql
import time
import random
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler('log.txt',encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def screen_size():
    width = 1920
    height = 1080
    return width, height

def connect_db():
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='student_email', charset='utf8')
    return connection

def add_user_detail(data):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "insert into user_detail_our_email(userName,fullName,gender,title,race,birthday," \
          "ssn,street,city,state,stateFull,zipCode,phoneNumber,mobileNumber,email,email_pwd,email_server,register_time) " \
          "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    result = cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()

def update_user_tag(email,tag):
    conn = connect_db()
    cursor = conn.cursor()
    register_time = time.strftime("%Y-%m-%d %X", time.localtime())
    sql = "UPDATE user_detail_our_email set tag=" + str(tag) + " where email='" + email + "'"
    result = cursor.execute(sql)
    conn.commit()
    conn.commit()
    cursor.close()
    conn.close()
    return result

def show_user_detail_page(page=0,total=20):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT fullName,email,register_time,tag FROM user_detail_our_email where tag<=2 order by register_time desc limit %s,%s" % (page * total, total)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_user_detail(tag):
    sql = 'SELECT * FROM user_detail_our_email WHERE tag=%s order by register_time' % tag
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    key_list = ['userName', 'fullName', 'gender', 'title', 'race', 'birthday', 'ssn', 'street', 'city',
                'state', 'stateFull', 'zipCode', 'phoneNumber', 'mobileNumber', 'email', 'email_pwd', 'email_server', 'tag']
    data = list(data)
    data = dict(zip(key_list, data))
    return data

def delete_user_detail_fail():
    conn = connect_db()
    cursor = conn.cursor()
    sql = "delete from user_detail_our_email where tag=3"
    result = cursor.execute(sql)
    print(result)
    conn.commit()
    cursor.close()
    conn.close()

def delete_user_detail_succeed(email):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "delete from user_detail_our_email  where email='" + email + "'"
    result = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def add_email_detail(data):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "insert into email_detail(stu_id,edu_email,edu_pwd,collect_time,college_id) values(%s,%s,%s,%s,%s)"
    result = cursor.execute(sql,data)
    if result:
        print("添加成功")
    else:
        print("添加失败")
    conn.commit()
    conn.commit()
    cursor.close()
    conn.close()

def show_email_detail():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_detail_our_email where tag=0 limit 20")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_email_detail_time(start,end):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_detail_our_email where collect_time>'"+ start +"' and collect_time<'"+ end +"' limit 20")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_email_detail_page(page=0,total=20):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM user_detail_our_email limit %s,%s" %(page * total,total)
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_email_detail_parameter(start_time='0000-00-00 00:00:00',end_time='2100-00-00 00:00:00',page=0,total=20):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM user_detail_our_email where collect_time>'"+ start_time +"' and collect_time<'"+ end_time + "' order by collect_time desc limit %s,%s" % (page * total, total)
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update_user_tag_time(email,tag):
    conn = connect_db()
    cursor = conn.cursor()
    register_time = time.strftime("%Y-%m-%d %X", time.localtime())
    print(register_time)
    sql = "UPDATE user_detail_our_email set register_time='"+ register_time +"',tag=" + str(tag) + " where email='" + email + "'"
    result = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return result



if __name__ == '__main__':
    # email = 'cjaferalhaz@guidelia.site'
    # a = update_user_tag_time(email,8)
    # print(a)
    data = ['2SEDP4Oi3V5MY', 'David\xa0C\xa0Burns', 'male', 'Mr.', 'White', '4/3/1980', '558-72-3492', '1107  Pearl Street', 'Sacramento', 'CA', 'California', '95827', '916-364-4588', '916-465-4515', '80421f53b8@ggmask.com', 'ccd2ee9fe4', 'pop.ggmask.com', '2021-06-30 14:59:54']
    add_user_detail(data)


    # a = show_email_detail_time('2020-09-29 00:00:00','2020-09-30 00:00:01')
    # for i in a:
    #     i = list(i)
    #     print(i[4],type(i[4]))
    #     k = str(i[4])
    #     print(k,type(k))
    # data = show_user_detail()
    # for a in data:
    #     data1 = list(a)
    #     print(data1)
    # data = get_user_detail(0)
    # print(data)
    # stu_id = '0560357'
    # edu_email = 'rubie.padilla@campus.mccd.edu'
    # edu_pwd = '051958'
    # add_email_detail([stu_id,edu_email,edu_pwd])
