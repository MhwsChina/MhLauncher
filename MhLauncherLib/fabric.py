import re
from .xcdl import *
import subprocess as sub
import os,zipfile,platform,tempfile
from json import loads
import requests as req
from random import randint
def rdt():
    return 'temp-'+str(randint(1,10000000000000))
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
    path=pj(p,f'instfabric{rdt()}.jar')
    dnld(url,path)
    cmd=[java,'-jar',path,'client','-dir',d,'-mcversion',ver,'-loader',lv,'-noprofile','-snapshot']
    sub.call(cmd)
    os.remove(path)
def get_library_path(name, path):
    libpath = os.path.join(path, "libraries")
    parts = name.split(":")
    base_path, libname, version = parts[0:3]
    for i in base_path.split("."):
        libpath = os.path.join(libpath, i)
    try:
        version, fileend = version.split("@")
    except ValueError:
        fileend = "jar"
    filename = f"{libname}-{version}{''.join(map(lambda p: f'-{p}', parts[3:]))}.{fileend}"
    libpath = os.path.join(libpath, libname, version, filename)
    return libpath
def empty(arg):
    pass
def get_jar_mainclass(path):
    zf = zipfile.ZipFile(path)
    with zf.open("META-INF/MANIFEST.MF") as f:
        lines = f.read().decode("utf-8").splitlines()
    zf.close()
    content = {}
    for i in lines:
        try:
            key, value = i.split(":")
            content[key] = value[1:]
        except Exception:
            pass
    return content["Main-Class"]
def get_classpath_separator():
    if platform.system() == "Windows":
        return ";"
    else:
        return ":"
def forge_processors(data,minecraft_directory,lzma_path,installer_path,java,callback):
    path = str(minecraft_directory)
    argument_vars = {"{MINECRAFT_JAR}": os.path.join(path, "versions", data["minecraft"], data["minecraft"] + ".jar")}
    for data_key, data_value in data["data"].items():
        if data_value["client"].startswith("[") and data_value["client"].endswith("]"):
            argument_vars["{" + data_key + "}"] = get_library_path(data_value["client"][1:-1], path)
        else:
            argument_vars["{" + data_key + "}"] = data_value["client"]
    with tempfile.TemporaryDirectory() as root_path:
        argument_vars["{INSTALLER}"] = installer_path
        argument_vars["{BINPATCH}"] = lzma_path
        argument_vars["{ROOT}"] = root_path
        argument_vars["{SIDE}"] = "client"
        classpath_seperator = get_classpath_separator()
        callback.get("setMax", empty)(len(data["processors"]))
        for count, i in enumerate(data["processors"]):
            if "client" not in i.get("sides", ["client"]):
                # Skip server side only processors
                continue
            callback.get("setStatus", empty)("Running processor " + i["jar"])
            # Get the classpath
            classpath = ""
            for c in i["classpath"]:
                classpath = classpath + get_library_path(c, path) + classpath_seperator
            classpath = classpath + get_library_path(i["jar"], path)
            mainclass = get_jar_mainclass(get_library_path(i["jar"], path))
            command = [java, "-cp", classpath, mainclass]
            for c in i["args"]:
                var = argument_vars.get(c, c)
                if var.startswith("[") and var.endswith("]"):
                    command.append(get_library_path(var[1:-1], path))
                else:
                    command.append(var)
            for argument_key, argument_value in argument_vars.items():
                for pos in range(len(command)):
                    command[pos] = command[pos].replace(argument_key, argument_value)
            sub.run(command)
            callback.get("setProgress", empty)(count)

def listforge():
    url="https://files.minecraftforge.net/maven/net/minecraftforge/forge/maven-metadata.xml"
    return parse_maven_metadata(url)['versions']
def getlatestforge(ver):
    verls=listforge()
    for i in verls:
        if i.split('-')[0]==ver:return i
    raise RuntimeError('版本不存在!')
def forge(v,java,p='.minecraft',d='.minecraft'):
    ver=getlatestforge(v)
    url=f"https://files.minecraftforge.net/maven/net/minecraftforge/forge/{ver}/forge-{ver}-installer.jar"
    path=pj(p,f'instforge{rdt()}.jar')
    dnld(url,path)
    zf=zipfile.ZipFile(path,"r")
    with zf.open("install_profile.json","r") as f:
        c=f.read()
    data=loads(c)
    ff=data['version']
    extract(zf,'version.json',pj(d,'versions',ff,f'{ff}.json'))
    lmza_path=pj(p,f'client{rdt()}.lzma')
    try:extract(zf,'data/client.lzma',lmza_path)
    except:pass
    forge_processors(data,d,lmza_path,path,java,{})
    zf.close()
    os.remove(path)
    os.remove(lmza_path)
