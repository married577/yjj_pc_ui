"""支付记录查询页面"""
from common.basePage import Action
from common.log import Log
from common.commonMethod import CommonMethod


class OnlinePaymentInquire(Action):

    # 个人中心-在线支付查询
    __onlinePay_inquire_url = CommonMethod().get_endpoint('online_payment_inquire_page')
    # 开始时间输入元素定位
    __one_start_time_loc = ('xpath', '//input[@id="DatePickerStart"]')
    # 结束时间输入元素定位
    __one_end_time_loc = ('xpath', '//input[@id="DatePickerEnd"]')
    # 点击查询元素定位
    __select_click_loc = ('xpath', '//input[@id="searchButton"]')
    # 在线支付查询-第一条记录的支付金额
    __first_price = ('xpath', '//tbody/tr[1]//span[@class="u_field_amount"]')
    # 在线支付查询-第一条记录的支付方式
    __pay_mode = ('xpath', '//tbody/tr[1]//td[5]')
    # 在线支付查询-第一条记录的支付类别
    __pay_type = ('xpath', '//tbody/tr[1]//td[6]')
    # 在线支付查询-第一条记录的支付状态
    __pay_state = ('xpath', '//tbody/tr[1]//td[7]')

    def input_start_time(self, stratime):
        """输入查询开始时间"""
        try:
            self.js_focus_element_loc(self.__one_start_time_loc)
            self.send_keys_loc(self.__one_start_time_loc, stratime)
        except:
            Log().info('输入查询在线支付开始时间错误')

    def input_end_time(self, endtime):
        """输入查询开始时间"""
        try:
            self.js_focus_element_loc(self.__one_end_time_loc)
            self.send_keys_loc(self.__one_end_time_loc, endtime)
        except:
            Log().info('输入查询在线支付结束时间错误')

    def click_select_button(self):
        """输入查询开始时间"""
        try:
            self.js_focus_element_loc(self.__select_click_loc)
            self.click_loc(self.__select_click_loc)
        except:
            Log().info('点击在线支付查询错误')

    # 打开在线支付查询页面
    def open_onlinePay_inquire_page(self):
        self.open(self.__onlinePay_inquire_url, '在线支付查询')
        Log().info('打开在线支付查询页面')

    # 获取第一条记录的支付金额
    def get_first_price(self):
        first_price = self.get_text_loc(self.__first_price)
        Log().info('第一条记录的支付金额: %s' % float(first_price[1:]))
        return float(first_price[1:])

    # 获取线支付查询-第一条记录的支付方式
    def get_pay_mode(self):
        pay_mode = self.get_text_loc(self.__pay_mode)
        Log().info('第一条记录的支付方式: %s' % pay_mode)
        return pay_mode

    # 获取第一条记录的支付类别
    def get_pay_type(self):
        pay_type = self.get_text_loc(self.__pay_type)
        Log().info('第一条记录的支付类别：%s' % pay_type)
        return pay_type

    # 获取第一条记录的支付状态
    def get_pay_state(self):
        pay_state = self.get_text_loc(self.__pay_state)
        Log().info('第一条记录的支付状态: %s' % pay_state)
        return pay_state

    # 同时获取第一条记录的支付金额、支付方式、支付类别、支付状态
    def get_onlinepay_inquire_first_message(self):
        first_price = self.get_first_price()
        pay_mode = self.get_pay_mode()
        pay_type = self.get_pay_type()
        pay_state = self.get_pay_state()
        return first_price, pay_mode, pay_type, pay_state

