import requests as rq
from json import loads
from .xcdl import *
from .log import *
import os
def pj(*args):
    return os.path.join(*args).replace('\\','/')
def gt(urls,timeout=10):
    for i in urls:
        try:return rq.get(i,timeout=timeout).text
        except:pass
def getverdict():
    ls=["https://launchermeta.mojang.com/mc/game/version_manifest.json",
        "https://bmclapi2.bangbang93.com/mc/game/version_manifest.json"
        ]
    return loads(gt(ls,10))
def ov(vdc,typ='release',lt=False,find=False):
    #typ=release,snapshot,old_beta,old_alpha
    vs=[]
    if lt:return vdc['latest'][typ]
    for v in vdc['versions']:
        if v['type']==typ:vs.append(v)
        if find:
            if v['id']==typ:return v
    return vs
def readv(ver,d='.minecraft'):
    with open(pj(d,'versions/'+ver+'/'+ver+'.json'),'r') as f:
        return loads(f.read())
def readass(aid,d='.minecraft'):
    with open(pj(d,'assets/indexes/'+aid+'.json'),'r') as f:
        return loads(f.read())
def gtmcurl(ver,vdc,d='.minecraft',bm=False,bq=False):
    us,ps,uu,pp=[],[],[],[]
    if bq:sha1s=[]
    verurl=ov(vdc,ver,find=True)
    if verurl!=[]:
        verurl=verurl['url']
        if bm:verurl=verurl.replace('piston-meta.mojang.com','bmclapi2.bangbang93.com')
        uu.append(verurl)
        pp.append(pj(d,'versions/'+ver+'/'+ver+'.json'))
        try:vdc=loads(rq.get(verurl,timeout=10).text)
        except:vdc=readv(ver)
        clienturl=f"https://bmclapi2.bangbang93.com/version/{ver}/client"
        uu.append(clienturl)
        pp.append(pj(d,'versions/'+ver+'/'+ver+'.jar'))
    else:vdc=readv(ver)
    for lib in vdc['libraries']:
        if 'downloads' not in lib:
            tags=lib['name'].split(':')
            if len(tags)==3:
                p,n,vs=tags
                p=p.replace('.','/')
                f=f'{p}/{n}/{vs}/{n}-{vs}.jar'
                path=pj(d,f'libraries/{f}')
            elif len(tags)==4:
                p,n,vs,xt=tags
                p=p.replace('.','/')
                f=f'{p}/{n}/{vs}/{n}-{vs}-{xt}.jar'
                path=pj(d,f'libraries/{f}')
            url=lib['url']+f
            us.append(url);ps.append(path)
            if bq:
                if 'sha1' in lib:sha1s.append(lib['sha1'])
                else:sha1s.append('SHABI')
            continue
        if "artifact" in lib["downloads"] and not "classifiers" in lib["downloads"]:
            url=str(lib["downloads"]["artifact"]["url"])
            if bm:url=url.replace('libraries.minecraft.net','bmclapi2.bangbang93.com/maven')
            path=pj(d,"libraries/"+lib["downloads"]["artifact"]["path"])
            us.append(url);ps.append(path)
            if bq:sha1s.append(lib["downloads"]["artifact"]['sha1'])
        if "classifiers" in lib["downloads"]:
            if "artifact" in lib["downloads"]:
                url = lib["downloads"]["artifact"]["url"]
                if bm:url=url.replace("libraries.minecraft.net","bmclapi2.bangbang93.com/maven")
                path = pj(d,"libraries/"+lib["downloads"]["artifact"]["path"])
                us.append(url);ps.append(path)
                if bq:sha1s.append(lib["downloads"]["artifact"]['sha1'])
            for cl in lib["downloads"]["classifiers"].values():
                url=cl["url"]
                if bm:url=url.replace("libraries.minecraft.net","bmclapi2.bangbang93.com/maven")
                path=pj(d,"libraries/"+cl["path"])
                us.append(url);ps.append(path)
                if bq:sha1s.append(cl['sha1'])
    try:assurl=vdc["assetIndex"]["url"]
    except:
        if bq:return us,ps,uu,pp,sha1s
        return us,ps,uu,pp
    if bm:assurl=assurl.replace("launcher.mojang.com","bmclapi2.bangbang93.com")
    asspath=pj(d,'assets/indexes/'+vdc["assetIndex"]["id"]+'.json')
    uu.append(assurl);pp.append(asspath)
    try:assdc=loads(rq.get(assurl,timeout=10).text)
    except:assdc=readass(vdc["assetIndex"]["id"])
    for obj in assdc['objects'].values():
        if bm:url=f"https://bmclapi2.bangbang93.com/assets/{obj['hash'][0:2]}/{obj['hash']}"
        else:url=f"https://resources.download.minecraft.net/{obj['hash'][0:2]}/{obj['hash']}"
        path=pj(d,f"assets/objects/{obj['hash'][0:2]}/{obj['hash']}")
        us.append(url);ps.append(path)
        if bq:sha1s.append(obj['hash'])
    if bq:return us,ps,uu,pp,sha1s
    return us,ps,uu,pp
def downloadmc(ver,vdc,thread=128,dlout=0,bm=False,d='.minecraft'):
    urls,paths,uu,pp=gtmcurl(ver,vdc,d,bm)
    print('开始下载',ver)
    print('开始下载资源文件')
    xcdnld(urls,paths,thread,dlout)
    print('开始下载主文件')
    xcdnld(uu,pp,thread,dlout)
    print(ver,'下载完成')
    pause()
