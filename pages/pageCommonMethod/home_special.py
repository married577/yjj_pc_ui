"""
首页和专题页共有的方法
"""
from common.basePage import Action
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException,NoSuchElementException
import random
import operator
from time import sleep
from datetime import datetime
from common.log import Log


class HomeAndSpecial(Action):

    def open_url(self, url):
        """打开url"""
        self.driver.get(url)

    def test_links(self, xpath, expt_url):
        """
        这里默认点击的元素会新开一个窗口
        :param xpath: 一组元素的定位
        :param expt_url:期望的url列表
        :return:
        """
        result = True
        msg = ''
        loc = ('xpath', xpath)
        elements = self.find_elements(loc)
        # print("url的长度:%s" % len(elements))
        for i in range(len(elements)):
            # 首页很多元素需要拖动
            self.js_focus_element_ele(elements[i], bottom=True)
            self.click_element(elements[i])
            try:
                self.wait_and_switch_window()
                # 获取实际url
                url = self.get_url()
            except:
                result = False
                msg = msg + "链接跳转失败，链接：%s；" % expt_url[i]
                url = None

            # 新窗口打开的情况下，验证
            if url:
                # 期望的url
                expected_url = expt_url[i]
                if expected_url in url:
                    self.close_and_switch_window()
                else:
                    result = False
                    msg = msg + "实际的链接地址：%s 与 期望的链接地址：%s 不一致；\n" % (url, expt_url[i])
                    self.close_and_switch_window()
        return result, msg

    def test_contains_links(self, xpath, expt_prod):
        """
        验证链接包含在一组期望列表中，通过特殊字符串join链接比较，区别test_contains_goodlinks方法
        :param xpath: 一组元素的定位
        :param expt_prod: 期望的一组商品编码的列表
        :return:result msg
        """
        result = True
        msg = ''
        loc = ('xpath', xpath)
        elements = self.find_elements(loc)
        expt_prod = "__".join(expt_prod)
        # print(type(expt_prod)) # 字符串
        for i in range(len(elements)):
            # 首页很多元素需要拖动
            self.js_focus_element_ele(elements[i], bottom=True)
            self.click_element(elements[i])
            try:
                self.wait_and_switch_window()
                # 获取实际url
                url = self.get_url()
            except:
                result = False
                msg = msg + "链接跳转失败，链接：%s；" % expt_prod[i]
                url = None

            # # 新窗口打开的情况下，验证
            if url:
                # 分割url获取商品编码
                url = url.split("/")
                x1 = url[4] + url[5] + url[6]
                # print("截取的字符串为：%s" % x1)
                x2 = url[-2]
                # print("获取的商品编码为：%s" % x2)
                # 判断是否打开商品详情页

                if x1 == 'merchandisedetailFDG':
                    if x2 not in expt_prod:
                        result = False
                        msg += "打开的第%s个链接: %s 不在期望列表内;\n" % (i, x2)
                else:
                    msg += "打开的不是商品详情页"
                    result = False
                # 比较完成后，最后要关闭窗口
                self.close_and_switch_window()
        return result, msg

    def test_contains_goodlinks(self, xpath, expt_prod):
        """
        验证商品链接包含在一组期望商品列表中，通过list的in 方法
        :param xpath: 一组元素的定位
        :param expt_prod: 期望的一组商品编码的列表
        :return:result msg
        """
        result = True
        msg = ''
        loc = ('xpath', xpath)
        elements = self.find_elements(loc)
        for i in range(len(elements)):
            # 首页很多元素需要拖动
            self.js_focus_element_ele(elements[i], bottom=True)
            self.click_element(elements[i])
            try:
                self.wait_and_switch_window()
                # 获取实际url
                url = self.get_url()
            except:
                result = False
                msg = msg + "链接跳转失败，链接：%s；" % expt_prod[i]
                url = None

            # # 新窗口打开的情况下，验证
            if url:
                # 分割url获取商品编码
                url = url.split("/")
                x1 = url[4] + url[5] + url[6]
                # print("截取的字符串为：%s" % x1)
                x2 = url[-2]
                # print("获取的商品编码为：%s" % x2)
                # 判断是否打开商品详情页

                if x1 == 'merchandisedetailFDG':
                    if x2 not in expt_prod:
                        result = False
                        msg += "打开的第%s个链接的商品编码: %s 不在期望列表内;\n" % (i+1, x2)
                else:
                    msg += "打开的不是商品详情页"
                    result = False
                # 比较完成后，最后要关闭窗口
                self.close_and_switch_window()
        return result, msg

    def test_texts(self, xpath, expect_text):
        """
        验证元素的文本值是否和期望一致
        :param xpath: 文本元素的定位
        :param expect_text: 文本元素的期望值
        :return:msg 和 result
        """
        result = True
        msg = ''
        loc = ('xpath', xpath)
        # 获取一组元素的文本
        try:
            actual_texts = self.get_content_text_for_elements(loc, timeout=5)
        except TimeoutException:
            # 如果元素获取不到，实际结果为空
            actual_texts = []
        # 打印元素的实际文本
        print(actual_texts)
        if operator.eq(actual_texts, expect_text):
            pass
        else:
            result = False
            msg = msg + "实际的文本值 ：%s 与期望的文本值 ：%s 不一致" % (actual_texts, expect_text)
        return result, msg

    def test_contain_texts(self, xpath, expect_text):
        """
        验证元素的文本值是否在期望范围内
        :param xpath: 文本元素的定位
        :param expect_text: 文本元素的期望值
        :return:msg 和 result
        """
        result = True
        msg = ''
        loc = ('xpath', xpath)
        # 获取一组元素的文本
        try:
            actual_texts = self.get_content_text_for_elements(loc, timeout=5)
        except TimeoutException:
            # 如果元素获取不到，实际结果为空
            actual_texts = []
        count = len(actual_texts)
        if count > 0:
            for text in actual_texts:
                if text not in expect_text:
                    result = False
                    msg = msg + "搜索结果页的分类:%s 不在期望的分类：%s 范围" % (text, expect_text)
        else:
            if len(expect_text) != 0:
                result = False
                msg += "实际结果：%s与预期结果不符：%s" % (actual_texts, expect_text)
        return result, msg

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
        # 获取元素的文本
        actual_text=[]
        try:
            elements = self.find_elements(locator, timeout=5)
            for ele in elements:
                text = self.get_text_content_ele(ele).strip('\n ')
                actual_text.append(text)
        except TimeoutException:
            pass

        # 求期望文本和实际文本的差
        # dif_count = len(set(actual_text) ^ set(expected))
        # if dif_count > 0:
        #     result = False
        #     sup_msg = "【%s】" % comments if supper == '' else "【%s】的【%s】" % (supper, comments)
        #     msg = msg + "%s的期望结果：%s与实际结果：%s不一致；" % (sup_msg, expected, actual_text)
        # return result, msg

        # 求期望文本和实际文本的差
        count = len(actual_text)
        if count > 0:
            for text in actual_text:
                if text not in expected:
                    result = False
                    sup_msg = "【%s】" % comments if supper == '' else "【%s】的【%s】" % (supper, comments)
                    msg = msg + "%s的期望结果：%s与实际结果：%s不一致；" % (sup_msg, expected, actual_text)
        else:
            if len(expected) != 0:
                result = False
                msg += "实际结果：%s与预期结果不符：%s" % (actual_text, expected)
        return result, msg

    def test_zycategory_links(self,xpath):
        """"
        中药专题页分类链接验证
        :param xpath:
        :param comments:
        :param supper:
        :return:
        """
        result = True
        msg = ''
        # 元素定位
        locator = ('xpath', xpath)
        # 获取元素
        elements = self.find_elements(locator)
        for i in range(len(elements)):
            ele = elements[i]
            text = self.get_text_content_ele(ele).strip('\n ')
            # 点击
            self.click_element(ele)
            try:
                self.wait_and_switch_window(-1)
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
                    text = "中药/" + text
                    if bread_crumb != text:
                        result = False
                        msg = msg + "点击一级分类【%s】之后，搜索结果页面包屑显示不正确，期望结果：【%s】,实际结果：【%s】" \
                              % (text, text, bread_crumb)
                self.close_and_switch_window()
            except TimeoutException:
                result = False
                # text = self.get_text_content_ele(ele).strip('\n ')
                msg = "点击一级分类【%s】之后未跳转到搜索结果页" % text
            return result, msg

    def test_zlcategory_links(self, xpath, comments, supper, expected):
        """
        诊疗分类链接验证
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
            for i in range(len(elements)):
                ele=elements[i]
                text=self.get_text_content_ele(ele).strip('\n ')
                # 点击
                self.click_element(ele)
                try:
                    self.wait_and_switch_window(-1)
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
                        text = "诊疗/" + text
                        if bread_crumb != text:
                            result = False
                            msg = msg + "点击一级分类【%s】之后，搜索结果页面包屑显示不正确，期望结果：【%s】,实际结果：【%s】" \
                                  % (text, text, bread_crumb)
                    self.close_and_switch_window()
                except TimeoutException:
                    result = False
                    # text = self.get_text_content_ele(ele).strip('\n ')
                    msg = "点击一级分类【%s】之后未跳转到搜索结果页" % text

        if comments in ['二级分类', '三级分类']:
            # 元素定位
            locator = ('xpath', xpath)
            # 获取元素
            try:
                elements = self.find_elements(locator,timeout=5)
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
                sup_1, sup_2 = suppers[0], suppers[1] if len(suppers) == 2 else ''
                # 找到上级元素并将鼠标移动到该分类上
                # 一级分类的定位（跟excel里面一致）
                level_one_loc = ('xpath', '//div[contains(@class, "m_ctgr_item")]//a[contains(text(),"%s")]' % sup_1)
                self.move_to_element(level_one_loc)
                # 点击元素(二级，或三级分类)
                self.click_element(ele)
                try:
                    self.wait_and_switch_window(-1)
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
                        bread_crumb_exp = "诊疗/" + supper + "/" + category_name
                        # 比较期望和实际的面包屑
                        if bread_crumb != bread_crumb_exp:
                            result = False
                            msg = msg + "点击分类【%s】之后，搜索结果页面包屑显示不正确，期望结果：【%s】,实际结果：【%s】" \
                                % (bread_crumb_exp, bread_crumb_exp, bread_crumb)
                    self.close_and_switch_window()
                except TimeoutException:
                    result = False
                    msg = "点击分类【%s/%s】之后未跳转到搜索结果页" % (supper, category_name)
            except TimeoutException:
                if expected !='':
                    result = False
                    msg = "点击分类【%s】之后未跳转到搜索结果页" % comments
        return result, msg

    def test_sycategory_links(self, xpath, comments, supper, expected):
        """
        首页商品分类链接验证
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
            elements = self.find_elements(locator, timeout=5)
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
            try:
                elements = self.find_elements(locator,timeout=5)
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
                sup_1, sup_2 = suppers[0], suppers[1] if len(suppers) == 2 else ''
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
            except TimeoutException:
                if expected != '':
                    result = False
                    msg = "页面上不显示的分类跳转失败"
        return result, msg

    def sepcial_level(self, xpath1,xpath2, xpath3,prod_no_li):
        """
        自定义专题页分类楼层验证
        :param catogry:
        :param xpath1: 分类
        :param xpath2: 图片 -- proid
        :param xpath3: 文本
        :param prod_no_li:
        :return:
        """
        result = True
        msg = ''
        # 点分类  -- 单个元素
        loc_cet = ('xpath', xpath1)
        self.click_loc(loc_cet)
        # 获取所有的商品编码
        loc_img = ('xpath', xpath2)
        prod_no = self.get_attribute_for_elements(loc_img, 'proid')
        # 实际个数
        count = len(prod_no)
        expected_count = len(set(prod_no) & set(prod_no_li))
        if count != expected_count:
            result = False
            msg = msg + '；'

        # 验证点击图片跳转
        # 生成0到count-1的随机数
        n = random.randint(0, count - 1)
        ele_imags = self.find_elements(loc_img)
        ele = ele_imags[n]
        # 点击
        self.click_element(ele)
        try:
            self.wait_and_switch_window()
            # 获取实际url
            url = self.get_url()
        except TimeoutException:
            result = False
            msg = msg+''
            url = None
        if url:
            expected_url = "front/merchandise/detail/FDG/"+ prod_no_li[n]
            if expected_url not in url:
                result = False
                msg = msg + ";"

        # 验证点击文本跳转
        loc_text = ('xpath', xpath3)
        # 生成0到count-1的随机数
        n = random.randint(0, count - 1)
        ele_text = self.find_elements(loc_text)
        ele = ele_text[n]
        # 点击
        self.click_element(ele)
        try:
            self.wait_and_switch_window()
            # 获取实际url
            url = self.get_url()
        except TimeoutException:
            result = False
            msg = msg + ''
            url = None
        if url:
            expected_url = "front/merchandise/detail/FDG/" + prod_no_li[n]
            if expected_url not in url:
                result = False
                msg = msg + ";"

        return result, msg



