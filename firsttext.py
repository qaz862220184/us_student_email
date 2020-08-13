
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
#launcher.DEFAULT_ARGS.remove("--enable-automation")
pyppeteer.DEBUG = True


def screen_size():
    # 使用tkinter获取屏幕大小
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height


url1 = 'https://www.fakeaddressgenerator.com/'
url2 = 'https://www.opencccapply.net/gateway/apply?cccMisCode=531'
# 前期注册完成，未跳转成功则使用该url
#url3 = 'https://idp.openccc.net/idp/profile/SAML2/Unsolicited/SSO?execution=e2s1'
resetIPAPI = "http://192.168.1.239:22999/api/refresh_sessions/24000"

def GetSessionProxy():
    super_proxy = socket.gethostbyname('zproxy.lum-superproxy.io')
    url = "http://%s-country-us-session-%s:%s@" + super_proxy + ":%d"
    port = 22225

    session_id = random.randint(0, 116225344)
    return url % ('lum-customer-hl_f5a6deb2-zone-sellerbdata', session_id, 'bcvjau85n9e9', port)

from fake_useragent import UserAgent
ua =UserAgent()

async def get_user_detail():

    browser = await launch({
        'userAgent': ua.chrome,
        'executablePath': pyppeteer.launcher.executablePath(),
        #'headless': False,
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
            #'--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            #'--proxy-server={}'.format(proxy_ip)
            #'--proxy-server=192.168.1.250:7890',
            '--proxy-server=192.168.1.239:24000'
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
    await page.goto(url1)
    await page.waitFor(5000)
    contents = await page.content()
    tree = etree.HTML(contents)
    tr_list = tree.xpath('/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/div[2]/table/tbody/tr')

    for tr in tr_list:
        a = tr.xpath('.//td[1]//text()')
        a = a[0]
        b = tr.xpath('.//td[2]//text()')
        b = b[0]
        user_detail.update({a: b})

    div_list = tree.xpath('//*[@class="row item"]')
    for i in range(7):
        a = div_list[i].xpath('.//div[1]//text()')
        a = a[0]
        b = div_list[i].xpath('.//div[2]//input/@value')[0]
        user_detail.update({a: b})

    # 获取email地址
    await page.waitFor(5000)
    page1 = await browser.newPage()
    await page1.setViewport({  # 最大化窗口
        "width": width,
        "height": 900
    })
    await page1.goto('https://www.temporary-mail.net/')
    await page1.waitFor(10000)
    email = await page1.Jeval('#active-mail','el => el.value')
    user_detail.update({'email':email})

    await browser.close()


async def main():

    #username = 'automation2'
    psd = 'qaz2020'
    PIN = '9210'
    #print("in main ")
    #print(os.environ.get('PYPPETEER_CHROMIUM_REVISION'))
    # 浏览器打开失败

    browser = await launch({
        #'userAgent' : ua.chrom,
        'executablePath' : pyppeteer.launcher.executablePath(),
        'headless': False,
        'dumpio': True,
        'autoClose': True,
        'args': [
            '--no-sandbox',
            "--start-maximized",
            '--disable-infobars',
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            #'--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            #'--proxy-server={}'.format(proxy_ip)

            #'--proxy-server=59.38.222.151:3128',
            '--proxy-server=192.168.1.250:7890',
            #'--proxy-server=175.6.66.48:3128'
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

    # await asyncio.wait([
    #     page.waitForNavigation({'timeout': 1000*60}),
    #     page.goto(url2)
    # ])
    # await page.goto(resetIPAPI)
    # await page.close()
    await page.goto(url2)
    #await page.waitForNavigation()

    #await page.evaluateOnNewDocument(' Object.defineProperties(navigator,"webdriver",{ get: () => undefined } ) ')


    await asyncio.wait([
        page.waitForNavigation({'timeout': 1000*200}),
        page.click('#portletContent_u16l1n18 > div > div.ccc-page-section > div > a:nth-child(2)'),
    ])

    # await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
    #                                  '{ webdriver:{ get: () => false } }) }')

    await asyncio.wait([
        page.waitForNavigation({'timeout': 1000*200}),
        page.click('#accountFormSubmit'),
    ])

    # await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
    #                                  '{ webdriver:{ get: () => false } }) }')

    # Legal Name
    await page.type('#inputFirstName',first_name)
    await page.waitFor(1000)
    await page.type('#inputMiddleName', middle_name)
    await page.waitFor(1000)
    await page.type('#inputLastName', last_name)
    await page.waitFor(1000)
    await page.click('#hasOtherNameNo')
    await page.waitFor(1000)
    await page.click('#hasPreferredNameNo')
    # Date of Birth
    await page.select('#inputBirthDateMonth',month)
    await page.waitFor(1000)
    await page.select('#inputBirthDateDay',day)
    await page.waitFor(1000)
    await page.type('#inputBirthDateYear',year)
    await page.waitFor(1000)
    await page.select('#inputBirthDateMonthConfirm',month)
    await page.waitFor(1000)
    await page.select('#inputBirthDateDayConfirm',day)
    await page.waitFor(1000)
    await page.type('#inputBirthDateYearConfirm',year)
    await page.waitFor(1000)
    #Social Security Number
    await page.click('#-have-ssn-yes')
    await page.waitFor(2000)
    await page.type('#-ssn-input1',SSN)
    await page.waitFor(1000)
    await page.type('#-ssn-input2',SSN)
    await page.waitFor(1000)

    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#accountFormSubmit'),
    ])
    # await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
    #                                  '{ webdriver:{ get: () => false } }) }')

    # Email
    await page.type('#inputEmail',user_detail['email'])
    await page.waitFor(1000)
    await page.type('#inputEmailConfirm',user_detail['email'])
    await page.waitFor(1000)
    # Telephone
    await page.type('#inputSmsPhone',user_detail['Phone Number'])
    await page.waitFor(1000)
    # Permanent Address
    await page.type('#inputStreetAddress1',user_detail['Street'])
    await page.waitFor(1000)
    await page.type('#inputStreetAddress2',user_detail['Street'])
    await page.waitFor(1000)
    await page.type('#inputCity',user_detail['City'])
    await page.waitFor(1000)
    await page.select('#inputState',user_detail['State'])
    await page.waitFor(1000)
    await page.type('#inputPostalCode',user_detail['Zip Code'])
    await page.waitFor(1000)
    # 提交报错
    await page.click('#accountFormSubmit'),
    await page.waitFor(5000)
    await page.click('#messageFooterLabel'),
    await page.waitFor(2000)
    await page.click('#inputAddressValidationOverride'),
    await page.waitFor(2000)

    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#accountFormSubmit'),
    ])
    # await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
    #                                  '{ webdriver:{ get: () => false } }) }')

    # Username and Password
    await page.type('#inputUserId',username)
    await page.waitFor(1000)
    await page.type('#inputPasswd',psd)
    await page.waitFor(1000)
    await page.type('#inputPasswdConfirm',psd)
    await page.waitFor(1000)
    # Security PIN
    await page.type('#inputPin',PIN)
    await page.waitFor(1000)
    await page.type('#inputPinConfirm',PIN)
    await page.waitFor(1000)
    # Security Questions
    await page.select('#inputSecurityQuestion1','1')
    await page.waitFor(1000)
    await page.type('#inputSecurityAnswer1','first')
    await page.waitFor(1000)
    await page.select('#inputSecurityQuestion2', '2')
    await page.waitFor(1000)
    await page.type('#inputSecurityAnswer2', 'second')
    await page.waitFor(1000)
    await page.select('#inputSecurityQuestion3', '3')
    await page.waitFor(1000)
    await page.type('#inputSecurityAnswer3', 'thirdly')
    await page.waitFor(1000)


    await page.mouse.click(478,754)
    print('点击人机验证')
    await page.waitFor(2000)

    await page.mouse.move(550,880)
    await page.mouse.click(576,877)

    print('点击音频验证')
    await page.waitFor(5000)


    try:
        frame =  page.frames
        for f in frame:
            title = await f.title()
            if title == 'reCAPTCHA':

                link = await f.Jeval('#audio-source','el => el.src')
                print(link)
                # 跳转到链接网站进行下载
                await page._client.send('Page.setDownloadBehavior',{
                    'behavior': 'allow',
                    'downloadPath':'./'
                })
                download_dir = r'C:\Users\Win\Downloads'
                path_text = r'C:\Users\Win\Downloads\payload.mp3'
                path_text1 = r'./payload.mp'
                if os.path.exists(path_text):
                    os.remove(path_text)
                    print('已删除')
                page1 = await browser.newPage()
                width, height = screen_size()
                await page.setViewport({  # 最大化窗口
                    "width": width,
                    "height": height
                })
                await page1.goto(link)
                await page1.waitFor(1000)


                await page1.hover('body > video ')
                start_x = page1.mouse._x
                start_y = page1.mouse._y
                print(start_x,start_y)
                await page1.mouse.click(start_x+125,start_y+55,{'delay':50})
                print('dianji420')
                await page1.waitFor(1000)
                await page1.mouse.click(start_x+125,start_y+55,{'delay':50})
                print('dianji430')
                await page1.keyboard.press('Enter')


                await page1.waitFor(3000)
                await page1.close()
                # response = requests.get(link)
                # print(response)
                # text = run.runCap()
                # print(text)
                import iat_ws_python3
                data = iat_ws_python3.data_text
                print(data)
                await page.waitFor(5000)
                await f.type('#audio-response',data)
                await page.waitFor(1000)
                await f.click('#recaptcha-verify-button')

    except BaseException:
        print("人机验证失败，请重试")
        await browser.close()

    # 现在前期页面注册已完成
    #print('前期注册已完成,接下来进行信息注册')
    await page.waitFor(2000)
    #await page.click('#accountFormSubmit')
    await asyncio.wait([
        page.waitForNavigation({'timeout': 1000*200}),
        page.click('#accountFormSubmit'),
    ])
    print('现在是可以看见CCCID的页面')
    # 将下面部分流程拆分出来
    global CCCID
    CCCID = await page.querySelector('#registrationSuccess > main > div.column > div > div > div > p:nth-child(1) > strong')
    print(CCCID)

    Tag = True
    try:
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000*600}),
            page.click('#registrationSuccess > main > div.column > div > div > button')
        ])

        # 强制等待10s，以防止页面未刷新出来
        await page.waitFor(20000)
    except:
        print('页面跳转失败')
        await page.close()
        Tag = False
    finally:
        print(Tag)



    print('页面跳转')


    await page.waitFor(10000)
    # Enrollment
    await page.select('#inputTermId','CAP_3870')
    await page.waitFor(1000)
    await page.select('#inputEduGoal','B')
    await page.waitFor(1000)
    await page.select('#inputMajorCategory','School of Humanities Languages Fine and Performing Arts')
    await page.waitFor(1000)
    await page.select('#inputMajorId','CAP_13694')
    await page.waitFor(1000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    #account
    await page.waitFor(6000)
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
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    # citizenship/military
    await page.waitFor(6000)

    await page.select('#inputCitizenshipStatus','1')
    await page.waitFor(1000)
    await page.select('#inputMilitaryStatus','1')
    await page.waitFor(1000)
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

    # await page.evaluate('_ => {window.scrollBy(0, window.innerHeight);}')
    # await page.hover('#continueBox > ol')
    # x = page.mouse._x
    # y = page.mouse._y
    # await page.mouse.click(x,y)

    commit = await page.querySelector('#continueBox > ol')
    print(commit)
    await commit.click()

    await page.click('body > div > div > div.logoutRedirect > a')

    await asyncio.sleep(10)
    #await page.click('#Pluto_6_u67l1n1100_5094775_finish-and-sign-out')
    await browser.close()



def write_excel_file(folder_path):
    result_path = os.path.join(folder_path, "edu_zhuce.xlsx")
    print(result_path)
    print('***** 开始写入excel文件 ' + result_path + ' ***** \n')
    if os.path.exists(result_path):
        print('***** excel已存在，在表后添加数据 ' + result_path + ' ***** \n')
        workbook = xl.load_workbook(result_path)
        sheet = workbook.active
        for key in user_detail:
            detail.append(user_detail[key])
        sheet.append(detail)
        workbook.save(result_path)
    else:
        print('***** excel不存在，创建excel ' + result_path + ' ***** \n')
        workbook = xl.Workbook()
        workbook.save(result_path)

        sheet = workbook.active
        for item in user_detail:
            headers.append(item)
        sheet.append(headers)
        for key in user_detail:
            detail.append(user_detail[key])

        sheet.append(detail)
        workbook.save(result_path)
    print('***** 生成Excel文件 ' + result_path + ' ***** \n')

# loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(main())
# loop.run_until_complete(task)

async def regist():
    browser = await launch({
        # 'userAgent' : ua.chrom,
        'executablePath': pyppeteer.launcher.executablePath(),
        #'headless': False,
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
            # '--proxy-server={}'.format(proxy_ip)
            '--proxy-server=192.168.1.250:7890',
            # '--proxy-server=192.168.1.239:24000'
        ]
    })
    # 创建一个新的隐身浏览器上下文。这不会与其他浏览器上下文共享 cookie /缓存
    await browser.createIncognitoBrowserContext()
    # page2 = await browser.newPage()
    # await page2.goto(resetIPAPI)
    # await page2.close()
    await asyncio.sleep(1)
    page = await browser.newPage()

    width, height = screen_size()
    # print(width,height)
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

    await page.type('#inputJUsername', username)
    await page.waitFor(500)
    await page.type('#inputJPassword', 'qaz2020')

    await asyncio.wait([
        page.waitForNavigation({'timeout': 60000}),
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
    await page.select('#inputTermId', 'CAP_3870')
    await page.waitFor(1000)
    await page.select('#inputEduGoal', 'B')
    await page.waitFor(1000)
    await page.select('#inputMajorCategory', 'School of Humanities Languages Fine and Performing Arts')
    await page.waitFor(1000)
    await page.select('#inputMajorId', 'CAP_13694')
    await page.waitFor(1000)
    await page.waitFor(5000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    # account
    await page.waitFor(3000)
    await page.click('#inputAddressSame')
    await page.waitFor(1000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
    ])

    # education
    await page.waitFor(6000)
    await page.select('#inputEnrollmentStatus', '1')
    await page.waitFor(1000)
    await page.select('#inputHsEduLevel', '2')
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
    await page.select('#inputCitizenshipStatus', '1')
    await page.waitFor(1000)
    await page.select('#inputMilitaryStatus', '1')
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
    await page.select('#inputGender', user_detail['Gender'].capitalize())
    await page.waitFor(1000)
    await page.select('#inputTransgender', 'No')
    await page.waitFor(1000)
    await page.select('#inputOrientation', 'StraightHetrosexual')
    await page.waitFor(1000)
    await page.select('#inputParentGuardianEdu1', '3')
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
    # await page.click('#YESNO_10_yes')
    await page.waitFor(1000)
    await page.waitFor(5000)
    await asyncio.wait([
        page.waitForNavigation(),
        page.click(
            '#applyForm > main > div.column.column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
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
    # await asyncio.sleep(101)

    # await page.click('#Pluto_6_u67l1n1100_5094775_finish-and-sign-out')
    await browser.close()


if __name__ == '__main__':
    #proxy_ip = GetSessionProxy().split('@')[-1]
    detail = []
    headers = []
    user_detail = {}
    CCCID = ''
    username = ''.join(random.sample("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 8))
    user_detail.update({'username': username})
    #proxy_ip = get_url()
    #asyncio.get_event_loop().run_until_complete(last_regist())
    try:
        asyncio.get_event_loop().run_until_complete(get_user_detail())
    except:
        print("获取用户信息失败")
        #continue

    print(user_detail)
    name = user_detail['Full Name']
    first_name = name.split(' ')[0]
    middle_name = name.split(' ')[1]
    last_name = name.split(' ')[2]

    Birthday = user_detail['Birthday']
    month = Birthday.split('/')[0]
    day = Birthday.split('/')[1]
    year = Birthday.split('/')[2]

    SSN = user_detail['Social Security Number'].replace('-', '')

    try:
        asyncio.get_event_loop().run_until_complete(main())
        write_excel_file("./")
    except Exception:
        print('执行失败，请重试')
        try:
            if CCCID == '':
                print('申请未完成')
            else:
                asyncio.get_event_loop().run_until_complete(regist())
                write_excel_file('./')
        except:
            print('注册失败')
        #continue






