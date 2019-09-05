#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import get
from os import environ
from sys import exit
from datetime import datetime
from math import ceil
import json
from html import unescape
from argparse import ArgumentParser, RawTextHelpFormatter

try:
    from naryal2580.style import info, fetchFormattedTime, uline, bold, italic, \
  dim, blue, yellow, rst, bad, coolExit, good
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
except Exception as e:
    print(e)
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
                                                                  site,
                                                                  rst,
                                                                  yellow,
                                                                  quota,
                                                                  rst
                                                                  )
    print(colorOut, end='\n\n')

def printNestedResult(keyword, title, link, site, quota):
    colorOut = '\t{}{}{}> {}{}{} {}{}{}{} | {}{}{} [{}{}{}]'.format(
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
                                                                  site,
                                                                  rst,
                                                                  yellow,
                                                                  quota,
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

def stackSearch(keyword_name,pagesize,maxpages,stack_search_apilink):
    printResult("UserName", "Main Stack AccountId", "URL", "Stack Site",
                                    "Your Quota")
    site_itr_total = len(stack_sites['top_stack_sites'])
    site_itr_current = 0
    for site in stack_sites['top_stack_sites']:
        site_itr_current += 1
        quota_remaining, quota_max = get_request_limit(api_key)
        page=1
        while quota_remaining > 0:
            query_string = '?page={}&pagesize={}&order=asc&sort=relevance&q={}&site={}&key={}'.format(
                page, pagesize, keyword_name, site, api_key)
            url = stack_search_apilink + query_string
            response = get(url)
            quota_remaining, quota_max = get_request_limit(api_key)
            page += 1

            json_data = json.loads(response.content)

            if 'items' in json_data:
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

            if page == maxpages + 1:
                print("Max Limit Reached")
                break

            if quota_remaining == 0:
                print(bad('Error -> API Quota Exaushed'), end='\n\n')

def stackUserSearch(username,pagesize,maxpages,user_search_apilink,casesensitvie):
    printResult("UserName", "Main AccountId", "URL", "Stack Site",
                                    "Your Quota")
    site_itr_total = len(stack_sites['top_stack_sites'])
    site_itr_current = 0
    for site in stack_sites['top_stack_sites']:
        site_itr_current += 1
        quota_remaining, quota_max = get_request_limit(api_key)
        page=1
        while quota_remaining > 0:
            query_string = '?page={}&pagesize={}&order=desc&sort=reputation&inname={}&site={}&key={}'.format(
                page, pagesize, username, site, api_key)
            url = user_search_apilink + query_string
            response = get(url)
            quota_remaining, quota_max = get_request_limit(api_key)
            page += 1

            json_data = json.loads(response.content)

            if 'items' in json_data:
                result_items = json_data['items']
                if len(result_items) > 0:
                    for item in result_items:
                        if casesensitvie:
                            if str(item['display_name']).lower() == username.lower():
                                link = unescape(str(item['link']))
                                quota_status = str(quota_remaining)+"/"+str(
                                                                    quota_max
                                                                        )
                                title = unescape(str(item['account_id']))
                                result_site = '{}({}/{})'.format(
                                                            site,
                                                            site_itr_current,
                                                            site_itr_total
                                                                )
                                printResult(username, title, link, site,
                                            quota_status)
                        else:
                            link = unescape(str(item['link']))
                            quota_status = str(quota_remaining)+"/"+str(
                                                                quota_max
                                                                    )
                            title = unescape(str(item['account_id']))
                            result_site = '{}({}/{})'.format(
                                                        site,
                                                        site_itr_current,
                                                        site_itr_total
                                                            )
                            printResult(username, title, link, site,
                                        quota_status)
                else:
                    quota_status = str(quota_remaining)+"/"+str(
                                                            quota_max
                                                                )
                    result_site = '{}({}/{})'.format(
                                                    site,
                                                    site_itr_current,
                                                    site_itr_total
                                                    )
                    printResult(username, "None", "None", site,
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
                printResult(username, "None", "None", site,
                            quota_status)
                break

            if page == maxpages + 1:
                print("Max Limit Reached")
                break

            if quota_remaining == 0:
                print(bad('Error -> API Quota Exaushed'), end='\n\n')

def getData(userId,site_name,query_type):
    site = stack_sites['all_stack_sites'][site_name]['name']

    api_link="https://api.stackexchange.com/2.2/users/{}/{}".format(userId,query_type)
    quota_remaining, quota_max = get_request_limit(api_key)
    page=1
    while quota_remaining > 0:
        query_string = '?page={}&pagesize={}&order=desc&sort=activity&site={}&key={}'.format(
            page, pagesize, site, api_key)
        url = api_link + query_string
        response = get(url)
        quota_remaining, quota_max = get_request_limit(api_key)
        quota_status = str(quota_remaining)+"/"+str(
                                                        quota_max
                                                            )
        page += 1

        json_data = json.loads(response.content)

        if 'items' in json_data:
            result_items = json_data['items']
            if len(result_items) > 0:
                for item in result_items:
                    if query_type == "questions":
                        question_id =unescape(str(item['question_id']))
                        link = unescape(str(item['link']))
                        printNestedResult(userId, question_id, link, site,
                                quota_status)
                    if query_type == "answers":
                        answer_id = unescape(str(item['answer_id']))
                        link = "{}/a/{}".format(stack_sites['top_stack_sites'][site_name]['url'],answer_id)
                        printNestedResult(userId, answer_id, link, site,
                                quota_status)
                    if query_type == "comments":
                        post_id = unescape(str(item['post_id']))
                        link=None
                        printNestedResult(userId, post_id, link, site,
                                quota_status)
                    
            else:
                printNestedResult(userId, "None", "None", site,
                            quota_status)
                break
        else:
            quota_remaining, quota_max = get_request_limit(api_key)
            quota_status = str(quota_remaining)+"/"+str(quota_max)
            printNestedResult(userId, "None", "None", site,
                        quota_status)
            break

        if page == maxpages + 1:
            print("Max Limit Reached")
            break

        if quota_remaining == 0:
            print(bad('Error -> API Quota Exaushed'), end='\n\n')

def getdataByUserId(userid,pagesize,maxpages,site_search_apilink,type):
    quota_remaining, quota_max = get_request_limit(api_key)
    page=1
    while quota_remaining > 0:
        query_string = '?page={}&pagesize={}&key={}'.format(
            page, pagesize, api_key)
        url = site_search_apilink + query_string
        response = get(url)
        quota_remaining, quota_max = get_request_limit(api_key)
        page += 1

        json_data = json.loads(response.content)

        if 'items' in json_data:
            result_items = json_data['items']
            if len(result_items) > 0:
                for item in result_items:
                    user_id = unescape(str(item['user_id']))
                    quota_status = str(quota_remaining)+"/"+str(
                                                        quota_max
                                                            )
                    site_name = unescape(str(item['site_name']))
                    printResult(userid, user_id, site_name, None,
                                quota_status)
                    if type == "questions":
                        print(good("Getting Questions"), end='\n\n')
                        getData(user_id,site_name,"questions")

                    if type == "answers":
                        print(good("Getting Answers"), end='\n\n')
                        getData(user_id,site_name,"answers")

                    if type == "comments":
                        print(good("Getting Comments"), end='\n\n')
                        getData(user_id,site_name,"comments")
            else:
                quota_status = str(quota_remaining)+"/"+str(
                                                        quota_max
                                                            )
                printResult(userid, "None", "None", None,
                            quota_status)
                break
        else:
            quota_remaining, quota_max = get_request_limit(api_key)
            quota_status = str(quota_remaining)+"/"+str(quota_max)
            printResult(userid, "None", "None", None,
                        quota_status)
            break

        if page == maxpages + 1:
            print("Max Limit Reached")
            break

        if quota_remaining == 0:
            print(bad('Error -> API Quota Exaushed'), end='\n\n')

if __name__ == '__main__':
    parser = ArgumentParser(
            description='StackDump', epilog='''Example:\n 
            Advanced Keyword Search: stackdump -k "example"\n
            Keywork search with Limit: stackdump -k "example" -l 50\n
            Find User exact match: stackdump -f Goron -e\n
            Get answers for Userid: stackdump -u 123123 -t answers\n
            Get questions for Userid: stackdump -u 123123 -t questions\n
            Get comments for Userid: stackdump -u 123123 -t comments\n
                                                          ''',
        formatter_class=RawTextHelpFormatter)

    requiredparser = parser.add_argument_group('required arguments')
    requiredparser.add_argument('-k', '--keyword', help="Keyword to lookup",
                                type=str, dest="keyword")
    requiredparser.add_argument('-l', '--limit', type=int, dest="limit",
                                help="Limit Results per Stack Site: min:10")

    requiredparser.add_argument('-f', '--find-user', help="UserId Lookup by Keyword",
                                type=str, dest="user")
    requiredparser.add_argument('-e', '--exact-match', help="Case sensitive search",
                                action='store_true',dest='exact')

    requiredparser.add_argument('-u', '--user-id', help="Stack UserId got from -f/--find-user",
                                type=int, dest="userId")

    requiredparser.add_argument('-t', '--type', help="Get all answers, questions and comments posted by an UserId",
                                type=str, dest="type")

    args = parser.parse_args()

    stack_search_apilink = "https://api.stackexchange.com/2.2/search/advanced"
    user_search_apilink = "https://api.stackexchange.com/2.2/users"
    user_associated_apilink = "https://api.stackexchange.com/2.2/users/"

    user_question_apilink ="https://api.stackexchange.com/2.2/users/6452322/questions"
    user_answer_apilink = "https://api.stackexchange.com/2.2/users/6452322/answers"
    user_comment_apilink = "https://api.stackexchange.com/2.2/users/6452322/comments"
    

    print(info('Started [at] {}'.format(datetime.now())), end='\n\n')

    pagesize = 10
    if args.limit:
            if args.limit >= 10 and args.limit <= 1000:
                maxpages = ceil(float(args.limit/10))
                print(maxpages)
            else:
                print(bad("--limit where 10>=limit<=1000"), end='\n\n')
                coolExit(1)
    else:
        maxpages=100

    if args.keyword:    
        try:
            print(info('Started Advanced Search'), end='\n\n')
            stackSearch(args.keyword,pagesize,maxpages,stack_search_apilink)
        except KeyboardInterrupt:
                        print(bad("Interupt Received"), end='\n\n')
                        coolExit(1)
    
    if args.user:
        try:
            print(info('Started User Search'), end='\n\n')
            stackUserSearch(args.user,pagesize,maxpages,user_search_apilink,args.exact)
        except KeyboardInterrupt:
                        print(bad("Interupt Received"), end='\n\n')
                        coolExit(1)

    if args.userId:
        if args.type!="":
            try:
                print(info('Checking Associated StackExchange Sites'), end='\n\n')
                user_associated_apilink =user_associated_apilink +str(args.userId) + "/associated"
                getdataByUserId(args.userId,pagesize,maxpages,user_associated_apilink,args.type)
            except KeyboardInterrupt:
                            print(bad("Interupt Received"), end='\n\n')
                            coolExit(1)
