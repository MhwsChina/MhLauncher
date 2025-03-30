import threading as thd
import requests as rq
import os,random
from sys import stdout
from time import sleep
#from tqdm import tqdm
f,f1,th,us=0,0,0,[]
thr=0
def pj(*args):
    return os.path.join(*args).replace('\\','/')
def exists(p):
    return os.path.exists(p)
def dnld(url,path,timeout=20,trys=0):
    try:
        res=rq.get(url,timeout=timeout)
        try:os.makedirs(os.path.split(path)[0])
        except:pass
        with open(path,'wb') as f:
            f.write(res.content)
        res=None
    except:
        if trys==4:return
        dnld(url,path,timeout,trys+1)
def onednld(url,path,timeout=20,chunk_size=1048576,r=None,rs=0):
    try:
        res=rq.get(url,timeout=timeout,stream=True)
        f,size=0,int(res.headers.get('content-length', 0))
        try:os.makedirs(os.path.split(path)[0])
        except:pass
        jdt=50
        with open(path,'wb') as ff:
            for c in res.iter_content(chunk_size=chunk_size):
                if c:
                    f+=len(c)
                    ff.write(c)
    except Exception as s:
        if rs:
            #stdout.write(f'\r下载错误:{s} 正在重试\n')
            raise
        onednld(url,path,timeout,chunk_size,r)
    print()
def dnlds():
    global f,th,us,rands,t
    while len(us)>0:
        u,p=us.pop(0)
        try:
            dnld(u,p)
            f+=1
        except:f-=1
    th+=1
def jd_tqdm(f1,thread):
    tmp,t=0,0
    for i in tqdm(range(f1),desc='进度',unit='文件'):
        if th>=thread:break
        while i>=f:sleep(0.1)
def jd_ui(tmp0,tmp1,tmp2,top):
    global thr
    while th<=thr:
        try:
            tmp0.set('总文件:'+str(f1))
            tmp1.set('已下载:'+str(f))
            if f1:tmp2.set('进度:'+str(int(f/f1*100))+'%')
            else:break
        except:break
        sleep(0.001)
    top.destroy()
def xcdnld(urls,paths,thread,tk=None,wt='下载中'):
    global us,f,th,f1,thr
    if us:
        for i in zip(urls,paths):
            us.append(i)
        f1+=len(urls)
        return
    th,f=0,0
    us=list(zip(urls,paths))
    f1=len(us)
    if f1<thread:thread=f1
    thr=0
    thr+=thread
    for i in range(thread):
        try:thd.Thread(target=dnlds).start()
        except:
            while True:
                try:thd.Thread(target=dnlds).start();break
                except:sleep(0.01)
    #jd_tqdm(f1,thread)
    if tk:
        top=tk.Toplevel()
        top.title(wt)
        top.geometry('200x100')
        tmp0,tmp1,tmp2=tk.StringVar(),tk.StringVar(),tk.StringVar()
        tk.Label(top,textvariable=tmp0).pack()
        tk.Label(top,textvariable=tmp1).pack()
        tk.Label(top,textvariable=tmp2).pack()
        thd.Thread(target=jd_ui,args=(tmp0,tmp1,tmp2,top)).start()
def joindl():
    global thr,th
    while th<thr:
        sleep(0.5)
def rtor(f,f1):
    jd=f/f1
    t0=int(50*jd)
    t1=50-t0
    stdout.write(f'\r进度:[{t0*"#"}{t1*"."}] {int(jd*100)}% {f}/{f1}')
