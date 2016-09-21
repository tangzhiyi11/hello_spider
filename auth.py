#-*- coding:utf-8 -*-

import requests
import re
import json
import cookielib
import ConfigParser
import os
import sys
import termcolor
import ConfigParser
import pickle

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')


class Auth(object):
    domain = 'https://www.douban.com/'

    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.login_url = 'https://www.douban.com/accounts/login?source=group'
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
        self.jar = cookielib.CookieJar()
        self.session = requests.Session()
        #self.response = self.session.get(self.login_url, cookies=self.session.cookies, headers=self.headers, verify=False)

    def login_douban(self, redir=domain):

        self.form['redir'] = redir
        self.response = self.session.post(self.login_url, cookies=self.jar, data=self.form, headers=self.headers)
        print 'Posted form...'

        #handle captcha code
        while True:
            soup = BeautifulSoup(self.response.text)
            self.captcha = soup.find('img', attrs={'id':'captcha_image'})
            if self.captcha:
                self.captcha_handle()
            else:
                break
        print self.session.cookies
        #write response into file , just for test
        self.test_result(self.response)
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

    @staticmethod
    def parse_conf(conf_file='config.ini'):
        conf = ConfigParser.ConfigParser()
        conf.read(conf_file)
        if conf.has_section('info'):
            account = conf.get('info', 'email')
            password = conf.get('info', 'password')
            return (account, password)
        else:
            return (None, None)

    def test_result(self, result):
        with open('result.txt', 'w') as result_file:
            result_file.write(result.text)

    def is_login(self):
        # check session
        url = "https://www.douban.com/accounts"
        r = self.session.get(url, allow_redirects=False, verify=False, headers=self.headers)
        status_code = int(r.status_code)
        print r.status_code
        self.test_result(r)
        if status_code == 301 or status_code == 302:
            # 未登录
            return False
        elif status_code == 200:
            print 'login already!'
            return True
        else:
            print 'not login!'
            return None



if __name__ == "__main__":
    (account, password) = Auth.parse_conf()
    if account and password:
        login = Auth(account, password)
        login.login_douban()
        login.is_login()
    else:
        print account
        print password
        print 'input user info!'
