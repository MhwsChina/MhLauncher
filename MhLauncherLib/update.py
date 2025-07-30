import requests as req
from json import loads
import sys,os,shutil
import tkinter.messagebox as mess
from .xcdl import *
from .log import *
def check_update(now_version,save_path='',oot=0,write_path=sys.argv[0],api_url='https://api.github.com/repos/MhwsChina/MhLauncher/tags',dlurl='https://github.com/MhwsChina/MhLauncher/releases/download/%tagver%/Launcher.exe',timeout=3):
    req.packages.urllib3.disable_warnings()
    for i in range(3):
        try:
            js=loads(req.get(api_url,timeout=timeout,verify=False).text)
        except:
            i+=1
            if i==4:raise RuntimeError('无法获取更新')
            log('获取更新失败,正在重试第'+str(i)+'次!')
    latest=js[0]
    n=list(map(int,latest['name'].replace('v','').split('.')))
    n1=list(map(int,now_version.replace('v','').split('.')))
    p=pj(save_path,'update.tmp')
    if n[0]>n1[0] or n[1]>n1[1] or n[2]>n1[2]:
        ur=['https://github.dpik.top/','https://gh.llkk.cc/','https://gh.dpik.top/']
        ok=False
        for i in ur:
            try:
                dnld(i+dlurl.replace('%tagver%',latest['name']),p,timeout)
                ok=True
                break
            except:pass
        if not ok:
            log('update error!!!!!!!')
            mess.showerror('错误','无法下载更新,请手动下载(可能是网络问题?)\n网址(已自动复制):\nhttps://wwzb.lanzouw.com/b00y9z56ne=\n提取码:2025')
            return
        shutil.move(sys.argv[0],pj(save_path,'OLD_LAUNCHER'))
        f=open(p,'rb')
        f1=open(sys.argv[0],'ab')
        f1.write(f.read())
        f1.close()
        f.close()
        os.remove(p)
        mess.showinfo('awa','已更新到最新版本!请重启程序')
        os._exit(0)
    else:
        log('(0_o)已经是最新版本了')
        if oot:mess.showinfo('0_o','已经是最新版本了')
