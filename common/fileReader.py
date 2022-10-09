# coding:utf-8
"""读取excel，ini配置文件"""
import configparser
import xlrd
import os
from config.file_path import CONFIG_FILE
import json


class ExcelUtil(object):

    def __init__(self, sheet_name, excel_path):
        if os.path.exists(excel_path):
            self.excel_path = excel_path
        else:
            raise FileNotFoundError(u'文件不存在！')
        self.data = xlrd.open_workbook(self.excel_path)
        self.table = self.data.sheet_by_name(sheet_name)
        # 获取总行数
        self.rowNum = self.table.nrows
        # 获取总列数
        self.colNum = self.table.ncols

    # 获取首行是字段名称的数据
    def dict_data(self):
        keys = self.table.row_values(0)
        if self.rowNum <= 1:
            print(u"总行数小于1")
        else:
            r = []
            j = 1
            for i in range(self.rowNum-1):
                s = {}
                # 从第二行取对应values值
                values = self.table.row_values(j)
                for x in range(self.colNum):
                    if values[x] != '' and ('[' == values[x][0] or '{' == values[x][0]):
                        s[keys[x]] = eval(values[x])
                    else:
                        s[keys[x]] = values[x]
                r.append(s)
                j += 1
            return r

    # 获取首行不是字段名称的数据
    def list_data(self):
        list = []
        for i in range(self.rowNum):
            row_values = self.table.row_values(i)
            if len(row_values) is 1:
                list.append(row_values[0])
            else:
                list.append(row_values)
        return list


class IniUtil(object):
    def __init__(self, ini_path=CONFIG_FILE):
        self.ini_path = ini_path
        # 生成config对象
        self.conf = configparser.ConfigParser()
        # 用config对象读取配置文件
        self.conf.read(self.ini_path, encoding="utf-8-sig")

    def get_sections(self):
        # 以列表形式返回所有的section的名称 ['45', '46']
        return self.conf.sections()

    def get_options_of_section(self, section_name):
        # 得到指定section的所有option的名称 ['host', 'user', 'password', 'port', 'database']
        return self.conf.options(section_name)

    def get_kvaules_of_section(self, section_name):
        # 得到指定section的所有键值对
        return self.conf.items(section_name)

    def get_value_of_option(self, section_name, option):
        # 得到指定section，option的值
        return self.conf.get(section_name, option)

    def update_value_of_opetion(self, section_name, option, value):
        # 修改指定section，option的值
        self.conf.set(section_name, option, value)
        self.conf.write(open(self.ini_path, "w", encoding="utf-8-sig"))

    def update_value_of_opetion2(self, section_name, option, value):
        # 修改指定section，option的值
        self.conf.set(section_name, option, value)
        self.conf.write(open(self.ini_path, "w", encoding="utf-8"))


class JsonUtil(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read_data()

    # 读取json文件
    def read_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            return data

    # 根据关键字获取数据
    def get_data(self, key):
        return self.data[key]

    # 写json
    def write_data(self, data):
        with open(self.file_path, 'w') as fp:
            fp.write(json.dumps(data))







