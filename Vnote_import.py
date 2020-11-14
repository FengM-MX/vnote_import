import os
import time
import json
import sys
import re

# 需要进行匹配导入笔记的文件
includeFile = [r'.*\.md']
# 排除在外，不进行遍历的文件夹的名字
excludeFolder = ['image', '_v_images', '_v_attachments']
# 时间格式化字符串
formatStr = '%Y-%m-%dT%H:%M:%SZ'
# vnote的配置文件名称
vnoteConfigName = '_vnote.json'
# vnote的模板文件
vnoteTemplate = {
    "created_time": "",
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


#获取当前路径
def getPath(path, name):
    if path.endswith('\\') or path.endswith('/'):
        return path+name
    if path.find('\\'):
        return path+'\\'+name
    else:
        return path+'/'+name

#匹配文件或问价夹的名称
def matchFile(fName, matchList):
    for match in matchList:
        if re.match(match,fName,re.I):
            return True
    return False

#将配置文件写入文件夹
def writeFile(fileName, fileContent):
    print('写入文件'+fileName+'中！'+'写入内容:'+fileContent)
    with open(fileName, mode='w+', encoding='UTF-8') as f:
        f.write(fileContent)
        f.close

#生成配置文件
def createVnoteConfig(path):
    vnote = vnoteTemplate.copy()
    files = []
    sub_directories = []
    # 获取文件名列表
    file_list = os.listdir(path)
    # print(file_list)
    for fName in file_list:
        # 当fName是文件时，则fName需要在放入到笔记的文件列表中，匹配规则使用正则表达式
        # 当fName是文件夹的时候，则fName不能再排除在外的文件夹中，匹配规则使用正则表达式
        if os.path.isdir(getPath(path, fName)) and matchFile(fName, excludeFolder):
            continue
        elif not os.path.isdir(getPath(path, fName)) and not matchFile(fName, includeFile):
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
        vnote['created_time'] = time.strftime(
            formatStr, time.localtime(time.time()))
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
    if len(sys.argv) == 1 or not os.path.isdir(sys.argv[1]):
        print('路径错误，请输入需要处理的文件夹的路径！')
        sys.exit()
    # 笔记本目录 下面放着文件
    path = sys.argv[1]
    print('处理目录'+path+'!')
    # 获取文件名列表
    createVnoteConfig(path)
    print('vnote文件夹解析完成！')