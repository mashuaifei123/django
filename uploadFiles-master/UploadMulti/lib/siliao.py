import docx
from docx.shared import Inches
import os
from aip import AipOcr
import sys, fitz
import os
from os import listdir
import pandas as pd
import json

# 这一个函数读取图片中的二进制数据
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def do1(path):
    APP_ID = '11030410'
    API_KEY = 'nFL4SLu5GjpM2K1aGQZPKidO'
    SECRET_KEY = 'QZpXrgt6XLFcC8IfzVQViWcORLVHzc28'
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 指定文件夹（拿去用的同学只要改这里）
    os.chdir(path)
    dirs = os.listdir()

    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }
    print('开始处理，共' + str(len(dirs)) + "张图片。")
    cnt = 0
    id = []
    filePath_name = []
    for filePath in dirs:
        try:
            filePath_name.append((os.path.splitext(filePath)[0]).split('i')[0])
            if filePath.split('.')[-1] == 'txt': continue
            cnt += 1
            print('正在处理第' + str(cnt) + '张图片')
            result = aipOcr.basicGeneral(get_file_content(filePath), options)
            cc = result['words_result']
            # print(cc)
            for i in range(len(cc)):
                if '11126' in cc[i]['words']:
                    id.append(cc[i]['words'])
            with open(filePath.split('.')[0] + '.txt', 'w', encoding='utf-8') as ans:
                for i in result['words_result']:
                    ans.write(i['words'] + '\n')

        except:
            pass
        print('处理完成')
    df_dict = dict(zip(filePath_name, id))
    # print(df_dict)
    print('全部处理完成！')
    return  df_dict

def do2(path):
    APP_ID = '11030410'
    API_KEY = 'nFL4SLu5GjpM2K1aGQZPKidO'
    SECRET_KEY = 'QZpXrgt6XLFcC8IfzVQViWcORLVHzc28'
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 指定文件夹（拿去用的同学只要改这里）
    os.chdir(path)
    dirs = os.listdir()

    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }
    print('开始处理，共' + str(len(dirs)) + "张图片。")
    cnt = 0
    id = []
    filePath_name = []
    for filePath in dirs:
        try:
            filePath_name.append((os.path.splitext(filePath)[0]).split('i')[0])
            if filePath.split('.')[-1] == 'txt': continue
            cnt += 1
            print('正在处理第' + str(cnt) + '张图片')
            result = aipOcr.basicGeneral(get_file_content(filePath), options)
            cc = result['words_result']
            # print(cc)
            for i in range(len(cc)):
                if cc[i]['words'].startswith('No.') or cc[i]['words'].startswith('A2200'):
                    id.append(cc[i]['words'])
            with open(filePath.split('.')[0] + '.txt', 'w', encoding='utf-8') as ans:
                for i in result['words_result']:
                    ans.write(i['words'] + '\n')
        except:
            pass
        # print('处理完成')
    df_dict = dict(zip(filePath_name, id))
    # print(df_dict)
    print('全部处理完成！')
    return df_dict



if __name__ == "__main__":
    # 指定文件夹
    os.chdir(r"K:\mashuaifei\饲料查询\图片")
    dirs = os.listdir()