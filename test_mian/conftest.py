import pytest
import allure
from driver.Client import Client


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # 失败截图
    if rep.when == 'setup' and rep.outcome == 'failed':
        allure.attach(body=Client.driver.get_screenshot_as_png(), name="setup失败截图",
                      attachment_type=allure.attachment_type.PNG)
    if rep.when == 'call' and rep.outcome == 'failed':
        allure.attach(body=Client.driver.get_screenshot_as_png(), name="test失败截图",
                      attachment_type=allure.attachment_type.PNG)
    if rep.when == 'teardown' and rep.outcome == 'failed':
        allure.attach(body=Client.driver.get_screenshot_as_png(), name="teardown失败截图",
                      attachment_type=allure.attachment_type.PNG)
