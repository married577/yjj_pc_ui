from common.fileReader import IniUtil, ExcelUtil
from common.basePage import browser
from driver.Client import Client
import os
from jsonpath import jsonpath
from config.file_path import RESOURCE_PATH
import json
from common.database import MySQLOperation
import re
from common.log import Log


class CommonMethod(object):

    def __init__(self):
        self.ini = IniUtil()
        self.env = self.ini.get_value_of_option('test_env', 'env')

    def get_host(self):
        """
        返回host
        :return: host
        """
        return self.ini.get_value_of_option('host', self.env)

    def get_endpoint(self, key):
        """
        根据url的名称，获取完整的url
        :param key:
        :return: 完整的url
        """
        # host
        host = self.get_host()
        # resource
        resource = self.ini.get_value_of_option('resource', key)
        # url
        url = host + resource
        return url

    def get_custom(self, key):
        """
        自定义url，获取url
        :return:
        """
        # host
        host = self.get_host()
        # url
        url = host + key
        return url

    def get_driver(self):
        """获取driver"""
        browser_name = self.ini.get_value_of_option('browser', 'browser')
        # driver = browser(browser=browser_name)
        driver = Client.init_web_driver()
        return driver

    def get_test_file(self, file_name):
        """
        获取测试数据的文件路径
        :param file_name: 测试文件的名称加后缀（无路径）
        :return: 文件的路径
        """
        part = r'%s\%s_env' % (RESOURCE_PATH, self.env)
        file_path = os.path.join(part, file_name)
        return file_path

    def get_login_user(self, tag_name):
        """
        根据tag名称，来获取不同环境的登录用户名密码
        :param tag_name: 登录用户的标签
        :return: 用户名密码
        """
        # 存放用户名密码的excel地址
        file_path = self.get_test_file('login_user.xlsx')
        # 获取excel内容
        ex = ExcelUtil('users', file_path)
        content = ex.dict_data()
        # 根据tag获取相应的用户密码
        for i in content:
            if i['tag'] == tag_name:
                return i['username'], i['password']
        else:
            # 若未能通过tag找到相应的账号
            return "未在excel配置相应账号", "请检查login_user.xlsx文件"

    def get_admin_account(self):
        """获取admin账号"""
        ini = IniUtil()
        name = "account_" + self.env
        admin_account = ini.get_value_of_option("admin_account", name)
        return eval(admin_account)

    def jsonpath_parse(self, rs, json_path):
        """
        解析jsonpath,返回list
        :param rs: json格式的response
        :param json_path: 目标值的json path
        :return: json path所指向的值（列表）
        """
        result = jsonpath(rs, json_path)
        return result

    def connect_db(self, connection_name):
        """
        连接数据库
        :param connection_name: option name under [db_test], [db_pre],[db_prod], eg: sup, b2b_app, b2b_be.
        :return: 已连接的数据库对象
        """
        # 获取数据库连接
        ini = IniUtil()
        section = "db_" + self.env
        con = ini.get_value_of_option(section, connection_name)
        connection = json.loads(con)
        # 连接数据库
        db = MySQLOperation(connection)
        return db

    def compare_list(self, list1, list2):
        """
        获取两个列表的交集，返回数量
        :param list1:
        :param list2:
        :return:
        """
        a = set(list1)
        b = set(list2)
        return len(a & b)

    # 获取字典的keys值，dict_ac实际结果字典
    def get_dict_keys(self, dict_ac):
        keys2 = []
        for item in dict_ac.items():
            keys2.append(item[0])
        return keys2

    # 比较两个字典是否相等,dict_ac实际结果，dict_ex预期结果
    def comporm_one_dic(self, dict_ex, dict_ac):
        keys1 = []
        for item in dict_ac.items():
            keys1.append(item[0])
        print(keys1)
        for i in keys1:
            result = True
            try:
                if dict_ex[i] != dict_ac[i]:
                    print("数据不一致")
                    print(dict_ac[i], dict_ex[i])
                    result = False
                    break
                else:
                    if result is False:
                        break
                    else:
                        result = True
                        print("数据一致")
                        print(dict_ac[i], dict_ex[i])
            except KeyError:
                result = False
        return result

    # 存在双层嵌套字典的比较方法，dict_ac实际结果，dict_ex预期结果
    def comporm_two_dic(self, dict_ex, dict_ac):

        if len(dict_ac.keys()) >= len(dict_ex.keys()):
            for i in self.get_dict_keys(dict_ac):
                try:
                    result = self.comporm_one_dic(dict_ex[i], dict_ac[i])
                    if result is False:
                        break
                except KeyError:
                    result = False
        else:
            result = False
            Log().info("实际结果的key值少于预期结果的key值，请检查")
        return result

    # 修改json对象的字段
    def modify_json_value(self, input_json, json_path, new_value):
        """

        :param input_json: json字符串
        :param json_path: 需要被更新的字段的jsonpath，若该字段隐藏在一段字符串中，无法用jsonpath找到，则用.字段名称表示比如“.cartId”。
        :param new_value: 新的值
        :return: 返回被更新了的json字符串
        """
        # 将input_json转化成字符串
        input_str = json.dumps(input_json)
        # 字段名称
        field_name = json_path.split('.')[-1]
        # 解析json path获取value
        field = self.jsonpath_parse(input_json, json_path)
        print("替换前原始值为：%s" % field)
        if field:
            # 处理能用jsonpath取到的字段
            # 字段值
            field_value = field[0]
            # 字段名称和value的组合
            if isinstance(field_value, str):
                value_tobe_replace = '"' + field_name + '": ' + '"' + str(field_value) + '"'
                replace_value = '"' + field_name + '": ' + '"' + str(new_value) + '"'
            elif isinstance(field_value, bool):
                value_tobe_replace = '"' + field_name + '": ' + str(field_value).lower()
                replace_value = '"' + field_name + '": ' + str(new_value).lower()
            else:
                value_tobe_replace = '"' + field_name + '": ' + str(field_value)
                replace_value = '"' + field_name + '": ' + str(new_value)
            # 将对应的值替换掉
            input_str = input_str.replace(value_tobe_replace, replace_value)
        else:
            # 处理不能用jsonpath取到的字段
            # 需要被替换的部分
            pattern = """((')|(\\\\")){1}%s((')|(\\\\")){1}[\s]*:[\s]*((')|(\\\\")){0,1}[0-9a-zA-Z_.]*((')|(\\\\")){0,1},""" % field_name
            # 整个字段名称和字段值
            field = re.search(pattern, input_str).group(0)
            field_name = field.split(':')[0]
            field_value = field.split(':')[1].rstrip(",")
            if '"' in field_name:
                mark = r'\"'
            else:
                mark = "'"
            try:
                value = eval(field_value.replace("\\", ''))
                field_type = type(value)
            except:
                field_type = bool
            if field_type is str:
                replace_value = "%s:" % field_name + mark + "%s" % new_value + mark + ","
            elif field_type is bool:
                replace_value = "%s:" % field_name + str(new_value).lower() + ","
            else:
                replace_value = "%s:" % field_name + str(new_value) + ","

            # 将需要替换的部分替换
            input_str = re.sub(pattern, replace_value, input_str)
        # 将input_str转化成json
        result = json.loads(input_str)
        return result

    # 将非json格式的input转化成json
    def convert_input_to_json(self, string):
        """
        data = "{loginName=wumeng&loginPwd=123456&appVersion=2.4.2&imei=dced90296131e146&model=DUK-AL20&systemVersion=dced90296131e146}"
        将上面这种非标准的输入字符串，转化成json格式
        """
        new_str = string.replace("&", '","').replace("=", '":"').replace('{', '{"').replace('}', '"}')
        return new_str

    def get_special_dic_key(self, dic, keyValue):
        """
        # 通过字典的关键字的模糊匹配，返回对应的key值，没有则返回空
        :return: 返回字典中的值
        """
        for key in dic.keys():
            if keyValue in key:
                return key

        value = ""
        return value

    def get_special_dic_value(self, dic, length):
        """
        # 通过字典的指定的值
        :return: 返回字典中的值
        """

        if length<=len(dic)-1:

            i = 0
            returnValue = ""
            for (key, value) in dic.items():

                if i==length:
                    returnValue = value
                    break
                i = i + 1

            Log().info("从字典中返回的值是：" + returnValue)

            return returnValue


    # def close_database(self, db):
    #     """
    #     关闭数据库连接
    #     :param db: 已连接的数据库对象
    #     :return:
    #     """
    #     db.close_db()
    #
    # def search_one_from_db(self, sql, db):
    #     """
    #     查询数据库，返回一条数据
    #     :param sql:
    #     :param db: 已连接的数据库对象
    #     :return: dict, eg: {'sup_user_id': 48229, 'login_name': 'wumeng', 'login_pwd': '123456'}
    #     """
    #     # 执行sql 返回结果
    #     rs = db.search_one(sql)
    #     return rs
    #
    # def search_all_from_db(self, sql, db):
    #     """
    #     查询数据库， 返回多条数据
    #     :param sql:
    #     :param db: 已连接的数据库对象
    #     :return: dict eg:
    #     { "Field1" : [value1, value1,value3, value4, value5],
    #     "Field2" : [value1, value1,value3, value4, value5]
    #     }
    #     """
    #     rs = db.search_all(sql)
    #     # 转换结果
    #     result = self.search_all_result_to_dict(rs)
    #     return result
    #
    # def update_data(self, sql, db):
    #     """
    #     用sql做新增，更新和删除操作
    #     :param sql: sql语句
    #     :param db: 已连接的数据库对象
    #     :return:
    #     """
    #     # 执行更新或delete的sql
    #     db.update(sql)
    #
    # def search_all_result_to_dict(self, result):
    #     """
    #     将从数据库返回的多条数据，转化成字典格式
    #     result: search_all_from_db的返回结果(或这种类型的数据)
    #
    #     将其转化成下面格式的字典：
    #     """
    #     r = {}
    #     keys = list(result[0])
    #     for k in keys:
    #         value = []
    #         for m in result:
    #             value.append(m[k])
    #         r[k] = value
    #     return r
    #
        # 修改json对象的字段

    # def modify_json_value(self, input_json, json_path, new_value):
    #     """
    #
    #     :param input_json: json字符串
    #     :param json_path: 需要被更新的字段的jsonpath，若该字段隐藏在一段字符串中，无法用jsonpath找到，则用.字段名称表示比如“.cartId”。
    #     :param new_value: 新的值
    #     :return: 返回被更新了的json字符串
    #     """
    #     # 将input_json转化成字符串
    #     input_str = json.dumps(input_json)
    #     # 字段名称
    #     field_name = json_path.split('.')[-1]
    #     # 解析json path获取value
    #     field = self.jsonpath_parse(input_json, json_path)
    #     if field:
    #         # 处理能用jsonpath取到的字段
    #         # 字段值
    #         field_value = field[0]
    #         # 字段名称和value的组合
    #         if isinstance(field_value, str):
    #             value_tobe_replace = '"' + field_name + '": ' + '"' + str(field_value) + '"'
    #             replace_value = '"' + field_name + '": ' + '"' + str(new_value) + '"'
    #         elif isinstance(field_value, bool):
    #             value_tobe_replace = '"' + field_name + '": ' + str(field_value).lower()
    #             replace_value = '"' + field_name + '": ' + str(new_value).lower()
    #         else:
    #             value_tobe_replace = '"' + field_name + '": ' + str(field_value)
    #             replace_value = '"' + field_name + '": ' + str(new_value)
    #         # 将对应的值替换掉
    #         input_str = input_str.replace(value_tobe_replace, replace_value)
    #     else:
    #         # 处理不能用jsonpath取到的字段
    #         # 需要被替换的部分
    #         pattern = """((')|(\\\\")){1}%s((')|(\\\\")){1}[\s]*:[\s]*((')|(\\\\")){0,1}[0-9a-zA-Z_.]*((')|(\\\\")){0,1},""" % field_name
    #         # 整个字段名称和字段值
    #         field = re.search(pattern, input_str).group(0)
    #         field_name = field.split(':')[0]
    #         field_value = field.split(':')[1].rstrip(",")
    #         if '"' in field_name:
    #             mark = r'\"'
    #         else:
    #             mark = "'"
    #         try:
    #             value = eval(field_value.replace("\\", ''))
    #             field_type = type(value)
    #         except:
    #             field_type = bool
    #         if field_type is str:
    #             replace_value = "%s:" % field_name + mark + "%s" % new_value + mark + ","
    #         elif field_type is bool:
    #             replace_value = "%s:" % field_name + str(new_value).lower() + ","
    #         else:
    #             replace_value = "%s:" % field_name + str(new_value) + ","
    #
    #         # 将需要替换的部分替换
    #         input_str = re.sub(pattern, replace_value, input_str)
    #     # 将input_str转化成json
    #     result = json.loads(input_str)
    #     return result
    #

# if __name__=='__main__':
    # # com = CommonMethod()
    # # url = com.get_endpoint('loginpage')
    # # com.get_login_user('1')
    # x = [{'tag': 'main', 'username': 'jtyscjsqd', 'password': '123456'}, {'tag': 'two_tickets', 'username': '湖北省直属机关医院', 'password': '123456'}, {'tag': 'pingpai', 'username': 'shengli', 'password': '123456'}, {'tag': 'specialoffer', 'username': 'whjryy', 'password': '888'}]
    # tag = 'dddd'
    # for item in x:
    #     if item['tag'] == tag:
    #         pass
    # com = CommonMethod()
    # ex = {"a":{"aa":11,"bb":22,"cc":33},"b":{"aa":11,"bb":22,"cc":33},"c":{"aa":11,"bb":22,"cc":33},"d":{"aa":11,"bb":22,"cc":33}}
    # ac = {"a":{"aa":11,"bb":22,"cc":33},"b":{"aa":11,"bb":22},"c":{},"d":{}}
    # ex1 = {"KZQ032050X":{"订单金额":65,"优惠金额":0,"奖励金抵扣":0,"全场立折":10.79,"支付优惠":0,"实付":54.21}, "KWZ076005XLS1":{"订单金额":0,"优惠金额":0,"奖励金抵扣":0,"全场立折":0,"支付优惠":0,"实付":0}, "KZQ029277X":{"订单金额":0,"优惠金额":0,"奖励金抵扣":0,"全场立折":0,"支付优惠":0,"实付":0}}
    # ac1 = {'KWZ076005XLS1': {'订单金额': 0, '优惠金额': 0, '奖励金抵扣': 0, '全场立折': 0, '支付优惠': 0, '实付': 0}, 'KZQ029277X': {'订单金额': 0, '优惠金额': 0, '奖励金抵扣': 0, '全场立折': 0, '支付优惠': 0, '实付': 0}, 'KZQ032050X': {'订单金额': 65.0, '全场立折': 10.79, '实付': 54.25}}
    # print(len(ex1.keys()))
    # print(len(ac1.keys()))
    # result = com.comporm_two_dic(ex1, ac1)
    # print(result)



