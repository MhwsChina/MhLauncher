import minecraft_launcher_lib as mclib
from .xcdl import *
import subprocess as sub
import os
from json import loads
def install(ver,d='.minecarft',java=None):
    fb=mclib.fabric.get_latest_installer_version()
    lv=mclib.fabric.get_latest_loader_version()
    if java:
        url=f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{installer_version}/fabric-installer-{installer_version}.jar"
        path='.minecraft/instfabric.jar'
    else:
        url=f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{installer_version}/fabric-installer-{installer_version}.exe"
        path='.minecraft/instfabric.exe'
    onednld(url,path,r=rtor)
    if java:sub.call([java,'-jar',path,'client','-dir',d,'-mcversion',ver,'-loader',lv,'-noprofile','-snapshot'])
    else:sub.call([path,'client','-dir',d,'-mcversion',ver,'-loader',lv,'-noprofile','-snapshot'])
    os.remove(path)
    f=d+'/'+
    pth=os.path.join(d,f)
    vd=open(f'{pth}/{f}.json','r')
    vdc=loads(vd.read())
    vd.close()
