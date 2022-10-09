"""我的订单页面"""
from common.basePage import Action
from common.commonMethod import CommonMethod
from time import sleep

test_file_path = CommonMethod().get_test_file('templete.xls')


class KSXDPage(Action):

    # Excel导入采购计划
    __import_button_loc = ('xpath', "//div[contains(@class, m_c_title)]//a[contains(@class, 'f_fr')][2]")

    # 弹出框上，商品编码
    __prodno_on_window_loc = ('xpath', "//*[@id='importForm']//label[contains(text(), '商品编码')]/input")

    # 弹出框上，上传excel按钮
    __upload_button_on_window_loc = ('xpath', '//input[@id="file"]')

    # 弹框上，导入按钮
    __import_button_on_window_loc = ('xpath', "//*[@id='importForm']//a[@data-excel='confirm']")

    # 弹框上的确认按钮
    __confirm_button_on_window_loc = ('xpath','//*[@id="layui-layer1"]//a')

    # 删除失效商品
    __delete_invalid_prods_loc = ('xpath', "//a[text()='清除失效商品']")

    # 提交订单
    __submit_button_loc = ('xpath', "//button[text()='提交订单']")

    # 导入采购计划,并提交订单
    def import_excel(self):
        self.click_loc(self.__import_button_loc)
        sleep(1)
        # 点击导入窗口的商品编码radio button
        self.click_loc(self.__prodno_on_window_loc)
        # 上传excel
        self.find_element_presence(self.__upload_button_on_window_loc).send_keys(test_file_path)
        # 点击导入按钮
        self.click_loc(self.__import_button_on_window_loc)
        # 点击确认按钮
        self.click_loc(self.__confirm_button_on_window_loc)
        # 删除失效商品
        self.click_loc(self.__delete_invalid_prods_loc)
        # 点击提交订单
        self.click_loc(self.__submit_button_loc)
        # 等待页面跳转到确认订单页面
        self.wait_title_change('确认订单信息', timeout=30)
        from pages.orderConfirmationPage import OrderConfirmation
        return OrderConfirmation(self.driver)








