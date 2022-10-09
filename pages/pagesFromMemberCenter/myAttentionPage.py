"""我的订单页面"""
from common.basePage import Action
import random
from selenium.common.exceptions import *
from common.commonMethod import CommonMethod
from common.log import Log

class MyAttentionPage(Action):

    # 商品元素
    __prods_loc = ('xpath', "//ul[@class='m_search_lst tac_member']/li")

    # 商品名称（基于整个商品元素）
    __prod_name_loc = ('xpath', './/a[@class="u_goods_name"]')

    # 取消关注
    __unfollow_link_loc = ('xpath', './/a[contains(@class, "qxgz")]')

    # 对某个商品取消关注时，弹出框上的确定按钮
    __confirm_button_loc = ('xpath', '//a[text()="确定"]')

    # 商品后面的加购物车按钮
    __add_cart_button_loc = ('xpath', '//button[@data-parabola="true" and contains(@class, "addOneToCart")]')

    # 随机选择一个商品加购物车
    def add_one_to_cart(self):
        # 所有有效的加购物车按钮
        add_to_cart_button_eles = self.find_elements(self.__add_cart_button_loc)
        # 列表中可以加购物车商品的数量
        count = len(add_to_cart_button_eles)
        if count > 0:
            # 生成0到count-1的随机数
            x = random.randint(0, count - 1)
            # 获取列表中第x个商品元素的加购物车按钮
            add_to_cart_button = add_to_cart_button_eles[x]
            # 商品编码
            prod_no_loc = ('xpath', './following-sibling::input[@name="prodno"]')
            prod_no_ele = self.find_element_based_on_element(add_to_cart_button, prod_no_loc)
            # 获取prod no
            prod_no = self.get_attribute_ele(prod_no_ele, 'value')
            # 聚焦元素
            self.js_focus_element_ele(add_to_cart_button, bottom=False)
            # 点击加入购物车
            self.click_element(add_to_cart_button)
            return prod_no

    # # 获取第一个商品的商品编码
    # def prodNo_of_first_prod(self):
    #     # 第一个商品元素
    #     first_prod = self.find_elements(self.__prods_loc)[0]
    #     # 通过商品名称的href属性的值，获取到商品编码
    #     prod_name_ele = self.find_element_based_on_element(first_prod, self.__prod_name_loc)
    #     # 获取prod no
    #     prod_no = self.get_attribute_ele(prod_name_ele, 'href').split('/')[-2]
    #     return prod_no

    # 随机选择商品，取消关注
    def unfollow(self):
        # 所有商品元素
        prods_ele = self.find_elements(self.__prods_loc)
        count = len(prods_ele)
        if count > 0:
            # 生成0到count-1的随机数
            x = random.randint(0, count - 1)
            # 获取列表中第x个商品元素
            prod = prods_ele[x]
            # 通过商品名称的href属性的值，获取到商品编码
            prod_name_ele = self.find_element_based_on_element(prod, self.__prod_name_loc)
            # 获取prod no
            prod_no = self.get_attribute_ele(prod_name_ele, 'href').split('/')[-2]
            # 该商品的取消关注链接
            unfollow_link_ele = self.find_element_based_on_element(prod, self.__unfollow_link_loc)
            # 聚焦元素
            self.js_focus_element_ele(unfollow_link_ele,bottom=False)
            # 点击取消关注
            self.click_element(unfollow_link_ele)
            # 点击弹出框上的确定按钮
            self.click_loc(self.__confirm_button_loc)
            return prod_no

    # 根据商品编码来判断商品是否在关注列表里面
    def is_prod_in_list(self, prod_no):
        # 所有商品元素
        try:
            prod_eles = self.find_elements(self.__prods_loc)
            count = len(prod_eles)
        except TimeoutException:
            prod_eles = []
            count = 0
        if count > 0:
            prod_no_list = []
            for prod in prod_eles:
                # 通过商品名称的href属性的值，获取到商品编码
                prod_name_ele = self.find_element_based_on_element(prod, self.__prod_name_loc)
                # 获取prod no
                prodNo = self.get_attribute_ele(prod_name_ele, 'href').split('/')[-2]
                prod_no_list.append(prodNo)
            if prod_no in prod_no_list:
                return True
            else:
                return False
        else:
            return False

    __search_button_loc = ('xpath', '//*[@id="searchMerchandiseBtn"]/button')

    # 等待页面刷新
    def wait_attention_page_refresh(self, timeout=10):
        """等待页面某元素过期，即等带页面刷新,此页面用搜索按钮判断"""
        try:
            self.wait_element_staleness(self.__search_button_loc, timeout)
        except (TimeoutException, NoSuchElementException):
            pass

    # 我的关注页地址
    __attention_page_url = CommonMethod().get_endpoint('attentionpage')

    # 打开我的关注页面
    def open_attention_page(self, url=__attention_page_url):
        self.open(url, '我的关注')

    # ==========================
    # 第一条商品的输入框的操作，校验
    # ==========================

    # 输入框 -- 第一条商品
    __input_loc = ('xpath', "//li[1]//input[contains(@class, 'input-xsm')]")
    # 输入框后面的单位 -- 第一条商品
    __unit_loc = ('xpath', "//li[1]//span[@class='u_goods_unit']")
    # 加号  -- 第一条商品
    __plus_loc = ('xpath', "//li[1]//i[contains(@class, 'fa-plus')]")
    # 减号 -- 第一条商品
    __minus_loc = ('xpath', "//li[1]//i[contains(@class, 'fa-minus')]")

    # 编辑商品数量
    def modify_prod_num(self, num):
        self.send_keys_loc(self.__input_loc, num)
        self.click_loc(self.__unit_loc)
        Log().info(u"编辑商品数量，输入： %s" % num)

    # 获取已输入的商品数量
    def get_prod_num(self):
        return self.get_attribute_loc(self.__input_loc, 'value')

    # 增商品
    def plus_prod(self):
        self.click_loc(self.__plus_loc)

    # 减商品
    def minus_prod(self):
        self.click_loc(self.__minus_loc)

    # ========================================================================
    # 商品输入框的校验
    # ========================================================================
    def get_result(self, default_num=None, plus=None, minus=None, input=None, input_expected=None, input_2=None):
        """

        :param default_num: 打开商品详情页时，商品数量输入框的默认期望值
        :param plus: 在默认值的基础上，点一次加号后的期望结果
        :param minus: 若input_2等于‘’，表示在默认值的基础上，点一次减号后的期望结果，
                        否则表示在输入框输入input_2后的基础上，点一次减号的期望结果
        :param input: 表示在输入框输入的值
        :param input_expected: 跟input是一对，表示在输入框输入input后，输入框的期望结果
        :param input_2: 跟minus是一对，表示在点减号之前，是否需要辅助输入
        :return:
        """
        result = True
        msg = ''
        if default_num != '':
            # 当默认值不为''时，检查默认值
            actual_num = self.get_prod_num()
            if actual_num != default_num:
                result = False
                msg = "我的关注页面，默认值应该为：%s，实际为：%s；" % (default_num, actual_num)

        if plus != '':
            # 当加不等于''时，检查点加号之后的数量
            self.plus_prod()
            # 输入框的值 -- 实际
            actual_num = self.get_prod_num()
            if actual_num != plus:
                result = False
                msg = msg + "我的关注页面，点加号之后，输入框的值应该为：%s，实际为：%s；" % (plus, actual_num)

        if minus != '':
            # 当减不等于''时，检查点减号之后的数量
            msg_part = ''
            if input_2 != '':
                # 如果input_2有值，说明要先做一次修改商品数量的操作
                self.modify_prod_num(input_2)
                msg_part = '输入框先输入：%s，' % input_2
            self.minus_prod()
            # 输入框的值 -- 实际
            actual_num = self.get_prod_num()
            if actual_num != minus:
                result = False
                msg = msg + "我的关注页面，%s点减之后，输入框的值应该为：%s，实际为：%s；" % (msg_part, minus, actual_num)

        if input != '':
            # 当输入值不等于''时，输入商品数量，检查输入之后的期望结果
            self.modify_prod_num(input)
            # 输入框的值 -- 实际
            actual_num = self.get_prod_num()
            if actual_num != input_expected:
                result = False
                msg = msg + "我的关注页面，输入数量%s之后，输入框的值应该为：%s，实际为：%s；" % (input, input_expected, actual_num)

        return result, msg









