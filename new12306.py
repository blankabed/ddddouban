import requests
import json
import urllib.parse
import re
from json import loads
import time
import datetime
import urllib.request
import http.cookiejar
requests.packages.urllib3.disable_warnings()
class Train:
    """12306抢票"""
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }
        self.site_dict = dict()
        self.secretStr = []
    def login(self, username, password):
        self.username = username
        self.password = password
        print("--------------------------登陆12306系统-------------------------")
        img_code = self.session.get(
            'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.8826254050991758',
            verify=False, headers=self.headers)
        with open(r'C:\Users\asus\Desktop\验证码.png', 'wb') as f:
            f.write(img_code.content)
        img_xy = input('请输入验证码坐标:')
        data = {
            "callback": "jQuery19108754385247664451_1555036549517",
            "answer": img_xy,
            "rand": "sjrand",
            "login_site": "E",
            "_": "1555036549519",
        }

        req = self.session.post('https://kyfw.12306.cn/passport/captcha/captcha-check', verify=False,
                                headers=self.headers,
                                data=data)
        print(req.text)
        code = re.findall(r'"result_code":"(.*?)"', req.text)[0]
        if code == '4':
            # 验证用户名与密码
            login_url = 'https://kyfw.12306.cn/passport/web/login'
            Form_Data = {
                'username': self.username,
                'password': self.password,
                'appid': 'otn',
                'answer': img_xy
            }
            response = self.session.post(login_url,headers=self.headers, data=Form_Data)
            print(response.content)
            res = loads(str(response.content).replace("'",'""'),strict=False)
            if res['result_code'] == 0:
                print('用户名密码验证正确')
                uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
                response = self.session.post(uamtk_url,headers=self.headers, data={'appid': 'otn'})
                res = response.json()
                if res['result_code'] == 0:
                    print('获取token成功')
                    check_token_url = 'https://kyfw.12306.cn/otn/uamauthclient'
                    response = self.session.post(check_token_url, headers=self.headers,data={'tk': res['newapptk']})
                    res = response.json()
                    if res['result_code'] == 0:
                        print('验证token通过')
                        print('登陆成功')
            else:
                print('用户名或密码错误')


        # # 用户名密码
        # data = {
        #     'username': self.username,
        #     'password': self.password,
        #     'appid': 'otn',
        #     'answer': img_xy
        # }
        # req = self.session.post('https://kyfw.12306.cn/passport/web/login', verify=False, headers=self.headers,
        #                         data=data)
        # req.encoding = 'utf-8'
        # print(re.findall('"result_message":"(.*?)"',req.text))
        # response = req.json(strict=False)
        # if response['result_code'] == 0:
        #     data = {
        #         'appid': 'otn',
        #     }
        #     req = self.session.post('https://kyfw.12306.cn/passport/web/auth/uamtk', verify=False, headers=self.headers,
        #                             data=data)
        #     req.encoding = 'utf-8'
        #     response = req.json(strict=False)
        #     print(response)
        #     tk = response['newapptk']
        #     data = {
        #         'tk': tk
        #     }
        #     req = self.session.post('https://kyfw.12306.cn/otn/uamauthclient', verify=False, headers=self.headers,
        #                             data=data)
        #     req.encoding = 'utf-8'
        #     response = req.json(strict=False)
        #     if response['result_code'] == 0:
        #         print('登录成功')
        #         return True
        # print('登录失败')
        # self.login(username, password)
def main():
    username=input("请12306账号：")
    password=input("请输入密码：")
    train=Train()
    train.login(username,password)
main()