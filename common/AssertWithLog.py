from common.log import Log
import pytest


def assume( result, message):
    pytest.assume(result, message)
    if not result:
        Log().error("\n断言错误：" + message)
