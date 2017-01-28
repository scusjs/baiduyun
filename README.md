# baiduyun

Python 百度云命令行工具，目前提供搜索、导出下载链接功能，实测可以使用迅雷等下载并加速。


environment
----

python2/3

需要包：requests, pyqt4（可选）, prettytable

可通过 pip 安装：

`pip install requests Qt.py prettytable`

> pyqt4 的安装参考[这里](https://riverbankcomputing.com/software/pyqt/download)


run
----

`python baiduyun`

or

`./baiduyun`

参数：

> `-b` 如果没有 PyQt4 环境，可以加上 `-b` 参数使用本地浏览器执行

> `--no-check-certificate` 不检查证书

程序运行后，会在用户的云盘 [我的应用数据](https://pan.baidu.com/disk/home#list/vmode=list&path=%2Fapps) 目录下添加一个 [应用文件夹](https://pan.baidu.com/disk/home#list/vmode=list&path=%2Fapps%2Fpcs_test_12)，将文件移动到这个文件夹即可。

> h 显示帮助菜单

> l 列出所有的文件（夹）

> s 搜索文件（夹）

> d 获取文件下载地址（需输入显示文件列表或者搜索后的序号）

> e 退出程序

![demo](https://raw.githubusercontent.com/scusjs/baiduyun/master/demo.gif)


原理
----

通过 Qt 内置浏览器使用 OAuth2 登录百度，获取 access_token，使用 [PCS API](https://d.pcs.baidu.com/rest/2.0/pcs/file?method=download&access_token=23.f2f2a457d65fefaaca199b3d1a0c42d5.2592000.1485530425.3325487139-4404738&path=/apps/docs4baidu/ndmz.mp4)进行操作。

可自行在百度开发者中心注册应用并开通 PCS API，然后替换 config.ini 文件中 client_id 和 base_path 即可。其中 client_id 为应用 apikey，base_path 为填写的 pcs 应用目录。

