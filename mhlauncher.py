import tkinter as tk #UI界面
import tkinter.ttk as ttk#UI界面
import tkinter.messagebox as mess#UI界面
import tkinter.colorchooser as cc
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
    ch=['opt','thread','check_update','bqwj','mb','outlog','bm','gl','text_color','font']
    ck=[0,128,1,0,2048,0,0,1,'#000000','@Fixedsys']
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
version,s3='v0.0.56',getrizhi()
log('正在加载配置文件...')
opt=init()
log('完成!')
if exists('mhl/OLD_LAUNCHER'):os.remove('mhl/OLD_LAUNCHER')
log('正在获取版本列表...')
vdc=verdict()
log('完成!')
if opt['check_update']:
    log('正在检查更新')
    try:
        th.Thread(target=check_update,args=(version,'mhl')).start()
    except:log('失败')
ffg=opt['text_color']
font=opt['font']
def Label(b,si=11,**kw):
    return tk.Label(b,**kw,highlightthickness=0,fg=ffg,font=(font,si))
def Listbox(b,si=11,**kw):
    return tk.Listbox(b,**kw,highlightthickness=0,fg=ffg,font=(font,si))
def Button(b,si=11,**kw):
    #activebackground='#fba632'
    return tk.Button(b,**kw,highlightthickness=0,activebackground=ffg,relief='groove',fg=ffg,font=(font,si))
def Entry(b,si=11,**kw):
    return tk.Entry(b,**kw,highlightthickness=0,fg=ffg,font=(font,si))
def Radiobutton(b,si=11,**kw):
    return tk.Radiobutton(b,**kw,highlightthickness=0,fg=ffg,font=(font,si),relief='flat')
class main_ui:
    def __init__(self):
        self.tmpa,self.tmpb,self.tmpc=0,0,0
        self.w=tk.Tk()
        self.createui()
        self.tmpp0=1
        self.mouse=0
        self.cc=ffg
    def mousep(self,e=None):
        if self.mouse>0 or e:
            self.mouse=0
            self.m1.set('移动窗口')
            return
        else:self.mouse+=1
        self.x = self.w.winfo_pointerx()-self.w.winfo_rootx()
        self.y = self.w.winfo_pointery()-self.w.winfo_rooty()
        self.m1.set('取消移动')
        th.Thread(target=self.movew).start()
    def movew(self):
        while self.mouse:
           self.w.geometry(f'+{self.w.winfo_pointerx()-self.x}+{self.w.winfo_pointery()-self.y}')
           sleep(0.000000000000001)
    def exit(self):
        '''bk=mess.askyesno('退出程序','确认关闭吗?')
        if bk==False:return'''
        os._exit(0)
    def iconify(self):
        self.w.state('withdrawn')
        if self.tmpp0:
            mess.showinfo('MhLauncher','已最小化,单击屏幕左上角按钮恢复窗口')
            self.tmpp0-=1
    def zhiding(self):
        while 1:
            if self.zd.get():self.w.attributes('-topmost',1)
            #else:self.w.attributes('-topmost',0)
            self.w1.attributes('-topmost','true')
            sleep(0.05)
    def resetui(self):
        self.w.state('normal')
        self.w.attributes('-topmost',1)
    def createui(self):
        ttk.Style().configure('TNotebook.Tab',font=(font,11),foreground=ffg)
        self.w.title('MhLauncher')
        self.w.overrideredirect(True)
        self.w.resizable(0, 0)
        self.w1=tk.Toplevel(self.w)
        self.w1.resizable(0, 0)
        self.w1.overrideredirect(True)
        self.w.attributes('-topmost',1)
        self.w1.geometry(f'+0+0')
        Button(self.w1,text='MhLauncher',bd=0,command=self.resetui).pack()
        title=tk.Frame(self.w)
        Label(title,text=f'MhLauncher {version}',si=13).pack()
        title.grid(row=0,column=0,sticky='w',pady=5,padx=5)
        self.m1=tk.StringVar()
        self.m1.set('移动窗口')
        Button(self.w,textvariable=self.m1,command=self.mousep,si=10).grid(row=0,column=0,padx=5)
        self.w.bind('<Escape>',self.mousep)
        closew=tk.Frame(self.w)
        Button(closew,text='-',bd=0,command=self.iconify).grid(row=0,column=0,padx=10)
        Button(closew,text='x',bd=0,command=self.exit).grid(row=0,column=1,padx=10)
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
        ########,activebackground='#fba632',relief='groove',bg='#ff9300'
        frml=tk.Frame(self.gm)
        Label(frml,text='版本列表').pack()
        vs0=tk.Scrollbar(frml,orient='vertical')
        vs0.pack(side='right',fill='y')
        self.vers=Listbox(frml,width=50,height=10,yscrollcommand=vs0.set)
        self.vers.pack(side='left')
        vs0.config(command=self.vers.yview)
        frml.grid(column=0,row=0,rowspan=2,padx=10,pady=5)
        frmne=tk.Frame(self.gm)
        frmnee=tk.Frame(frmne)
        Label(frmnee,text='游戏名').pack(side='left',padx=2,pady=5)
        #Button(frmnee,text='正版登录').pack(side='left',padx=2,pady=5)
        frmnee.pack(padx=2,pady=5,anchor='center')
        self.usbox=Entry(frmne)
        self.usbox.bind('<Return>',self.setus)
        self.usbox.pack(side='bottom',anchor='s',padx=2,pady=5)
        frmne.grid(column=1,row=0,padx=10,pady=5)
        #获取输入的游戏名self.usbox.get()
        frmr=tk.Frame(self.gm)
        #self.vers.grid(row=0,column=0,columnspan=3)
        Button(frmr,width=20,text='启动',command=lambda: th.Thread(target=self.runmc).start()).grid(row=0,column=0)
        Button(frmr,width=20,text='删除',command=self.rmmc).grid(row=1,column=0)
        Button(frmr,width=20,text='导出启动脚本',command=lambda: self.runmc(1)).grid(row=2,column=0)
        frmr.grid(column=1,row=1,padx=10,pady=5)
        #下载界面
        frml1=tk.Frame(self.dl)
        Label(frml1,text='版本列表').pack()
        vs1=tk.Scrollbar(frml1,orient='vertical')
        vs1.pack(side='right',fill='y')
        self.dlls=Listbox(frml1,width=50,height=10,yscrollcommand=vs1.set)
        self.dlls.pack(side='left')
        vs1.config(command=self.dlls.yview)
        frml1.grid(row=0,column=0,rowspan=2,padx=10,pady=5)
        frm2=tk.Frame(self.dl)
        self.dltype=tk.StringVar()
        self.dltype.set('release')
        Radiobutton(frm2,text='正式版',variable=self.dltype,value='release',command=self.sxdlls).grid(row=0,column=0,sticky='w')
        Radiobutton(frm2,text='测试版',variable=self.dltype,value='snapshot',command=self.sxdlls).grid(row=1,column=0,sticky='w')
        Radiobutton(frm2,text='远古beta版',variable=self.dltype,value='old_beta',command=self.sxdlls).grid(row=2,column=0,sticky='w')
        Radiobutton(frm2,text='远古alpha版',variable=self.dltype,value='old_alpha',command=self.sxdlls).grid(row=3,column=0,sticky='w')
        Button(frm2,text='下载',command=lambda: th.Thread(target=self.dlmc).start()).grid(row=4,sticky='w')
        frm2.grid(row=0,column=1,padx=10,pady=5)
        #设置页面
        self.mb=tk.IntVar()
        #self.mb.set('1024')
        frm3=tk.Frame(self.sett)
        Label(frm3,text='运行内存(mb) 推荐在1024-4096之间').pack(anchor='w')
        tk.Spinbox(frm3,from_=0,to=32768,increment=1024,textvariable=self.mb).pack(anchor='w')
        frm3.grid(row=0,column=0,sticky='w')
        frm4=tk.Frame(self.sett)
        self.dlth=tk.IntVar()
        Label(frm4,text='下载线程').pack(anchor='w')
        tk.Spinbox(frm4,from_=0,to=512,increment=16,textvariable=self.dlth).pack(anchor='w')
        frm4.grid(row=1,column=0,sticky='w')
        frm5=tk.Frame(self.sett)
        Label(frm5,text='下载源').pack(anchor='w')
        self.bm=tk.IntVar()
        #self.bm.set('0')
        Radiobutton(frm5,text='官方(最新,速度快)',variable=self.bm,value=0).pack(anchor='w')
        Radiobutton(frm5,text='国内(如果官方源下载慢选这个)',variable=self.bm,value=1).pack(anchor='w')
        frm5.grid(row=2,column=0,sticky='w')
        frm6=tk.Frame(self.sett)
        Label(frm6,text='程序启动时检查更新').pack()
        self.checkup=tk.IntVar()
        #self.checkup.set('1')
        Radiobutton(frm6,text='是',variable=self.checkup,value=1).pack(side='left',anchor='w')
        Radiobutton(frm6,text='否',variable=self.checkup,value=0).pack(side='left',anchor='e')
        frm6.grid(row=3,column=0,sticky='w')
        frm7=tk.Frame(self.sett)
        Label(frm7,text='补全文件设置').pack(anchor='w')
        self.bqwj=tk.IntVar()
        Radiobutton(frm7,text='快速',variable=self.bqwj,value=0).pack(side='left',anchor='w')
        Radiobutton(frm7,text='全面',variable=self.bqwj,value=1).pack(side='left',anchor='e')
        frm7.grid(row=0,column=1,padx=15)
        frm8=tk.Frame(self.sett)
        Label(frm8,text='版本隔离').pack(anchor='w')
        self.gl=tk.IntVar()
        Radiobutton(frm8,text='关闭',variable=self.gl,value=0).pack(side='left',anchor='w')
        Radiobutton(frm8,text='开启',variable=self.gl,value=1).pack(side='left',anchor='e')
        frm8.grid(row=1,column=1,padx=15)
        frm9=tk.Frame(self.sett)
        Label(frm9,text='窗口置顶').pack(anchor='w')
        self.zd=tk.IntVar()
        Radiobutton(frm9,text='关闭',variable=self.zd,value=0).pack(side='left',anchor='w')
        Radiobutton(frm9,text='开启',variable=self.zd,value=1).pack(side='left',anchor='e')
        frm9.grid(row=2,column=1,padx=15)
        fra=tk.Frame(self.sett)
        Button(fra,text='选取文字颜色',command=self.cols).pack()
        fra.grid(row=3,column=1,padx=15)
        Button(self.sett,text='保存设置',command=self.saveopt).grid(row=3,column=2,sticky='e')
        #关于
        Label(self.gy,text=f'MhLauncher {version}').pack(anchor='w')
        Label(self.gy,text='(c)Copyright 2025 (炜某晟)_MhwsChina_').pack(anchor='w')
        vs5=tk.Scrollbar(self.gy,orient='vertical')
        vs5.pack(side='left',fill='y')
        self.gxrz=tk.Text(self.gy,width=45,height=8,fg=ffg,font=(font,11),yscrollcommand=vs5.set)
        self.gxrz.insert('end',s3)
        self.gxrz.pack(side='left')
        vs5.config(command=self.gxrz.yview)
        Button(self.gy,text='检查更新',command=lambda: th.Thread(target=check_update,args=(version,'mhl',1)).start()).pack(side='left')
        Button(self.gy,text='查看源代码',command=lambda: webb.open('https://github.com/MhwsChina/MhLauncher')).pack(side='left')
        #fabric界面
        frm10=tk.Frame(self.fb)
        Label(frm10,text='版本列表').pack()
        vs2=tk.Scrollbar(frm10,orient='vertical')
        vs2.pack(side='right',fill='y')
        self.vers1=Listbox(frm10,width=50,height=10,yscrollcommand=vs2.set)
        self.vers1.pack(side='left')
        vs2.config(command=self.vers1.yview)
        frm10.grid(column=0,row=0,padx=10,pady=5,rowspan=2)
        Button(self.fb,text='安装',command=lambda: th.Thread(target=self.fabric).start()).grid(column=1,row=0,padx=10,pady=5)
        frm11=tk.Frame(self.fb)
        self.isfg=tk.IntVar()
        Radiobutton(frm11,text='fabric',variable=self.isfg,value=0).pack()
        Radiobutton(frm11,text='forge',variable=self.isfg,value=1).pack()
        frm11.grid(column=1,row=1,padx=10,pady=5)
        #mod页面
        frm12=tk.Frame(self.modd)
        self.labela=Label(frm12,text='模组列表')
        self.labela.pack()
        vs3=tk.Scrollbar(frm12,orient='vertical')
        vs3.pack(side='right',fill='y')
        self.mods=Listbox(frm12,width=50,height=10,yscrollcommand=vs3.set)
        self.mods.pack(side='left')
        vs3.config(command=self.mods.yview)
        frm12.grid(row=0,column=0,padx=10,pady=5)
        self.ssnum=tk.IntVar()
        frm13=tk.Frame(self.modd)
        Label(frm13,text='搜索数量').pack()
        tk.Spinbox(frm13,from_=1,to=60,textvariable=self.ssnum).pack()
        self.ssnum.set(20)
        Label(frm13,text='排序方法').pack()
        self.pxff=tk.StringVar()
        tk.Spinbox(frm13,textvariable=self.pxff,values=('关联','下载量','(作者)关注数量','发布日期','更新日期')[::-1]).pack()
        self.pxff.set('下载量')
        Label(frm13,text='搜索内容').pack()
        self.sstext=Entry(frm13)
        self.sstext.pack()
        self.buttona=tk.StringVar()
        self.buttona.set('选择')
        Button(frm13,text='搜索',command=self.searchmod).pack()
        Button(frm13,textvariable=self.buttona,command=self.dlmod).pack()
        frm13.grid(row=0,column=1,padx=10,pady=5)
        #工具箱
        frm14=tk.Frame(self.gjbox)
        #进程列表
        Label(frm14,text='进程列表').pack()
        vs4=tk.Scrollbar(frm14,orient='vertical')
        vs4.pack(side='right',fill='y')
        self.tasks=Listbox(frm14,width=50,height=10,yscrollcommand=vs4.set)
        self.tasks.pack(side='left')
        vs4.config(command=self.tasks.yview)
        frm14.grid(row=0,column=0,padx=10,pady=5)
        frm15=tk.Frame(self.gjbox)
        Button(frm15,text='刷新进程列表',command=self.flushtask).grid(column=0,row=0,columnspan=3)
        Button(frm15,text='关闭',command=self.kill).grid(column=0,row=1)
        Button(frm15,text='冻结',command=self.suspend).grid(column=1,row=1)
        Button(frm15,text='解冻',command=self.resume).grid(column=2,row=1)
        Button(frm15,text='关闭并删除',command=self.rmtask).grid(column=0,row=2,columnspan=3)
        Button(frm15,text='删除该进程的文件夹(卸载)',command=lambda: self.rmtask(1)).grid(column=0,row=3,columnspan=3)
        #tk.Button(frm15,text='获取详细信息').pack()
        frm151=tk.Frame(frm15)
        Label(frm151,text='命令执行/进程搜索').pack()
        self.cmdt=Entry(frm151)
        self.cmdt.pack()
        frm151.grid(column=0,row=4,columnspan=4)
        Button(frm15,text='执行',command=lambda: self.cmd(self.cmdt.get())).grid(column=0,row=5)
        Button(frm15,text='搜索',command=lambda: self.flushtask(self.cmdt.get())).grid(column=1,row=5)
        frm15.grid(row=0,column=1,padx=10,pady=5)
        x=int((self.w.winfo_screenwidth()-self.w.winfo_reqwidth())/2)
        y=int((self.w.winfo_screenheight()-self.w.winfo_reqheight())/2)
        self.w.geometry(f'+{x}+{y}')
        #######################
        self.loadopt(opt)
        #anself.listver()
        self.sxdlls()
        self.nt0.grid(row=1,column=0,padx=10,pady=5)
        th.Thread(target=self.zhiding).start()
        th.Thread(target=self.searchmod).start()
        th.Thread(target=self.sxver).start()
        self.flushtask()
        #获取运行内存self.mb.get()
        #获取下载线程self.dlth.get()
        #获取是否国内源self.bm.get()
        #获取检查更新self.checkup.get()
        #是否全面补全文件self.bqwj.get()
        #版本隔离self.gl.get()'''
    def sxver(self):
        while 1:
            self.listver()
            time.sleep(3)
    def cols(self):
        tmp=cc.askcolor()
        if tmp[0]==None:return
        self.cc=tmp[1]
        self.saveopt()
        mess.showinfo('setting','设置颜色成功,需重启程序才能生效!')
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
        slb(Label)
    def saveopt(self):
        opt['thread']=self.dlth.get()
        opt['bm']=self.bm.get()
        opt['check_update']=self.checkup.get()
        opt['bqwj']=self.bqwj.get()
        opt['gl']=self.gl.get()
        opt['mb']=self.mb.get()
        opt['text_color']=self.cc
        upopt(opt)
        mess.showinfo('保存设置','保存成功')
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
        java='java-runtime-gamma'
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
        tmp=mess.askyesno('MhLauncher',f'确认删除{ver}吗?')
        if tmp==False:return
        removemc(ver)
        self.listver()
    def listver(self):
        tmpv=allv()
        if len(tmpv)==self.vers.size():return
        self.vers.delete(0,'end')
        self.vers1.delete(0,'end')
        for i in tmpv:
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
        if not vdc:return
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
            self.labela['text']='mod版本'
            self.tmpc=self.mods.get(self.mods.curselection()[0])
            self.modurls=modurl(self.tmpb,self.tmpc)
            self.mods.delete(0,'end')
            for i in self.modurls:
                self.mods.insert('end',i['version'])
            return
        if self.tmpa==2:
            if not self.mods.curselection():
                mess.showinfo('提示','没有选择mod版本');return
            self.tmpa=3
            self.labela['text']='mod加载器'
            self.buttona.set('下载')
            self.tmodver=self.mods.get(self.mods.curselection()[0])
            modloader=[]
            for i in self.modurls:
                if i['version']==self.tmodver:
                    for i in i['loaders']:
                        if not i in modloader:
                            modloader.append(i)
            self.mods.delete(0,'end')
            for i in modloader:
                self.mods.insert('end',i)
            return
        if self.tmpa==3:
            if not self.mods.curselection():
                mess.showinfo('提示','没有选择mod加载器');return
            loader=self.mods.get(self.mods.curselection()[0])
            for i in self.modurls:
                if i['version']==self.tmodver and loader in i['loaders']:
                    f=i['files'][0]
                    fp=filedialog.asksaveasfilename(title='下载mod',initialfile=f[1])
                    if not fp:return
                    dnld(f[0],fp)
                    break
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
    def flushtask(self,search=False):
        if search:self.tt=sorted(self.srchtask(search),key=lambda a:a[1])
        else:self.tt=sorted(self.getalltask(),key=lambda a:a[1])
        self.tasks.delete(0,'end')
        for i in self.tt:
            self.tasks.insert('end','pid='+str(i[0])+'   '+str(i[1]))
    def srchtask(self,t):
        ts=[]
        t=t.lower()
        for i in psutil.process_iter():
            n=i.name().lower()
            if n==t or t in n or n in t:
                ts.append((i.pid,i.name()))
        return ts
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
    def suspend(self):
        if not self.tasks.curselection():return
        nm=self.tt[self.tasks.curselection()[0]][1]
        for i in self.getpid(nm):
            try:psutil.Process(i).suspend()
            except:pass
            sleep(0.5)
    def resume(self):
        if not self.tasks.curselection():return
        nm=self.tt[self.tasks.curselection()[0]][1]
        for i in self.getpid(nm):
            try:psutil.Process(i).resume()
            except:pass
            sleep(0.5)
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
