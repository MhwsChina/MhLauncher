from .inst import *
from .xcdl import *
from .args import *
from json import loads,dumps
import subprocess as sub
import os,zipfile,hashlib,uuid,random,platform
import shutil as sht
import tkinter as tk
import tkinter.messagebox as mess
import threading as th
def javart():
    if platform.system() == 'Windows':
        return 'java.exe'
    if platform.system() == 'Darwin':
        return 'java'
    if platform.system()=='Linux':
        return 'java'
def unpress(fl,p,f=False):
    try:
        z=zipfile.ZipFile(fl)
        for z1 in z.namelist():
            z.extract(z1,p)
            if f:print('解压',z1)
        z.close()
    except:pass
def testplayer():
    rd=str(uuid.uuid4())
    return {'username':f'Player{random.randint(100,9999)}','uuid':rd,'token':rd}
def ghash(f,typ='sha1'):
    with open(f,'rb') as f:
        return hashlib.new(typ,f.read()).hexdigest()
def exists(p):
    return os.path.exists(p)
def verdict():
    n={'latest':{},'versions':[]}
    try:v=getverdict()
    except:
        print('无法获取mc版本列表,无法进行下载游戏操作!')
        return {}
    try:s=v['versions']
    except:
        print('版本列表错误,请尝试关闭vpn/加速器或检查网络')
        return {}
    return v
def setmem():
    s=input('1.自定义/2.自动分配',['1','2'])
    if s=='1':
        b='M' if input('1.mb/2.gb',['1','2'])=='1' else 'G'
        c=str(input('大小:',typ=int))
        return ['-Xmx'+c+b,'-Xmn'+c+b]
    return []
def fmmb(c):
    return ['-Xmx'+str(c)+'M','-Xmn'+'256'+'M']
def runmc(ver,vdc,javaw,o=None,bqthread=128,sha=0,marg=[],outlog=False,out=None,gl=False,bm=False,d='.minecraft'):
    print('正在补全文件...')
    dc=readv(ver)
    if 'inheritsFrom' in dc:
        bqwj(dc['inheritsFrom'],vdc,d,bqthread,sha)
    bqwj(ver,vdc,d,bqthread,sha)
    print('完成!')
    if not o:o=testplayer()
    if not 'javaw' in javaw:
        outlog=True
    if outlog:javaw=javaw.replace('javaw','java')
    cmd=getmcargs(ver,javaw,o,marg,d,gl)
    if out:
        cmd[0]='"{}"'.format(cmd[0].replace('"',''))
        with open(out,'w',encoding='utf-8') as f:
            f.write(' '.join(cmd))
            mess.showinfo('awa','导出启动脚本完成')
    else:
        print('正在启动',ver)
        th.Thread(target=mess.showinfo,args=('awa','启动成功,游戏窗口待会出现')).start()
        sub.call(cmd,creationflags=sub.CREATE_NO_WINDOW)
def bqwj(ver,vdc,di,thread,sha=0):
    f=pj(di,'versions/'+ver+'/'+ver+'.json')
    f=open(f,'r')
    d=loads(f.read())
    f.close()
    us,ps,uu,pp,sha1=gtmcurl(ver,vdc,di,0,1)
    uss,pss=[],[]
    for i in range(len(us)):
        u,p,s=us[i],ps[i],sha1[i]
        if not exists(p):uss.append(u);pss.append(p)
        if sha:
            if not s:continue
            if ghash(p)!=s:uss.append(u);pss.append(p)
    for i in range(len(uu)):
        u,p=uu[i],pp[i]
        if not exists(p):uss.append(u);pss.append(p)
    if not uss==[]:
        xcdnld(uss,pss,thread,[],tk,'补全文件')
        joindl()
    for l in d['libraries']:
        if 'downloads' not in l:continue
        if 'classifiers' in l['downloads']:
            for n in l['downloads']:
                if n=='artifact':
                    p=pj(di,'versions/'+ver+'/'+ver+'-natives')
                    fl=pj(di,'libraries'+'/'+l["downloads"][n]['path'])
                    unpress(fl,p)
                if n=='classifiers':
                    for n in l['downloads'][n].values():
                        p=pj(di,'versions/'+ver+'/'+ver+'-natives')
                        fl=pj(di,'libraries'+'/'+n['path'])
                        unpress(fl,p)
def allv(d='.minecraft'):
    p=pj(d,'versions')
    ls=[]
    if not exists(p):
        return []
    for i in os.listdir(p):
        if exists(pj(p,i+'/'+i+'.json')):
            ls.append(i)
    return ls
def isv(i,d='.minecraft'):
    return exists(pj(d,'versions/'+i+'/'+i+'.json'))
def isjavaf(java,find=javart()):
    v,tag,pth=0,0,0
    for r,d,f in os.walk(java):
        for name in f:
            if 'bin' in r and name==find:
                tag=True
                pth=pj(r,name)
            if name=='release':
                f=open(pj(r,name),'r')
                i=f.readline()
                while i:
                    i=i.replace('\n','').replace('"','')
                    if i.split('=')[0]=='JAVA_VERSION':
                        v=i.split('=')[1]
                        if '1.8.0' in v:v='8'
                        else:v=v.split('.')[0]
                        break
                    i=f.readline()                   
    return pth,v
def fjava(find=javart(),ls=['java'],t=True):
    jv={}
    if t:ls.append(pj(os.path.expandvars("%APPDATA%"),'.minecraft/runtime'))
    for java in ls:
        if exists(java):
            for i in os.listdir(java):
                tmpp=pj(java,i)
                if os.path.isfile(tmpp):continue
                pth,v=isjavaf(tmpp,find)
                jv[v]=pth
    return jv
def indexv(v,vd):
    dc={}
    vdd=vd['versions'][::-1]
    for i in range(len(vdd)):
        if vdd[i]['id']=='1.12':dc['8']=i#java8 
        if vdd[i]['id']=='17w13a':dc['8s']=i#java8 
        if vdd[i]['id']=='1.17':dc['16']=i#java16
        if vdd[i]['id']=='21w19a':dc['16s']=i#java16
        if vdd[i]['id']=='1.18':dc['17']=i#java17
        if vdd[i]['id']=='1.18-pre2':dc['17s']=i#java17
        if vdd[i]['id']=='1.20.5':dc['21']=i#java21 x64
        if vdd[i]['id']=='24w14a':dc['21s']=i#java21 x64
        if vdd[i]['id']==v:dc['v']=[i,vdd[i]['type']]
    return dc
def mcjava(v,vd,d='.minecraft',m=True):
    dc=readv(v)
    if 'inheritsFrom' in dc:dc=readv(dc['inheritsFrom'])
    """if 'id' in dc:v=dc['id']
    if 'inheritsFrom' in dc:v=dc['inheritsFrom']
    dc=indexv(v,vd)
    mvv=dc['v']
    if mvv[1]=='snapshot':
        if mvv[0]>=0 and mvv[0]<dc['16s']:return '8'
        if mvv[0]>=dc['16s'] and mvv[0]<dc['17s']:return '16'
        if mvv[0]>=dc['17s'] and mvv[0]<dc['21s']:return '17'
        if mvv[0]>=dc['21s']:return '21'
    else:
        if mvv[0]>=0 and mvv[0]<dc['16']:return '8'
        if mvv[0]>=dc['16'] and mvv[0]<dc['17']:return '16'
        if mvv[0]>=dc['17'] and mvv[0]<dc['21']:return '17'
        if mvv[0]>=dc['21']:return '21'"""
    if 'javaVersion' in dc:
        if m:return str(dc['javaVersion']['majorVersion'])
        else:return str(dc['javaVersion']['component'])
    else:
        if m:return '17'
        else:return 'java-runtime-gamma'
def removemc(ver,d='.minecraft'):
    p=pj(d,'versions',ver,ver+'.json')
    if exists(p):
        os.rename(p,pj(d,'versions',ver,'remove_json.json'))
        print('删除',p)
    p=pj(d,'versions',ver,ver+'.jar')
    if exists(p):
        os.rename(p,pj(d,'versions',ver,'remove_jar.jar'))
        print('删除',p)
    print(ver,'删除完毕')   
'''def downjava(ver,p='java',dp=''):
    dc={
        '21':'https://download.java.net/openjdk/jdk21/ri/openjdk-21+35_windows-x64_bin.zip',
        '17':'https://download.oracle.com/java/17/archive/jdk-17.0.12_windows-x64_bin.zip',
        '16':'https://download.java.net/openjdk/jdk16/ri/openjdk-16+36_windows-x64_bin.zip',
        '8':'https://download.java.net/openjdk/jdk8u44/ri/openjdk-8u44-windows-i586.zip'
        }
    f=pj(dp,'java'+ver+'.zip')
    print('开始下载java'+ver,'可能需要几分钟')
    onednld(dc[ver],f,10,r=rtor)
    print('下载完成')
    if not exists(p):os.mkdir(p)
    unpress(f,p,True)
    os.remove(f)'''
