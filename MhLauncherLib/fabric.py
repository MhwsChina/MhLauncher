import re
from .xcdl import *
import subprocess as sub
import os,zipfile
from json import loads
import requests as req
def extract(zf,zp,ep):
    try:
        os.makedirs(os.path.dirname(ep))
    except:pass
    with zf.open(zp,'r') as f:
        with open(ep,'wb') as f1:
            f1.write(f.read())
def pj(*args):
    return os.path.join(*args).replace('\\','/')
def parse_maven_metadata(url: str):
    r = req.get(url)
    data = {}
    data["release"] = re.search("(?<=<release>).*?(?=</release>)", r.text, re.MULTILINE).group()
    data["latest"] = re.search("(?<=<latest>).*?(?=</latest>)", r.text, re.MULTILINE).group()
    data["versions"] = re.findall("(?<=<version>).*?(?=</version>)", r.text, re.MULTILINE)
    return data
def get_latest_installer_version():
    FABRIC_INSTALLER_MAVEN_URL = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/maven-metadata.xml"
    return parse_maven_metadata(FABRIC_INSTALLER_MAVEN_URL)["latest"]
def get_all_loader_versions():
    FABRIC_LOADER_VERSIONS_URL = "https://meta.fabricmc.net/v2/versions/loader"
    return req.get(FABRIC_LOADER_VERSIONS_URL).json()
def get_latest_loader_version():
    loader_versions = get_all_loader_versions()
    return loader_versions[0]["version"]
def fabric(ver,java,p='.minecraft',d='.minecraft'):
    fb=get_latest_installer_version()
    lv=get_latest_loader_version()
    url=f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{fb}/fabric-installer-{fb}.jar"
    path=p+'/instfabric.jar'
    dnld(url,path)
    cmd=[java,'-jar',path,'client','-dir',d,'-mcversion',ver,'-loader',lv,'-noprofile','-snapshot']
    sub.call(cmd)
    os.remove(path)
def listforge():
    url="https://files.minecraftforge.net/maven/net/minecraftforge/forge/maven-metadata.xml"
    return parse_maven_metadata(url)['versions']
def getlatestforge(ver):
    verls=listforge()
    for i in verls:
        if i.split('-')[0]==ver:return i
    raise RuntimeError('版本不存在!')
def forge(v,p='.minecraft',d='.minecraft'):
    ver=getlatestforge(v)
    url=f"https://files.minecraftforge.net/maven/net/minecraftforge/forge/{ver}/forge-{ver}-installer.jar"
    path=p+'/instforge.jar'
    dnld(url,path)
    zf=zipfile.ZipFile(path,"r")
    with zf.open("install_profile.json","r") as f:
        c=f.read()
    ff=loads(c)['version']
    extract(zf,'version.json',pj(d,'versions',ff,f'{ff}.json'))
    zf.close()
