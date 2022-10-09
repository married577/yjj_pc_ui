"""订单完成页面"""
from common.basePage import Action
from selenium.common.exceptions import TimeoutException
from common.log import Log
from time import sleep


class Online_Payment(Action):
    """订单在线支付页面"""
    # 支付宝支付元素
    __alipay_path = ('xpath', '//span[contains(text(),"支付宝")]')
    # 微信支付元素
    __wx_path = ('xpath', '//span[contains(text(),"微信")]')
    # 个人网上银行元素
    __person_bank_path = ('xpath', '//span[contains(text(),"个人网银")]')
    # 企业网上银行元素
    __enterprise_bank_path = ('xpath', '//span[contains(text(),"企业网银")]')
    # 【确认订单信息】页面提交订单操作
    __submit_order_path = ('xpath', '//*[@class="btn btn-primary"]')
    # 【支付方式选择页面】前往支付按钮操作
    __to_payment_path = ('xpath', '//input[@class="btn btn-primary u_btn_pay"]')
    # 【支付方式选择页面】应付金额
    __payment_Amount_payable = ('xpath', '//*[@class="u_order_no"]')
    # 【支付方式选择页面】订单金额
    __payment_Order_amount = ('xpath', '/html/body/div[3]/div/div[1]/div[3]/p[2]/span')
    # 【支付方式选择页面】订单详情按钮
    __payment_OrderPay_detail = ('xpath', '//input[@id="OrderPay_detail"]')
    # 【支付方式选择页面】订单详情按钮
    __payment_order_info_money = ('xpath', '//*[@id="resultPayPrice"]')

    # 获取在线支付页应付金额
    def get_order_info_money(self):
        return float(self.get_text_loc(self.__payment_order_info_money)[:-1])

    # 获取应付金额
    def get_Amount_payable(self):
        return float(self.get_text_loc(self.__payment_Amount_payable))

    # 获取订单详情展开后的订单金额，并且去除最后一个单位“元”
    def get_Order_amount(self):
        return float(self.get_text_loc(self.__payment_Order_amount)[:-1])

    # 验证订单确认页应付余额、【支付方式选择页面】应付金额、【支付方式选择页面】订单金额是否相等
    def Verification_payment(self, order_yf_price, payment_Amount_payable, payment_Order_amount):
        if order_yf_price == payment_Amount_payable:
            if order_yf_price == payment_Order_amount:
                Log().info("订单确认页应付余额:%s、【支付方式选择页面】应付金额:%s、【支付方式选择页面】订单金额:%s,相等，测试通过" % (order_yf_price, payment_Amount_payable, payment_Order_amount))
                return True
        else:
            Log().info("订单确认页应付余额:%s、【支付方式选择页面】应付金额:%s、【支付方式选择页面】订单金额:%s,不相等，请检查" % (order_yf_price, payment_Amount_payable, payment_Order_amount))
            return False


    # 点击订单详情按钮
    def submit_OrderPay_detail(self):
        self.click_loc(self.__payment_OrderPay_detail)

    # 点击提交按钮
    def submit_order_to_pay(self):
        self.click_loc(self.__submit_order_path)

    # 点击支付宝支付方式
    def click_ali_pay(self):
        self.click_loc(self.__alipay_path)

    # 点击微信支付方式
    def click_wx_pay(self):
        self.click_loc(self.__wx_path)

    # 点击个人网上银行支付方式
    def click_personbank_pay(self):
        self.click_loc(self.__person_bank_path)

    # 点击企业网上银行支付方式
    def click_enterprisebank_pay(self):
        self.click_loc(self.__enterprise_bank_path)

    # 点击前往支付按钮
    def submit_to_paymentpage(self):
        self.click_loc(self.__to_payment_path)

    # 支付宝支付页面金额
    __alipay_money = ('xpath', '//div[@class="ft-center qrcode-header-money"]')

    # 微信支付页面金额
    __wxpay_money = ('xpath', '//span[@id="amountW"]')

    # 个人网银支付页面金额
    __person_bank_money = ('xpath', '//div[contains(text(),"订单金额：")]/following-sibling::div[1]')

    # 企业网银支付页面金额
    __enterprise_bank_money = ('xpath', '//div[contains(text(),"订单金额：")]/following-sibling::div[1]')

    # 获取支付宝应付金额
    def get_alipay_money(self):
        print(float(self.get_text_loc(self.__alipay_money)))
        return float(self.get_text_loc(self.__alipay_money))

    # 获取微信应付金额
    def get_wxpay_money(self):
        return float(self.get_text_loc(self.__wxpay_money))

    # 获取个人网银应付金额
    def get_personbankpay_money(self):
        return float(self.get_text_loc(self.__person_bank_money))

    # 获取企业网银应付金额
    def get_enterprisebankpay_money(self):
        return float(self.get_text_loc(self.__enterprise_bank_money))

    def Verification_onlinepay(self, order_yf_price, onlinepay_money):
        if order_yf_price == onlinepay_money:
            Log().info("订单确认页应付余额:%s、【最终三方页面】应付金额:%s，相等，测试通过" % (order_yf_price, onlinepay_money))
            return True
        else:
            Log().info("订单确认页应付余额:%s、【最终三方页面】应付金额:%s，不相等" % (order_yf_price, onlinepay_money))
            return False

    # 个人网银登录支付按钮
    __person_bank_login = ('xpath', '//*[@id="leftBtn"]/input')

    # 企业网银登录支付按钮
    __enterprise_bank_login = ('xpath', '//*[@id="leftBtn"]/input')

    # 个人网银登录支付按钮
    __person_bank_pay = ('xpath', '//*[@id="cfgBtn"]/input')



    # 个人网银支付成功元素校验
    __personbank_pay_sucess = ('xpath', '//*[contains(text(),"支付成功")]')

    # 企业网银确认制单按钮
    __enterprise_bank_Confirmation_order = ('xpath', '//*[@id="cfgBtn"]/input')

    # 企业网银登陆网银复合按钮
    __enterprise_bank_Compound = ('xpath', '//*[@id="noticeBtn"]/input')

    # 企业网银登陆网银登录按钮
    __enterprise_bank_login2 = ('xpath', '//*[@id="leftBtn"]/input')

    # 企业网银登录支付按钮
    __enterprise_bank_pay = ('xpath', '//*[@id="cfgBtn"]/input')

    # 企业网银支付成功元素校验
    __enterprisebank_pay_sucess = ('xpath', '//*[contains(text(),"支付成功")]')

    # 点击个人网银登录按钮
    def click_person_bank_login(self):
        self.click_loc(self.__person_bank_login)

    # 点击企业网银登录按钮
    def click_enterprise_bank_login(self):
        self.click_loc(self.__person_bank_login)

    # 点击个人网银支付按钮
    def click_person_bank_pay(self):
        self.click_loc(self.__person_bank_pay)



    # 点击企业网银确认制单按钮
    # def click_enterprise_bank_pay(self):
    #     self.click_loc(self.__enterprise_bank_Confirmation_order)

    # 点击企业网银登陆网银复合按钮
    def click_enterprise_bank_pay(self):
        self.click_loc(self.__enterprise_bank_Compound)

    # 企业网银点击支付系列操作集合
    def click_enterprise_bank_allpay(self):
        # 点击登录
        self.click_loc(self.__enterprise_bank_login)
        # 点击确认制单
        self.click_loc(self.__enterprise_bank_Confirmation_order)
        # 点击网银复核
        self.click_loc(self.__enterprise_bank_Compound)
        # 点击登录
        self.click_loc(self.__enterprise_bank_login2)
        # 点击确认支付
        self.click_loc(self.__enterprise_bank_pay)

    # 个人网银支付按钮集合
    def click_person_bank_allpay(self):
        self.click_loc(self.__person_bank_login)
        self.click_loc(self.__person_bank_pay)

    # 校验网银（包含个人、企业）是否支付成功
    def check_personbank_pay_sucess(self):
        """验证支付是否成功，成功返回true，否则返回false"""
        try:
            result = self.is_display(self.__personbank_pay_sucess, 10)
        except TimeoutException:
            result = False
        return result

    # 获取微信支付收款商家【九州通】元素
    __wx_payment_merchantname = ('xpath', '//dd[contains(text(),"收款商家：九州通")]')

    # 校验微信支付收款商家【九州通】元素是否存在
    def check_x_payment_merchantname(self):
        """验证微信支付收款商家【九州通】是否存在，成功返回true，否则返回false"""
        try:
            result = self.is_display(self.__wx_payment_merchantname, 10)
            Log().info("微信支付收款商家是【九州通】，测试通过")
        except TimeoutException:
            Log().info("微信支付收款商家不是【九州通】")
            result = False
        return result

    # 关闭微信二维码页面
    __wx_payment_close = ('xpath', '//*[@id="WXPayLayer"]/div[2]/div[1]/a/i')

    # 获取微信支付页面流水号
    __wx_payment_Serialnumber = ('xpath', '//dd[@id="trxW"]')

    # 点击前往支付，获取第1次的微信支付页流水号M，然后关闭页面，再次点击前往支付，获取第2次的微信支付页流水号N，比较M和N是否不一样，校验微信支付流水号
    def check_wx_payment_Serialnumber(self):
        """获取第1次的微信支付页流水号M，然后关闭页面，再次点击前往支付，获取第2次的微信支付页流水号N，比较M和N是否不一样，校验微信支付流水号，不一样返回true，否则返回false"""
        # # 点击前往支付
        # self.submit_to_paymentpage()
        # 第1次获取微信支付页面流水号
        M = self.get_text_loc(self.__wx_payment_Serialnumber)
        # 点击关闭微信支付页面
        self.click_loc(self.__wx_payment_close)
        # 点击前往支付
        self.submit_to_paymentpage()
        # 第2次获取微信支付页面流水号
        N = self.get_text_loc(self.__wx_payment_Serialnumber)
        if M == N:
            Log().info("微信两次支付流水号一致，不正确，流水号：同一个订单本地流水号不等于上次的流水号")
            return False
        else:
            Log().info("微信两次支付流水号不一致，正确，流水号：同一个订单本地流水号不等于上次的流水号")
            return True

    # ==================================================页面等待================================================

    def wait_result_onlinepage_load(self, timeout=30):
        """等待选中支付方法页打开"""
        try:
            self.is_title_contains(u"选择支付方法", timeout)
        except TimeoutException:
            Log().info(u"选择支付方法信息页面未打开")


class Moneyback_Payment(Online_Payment):
    """回款充值页面"""
    # def __init__(self):
    #     # self.ini = IniUtil()
    #     # self.env = self.ini.get_value_of_option('test_env', 'env')
    #     self.com = CommonMethod()
    #     # 获取浏览器驱动
    #     self.driver = self.com.get_driver()
    #     # self.onlinepayment = Online_Payment(self.driver)
    # ===============================去充值========================= #
    # 充值金额
    __amount_100_loc = ('xpath', "//p[text()='100元']/..")
    __amount_500_loc = ('xpath', "//p[text()='500元']/..")
    __amount_1000_loc = ('xpath', "//p[text()='1,000元']/..")
    __amount_5000_loc = ('xpath', "//p[text()='5,000元']/..")
    __amount_10000_loc = ('xpath', "//p[text()='10,000元']/..")
    __amount_other_loc = ('xpath', "//p[text()='其它金额']/..")

    # 充值金额预设值
    _chongzhi_money = 0.08

    # 请输入充值金额
    __amount_input_loc = ('xpath', '//*[@id="in_price"]')

    # 确认按钮
    __confirm_amount_loc = ('xpath', "//button[@class='pay_button']")

    # 个人网银
    __personbank_qrwy_loc = ('xpath', "//span[text()='个人网银']")

    # 企业网银
    __enterprisebank_qrwy_loc = ('xpath', "//span[text()='企业网银']")

    # wx网银
    __wx_qrwy_loc = ('xpath', "//span[text()='微信']")

    # ali网银
    __ali_qrwy_loc = ('xpath', "//span[text()='支付宝']")

    # 去充值
    __qcz_loc = ('xpath', "//input[@value='去充值']")

    # 支付宝充值页金额
    __alipay_money_moneyback = ('xpath', '//div[contains(text(),"扫一扫")]/following-sibling::div[1]')

    # 微信充值页金额

    # 获取支付宝应付金额
    def get_alipay_money_moneyback(self):
        print(float(self.get_text_loc(self.__alipay_money_moneyback)))
        return float(self.get_text_loc(self.__alipay_money_moneyback))

    # 获取微信应付金额
    def get_wxpay_money_moneyback(self):
        return float(self.get_text_loc(self.__wxpay_money))

    # 选择充值金额
    def select_amount(self, amount):
        if amount == 100:
            # 点击100元
            self.click_loc(self.__amount_100_loc)
        elif amount == 500:
            # 点击500元
            self.click_loc(self.__amount_500_loc)
        elif amount == 1000:
            # 点击1000元
            self.click_loc(self.__amount_1000_loc)
        elif amount == 5000:
            # 点击5000元
            self.click_loc(self.__amount_5000_loc)
        elif amount == 10000:
            # 点击10000元
            self.click_loc(self.__amount_10000_loc)
        else:
            # 点击其他金额
            sleep(6)
            self.click_loc(self.__amount_other_loc)
            # 输入金额
            self.send_keys_loc(self.__amount_input_loc, str(amount))
            # 点击确定按钮
            self.js_focus_element_loc(self.__confirm_amount_loc, bottom=False)
            self.click_loc(self.__confirm_amount_loc)

    # 选中ali网页，点去充值
    def alichong_zhi(self):
        # 选择ali网银
        self.js_focus_element_loc(self.__ali_qrwy_loc, bottom=False)
        self.click_loc(self.__ali_qrwy_loc)
        # 点击去充值
        self.js_focus_element_loc(self.__qcz_loc)
        self.click_loc(self.__qcz_loc)

    # 选中wx网页，点去充值
    def wxchong_zhi(self):
        # 选择wx网银
        self.js_focus_element_loc(self.__wx_qrwy_loc, bottom=False)
        self.click_loc(self.__wx_qrwy_loc)
        # 点击去充值
        self.js_focus_element_loc(self.__qcz_loc)
        self.click_loc(self.__qcz_loc)

    # 选中个人网页，点去充值
    def personbankchong_zhi(self):
        # 选择个人网银
        self.js_focus_element_loc(self.__personbank_qrwy_loc, bottom=False)
        self.click_loc(self.__personbank_qrwy_loc)
        # 点击去充值
        self.js_focus_element_loc(self.__qcz_loc)
        self.click_loc(self.__qcz_loc)

    # 选中企业网页，点去充值
    def enterprisebankchong_zhi(self):
        # 选择企业网银
        self.js_focus_element_loc(self.__enterprisebank_qrwy_loc, bottom=False)
        self.click_loc(self.__enterprisebank_qrwy_loc)
        # 点击去充值
        self.js_focus_element_loc(self.__qcz_loc)
        self.click_loc(self.__qcz_loc)

    # 订单编号信息
    __order_code_loc = ('xpath', '//div[@class="m_pay_info_l"]//h3[@class="u_order_info"]')

    # 获取订单编号
    def get_order_code(self):
        text = self.get_text_loc(self.__order_code_loc)
        order_code = text.split("付款号：")[1]
        return order_code

    # 个人网银
    __qywy_loc = ('xpath', "//span[text()='个人网银']/preceding-sibling::span")

    # 前往支付
    __qwzf_loc = ('xpath', "//input[@value='前往支付']")

    # 选中个人网页，点前往支付
    def qwzf(self):
        self.js_focus_element_loc(self.__qywy_loc)
        self.click_loc(self.__qywy_loc)
        self.js_focus_element_loc(self.__qwzf_loc)
        self.click_loc(self.__qwzf_loc)

    # --------------------------------第三方页面------------------------------------
    # 登录按钮
    __login_loc = ('xpath', '//*[@id="leftBtn"]/input')

    # 确认支付
    __confirm_order_loc = ('xpath', '//*[@id="cfgBtn"]/input')

    # 登录网银符合
    __double_confirm_loc = ('xpath', '//*[@id="noticeBtn"]/input')

    # 点击登录,并确认 -- 支付
    def sfzf(self):
        # 登录
        self.click_loc(self.__login_loc)
        # 确认支付
        self.click_loc(self.__confirm_order_loc)
        # 返回商城取货
        self.click_loc(self.__double_confirm_loc)
        self.wait_title_change('订单支付成功', timeout=30)
        Log().info(u'跳转到订单支付成功页面')
        from pages.orderPaymentCompletePage import OrderPaymentComplete
        return OrderPaymentComplete(self.driver)

    # 点击登录,并确认  -- 充值
    def ali_sfcz(self):
        # 获取ali支付的金额
        self.alipay_money_moneyback = self.get_alipay_money_moneyback()
        print(self.alipay_money_moneyback)
        # 校验ali支付的金额正确性
        self.Verification_onlinepay(float(self._chongzhi_money), self.alipay_money_moneyback)

    def wx_sfcz(self):
        # 获取wx支付的金额
        self.wxpay_money = self.get_wxpay_money()
        print(self.wxpay_money)
        # 校验wx支付的金额正确性
        self.Verification_onlinepay(float(self._chongzhi_money), self.wxpay_money)

    def personbank_sfcz(self):
        # 点击个人网银支付按钮系列操作
        self.click_person_bank_allpay()
        # 校验支付是否成功
        self.check_personbank_pay_sucess()

    def enterprisebank_sfcz(self):
        # 点击企业网银支付按钮系列操作
        self.click_enterprise_bank_allpay()
        # 校验支付是否成功
        self.check_personbank_pay_sucess()

    # ali充值完整流程
    def ali_chongzhi_workflow(self, amount):
        # 支付页面，选择支付金额
        self.select_amount(amount)
        # 支付页面，选择个人网银，去充值
        self.alichong_zhi()
        # 三方支付
        self.ali_sfcz()

    # wx充值完整流程
    def wx_chongzhi_workflow(self, amount):
        # 支付页面，选择支付金额
        self.select_amount(amount)
        # 支付页面，选择个人网银，去充值
        self.wxchong_zhi()
        # 三方支付
        self.wx_sfcz()

    # 个人银行充值完整流程
    def personbank_chongzhi_workflow(self, amount):
        # 支付页面，选择支付金额
        self.select_amount(amount)
        # 支付页面，选择个人网银，去充值
        self.personbankchong_zhi()
        # 三方支付
        self.personbank_sfcz()

    # 企业银行充值完整流程
    def enterprisebank_chongzhi_workflow(self, amount):
        # 支付页面，选择支付金额
        self.select_amount(amount)
        # 支付页面，选择个人网银，去充值
        self.enterprisebankchong_zhi()
        # 三方支付
        self.enterprisebank_sfcz()


    # —————————在线支付查询验证金额是否正确————————————

    # 在线支付查询结果的第一排信息集合
    __online_payment_select_table1 = ('xpath', '//table[@class="table u_table_query"]//tbody//tr[1]')

    # 打开在线支付查询页面
    def openurl_online_payment_select(self, url, title):

        self.open(url, title='在线支付查询')
        Log().info(u"打开在线支付查询页面: %s" % url)

    # 获取在线支付页第一行的数据集为列表
    def get_online_payment_table_one(self):
        result = self.get_text_loc(self.__online_payment_select_table1)
        result_test = result.split(' ')
        return result_test

    # 在线支付查询页第一行【金额】校验
    def check_money_online_payment(self):
        # 获取在线支付查询页第一行倒数第四位【金额】，格式如：“['2019-01-20', '21:01:25', '无', '￥22', '支付宝', '回款', '未支付']”
        money = float(self.get_online_payment_table_one()[-4].replace('￥', ''))
        if money == float(self._chongzhi_money):
            Log().info("校验在线支付金额正确")
            return True
        else:
            Log().info("校验在线支付金额不正确")
            return False

    # 在线支付查询页第一行【支付方式】校验
    def check_zhifufangshi_online_payment(self, payment_method = "支付宝"):
        # 获取在线支付查询页第一行倒数第四位【金额】，格式如：“['2019-01-20', '21:01:25', '无', '￥22', '支付宝', '回款', '未支付']”
        zhifufangshi = self.get_online_payment_table_one()[-3]
        if zhifufangshi == payment_method:
            Log().info("校验在线支付支付方式正确")
            return True
        else:
            Log().info("校验在线支付支付方式不正确，实际支付方式为 %s" % zhifufangshi)
            return False


    # 在线支付查询页第一行【支付类别】校验
    def check_zhifuleibie_online_payment(self):
        # 获取在线支付查询页第一行倒数第四位【金额】，格式如：“['2019-01-20', '21:01:25', '无', '￥22', '支付宝', '回款', '未支付']”
        zhifuleibie = self.get_online_payment_table_one()[-2]
        if zhifuleibie == "回款":
            Log().info("校验在线支付支付类别正确")
            return True
        else:
            Log().info("校验在线支付支付类别不正确，实际支付类别为 %s" % zhifuleibie)
            return False

    # 校验在线支付查询页所有的项，金额、支付方式、支付类别
    def check_all_online_payment(self, payment_method = "支付宝"):
        # 校验支付金额
        self.check_money_online_payment()
        # 校验支付方式
        self.check_zhifufangshi_online_payment(payment_method)
        # 校验支付
        self.check_zhifuleibie_online_payment()

    # 【支付方式选择页面】前往支付按钮操作
    __to_payment_path = ('xpath', '//input[@class="btn btn-primary ver_mid u_btn_pay"]')

    # 点击前往支付按钮
    def submit_to_paymentpage(self):
        self.click_loc(self.__to_payment_path)

   # 关闭微信二维码页面
    __wx_payment_close = ('xpath', '//*[@id="WXPayLayer"]/div[2]/div[1]/a/i')

    # 获取微信支付页面流水号
    __wx_payment_Serialnumber = ('xpath', '//dd[@id="trxW"]')

    # 点击前往支付，获取第1次的微信支付页流水号M，然后关闭页面，再次点击前往支付，获取第2次的微信支付页流水号N，比较M和N是否不一样，校验微信支付流水号
    def check_wx_payment_Serialnumber(self):
        """获取第1次的微信支付页流水号M，然后关闭页面，再次点击前往支付，获取第2次的微信支付页流水号N，比较M和N是否不一样，校验微信支付流水号，不一样返回true，否则返回false"""
        # # 点击前往支付
        # self.submit_to_paymentpage()
        # 第1次获取微信支付页面流水号
        M = self.get_text_loc(self.__wx_payment_Serialnumber)
        # 点击关闭微信支付页面
        self.click_loc(self.__wx_payment_close)
        # 点击前往支付
        self.submit_to_paymentpage()
        # 第2次获取微信支付页面流水号
        N = self.get_text_loc(self.__wx_payment_Serialnumber)
        if M == N:
            Log().info("微信两次支付流水号一致，不正确，流水号：同一个订单本地流水号不等于上次的流水号")
            return False
        else:
            Log().info("微信两次支付流水号不一致，正确，流水号：同一个订单本地流水号不等于上次的流水号")
            return True


