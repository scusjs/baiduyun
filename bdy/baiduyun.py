# coding: utf-8
##
# @file baiduyun.py
# @brief 
# @author scusjs@foxmail.com
# @version 0.1.00
# @date 2016-12-28
from __future__ import print_function
import sys
import json
import requests
from . import oauth_ui
from . import utils

if sys.version_info[0] < 3:
    str = unicode
    bytes = str


class BaiduYun(object):
    def __init__(self, oauth_info):
        self.oauth_info = oauth_info
        self.base_url = utils.get_config("base_url")
        self.base_path = utils.get_config("base_path")

    def space_info(self):
        params = {"method": "info",
                  "access_token": oauth_info['access_token']}
        response = requests.get(utils.get_config('quota_url'),
                                params=params)
        result = json.loads(response.content)
        if 'error_code' in result:
            return False, result
        return True, result

    def list_dir(self, path="/", method='list', by='time'):
        path = self.base_path + path
        params = {"method": method,
                  "access_token": self.oauth_info['access_token'],
                  "by": by,
                  "path": path}
        response = requests.get(self.base_url,
                                params=params)
        result = json.loads(response.content)
        if 'error_code' in result:
            return False, result
        result = self._get_result_list(result['list'])
        return True, result

    def search_file(self, keyword, path="/", re=1, method='search'):
        path = self.base_path + path
        params = {"method": method,
                  "access_token": self.oauth_info['access_token'],
                  "path": path,
                  "wd": keyword,
                  "re": re}
        response = requests.get(self.base_url,
                                params=params)
        result = json.loads(response.content)
        if 'error_code' in result:
            return False, result
        result = self._get_result_list(result['list'])
        return True, result

    def _get_download_info(self, path):
        return "https://d.pcs.baidu.com/rest/2.0/pcs/file?" \
               "method=download&access_token={access_token}" \
               "&path={path}".format(access_token=self.oauth_info['access_token'],
                                     path=path)

    def _get_result_list(self, file_list):
        for i, val in enumerate(file_list):
            val['download'] = self._get_download_info(val['path'])
            val['name'] = (val['path']).split('/')[-1]
            file_list[i] = val
        return file_list


if __name__ == "__main__":
    oauth_info = utils.read_oauth_info()
    if not utils.oauth_check(oauth_info):
        client_id = utils.get_config("apikey")
        oa_url = "http://openapi.baidu.com/oauth/2.0/authorize?client_id={client_id}" \
                 "&response_type=token&redirect_uri=oob" \
                 "&scope=netdisk".format(client_id=client_id)
        oa_result_base = utils.get_config("oa_result")
        oauth_result = oauth_ui.get_oa_info(oa_url, oa_result_base)
        oauth_info = utils.get_oauth_result(oauth_result)
        if not utils.oauth_check(oauth_info):
            print(oauth_info)
            print("登录错误")
            exit()
        utils.save_oauth_info(oauth_info)

    print("获取数据成功")
    bdy = BaiduYun(oauth_info)

    utils.menu(bdy)

