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
def getfg():
    if platform.system()=='Windows':
        return ';'
    else:return ':'
def fmcp(cp,rn=False):
    cp=cp.split(':')
    cp[0]=cp[0].replace('.','/')
    cp[2]=f'{cp[2]}/{cp[1]}-{cp[2]}'
    if len(cp)==4:
        cp[2]+=f'-{cp[3]}'
        del cp[3]
    cp[2]+='.jar'
    if rn:return ('/'.join(cp),cp[1])
    return '/'.join(cp)
def getcp(ver,d='.minecraft',cl=True):
    fg=getfg()
    v=readv(ver,d)
    cps,ns=[],[]
    for c in v['libraries']:
        if 'rules' in c and not parsel(c['rules']):continue
        f,n=fmcp(c['name'],1)
        cps.append(pj(d,'libraries',f))
        ns.append(n)
    if 'inheritsFrom' in v:
        cps1=[]
        for f,n in getcp(v['inheritsFrom'],d,False):
            if not n in ns:
                cps1.append(f)
        cps=cps1+cps
        veri=v['inheritsFrom']
    else:veri=ver
    if cl:
        if v['mainClass']=='cpw.mods.bootstraplauncher.BootstrapLauncher':
            cps.append(pj(d,'versions',ver,ver+'.jar'))
        else:
            cps.append(pj(d,'versions',veri,veri+'.jar'))
        return fg.join(cps)
    else:return list(zip(cps,ns))
def fmarg(txt,ver,classpath,v,opt,gmdir,d='.minecraft',fg=getfg()):
    if 'assets' in v:
        txt=txt.replace('${natives_directory}',pj(d,f'versions/{ver}/{ver}-natives'))\
             .replace('${launcher_name}','MhLauncher')\
             .replace('${launcher_version}','114514.0.0')\
             .replace('${classpath}',classpath)\
             .replace('${auth_player_name}',opt['username'])\
             .replace('${version_name}',ver)\
             .replace('${game_directory}',gmdir)\
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
             .replace('${library_directory}',pj(d,'libraries'))\
             .replace('${classpath_separator}',fg)
             #.replace('${quickPlayPath}',opt['quickplaypath'])\
             #.replace('${quickPlaySingleplayer}',opt['quickplaysingleplayer'])\
             #.replace('${quickPlayMultiplayer}',opt['quickplaymultiplayer'])\
             #.replace('${quickPlayRealms}',opy['quickplayrealms'])
    else:
        txt=txt.replace('${natives_directory}',pj(d,f'versions/{ver}/{ver}-natives'))\
             .replace('${launcher_name}','MhLauncher')\
             .replace('${launcher_version}','114514.0.0')\
             .replace('${classpath}',classpath)\
             .replace('${auth_player_name}',opt['username'])\
             .replace('${version_name}',ver)\
             .replace('${game_directory}',gmdir)\
             .replace('${auth_uuid}',opt['uuid'])\
             .replace('${auth_access_token}',opt['token'])\
             .replace('${user_type}','msa')\
             .replace('${version_type}','MhLauncher')\
             .replace('${user_properties}','{}')\
             .replace('${resolution_width}','854')\
             .replace('${resolution_height}','480')\
             .replace('${game_assets}',pj(d,"assets/virtual/legacy"))\
             .replace('${auth_session}',opt['token'])\
             .replace('${library_directory}',pj(d,'libraries'))\
             .replace('${classpath_separator}',fg)
    return txt
def getjvm(v,ver,classpath,opt,d,gmdir):
    fg=getfg()
    args=[]
    yh='-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump'
    if 'inheritsFrom' in v:
        args=args+getjvm(readv(v['inheritsFrom'],d),v['inheritsFrom'],classpath,opt,d,gmdir)
    if 'arguments' in v:
        if 'jvm' in v['arguments']:
            for i in v['arguments']['jvm']:
                if type(i)==str:
                    args.append(fmarg(i,ver,classpath,v,opt,gmdir,d,fg))
                else:
                    if 'rules' in i and not parsel(i['rules']):continue
                    value=i['value']
                    if type(value)==list:
                        for ii in value: 
                            args.append(ii)
                    else:
                        args.append(value)
    if 'jvmArguments' in v:
        args=args+v['jvmArguments']
    if not 'jvmArguments' in v and not 'arguments' in v:
        args.append('-Djava.library.path='+pj(d,f'versions/{ver}/{ver}-natives'))
    if 'minecraftArguments' in v:
        if platform.system()=='Windows' and not yh in args:
            args.append(yh)
        args.append('-cp')
        args.append(classpath)
    return args
def getgame(v,ver,classpath,opt,d,gmdir):
    fg=getfg()
    args=[]
    if 'inheritsFrom' in v and not 'minecraftArguments' in v:
        args=args+getgame(readv(v['inheritsFrom'],d),v['inheritsFrom'],classpath,opt,d,gmdir)
    if 'arguments' in v:
        if 'game' in v['arguments']:
            for i in v['arguments']['game']:
               if type(i)==str:
                   args.append(fmarg(i,ver,classpath,v,opt,gmdir,d,fg))
        
    if 'minecraftArguments' in v:
        args=args+fmarg(v['minecraftArguments'],ver,classpath,v,opt,gmdir,d,fg).split()
    return args
def getmcargs(ver,java,opt,marg=[],d='.minecraft',gl=False):
    v=readv(ver,d)
    args=[java,
          '-XX:+UseG1GC',
          '-XX:-UseAdaptiveSizePolicy',
          '-XX:-OmitStackTraceInFastThrow',
          '-Djdk.lang.Process.allowAmbiguousCommands=true',
          '-Dfml.ignoreInvalidMinecraftCertificates=True',
          '-Dfml.ignorePatchDiscrepancies=True',
          '-Dlog4j2.formatMsgNoLookups=true'
          ]
    if marg:args=args+marg
    classpath=getcp(ver,d=d)
    if gl:gmdir=pj(d,'versions',ver)
    else:gmdir=d
    args=args+getjvm(v,ver,classpath,opt,d,gmdir)
    args.append(v['mainClass'])
    args=args+getgame(v,ver,classpath,opt,d,gmdir)
    return args
