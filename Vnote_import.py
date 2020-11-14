import os
import time
import json

#需要进行排除在外不导入的文件
excludeFile = ['_vnote.json', '_v_recycle_bin']
#时间格式化字符串
formatStr = '%Y-%m-%dT%H:%M:%SZ'
#vnote的配置文件名称
vnoteConfigName = '_vnote.json'
# vnote的模板文件
vnoteTemplate = {
    "created_time": "2020-11-12T15:09:09Z",
    "files": [],
    "sub_directories": [],
    "version": "1"
}
# file的模板文件
file = {
    'attachment_folder': '',
    'attachments': [],
    'created_time': '',
    'modified_time': '',
    'name': '',
    'tags': []
}
# 子目录的模板文件
sub_directorie = {
    "name": ""
}


def getPath(path, name):
    if path.endswith('\\') or path.endswith('/'):
        return path+name
    if path.find('\\'):
        return path+'\\'+name
    else:
        return path+'/'+name


def writeFile(fileName, fileContent):
    print('写入文件'+path+'中！'+'写入内容:'+fileContent)
    with open(fileName, mode='w+', encoding='UTF-8') as f:
        f.write(fileContent)
        f.close



def createVnoteConfig(path):
    vnote = vnoteTemplate.copy()
    files = []
    sub_directories = []
    # 获取文件名列表
    file_list = os.listdir(path)
    # print(file_list)
    for fName in file_list:
        # 当当前文件是_vnote.json文件、不以.md结尾、或者不是路径则继续下一个流程
        if fName in excludeFile or (not fName.endswith('.md') and not os.path.isdir(getPath(path, fName))):
            continue

        # 如果是目录则递归进行
        if os.path.isdir(getPath(path, fName)):
            # 只有当子文件夹中存在有用的内容，才需要加入子目录中
            if createVnoteConfig(getPath(path, fName)) != '':
                newFolder = sub_directorie.copy()
                newFolder['name'] = str(fName)
                sub_directories.append(newFolder)
        # 如果是文件的话，则生成对应的字符串
        else:
            # 创建时间
            createdTime = time.localtime(
                os.stat(getPath(path, str(fName))).st_ctime)
            createdTimeStr = time.strftime(formatStr, createdTime)
            # 修改时间
            modifiedTime = time.localtime(
                os.stat(getPath(path, str(fName))).st_mtime)
            modifiedTimeStr = time.strftime(formatStr, modifiedTime)
            # 设置文件属性
            newFile = file.copy()
            newFile['created_time'] = createdTimeStr
            newFile['modified_time'] = modifiedTimeStr
            newFile['name'] = str(fName)
            files.append(newFile)
    if len(files) or len(sub_directories):
        vnote['created_time']=time.strftime(formatStr, time.localtime(time.time()))
        vnote['files'] = files
        vnote['sub_directories'] = sub_directories
        # 当目录结果解析成功，则写入文件中
        writeFile(getPath(path, vnoteConfigName),
                 json.dumps(vnote, sort_keys=True, indent=4, separators=(',', ': ')))
        return vnote
    else:
        return ''


# 主程序
if __name__ == "__main__":
    # 笔记本目录 下面放着文件
    path = ''
    # 获取文件名列表
    createVnoteConfig(path)
    print('vnote文件夹解析完成！')
