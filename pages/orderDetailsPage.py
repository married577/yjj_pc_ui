"""订单详情页"""

from common.basePage import Action
from selenium.common.exceptions import TimeoutException
from common.fileReader import IniUtil
from common.log import Log
from time import sleep


class OrderDetails(Action):

    f = IniUtil()

    # ******************************************订单详情左侧金额信息******************************************
    """商品总金额、立减金额、优惠券金额、奖励金金额、全场立折金额、支付优惠金额、应付金额"""
    # 商品实付金额-订单同步2.0
    __amount_sun2_loc = ('xpath', '//div[@class="u_orderDetailL"]//ul[3]//span[@class="orderDetailC orderDetailCRed"]')
    # 立减金额
    __amount_lijian_loc = ('xpath', '//dt/span[text()="立减"]/../following-sibling::dd/span')
    # 优惠券金额
    __amount_coupon_loc = ('xpath', '//dt/span[text()="优惠券"]/../following-sibling::dd/span')
    # 应付金额
    __amount_payable_loc = ('xpath', '//dt/span[text()="应付金额"]/../following-sibling::dd//span')

    # 获取商品总金额
    def get_amount_sum(self):
        amount_sum = ''
        amount_sum = float(self.get_text_loc(self.__amount_sun2_loc).split('￥')[1])
        return amount_sum

    # 获取立减金额
    def get_amount_lijian(self):
        try:
            price = float(self.get_text_loc(self.__amount_lijian_loc).split('￥')[1])
        except:
            price = float(0)
        return price

    # 获取优惠券金额
    def get_amount_coupon(self):
        try:
            price = float(self.get_text_loc(self.__amount_coupon_loc).split('￥')[1])
        except:
            price = float(0)
        return price

    # 获取应付金额
    def get_amount_payable(self):
        try:
            price = float(self.get_text_loc(self.__amount_payable_loc).split('￥')[1])
        except:
            price = float(0)
        return price

    # 获取所有需要校验的金额将入列表
    def get_amount_all_list(self):
        # 获取商品总金额
        amount_sum = self.get_amount_sum()
        # 获取立减金额
        amount_lijian = self.get_amount_lijian()
        # 获取优惠券金额
        amount_coupon = self.get_amount_coupon()
        # 获取应付金额
        amount_payable = self.get_amount_payable()
        # 返回金额列表
        all_amount_list = [amount_sum, amount_lijian, amount_coupon, amount_payable]
        return all_amount_list

    # ******************************************订单详情左侧操作*****************************************
    # 订单同步2.0-订单编号
    __order2_number = ('xpath', '//div[@class="u_orderDetailL"]/h2')

    def get_order_number(self):
        """获取订单同步1.0开票单号或者订单同步2.0订单编号"""
        order_number = ''
        order_number = self.get_text_loc(self.__order2_number).split('：')[1]
        return order_number

    # ******************************************订单详情右侧商品详情******************************************
    """tips页面订单金额、优惠金额、奖励金抵扣、全场立折、支付优惠、实付"""
    # 单个商品订单金额
    __goods_amount_sum_loc = ('xpath', '//*[text()="订单金额："]/following-sibling::span')
    # 单个商品优惠金额
    __goods_amount_youhui_loc = ('xpath', '//*[text()="优惠金额："]/following-sibling::span')
    # 单个商品实付金额
    __goods_amount_payable_loc = ('xpath', '//*[text()="实付："]/following-sibling::span')

    # 获取单个商品订单金额
    def get_goods_amount_sum(self):
        try:
            price = float(self.get_text_loc(self.__goods_amount_sum_loc).split('￥')[1])
        except:
            price = float(0)
        return price

    # 获取单个商品优惠金额
    def get_goods_amount_youhui(self):
        try:
            price = float(self.get_text_loc(self.__goods_amount_youhui_loc).split('￥')[1])
        except:
            price = float(0)
        return price

    # 获取单个商品实付金额
    def get_goods_amount_payable(self):
        try:
            price = float(self.get_text_loc(self.__goods_amount_payable_loc).split('￥')[1])
        except:
            price = float(0)
        return price

    # 获取单个商品tips页所有需要校验的金额将入列表
    def get_goods_amount_all_list(self):
        # 获取商品订单
        amount_sum = self.get_amount_sum()
        # 获取优惠券金额
        amount_coupon = self.get_amount_coupon()
        # 获取应付金额
        amount_payable = self.get_amount_payable()
        # 返回金额列表
        all_amount_list = [amount_sum, amount_coupon, amount_payable]
        return all_amount_list

    # *****************************************订单详情右侧操作*******************************************

    __prod_name = ('xpath', '//li[@class="li"][1]/div[1]/div[1]/div[2]/div[1]')

    # 提取商品名称
    def get_prod_name(self):
        text = self.get_text_loc(self.__prod_name)
        return text

    # 加入购物车元素
    __buy_again = ('xpath', '//li[@class="li"][1]//div[contains(text(),"加入购物车")]')
    __buy_again_text = ('xpath', '/html/body/div[@role="alert"]/p')

    # 点击加入购物车
    def click_buy_again(self):
        self.click_loc(self.__buy_again)
        # 获取加购成功提示消息
        text = self.get_text_loc(self.__buy_again_text)
        return text

    __order_number_loc = ('xpath', '//div[@class="top"]')

    # 获取详情页订单编号
    def get_order_number1(self):
        x = self.get_text_loc(self.__order_number_loc)
        # 去掉获取商品名称的末尾的空格
        return x

    __contact_merchant_loc = ('xpath', '//*[text()="联系商家"]')
    __service_name_loc = ('xpath', '//span[@class="em-widget-header-nickname"]')

    # 点击联系商家
    def click_contact_merchant(self):
        __iframe_loc = ('xpath', '//*[@class="easemobim-chat-panel"]')
        __iframe_close_loc = ('xpath', '//*[@title="关闭"]')
        self.js_focus_element_loc(self.__contact_merchant_loc)
        self.click_loc(self.__contact_merchant_loc)
        sleep(3)
        # self.switch_window()
        # 切换iframe句柄
        self.switch_frame(__iframe_loc)
        sleep(3)
        text = self.get_text_loc(self.__service_name_loc)
        # 关闭客服框
        self.click_loc(__iframe_close_loc)
        # 跳出 iframe
        self.back_to_default_window()
        return text

    __buy_again_button_loc = ('xpath', '//div[contains(text(),"再次购买")]')

    # 点击再次购买
    def click_again_bug(self):
        self.js_focus_element_loc(self.__buy_again_button_loc)
        self.click_loc(self.__buy_again_button_loc)

    __cancellation_order_button_loc = ('xpath', '//div[contains(text(),"取消订单")]')
    __select_reason_loc = ('xpath', '//*[@id="wrapper"]/div/div[1]/div')
    __affirm_cancellation_loc = ('xpath', '//span[text()="确认取消"]')
    __cancellation_hint_loc = ('xpath', '/html/body/div[@role="alert"]/p')

    # 点击取消订单
    def click_cancellation_order(self):
        self.js_focus_element_loc(self.__cancellation_order_button_loc)
        self.click_loc(self.__cancellation_order_button_loc)
        sleep(2)
        # 选择取消原因
        self.click_loc(self.__select_reason_loc)
        sleep(1)
        # 确认取消
        self.click_loc(self.__affirm_cancellation_loc)
        # 提取取消提示
        text = self.get_text_loc(self.__cancellation_hint_loc)
        return text


    # ******************************************等待******************************************

    def wait_page_load(self, timeout=10):
        """等待页面的打开，这里用开票单号来判断页面是否打开"""
        self.is_visibility(self.__order2_number, timeout)