# coding: utf-8
##
# @file oauth_browser.py
# @brief 
# @author scusjs@foxmail.com
# @version 0.1.00
# @date 2016-12-30
from __future__ import print_function, unicode_literals
import webbrowser
from . import utils


def get_oa_info(oa_url, oa_result_base):
    print("请在浏览器中登录您的百度账户，并且将登录成功后的 url 地址复制过来")
    utils.r_input("按回车继续。。。")
    webbrowser.open(oa_url)
    oa_result = utils.r_input("请输入登录成功后跳转的 url 地址: ")
    if check_success(oa_result, oa_result_base):
        return oa_result
    return ""


def check_success(oa_result, oa_result_base):
    return oa_result_base in oa_result and oa_result != oa_result_base

if __name__ == "__main__":
    print(check_success("http://example.com/oauth#info", "http://example.com/oauth"))
    print(check_success("http://example.com/oauth", "http://example.com/oauth"))
    get_oa_info("https://baidu.com", "https://baidu.com")
