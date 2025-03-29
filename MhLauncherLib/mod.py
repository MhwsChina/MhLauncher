import requests as req
#下载:https://cdn.modrinth.com/data/{project_id}/versions/{id}/{filename}
#获取mod的mc版本(所有版本)https://api.modrinth.com/v2/project/{mod}/version
#搜索:https://api.modrinth.com/v2/search?limit={搜索数量}&index={排序类型}&query={搜索内容}&facets=%5B%5B%22project_type%3Amod%22%5D%5D
#搜索内容若无去掉&query=
'''
排序类型
relevance关联
downloads下载量
follows(作者)关注数量
newest发布日期
updated更新日期
'''
def searchmod(mod=None,limit=20,index='downloads',timeout=10) -> dict:
    url=f'https://api.modrinth.com/v2/search?limit={limit}&index={index}'
    if mod:url+=f'&query={mod}'
    url+='&facets=%5B%5B%22project_type%3Amod%22%5D%5D'
    rs=req.get(url,timeout=timeout)
    return rs.json()
def modurl(mod,mcver,loader='fabric',timeout=10) -> tuple:
    url=f'https://api.modrinth.com/v2/project/{mod}/version'
    rs=req.get(url,timeout=timeout)
    dic=rs.json()
    for i in dic:
        if mcver in i['game_versions'] and loader in i['loaders']:
            files=[]
            for file in i['files']:
                files.append((file['url'],file['filename'],file['hashes']))
            return (files,i['project_id'],i['id'])
