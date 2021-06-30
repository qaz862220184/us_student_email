# -*- encoding=utf8 -*-
import asyncio
import pyppeteer
import os
import time
import subprocess
import iat_ws_python3 as iat3
from pyppeteer import launch
import shutil
import fake_useragent
import publicFun
import traceback

pyppeteer.DEBUG = True
psd = 'qaz2020'
PIN = '9210'


class Browser(object):

    def __init__(self, user_detail):
        self.user_detail = user_detail

    async def newbrowser(self):
        ip_pool = ['127.0.0.1:30010', '127.0.0.1:30011', '127.0.0.1:30012', '127.0.0.1:30013', '127.0.0.1:30014', ]
        a = ['127.0.0.1:30015', '127.0.0.1:30016', '127.0.0.1:30017'
            , '127.0.0.1:30018', '127.0.0.1:30019', ]
        proxy_ip = 'cellular-us:ny12356~@luminati-us.com:12903'
        try:
            self.browser = await launch({
                # 'userAgent' : fake_useragent.UserAgent,
                'executablePath': pyppeteer.launcher.executablePath(),
                # 'executablePath': "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                # 'headless': False,
                'dumpio': True,
                'autoClose': True,
                # 'slowMo':100,
                'handleSIGTERM': True,
                'handleSIGHUP': True,
                'args': [
                    '--no-sandbox',
                    "--start-maximized",
                    '--disable-infobars',
                    '--disable-extensions',
                    '--disable-web-security',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--lang=en-US',
                    # '--proxy-server=socks5://{}'.format(proxy_ip)
                    # '--proxy-server={}'.format(proxy)
                    # '--proxy-server=192.168.1.250:7890'
                    # '--proxy-server=127.0.0.1:30019'
                    # '--proxy-server=socks5://amazon:1q2w33e4r@192.3.172.119:1080'
                    # '--proxy-server={}'.format(random.choice(ip_pool))
                    # '--proxy-server=192.168.1.250:7890'
                ]
            }, userDataDir='./apply/%s' % user_detail['email'],
                ignoreDefaultArgs=['--enable-automation'],
            )
        except:
            traceback.print_exc()
            print('浏览器打开失败', time.localtime())
            await self.browser.close()

    async def parameter(self, page):
        # 直接删除webdrive
        await page.evaluateOnNewDocument("""() => {
            delete navigator.__proto__.webdriver;
            }""")
        # await page.evaluateOnNewDocument("""() => {
        #             Object.defineProperty(navigator, webdriver, { get: () => false })
        #         }""")
        # 设置ua
        ua = fake_useragent.UserAgent()
        useragent = ua.chrome
        await page.setUserAgent(useragent)
        # await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36')
        # 设置permissions通知 (无关,成功了1次)
        await page.evaluateOnNewDocument("""() => {
            Object.defineProperty(Notification, 'permission', { get: () => 'default' })
        }""")

        # 设置插件(有影响)
        await page.evaluateOnNewDocument("""() => {
                Object.defineProperty(navigator, 'plugins', {
                  get: function() {
                    return [
                {
                    0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format", enabledPlugin: Plugin},
                    description: "Portable Document Format",
                    filename: "internal-pdf-viewer",
                    length: 1,
                    name: "Chrome PDF Plugin"
                },
                {
                    0: {type: "application/pdf", suffixes: "pdf", description: "", enabledPlugin: Plugin},
                    description: "",
                    filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                    length: 1,
                    name: "Chrome PDF Viewer"
                },
                {
                    0: {type: "application/x-nacl", suffixes: "", description: "Native Client Executable", enabledPlugin: Plugin},
                    1: {type: "application/x-pnacl", suffixes: "", description: "Portable Native Client Executable", enabledPlugin: Plugin},
                    description: "",
                    filename: "internal-nacl-plugin",
                    length: 2,
                    name: "Native Client"
                }
                ];
                  },
                })
                }""")
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
                        }''', 'fdhdfthfv')
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

    async def main(self, browser):
        user_detail = self.user_detail
        page = await browser.newPage()
        width, height = publicFun.screen_size()
        await page.setViewport({  # 最大化窗口
            "width": width,
            "height": 900
        })

        # await page.evaluateOnNewDocument("""() => {
        #             Object.defineProperty(navigator, webdriver, { get: () => false })
        #         }""")

        try:
            await self.parameter(page)
            # ua = fake_useragent.UserAgent()
            # useragent = ua.chrome
            # await page.setUserAgent(useragent)
            page.setDefaultNavigationTimeout(60000)
        except:
            traceback.print_exc()
            publicFun.logger.info('配置浏览器环境出错')

        ua_update = await page.evaluate('''() => {var ua = navigator.userAgent;return ua}''')
        print('这里是获取到的浏览器ua', ua_update)

        await page.goto('https://www.opencccapply.net/gateway/apply?cccMisCode=531', {'waitUntil': 'domcontentloaded'})

        #await page.screenshot({'path': 'aaaaaaaaa.png'})
        try:
            await asyncio.wait([
                page.click('#portletContent_u16l1n18 > div > div.ccc-page-section > div > a:nth-child(2)'),
                page.waitForNavigation({'waitUntil': 'domcontentloaded'}),
            ])
            # await page.click('#portletContent_u16l1n18 > div > div.ccc-page-section > div > a:nth-child(2)')
        except Exception:
            #await page.screenshot({'path': 'bbbbbbbbb.png'})
            await page.close()
            await browser.close()
            print('页面加载超时')

        await asyncio.wait([
            page.click('#accountFormSubmit'),
            page.waitForNavigation({'waitUntil': 'domcontentloaded'}),
        ])

        # Legal Name
        await page.type('#inputFirstName', user_detail['fullName'].split(' ')[0])
        await page.waitFor(1000)
        await page.type('#inputMiddleName', user_detail['fullName'].split(' ')[1])
        await page.waitFor(1000)
        await page.type('#inputLastName', user_detail['fullName'].split(' ')[2])
        await page.waitFor(1000)
        await page.click('#hasOtherNameNo')
        await page.waitFor(1000)
        await page.click('#hasPreferredNameNo')
        # Date of Birth
        await page.select('#inputBirthDateMonth', user_detail['birthday'].split('/')[0])
        await page.waitFor(1000)
        await page.select('#inputBirthDateDay', user_detail['birthday'].split('/')[1])
        await page.waitFor(1000)
        await page.type('#inputBirthDateYear', user_detail['birthday'].split('/')[2])
        await page.waitFor(1000)
        await page.select('#inputBirthDateMonthConfirm', user_detail['birthday'].split('/')[0])
        await page.waitFor(1000)
        await page.select('#inputBirthDateDayConfirm', user_detail['birthday'].split('/')[1])
        await page.waitFor(1000)
        await page.type('#inputBirthDateYearConfirm', user_detail['birthday'].split('/')[2])
        await page.waitFor(1000)
        # Social Security Number
        await page.click('#-have-ssn-yes')
        await page.waitFor(2000)
        await page.type('#-ssn-input1', user_detail['ssn'].replace('-', ''))
        await page.waitFor(1000)
        await page.type('#-ssn-input2', user_detail['ssn'].replace('-', ''))
        await page.waitFor(1000)
        await asyncio.wait([
            page.click('#accountFormSubmit'),
            page.waitForNavigation(),
        ])
        await page.waitFor(5000)
        # Email
        await page.type('#inputEmail', user_detail['email'])
        await page.waitFor(1000)
        await page.type('#inputEmailConfirm', user_detail['email'])
        await page.waitFor(1000)
        # Telephone
        await page.type('#inputSmsPhone', user_detail['phoneNumber'])
        await page.waitFor(1000)
        # Permanent Address
        await page.type('#inputStreetAddress1', user_detail['street'])
        await page.waitFor(1000)
        await page.type('#inputStreetAddress2', user_detail['street'])
        await page.waitFor(1000)
        await page.type('#inputCity', user_detail['city'])
        await page.waitFor(1000)
        await page.select('#inputState', user_detail['state'])
        await page.waitFor(1000)
        await page.type('#inputPostalCode', user_detail['zipCode'])
        await page.waitFor(1000)

        # 提交报错
        await asyncio.wait([
            page.waitForNavigation({'timeout': 60000}),
            page.click('#accountFormSubmit'),
        ])
        if await page.querySelector('#messageFooterLabel'):
            await page.waitFor(2000)
            await page.click('#messageFooterLabel')
            await page.waitFor(2000)
            await page.click('#inputAddressValidationOverride')
            await page.waitFor(2000)
            await asyncio.wait([
                page.waitForNavigation({'timeout': 60000}),
                page.click('#accountFormSubmit'),
            ])
        await page.waitFor(5000)
        # Username and Password
        await page.type('#inputUserId', user_detail['userName'])
        await page.waitFor(1000)
        await page.type('#inputPasswd', psd)
        await page.waitFor(1000)
        await page.type('#inputPasswdConfirm', psd)
        await page.waitFor(1000)
        # Security PIN
        await page.type('#inputPin', PIN)
        await page.waitFor(1000)
        await page.type('#inputPinConfirm', PIN)
        await page.waitFor(1000)
        # Security Questions
        await page.select('#inputSecurityQuestion1', '1')
        await page.waitFor(1000)
        await page.type('#inputSecurityAnswer1', 'xiefu')
        await page.waitFor(1000)
        await page.select('#inputSecurityQuestion2', '2')
        await page.waitFor(1000)
        await page.type('#inputSecurityAnswer2', 'Rolls-Royce Phantom')
        await page.waitFor(1000)
        await page.select('#inputSecurityQuestion3', '3')
        await page.waitFor(1000)
        await page.type('#inputSecurityAnswer3', user_detail['fullName'])
        await page.waitFor(1000)
        await page.click('#recaptcha > div > div > iframe')
        print('点击人机验证')
        await page.waitFor(2000)
        now_path = os.path.abspath(os.path.abspath(os.path.dirname(__file__)))
        now_path = now_path + '_' + user_detail['userName']
        try:
            frame = page.frames
            for f in frame:
                title = await f.title()
                flag = await f.querySelector('#recaptcha-audio-button')
                if title == 'reCAPTCHA' and flag:  # recaptcha challenge
                    print('存在谷歌验证码的弹出框')
                    await page.waitFor(2000)
                    await f.click('#recaptcha-audio-button')
                    await page.waitFor(2000)
                    link = await f.Jeval('#audio-source', 'el => el.src')
                    path_text = now_path + '\payload.mp3'
                    await page.waitFor(1000)
                    page1 = await browser.newPage()
                    cdp = await page1.target.createCDPSession()
                    await cdp.send('Page.setDownloadBehavior', {
                        'behavior': 'allow',  # 允许所有下载请求
                        'downloadPath': now_path  # 设置下载路径
                    })
                    width, height = publicFun.screen_size()
                    await page.setViewport({  # 最大化窗口
                        "width": width,
                        "height": height
                    })
                    await page1.goto(link)
                    await page1.waitFor(1000)

                    await page1.hover('body > video ')
                    start_x = page1.mouse._x
                    start_y = page1.mouse._y
                    print(start_x, start_y)
                    await page1.mouse.click(start_x + 125, start_y + 55, {'delay': 50})
                    await page1.waitFor(1000)
                    await page1.mouse.click(start_x + 125, start_y + 55, {'delay': 50})
                    await page1.keyboard.press('Enter')
                    await page1.waitFor(3000)
                    await page1.close()

                    await page.waitFor(1000)
                    data = iat3.run(path_text)
                    await page.waitFor(1000)
                    await f.type('#audio-response', data)
                    await page.waitFor(1000)
                    await f.click('#recaptcha-verify-button')
                    await page.waitFor(2000)

                    async def try_test(f):
                        elements = await(await f.querySelector(
                            'body > div > div > div.rc-audiochallenge-error-message')).getProperty(
                            'textContent')
                        title = await elements.jsonValue()
                        if title.strip() == 'Multiple correct solutions required - please solve more.':

                            try:
                                shutil.rmtree(now_path)
                            except WindowsError:
                                pass
                            await f.click('#recaptcha-reload-button')
                            await page.waitFor(2000)
                            link = await f.Jeval('#audio-source', 'el => el.src')
                            path_text = now_path + '\payload.mp3'
                            await page.waitFor(1000)
                            page1 = await browser.newPage()
                            cdp = await page1.target.createCDPSession()
                            await cdp.send('Page.setDownloadBehavior', {
                                'behavior': 'allow',  # 允许所有下载请求
                                'downloadPath': now_path  # 设置下载路径
                            })
                            width, height = publicFun.screen_size()
                            await page.setViewport({  # 最大化窗口
                                "width": width,
                                "height": height
                            })
                            await page1.goto(link)
                            await page1.waitFor(1000)

                            await page1.hover('body > video ')
                            start_x = page1.mouse._x
                            start_y = page1.mouse._y
                            print(start_x, start_y)
                            await page1.mouse.click(start_x + 125, start_y + 55, {'delay': 50})
                            await page1.waitFor(1000)
                            await page1.mouse.click(start_x + 125, start_y + 55, {'delay': 50})
                            await page1.keyboard.press('Enter')
                            await page1.waitFor(3000)
                            await page1.close()

                            await page.waitFor(1000)
                            data = iat3.run(path_text)
                            await page.waitFor(1000)
                            await f.type('#audio-response', data)
                            await page.waitFor(1000)
                            await f.click('#recaptcha-verify-button')
                            await page.waitFor(2000)

                            if await f.querySelector(
                                    'body > div > div > div:nth-child(1) > div.rc-doscaptcha-body > div'):
                                flag = 'Your computer or network may be sending automated queries. To protect our users, we can\'t process your request right now. For more details visit '
                                return False

                            await try_test(f)

                    await try_test(f)

                    break
        except:
            traceback.print_exc()
            print("人机验证失败，请重试")
            await page.screenshot({'path': 'bbbbbbbbb.png'})
            await page.close()
            await browser.close()

            return False
        finally:
            try:
                shutil.rmtree(now_path)
            except WindowsError:
                pass

        await page.waitFor(2000)
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000 * 60}),
            page.click('#accountFormSubmit'),
        ])
        await page.waitForSelector('#registrationSuccess')
        CCCID = await page.querySelector(
            '#registrationSuccess > main > div.column > div > div > div > p:nth-child(1) > strong')
        tag = False
        if CCCID == None:
            print('申请失败')
            await browser.close()
        else:
            tag = True
        await asyncio.wait([
            page.waitForNavigation({'timeout': 1000 * 30}),
            page.click('#registrationSuccess > main > div.column > div > div > button')
        ])
        await page.close()
        await browser.close()
        return tag

    def kill(self, name):
        # win平台
        pid = self.browser.process.pid
        subprocess.Popen("taskkill /F /pid %s " % pid, shell=True)
        print("结束进程：%d" % pid)
        print("等待结果：%d" % self.browser.process.wait())

        # linux平台
        # try:
        #     pid = self.browser.process.pid
        #     pgid = os.getpgid(pid)
        #     # 强制结束
        #     os.kill(pid, signal.SIGKILL)
        #     print("结束进程：%d" % pid)
        #     print("父进程是：%d" % pgid)
        #     print("等待结果：%d" % self.browser.process.wait())
        # except BaseException as err:
        #     print("close: {0}".format(err))
        # time.sleep(3)
        # 查看是否还有其他进程
        # for proc in psutil.process_iter():
        #     if name in proc.name():
        #         try:
        #             os.kill(proc.pid, signal.SIGTERM)
        #             print('已杀死[pid:%s]的进程[pgid：%s][名称：%s]' % (proc.pid, pgid, proc.name()))
        #         except BaseException as err:
        #             print("kill: {0}".format(err))

    async def do(self):
        await self.newbrowser()
        try:
            tag = await self.main(self.browser)
            # self.kill('chrome')
            return tag
        except:
            traceback.print_exc()
            print('申请失败', time.localtime(), self.user_detail['userName'])
            await self.browser.close()
            # self.kill('chrome')
            return False
        finally:
            self.kill('chrome')


if __name__ == '__main__':

    while True:
        user_detail = publicFun.get_user_detail(0)
        if user_detail:
            try:
                print(user_detail)
                try:
                    tag = asyncio.get_event_loop().run_until_complete(Browser(user_detail).do())
                    if tag == True:
                        publicFun.update_user_tag(user_detail['email'], 1)
                        flag = True
                    else:
                        publicFun.update_user_tag(user_detail['email'], 3)
                        print('人机验证失败')
                except:
                    publicFun.update_user_tag(user_detail['email'], 3)
                    traceback.print_exc()
                    print('申请失败')
            except Exception:
                traceback.print_exc()
                continue
            finally:
                print(time.strftime("%Y-%m-%d %X", time.localtime()))
                time.sleep(30)
