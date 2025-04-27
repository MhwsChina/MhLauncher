import tkinter as tk #UI界面
import tkinter.ttk as ttk#UI界面
import tkinter.messagebox as mess#UI界面
from tkinter import filedialog#UI界面
from MhLauncherLib import *#MhLauncher
import webbrowser as webb#打开浏览器
import threading as th#多线程
import os,sys,psutil,shutil#文件,进程等
import subprocess as sub#运行命令
from time import sleep#停顿(休息),在特定功能中阻止未响应
def getuuid(username):
    if exists('.minecraft/usercache.json'):
        with open('.minecraft/usercache.json') as f:
            v=loads(f.read())
            for i in v:
                if i['name']==username:return i['uuid']
    return str(uuid.uuid4())
def init():
    if not exists('mhl'):os.mkdir('mhl')
    if not exists('mhl/options.json'):dic=fdic()
    else:
        with open('mhl/options.json') as f:
            try:dic=loads(f.read())
            except:dic=fdic()
    dic=fdic(dic)
    upopt(dic)
    return dic
def fdic(dic={}):
    ch=['opt','thread','check_update','bqwj','mb','outlog','bm','gl']
    ck=[0,256,1,0,2048,0,0,0]
    for i in range(len(ch)):
        c,k=ch[i],ck[i]
        if not c in dic:
            if c=='opt':
                dic['opt']={}
                dic['opt']['username']=''
                dic['opt']['uuid']=getuuid(dic['opt']['username'])
                dic['opt']['token']=dic['opt']['uuid']
            else: dic[c]=k
    return dic
def upopt(opt):
    with open('mhl/options.json','w') as f:
        f.write(dumps(opt))
def walk(root,path=''):
    paths=[]
    try:ls=os.listdir(pj(root,path))
    except:return []
    for i in ls:
        if os.path.isdir(pj(root,path,i)):paths=paths+walk(root,pj(path,i))
        paths.append((root,path,i))
    return paths
version,s3='v0.0.39',getrizhi()
print('正在加载配置文件...')
opt=init()
print('完成!')
if exists('mhl/OLD_LAUNCHER'):os.remove('mhl/OLD_LAUNCHER')
print('正在获取版本列表...')
vdc=verdict(sv='mhl')
print('完成!')
if opt['check_update']:
    print('正在检查更新')
    try:
        th.Thread(target=check_update,args=(version,'mhl')).start()
    except:print('失败')
class main_ui:
    def __init__(self):
        self.tmpa,self.tmpb,self.tmpc=0,0,0
        self.w=tk.Tk()
        self.createui()
        self.tmpp0=1
    def mousep(self,event):
        self.X=event.x
        self.Y=event.y
    def mouser(self,event):
        self.X=0
        self.Y=0
    def mousem(self,event):
        dx=event.x-self.X
        dy=event.y-self.Y
        nx=self.w.winfo_x()+dx
        ny=self.w.winfo_y()+dy
        self.w.geometry(f'+{nx}+{ny}')
    def exit(self):
        bk=mess.askyesno('退出程序','确认关闭吗?')
        if bk==False:return
        os._exit(0)
    def iconify(self):
        self.w.state('withdrawn')
        if self.tmpp0:
            mess.showinfo('MhLauncher','已最小化,单击屏幕左上角按钮恢复窗口')
            self.tmpp0-=1
    def zhiding(self):
        while 1:
            if self.zd.get():self.w.attributes('-topmost',1)
            else:self.w.attributes('-topmost',0)
            self.w1.attributes('-topmost','true')
            sleep(0.05)
    def createui(self):
        self.w.title('MhLauncher')
        self.w.overrideredirect(True)
        self.w.resizable(0, 0)
        x=int((self.w.winfo_screenwidth()-self.w.winfo_reqwidth())/2)
        y=int((self.w.winfo_screenheight()-self.w.winfo_reqheight())/2)
        self.w.geometry(f'+{x}+{y}')
        self.w1=tk.Toplevel(self.w)
        self.w1.resizable(0, 0)
        self.w1.overrideredirect(True)
        self.w1.geometry(f'+0+0')
        tk.Button(self.w1,text='MhLauncher',bd=0,command=lambda: self.w.state('normal')).pack()
        #self.w.bind('<ButtonPress-1>',self.mousep)
        #self.w.bind('<ButtonRelease-1>',self.mouser)
        #self.w.bind("<B1-Motion>",self.mousem)
        title=tk.Frame(self.w)
        tk.Label(title,text=f'MhLauncher {version}').pack()
        title.grid(row=0,column=0,sticky='w',pady=5,padx=5)
        closew=tk.Frame(self.w)
        tk.Button(closew,text='-',bd=0,command=self.iconify).grid(row=0,column=0,padx=10)
        tk.Button(closew,text='x',bd=0,command=self.exit).grid(row=0,column=1,padx=10)
        closew.grid(row=0,column=0,sticky='e')
        self.nt0=ttk.Notebook(self.w)
        self.gm=tk.Frame()
        self.nt0.add(self.gm,text='启动')
        self.dl=tk.Frame()
        self.nt0.add(self.dl,text='下载')
        self.modd=tk.Frame()
        self.nt0.add(self.modd,text='下载mod')
        self.fb=tk.Frame()
        self.nt0.add(self.fb,text='安装fabric/forge')
        self.sett=tk.Frame()
        self.nt0.add(self.sett,text='设置')
        self.gjbox=tk.Frame()
        self.nt0.add(self.gjbox,text='工具箱')
        self.gy=tk.Frame()
        self.nt0.add(self.gy,text='关于')
        #启动界面
        frml=tk.Frame(self.gm)
        tk.Label(frml,text='版本列表').pack()
        vs0=tk.Scrollbar(frml,orient='vertical')
        vs0.pack(side='right',fill='y')
        self.vers=tk.Listbox(frml,width=50,height=10,yscrollcommand=vs0.set)
        self.vers.pack(side='left')
        vs0.config(command=self.vers.yview)
        frml.pack(side='left',anchor='w',padx=10,pady=5)
        frmne=tk.Frame(self.gm)
        tk.Label(frmne,text='游戏名').pack(side='top',anchor='center',padx=2,pady=5)
        self.usbox=tk.Entry(frmne)
        self.usbox.bind('<Return>',self.setus)
        self.usbox.pack(side='bottom',anchor='s',padx=2,pady=5)
        frmne.pack(side='top',anchor='ne',padx=10,pady=5)
        #获取输入的游戏名self.usbox.get()
        frmr=tk.Frame(self.gm)
        #self.vers.grid(row=0,column=0,columnspan=3)
        tk.Button(frmr,width=20,text='启动',command=lambda: th.Thread(target=self.runmc).start()).grid(row=0,column=0)
        tk.Button(frmr,width=20,text='删除',command=self.rmmc).grid(row=1,column=0)
        tk.Button(frmr,width=20,text='导出启动脚本',command=lambda: th.Thread(target=self.runmc,args=(1,)).start()).grid(row=2,column=0)
        frmr.pack(side='left',anchor='se',padx=10,pady=5)
        #下载界面
        frml1=tk.Frame(self.dl)
        tk.Label(frml1,text='版本列表').pack()
        vs1=tk.Scrollbar(frml1,orient='vertical')
        vs1.pack(side='right',fill='y')
        self.dlls=tk.Listbox(frml1,width=50,height=10,yscrollcommand=vs1.set)
        self.dlls.pack(side='left')
        vs1.config(command=self.dlls.yview)
        frml1.pack(side='left',anchor='w',padx=10,pady=5)
        frm2=tk.Frame(self.dl)
        self.dltype=tk.StringVar()
        self.dltype.set('release')
        tk.Radiobutton(frm2,text='正式版',variable=self.dltype,value='release',command=self.sxdlls).grid(row=0,column=0,sticky='w')
        tk.Radiobutton(frm2,text='测试版',variable=self.dltype,value='snapshot',command=self.sxdlls).grid(row=1,column=0,sticky='w')
        tk.Radiobutton(frm2,text='远古beta版',variable=self.dltype,value='old_beta',command=self.sxdlls).grid(row=2,column=0,sticky='w')
        tk.Radiobutton(frm2,text='远古alpha版',variable=self.dltype,value='old_alpha',command=self.sxdlls).grid(row=3,column=0,sticky='w')
        tk.Button(frm2,text='下载',command=lambda: th.Thread(target=self.dlmc).start()).grid(row=4,sticky='w')
        frm2.pack(side='top',anchor='e',padx=10,pady=5)
        #设置页面
        self.mb=tk.IntVar()
        #self.mb.set('1024')
        frm3=tk.Frame(self.sett)
        tk.Label(frm3,text='运行内存(mb) 推荐在1024-4096之间').pack(anchor='w')
        tk.Spinbox(frm3,from_=0,to=32768,increment=1024,textvariable=self.mb).pack(anchor='w')
        frm3.grid(row=0,column=0,sticky='w')
        frm4=tk.Frame(self.sett)
        self.dlth=tk.IntVar()
        tk.Label(frm4,text='下载线程').pack(anchor='w')
        tk.Spinbox(frm4,from_=0,to=512,increment=16,textvariable=self.dlth).pack(anchor='w')
        frm4.grid(row=1,column=0,sticky='w')
        frm5=tk.Frame(self.sett)
        tk.Label(frm5,text='下载源').pack(anchor='w')
        self.bm=tk.IntVar()
        #self.bm.set('0')
        tk.Radiobutton(frm5,text='官方(最新,速度快)',variable=self.bm,value=0).pack(anchor='w')
        tk.Radiobutton(frm5,text='国内(如果官方源下载慢选这个)',variable=self.bm,value=1).pack(anchor='w')
        frm5.grid(row=2,column=0,sticky='w')
        frm6=tk.Frame(self.sett)
        tk.Label(frm6,text='程序启动时检查更新').pack()
        self.checkup=tk.IntVar()
        #self.checkup.set('1')
        tk.Radiobutton(frm6,text='是',variable=self.checkup,value=1).pack(side='left',anchor='w')
        tk.Radiobutton(frm6,text='否',variable=self.checkup,value=0).pack(side='left',anchor='e')
        frm6.grid(row=3,column=0,sticky='w')
        frm7=tk.Frame(self.sett)
        tk.Label(frm7,text='补全文件设置').pack(anchor='w')
        self.bqwj=tk.IntVar()
        tk.Radiobutton(frm7,text='快速',variable=self.bqwj,value=0).pack(side='left',anchor='w')
        tk.Radiobutton(frm7,text='全面',variable=self.bqwj,value=1).pack(side='left',anchor='e')
        frm7.grid(row=0,column=1,padx=15)
        frm8=tk.Frame(self.sett)
        tk.Label(frm8,text='版本隔离').pack(anchor='w')
        self.gl=tk.IntVar()
        tk.Radiobutton(frm8,text='关闭',variable=self.gl,value=0).pack(side='left',anchor='w')
        tk.Radiobutton(frm8,text='开启',variable=self.gl,value=1).pack(side='left',anchor='e')
        frm8.grid(row=1,column=1,padx=15)
        frm9=tk.Frame(self.sett)
        tk.Label(frm9,text='窗口置顶').pack(anchor='w')
        self.zd=tk.IntVar()
        tk.Radiobutton(frm9,text='关闭',variable=self.zd,value=0).pack(side='left',anchor='w')
        tk.Radiobutton(frm9,text='开启',variable=self.zd,value=1).pack(side='left',anchor='e')
        frm9.grid(row=2,column=1,padx=15)
        tk.Button(self.sett,text='保存设置',command=self.saveopt).grid(row=3,column=1,sticky='e')
        #关于
        tk.Label(self.gy,text=f'MhLauncher {version}').pack(anchor='w')
        tk.Label(self.gy,text='(c)Copyright 2025 (炜某晟)_MhwsChina_').pack(anchor='w')
        tk.Button(self.gy,text='查看源代码',command=lambda: webb.open('https://github.com/MhwsChina/MhLauncher')).pack(anchor='w')
        tk.Label(self.gy,text='更新日志').pack(anchor='w')
        gxrz=tk.Text(self.gy,width=45,height=8)
        gxrz.insert('end',s3)
        gxrz.pack(side='left')
        tk.Button(self.gy,text='检查更新',command=lambda: th.Thread(target=check_update,args=(version,'mhl',1)).start()).pack(side='left')
        #fabric界面
        frm10=tk.Frame(self.fb)
        tk.Label(frm10,text='版本列表').pack()
        vs2=tk.Scrollbar(frm10,orient='vertical')
        vs2.pack(side='right',fill='y')
        self.vers1=tk.Listbox(frm10,width=50,height=10,yscrollcommand=vs2.set)
        self.vers1.pack(side='left')
        vs2.config(command=self.vers1.yview)
        frm10.grid(column=0,row=0,padx=10,pady=5,rowspan=2)
        tk.Button(self.fb,text='安装',command=lambda: th.Thread(target=self.fabric).start()).grid(column=1,row=0,padx=10,pady=5)
        frm11=tk.Frame(self.fb)
        self.isfg=tk.IntVar()
        tk.Radiobutton(frm11,text='fabric',variable=self.isfg,value=0).pack()
        tk.Radiobutton(frm11,text='forge',variable=self.isfg,value=1).pack()
        frm11.grid(column=1,row=1,padx=10,pady=5)
        #mod页面
        frm12=tk.Frame(self.modd)
        self.labela=tk.Label(frm12,text='模组列表')
        self.labela.pack()
        vs3=tk.Scrollbar(frm12,orient='vertical')
        vs3.pack(side='right',fill='y')
        self.mods=tk.Listbox(frm12,width=50,height=10,yscrollcommand=vs3.set)
        self.mods.pack(side='left')
        vs3.config(command=self.mods.yview)
        frm12.grid(row=0,column=0,padx=10,pady=5)
        self.ssnum=tk.IntVar()
        frm13=tk.Frame(self.modd)
        tk.Label(frm13,text='搜索数量').pack()
        tk.Spinbox(frm13,from_=1,to=60,textvariable=self.ssnum).pack()
        self.ssnum.set(20)
        tk.Label(frm13,text='排序方法').pack()
        self.pxff=tk.StringVar()
        tk.Spinbox(frm13,textvariable=self.pxff,values=('关联','下载量','(作者)关注数量','发布日期','更新日期')[::-1]).pack()
        self.pxff.set('下载量')
        tk.Label(frm13,text='搜索内容').pack()
        self.sstext=tk.Entry(frm13)
        self.sstext.pack()
        self.buttona=tk.StringVar()
        self.buttona.set('选择')
        tk.Button(frm13,text='搜索',command=self.searchmod).pack()
        tk.Button(frm13,textvariable=self.buttona,command=self.dlmod).pack()
        frm13.grid(row=0,column=1,padx=10,pady=5)
        #工具箱
        frm14=tk.Frame(self.gjbox)
        #进程列表
        tk.Label(frm14,text='进程列表').pack()
        vs4=tk.Scrollbar(frm14,orient='vertical')
        vs4.pack(side='right',fill='y')
        self.tasks=tk.Listbox(frm14,width=50,height=10,yscrollcommand=vs4.set)
        self.tasks.pack(side='left')
        vs4.config(command=self.tasks.yview)
        frm14.grid(row=0,column=0,padx=10,pady=5)
        frm15=tk.Frame(self.gjbox)
        tk.Button(frm15,text='刷新进程列表',command=self.flushtask).pack()
        tk.Button(frm15,text='关闭所有该名字的进程',command=self.kill).pack()
        tk.Button(frm15,text='关闭并删除',command=self.rmtask).pack()
        tk.Button(frm15,text='删除该进程的文件夹(卸载)',command=lambda: self.rmtask(1)).pack()
        #tk.Button(frm15,text='获取详细信息').pack()
        tk.Label(frm15,text='命令执行(cmd不可用时)').pack()
        self.cmdt=tk.Entry(frm15)
        self.cmdt.pack()
        tk.Button(frm15,text='执行',command=lambda: self.cmd(self.cmdt.get())).pack()
        frm15.grid(row=0,column=1,padx=10,pady=5)
        #######################
        self.loadopt(opt)
        self.listver()
        self.sxdlls()
        self.nt0.grid(row=1,column=0,padx=10,pady=5)
        th.Thread(target=self.zhiding).start()
        th.Thread(target=self.searchmod).start()
        self.flushtask()
        #获取运行内存self.mb.get()
        #获取下载线程self.dlth.get()
        #获取是否国内源self.bm.get()
        #获取检查更新self.checkup.get()
        #是否全面补全文件self.bqwj.get()
        #版本隔离self.gl.get()
    def runui(self):
        self.w.mainloop()
    def loadopt(self,opt):
        self.dlth.set(opt['thread'])
        self.mb.set(opt['mb'])
        self.bm.set(opt['bm'])
        self.checkup.set(opt['check_update'])
        self.bqwj.set(opt['bqwj'])
        self.gl.set(opt['gl'])
        self.usbox.insert(0,opt['opt']['username'])
    def saveopt(self):
        opt['thread']=self.dlth.get()
        opt['bm']=self.bm.get()
        opt['check_update']=self.checkup.get()
        opt['bqwj']=self.bqwj.get()
        opt['gl']=self.gl.get()
        opt['mb']=self.mb.get()
        upopt(opt)
    def setus(self,event):
        opt['opt']['username']=self.usbox.get()
        upopt(opt)
    def runmc(self,out=None):
        if self.usbox.get()!='':self.setus(1)
        else:mess.showinfo('提示','请先输入游戏名');return
        if not self.vers.curselection():
            mess.showinfo('提示','没有选择版本');return            
        ver=self.vers.get(self.vers.curselection()[0])
        if out:out=ver+'.bat'
        j=mcjava(ver,vdc)
        try:javaw=fjava(ls=['mhl/java'],t=1)[j]
        except:
            downjava(mcjava(ver,vdc,m=False),'./mhl/java',self.dlth.get())
            javaw=fjava(ls=['mhl/java'],t=1)[j]
        runmc(ver,vdc,javaw,opt['opt'],self.dlth.get(),self.bqwj.get(),fmmb(self.mb.get()),False,out,self.gl.get(),self.bm.get())
    def fabric(self): 
        if not self.vers1.curselection():
            mess.showinfo('提示','没有选择版本');return            
        ver=self.vers1.get(self.vers1.curselection()[0])
        java='java-runtime-gamma-snapshot'
        try:javaw=fjava(ls=['mhl/java'],t=1)['17']
        except:
            downjava(java,'./mhl/java',self.dlth.get())
            javaw=fjava(ls=['mhl/java'],t=1)['17']
        #javaw=javaw.replace('javaw','java')
        th.Thread(target=mess.showinfo,args=('安装Fabric/Forge','已开始安装,过程可能需要一两分钟,请耐心等待')).start()
        if self.isfg.get():forge(ver,javaw,'mhl');ver='Forge'+ver
        else:fabric(ver,javaw,'mhl');ver='Fabric'+ver
        self.listver()
        mess.showinfo('安装Fabric/Forge',f'{ver}已成功安装')
    def rmmc(self):
        if not self.vers.curselection():
            mess.showinfo('提示','没有选择版本');return            
        ver=self.vers.get(self.vers.curselection()[0])
        removemc(ver)
        self.listver()
    def listver(self):
        self.vers.delete(0,'end')
        self.vers1.delete(0,'end')
        for i in allv():
            self.vers.insert('end',i)
            self.vers1.insert('end',i)
    def dlmc(self):
        if not self.dlls.curselection():
            mess.showinfo('提示','没有选择版本');return            
        ver=self.dlls.get(self.dlls.curselection()[0])
        print('下载',ver)
        downloadmc(ver,vdc,self.dlth.get(),self.bm.get(),tk)
        self.listver()
        joindl()
        mess.showinfo('提示',f'{ver}下载完毕')
    def sxdlls(self):
        self.dlls.delete(0,'end')
        for i in ov(vdc,typ=self.dltype.get()):
            self.dlls.insert('end',i['id'])
    def searchmod(self):
        self.tmpa=0
        self.buttona.set('选择')
        self.labela['text']='模组列表'
        dc={'关联':'relevance','下载量':'downloads','(作者)关注数量':'follows','发布日期':'newest','更新日期':'updated'}
        px=dc[self.pxff.get()]
        ssnum=self.ssnum.get()
        mod=self.sstext.get()
        self.mods.delete(0,'end')
        self.modss=formatsc(searchmod(mod,ssnum,px))
        for i in self.modss:
            self.mods.insert('end',i[0])
    def dlmod(self):
        if self.tmpa==0:
            if not self.mods.curselection():
                mess.showinfo('提示','没有选择mod');return
            self.tmpa=1
            self.labela['text']='mc版本'
            self.tmpb=self.modss[self.mods.curselection()[0]][2]
            tmp=self.modss[self.mods.curselection()[0]][1]
            self.modss[self.mods.curselection()[0]][1]
            self.mods.delete(0,'end')
            for i in tmp:
                self.mods.insert(0,i)
            return
        if self.tmpa==1:
            if not self.mods.curselection():
                mess.showinfo('提示','没有选择mc版本');return
            self.tmpa=2
            self.labela['text']='mod加载器'
            self.tmpc=self.mods.get(self.mods.curselection()[0]) 
            self.mods.delete(0,'end')
            for i in modurl(self.tmpb,self.tmpc):
                self.mods.insert('end',i)
            return
        if self.tmpa==2:
            if not self.mods.curselection():
                mess.showinfo('提示','没有选择mod加载器');return
            loader=self.mods.get(self.mods.curselection()[0])
            self.dlp=filedialog.askdirectory()
            for i in modurl(self.tmpb,self.tmpc,loader)[0]:
                dnld(i[0],pj(self.dlp,i[1]))
            th.Thread(target=self.searchmod).start()
            mess.showinfo('安装模组','下载完成!')
            return
    def killtask(self,pid):
        psutil.Process(pid).terminate()
    def getalltask(self):
        ts=[]
        for i in psutil.process_iter():
            ts.append((i.pid,i.name()))
        return ts
    def flushtask(self):
        self.tt=self.getalltask()
        self.tasks.delete(0,'end')
        for i in self.tt:
            self.tasks.insert('end',i[1]+'    pid='+str(i[0]))
    def cmd(self,cmd):
        th.Thread(target=sub.run,args=(cmd,)).start()
    def kill(self):
        if not self.tasks.curselection():return
        nm=self.tt[self.tasks.curselection()[0]][1]
        tmp=0
        p=self.getpid(nm)
        while p:
            for i in p:
                try:self.killtask(i)
                except:tmp=1
            sleep(0.5)
            if tmp:break
            self.getpid(nm)
        self.flushtask()
    def getpid(self,name):
        return [i.pid for i in psutil.process_iter() if i.name()==name]
    def killp(self,name):
        for i in self.getpid(name):
            try:self.killtask(i)
            except:pass
    def rmtask(self,di=0):
        if not self.tasks.curselection():return
        pid=self.tt[self.tasks.curselection()[0]][0]
        nm=self.tt[self.tasks.curselection()[0]][1]
        d=psutil.Process(pid).exe()
        fd=os.path.split(d)[0]
        self.killp(nm)
        dls=[]
        try:os.remove(d)
        except:dls.append((d,nm))
        if not di:
            while 1:
                try:os.remove(d);return
                except:pass
        for i in walk(fd):
            r,d,f=i
            p=pj(r,d,f)
            try:self.killp(f)
            except:continue
            dls.append((p,f))
        while dls:
            p,f=dls.pop(0)
            self.killp(f)
            try:
                if os.path.exists(p):
                    if os.path.isdir(p):
                        shutil.rmtree(p)
                        continue
                    os.remove(p)
            except:
                dls.append((p,f))
main=main_ui()
main.runui()
