# coding:utf-8
"""各文件路径在这里维护"""
import os

# 项目路径
import time

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
# 配置文件路径
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'conf.ini')
# 日志文件路径
LOG_PATH = os.path.join(BASE_PATH, 'log')
# 报告路径
# REPORT_PATH = os.path.join(BASE_PATH, 'report')
# 主流程测试用例路径
TEST_CASE_PATH = os.path.join(BASE_PATH, 'test', 'test_mian')
# 分支优惠券测试用例路径
BRANCH_COUPON_CASE_PATH = os.path.join(BASE_PATH, 'test', 'branch_coupon')
# 测试数据文件路径
RESOURCE_PATH = os.path.join(BASE_PATH, 'test', 'resource')
# 冲刺测试用例路劲
SPRINT_CASE_PATH = os.path.join(BASE_PATH, 'test', 'sprint_21_1')
# ERP接口入参json文件的路径
ERP_JSON_PATH = os.path.join(BASE_PATH, 'backend_data', 'erp_stockout.json')
# 线上bug监控测试文件路径
ONLINE_ISSUE_TEST_PATH = os.path.join(BASE_PATH, 'test', 'online_issues')



# pytest.ini文件地址
PYTEST_FILE_PATH = os.path.join(BASE_PATH, 'pytest.ini')
# 报告的地址
RESULT_PATH = os.path.join(BASE_PATH, 'tmp', 'result')
REPORT_PATH = os.path.join(BASE_PATH, 'tmp', 'report', time.strftime('%Y%m%d%H%M%S'))
