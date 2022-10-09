"""历史采购页面"""
from common.basePage import Action
from common.commonMethod import CommonMethod
from time import sleep
from common.log import Log


class HistoryOrderPage(Action):

    # 历史采购页地址
    __history_order_page_url = CommonMethod().get_endpoint('history_order_page')

    # 打开搜索商品列表页面
    def open_history_order_page(self, url=__history_order_page_url, start_date=None, end_date=None):
        if start_date and end_date:
            url_part = "?selectPur=1&&timeS=%s%%20-%%20%s" % (start_date, end_date)
        elif start_date:
            url_part = "?selectPur=1&&timeS=%s%%20-%%20%s" % (start_date, start_date)
        elif end_date:
            url_part = "?selectPur=1&&timeS=%s%%20-%%20%s" % (end_date, end_date)
        else:
            url_part = ''
        self.open(url+url_part, '历史采购')

    # ===================根据商品编码做操作,若列表中同个商品有多个，只操作第一个=========================================

    # 编辑商品数量
    def modify_prod_num(self, num, prod_no):
        __prod_quantity_loc = ('xpath', '//input[@data-prodno="%s"]' % prod_no)
        self.send_keys_loc(__prod_quantity_loc, num)
        __prod_storage_loc = ('xpath', '//input[@data-prodno="%s"]/ancestor::td/preceding-sibling::td[1]' % prod_no)
        self.click_loc(__prod_storage_loc)
        Log().info(u"编辑商品数量，输入： %s" % num)

    # 获取已输入的商品数量
    def get_prod_num(self, prod_no):
        __prod_quantity_loc = ('xpath', '//input[@data-prodno="%s"]' % prod_no)
        return self.get_attribute_loc(__prod_quantity_loc, 'value')

    # 增商品
    def plus_prod(self, prod_no):
        __plus_loc = ('xpath', '//input[@data-prodno="%s"]/../preceding-sibling::a[@class="u_goods_increa"]' % prod_no)
        self.click_loc(__plus_loc)

    # 减商品
    def minus_prod(self, prod_no):
        __minus_loc = ('xpath', '//input[@data-prodno="%s"]/../preceding-sibling::a[@class="u_goods_reduce"]' % prod_no)
        self.click_loc(__minus_loc)

    # ========================================================================
    # 商品输入框的校验
    # ========================================================================
    def get_result(self, prod_no, default_num=None, plus=None, minus=None, input=None, input_expected=None, input_2=None):
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
                msg = "历史采购页，默认值应该为：%s，实际为：%s；" % (default_num, actual_num)

        if plus != '':
            # 当加不等于''时，检查点加号之后的数量
            self.plus_prod(prod_no)
            # 输入框的值 -- 实际
            actual_num = self.get_prod_num(prod_no)
            if actual_num != plus:
                result = False
                msg = msg + "历史采购页，点加号之后，输入框的值应该为：%s，实际为：%s；" % (plus, actual_num)

        if minus != '':
            # 当减不等于''时，检查点减号之后的数量
            msg_part = ''
            if input_2 != '':
                # 如果input_2有值，说明要先做一次修改商品数量的操作
                self.modify_prod_num(input_2,prod_no)
                msg_part = '输入框先输入：%s，' % input_2
            self.minus_prod(prod_no)
            # 输入框的值 -- 实际
            actual_num = self.get_prod_num(prod_no)
            if actual_num != minus:
                result = False
                msg = msg + "历史采购页，%s点减之后，输入框的值应该为：%s，实际为：%s；" % (msg_part, minus, actual_num)

        if input != '':
            # 当输入值不等于''时，输入商品数量，检查输入之后的期望结果
            self.modify_prod_num(input, prod_no)
            # 输入框的值 -- 实际
            actual_num = self.get_prod_num(prod_no)
            if actual_num != input_expected:
                result = False
                msg = msg + "历史采购页，输入数量%s之后，输入框的值应该为：%s，实际为：%s；" % (input, input_expected, actual_num)

        return result, msg
