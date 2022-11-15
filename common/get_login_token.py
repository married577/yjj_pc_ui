# coding=utf-8

from selenium import webdriver
import time
import requests
import json

# 登录url、账号、密码
url = "https://web-api.pre.yyjzt.com/auth/api/app/login/password"
account = "武汉市新洲区好药师周铺大药房"
password = "e10adc3949ba59abbe56e057f20f883e"


# 获取登录token
def get_token():
    data = {"clientType": "PC", "loginNameOrMobile": account, "loginPwd": password}
    headers = {'token_platform_client_type': 'USER',
               'sy_plat': 'B2B',
               'Content-Type': 'application/json',
               'Accept': 'application/json, text/plain, */*'}

    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    token = res.json()['data']['zhcaiToken']  # json提取器获取token
    userMobile = res.json()['data']['user']['userMobile']
    # Test_demo.token = re.search('"token" : "(.*?)"', res)   正则表达式获取token
    return token, userMobile


# 获取公司ID
def get_company_id():
    # 获取公司ID的url
    __rul = "https://web-api.pre.yyjzt.com/user/api/admin/userb2bcompanybind/companyList"
    token, userMobile = get_token()
    data = {"phone": userMobile}
    headers = {'token_platform_client_type': 'USER',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json, text/plain, */*',
               'zhcaiToken': token}

    res = requests.post(url=__rul, data=data, headers=headers)
    list = res.json()['data']['list']  # json提取器获取companyId
    companyid = list[0]['companyId']
    return companyid


# 获取首页token
def get_home_page_token():
    # 获取首页token的url
    __url = "https://web-api.pre.yyjzt.com/auth/api/app/login/bindCompanyId"
    # 获取公司ID
    companyid = get_company_id()
    # 获取登录的token
    token, userMobile = get_token()
    data = {"companyId": companyid, "clientType": "PC"}
    headers = {'token_platform_client_type': 'USER',
               'Content-Type': 'application/json',
               'zhcaiToken': token,
               'Accept': 'application/json, text/plain, */*'}

    res = requests.post(url=__url, data=json.dumps(data), headers=headers)
    # print(res.request.headers)
    token1 = res.json()['data']['zhcaiToken']  # json提取器获取token
    # Test_demo.token = re.search('"token" : "(.*?)"', res)   正则表达式获取token
    token2 = 'ssr_'
    token = token2 + token1
    return token

    # 通过登录接口获取的token


"""
def cookies_login():
    token1 = get_home_page_token()
    token2 = 'ssr_'
    token = token2 + token1  # 拼接token
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.pre.yyjzt.com/")  # 要登陆的网站

    cookies1 = {u'name': u'yjj-token', u'value': token}
    cookies2 = {u'name': u'areaCode', u'value': u'42011100'}
    cookies3 = {u'name': u'companyId', u'value': u'781020001'}
    cookies4 = {u'name': u'companyName',
                u'value': u'%E6%AD%A6%E6%B1%89%E5%B8%82%E6%96%B0%E6%B4%B2%E5%8C%BA%E5%A5%BD%E8%8D%AF%E5%B8%88%E5%91%A8%E9%93%BA%E5%A4%A7%E8%8D%AF%E6%88%BF'}
    cookies5 = {u'name': u'existBindCustomer', u'value': u'1'}
    cookies6 = {u'name': u'loginName',
                u'value': u'%E6%AD%A6%E6%B1%89%E5%B8%82%E6%96%B0%E6%B4%B2%E5%8C%BA%E5%A5%BD%E8%8D%AF%E5%B8%88%E5%91%A8%E9%93%BA%E5%A4%A7%E8%8D%AF%E6%88%BF'}
    cookies7 = {u'name': u'nickName', u'value': u'%E5%BE%AE%E4%BF%A1%E7%94%A8%E6%88%B7'}
    cookies8 = {u'name': u'userId', u'value': u'4'}
    cookies9 = {u'name': u'userMobile', u'value': u'17798242409'}
    cookies10 = {u'name': u'userName', u'value': u'%E5%91%A8%E9%93%BA%E8%B4%9F%E8%B4%A3%E4%BA%BA'}

    driver.add_cookie(cookies1)  # 这里添加cookie，有时cookie可能会有多条，需要添加多次
    driver.add_cookie(cookies2)
    driver.add_cookie(cookies3)
    driver.add_cookie(cookies4)
    driver.add_cookie(cookies5)
    driver.add_cookie(cookies6)
    driver.add_cookie(cookies7)
    driver.add_cookie(cookies8)
    driver.add_cookie(cookies9)
    driver.add_cookie(cookies10)
    time.sleep(3)

"""
