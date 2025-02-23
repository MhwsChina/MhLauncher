import requests as req
from json import loads
import sys,os
from .xcdl import *
from .log import *
def check_update(now_version,timeout=10,save_path='',write_path=sys.argv[0],api_url='https://api.github.com/repos/MhwsChina/MhLauncher/tags',dlurl='https://gh.llkk.cc/https://github.com/MhwsChina/MhLauncher/releases/download/v0.0.2/Launcher.exe'):
    req.packages.urllib3.disable_warnings()
    js=loads(req.get(api_url,timeout=timeout,verify=False).text)
    latest=js[0]
    n=list(map(int,latest['name'].replace('v','').split('.')))
    n1=list(map(int,now_version.replace('v','').split('.')))
    p=pj(save_path,'update.tmp')
    if n[0]>n1[0] or n[1]>n1[1] or n[2]>n1[2]:
        s=input('发现新版本,是否更新?(输入y表示确认更新)')
        if s!='y':return
        onednld(dlurl,r=rtor)
        os.rename(sys.argv[0],'OLD_LAUNCHER')
        f=open(p,'rb')
        f1=open(sys.argv[0],'ab')
        f1.write(f.read())
        f1.close()
        f.close()
        os.remove(p)
        print('更新完成!请重启程序!')
        pause()
        sys.exit(0)
