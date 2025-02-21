#微软登录

from requests import post 
from requests import get
from json import loads
from json import dumps
import webbrowser#打开网页

def OAuth():
    webbrowser.open("https://login.live.com/oauth20_authorize.srf\
 ?client_id=00000000402b5328\
 &response_type=code\
 &scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL\
 &redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf")
    re_url = str(input("enter the replace url:"))
    begin = re_url.find("code=") + 5
    end = re_url.find("&lc")
    code = str("")#申请码
    for ch in range(begin, end):
        code += re_url[ch]#拼接邀请码
    data = {
        "client_id": "00000000402b5328", # 还是Minecraft客户端id
        "code": code, # 第一步中获取的代码
        "grant_type": "authorization_code",
        "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
        "scope": "service::user.auth.xboxlive.com::MBI_SSL"
    }#请求的数据
    url = "https://login.live.com/oauth20_token.srf"
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }#请求头

    res = post(url=url, data=data, headers=header)
    dic = loads(res.text)
    access_token = dic["access_token"]

    '''

    XBox Live 身份验证

    '''
    data = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": access_token # 第二步中获取的访问令牌
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }
    url = "https://user.auth.xboxlive.com/user/authenticate"
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = dumps(data)
    res = post(url=url, data=data, headers=header)
    Token = loads(res.text)["Token"]
    uhs = str()
    for i in loads(res.text)["DisplayClaims"]["xui"]:
        uhs = i["uhs"]
    '''

    XSTS 身份验证

    '''
    data = dumps({
        "Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [
                Token
            ]
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
    })
    url = "https://xsts.auth.xboxlive.com/xsts/authorize"
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    res = post(url=url, data=data, headers=header)
    dic = loads(res.text)
    XSTS_token = dic["Token"]
    '''

    获取 Minecraft 访问令牌

    ''' 
    data = dumps({
        "identityToken": "XBL3.0 x=" + uhs + ";" + XSTS_token
    })
    url = "https://api.minecraftservices.com/authentication/login_with_xbox"
    res = post(url=url, data=data)
    dic = loads(res.text)
    jwt = dic["access_token"]#jwt token,也就是Minecraft访问令牌

    header = {
        "Authorization": "Bearer " + jwt
    }
    res = get(url = "https://api.minecraftservices.com/entitlements/mcstore", headers=header)
    if(res.text == ""):
        return {}
    else:
        '''
        
        获取玩家 UUID
        
        '''
        header = {
            "Authorization": "Bearer " + jwt
        }
        res = get(url="https://api.minecraftservices.com/minecraft/profile", headers=header)
        dic = loads(res.text)
        print(dic)
        username = dic["name"]#用户名
        uuid = dic["id"]#uuid

        return {
            "username": username,
            "uuid": uuid,
            "access_token": jwt
        }
