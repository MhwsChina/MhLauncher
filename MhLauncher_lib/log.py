import sys,time
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
    sys.stdout.write(' '.join(map(str,[*args]))+end)
def log(txt,mode='INFO'):
    t=time.strftime('%H:%M:%S',time.localtime(time.time()))
    print(f'[{t} {mode}]: {txt}')
def pause():
    return input('按Enter键继续...')
