# coding=utf-8
"""订单提交完成 --- 线下结算订单提交成功
url:/member/order/successPage.htm
页面标题：订单提交完成 - 九州通网

"""
from common.basePage import Action
from pages.topCommonMenu.baseMenus import BaseMenus
from common.log import Log

class OfflineOrderSuccessPage(BaseMenus):

    # 订单编号
    __order_code_loc = ('xpath', "//span[text()='订单编号：']/following-sibling::div[1]//b")
    # 订单金额
    __order_amount_loc = ('xpath', "//span[text()='订单金额：']/following-sibling::b")
    # 订单优惠
    __order_discount_loc = ('xpath', "//span[text()='订单优惠：']/following-sibling::b")
    # 查看订单
    __view_order_loc = ('xpath', "//a[text()='查看订单']")
    # 返回购物车
    __return_to_cart_loc = ('xpath', "//a[text()='返回购物车']")
    # 我的订单
    __view_myorder_loc = ('xpath', "//ul/li/a[text()='我的订单']")

    def get_order_code(self):
        """
        获取订单编号
        :return: 返回订单编号
        """
        return self.get_text_loc(self.__order_code_loc)

    def get_order_amount(self):
        """
        获取订单金额
        :return: 订单金额 -- float类型
        """
        # 文本：¥133.5
        text = self.get_text_loc(self.__order_amount_loc)
        amount = float(text[1:])
        return amount

    def get_order_discount(self):
        """
        获取订单优惠金额-- 只有订单使用了优惠时，该字段才显示
        :return: 订单优惠金额 -- float类型
        """
        # 文本：¥133.5
        try:
            text = self.get_text_loc(self.__order_discount_loc)
        except:
            discount = float(0)
        else:
            discount = float(text[1:])
        print("优惠券金额为%s" % discount)
        return discount

    # 获取所有需要校验的金额将入列表(订单金额、优惠金额)
    def get_offline_order_prices_all_list(self):
        # 获取商品总金额
        amount_sum = self.get_order_amount()
        # 获取立减金额
        amount_yh = self.get_order_discount()
        # 返回金额列表
        all_amount_list = [amount_sum, amount_yh]
        return all_amount_list

    def return_to_cart_page(self):
        """
        点击返回购物车链接，回到我的购物车页面
        :return: 我的购物车页面对象
        """
        # 点击返回我的购物车页面
        self.click_loc(self.__return_to_cart_loc)
        # 等待页面加载跳转
        self.wait_title_change('我的购物车')
        from pages.myCartPage import MyCart
        return MyCart(self.driver)

    def go_to_order_detail_page(self):
        """
        点击查看订单链接，跳转到订单详情页
        :return: 订单详情页对象
        """
        # 点击查看订单
        self.click_loc(self.__view_order_loc)
        # 等待页面加载跳转
        self.wait_title_change('订单详情页')
        from pages.orderDetailsPage import OrderDetails
        return OrderDetails(self.driver)

