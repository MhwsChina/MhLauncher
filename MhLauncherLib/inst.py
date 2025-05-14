import requests as rq
from json import loads
from .xcdl import *
from .log import *
import os
def pj(*args):
    return os.path.join(*args).replace('\\','/')
def gt(urls,timeout=10):
    for i in urls:
        try:
            log('GET'+' '+i)
            return rq.get(i,timeout=timeout).text
        except:pass
def getverdict():
    ls=["https://launchermeta.mojang.com/mc/game/version_manifest.json",
        "https://bmclapi2.bangbang93.com/mc/game/version_manifest.json"
        ]
    return loads(gt(ls,5))
def ov(vdc,typ='release',lt=False,find=False):
    #typ=release,snapshot,old_beta,old_alpha
    vs=[]
    if lt:return vdc['latest'][typ]
    for v in vdc['versions']:
        if v['type']==typ:vs.append(v)
        if find:
            if v['id']==typ:return v
    return vs
def printvdc(vdc):
    if vdc=={}:
        print('无可用版本,请检查网络连接!')
        pause()
        return
    print('1.正式版\n2.测试版\n3.远古alpha版\n4.远古beta版')
    c=input('选择序号:',['1','2','3','4'])
    if c=='1':t='release'
    if c=='2':t='snapshot'
    if c=='3':t='old_alpha'
    if c=='4':t='old_beta'
    o=ov(vdc,t)[::-1]
    i,j=len(o),0
    clear()
    while i:
        i-=1;j+=1
        print('\r版本:',o[i]['id'],'发布时间:',o[i]['releaseTime'])
        if j>=15:
            j=0
            tmp=input('1.下一页/2.返回',['1','2'])
            if tmp=='2':return
            print('\r'+20*' ',end='')
    if j<15:pause()
def readv(ver,d='.minecraft'):
    with open(pj(d,'versions/'+ver+'/'+ver+'.json'),'r') as f:
        return loads(f.read())
def readass(aid,d='.minecraft'):
    with open(pj(d,'assets/indexes/'+aid+'.json'),'r') as f:
        return loads(f.read())
def getjsonurl(vdc,ver,d='.minecraft'):
    if not vdc:return 0,0
    verurl=ov(vdc,ver,find=True)
    if verurl==[]:return False,pj(d,'versions/'+ver+'/'+ver+'.json')
    verurl=verurl['url']
    #if bm:verurl=verurl.replace('piston-meta.mojang.com','bmclapi2.bangbang93.com')
    return verurl,pj(d,'versions/'+ver+'/'+ver+'.json')
def getassurl(vdc,d='.minecraft'):
    if not vdc:return 0,0
    if 'assetIndex' in vdc:
        return vdc["assetIndex"]["url"],pj(d,'assets/indexes/'+vdc["assetIndex"]["id"]+'.json')
    else:return False,False
def get_library_path(name, path):
    libpath = pj(path, "libraries")
    parts = name.split(":")
    base_path, libname, version = parts[0:3]
    for i in base_path.split("."):
        libpath = pj(libpath, i)
    try:
        version, fileend = version.split("@")
    except ValueError:
        fileend = "jar"
    filename = f"{libname}-{version}{''.join(map(lambda p: f'-{p}', parts[3:]))}.{fileend}"
    libpath = pj(libpath, libname, version, filename)
    return libpath
def libraries(vdc,bm=False,bq=False,d='.minecraft',uri='https://bmclapi2.bangbang93.com'):
    us,ps,sha1s=[],[],[]
    for lib in vdc['libraries']:
        if 'downloads' not in lib:
            if 'url' not in lib:continue
            f=get_library_path(lib['name'],'')
            url=lib['url']+f
            path=pj(d,f)
            us.append(url);ps.append(path)
            if bq:
                if 'sha1' in lib:sha1s.append(lib['sha1'])
                else:sha1s.append(False)
            continue
        if "artifact" in lib["downloads"] and not "classifiers" in lib["downloads"]:
            if lib["downloads"]["artifact"]["url"]=='':continue
            url=str(lib["downloads"]["artifact"]["url"])
            if bm:url=url.replace('https://libraries.minecraft.net',uri+'/maven')
            path=pj(d,"libraries/"+lib["downloads"]["artifact"]["path"])
            us.append(url);ps.append(path)
            if bq:sha1s.append(lib["downloads"]["artifact"]['sha1'])
        if "classifiers" in lib["downloads"]:
            if "artifact" in lib["downloads"]:
                url = lib["downloads"]["artifact"]["url"]
                if bm:url=url.replace("https://libraries.minecraft.net",uri+"/maven")
                path = pj(d,"libraries/"+lib["downloads"]["artifact"]["path"])
                us.append(url);ps.append(path)
                if bq:sha1s.append(lib["downloads"]["artifact"]['sha1'])
            for cl in lib["downloads"]["classifiers"].values():
                url=cl["url"]
                if bm:url=url.replace("https://libraries.minecraft.net",uri+"/maven")
                path=pj(d,"libraries/"+cl["path"])
                us.append(url);ps.append(path)
                if bq:sha1s.append(cl['sha1'])
    if bq:return us,ps,sha1s
    return us,ps
def assets(assdc,bm=False,bq=False,d='.minecraft',uri='https://bmclapi2.bangbang93.com'):
    us,ps,sha1s=[],[],[]
    for obj in assdc['objects'].values():
        if bm:url=f"{uri}/assets/{obj['hash'][0:2]}/{obj['hash']}"
        else:url=f"https://resources.download.minecraft.net/{obj['hash'][0:2]}/{obj['hash']}"
        path=pj(d,f"assets/objects/{obj['hash'][0:2]}/{obj['hash']}")
        us.append(url);ps.append(path)
        if bq:sha1s.append(obj['hash'])
    if bq:return us,ps,sha1s
    return us,ps
def gtmcurl(ver,vdc,d='.minecraft',bm=False,bq=False,uri='https://bmclapi2.bangbang93.com'):
    if not bq and vdc=={}:
        print('无法加载版本列表,请检查网络连接')
        return
    us,ps,uu,pp=[],[],[],[]
    sha1s=[]
    url,path=getjsonurl(vdc,ver,d)
    if url:
        if bq:uu.append(url);pp.append(path)
        else:
            print('开始下载版本索引')
            dnld(url,path,1000)
            print('完成')
    try:vdc=readv(ver)
    except:
        print('开始下载版本索引')
        dnld(url,path,1000)
        print('完成')
        vdc=readv(ver)
    if 'downloads' in vdc:
        if bm:clienturl=f"https://bmclapi2.bangbang93.com/version/{ver}/client"
        else:clienturl=vdc['downloads']['client']['url']
        clientpath=pj(d,'versions/'+ver+'/'+ver+'.jar')
        us.append(clienturl);ps.append(clientpath)
        sha1s.append(vdc['downloads']['client']['sha1'])
    us1,ps1,sh=libraries(vdc,bm,1,d,uri)
    us=us+us1
    ps=ps+ps1
    sha1s=sha1s+sh
    url,path=getassurl(vdc,d)
    if url:
        if bq:uu.append(url);pp.append(path)
        else:
            print('开始下载资源索引')
            dnld(url,path,1000)
            print('完成')
    if 'assetIndex' in vdc:
        try:assdc=readass(vdc["assetIndex"]["id"])
        except:
            url,path=getassurl(vdc,d)
            print('开始下载资源索引')
            dnld(url,path,1000)
            print('完成')
        assdc=readass(vdc["assetIndex"]["id"])
        us1,ps1,sh=assets(assdc,bm,1,d,uri)
        us=us+us1
        ps=ps+ps1
        sha1s=sha1s+sh
    if bq:return us,ps,uu,pp,sha1s
    return us,ps,sha1s
'''def downloadmc_noui(ver,vdc,thread=128,dlout=0,bm=False,d='.minecraft'):
    print('开始下载',ver)
    urls,paths=gtmcurl(ver,vdc,d,bm)
    print('开始下载资源文件')
    xcdnld(urls,paths,thread,dlout)
    #asyncio.run(asyncdl(urls,paths,300))
    print(ver,'下载完成')
    pause()'''
def downloadmc(ver,vdc,thread,bm=False,tk=None,d='.minecraft'):
    urls,paths,sha1s=gtmcurl(ver,vdc,d,bm)
    xcdnld(urls,paths,thread,sha1s,tk,'下载游戏')
