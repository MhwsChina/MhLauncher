import platform,os
from json import loads,dumps
import requests as rq
from .xcdl import *
from .log import *
def ifarm():
    if 'aarch' in platform.architecture()[0]:return 1
    return 0
def gtjavals():
    url='https://launchermeta.mojang.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json'
    while True:
        try:
            return loads(rq.get(url,timeout=999999).text)
        except:raise
def getxt():
    xt=''
    if platform.system()=='Darwin':xt+='mac-os'
    else:xt+=platform.system().lower()
    if ifarm() and platform.system()!='Linux':
        xt+='-arm64'
    else:
        if platform.system()=='Windows':
            xt+='-x64'
    return xt
def downjava(name,path='',dlthread=128):
    ls=gtjavals()
    tmp=ls[getxt()][name][0]
    url=tmp['manifest']['url']
    js=loads(rq.get(url,timeout=999999).text)
    u,p=[],[]
    path=pj(path,tmp['version']['name'])
    for i in js['files']:
        j=js['files'][i]
        if j['type']=='directory':
            if not os.path.exists(i):
                os.makedirs(pj(path,i))
        else:
            if 'downloads' in j:
                if 'raw' in j['downloads']:
                    u.append(j['downloads']['raw']['url'])
                    p.append(pj(path,i))
    xcdnld(u,p,dlthread)
