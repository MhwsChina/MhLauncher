import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mess
from tkinter import filedialog
from MhLauncherLib import *
import webbrowser as webb
import threading as th
import os,sys
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
            dic=loads(f.read())
    dic=fdic(dic)
    upopt(dic)
    return dic
def fdic(dic={}):
    ch=['opt','thread','check_update','bqwj','mb','outlog','bm','gl','zd']
    ck=[0,256,1,0,2048,0,0,0,10]
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
version='v0.0.30'
s3='''
=======更新日志=======
源码:https://github.com/MhwsChina/MhLauncher
v0.0.30
修复了启动forge之后闪退的bug
若还闪退请重新安装forge
v0.0.29
删除旧版本日志
增加安装模组的功能
v0.0.28
新增安装Forge选项
安装模组(将在v0.0.29实现)
修复了一些bug
v0.0.27
新增安装Fabric选项
(但是要装好久)
v0.0.26
修复检查更新UI的bug
修复不能启动1.16版本mc的bug
v0.0.25
优化UI
v0.0.24
修复了一些bug
v0.0.23
添加ui界面!!!!!!!!!!!!!
修复了一些bug
'''[1:-1]
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
        os._exit(0)
    def iconify(self):
        self.w.overrideredirect(False)
        self.w.iconify()
        self.w.overrideredirect(True)
    def zhiding(self):
        while 1:
            if self.zd.get():self.w.attributes('-topmost',1)
            else:self.w.attributes('-topmost',0)
            sleep(0.05)
    def createui(self):
        self.w.title('MhLauncher')
        self.w.overrideredirect(True)
        self.w.resizable(0, 0)
        x=int((self.w.winfo_screenwidth()-self.w.winfo_reqwidth())/2)
        y=int((self.w.winfo_screenheight()-self.w.winfo_reqheight())/2)
        self.w.geometry(f'+{x}+{y}')
        self.w.bind('<ButtonPress-1>',self.mousep)
        self.w.bind('<ButtonRelease-1>',self.mouser)
        self.w.bind("<B1-Motion>",self.mousem)
        closew=tk.Frame(self.w)
        #tk.Button(closew,text='-',bd=0,command=self.iconify).grid(row=0,column=0,padx=10)
        tk.Button(closew,text='x',bd=0,command=self.exit).grid(row=0,column=1,padx=10)
        closew.grid(row=0,column=0,sticky='ne')
        self.nt0=ttk.Notebook(self.w)
        self.gm=tk.Frame()
        self.nt0.add(self.gm,text='启动')
        self.dl=tk.Frame()
        self.nt0.add(self.dl,text='下载')
        self.sett=tk.Frame()
        self.nt0.add(self.sett,text='设置')
        self.gy=tk.Frame()
        self.nt0.add(self.gy,text='关于')
        self.fb=tk.Frame()
        self.nt0.add(self.fb,text='安装fabric/forge')
        self.modd=tk.Frame()
        self.nt0.add(self.modd,text='下载mod')
        #启动界面
        frml=tk.Frame(self.gm)
        tk.Label(frml,text='版本列表').pack()
        self.vers=tk.Listbox(frml,width=50,height=10)
        self.vers.pack()
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
        self.dlls=tk.Listbox(frml1,width=50,height=10)
        self.dlls.pack()
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
        self.vers1=tk.Listbox(frm10,width=50,height=10)
        self.vers1.pack()
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
        self.mods=tk.Listbox(frm12,width=50,height=10)
        self.mods.pack()
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
        #######################
        self.loadopt(opt)
        self.listver()
        self.sxdlls()
        self.nt0.grid(row=1,column=0,padx=10,pady=5)
        th.Thread(target=self.zhiding).start()
        th.Thread(target=self.searchmod).start()
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
        self.zd.set(opt['zd'])
    def saveopt(self):
        opt['thread']=self.dlth.get()
        opt['bm']=self.bm.get()
        opt['check_update']=self.checkup.get()
        opt['bqwj']=self.bqwj.get()
        opt['gl']=self.gl.get()
        opt['mb']=self.mb.get()
        opt['zd']=self.zd.get()
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
    def sxdlls(self):
        self.dlls.delete(0,'end')
        for i in ov(vdc,typ=self.dltype.get()):
            self.dlls.insert('end',i['id'])
    def searchmod(self):
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
            self.buttona.set('下载')
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
            p=filedialog.askdirectory()
            mu=modurl(self.tmpb,self.tmpc,loader)
            for file in mu[0]:
                dnld(file[0],pj(p,file[1]))
            self.tmpa=0
            self.buttona.set('选择')
            self.labela['text']='模组列表'
            th.Thread(target=self.searchmod).start()
            mess.showinfo('安装模组','下载完成!')
            return
main=main_ui()
main.runui()
