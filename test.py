# -*- coding:utf-8 -*-

import auth
import requests


def run():
    url = 'https://www.douban.com/group/252218/'
    (account, password) = auth.Auth.parse_conf()
    if not account or not password:
        print 'input account and password!'

    douban = auth.Auth(account, password)
    douban.login()
    result = douban.url_get(url)
    douban.test_result(result)

if __name__ == '__main__':
    run()