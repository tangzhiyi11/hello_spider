#-*- coding:utf-8 -*-

import requests
import re
import json
import cookielib
import ConfigParser
import os
import sys

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host': "accounts.douban.com",
    'Referer': "https://accounts.douban.com/login?source=group",
}
session = requests.Session()
session.cookies = cookielib.LWPCookieJar('cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    pass


# def is_login():
#     # check session
#     url = "https://www.zhihu.com/settings/profile"
#     r = requests.get(url, allow_redirects=False, verify=False, headers=headers)
#     status_code = int(r.status_code)
#     if status_code == 301 or status_code == 302:
#         return False
#     elif status_code == 200:
#         return True
#     else:
#         Logging.warn(u"网络故障")
#         return None


def read_account_from_config_file(config_file="config.ini"):
    conf = ConfigParser.ConfigParser()
    conf.read(config_file)
    if conf.has_section('info'):
        account = conf.get('info', 'email')
        password = conf.get('info', 'password')
        return (account, password)
    else:
        print "解析配置文件失败!"
        return (None, None)


def login(account=None, password=None):
    (account, password) = read_account_from_config_file()
    if account == None or password == None:
        print "输入用户名和密码！"
        return
    form = {}
    form['form_email'] = account
    form['password'] = password
    form['source'] = None
    form['remember'] = 'on'
    form['login'] = '登录'
    url = 'https://accounts.douban.com/login'
    result = session.post(url, data=form, headers=headers, verify=False)
    print result.status_code

    while True:
        soup = BeautifulSoup(result.text)
        captcha = soup.find('img', attrs={'id': 'captcha_image'})
        if captcha:
            result = captcha_handle(form, soup, url)
        else:
            break


def captcha_handle(form, soup, url):
    captcha_url = soup.find('img', attrs={'id': 'captcha_image'})['src']
    print captcha_url
    img = requests.get(captcha_url, headers=headers, verify=False)
    img_name = 'verify.gif'
    open(img_name, "wb").write(img.content)
    os.system('%s' % img_name)
    captcha_id = soup.find('input', attrs={'id': 'captcha-id'})
    captcha_soution = raw_input("input captcha:")
    form['captcha-id'] = captcha_id
    form['captcha-solution'] = captcha_soution
    result = session.post(url, data=form,  verify=False)
    print 'in captcha_handle'
    print result.status_code
    return result


if __name__ == "__main__":
    login()