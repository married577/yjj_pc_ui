from mysql import connector
# 由于需要安装数据库连接程序，影响线上发版，所有暂时注释掉_2019_2_5
# import cx_Oracle


class MySQLOperation(object):

    def __init__(self, connections):
        # 连接数据库
        self.cnn = connector.connect(**connections)
        print('连接数据库')
        # 获取数据库游标
        self.cursor = self.cnn.cursor(cursor_class=connector.cursor.MySQLCursorDict)
        print('获取数据库游标')

    # 查询一条语句,返回字典
    # 例子：{'supplier_id': 139, 'supplier_name': '供应商勿动', 'link_phone': '13312345678'}
    def search_one(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        print('执行sql语句%s' % sql)
        return result

    # 查询多条数据
    def search_all(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    # 更新数据
    def update(self, sql):
        self.cursor.execute(sql)
        self.cnn.commit()

    # 执行多条语句
    def excute_multiple(self, sql_list):
        for sql in sql_list:
            self.cursor.execute(sql)
        self.cnn.commit()

    # 关闭数据库连接
    def close_db(self):
        # 关闭游标
        self.cursor.close()
        print('关闭游标')
        # 关闭数据库连接
        self.cnn.close()
        print('关闭数据库连接')

    def search_all_result_to_dict(self):
        """
        处理查询到多条数据的结果,
        返回结果类型：字典
        { fieldname1: [value1， value2， value3, value4]
        feildname2: [value11, value22, value33, value44]
        }
        """
        sql2 = "select resource_id from tb_sup_resource where resource_id in (select resource_id from tb_sup_role_resource where role_id = 66) and resource_type=1 and parent_id is not NULL"
        result = self.search_all(sql2)
        r = {}
        keys = list(result[0])
        for k in keys:
            value = []
            for m in result:
                value.append(m[k])
            r[k] = value
        return r

# 由于需要安装数据库连接程序，影响线上发版，所有暂时注释掉_2019_2_5
# class OracleOperation(object):
#     # conn = cx_Oracle.connect('syerp /syerp@10.3.5.229:1521/orcl')
#     #
#     # c = conn.cursor() # 获取cursor()
#     #
#     # x = c.execute('select PK, prodid from TB_GOS_SALE_SALEORDERDET where billid ='FDGXSG08581663'')  # 使用cursor()操作查询
#     #
#     # x.fetchone()  # 展示查询结果，fetchone函数是获得一行结果，fetchall函数是获得所有行结果。均为元组
#     #
#     # c.close()  # 关闭cursor()
#     #
#     # conn.close()  # 关闭数据库连接
#
#     def __init__(self):
#         # 连接数据库
#         self.cnn = cx_Oracle.connect('syerp/syerp@10.3.5.229:1521/orcl')
#         # 获取数据库游标
#         self.cursor = self.cnn.cursor()
#
#     # 查询一条语句,返回字典
#     # 例子：{'supplier_id': 139, 'supplier_name': '供应商勿动', 'link_phone': '13312345678'}
#     def search_one(self):
#         self.cursor.execute("select PK, prodid from TB_GOS_SALE_SALEORDERDET where billid ='FDGXSG08581663'")
#         result = self.cursor.fetchone()
#         return result
#
#     # 查询多条数据
#     def search_all(self, sql):
#         self.cursor.execute("select billstate from TB_GOS_SALE_SALEORDERDET where billid in ('FDGXSG08581665','FDGXSG08581663');")
#         result = self.cursor.fetchall()
#         return result
#
#     # 更新数据
#     def update(self, sql):
#         self.cursor.execute(sql)
#         self.cnn.commit()
#
#     # 执行多条语句
#     def excute_multiple(self, sql_list):
#         for sql in sql_list:
#             self.cursor.execute(sql)
#         self.cnn.commit()
#
#     # 关闭数据库连接
#     def close_db(self):
#         # 关闭游标
#         self.cursor.close()
#         # 关闭数据库连接
#         self.cnn.close()
#
#     def search_all_result_to_dict(self):
#         """
#         处理查询到多条数据的结果,
#         返回结果类型：字典
#         { fieldname1: [value1， value2， value3, value4]
#         feildname2: [value11, value22, value33, value44]
#         }
#         """
#         sql2 = "select resource_id from tb_sup_resource where resource_id in (select resource_id from tb_sup_role_resource where role_id = 66) and resource_type=1 and parent_id is not NULL"
#         result = self.search_all(sql2)
#         r = {}
#         keys = list(result[0])
#         for k in keys:
#             value = []
#             for m in result:
#                 value.append(m[k])
#             r[k] = value
#         return r

# if __name__ == "__main__":
    # from common.fileReader import IniUtil
    # import json
    # ini = IniUtil()
    # cof = ini.get_value_of_option("db_pre", "supp_connection")
    # connection = json.loads(cof)
    # import sys
    # print(sys.path)
    # sys.path.append(r'D:\oracle\instantclient_18_3')
    # print(sys.path)
    # db = OracleOperation()
    # sql = "select supplier_ID, supplier_name, link_phone from tb_sup_b2b t where t.supplier_name='供应商勿动'"
    # x = db.search_one()
    # print(x)
    # db.close_db()
    # print(x)









