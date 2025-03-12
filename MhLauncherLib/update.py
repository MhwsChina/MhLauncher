import requests as req
from json import loads
import sys,os,shutil
from .xcdl import *
from .log import *
def check_update(now_version,save_path='',write_path=sys.argv[0],api_url='https://api.github.com/repos/MhwsChina/MhLauncher/tags',dlurl='https://gh.llkk.cc/https://github.com/MhwsChina/MhLauncher/releases/download/%tagver%/Launcher.exe',timeout=10):
    req.packages.urllib3.disable_warnings()
    i=0
    for i in range(3):
        try:
            js=loads(req.get(api_url,timeout=timeout,verify=False).text)
        except:
            i+=1
            if i==4:raise RuntimeError('无法获取更新')
            log('[update]: 获取更新失败,正在重试第'+str(i)+'次!')
    latest=js[0]
    n=list(map(int,latest['name'].replace('v','').split('.')))
    n1=list(map(int,now_version.replace('v','').split('.')))
    p=pj(save_path,'update.tmp')
    if n[0]>n1[0] or n[1]>n1[1] or n[2]>n1[2]:
        s=input('发现新版本,是否更新?(输入y表示确认更新)')
        if s!='y':return
        onednld(dlurl.replace('%tagver%',latest['name']),p,r=rtor)
        shutil.move(sys.argv[0],pj(save_path,'OLD_LAUNCHER'))
        f=open(p,'rb')
        f1=open(sys.argv[0],'ab')
        f1.write(f.read())
        f1.close()
        f.close()
        os.remove(p)
        print('更新完成!请重启程序!')
        pause()
        sys.exit(0)
