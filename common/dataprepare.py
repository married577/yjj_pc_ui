# coding:utf-8
"""用来做数据准备，或数据依赖的准备"""
from bs4 import BeautifulSoup
import requests
from common.commonMethod import CommonMethod
from pages.loginPage import LoginPage
from time import sleep

# 1. 从商品搜索结果页，拿到第一个有库存的商品的prodno
def get_prod_info(html_doc):
    soap = BeautifulSoup(html_doc, features="html.parser")
    # 找到所有商品的class为m_goods_nums_wrap的div 模块
    divs = soap.find_all('div', 'm_goods_nums_wrap')

    prodno = ''

    # 找到第一个有库存的商品，就退出循环
    for div in divs:
        # 商品的prodno，prodid，中包装数所在的tag都属于div的兄弟节点
        next_tag = list(div.next_siblings)
        # 从兄弟节点中找出prodno
        if len(next_tag) is 17:
            for t in next_tag:
                if type(t).__name__ is 'Tag':
                    tag_name = t.name
                    if tag_name == 'input':
                        id = t['id']
                        if id == 'prodno':
                            prodno = t['value']

            # 找到第一个商品就退出循环
            break
    return prodno


# 2. 获取商品搜索页
def get_search_html(user_name, password):
    """
    :param user_name:
    :param password:
    :return:
    """
    # 1. 获取测试环境
    com = CommonMethod()
    env = com.env
    # 2. 获取host, username, password
    host = com.get_host()

    # 3. 登录请求的url,以及搜索有库存商品请求的url
    url_login = "%s/user/topLogin.json?jzt_username=%s&jzt_password=%s" % (host, user_name,password)
    url_search = '%s/search/merchandise.htm?v=1&keyword=kl&manufacture=&haveStorage=true' % host
    # 4 发送登录请求
    r = requests.Session()
    r.post(url_login)
    # 5. 发送搜索有库存商品的请求
    try:
        print("打开商品搜索页。。。")
        rs_search = r.get(url_search, timeout=30)
        result = rs_search.text
        print("打开成功")
    except:
        result = None
        pass
    return result


def get_prodno_with_storage(user_name, password):
    """
    根据登录用户，获取任意一个有库存的商品
    :param user_name:
    :param password:
    :return:
    """
    html = get_search_html(user_name, password)
    prod = get_prod_info(html)
    return prod


def find_prod_have_store(driver, username, password):
    """
    获取登录用户的有库存的商品的列表
    :return:
    # """
    # # 获取测试环境
    # com = CommonMethod()
    # 获取浏览器的驱动
    # driver = com.get_driver()
    # 登录后，首页进行搜素
    homepage = LoginPage(driver).login_homepage(username, password)
    resultpage = homepage.search_goods("kl")
    # 点击只看有货按钮
    resultpage.click_storage_loc()
    sleep(5)
    prod_no = resultpage.get_prodno_in_list()
    return prod_no


if __name__ == "__main__":

    y = get_prodno_with_storage('5241526','5241526')
    print(y)











