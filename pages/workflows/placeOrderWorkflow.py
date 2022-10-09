"""下单流程"""
from common.basePage import Action
from common.log import Log
from common.commonMethod import CommonMethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from pages.prodSearchResultPage import SearchResult
from pages.homePage import HomePage
from time import sleep
from pages.myCartPage import MyCart
from pages.prodDetailsPage import DetailsPage
from pages.paymentProcessPages.placeOrder.onlineOrderSubmitSuccessPage import OnlineOrderSuccessPage


class PlaceOrder(Action):

    def clear_cart(self):
        """
        打开购物车页面，并清空购物车
        :return:
        """
        cart_page = MyCart(self.driver)
        # 打开购物车页面
        cart_page.open_cart_page()
        # 清空购物车
        cart_page.clean_prod_in_cart()

    # def add_prod_workflow(self, prod_no, number=None, page_name='Detail'):
    #     """
    #     清空购物车，并在商品详情页或搜索页面将商品加入购物车
    #     :param prod_no: 商品编码
    #     :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
    #     :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页，默认值为Detail
    #     :return: 商品详情页或搜索结果页的page对象
    #     """
    #     page_object = {'Detail': DetailsPage(self.driver), 'Result': SearchResult(self.driver)}
    #     # 1. 清空购物车
    #     self.clear_cart()
    #     # 2. 打开相应页面加购物车
    #     page = page_object[page_name]
    #     page.add_cart_workflow(prod_no, number)
    #     return page

    def add_prod_workflow(self, page_name='Detail', **prod_info):
        """
        清空购物车，并在商品详情页或搜索页面将商品加入购物车
        :param prod_info为字典格式，格式为：{'prod_no':number,'DYA002010I':1}
        :param prod_no: 商品编码
        :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
        :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页，默认值为Detail
        :return: 商品详情页或搜索结果页的page对象
        """
        page_object = {'Detail': DetailsPage(self.driver), 'Result': SearchResult(self.driver)}
        # 1. 清空购物车
        self.clear_cart()
        # 2. 打开相应页面加购物车
        page = page_object[page_name]
        page.add_cart_workflow_dic(**prod_info)
        return page

    # def to_my_cart_page_workflow(self, prod_no, number=None, page_name='Detail'):
    #     """
    #     清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面
    #     :param prod_no:商品编码
    #     :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
    #     :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页，默认值为Detail
    #     :return: 我的购物车页的page对象
    #     """
    #     # 加购物车
    #     page = self.add_prod_workflow(prod_no, number, page_name)
    #     sleep(1)
    #     # 点击右上方的我的购物车按钮,进入我的购物车页面
    #     cart_page = page.go_to_my_cart_page()
    #     sleep(1)
    #     # 刷新购物车
    #     self.refresh()
    #     return cart_page

    def to_my_cart_page_workflow(self, page_name='Detail', **prod_info):
        """
        清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面
        :param prod_info为字典格式，格式为：{'prod_no':number,'DYA002010I':1}
        :param prod_no:商品编码
        :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
        :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页，默认值为Detail
        :return: 我的购物车页的page对象
        """
        # 加购物车
        page = self.add_prod_workflow(page_name, **prod_info)
        sleep(1)
        # 点击右上方的我的购物车按钮,进入我的购物车页面
        sidebar = SideBar(self.driver)
        sidebar.close_side_window()
        cart_page = page.go_to_my_cart_page()
        sleep(1)
        # 刷新购物车
        self.refresh()
        return cart_page

    # def to_order_confirm_page(self, prod_no, number=None, page_name='Detail'):
    #     """
    #     清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面
    #     :param prod_no:商品编码
    #     :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
    #     :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
    #     :return: 确认订单页的page对象
    #     """
    #     # 到我的购物车页面
    #     cart_page = self.to_my_cart_page_workflow(prod_no, number,page_name)
    #     # 我的购物车页面提交订单，跳转到确认订单页面
    #     comfirm_page = cart_page.submit_order()
    #     return comfirm_page

    def to_order_confirm_page(self, page_name='Detail', **prod_info):
        """
        清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面
        :param prod_info为字典格式，格式为：{'prod_no':number,'DYA002010I':1}
        :param prod_no:商品编码
        :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
        :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
        :return: 确认订单页的page对象
        """
        # 到我的购物车页面
        cart_page = self.to_my_cart_page_workflow(page_name, **prod_info)
        # 我的购物车页面提交订单，跳转到确认订单页面
        comfirm_page = cart_page.submit_order()
        return comfirm_page


    def add_prod_list_workflow(self, prod_no_list, number_list, page_name='Detail'):
        """
        清空购物车--》在搜索结果/商品详情页商品列表多次加购--》我的购物车页面--》确认订单页面
        :param prod_no_list:商品编码列表
        :param number_list:加购数量列表，对应商品编码
        :param page_name:将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
        :return:确认订单页的page对象
        """
        page_object = {'Detail': DetailsPage(self.driver), 'Result': SearchResult(self.driver)}
        # 1. 清空购物车
        self.clear_cart()
        # 2. 打开相应页面加购物车
        page = page_object[page_name]
        for x, y in zip(prod_no_list, number_list):
            page.add_cart_workflow(x, y)
        sleep(1)
        # 点击右上方的我的购物车按钮,进入我的购物车页面
        cart_page = page.go_to_my_cart_page()
        sleep(1)
        # 刷新购物车
        self.refresh()
        # 我的购物车页面提交订单，跳转到确认订单页面
        comfirm_page = cart_page.submit_order()
        return comfirm_page

    def add_prod_list_workflow_to_cart(self, prod_no_list, number_list, page_name='Detail'):
        """
        清空购物车--》在搜索结果/商品详情页商品列表多次加购--》我的购物车页面--》确认订单页面
        :param prod_no_list:商品编码列表
        :param number_list:加购数量列表，对应商品编码
        :param page_name:将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
        :return:确认订单页的page对象
        """
        page_object = {'Detail': DetailsPage(self.driver), 'Result': SearchResult(self.driver)}
        # 1. 清空购物车
        self.clear_cart()
        # 2. 打开相应页面加购物车
        page = page_object[page_name]
        for x, y in zip(prod_no_list, number_list):
            page.add_cart_workflow(x, y)
        sleep(1)
        # 点击右上方的我的购物车按钮,进入我的购物车页面
        cart_page = page.go_to_my_cart_page()
        sleep(3)
        # 刷新购物车
        self.refresh()



    # def __to_offline_payment_success_page(self, prod_no, number=None, page_name='Detail'):
    #     """
    #     清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面--》选择线下结算，并提交订单
    #     :param prod_no: 商品编码
    #     :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
    #     :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
    #     :return: 订单提交完成页面的page对象
    #     """
    #     # 到确认订单页面
    #     confirm_page = self.to_order_confirm_page(prod_no, number, page_name)
    #     # 确认订单页，选择线下结算
    #     success_page = confirm_page.submit_order_offline()
    #     return success_page

    def to_offline_payment_success_page(self, page_name='Detail', **prod_info):
        """
        清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面--》选择线下结算，并提交订单
        :param prod_info为字典格式，格式为：{'prod_no':number,'DYA002010I':1}
        :param prod_no: 商品编码
        :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
        :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
        :return: 订单提交完成页面的page对象
        """
        # 到确认订单页面
        confirm_page = self.to_order_confirm_page(page_name, **prod_info)
        # 确认订单页，选择线下结算
        success_page = confirm_page.submit_order_offline()
        return success_page


    # def to_payment_mode_page(self, prod_no, number=None, page_name='Detail', payment_type='online'):
    #     """
    #     清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面，选择在线支付(不使用余额)，并提交订单
    #     --》选择支付方式页面
    #     :param prod_no: 商品编码
    #     :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
    #     :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
    #     :param payment_type: 支付方式：online=线上支付-不使用余额，balance=线上支付-使用余额
    #     :return: 选择支付方式页面的page对象
    #     """
    #     # 到确认订单页面
    #     confirm_page = self.to_order_confirm_page(prod_no, number, page_name)
    #     if payment_type.lower() == 'balance':
    #         # 确认订单页，选择在线支付 - 使用余额
    #         page = confirm_page.submit_order_online_with_balance()
    #         if isinstance(page, OnlineOrderSuccessPage):
    #             # 如果返回的页面是OnlineOrderSuccessPage页面，即在线支付成功页面,则返回None
    #             return None
    #         else:
    #             # 如果返回的是在线支付方式选择页面，返回该页面
    #             return page
    #     else:
    #         # 确认订单页，选择在线支付 - 不使用余额
    #         online_payment_page = confirm_page.submit_order_online_without_balance()
    #         return online_payment_page

    def to_payment_mode_page(self, page_name='Detail', payment_type='online', **prod_info):
        """
        清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面，选择在线支付(不使用余额)，并提交订单
        --》选择支付方式页面
        :param prod_info为字典格式，格式为：{'prod_no':number,'DYA002010I':1}
        :param prod_no: 商品编码
        :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
        :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
        :param payment_type: 支付方式：online=线上支付-不使用余额，balance=线上支付-使用余额
        :return: 选择支付方式页面的page对象
        """
        # 到确认订单页面
        confirm_page = self.to_order_confirm_page(page_name, **prod_info)
        if payment_type.lower() == 'balance':
            # 确认订单页，选择在线支付 - 使用余额
            page = confirm_page.submit_order_online_with_balance()
            if isinstance(page, OnlineOrderSuccessPage):
                # 如果返回的页面是OnlineOrderSuccessPage页面，即在线支付成功页面,则返回None
                return None
            else:
                # 如果返回的是在线支付方式选择页面，返回该页面
                return page
        else:
            # 确认订单页，选择在线支付 - 不使用余额
            online_payment_page = confirm_page.submit_order_online_without_balance()
            return online_payment_page

    # def __to_online_payment_success_page(self, prod_no, number=None, page_name='Detail', payment_mode='个人网银'):
    #     """
    #     清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面，选择在线支付(不使用余额)，并提交订单
    #     --》支付成功页面
    #     :param prod_no: 商品编码
    #     :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
    #     :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
    #     :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
    #     :return: 若payment_mode为支付宝，返回支付宝支付页面的page对象；若payment_mode为微信，返回微信支付页面的page对象；
    #     否则，返回支付成功的页面
    #     """
    #     # 到确认订单页面
    #     confirm_page = self.to_order_confirm_page(prod_no, number, page_name)
    #     # 确认订单页，选择在线支付且不使用余额
    #     online_payment_page = confirm_page.submit_order_online_without_balance()
    #     # 支付方式选择页面，选择支付方式
    #     page = online_payment_page.select_payment_mode_go_to_pay(payment_mode)
    #     return page

    def to_online_payment_success_page(self, page_name='Detail', payment_mode='个人网银', **prod_info):
        """
        清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面，选择在线支付(不使用余额)，并提交订单
        --》支付成功页面
        :param prod_info为字典格式，格式为：{'prod_no':number,'DYA002010I':1}
        :param prod_no: 商品编码
        :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
        :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
        :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
        :return: 若payment_mode为支付宝，返回支付宝支付页面的page对象；若payment_mode为微信，返回微信支付页面的page对象；
        否则，返回支付成功的页面
        """
        # 到确认订单页面
        confirm_page = self.to_order_confirm_page(page_name, **prod_info)
        # 确认订单页，选择在线支付且不使用余额
        online_payment_page = confirm_page.submit_order_online_without_balance()
        # 支付方式选择页面，选择支付方式
        page = online_payment_page.select_payment_mode_go_to_pay(payment_mode)
        return page


    # def __to_online_payment_success_page_with_balance(self, prod_no, number=None, page_name='Detail', payment_mode='个人网银'):
    #     """
    #     清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面
    #     --》选择在线支付（使用余额），并提交订单--》支付成功页面
    #     :param prod_no: 商品编码
    #     :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
    #     :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
    #     :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
    #     :return: 若payment_mode为支付宝，返回支付宝支付页面的page对象；若payment_mode为微信，返回微信支付页面的page对象；
    #     否则，返回支付成功的页面
    #     """
    #     # 到确认订单页面
    #     confirm_page = self.to_order_confirm_page(prod_no, number, page_name)
    #     # 确认订单页，选择在线支付，并使用余额
    #     page = confirm_page.submit_order_online_with_balance()
    #     if isinstance(page, OnlineOrderSuccessPage):
    #         # 如果返回的页面是OnlineOrderSuccessPage页面，即在线支付成功页面,则直接返回该页面
    #         return page
    #     else:
    #         # 如果返回的是在线支付方式选择页面，选择支付方式
    #         page = page.select_payment_mode_go_to_pay(payment_mode)
    #         # 若选择支付宝/微信支付，则返回支付宝/微信页面，否则返回相应的支付成功页面
    #         return page

    def __to_online_payment_success_page_with_balance(self, page_name='Detail', payment_mode='个人网银', **prod_info):
        """
        清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面
        --》选择在线支付（使用余额），并提交订单--》支付成功页面
        :param prod_info为字典格式，格式为：{'prod_no':number,'DYA002010I':1}
        :param prod_no: 商品编码
        :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
        :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
        :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
        :return: 若payment_mode为支付宝，返回支付宝支付页面的page对象；若payment_mode为微信，返回微信支付页面的page对象；
        否则，返回支付成功的页面
        """
        # 到确认订单页面
        confirm_page = self.to_order_confirm_page(page_name, **prod_info)
        # 确认订单页，选择在线支付，并使用余额
        page = confirm_page.submit_order_online_with_balance()
        if isinstance(page, OnlineOrderSuccessPage):
            # 如果返回的页面是OnlineOrderSuccessPage页面，即在线支付成功页面,则直接返回该页面
            return page
        else:
            # 如果返回的是在线支付方式选择页面，选择支付方式
            page = page.select_payment_mode_go_to_pay(payment_mode)
            # 若选择支付宝/微信支付，则返回支付宝/微信页面，否则返回相应的支付成功页面
            return page

    # def to_success_page(self, prod_no, number=None, page_name='Detail', payment_type='online', payment_mode='个人网银'):
    #     """
    #     清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面--》支付成功页面
    #     :param prod_no: 商品编码
    #     :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
    #     :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
    #     :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
    #     :param payment_type: 支付方式：offline=线下结算，online=线上支付-不使用余额，balance=线上支付-使用余额
    #     :return:
    #     payment_type = 线下结算时，返回订单提交成功的页面page对象；
    #     payment_type = 在线支付时，若payment_mode为支付宝，返回支付宝支付页面的page对象；若payment_mode为微信，返回微信支付页面的page对象；
    #     否则，返回支付成功的页面；
    #     payment_type = 使用余额支付时，若余额足够，返回订单支付成功页面的page对象；若余额不足够，payment_mode为支付宝，返回支付宝支付页面的page对象；payment_mode为微信，返回微信支付页面的page对象；
    #     否则，返回支付成功的页面；
    #     """
    #     if payment_type.lower() == 'offline':
    #         return self.__to_offline_payment_success_page(prod_no, number, page_name)
    #     elif payment_type.lower() == 'balance':
    #         return self.__to_online_payment_success_page_with_balance(prod_no, number, page_name, payment_mode)
    #     else:
    #         return self.__to_online_payment_success_page(prod_no, number, page_name, payment_mode)

    def to_success_page(self, page_name='Detail', payment_type='online', payment_mode='个人网银', **prod_info):
        """
        清空购物车--》在搜索结果/商品详情页加购--》我的购物车页面--》确认订单页面--》支付成功页面
        :param prod_info为字典格式，格式为：{'prod_no':number,'DYA002010I':1}
        :param prod_no: 商品编码
        :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
        :param page_name: 将商品加购物车的页面名称：‘Detail’= 商品详情页；‘Result’= 搜索结果页；默认值为Detail
        :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
        :param payment_type: 支付方式：offline=线下结算，online=线上支付-不使用余额，balance=线上支付-使用余额
        :return:
        payment_type = 线下结算时，返回订单提交成功的页面page对象；
        payment_type = 在线支付时，若payment_mode为支付宝，返回支付宝支付页面的page对象；若payment_mode为微信，返回微信支付页面的page对象；
        否则，返回支付成功的页面；
        payment_type = 使用余额支付时，若余额足够，返回订单支付成功页面的page对象；若余额不足够，payment_mode为支付宝，返回支付宝支付页面的page对象；payment_mode为微信，返回微信支付页面的page对象；
        否则，返回支付成功的页面；
        """
        if payment_type.lower() == 'offline':
            return self.to_offline_payment_success_page(page_name, **prod_info)
        elif payment_type.lower() == 'balance':
            return self.__to_online_payment_success_page_with_balance(page_name, payment_mode, **prod_info)
        else:
            return self.to_online_payment_success_page(page_name, payment_mode, **prod_info)
