# coding: utf-8
"""我的缺货篮页面"""
from common.basePage import Action
from pages.memberCenterPage import MemberCenter
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from common.commonMethod import CommonMethod
from common.log import Log


class ShortageBasketPage(Action):

    # 我的缺货篮页面地址
    __shortage_basket_page_url = CommonMethod().get_endpoint('shortage_basket_page')

    # 打开搜索商品列表页面
    def open_basket_page(self, url=__shortage_basket_page_url, start_date=None, end_date=None):
        if start_date and end_date:
            url_part = "?daohuo=&dbasketItemState=&startTime=%s&endTime=%s" % (start_date, end_date)
        elif start_date:
            url_part = "?daohuo=&dbasketItemState=&startTime=%s&endTime=%s" % (start_date, start_date)
        elif end_date:
            url_part = "?daohuo=&dbasketItemState=&startTime=%s&endTime=%s" % (end_date, end_date)
        else:
            url_part = ''
        self.open(url + url_part, '我的缺货篮')

    # ===================根据商品编码做操作,若列表中同个商品有多个，只操作第一个=========================================

    # 编辑商品数量
    def modify_prod_num(self, num, prod_no):
        __prod_quantity_loc = ('xpath', "//input[@value='%s']/preceding-sibling::div//input" % prod_no)
        self.send_keys_loc(__prod_quantity_loc, num)
        __prod_unit_loc = ('xpath', "//input[@value='%s']/preceding-sibling::div/span[@class='u_goods_unit']" % prod_no)
        self.click_loc(__prod_unit_loc)
        Log().info(u"编辑商品数量，输入： %s" % num)

    # 获取已输入的商品数量
    def get_prod_num(self, prod_no):
        __prod_quantity_loc = ('xpath', "//input[@value='%s']/preceding-sibling::div//input" % prod_no)
        return self.get_attribute_loc(__prod_quantity_loc, 'value')

    # 增商品
    def plus_prod(self, prod_no):
        __plus_loc = ('xpath', "//input[@value='%s']/preceding-sibling::div//a[@class='u_goods_increa']" % prod_no)
        self.click_loc(__plus_loc)

    # 减商品
    def minus_prod(self, prod_no):
        __minus_loc = ('xpath', "//input[@value='%s']/preceding-sibling::div//a[contains(@class,'u_goods_reduce')]" % prod_no)
        self.click_loc(__minus_loc)

    # ========================================================================
    # 商品输入框的校验
    # ========================================================================
    def get_result(self, prod_no, default_num=None, plus=None, minus=None, input=None, input_expected=None,
                   input_2=None):
        """

        :param prod_no: 商品编码
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
            actual_num = self.get_prod_num(prod_no)
            if actual_num != default_num:
                result = False
                msg = "我的缺货篮页面，默认值应该为：%s，实际为：%s；" % (default_num, actual_num)

        if plus != '':
            # 当加不等于''时，检查点加号之后的数量
            self.plus_prod(prod_no)
            # 输入框的值 -- 实际
            actual_num = self.get_prod_num(prod_no)
            if actual_num != plus:
                result = False
                msg = msg + "我的缺货篮页面，点加号之后，输入框的值应该为：%s，实际为：%s；" % (plus, actual_num)

        if minus != '':
            # 当减不等于''时，检查点减号之后的数量
            msg_part = ''
            if input_2 != '':
                # 如果input_2有值，说明要先做一次修改商品数量的操作
                self.modify_prod_num(input_2, prod_no)
                msg_part = '输入框先输入：%s，' % input_2
            self.minus_prod(prod_no)
            # 输入框的值 -- 实际
            actual_num = self.get_prod_num(prod_no)
            if actual_num != minus:
                result = False
                msg = msg + "我的缺货篮页面，%s点减之后，输入框的值应该为：%s，实际为：%s；" % (msg_part, minus, actual_num)

        if input != '':
            # 当输入值不等于''时，输入商品数量，检查输入之后的期望结果
            self.modify_prod_num(input, prod_no)
            # 输入框的值 -- 实际
            actual_num = self.get_prod_num(prod_no)
            if actual_num != input_expected:
                result = False
                msg = msg + "我的缺货篮页面，输入数量%s之后，输入框的值应该为：%s，实际为：%s；" % (input, input_expected, actual_num)

        return result, msg

    # 缺货登记列表商品信息基准路径
    base_xpath = "//li[@class='m_abate_f' and position()="

    # 删除选中缺货登记链接
    __delete_selected_prod_links_loc = ('xpath', " //a[contains(@class, 'u_cart_delAll')]")

    # 缺货登记列表总数量
    __total_count_loc = ('xpath', '//span[@class="u_goods_buyed"]')

    # 获取缺货登记列表总条数
    def total_count(self):
        """
        获取总数量
        :return: 缺货登记记录条数
        """
        count = len(self.get_text_for_elements(self.__total_count_loc))
        return count

    # 获取缺货登记列表的某个商品的编码prodno,登记数量以及登记时间
    def get_prod_info_of_first_prod(self, index=1):
        """
        选中列表中的一个商品，返回相关信息
        :param index: 1 表示第一条，2 表示第二条，以此类推。
        :return: 商品编码，登记数量， 登记时间
        """
        # 根据index的值，重组base_path的值
        base_path = self.base_xpath + str(index) + "]"
        """locator：缺货登记列表的商品图片链接"""
        __prod_link_loc = ('xpath', base_path + "/a")
        # 获取第一个缺货商品图片链接的href属性的值
        href = self.get_attribute_loc(__prod_link_loc, 'href')
        # 得到prodno
        prodNo = href.split('/')[-2]
        """locator：缺货登记列表的登记数量"""
        __prod_num_loc = ('xpath', base_path + "//div[@class='num']/b")
        # 获取第一个缺货商品的登记数量
        num = self.get_text_loc(__prod_num_loc)
        # """locator：缺货登记列表的登记时间"""
        # __prod_register_datatime_loc = ('xpath', base_path + "/div/span")
        # # 获取第一个缺货商品的登记时间
        # datatime = self.get_text_loc(__prod_register_datatime_loc)
        return prodNo, num

    # 勾选某个缺货商品，并删除
    def select_prod(self, index=1):
        """
        勾选某个商品的删除复选框
        :param index: 1 表示第一条，2 表示第二条，以此类推。
        :return:
        """
        # 根据index的值，重组base_path的值
        base_path = self.base_xpath + str(index) + "]"
        """locator：缺货登记列表复选框"""
        __prod_checkbox_loc = ('xpath', base_path + "/label/span")
        # 点击商品的复选框
        self.click_loc(__prod_checkbox_loc)

    # 点删除选中缺货登记（有记录被勾选的情况下），弹出的确认窗口中，确定按钮
    __confirm_button_loc= ('xpath', "//a[text()='确定']")

    # 点击删除选中缺货登记链接
    def delete_selected_record(self):
        # 让删除选中缺货登记链接可见
        self.js_focus_element_loc(self.__delete_selected_prod_links_loc)
        # 点击删除选中缺货登记链接
        self.click_loc(self.__delete_selected_prod_links_loc)
        # 点击确认按钮
        self.click_loc(self.__confirm_button_loc)

    # 等待页面刷新
    def wait_result_page_refresh(self, timeout=10):
        """等待页面某元素过期，即等带页面刷新,此页面用搜索按钮判断"""
        try:
            self.wait_element_staleness(self.__delete_selected_prod_links_loc, timeout)
        except (TimeoutException, NoSuchElementException):
            pass

    # 打开我的缺货篮页面
    def open_shortage_basket_from_member_center(self):
        """
        打开缺货篮页面。需要从会员中心首页打开
        :return:
        """
        # 打开会员中心首页
        member_page = MemberCenter(self.driver)
        member_page.open_center_page()
        # 从会员中心首页，打开缺货篮页面
        member_page.click_qhldh_number()
        # 切换页面到缺货篮页面
        member_page.switch_window()
        # 等待页面title完整出现
        member_page.wait_title_change(u'我的缺货篮')





