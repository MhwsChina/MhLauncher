from MhLauncher_lib import *
import os,sys
import webbrowser as wb
from json import dumps,loads
def getuuid(username):
    if exists('.minecraft/usercache.json'):
        with open('.minecraft/usercache.json') as f:
            v=loads(f.read())
            for i in v:
                if i['name']==username:return i['uuid']
    return '00000FFFFFFFFFFFFFFFFFFFFFFE5CC6'
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
    ch=['opt','thread','check_update','bqwj']
    ck=[0,128,1,0]
    for i in range(len(ch)):
        c,k=ch[i],ck[i]
        if not c in dic:
            if c=='opt':
                dic['opt']={}
                dic['opt']['username']=input('请输入游戏名:')
                dic['opt']['uuid']=getuuid(dic['opt']['username'])
                dic['opt']['token']='00000FFFFFFFFFFFFFFFFFFFFFFE5CC6'
            else: dic[c]=k
    return dic
def upopt(opt):
    with open('mhl/options.json','w') as f:
        f.write(dumps(opt))
def qidong(out=None):
    v=allv()
    if v==[]:print('没有可用版本,请先下载');pause();return
    j=0
    for i in v:
        print(j,i)
        j+=1
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
                downjava(j,'./mhl/java','./mhl')
                java=fjava(ls=['mhl/java'],t=1)[j]
            else:return
        if out:runmc(v[n],vdc,java,o=opt['opt'],out=v[n]+'.bat',bqthread=opt['thread'],sha=opt['bqwj'])
        else:runmc(v[n],vdc,java,o=opt['opt'],bqthread=opt['thread'],sha=opt['bqwj'])
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

'''[1:-1],'v0.0.6'
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
4.自动安装java
5.自动检查更新设置
6.查看本程序源代码(github)
7.查看本程序协议
8.设置游戏运行内存
9.补全文件设置
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
    except:raise;print('失败')
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
            try:downloadmc(ver,vdc,thread=opt['thread'])
            except:print('下载失败');pause()
        if b=='3':
            print('1.正式版\n2.测试版\n3.远古alpha版\n4.远古beta版')
            c=input('选择序号:')
            if c=='1':t='release'
            if c=='2':t='snapshot'
            if c=='3':t='old_alpha'
            if c=='4':t='old_beta'
            for i in ov(vdc,t):print(i['id'])
            pause()
            continue
        if b=='2':
            try:downloadmc(ov(vdc,'snapshot',1),vdc,thread=opt['thread'])
            except:print('下载失败');pause()
        if b=='1':
            try:downloadmc(ov(vdc,'release',1),vdc,thread=opt['thread'])
            except:print('下载失败');pause()
    if a=='3':qidong(True)
    if a=='4':rmmc()
    if a=='0':
        print(s2)
        b=input('选择序号:')
        if b=='1':
            opt['opt']['username']=input('请输入游戏名:');upopt(opt)
        if b=='2':
            opt['thread']=input('请输入线程数(默认128)',typ=int);upopt(opt)
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
            c=input('请输入Java版本(8/16/17/21)(输入-1返回):',['8','16','17','21','-1'])
            if c=='-1':continue
            downjava(c,'./mhl/java','./mhl')
        if b=='5':
            print('是否在程序启动时检查更新?')
            c=input('(输入y表示是,输入n表示否)',['n','y'])
            if c=='y':opt['check_update']=1
            else:opt['check_update']=0
            upopt(opt)
        if b=='6':
            wb.open('https://github.com/MhwsChina/MhLauncher')
        if b=='9':
            c=input('1.快速模式(但不全面)/2.全面模式(但不快速)/3.返回',['1','2','3'])
            if c=='1':opt['bqwj']=0
            if c=='2':opt['bqwj']=1
            upopt(opt)
        if b=='-2':
            print(s3)
            pause()
        if b=='7':
            show_license()
            pause()
        if b=='8':
            opt['opt']=setmem(opt['opt'])
            upopt(opt)
