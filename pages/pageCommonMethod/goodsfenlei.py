"""
商品分类的方法
"""
from common.basePage import Action
from selenium.common.exceptions import TimeoutException
import random


class Goodsfenlei(Action):

    def test_category_text(self, xpath, expected, comments, supper):
        """
        商品分类文本验证
        :param xpath: 分类的xpath
        :param expected: 期望的文本信息
        :param comments: 备注
        :param supper: 上级
        :return:
        """
        result = True
        msg = ''
        # ####################### 先校验各层级分类的文本 #######################
        # 元素定位
        locator = ('xpath', xpath)
        # 获取元素
        elements = self.find_elements(locator)
        # 获取元素的文本
        actual_text = []
        for ele in elements:
            text = self.get_text_content_ele(ele).strip('\n ')
            actual_text.append(text)
        # 求期望文本和实际文本的差
        dif_count = len(set(actual_text) ^ set(expected))
        if dif_count > 0:
            result = False
            sup_msg = "【%s】" % comments if supper == '' else "【%s】的【%s】" % (supper, comments)
            msg = msg + "%s的期望结果：%s与实际结果：%s不一致；" % (sup_msg, expected, actual_text)
        return result, msg

    def test_category_links(self, xpath, comments, supper):
        """
        商品分类链接验证
        :param xpath:
        :param comments:
        :param supper:
        :return:
        """
        result = True
        msg = ''
        if comments == "一级分类":
            # 元素定位
            locator = ('xpath', xpath)
            # 获取元素
            elements = self.find_elements(locator)
            # 数量
            count = len(elements)
            # 生成0到count-1的随机数
            n = random.randint(0, count - 1)
            ele = elements[n]
            text = self.get_text_content_ele(ele).strip('\n ')
            # 点击
            self.click_element(ele)
            try:
                # 检查是否到达商品搜索列表页面
                self.is_title_contains('商品搜索列表', timeout=10)
                # 检查url
                url = self.get_url()
                if text not in url:
                    result = False
                    msg = msg + "一级分类【%s】跳转的url错误。实际结果：%s;" % (text, url)
                else:
                    # url正确的情况下，检查搜索结果页面的面包屑
                    from pages.prodSearchResultPage import SearchResult
                    page = SearchResult(self.driver)
                    # 获取实际的面包屑
                    bread_crumb = page.get_bread_crumb_content()
                    # 比较期望和实际的面包屑
                    if bread_crumb != text:
                        result = False
                        msg = msg + "点击一级分类【%s】之后，搜索结果页面包屑显示不正确，期望结果：【%s】,实际结果：【%s】" \
                              % (text, text, bread_crumb)
            except TimeoutException:
                result = False
                # text = self.get_text_content_ele(ele).strip('\n ')
                msg = "点击一级分类【%s】之后未跳转到搜索结果页" % text
        if comments in ['二级分类', '三级分类']:
            # 元素定位
            locator = ('xpath', xpath)
            # 获取元素
            elements = self.find_elements(locator)
            # 数量
            count = len(elements)
            # 生成0到count-1的随机数
            n = random.randint(0, count - 1)
            ele = elements[n]
            # 分类的名称
            category_name = self.get_text_content_ele(ele).strip('\n ')
            # 分类所属的一级分类和二级分类
            suppers = supper.split('/')
            # 一级分类，二级分类（若本身是二级分类，则sup_2就为空）
            sup_1, sup_2 = supper[0], suppers[1] if len(suppers) == 2 else ''
            # 找到上级元素并将鼠标移动到该分类上
            # 一级分类的定位（跟excel里面一致）
            level_one_loc = ('xpath', '//div[contains(@class, "m_ctgr_item")]/a[contains(@onclick,"%s")]' % sup_1)
            self.move_to_element(level_one_loc)
            # 点击元素(二级，或三级分类)
            self.click_element(ele)
            try:
                self.is_title_contains('商品搜索列表', timeout=10)
                url = self.get_url()
                if (category_name and sup_1 and sup_2) not in url:
                    result = False
                    msg = msg + "分类【%s/%s】跳转的url错误。实际结果：%s" % (supper, category_name, url)
                else:
                    # url正确的情况下，检查搜索结果页面的面包屑
                    from pages.prodSearchResultPage import SearchResult
                    page = SearchResult(self.driver)
                    # 获取实际的面包屑
                    bread_crumb = page.get_bread_crumb_content()
                    # 期望的面包屑
                    bread_crumb_exp = supper + "/" + category_name
                    # 比较期望和实际的面包屑
                    if bread_crumb != bread_crumb_exp:
                        result = False
                        msg = msg + "点击分类【%s】之后，搜索结果页面包屑显示不正确，期望结果：【%s】,实际结果：【%s】" \
                            % (bread_crumb_exp, bread_crumb_exp, bread_crumb)
            except TimeoutException:
                result = False
                msg = "点击分类【%s/%s】之后未跳转到搜索结果页" % (supper, category_name)
        return result, msg





