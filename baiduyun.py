# coding: utf-8
##
# @file baiduyun.py
# @brief 
# @author scusjs@foxmail.com
# @version 0.1.00
# @date 2016-12-28

import oauth_ui
import utils
import requests
import json

client_id, base_path = utils.get_config()


oa_url = "http://openapi.baidu.com/oauth/2.0/authorize?client_id=" + client_id + "&response_type=token&redirect_uri=oob&scope=netdisk"
oa_result_base = "http://openapi.baidu.com/oauth/2.0/login_success"


class Baiduyun(object):
    def __init__(self, oauth_info):
        self.oauth_info = oauth_info
        self.baseurl = "https://c.pcs.baidu.com/rest/2.0/pcs/file"

    def spaceInfo(self):
        baseurl = "https://pcs.baidu.com/rest/2.0/pcs/quota"
        params = {"method":"info", "access_token":oauth_info['access_token']}
        result = json.loads(requests.get(baseurl, params=params).content)
        if result.has_key("error_code"):
            return False, result
        return True, result


    def listDir(self, path = "/"):
        method = "list"
        path = base_path + path
        params = {"method":method, "access_token":oauth_info['access_token'], "by":"time", "path":path}
        result = json.loads(requests.get(self.baseurl, params=params).content)
        if result.has_key("error_code"):
            return False, result
        result = self._getResultList(result['list'])
        return True, result

    def searchFile(self, keyword, path = "/", re = 1):
        method = "search"
        path = base_path + path
        params = {"method":method, "access_token":oauth_info['access_token'], "path":path, "wd":keyword, "re":re}
        result = json.loads(requests.get(self.baseurl, params=params).content)
        if result.has_key("error_code"):
            return False, result
        result = self._getResultList(result['list'])
        return True, result

    def _getDownloadinfo(self, path):
        return "https://d.pcs.baidu.com/rest/2.0/pcs/file?method=download&access_token=" + oauth_info['access_token'] + "&path=" + path

    def _getResultList(self, fileList):
        for i in range(len(fileList)):
            fileList[i]['download'] = self._getDownloadinfo(fileList[i]['path'])
            fileList[i]['name'] = (fileList[i]['path']).split("/")[-1]
        return fileList



if __name__ == "__main__":
    oauth_info = utils.read_oauth_info()
    if not utils.oauth_check(oauth_info):
        oauth_result = oauth_ui.get_oa_info(oa_url, oa_result_base)
        oauth_info = utils.get_oauth_result(oauth_result)
        if not utils.oauth_check(oauth_info):
            print(oauth_info)
            print("登录错误")
            exit()
        utils.save_oauth_info(oauth_info)

    print("获取数据成功")
    bdy = Baiduyun(oauth_info)

    utils.menu(bdy)

