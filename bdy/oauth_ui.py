# coding: utf-8
##
# @file oauth_ui.py
# @brief 
# @author scusjs@foxmail.com
# @version 0.1.00
# @date 2016-12-28
from __future__ import print_function, unicode_literals

try:
    from PyQt4.QtWebKit import QWebView
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QUrl
except ImportError:
    print("尚未安装PyQt4模块，请安装后使用")
    exit()

from .utils import PY2

if PY2:
    str = unicode
    bytes = str


class OAuth2Application(QApplication):
    def __init__(self, oa_url, oa_result_base, args):
        super(OAuth2Application, self).__init__(args)
        self.oa_result_base = oa_result_base
        self.oa_result = oa_result_base
        self.browser = QWebView()
        self.browser.loadFinished.connect(self.__result_available)
        self.browser.load(QUrl(oa_url))
        self.browser.show()
        self.exec_()

    def __result_available(self, ok):
        current_url = self.browser.url().toString()
        if self.oa_result_base in current_url:
            self.oa_result = current_url
            self.browser.close()
            self.exit()

    def check_success(self):
        return self.oa_result != self.oa_result_base


def get_oa_info(oa_url, oa_result_base):
    app = OAuth2Application(oa_url, oa_result_base, sys.argv)
    if not app.check_success():
        return ""
    return str(app.oa_result)


if __name__ == "__main__":
    import utils
    client_id = utils.get_config('apikey')
    oa_result_base = utils.get_config('oa_result')
    print(client_id)
    oa_url = "http://openapi.baidu.com/oauth/2.0/authorize?" \
             "client_id={client_id}&response_type=token" \
             "&redirect_uri=oob&scope=netdisk".format(client_id=client_id)
    print(get_oa_info(oa_url, oa_result_base))

