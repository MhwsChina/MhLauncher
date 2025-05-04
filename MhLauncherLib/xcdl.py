import threading as thd
import requests as rq
import os,random,hashlib
from sys import stdout
from time import sleep
#from tqdm import tqdm
f,f1,th,us=0,0,0,[]
thr=0
hashing=0
threads=[]
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
def ghash(f,typ='sha1'):
    global hashing
    while hashing>=2:sleep(0.01)
    hashing+=1
    with open(f,'rb') as f:
        while True:
            try:
                sha1=hashlib.new(typ)
                sha1.update(f.read())
                hashing-=1
                return sha1.hexdigest()
            except:pass
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
        u,p,sha=us.pop(0)
        if sha:
            if exists(p):
                if type(sha)==dict:
                    sb=ghash(p,sha['type'])
                    chk=sha['hash']
                else:
                    sb=ghash(p,'sha1')
                    chk=sha
                if sb==chk:
                    f+=1
                    continue
        try:
            print(u)
            dnld(u,p)
            f+=1
        except:f-=1
    th+=1
def jd_tqdm(f1,thread):
    tmp,t=0,0
    for i in tqdm(range(f1),desc='进度',unit='文件'):
        if th>=thread:break
        while i>=f:sleep(0.1)
def jd_ui(tmp0,tmp1,tmp2,tim,top):
    global thr
    s,m,h=0,0,0
    while th<thr:
        if s>59:s,m=0,m+1
        if m>59:m,h=0,h+1
        try:
            tmp0.set('总文件:'+str(f1))
            tmp1.set('已下载:'+str(f))
            if f1:tmp2.set('进度:'+str(int(f/f1*100))+'%')
            else:break
            tim.set(f'用时:{h}时{m}分{s}秒')
        except:break
        s+=1
        sleep(1)
    top.destroy()
def xcdnld(urls,paths,thread,sha=[],tk=None,wt='下载中',join=False):
    global us,f,th,f1,thr,threads
    if us:thread=th
    else:th,f=0,0
    if thread>len(urls):thread=len(urls)
    if not sha:sha=len(urls)*[0]
    #sha=[{'type':'sha1','hash':hash}]
    us=us+list(zip(urls,paths,sha))
    f1,thr=len(us),thread
    for i in range(thread):
        while 1:
            try:
                t=thd.Thread(target=dnlds)
                t.start()
                threads.append(t)
                break
            except:pass
    if join:
        for i in threads:
            try:i.join()
            except:pass
        print('------download ok------',f)
    #jd_tqdm(f1,thread)
    if tk:
        top=tk.Toplevel()
        top.title(wt)
        top.geometry('200x100')
        tmp0,tmp1,tmp2=tk.StringVar(),tk.StringVar(),tk.StringVar()
        tim=tk.StringVar()
        tk.Label(top,textvariable=tmp0,fg='#ff9300',font=('consolas',11)).pack()
        tk.Label(top,textvariable=tmp1,fg='#ff9300',font=('consolas',11)).pack()
        tk.Label(top,textvariable=tmp2,fg='#ff9300',font=('consolas',11)).pack()
        tk.Label(top,textvariable=tim,fg='#ff9300',font=('consolas',11)).pack()
        thd.Thread(target=jd_ui,args=(tmp0,tmp1,tmp2,tim,top)).start()
def joindl():
    global thr,th
    while th<thr:
        sleep(0.5)
def rtor(f,f1):
    jd=f/f1
    t0=int(50*jd)
    t1=50-t0
    stdout.write(f'\r进度:[{t0*"#"}{t1*"."}] {int(jd*100)}% {f}/{f1}')
