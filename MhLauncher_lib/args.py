from .log import *
import os,platform,re
from json import loads
def pj(*args):
    return os.path.join(*args).replace('\\','/')
def readv(ver,d='.minecraft'):
    with open(pj(d,'versions/'+ver+'/'+ver+'.json'),'r') as f:
        return loads(f.read())
def get_os_version() -> str:
    if platform.system() == "Windows":
        ver = sys.getwindowsversion()
        return f"{ver.major}.{ver.minor}"
    elif platform.system == "Darwin":
        return ""
    else:
        return platform.uname().release
def parseo(rule):
    if rule["action"] == "allow":returnvalue = False
    elif rule["action"] == "disallow":returnvalue = True
    for os_key, os_value in rule.get("os", {}).items():
        if os_key == "name":
            if os_value == "windows" and platform.system() != 'Windows':
                return returnvalue
            elif os_value == "osx" and platform.system() != 'Darwin':
                return returnvalue
            elif os_value == "linux" and platform.system() != 'Linux':
                return returnvalue
        elif os_key == "arch":
            if os_value == "x86" and platform.architecture()[0] != "32bit":
                return returnvalue
        elif os_key == "version":
            if not re.match(os_value, get_os_version()):
                return returnvalue
    return not returnvalue
def parsel(rules):
    for i in rules:
        if not parseo(i):
            return False
    return True
def getcp(ver,d='.minecraft',cl=True):
    if platform.system()=='Windows':fg=';'
    else:fg=':'
    v=readv(ver,d)
    classpath=''
    if 'inheritsFrom' in v:
        classpath+=getcp(v['inheritsFrom'],d,False)
        ver=v['inheritsFrom']
    for c in v['libraries']:
        p=False
        if 'rules' in c and not parsel(c['rules']):continue
        tags=c['name'].split(':')
        if len(tags)==3:
            p,n,vs=tags
            p=p.replace('.','/')
            f=f'{p}/{n}/{vs}/{n}-{vs}.jar'
            path=pj(d,f'libraries/{f}')
        elif len(tags)==4:
            p,n,vs,xt=tags
            p=p.replace('.','/')
            f=f'{p}/{n}/{vs}/{n}-{vs}-{xt}.jar'
            path=pj(d,f'libraries/{f}')
        else:continue
        classpath+=path+fg
    if cl:classpath+=pj(d,'versions',ver,ver+'.jar')
    return classpath
def fmarg(txt,ver,classpath,v,opt,d='.minecraft'):
    if 'assets' in v:
        txt=txt.replace('${natives_directory}',pj(d,f'versions/{ver}/natives'))\
             .replace('${launcher_name}','MhLauncher')\
             .replace('${launcher_version}','114514.0.0')\
             .replace('${classpath}',classpath)\
             .replace('${auth_player_name}',opt['username'])\
             .replace('${version_name}',ver)\
             .replace('${game_directory}',d)\
             .replace('${assets_root}',pj(d,'assets'))\
             .replace('${assets_index_name}',v['assets'])\
             .replace('${auth_uuid}',opt['uuid'])\
             .replace('${auth_access_token}',opt['token'])\
             .replace('${user_type}','msa')\
             .replace('${version_type}','MhLauncher')\
             .replace('${user_properties}','{}')\
             .replace('${resolution_width}','854')\
             .replace('${resolution_height}','480')\
             .replace('${game_assets}',pj(d,"assets/virtual/legacy"))\
             .replace('${auth_session}',opt['token'])\
             .replace('${library_directory}',pj(d,'libraries'))     
             #.replace('${quickPlayPath}',opt['quickplaypath'])\
             #.replace('${quickPlaySingleplayer}',opt['quickplaysingleplayer'])\
             #.replace('${quickPlayMultiplayer}',opt['quickplaymultiplayer'])\
             #.replace('${quickPlayRealms}',opy['quickplayrealms'])
    else:
        txt=txt.replace('${natives_directory}',pj(d,f'versions/{ver}/natives'))\
             .replace('${launcher_name}','MhLauncher')\
             .replace('${launcher_version}','114514.0.0')\
             .replace('${classpath}',classpath)\
             .replace('${auth_player_name}',opt['username'])\
             .replace('${version_name}',ver)\
             .replace('${game_directory}',d)\
             .replace('${auth_uuid}',opt['uuid'])\
             .replace('${auth_access_token}',opt['token'])\
             .replace('${user_type}','msa')\
             .replace('${version_type}','MhLauncher')\
             .replace('${user_properties}','{}')\
             .replace('${resolution_width}','854')\
             .replace('${resolution_height}','480')\
             .replace('${game_assets}',pj(d,"assets/virtual/legacy"))\
             .replace('${auth_session}',opt['token'])\
             .replace('${library_directory}',pj(d,'libraries'))
    return txt
def getjvm(v,ver,classpath,opt,d):
    args=[]
    if 'inheritsFrom' in v:
        args=args+getjvm(readv(v['inheritsFrom'],d),ver,classpath,opt,d)
    elif 'arguments' in v:
        if 'jvm' in v['arguments']:
            for i in v['arguments']['jvm']:
                if type(i)==str:
                    args.append(fmarg(i,ver,classpath,v,opt,d))
                else:
                    if 'rules' in i and not parsel(i['rules']):continue
                    args.append(i['value'])
    elif 'jvmArguments' in v:
        args=args+v['jvmArguments']
    else:
        args.append('-Djava.library.path='+pj(d,f'versions/{ver}/natives'))
    if 'minecraftArguments' in v:
        args.append('-cp')
        args.append(classpath)
    return args
def getgame(v,ver,classpath,opt,d):
    args=[]
    if 'inheritsFrom' in v:
        return getgame(readv(v['inheritsFrom'],d),ver,classpath,opt,d)
    if 'arguments' in v:
        if 'game' in v['arguments']:
            for i in v['arguments']['game']:
               if type(i)==str:
                   args.append(fmarg(i,ver,classpath,v,opt,d))
    if 'minecraftArguments' in v:
        args=args+fmarg(v['minecraftArguments'],ver,classpath,v,opt,d).split()
    return args
def getmcargs(ver,java,opt,marg=[],d='.minecraft'):
    v=readv(ver,d)
    args=[java,'-XX:+UseG1GC','-XX:-UseAdaptiveSizePolicy','-XX:-OmitStackTraceInFastThrow']
    if marg:args=args+marg
    classpath=getcp(ver,d=d)
    args=args+getjvm(v,ver,classpath,opt,d)
    args.append(v['mainClass'])
    args=args+getgame(v,ver,classpath,opt,d)
    return args
