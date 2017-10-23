# coding: utf-8
##
# @file utils.py
# @brief 
# @author scusjs@foxmail.com
# @version 0.1.00
# @date 2016-12-28
from __future__ import print_function, unicode_literals

import sys

import json
import os
import platform
import requests
from prettytable import PrettyTable

PY2 = sys.version_info[0] < 3
WIN_PLATFORM = 'windows' in platform.platform().lower()

if PY2:
    from ConfigParser import ConfigParser
    import urlparse
    bytes = str
    str = unicode
else:
    from configparser import ConfigParser
    from urllib import parse as urlparse
    raw_input = input


def get_config(which):
    config = ConfigParser()
    path = os.path.join(os.path.dirname(__file__),
                        'config.ini')
    config.read(path)
    return config.get("bdy", which)


def get_oauth_result(url):
    url = url.replace("#", "?", 1)
    return dict(urlparse.parse_qsl(url))


def save_oauth_info(oauth_info):
    with open('user_access_token', 'w') as f:
        json.dump(oauth_info, f)
        

def read_oauth_info():
    oauth_info = {}
    try:
        with open('user_access_token', 'r') as f:
            oauth_info = json.load(f)
    except:
        pass
    return oauth_info


def oauth_check(oauth_info, verify=True):
    if len(oauth_info) != 5 or 'scope' not in oauth_info \
           or "netdisk" not in oauth_info['scope'] \
           or 'access_token' not in oauth_info:
        return False
    url = "https://openapi.baidu.com/rest/2.0/passport/users/getLoggedInUser" \
          "?access_token={access_token}".format(access_token=oauth_info['access_token'])
    user_info = requests.get(url,verify).json()
    print(user_info)
    if 'error_code' in user_info:
        return False
    return True


def get_size_in_nice_string(size_in_bytes):
    for (cutoff, label) in [(1024*1024*1024, "GB"),
                            (1024*1024, "MB"),
                            (1024, "KB"),
                            ]:
        if size_in_bytes >= cutoff:
            return "%.1f %s" % (size_in_bytes * 1.0 / cutoff, label)

    if size_in_bytes == 1:
        return "1 byte"
    else:
        bytes = "%.1f" % (size_in_bytes or 0,)
        return (bytes[:-2] if bytes.endswith('.0') else bytes) + ' bytes'


def r_input(words):
    if PY2:
        if WIN_PLATFORM:
            return raw_input(words.encode('gbk'))
        else:
            return raw_input(words.encode('utf8'))
    else:
        return raw_input(words)


file_list = []


def menu(bdy):
    global file_list
    file_list = []
    help_text = "\nh 帮助\nl 列出文件列表\nd 获取下载地址\ndl 序列获取下载地址\ns 搜索文件\nq 退出\n"
    while True:
        print(help_text)
        user_input = r_input("请输入命令:")
        if user_input == "l":
            request_flag, file_list_tmp = bdy.list_dir()
            show_table(request_flag, file_list_tmp)

        elif user_input == "q":
            exit()
        elif user_input == "d":
            try:
                user_input = int(r_input("请输入待下载序列号:"))
                if user_input >= len(file_list) or user_input < 0:
                    raise Exception()
            except:
                print("请输入正确的数字序号\n")
                continue
            print("下载地址为：")
            #print(file_list[user_input]['download'])
            print("\n或者\n".join(file_list[user_input]['download']))
        elif user_input == "dl":
            try:
                start_index = int(r_input("请输入起始下载序列号:"))
                if start_index >= len(file_list) or start_index < 0:
                    raise Exception()
            except:
                print("请输入正确的数字序号\n")
                continue
            try:
                end_index = int(r_input("请输入终止下载序列号:"))
                if end_index >= len(file_list) or end_index < start_index:
                    raise Exception()
            except:
                print("请输入正确的数字序号\n")
                continue

            print("正在获取%d到%d的下载地址\n"%(start_index,end_index))
            downlist_file = open("downlist.txt", 'w')
            for i in range(start_index,end_index+1):
                downlist_file.writelines(file_list[i]['download'][1]+'\n')
            downlist_file.close()
            print("已将所有下载地址保存到以下目录的“downlist.txt”文件中:\n%s\n" % os.getcwd())
        elif user_input == "s":
            user_input = r_input("请输入查询文件关键字：")
            request_flag, file_list_tmp = bdy.search_file(user_input)
            show_table(request_flag, file_list_tmp)
        else:
            print(help_text)


def show_table(request_flag, file_list_tmp):
    rows = ["序列号", "文件/目录名", "文件大小"]
    if WIN_PLATFORM:
        encoding = 'gbk'
    else:
        encoding = 'utf-8'
    table = PrettyTable(rows, encoding=encoding)
    if not request_flag:
        print(file_list_tmp)
        return
    global file_list
    file_list = file_list_tmp
    table.padding_width = 1
    for i, val in enumerate(file_list):
        table.add_row([i, val['name'], get_size_in_nice_string(val['size'])])
    print(table)


if __name__ == "__main__":
    url = "http://openapi.baidu.com/oauth/2.0/login_success#expires_in=2592000" \
          "&access_token=23.1890fb4a4b30beaf3cf0f248b5a28a2f.2592000.1485506843.3325487139-9136836" \
          "&session_secret=c3722940549193100b76a0cf540b23d7" \
          "&session_key=9mtqVJioDUmdeS50li0pEhXJmEqXM7h4DE9OMWh22mIPRMnNkCxan+5XKtYmvGxAI5wf3tAWWg" \
          "SXKiKfoPBtZ4jhypKP+1/IXg==&scope=basic"
    save_oauth_info(get_oauth_result(url))
    user_info = read_oauth_info()
    print(oauth_check(user_info))
