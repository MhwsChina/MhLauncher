import sys,time,os,inspect
inputf=input
def input(txt='',ls=[],typ=str,err='输入不正确,请重新输入!'):
    while True:
        tmp=inputf(txt)
        if not tmp in ls and ls!=[]:
            print(err)
            continue
        try:tmp=typ(tmp);break
        except:print(err)
    return tmp
pprint=print
def print(*args,end='\n'):
    return
    sys.stdout.write(' '.join(map(str,[*args]))+end)
def log(*args,mode='INFO'):
    txt=' '.join([*args])
    m=inspect.currentframe().f_back.f_code.co_name
    if m=='<module>':m='[MAIN]: '
    else:m=f'[{m}]: '
    t=time.strftime('%H:%M:%S',time.localtime(time.time()))
    print(f'[{t} {mode}]: {m}{txt}')
def pause():
    return input('按Enter键继续...')
def clear():
    if os.name=='nt':os.system('cls')
    if os.name=='posix':os.system('clear')
def listprint(ls,fst=0):
    l,j=len(str(len(ls))),0
    if fst:
        for i in fst:
            print(i,end='')
            if len(i)<l:
                print((l-len(i))*' ',end='')
            print(' ',end='')
        print()
    for i in ls:
        print('{0:<{1}} {2}'.format(j,l,i))
        j+=1
def pj(*args):
    return os.path.join(*args).replace('\\','/')
