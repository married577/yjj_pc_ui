"""预生产环境运行"""

import pytest
from config.file_path import RESULT_PATH, REPORT_PATH,PYTEST_FILE_PATH
import subprocess
from common.fileReader import IniUtil

if __name__ == '__main__':
    # 修改环境
    file = IniUtil()
    file.update_value_of_opetion('test_env', 'env', 'pre')
    # # 修改执行路径
    IniUtil(PYTEST_FILE_PATH).update_value_of_opetion2('pytest', 'testpaths', 'test_mian')
    # 执行测试用例并生成报告
    pytest.main(['-q', '--alluredir={}'.format(RESULT_PATH), '--clean-alluredir'])
    # subprocess.call("allure generate %s -c -o %s" % (RESULT_PATH,REPORT_PATH), shell=True)