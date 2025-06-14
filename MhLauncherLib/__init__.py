from .inst import *
from .launch import *
from .log import *
from .update import *
from .args import *
from .java import *
from .fabric import *
from .mod import *
rizhi='''=======更新日志=======
源码:https://github.com/MhwsChina/MhLauncher
v0.0.47
一些修改
下载mod时支持自定义版本
v0.0.46
修复了启动后Failed to execute script的bug
v0.0.45
UI修改
删除游戏时不会删除存档(版本隔离时)
v0.0.44
UI小调整
v0.0.43
修复了一些bug
一些修改
v0.0.42
修复了一个bug
v0.0.41
一些小修改
v0.0.40
修复了部分版本无法识别java的bug
其他一些小修改
v0.0.39
自动更新变快
v0.0.38
第一次启动不需要网络了
(不用加载版本列表)
v0.0.37
修复了无法补全文件的bug
v0.0.36
修复了无法下载java的bug
(恶性)会导致无法启动游戏
其他一些小修改
v0.0.35
修复了不能启动1.20版本forge的bug
v0.0.34
下载时不会下载重复文件
v0.0.33
修复了一些bug,优化UI
新增工具箱功能
取消窗口移动(万不得已,不然滚动条没法用)
v0.0.32
修复了很多bug
v0.0.31
修复了一些bug
v0.0.30
修复了启动forge之后闪退的bug
若还闪退请重新安装forge
v0.0.29
删除旧版本日志
增加安装模组的功能
v0.0.28
新增安装Forge选项
安装模组(将在v0.0.29实现)
修复了一些bug
v0.0.27
新增安装Fabric选项
(但是要装好久)
v0.0.26
修复检查更新UI的bug
修复不能启动1.16版本mc的bug
v0.0.25
优化UI
v0.0.24
修复了一些bug
v0.0.23
添加ui界面!!!!!!!!!!!!!
修复了一些bug
'''[1:-1]
def getrizhi():
    return rizhi
