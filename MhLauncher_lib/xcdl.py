import threading as thd
import requests as rq
import os,random
from sys import stdout
from time import sleep
from tqdm import tqdm
f,th,us,ps,rands,t=0,0,[],[],[],False
def pj(a,b):
    return os.path.join(a,b).replace('\\','/')
def qp(n, chuck):
    rs=[]
    if n<chuck:return [[i,i] for i in range(n)]
    if chuck==1:return [[0,n-1]]
    step,c = round(n/chuck),0
    while c<n:
        tmp=c
        c+=step
        if c>n:c=n
        rs.append((tmp,c))
    return rs
def exists(p):
    return os.path.exists(p)
def dnld(url,path,timeout=20):
    try:
        res=rq.get(url,timeout=timeout)
        try:os.makedirs(os.path.split(path)[0],exists_ok=1)
        except:pass
        with open(path,'wb') as f:
            f.write(res.content)
        res=None
    except:
        dnld(url,path,timeout)
def onednld(url,path,timeout=20,chunk_size=1048576,r=None,rs=0):
    try:
        res=rq.get(url,timeout=timeout,stream=True)
        f,size=0,int(res.headers.get('content-length', 0))
        try:os.makedirs(os.path.split(path)[0],exists_ok=1)
        except:pass
        jdt=50
        with open(path,'wb') as ff:
            for c in res.iter_content(chunk_size=chunk_size):
                if c:
                    f+=len(c)
                    ff.write(c)
                    if r!=None:r(f,size)
    except Exception as s:
        if rs:
            stdout.write(f'\r下载错误:{s} 正在重试\n')
            #raise
        onednld(url,path,timeout,chunk_size,r)
    print()
def dnlds(out=False):
    global f,th,us,ps,rands,t
    while len(us)>0:
        while t:sleep(0.000001)
        t=True
        u=us.pop(0)
        p=ps.pop(0)
        t=False
        if out:stdout.write(f'\r下载 {p}{40*" "}\n')
        #stdout.write(f'\r下载 {u}{40*" "}\n')
        try:
            dnld(u,p)
            f+=1
        except:f-=1
    th+=1
def xcdnld(urls,paths,thread,out=False):
    global us,ps,f,th
    th,f=0,0
    us=urls
    ps=paths
    f1=len(urls)
    if f1<thread:thread=f1
    for i in range(thread):
        try:thd.Thread(target=dnlds,args=(out,)).start()
        except:
            while True:
                try:thd.Thread(target=dnlds,args=(out,)).start();break
                except:sleep(0.01)
    '''jdt=50
    while True:
        try:
            if th>=thread:
                jd=f/f1
                t0=int(jdt*jd)
                t1=jdt-t0
                stdout.write(f'\r进度:[{t0*"#"}{t1*"."}] {int(jd*100)}% {f}/{f1} {th}')
                break
            jd=f/f1
            t0=int(jdt*jd)
            t1=jdt-t0
            stdout.write(f'\r进度:[{t0*"#"}{t1*"."}] {int(jd*100)}% {f}/{f1} {th}')
        except:pass
        sleep(0.05)
    stdout.write('\n')'''
    tmp,t=0,0
    for i in tqdm(range(f1),desc='进度',unit='文件'):
        if th>=thread:break
        while i+1>=f:sleep(0.1)
def rtor(f,f1):
    jd=f/f1
    t0=int(50*jd)
    t1=50-t0
    stdout.write(f'\r进度:[{t0*"#"}{t1*"."}] {int(jd*100)}% {f}/{f1}')
