import asyncio
import pyppeteer
import os
import requests
import json
import pyautogui
from lxml import etree
from pyppeteer import launch
import re
import socket
import random
email = 'qifcz5e6@temporary-mail.net'

'''
def screen_size():
    # 使用tkinter获取屏幕大小
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height


url = 'https://www.google.com/recaptcha/api2/demo'


def GetSessionProxy():
    super_proxy = socket.gethostbyname('zproxy.lum-superproxy.io')
    url = "http://%s-country-us-session-%s:%s@" + super_proxy + ":%d"
    port = 22225

    session_id = random.randint(0, 116225344)
    return url % ('lum-customer-hl_f5a6deb2-zone-sellerbdata', session_id, 'bcvjau85n9e9', port)

ip = GetSessionProxy()
print(ip.split('@')[-1])
'''
from fake_useragent import UserAgent
ua = UserAgent()
#ie浏览器的user agent
print(ua.chrome)
print(ua.chrome)
print(ua.chrome)



'''
# 保存cookie
async def save_cookie(cookie):
    with open("cookie.json", 'w+', encoding="utf-8") as file:
        json.dump(cookie, file, ensure_ascii=False)


async def load_cookie():
    with open("cookie.json", 'r', encoding="utf-8") as file:
        cookie = json.load(file)
    return cookie

async def get_edu():

    browser = await launch({
        'executablePath': pyppeteer.launcher.executablePath(),
        'headless': False,
        'dumpio': True,
        'autoClose': False,
        'args': [
            '--no-sandbox',
            "--start-maximized",
            '--disable-infobars',
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--enable-automation',
            #'--proxy-server={}'.format(proxy_ip)
            #'--proxy-server=192.168.1.250:7890',
            '--proxy-server=192.168.1.239:24004'
        ]
    })
    page = await browser.newPage()
    width, height = screen_size()
    # print(width,height)
    await page.setViewport({  # 最大化窗口
        "width": width,
        "height": 900
    })
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                     '{ webdriver:{ get: () => false } }) }')



    # 获取email地址
    await page.goto(url)
    #63 452     167 713
    pyautogui.click(63,452)
    await page.waitFor(2000)
    pyautogui.click(167,713)

    try:
        frame = page.frames
        for f in frame:
            title = await f.title()
            if title == 'reCAPTCHA':
                cookies2 = await page.cookies()
                await save_cookie(cookies2)




                link = await f.Jeval('#audio-source', 'el => el.src')
                print(link)
    except:
        pass


asyncio.get_event_loop().run_until_complete(get_edu())
'''