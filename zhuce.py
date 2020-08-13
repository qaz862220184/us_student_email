
import asyncio
import pyppeteer
import openpyxl as xl
import os
import requests
import pyautogui
import socket
from lxml import etree
from pyppeteer import launch,launcher
import random
pyppeteer.DEBUG = True

url2 = 'https://www.opencccapply.net/gateway/apply?cccMisCode=531'


def screen_size():
    # 使用tkinter获取屏幕大小
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height


async def main():


    browser = await launch({
        #'userAgent' : ua.chrom,
        'executablePath' : pyppeteer.launcher.executablePath(),
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

            '--disable-setuid-sandbox',
            '--disable-gpu',
            #'--proxy-server={}'.format(proxy_ip)
            '--proxy-server=192.168.1.250:7890',
            #'--proxy-server=192.168.1.239:24000'
        ]
    })
    #创建一个新的隐身浏览器上下文。这不会与其他浏览器上下文共享 cookie /缓存
    await browser.createIncognitoBrowserContext()
    # page2 = await browser.newPage()
    # await page2.goto(resetIPAPI)
    # await page2.close()
    await asyncio.sleep(1)
    page = await browser.newPage()

    width, height = screen_size()
    #print(width,height)
    await page.setViewport({  # 最大化窗口
        "width": width,
        "height": 900
    })
    # await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
    #                                  '{ webdriver:{ get: () => false } }) }')


    await page.goto(url2)

    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#portal-sign-in-link')
    ])

    await page.type('#inputJUsername',username)
    await page.waitFor(500)
    await page.type('#inputJPassword','qaz2020')


    await asyncio.wait([
        page.waitForNavigation({'timeout':60000}),
        page.click('#loginPane > div > form > div:nth-child(2) > div.col-sm-2.sign-in-button-cell > button'),
        # page.hover('#loginPane > div > form > div:nth-child(2) > div.col-sm-2.sign-in-button-cell > button'),
        # page.mouse.click(page.mouse._x,page.mouse._y)
    ])
    print('强制等待')
    await page.waitFor(10000)
    print('强制等待完成')

    await page.waitForSelector('#applyForm')
    print('等待出线')


    sign = await page.querySelector('#beginApplicationButton')
    await sign.click()



    print('页面跳转成功')
    await page.waitFor(6000)
    # Enrollment
    await page.select('#inputTermId','CAP_3870')
    await page.waitFor(1000)
    await page.select('#inputEduGoal','B')
    await page.waitFor(1000)
    await page.select('#inputMajorCategory','School of Humanities Languages Fine and Performing Arts')
    await page.waitFor(1000)
    await page.select('#inputMajorId','CAP_13694')
    await page.waitFor(1000)
    await page.waitFor(5000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    #account
    await page.waitFor(3000)
    await page.click('#inputAddressSame')
    await page.waitFor(1000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    # education
    await page.waitFor(6000)
    await page.select('#inputEnrollmentStatus','1')
    await page.waitFor(1000)
    await page.select('#inputHsEduLevel','2')
    await page.waitFor(1000)
    await page.click('#inputHsAttendance3')
    await page.waitFor(1000)
    await page.waitFor(3000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    # citizenship/military
    await page.waitFor(2000)
    await page.select('#inputCitizenshipStatus','1')
    await page.waitFor(1000)
    await page.select('#inputMilitaryStatus','1')
    await page.waitFor(1000)
    await page.waitFor(3000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    # residency
    await page.waitFor(6000)
    await page.click('#inputCaRes2YearsYes')
    await page.waitFor(1000)
    await page.click('#inputIsEverInFosterCareNo')
    await page.waitFor(1000)
    await page.waitFor(5000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    # need & interests
    await page.waitFor(6000)
    await page.click('#inputEnglishYes')
    await page.waitFor(1000)
    await page.click('#inputFinAidInfoNo')
    await page.waitFor(1000)
    await page.click('#inputAssistanceNo')
    await page.waitFor(1000)
    await page.click('#inputAthleticInterest3')
    await page.waitFor(1000)

    await page.click('#inputHealthServices')
    await page.waitFor(1000)
    await page.click('#inputOnlineClasses')
    await page.waitFor(1000)
    await page.click('#inputBasicSkills')
    await page.waitFor(1000)
    await page.click('#inputStudentGov')
    await page.waitFor(1000)
    await page.waitFor(5000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    # demographic information
    await page.waitFor(6000)
    await page.select('#inputGender',user_detail['Gender'].capitalize())
    await page.waitFor(1000)
    await page.select('#inputTransgender','No')
    await page.waitFor(1000)
    await page.select('#inputOrientation','StraightHetrosexual')
    await page.waitFor(1000)
    await page.select('#inputParentGuardianEdu1','3')
    await page.waitFor(1000)
    await page.select('#inputParentGuardianEdu2', '3')
    await page.waitFor(1000)
    await page.click('#inputHispanicNo')
    await page.waitFor(1000)
    await page.click('#inputRaceEthnicity800')
    await page.waitFor(1000)
    await page.click('#inputRaceEthnicity801')
    await page.waitFor(1000)
    await page.waitFor(5000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    # supplemental questions
    await page.waitFor(6000)
    await page.waitFor(2000)
    await page.click('#YESNO_1_no')
    await page.waitFor(1000)
    await page.click('#YESNO_2_no')
    await page.waitFor(1000)
    await page.click('#YESNO_3_no')
    await page.waitFor(1000)
    await page.click('#YESNO_4_no')
    await page.waitFor(1000)
    await page.click('#YESNO_5_no')
    await page.waitFor(1000)
    await page.click('#YESNO_6_no')
    await page.waitFor(1000)
    await page.click('#YESNO_7_no')
    await page.waitFor(1000)
    await page.click('#YESNO_8_no')
    await page.waitFor(1000)
    await page.click('#_supp_CHECK_1')
    await page.waitFor(1000)
    await page.click('#_supp_CHECK_2')
    await page.waitFor(1000)
    await page.click('#_supp_CHECK_3')
    await page.waitFor(1000)
    await page.click('#_supp_CHECK_4')
    await page.waitFor(1000)
    await page.click('#YESNO_9_yes')
    #await page.click('#YESNO_10_yes')
    await page.waitFor(1000)
    await page.waitFor(5000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#applyForm > main > div.column.column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    # submission
    await page.waitFor(6000)
    await page.waitFor(2000)
    await page.click('#inputConsentYes')
    await page.waitFor(1000)
    await page.click('#inputESignature')
    await page.waitFor(1000)
    await page.click('#inputFinancialAidAck')
    await page.waitFor(1000)
    await page.waitFor(5000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#submit-application-button')
    ])

    job_page = await page.content()

    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#applyForm > main > div.column.column1 > div.ccc-page-section.buttonBox > ol > li > button')
    ])

    await page.click('#inputEnglishVerySatisfied')
    await page.waitFor(1000)
    await page.click('#RecommendYes')
    await page.waitFor(1000)
    await page.click('#applyForm > main > div.column.column1 > div.ccc-page-section.current-fieldset > button')
    await page.waitFor(2000)

    '''
    await page.evaluate('_ => {window.scrollBy(0, window.innerHeight);}')
    await page.hover('#continueBox > ol')
    x = page.mouse._x
    y = page.mouse._y
    await page.mouse.click(x,y)

    await page.waitFor(5000)
    await page.click('body > div > div > div.logoutRedirect > a')
    '''
    # await asyncio.wait([
    #     page.waitForNavigation(),
    #     page.click('body > div > div > div.logoutRedirect > a')
    # ])
    #await asyncio.sleep(101)

    #await page.click('#Pluto_6_u67l1n1100_5094775_finish-and-sign-out')
    await browser.close()



if __name__ == '__main__':
    user_detail = {'Full Name': 'Anthony\xa0E\xa0McTaggart', 'Gender': 'male', 'Title': 'Mr.', 'Race': 'White', 'Birthday': '11/20/1985', 'Social Security Number': '765-18-0619', 'Street': '885  East Avenue', 'City': 'Phoenix', 'State': 'AZ', 'State Full': 'Arizona', 'Zip Code': '85003', 'Phone Number': '480-225-9001', 'Mobile Number': '480-686-0954', 'email': '5wv0he9y@temporary-mail.net'}
    username='arXqR2xp'
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except:
        print('注册失败')
    else:
        print('注册成功')