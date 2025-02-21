import threading as thd
import requests as rq
import os,random
from sys import stdout
from time import sleep
f,th,us,ps,rands,t=0,0,[],[],[],False
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
def dnld(url,path,timeout=2):
    try:
        res=rq.get(url,timeout=timeout)
        p=os.path.split(path)[0]
        if not os.path.exists(p):
            try:os.makedirs(p)
            except:pass
        with open(path,'wb') as f:
            f.write(res.content)
    except:
        dnld(url,path,timeout)
def onednld(url,path,timeout=2,chunk_size=1048576,r=None):
    try:
        res=rq.get(url,timeout=timeout,stream=True)
        p,f,size=os.path.split(path)[0],0,int(res.headers.get('content-length', 0))
        if not os.path.exists(p):
            try:os.makedirs(p)
            except:pass
        jdt=50
        with open(path,'wb') as ff:
            for c in res.iter_content(chunk_size=chunk_size):
                if c:
                    f+=len(c)
                    ff.write(c)
                    if r!=None:r(f,size)
    except:
        raise
        onednld(url,path,timeout,chunk_size,r)
    print()
def dnlds():
    global f,th,us,ps,rands,t
    while len(us)>0:
        while t:sleep(0.000001)
        t=True
        u=us.pop(0)
        p=ps.pop(0)
        t=False
        stdout.write(f'\r下载 {p}{40*" "}\n')
        try:
            dnld(u,p)
            f+=1
        except:f-=1
    th+=1
def xcdnld(urls,paths,thread):
    global us,ps,f,th
    th,f=0,0
    us=urls
    ps=paths
    f1=len(urls)
    ls=qp(f1,thread)
    for i in range(thread):
        thd.Thread(target=dnlds).start()
        sleep(0.01)
    jdt=50
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
            sleep(0.00000000000000000000000000000000000000000001)
        except:pass
    stdout.write('\n')
def rtor(f,f1):
    jd=f/f1
    t0=int(50*jd)
    t1=50-t0
    stdout.write(f'\r进度:[{t0*"#"}{t1*"."}] {int(jd*100)}% {f}/{f1}')
