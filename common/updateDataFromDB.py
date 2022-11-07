"""通过数据库修改或新增数据的方法"""
from common.commonMethod import CommonMethod
import datetime,requests

from common.fileReader import IniUtil
from common.log import Log
import math


class OperationInDB(object):

    def __init__(self):
        self.com = CommonMethod()
        self.db = self.com.connect_db('b2b')
        self.env = IniUtil().get_value_of_option('test_env', 'env')
#
# if __name__ == '__main__':
#     d = OperationInDB()
