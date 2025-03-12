from MhLauncherLib import *
import os,sys,uuid
import webbrowser as wb
from json import dumps,loads
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
    ch=['opt','thread','check_update','bqwj','dlout','marg','outlog','bm']
    ck=[0,256,1,0,0,[],0,0]
    for i in range(len(ch)):
        c,k=ch[i],ck[i]
        if not c in dic:
            if c=='opt':
                dic['opt']={}
                dic['opt']['username']=input('请输入游戏名:')
                dic['opt']['uuid']=getuuid(dic['opt']['username'])
                dic['opt']['token']=dic['opt']['uuid']
            else: dic[c]=k
    return dic
def upopt(opt):
    with open('mhl/options.json','w') as f:
        f.write(dumps(opt))
def qidong(out=None):
    v=allv()
    if v==[]:print('没有可用版本,请先下载');pause();return
    j=0
    listprint(v,['序号','版本'])
    if out:
        try:n=int(input('输入要生成的序号'))
        except:return
    else:
        try:n=int(input('输入要启动的序号'))
        except:return
    try:v[n]=v[n]
    except:print('输入有误');pause();return
    if isv(v[n]):
        j=mcjava(v[n],vdc)
        try:java=fjava(ls=['mhl/java'],t=1)[j]
        except:
            print('未找到java\n1.手动导入\n2.自动下载')
            sa=input('选择序号:')
            if sa=='1':
                java=input(f'java{j}文件夹路径:')
                if isjavaf(java,'javaw.exe'):
                    opt[v]=pth
                    upopt(opt)
                    java=opt['java'][j]
                else:
                    print('无效的java')
                    pause()
                    return
            elif sa=='2':
                downjava(mcjava(v[n],vdc,m=False),'./mhl/java',opt['thread'])
                java=fjava(ls=['mhl/java'],t=1)[j]
            else:return
        if out:runmc(v[n],vdc,java,opt['opt'],opt['thread'],opt['bqwj'],opt['dlout'],opt['marg'],opt['outlog'],v[n]+'.bat')
        else:runmc(v[n],vdc,java,opt['opt'],opt['thread'],opt['bqwj'],opt['dlout'],opt['marg'],opt['outlog'])
def rmmc():
    v=allv()
    if v==[]:print('没有可删除版本');pause();return
    j=0
    for i in v:
        print(j,i)
        j+=1
    try:n=int(input('输入要删除的序号'))
    except:print('输入有误');pause();return
    try:n=v[n]
    except:print('输入有误');pause();return
    n1=input(f'确定删除{n}?(y/n)')
    if n1=='y':removemc(n,vdc)
    else:print('已取消操作')
    pause()
welc,version='''
  __  __ _     _                           _               
 |  \/  | |__ | |    __ _ _   _ _ __   ___| |__   ___ _ __ 
 | |\/| | '_ \| |   / _` | | | | '_ \ / __| '_ \ / _ \ '__|
 | |  | | | | | |__| (_| | |_| | | | | (__| | | |  __/ |   
 |_|  |_|_| |_|_____\__,_|\__,_|_| |_|\___|_| |_|\___|_|

'''[1:-1],'v0.0.18'
s='''
1.下载游戏
2.启动游戏
3.导出启动脚本
4.删除游戏
0.设置
'''[1:-1]
s1='''
1.最新正式版
2.最新测试版
3.查看版本列表
4.自定义版本
-1.返回
'''[1:-1]
s2='''
1.设置游戏名
2.设置下载线程
3.自定义皮肤
4.自动检查更新设置
5.查看本程序源代码(github)
6.查看本程序协议
7.设置游戏运行内存
8.补全文件设置
9.多线程下载输出设置
10.游戏日志输出设置
11.设置下载源
-1.返回
-2.查看更新日志
'''[1:-1]
s3='''
=======更新日志=======
源码:https://github.com/MhwsChina/MhLauncher
v0.0.1
支持启动mc,下载mc
v0.0.2
优化多线程下载
自定义皮肤
自动安装java
优化导出启动脚本
v0.0.3
解决无法在无网络下启动mc的问题
增加自动更新
v0.0.4
支持查看协议
优化兼容性
补全文件更加快速
优化自动更新
v0.0.5
修复了一些bug
增添自定义游戏运行内存功能
v0.0.6
优化自动更新
补全文件更新
v0.0.7
优化多线程下载
v0.0.8
支持启动fabric,forge
重构,重写启动游戏代码(花了好长时间)
重写导出启动脚本代码
不再需要minecraft-launcher-lib
优化检测java代码
v0.0.9
多线程下载修复了一个bug
v0.0.10
修复了一些bug
v0.0.11
修复了很多bug
v0.0.12
优化下载mc
v0.0.13
加入bmclapi下载源
v0.0.14
下载更加迅速
v0.0.15
紧急修复一些bug
v0.0.16
修复了一些bug
v0.0.17
修复了一些bug
v0.0.18
支持windows,macos,linux等各种系统
只要能装python就能启动
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
    try:check_update(version,'mhl')
    except:print('失败')
while True:
    if not exists('.minecraft'):os.mkdir('.minecraft')
    clear()
    print(welc)
    print('MhLauncher mc启动器',version)
    print('Auther:(炜某晟)_MhwsChina_ 禁止盗版')
    print(s)
    a=input('选择序号:')
    #downloadmc('1.8.9',vdc)
    #runmc('1.20.1',vdc,r'F:\mc\mcjava\Java\jdk17\bin\javaw.exe',out='1.bat') 691692
    if a=='2':qidong()
    if a=='1':
        print(s1)
        b=input('选择序号:')
        if b=='4':
            ver=input('游戏版本:')
            if ver=='':continue
            try:downloadmc(ver,vdc,opt['thread'],opt['dlout'],bm=opt['bm'])
            except:raise;print('下载失败');pause()
        if b=='3':
            printvdc(vdc)
        if b=='2':
            try:downloadmc(ov(vdc,'snapshot',1),vdc,opt['thread'],opt['dlout'],bm=opt['bm'])
            except:print('下载失败');pause()
        if b=='1':
            try:downloadmc(ov(vdc,'release',1),vdc,opt['thread'],opt['dlout'],bm=opt['bm'])
            except:print('下载失败');pause()
    if a=='3':qidong(True)
    if a=='4':rmmc()
    if a=='0':
        print(s2)
        b=input('选择序号:')
        if b=='1':
            opt['opt']['username']=input('请输入游戏名:');upopt(opt)
        if b=='2':
            opt['thread']=input('请输入线程数(默认256,推荐128-512之间最佳)',typ=int);upopt(opt)
        if b=='3':
            print('[温馨提示]: 皮肤功能暂未测试,可能无法使用')
            url=input('皮肤网址(输-1返回):')
            if url=='-1':continue
            typ=input('皮肤类型:(steve/alex)',['steve','alex']).upper()
            ssk={'skins':[{
                'id':'nul',
                'state':'ACTIVE',
                'url':url,
                'variant':'CLASSIC',
                'alias':typ
                }]}
            opt['opt']=opt['opt'].update(ssk)
            upopt(opt)
        if b=='4':
            print('是否在程序启动时检查更新?')
            c=input('(输入y表示是,输入n表示否,默认为是)',['n','y'])
            if c=='y':opt['check_update']=1
            else:opt['check_update']=0
            upopt(opt)
        if b=='5':
            wb.open('https://github.com/MhwsChina/MhLauncher')
        if b=='8':
            c=input('1.快速模式(但不全面)(默认)/2.全面模式(但不快速)/3.返回',['1','2','3'])
            if c=='1':opt['bqwj']=0
            if c=='2':opt['bqwj']=1
            upopt(opt)
        if b=='9':
            print('是否在下载时显示下载的文件?')
            c=input('(输入y表示是,输入n表示否,默认为否)',['n','y'])
            if c=='y':opt['dlout']=1
            else:opt['dlout']=0
            upopt(opt)
        if b=='10':
            print('是否在游戏运行时输出日志?')
            c=input('(输入y表示是,输入n表示否,默认为否)',['n','y'])
            if c=='y':opt['outlog']=1
            else:opt['outlog']=0
            upopt(opt)
        if b=='11':
            print('选择下载源:\n1.官方源(速度慢,但是最新)\n2.国内源(速度快,但不是最新)(默认)')
            c=input('请选择序号:')
            if c=='1':opt['bm']=0
            else:opt['bm']=1
            upopt(opt)
        if b=='-2':
            print(s3)
            pause()
        if b=='6':
            show_license()
            pause()
        if b=='7':
            opt['marg']=setmem()
            upopt(opt)
