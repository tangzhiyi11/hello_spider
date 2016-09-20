#-*- coding:utf-8 -*-

import requests
import re
import json
import cookielib
import ConfigParser
import os
import sys
import termcolor

from bs4 import BeautifulSoup


class Douban(object):
    domain = 'https://www.douban.com/group/xiaotanzi/'

    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.login_url = 'https://www.douban.com/accounts/login?source=group'

        self.jar = cookielib.LWPCookieJar('cookie')
        self.form = {
            'form_email' : self.account,
            'form_password' : self.password,
            'source' : 'group',
            #'remember' : 'on',
            'login' : '登录',
        }
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Host': "www.douban.com",
            'Referer': "https://www.douban.com/group/explore",
            'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding' : 'gzip, deflate, br',
        }
        self.session = requests.Session()
        self.session.cookies = cookielib.LWPCookieJar('cookies')
        self.response = self.session.get(self.login_url, cookies=self.jar, headers=self.headers, verify=False)

    def login_douban(self, redir=domain):

        self.form['redir'] = redir
        self.response = self.session.post(self.login_url, data=self.form, headers=self.headers)
        print 'Posted form...'

        #handle captcha code
        while True:
            soup = BeautifulSoup(self.response.text)
            self.captcha = soup.find('img', attrs={'id':'captcha_image'})
            if self.captcha:
                self.captcha_handle()
            else:
                break
        self.session.cookies.save()
        print 'login successful!'

    def captcha_handle(self):
        captcha_url = self.captcha['src']
        captcha_id = re.findall('id=(.+)&', captcha_url)[0]
        img = requests.get(captcha_url, headers=self.headers, verify=False)
        with open('verify.gif', 'wb') as verify_file:
            verify_file.write(img.content)
            verify_file.flush()
        os.system('verify.gif')
        captcha_solution = raw_input('input captcha:')
        self.form['captcha-id'] = captcha_id
        self.form['captcha-solution'] = captcha_solution
        self.response = self.session.post(self.login_url, data=self.form, headers=self.headers, verify=False)



if __name__ == "__main__":
    login = Douban('854742740@qq.com', 'tzy123456110')
    login.login_douban()