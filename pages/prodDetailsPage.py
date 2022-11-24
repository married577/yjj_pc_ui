"""商品详情页"""
from common.log import Log
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from common.commonMethod import CommonMethod
from pages.topCommonMenu.baseMenus import BaseMenus
import random
import operator
from time import sleep


class DetailsPage(BaseMenus):

    # ==================================================搜索=====================================================
    # 搜索框
    __search_text_loc = ('xpath', '//*[@id="__layout"]/div/div/div[2]/div/div/div[2]/div[1]/div/div/div[1]/input')
    __search_button_loc = ('xpath', "//div[@class='m_sch_btn']/button")

    # ==============================================打开主页=====================================================
    # 商品详情页地址
    __detial_page_url = CommonMethod().get_endpoint('detailpage')
    # 打开商品详情页
    def open_page(self, prod_no, branchid='FDG'):
        url = self.__detial_page_url + prod_no
        url = url.replace('FDG', branchid)
        self.open(url, title=u'商品详情')
        Log().info(u"打开商品详情页，URL: %s" % url)

    # 搜索
    def search_goods(self, keywords=''):
        sleep(2)
        self.send_keys_loc(self.__search_text_loc, keywords)
        self.enter_key(self.__search_text_loc)
        # self.click_loc(self.__search_button_loc)
        # 等待页面跳转到搜索结果页面
        # self.wait_title_change('商品搜索列表', timeout=30)
        # Log().info(u'跳转到商品搜索列表页面')
        from pages.prodSearchResultPage import SearchResult
        return SearchResult(self.driver)

    # ===========================================商品面包屑操作=====================================================
     # 面包屑元素
    __loc_mianbaoxie = ("xpath", "//div[@class='col-lg-12 col-md-12']/ul/li/a")

    def test_mbx(self, expect_fenlei):
        """验证商品详情页面包屑"""
        result = True
        msg = ''
        # 获取面包屑文本
        actual_fenlei = self.get_text_for_elements(self.__loc_mianbaoxie)
        print(actual_fenlei)
        if operator.eq(actual_fenlei, expect_fenlei):
            pass
        else:
            result = False
            msg = msg + "实际的文本值 ：%s 与期望的文本值 ：%s 不一致" % (actual_fenlei, expect_fenlei)
        return result, msg

    def verify_mbx(self, index, text):
        """
        验证商品详情页的各级面包屑
        :param text:
        :return:
        """
        msg = ''
        mbx = self.get_text_for_elements(self.__loc_mianbaoxie)
        if mbx[index - 1] == text:
            result = True
        else:
            result = False
            msg = msg + "第：%s 级分类和期望的分类值：%s 不一致" % (index, text)
        return result, msg

    # ==============================================商品详细信息=====================================================
    # 商品编码
    __prod_no_loc = ('xpath', "//div[@class='m_sec_bd']//dl/dt[contains(text(),'商品编码')]/following-sibling::dd")
    # 商品名称
    __prod_name_loc = ('xpath', '//div[@class="gd-full_screen"]/div/div[2]/div[2]/h3/span[2]')
    # 商品价格 -- 采购价
    __prod_price_loc = ('xpath', '//span[contains(@class, "u_purc_price")]')
    # 参考零售价
    __prod_retail_loc = ('xpath', '//dl[@class="u_goods_item u_mtp"]//span[@class="u_goods_price col-lg-4"]')
    # 赚
    __prod_earn_money = ('xpath', '//dl[@class="u_goods_item u_mtp"]//span[@class="u_dec_price"]')
    # 毛利率
    __prod_rate_loc = ('xpath', '//dl[@class="u_goods_item u_mtp"]//span[@class="u_retail_rate"]')
    # 商品剂型
    _prod_jixing_loc = ('xpath', '//div[@class="m_goods_mes"]//dt[text()="剂型"]/../dd')
    # 第一个商品名称跳转
    __detail_goods_name_loc = ('xpath', '//div[@class="sr-list-item"][1]//div/div[3]/span')

    # 从搜索页面第一个商品，进入商品详情
    def go_to_proddetail(self):
        # 进入商品详情
        self.click_loc(self.__detail_goods_name_loc)
        # 切换最新窗口
        self.switch_window()
        sleep(2)

    # 获取详情页prodno
    def get_prodno(self):
        return self.get_text_loc(self.__prod_no_loc)

    # 获取详情页prodname
    def get_prodname(self):
        x = self.get_text_loc(self.__prod_name_loc)
        # 去掉获取商品名称的末尾的空格
        return x

    __member_center_loc = ('xpath', '//*[@id="__layout"]/div/div/div[1]/div[1]/div/div[2]/span[3]')

    # 进入会员中心
    def get_member_center(self):
        self.click_loc(self.__member_center_loc)
        # 切换最新窗口
        self.switch_window()
        sleep(2)

    def get_purchase_price(self):
        """
        获取商品的采购价
        :return: 商品的采购价
        """
        text = self.get_text_loc(self.__prod_price_loc)
        return text

    def get_jixing(self):
        """
        获取商品详情页的剂型
        :return: 详情页的剂型
        """
        text = self.get_text_loc(self._prod_jixing_loc)
        return text

    def get_retail_price(self):
        """
        获取商品详情页的 <零售价>
        """
        text = self.get_text_loc(self.__prod_retail_loc)
        return text

    def get_earn_price(self):
        """
        获取商品详情页的<赚>
        :return: 商品详情页的<赚> 金额
        """
        text = self.get_text_loc(self.__prod_earn_money)
        return text

    def get_rate(self):
        """
        获取商品详情页的<毛利率>
        :return:
        """
        text = self.get_text_loc(self.__prod_rate_loc)
        return text

    # ===========================================商品、店铺关注操作=====================================================
    # 关注logo
    # __link_loc = ('link text', u'关注')
    __link_loc = ('xpath', '//div[@class="gd-full_screen"]/div/div[2]/div[1]/div[3]/span')
    __link_store_loc = ('xpath', '//div[@class="si-follow"]/button/span')

    # 点击商品关注
    def click_gz(self):
        # 获取关注文本
        text = self.get_text_loc(self.__link_loc)
        if text == "关注":
            self.click_loc(self.__link_loc)

    # 点击店铺商品关注
    def click_store_gz(self):
        # 获取关注文本
        text = self.get_text_loc(self.__link_store_loc)
        if text == "关注":
            self.click_loc(self.__link_store_loc)

    # 获取商品关注文本，点击关注,查看状态并恢复
    def gz(self):
        # 获取关注文本
        text1 = self.get_text_loc(self.__link_loc)
        # 点击关注
        self.click_loc(self.__link_loc)
        sleep(2)
        # 点击后获取关注文本
        text2 = self.get_text_loc(self.__link_loc)
        # 还原关注状态
        self.click_loc(self.__link_loc)
        sleep(2)
        # 获取关注文本
        text3 = self.get_text_loc(self.__link_loc)
        return text1, text2, text3

    # 获取店铺关注文本，点击关注,查看状态并恢复
    def store_gz(self):
        # 获取关注文本
        text1 = self.get_text_loc(self.__link_store_loc)
        # 点击关注
        self.click_loc(self.__link_store_loc)
        sleep(2)
        # 点击后获取关注文本
        text2 = self.get_text_loc(self.__link_store_loc)
        # 还原关注状态
        self.click_loc(self.__link_store_loc)
        sleep(2)
        # 获取关注文本
        text3 = self.get_text_loc(self.__link_store_loc)
        return text1, text2, text3

    __store_name_loc = ('xpath', '//div[@class="gd-full_screen"]/div/div[2]/div[3]/div[2]/div[2]/h3/span')

    # 获取店铺名称
    def get_store_name(self):
        x = self.get_text_loc(self.__store_name_loc)
        return x

    __store_homepage_loc1 = ('xpath', '//div[@class="si-enter"]/button/span/span')
    __store_homepage_loc2 = ('xpath', '//div[@class="shop-body"]/div[1]/div[2]/div/div[1]/div[1]')

    # 店铺主页跳转,获取店铺主页店铺名称
    def store_homepage(self):
        # 点击进店逛逛
        self.click_loc(self.__store_homepage_loc1)
        # 切换窗口到最新窗口
        self.switch_window()
        sleep(2)
        # 获取店铺主页，店铺名称
        text = self.get_text_loc(self.__store_homepage_loc2)
        return text

    # 点击关注之后，弹出消息
    __msg_loc = ('xpath', "//div[@id='layui-layer1']/div[@class='layui-layer-setwin']")

    # 获取弹出消息的文本
    def get_message_text(self):
        text = self.get_text_loc(self.__msg_loc)
        return text

    __yjj_icon_loc = ('xpath', '//*[@id="__layout"]/div/div/div[2]/div/div/div[1]/div/img')

    # 药九九图标跳转
    def yjj_icon_skip(self):
        # 点击药九九图标
        self.click_loc(self.__yjj_icon_loc)
        # 切换到最新窗口
        self.switch_window()
        sleep(2)

    # ===========================================商品加购操作=====================================================
    # 加购物车
    __add_button_loc = ('xpath', '//*[@id="addToCartButton"]')
    # 商品数量
    __prod_quantity_loc = ('xpath', '//*[@id="merchandiseNumber"]')
    # 加号
    __plus_loc = ('xpath', "//i[contains(@class,'fa-plus')]")
    # 减号
    __minus_loc = ('xpath', "//i[contains(@class,'fa-minus')]")
    # 商品单位
    __prod_unit_loc = ('xpath', "//div[@class='m_goods_nums_wrap']//span[@class='u_goods_unit']")
    # 购物车
    __my_cart_loc = ('xpath', '//*[@id="__layout"]/div/div/div[2]/div/div//div[3]/div/div[2]/div/span[1]')
    # 加购提示
    __add_hint_loc = ('xpath', '/html/body/div[@role="alert"]/p')

    def click_add_to_cart(self):
        """点击加购物车按钮"""
        self.click_loc(self.__add_button_loc)
        Log().info(u"点击加入购物车按钮")

    def get_add_hint(self):
        try:
            # 获取加购成功提示
            text = self.get_text_loc(self.__add_hint_loc)
            return text
        except TimeoutException:
            print(u'没有定位到提示信息')

    # 购物车页面跳转
    def go_to_my_cart(self):
        # 点击购物车跳转
        self.click_loc(self.__my_cart_loc)
        Log().info(u"进入购物车页面")
        # 切换到最新窗口
        self.switch_window()
        sleep(3)

    # 编辑商品数量
    def modify_prod_num(self, num):
        self.send_keys_loc2(self.__prod_quantity_loc, num)
        self.click_loc(self.__prod_unit_loc)
        Log().info(u"编辑商品数量，输入： %s" % num)

    # 获取已输入的商品数量
    def get_prod_num(self):
        return self.get_attribute_loc(self.__prod_quantity_loc, 'value')

    # 增商品(需要做库存限制，暂未实现)
    def plus_prod(self):
        self.click_loc(self.__plus_loc)

    # 减商品
    def minus_prod(self):
        self.click_loc(self.__minus_loc)

    def add_cart_workflow(self, prod_no, num=None, branchid='FDG'):
        """打开商品详情页，编辑采购数量，加入购物车"""
        self.open_page(prod_no,branchid=branchid)
        if num:
            # 编辑采购数量
            self.modify_prod_num(num)
        # 加入购物车
        self.click_add_to_cart()
        # 实际加入购物车的数量
        number = self.get_prod_num()
        return number

    def add_cart_workflow_dic(self, **prod_info):
        """打开商品详情页，编辑采购数量，加入购物车
        :param prod_info为字典格式，格式为：{'prod_no':number,'DYA002010I':1}
        :param prod_no: 商品编码
        :param number: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
        """
        prod_info_new = {}
        for prod_no, num in zip(prod_info.keys(), prod_info.values()):
            self.open_page(prod_no)
            if num:
                # 编辑采购数量
                self.modify_prod_num(num)
            # 加入购物车
            self.click_add_to_cart()
            # 实际加入购物车的数量
            number = self.get_prod_num()
            prod_info_new[prod_no] = number
        return prod_info_new

    # ================================================商品说明信息================================================
    # 商品详情
    __prod_detail_loc = ('xpath', '//div[@class="m_detail_tab"]/span[text()="商品详情"]')
    # 商品参数
    __prod_parmas_loc = ('xpath', "//*[text()='商品参数']")
    # 商品说明书
    __prod_info_loc = ('xpath', '//h4[contains(text(), "商品说明书")]')
    # 器械注册证
    __Instrument_registration_certificate_loc = ('xpath', "//*[text()='器械注册证']")
    # 药监局数据查询
    __link_drug_data = ('xpath', '//*[@id="pane-0"]/div/div[2]/p/a')

    # 根据字段名称检查商品详情页面某元素是否存在
    def check_exist_in_detail_page(self, field_name):
        if field_name == u"商品详情":
            locator = self.__prod_detail_loc
        elif field_name == u"商品参数":
            locator = self.__prod_parmas_loc
        elif field_name == u"商品说明书":
            locator = self.__prod_info_loc
        elif field_name == u"器械注册证":
            locator = self.__Instrument_registration_certificate_loc
        else:
            locator = None
        if locator is None:
            return False
        else:
            sleep(1)
            self.js_focus_element_loc(locator,bottom=False)
            result = self.is_located(locator)
            return result

    # 点击商品详情页里的药监局数据查询，应该进入药监局数据查询页面
    def click_drug_data(self):
        # 滚动条
        self.js_focus_element_loc(self.__link_drug_data)
        self.click_loc(self.__link_drug_data)
        Log().info(u"点击药监局数据查询")
        # 新开页面并且切换到新页面
        self.wait_and_switch_window()

    # ================================================商品极力推荐================================================
    # 极力推荐元素
    __loc_jltj_biaoqian = ("xpath", '//div[@class="pull-right m_goods_rec_wrap"]//span[@class="u_rec_title"]')
    __loc_jltj_mokuai = ('xpath',"//div[@class='m_rec_content']/ul/li")
    __loc_jltj_noimg = ("xpath", "//div[@class='m_rec_hd']/div[@class='m_rec_no_content']/img")
    __loc_jltj_notext = ("xpath", '//div[@class="pull-right m_goods_rec_wrap"]//p[@class="u_desc"]')
    __loc_jltj_prno = ('xpath',"//div[@class='m_rec_content']/ul/li//a[@class='u_goods_tit']")

    def test_jltj(self, expect_text):
        """验证商品详情页极力推荐标签"""
        result = True
        msg = ''
        # 获取标签文本
        actual_text = self.get_text_for_elements(self.__loc_jltj_biaoqian)
        print(actual_text)
        if operator.eq(actual_text, expect_text):
            pass
        else:
            result = False
            msg = msg + "实际的文本值 ：%s 与期望的文本值 ：%s 不一致" % (actual_text, expect_text)
        return result, msg

    def is_jltj_mokuai_exist(self):
        """
        判断智能推荐模块是否显示
        :return: 存在返回True，否则返回False
        """
        result = True
        try:
            self.find_element_presence(self.__loc_jltj_mokuai, timeout=2)
        except TimeoutException:
            result =  False
        return result

    def jltj_prod(self):
        """
        随机点击一个极力推荐的商品
        """
        prod_list = self.find_elements(self.__loc_jltj_prno)
        count = len(prod_list)
        # print(count)
        # 获取随机数, 大于5需要点击向下箭头
        if count > 4:
            x = random.randint(1, 4)
        else:
            x = random.randint(1, count)
        print("极力推荐点击第%s个" % x)
        # 获取商品名称和编码
        ele = prod_list[x-1]
        attr = self.get_attribute_ele(ele, 'href')
        prodno = attr.split('?')[0].split('/')[-1]
        prodname = self.get_text_ele(ele)
        print("点击的极力推荐的商品编码和名称是%s和%s " % (prodno, prodname))
        # 点击该商品的title
        self.js_focus_element_ele(ele)
        self.click_element(ele)
        return prodno, prodname

    def is_jltj_img_exist(self):
        """
        判断极力推荐无商品的图片是否显示
        :return: 存在返回True，否则返回False
        """
        try:
            self.find_element_presence(self.__loc_jltj_noimg, timeout=2)
            return True
        except TimeoutException:
            return False

    def test_jltj_notext(self):
        """验证商品详情页极力推荐无商品提示语"""
        # 获取标签文本
        actual_text = self.get_text_loc(self.__loc_jltj_notext)
        return actual_text

    # 咨询客服按钮
    __consulting_customer_servise = ('xpath', '//div[@class="si-customer_service"]/button/span')

    def check_page_after_click_customer_servise(self):
        """
        判断点击咨询客服之后，页面跳转是否正确，用页面标题判断
        :return: 跳转正确返回True,否则返回False
        """
        self.js_focus_element_loc(self.__consulting_customer_servise)
        self.click_loc(self.__consulting_customer_servise)
        Log().info(u"点击咨询客服")
        sleep(2)

    __service_page_text_loc = ('xpath', '//div[@id="em-kefu-webim-chat"]//span[@class="em-widget-header-nickname"]')

    # 客服页面校验文本获取
    def get_service_page_text(self):
        Log().info(u"店铺客服页面")
        # 获取校验文本
        text = self.get_text_loc(self.__service_page_text_loc)
        return text

    # ================================================商品店铺操作================================================

    def click_shop_to_shop(self):
        pass

    # ===================================================页面等待================================================

    def wait_detail_page_refresh(self, timeout=10):
        """
        等待页面某元素过期，即等带页面刷新,此页面用搜索按钮判断
        这里商品详情页的搜索按钮若过期，代表页面已经刷新（已经打开别的页面）
        """
        try:
            self.wait_element_staleness(self.__search_button_loc, timeout)
        except (TimeoutException, NoSuchElementException):
            pass

    def wait_detail_page_load(self, timeout=10):
        """等待详情页打开"""
        try:
            self.is_title_contains(u"商品详情", timeout)
        except TimeoutException:
            pass

    def wait_member_refresh(self, timeout=20):
        """
        等待页面某元素过期，即等带页面刷新,此页面用搜索按钮判断
        这里会员中心的搜索按钮若过期，代表页面已经刷新（已经打开别的页面）
        """
        try:
            self.wait_element_staleness(self.__search_button_loc, timeout)
        except (TimeoutException, NoSuchElementException):
            pass


















