import requests
import ConfigParser
import argparse
import pickle
import sys
import time
import re

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


urls = []
result_list = []

def parse_config(file_name):
    conf = ConfigParser.ConfigParser()
    with open(file_name) as input_file:
        conf.readfp(input_file)
        for section in conf.sections():
            url_dict = {}
            url_dict['url'] = conf.get(section, 'url')
            url_dict['host'] = conf.get(section, 'host')
            url_dict['accept'] = conf.get(section, 'accept')
            url_dict['user_agent'] = conf.get(section, 'user_agent')
            url_dict['name'] = section
            urls.append(url_dict)


def get_html():
    for url_dict in urls:
        headers = {}
        headers['Host'] = url_dict['host']
        headers['Accept'] = url_dict['accept']
        headers['User-Agent'] = url_dict['user_agent']
        url = url_dict['url']
        result = requests.get(url, headers=headers)
        result = [result, url_dict['name']]
        result_list.append(result)


def get_html_increase():
    for url_dict in urls:
        headers = {}
        headers['Host'] = url_dict['host']
        headers['Accept'] = url_dict['accept']
        headers['User-Agent'] = url_dict['user_agent']
        url = url_dict['url']
        i = 0
        while i < 500:
            this_url = url + str(i)
            result = requests.get(url, headers=headers)
            if result.status_code == 200:
                get_urls_from_html(result.text)
            else:
                print "failed!"
            i += 25


def get_topic_id_from_url(url):
    if not url.endswith('/'):
        url += '/'
    return url.split('/')[-2]


def get_timestamp(latest_time):
    if re.match(r'^\d{2}.*', latest_time) == None:
        time_array = time.strptime(latest_time, '%Y-%m-%d')
    else:
        time_array = time.strptime('2016-'+latest_time, '%Y-%m-%d %H:%M')
    timestamp = int(time.mktime(time_array))
    return timestamp


def get_urls_from_html(html):
    soup = BeautifulSoup(html)
    tr_list = soup.find_all('tr',attrs={'class':''})

    for tr in tr_list:
        if not tr.has_attr('class'):
            continue
        #get url
        title_td = tr.find('td', attrs={'class' : 'title'})
        url = title_td.find('a')['href']
        topic_id = get_topic_id_from_url(url)
        print topic_id
        #get latest time
        time_td = tr.find('td', attrs={'class' : 'time'})
        latest_time = get_timestamp(time_td.text)
        print latest_time


def run():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('url_conf', help='input url config file')
    args = args_parser.parse_args()
    parse_config(args.url_conf)
    get_html_increase()
    # for result in result_list:
    #     if result[0].status_code == 200:
    #         text = result[0].text
    #         print 'get %s html!' % result[1]
    #         result_file_name = 'result_' + result[1] + '.txt'
    #         result_file = open(result_file_name, 'w')
    #         result_file.write(text)
    #         result_file.close()
    #         result_pickle_name = 'result_' + result[1] + '.pkl'
    #         result_pickle = open(result_pickle_name, 'wb')
    #         pickle.dump(text, result_pickle)
    #         result_pickle.close()
    #         get_urls_from_html(text)

if __name__ == '__main__':
    run()