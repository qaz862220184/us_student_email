import asyncio
import pyppeteer
import os, time
import traceback
from pyppeteer import launch
import publicFun
import fake_useragent

pyppeteer.DEBUG = True


class Browser(object):
    def __init__(self, apply_detail):
        self.apply_detail = apply_detail

    async def newbrowser(self):
        ip_pool = ['127.0.0.1:30010', '127.0.0.1:30011', '127.0.0.1:30012', '127.0.0.1:30013', '127.0.0.1:30014', ]
        a = ['127.0.0.1:30015', '127.0.0.1:30016', '127.0.0.1:30017'
            , '127.0.0.1:30018', '127.0.0.1:30019', ]
        try:
            self.browser = await launch({
                # 'executablePath': "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                'executablePath': pyppeteer.launcher.executablePath(),
                # 'headless': False,
                'dumpio': True,
                # 'slowMo': 500,
                'args': [
                    '--no-sandbox',
                    "--start-maximized",
                    '--disable-infobars',
                    '--disable-extensions',
                    '--disable-web-security',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--lang=en-US',
                    # '--proxy-server=192.168.1.250:7890'
                    # '--proxy-server={}'.format(proxy_ip)
                    # '--proxy-server={}'.format(random.choice(ip_pool))
                ]
            }, userDataDir='./register/%s' % apply_detail['email'],
            )
        except:
            await self.browser.close()

    async def parameter(self, page):
        # 直接删除webdrive
        await page.evaluateOnNewDocument("""() => {
            delete navigator.__proto__.webdriver;
            }""")
        # 设置ua
        ua = fake_useragent.UserAgent()
        useragent = ua.chrome
        await page.setUserAgent(useragent)
        # await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36')
        # 设置permissions通知
        await page.evaluateOnNewDocument("""() => {
            Object.defineProperty(Notification, 'permission', { get: () => 'default' })
        }""")

        # 设置插件

        # chrome检测
        await page.evaluateOnNewDocument("""() => {window.chrome = {
                app: {},
                csi: function() {},
                loadTimes: function() {},
                runtime: {},
              }
        }""")
        # 设置canvas指纹
        await page.evaluateOnNewDocument('''value => {
            function jsCode(value) {
                String.prototype.hashCode = function() {
                  var hash = 0, i, chr
                  if (this.length === 0) return hash
                  for (i = 0; i < this.length; i++) {
                    chr   = this.charCodeAt(i)
                    hash  = ((hash << 5) - hash) + chr
                    hash |= 0
                  }
                  return hash
                }
                function canvasReset(value){
                  CanvasRenderingContext2D.prototype.getImageData = function(a) {
                  return function() {
                    spoofFromContext(this, a)
                    return a.apply(this, arguments)
                  }
                  }(CanvasRenderingContext2D.prototype.getImageData)
                  HTMLCanvasElement.prototype.toDataURL = (function() {
                    var original = HTMLCanvasElement.prototype.toDataURL
                    return function() {
                      spoof(this)
                      return original.apply(this, arguments)
                    }
                  })()
                  function spoof(canvas){
                    var ctx = canvas.getContext("2d")
                    spoofFromContext(ctx)
                  }
                  function spoofFromContext(ctx, a){
                    if(!a) a = ctx.getImageData
                    let data = a.call(ctx, 0, 0, ctx.canvas.width, ctx.canvas.height)
                    console.log(value)
                    let dataValue = JSON.stringify(Math.abs(value.hashCode()))
                    data.data = data.data.forEach((value, index)=>{ data.data[index] = 0 })
                    for(var c = 0; c < dataValue.length; c++) {
                      if(a != 0){
                        data.data[c] = dataValue[c]
                      }
                    }
                    ctx.putImageData(data, 0, 0)
                  } 
                }
                canvasReset(value)

                function bin2hex(s) {
                  var i, l, o = '', n
                  s += ''
                  for (i = 0, l = s.length; i < l; i++) {
                    n = s.charCodeAt(i)
                      .toString(16)
                    o += n.length < 2 ? '0' + n : n
                  }
                  return o
                }
                function getUUID(domain) {
                  var canvas = document.createElement('canvas')
                  var b64 = canvas.toDataURL().replace("data:image/png;base64,","")
                  var bin = atob(b64)
                  var crc = bin2hex(bin.slice(-16,-12))
                  return crc
                }
                let canvasFingerprint = getUUID()
                console.log(canvasFingerprint)}
                jsCode(value)
                }''', 'username')
        # 设置时区
        await page.evaluateOnNewDocument("""() => {
            let timeindex =  new Date().getTimezoneOffset() / -60
                Date.prototype.toGMTString = function(Da) {
                  var z = new Da().toGMTString
                  return function() {
                    let time = (360 / 60) + timeindex
                    return z.apply(new Date(new Date(this).getTime() + (3600000 * time)), arguments)
                  } 
                }(Date)
                Date.prototype.toUTCString = function() {
                  var x = Date.prototype.toUTCString
                    return function() {
                      let time = (360 / 60) + timeindex
                      return x.apply(new Date(new Date(this).getTime() + (3600000 * time)), arguments)
                  } 
                }()
                Date.prototype.getTimezoneOffset = function() {
                  var b = Date.prototype.getTimezoneOffset
                    return function() {
                      return 360
                  } 
                }()
                Intl.DateTimeFormat.prototype.resolvedOptions = function() {
                  var germanFakeRegion = new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York' }).resolvedOptions()
                  return function() {
                    return germanFakeRegion
                  } 
                }()
            }""")
        # 设置语言
        language = 'en-US'
        languages = ['en-US', 'en;q=0.9']
        await page.evaluateOnNewDocument('''data =>{ 
                                    Object.defineProperty(navigator, 'language', { get: () => data }); 
                                }''', language)
        await page.evaluateOnNewDocument('''data =>{ 
                                                Object.defineProperty(navigator, 'languages', { get: () => data }); 
                                            }''', languages)
        # 设置显卡型号
        graphicscard = 'ANGLE (Intel(R) HD Graphics 5300 Direct3D11 vs_5_0 ps_5_0)'
        await page.evaluateOnNewDocument('''data => {WebGLRenderingContext.prototype.getParameter = function() {
                          var b = WebGLRenderingContext.prototype.getParameter
                          return function() {
                            if (arguments[0] == 37446) {
                              return data 
                            } 
                            return b.apply(this, arguments)
                          } 
                        }()}''', graphicscard)

        # 设置分辨率
        width = '1920'
        height = '1080'
        await page.evaluateOnNewDocument('''height => {Object.defineProperty(window.screen, 'height', {
                            value: height,
                            writable: true,
                            configurable: true,
                            enumerable: true,
                          })}''', height)

        await page.evaluateOnNewDocument('''width => {Object.defineProperty(window.screen, 'width', {
                                value: width,
                                writable: true,
                                configurable: true,
                                enumerable: true,
                              })}''', width)

        await page.evaluateOnNewDocument('''height => {Object.defineProperty(window.screen, 'availHeight', {
                                value: height,
                                writable: true,
                                configurable: true,
                                enumerable: true,
                              })}''', height)

        await page.evaluateOnNewDocument('''width => {Object.defineProperty(window.screen, 'availWidth', {
                                    value: width,
                                    writable: true,
                                    configurable: true,
                                    enumerable: true,
                                  })}''', width)

    async def regist(self, apply_detail, browser):
        url = 'https://www.opencccapply.net/gateway/apply?cccMisCode=531'

        page = await browser.newPage()
        width, height = publicFun.screen_size()
        await page.setViewport({  # 最大化窗口
            "width": width,
            "height": 1040
        })
        await self.parameter(page)

        await page.goto(url)
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click('#portal-sign-in-link')
        ])

        await page.type('#inputJUsername', apply_detail['userName'])
        await page.waitFor(500)
        await page.type('#inputJPassword', 'qaz2020')
        await asyncio.wait([
            page.waitForNavigation({'timeout': 60000}),
            page.click('#loginPane > div > form > div:nth-child(2) > div.col-sm-2.sign-in-button-cell > button'),
        ])
        await page.waitFor(10000)
        await page.waitForSelector('#applyForm')

        sign = await page.querySelector('#beginApplicationButton')
        await sign.click()
        print('页面跳转成功')
        await page.waitFor(10000)
        # Enrollment
        print('Enrollment')
        await page.select('#inputTermId', 'CAP_3872')
        await page.waitFor(1000)
        await page.select('#inputEduGoal', 'B')
        await page.waitFor(1000)
        await page.select('#inputMajorCategory', 'School of Business')
        await page.waitFor(1000)
        await page.select('#inputMajorId', 'CAP_13607')
        await page.waitFor(1000)
        await page.waitFor(5000)
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
        ])
        # await page.waitFor(9999999)
        # account
        await page.waitFor(3000)
        print('account')
        await page.waitFor(3000)
        await page.click('#inputAddressSame')
        await page.waitFor(1000)
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
        ])
        # education
        print('education')
        await page.waitFor(10000)
        await page.select('#inputEnrollmentStatus', '1')
        await page.waitFor(1000)
        await page.select('#inputHsEduLevel', '2')
        await page.waitFor(1000)
        await page.select('#inputHsAttendance', '3')
        await page.waitFor(1000)
        await page.waitFor(3000)
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
        ])
        # citizenship/military
        print('citizenship')
        await page.waitFor(2000)
        await page.select('#inputCitizenshipStatus', '1')
        await page.waitFor(1000)
        await page.select('#inputMilitaryStatus', '1')
        await page.waitFor(1000)
        await page.waitFor(3000)
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
        ])
        # residency
        print('residency')
        await page.waitFor(10000)
        await page.click('#inputCaRes2YearsYes')
        await page.waitFor(1000)
        if await page.querySelector('#inputHomelessYouthNo'):
            await page.click('#inputHomelessYouthNo')
            await page.waitFor(1000)
        await page.click('#inputIsEverInFosterCareNo')
        await page.waitFor(1000)
        await page.click('#inputIsEverInFosterCareNo')
        await page.waitFor(5000)
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
        ])
        # need & interests
        print('need')
        await page.waitFor(10000)
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
        await page.click('#inputEOPS')
        await page.waitFor(1000)
        await page.click('#inputCalWorks')
        await page.waitFor(1000)
        await page.click('#inputScholarshipInfo')
        await page.waitFor(1000)
        await page.waitFor(5000)
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
        ])
        # demographic information
        print('demographic')
        await page.waitFor(10000)
        await page.select('#inputGender', apply_detail['gender'].capitalize())
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
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click('#column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
        ])
        # supplemental questions
        print('supplemental')
        await page.waitFor(10000)
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
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click(
                '#applyForm > main > div.column.column2 > div.buttonBox.ccc-page-section > ol > li.save-continue > button')
        ])
        # submission
        print('submission')
        await page.waitFor(10000)
        await page.waitFor(2000)
        await page.click('#inputConsentYes')
        await page.waitFor(1000)
        await page.click('#inputESignature')
        await page.waitFor(1000)
        await page.click('#inputFinancialAidAck')
        await page.waitFor(1000)
        await page.waitFor(5000)
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click('#submit-application-button')
        ])
        await page.waitFor(3000)
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click('#applyForm > main > div.column.column1 > div.ccc-page-section.buttonBox > ol > li > button')
        ])
        await page.waitFor(5000)
        await page.click('#inputEnglishVerySatisfied')
        await page.waitFor(1000)
        await page.click('#RecommendYes')
        await page.waitFor(1000)
        await page.click('#applyForm > main > div.column.column1 > div.ccc-page-section.current-fieldset > button')
        await page.waitFor(2000)
        await browser.close()
        # return pid

    async def do(self):
        await self.newbrowser()
        try:
            await self.regist(self.apply_detail, self.browser)
            return True
        except:
            await self.browser.close()
            return False


if __name__ == '__main__':
    pid = ''
    while True:
        try:
            apply_detail = publicFun.get_user_detail(1)
        except:
            time.sleep(300)
            continue
        if apply_detail:
            try:
                flag = asyncio.get_event_loop().run_until_complete(Browser(apply_detail).do())
                if flag:
                    publicFun.update_user_tag_time(apply_detail['email'], 2)
                    publicFun.logger.info('%s 申请成功' % apply_detail['email'])
                else:
                    publicFun.update_user_tag_time(apply_detail['email'], 4)
            except Exception as e:
                traceback.print_exc()
                publicFun.update_user_tag_time(apply_detail['email'], 4)
                publicFun.logger.info('%s,%s' % (apply_detail['email'], e))
            finally:
                # os.system('taskkill /pid' + str(pid) + '-t -f')
                time.sleep(30)
        else:
            time.sleep(300)
