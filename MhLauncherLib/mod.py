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
def searchmod(mod=None,limit=20,index='downloads',timeout=10) -> list:
    url=f'https://api.modrinth.com/v2/search?limit={limit}&index={index}'
    if mod:url+=f'&query={mod}'
    url+='&facets=%5B%5B%22project_type%3Amod%22%5D%5D'
    rs=req.get(url,timeout=timeout)
    return rs.json()['hits']
def modurl(mod,mcver,timeout=10) -> tuple:
    #mod=slug
    url=f'https://api.modrinth.com/v2/project/{mod}/version'
    rs=req.get(url,timeout=timeout)
    dic=rs.json()
    '''loaders=[]
    for i in dic:
        if not loader:
            if mcver in i['game_versions']:
                for j in i['loaders']:
                    if not j in loaders:
                        loaders.append(j)
        if mcver in i['game_versions'] and loader in i['loaders']:
            files=[]
            for file in i['files']:
                files.append((file['url'],file['filename'],file['hashes']))
            return (files,i['project_id'],i['id'],i['loaders'])'''
    urls=tuple()
    for i in dic:
        if mcver in i['game_versions']:
            tmp={}
            files=[]
            for f in i['files']:
                files.append((f['url'],f['filename'],f['hashes']))
            tmp['files']=files
            tmp['project_id']=i['project_id']
            tmp['id']=i['id']
            tmp['loaders']=i['loaders']
            tmp['version']=i['version_number']
            tmp['type']=i['version_type']
            urls=urls+(tmp,)
    return urls
def formatsc(sd) -> list:
    ls=[]
    for i in sd:
        ls.append((i['title'],i['versions'],i['slug'],i['icon_url']))
    return ls
'''
modurl(mod,mcver) -> tuple
(
    {
        files: [
            (
                url->str,
                filename->str,
                sha->dict
                {
                    'sha1':str,
                    'sha256':str,
                    'sha2':str,
                    ...
                }
            )
        ],
        project_id: str,
        id: str,
        loaders: ['fabric','forge'.......],
        version: str,
        type: str(release,snapshot....)
    }...........
)
#mod=modname
formatsc(sd) -> list
[
    (
        modtitle->str,
        mcversions->list['1.20.1','1.21'.......],
        modname->str,
        modiconurl->str
    )
]
#sd=searchmod()
'''
