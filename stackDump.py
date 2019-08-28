#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import get
from os import environ
from sys import exit
from datetime import datetime
import json
from html import unescape
from argparse import ArgumentParser, RawTextHelpFormatter

try:
    from naryal2580.style import info, fetchFormattedTime, uline, bold, italic, \
  dim, blue, yellow, rst, bad, coolExit
except ImportError:
    print("Install missing package with `pip3 install -r ./requirements.txt`", end='\n\n')
    exit(1)

__version__ = 0.7

banner = '''
 ____  _             _      ____
/ ___|| |_ __ _  ___| | __ |  _ \ _   _ _ __ ___  _ __
\___ \| __/ _` |/ __| |/ / | | | | | | | '_ ` _ \| '_ \\
 ___) | || (_| | (__|   <  | |_| | |_| | | | | | | |_) |
|____/ \__\__,_|\___|_|\_\ |____/ \__,_|_| |_| |_| .__/
                                                 |_|     v{}'''.format(
                                                                    __version__
                                                                        )[1:]


print(banner)

try:
    if environ['STACK_API_KEY']:
        api_key = environ['STACK_API_KEY']
except KeyError:
    print(bad("Please Export API key `export STACK_API_KEY='your_key_here'`\n check https://stackapps.com/apps/oauth/register for more details"), end='\n\n')
    coolExit(1)

try:
    stack_sites = json.load(open('stackSites.json'))
except:
    print(bad("Problem with opening stackSites.json File"), end='\n\n')
    coolExit(1)

def printResult(keyword, title, link, site, quota):
    colorOut = '{}{}{}> {}{}{} {}{}{}{} | {}{}{} [{}{}{}]'.format(
                                                                  uline,
                                                                  keyword,
                                                                  rst,
                                                                  bold,
                                                                  title,
                                                                  rst,
                                                                  italic,
                                                                  blue,
                                                                  link,
                                                                  rst,
                                                                  dim,
                                                                  result_site,
                                                                  rst,
                                                                  yellow,
                                                                  quota_status,
                                                                  rst
                                                                  )
    print(colorOut, end='\n\n')


def get_request_limit(key):
    url = "https://api.stackexchange.com/2.2/sites?page=1&pagesize=10&key={}".\
          format(key)
    res = get(url)
    quota_remaining = quota_max = 0
    if res.status_code == 200:
        json_data = json.loads(res.content)
        quota_remaining, quota_max = json_data['quota_remaining'], \
            json_data['quota_max']
    return quota_remaining, quota_max


if __name__ == '__main__':
    parser = ArgumentParser(
        description='StackDump', epilog='''Example: stackdump -k "example"\n''',
        formatter_class=RawTextHelpFormatter)

    requiredparser = parser.add_argument_group('required arguments')
    requiredparser.add_argument('-k', '--keyword', help="Keyword to lookup",
                                type=str, dest="keyword", required=True)
    args = parser.parse_args()

    print(info('Started [at] {}'.format(datetime.now())), end='\n\n')

    apilink = "https://api.stackexchange.com/2.2/search/advanced"
    page = 1
    pagesize = 10

    if args.keyword:
        try:
            site_itr_total = len(stack_sites['top_stack_sites'])
            site_itr_current = 0
            for site in stack_sites['top_stack_sites']:
                site_itr_current += 1
                quota_remaining, quota_max = get_request_limit(api_key)
                keyword_name = args.keyword
                if quota_remaining > 0:
                    while 1:
                        query_string = '?page={}&pagesize={}&order=asc&sor'.format(
                            page, pagesize)
                        query_string += "t=relevance&q={}&site={}&key={}".format(
                            keyword_name, site, api_key)
                        url = apilink + query_string
                        response = get(url)
                        page += 1

                        json_data = json.loads(response.content)

                        if 'items' in json_data:
                            quota_remaining, quota_max = get_request_limit(api_key)
                            result_items = json_data['items']
                            if len(result_items) > 0:
                                for item in result_items:
                                    link = unescape(str(item['link']))
                                    quota_status = str(quota_remaining)+"/"+str(
                                                                        quota_max
                                                                            )
                                    title = unescape(str(item['title']))
                                    result_site = '{}({}/{})'.format(
                                                                site,
                                                                site_itr_current,
                                                                site_itr_total
                                                                    )
                                    printResult(keyword_name, title, link, site,
                                                quota_status)
                            else:
                                quota_remaining, quota_max = get_request_limit(
                                                                            api_key
                                                                            )
                                quota_status = str(quota_remaining)+"/"+str(
                                                                        quota_max
                                                                            )
                                result_site = '{}({}/{})'.format(
                                                                site,
                                                                site_itr_current,
                                                                site_itr_total
                                                                )
                                printResult(keyword_name, "None", "None", site,
                                            quota_status)
                                break
                        else:
                            quota_remaining, quota_max = get_request_limit(api_key)
                            quota_status = str(quota_remaining)+"/"+str(quota_max)
                            result_site = '{}({}/{})'.format(
                                                            site,
                                                            site_itr_current,
                                                            site_itr_total
                                                            )
                            printResult(keyword_name, "None", "None", site,
                                        quota_status)
                            break

                        if quota_remaining == 0:
                            print(bad('Error -> API Quota Exaushed'), end='\n\n')
                            coolExit(1)

                        break 
                else:
                    print(bad('Error -> API Quota Exaushed'), end='\n\n')
                    break
            coolExit(0)
        except KeyboardInterrupt:
                        print(bad("Interupt Received"), end='\n\n')
                        coolExit(1)
