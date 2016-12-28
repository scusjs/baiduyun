##
# @file oauth_ui.py
# @brief 
# @author scusjs@foxmail.com
# @version 0.1.00
# @date 2016-12-28

from PyQt4.QtWebKit import QWebView
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
import sys

class OAuth2Application(QApplication):
    def __init__(self, oa_url, oa_result_base, args):
        super(QApplication, self).__init__(args)
        QApplication.__init__(self, args)
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
    oa_url = "http://openapi.baidu.com/oauth/2.0/authorize?client_id=FS0X9n8iwlSnqy5cIuwhQXYX&response_type=token&redirect_uri=oob"
    oa_result_base = "http://openapi.baidu.com/oauth/2.0/login_success"
    print(get_oa_info(oa_url, oa_result_base))

