# coding: utf-8
"""商品搜索列表页面"""

from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
from common.log import Log
import re
from pages.topCommonMenu.baseMenus import BaseMenus
from common.commonMethod import CommonMethod
from common.log import Log
from pages.pageCommonMethod.home_special import HomeAndSpecial
import operator
from time import sleep
from common.fileReader import IniUtil


class SearchResult(BaseMenus):

    f = IniUtil()

    # ==================================================打开搜索结果页面==========================================
    # 搜索结果页地址
    __result_page_url = CommonMethod().get_endpoint('resultpage')

    # 打开搜索商品列表页面
    def open_search_result_page(self, url=__result_page_url, keyword=None):
        if keyword:
            url = url + "?keyword=%s" % keyword
        self.open(url, '商品搜索列表 - 九州通网')

    # ======================================搜索判断===================================================

    def is_name_contain_keyword(self, keywords):
        """判断商品搜索列表中，是否所有商品名称都包含商品名称关键字（商品名称的部分）"""
        result = True
        if len(self.get_prods_list()) > 0:
            list_n = self.get_attribute_for_elements(self.__prod_bigPicture_name, 'onclick')
            for p in list_n:
                name = p.split(',')[3]
                print("商品搜索列表的名称为 :% s " % name)
                if keywords not in name:
                    result = False
        else:
            result = False
        return result

    # 生产厂家
    __manufacturer_bigPicture = (
    'xpath', '//ul[@id="list_big_pic"]/li[not(div[3]!="")]/span[4][@class="u_goods_com text-overflow"]')

    def is_manufacturer_contain_keyword(self, keywords):
        """判断商品搜索列表中，是否所有商品的生产厂商名称都包含生产厂商关键字（生产厂商的部分）"""
        result = True
        if len(self.get_prods_list()) > 0:
            list_m = self.get_text_for_elements(self.__manufacturer_bigPicture)
            for m in list_m:
                if keywords not in m:
                    result = False
                    print("关键为{},其中不包含关键字名称为{}".format(keywords, m))
        else:
            result = False
        return result

    # 搜索框
    __search_text_loc = ('xpath', '//*[@id="searchText"]')
    __search_button_loc = ('xpath', "//div[@class='m_sch_btn']/button")

    # 获取搜索框的值
    def get_text_in_search_textbox(self):
        text = self.get_attribute_loc(self.__search_text_loc, 'value')
        return text

    # 搜索
    def search_goods(self, keywords=''):
        sleep(2)
        self.send_keys_loc(self.__search_text_loc, keywords)
        self.enter_key(self.__search_text_loc)

    # ==============================================搜索过滤区域=======================================================
    # 综合按钮
    __general_loc = ('xpath', "//a[text()='综合']")
    # 销量按钮
    __sale_loc = ('xpath', "//a[text()='销量']")
    # 享优惠按钮
    __promotion_loc = ('xpath', '//input[@id="isPromotion"]/following-sibling::span[1]')
    # 历史采购按钮
    __history_loc = ('xpath', '//input[@id="isHistory"]/following-sibling::span[1]')
    # 只看有货按钮
    __haveStorage_loc = ('xpath', '//input[@id="haveStorage"]/following-sibling::span[1]')
    # otc 按钮
    __otc__button_loc = ('xpath', '//div[@class="checkbox"]//input[@id="otc"]/following-sibling::span[1]')
    # 处方药 按钮
    __chuf__button_loc = ('xpath', '//div[@class="checkbox"]//input[@id="chuf"]/following-sibling::span[1]')
    # 搜索过滤区-价格的下限
    __price_down_loc = ('xpath', '//input[@id="startPrice"]')
    # 搜索过滤区-价格的上限
    __price_up_loc = ('xpath', '//input[@id="endPrice"]')
    # 搜索过滤区-确定按钮
    __price_confirm = ('xpath', '//a[text()="确定"]')
    # 搜索结果列表中-历史采购标签-列表模式
    __history_list_loc = ('xpath', '//span[@class="u_img_wrap"]/following-sibling::span[@class="u_img_num_hos"]')
    # 搜索结果列表中-历史采购标签-大图模式
    __history_big_loc = ('xpath', '//ul[@id="list_big_pic"]/li[not(div[3]!="")]//div[@class="coupon_box"]/span')
    # 搜索结果列表中的otc/处方药的值--列表模式
    __prod_otc_list = ('xpath', '//ul[@id="list_no_pic"]//span[@class="m_tag m_tag_bq"]')
    # 搜索结果列表中的otc/处方药的值--大图模式
    __prod__otc_big = ('xpath', '//ul[@id="list_big_pic"]/li[not(div[3]!="")]/span[3]/i')
    # 搜索结果列表中-库存-大图模式
    __kucun_big_loc = ('xpath', '//ul[@id="list_big_pic"]/li//div[@class="stock"]/text()')
    # 搜索结果列表中-本地库存-列表模式
    __kucun_list_loc = ('xpath', '//p[@class="u_goods_stock"]/span[@class="u_goods_txt"]')

    def click_general_button(self):
        """
        搜索结果列表点击"综合"按钮
        :return:
        """
        self.click_loc(self.__general_loc)
        Log().info("搜索结果列表点击综合按钮")

    def click_sale_button(self):
        """
        搜索结果列表点击"销量"按钮
        :return:
        """
        self.click_loc(self.__sale_loc)
        Log().info("搜索结果列表点击销量按钮")

    def click_promotion_button(self):
        """
        搜索结果列表点击"享优惠"按钮
        :return:
        """
        self.click_loc(self.__promotion_loc)
        Log().info("搜索结果列表点击享优惠按钮")

    def click_history_button(self):
        """
        搜索结果列表点击"历史采购"按钮
        :return:
        """
        self.click_loc(self.__history_loc)
        Log().info("搜索结果列表点击历史采购按钮")

    def click_storage_loc(self):
        """
        搜索结果列表页点击"只看有货"按钮
        :return:
        """
        # 点击"只看有货"按钮
        self.click_loc(self.__haveStorage_loc)
        self.wait_result_page_refresh()
        Log().info("搜索结果列表点击只看有货按钮")

    def click_otc_button(self):
        """
        搜索结果列表点击"otc"按钮
        :return:
        """
        self.click_loc(self.__otc__button_loc)
        Log().info("搜索结果列表筛选栏点击OTC按钮")

    def click_chuf_button(self):
        """
        搜索结果列表点击"处方药"按钮
        :return:
        """
        self.click_loc(self.__chuf__button_loc)
        Log().info("搜索结果列表筛选栏点击处方药按钮")

    def is_attribute_contain_keyword(self, keywords):
        """判断商品搜索列表中，药品属性包含关键字：OTC或者处方药"""
        result = True
        if len(self.get_prods_list()) > 0:
            list_m = self.get_text_for_elements(self.__prod__otc_big)
            Log().info("商品的属性为:%s" % list_m[1])
            for m in list_m:
                if keywords not in m:
                    result = False
                    Log().info("商品搜索列表，筛选项为：%s，商品的实际属性为：%s" % (keywords, m))
        else:
            result = False
        return result

    def is_history_contain(self):
        """判断商品搜索列表中，包含关键字：【历史采购】"""
        result = True
        if len(self.get_prods_list()) > 0:
            text = self.get_text_for_elements(self.__history_big_loc)
            if "历史购买" not in text:
                result = False
                Log().info("商品搜索列表筛选历史采购商品，期望值是：历史采购，实际值为：%s" % text)
        else:
            Log().info("商品搜索列表筛选历史采购无数据！")
            result = False
        return result

    def is_has_storage(self):
        """判断商品搜索列表中全部商品有货"""
        result = True
        sleep(1)
        if len(self.get_prods_list()) > 0:
            text = self.get_text_for_elements(self.__kucun_list_loc)
            print(text)
            text2 = [i for i in text if float(i) <= 0]
            if len(text2) > 0:
                result = False
            if "无" in text:
                result = False
                Log().info("搜索有货商品时错误出现无库存商品")
        else:
            Log().info("商品搜索列表筛选历史采购无数据！")
            result = False
        return result

    def price_rank(self, down, up):
        """
        搜索结果商品列表，筛选栏-价格，输入上限和下限
        :param down: 价格区间-下限
        :param up: 价格区间-上限
        :return:
        """
        # 鼠标首先点击一下价格框的下限，整个控件才会出来
        self.click_loc(self.__price_down_loc)
        # 点击价格框的下限和上限
        self.send_keys_loc(self.__price_down_loc, down)
        self.send_keys_loc(self.__price_up_loc, up)

    def price_enter(self, down, up):
        """
        搜索结果商品列表，筛选栏-价格，输入上限和下限，点击enter键
        :param down: 价格区间-下限
        :param up: 价格区间-上限
        :return:
        """
        # 输入价格框的下限和上限
        self.price_rank(down, up)
        # 价格区间下限框输入enter
        self.enter_key(self.__price_up_loc)

    def price_confirm(self, down, up):
        """
        搜索结果商品列表，筛选栏-价格，输入上限和下限，点击确定按钮
        :param down: 价格区间-下限
        :param up: 价格区间-上限
        :return: 包含
        """
        # 输入价格框的下限和上限
        self.price_rank(down, up)
        self.js_focus_element_loc(self.__price_confirm)
        try:
            result = self.is_clickable(self.__price_confirm)
        except TimeoutException:
            result = False
        if result:
            # 点击价格框的确定按钮
            self.click_loc(self.__price_confirm)
        return result

    # 在结果中搜索
    __search_in_result_text_loc = ('xpath', "//input[@placeholder='在结果中搜索']")
    # 在结果中搜索的搜索按钮
    __search_in_result_button_loc = ('xpath', "//input[@placeholder='在结果中搜索']/following-sibling::i[1]")

    # 在结果中搜索输入框输入关键字搜索
    def search_goods_in_search_result(self, keywords):
        # 滚动滚动条将搜索框显示出来
        self.js_focus_element_loc(self.__search_in_result_text_loc)
        # 在搜索输入框内输入关键字
        self.send_keys_loc(self.__search_in_result_text_loc, keywords, clear_first=False, click_first=True)
        # 点击搜索
        self.click_loc(self.__search_in_result_button_loc)

    # 随机点击剂型的前10个(后面的剂型需要点击更多按钮)并且返回点击剂型的名称
    def click_jixing(self):
        i = random.randint(1, 10)
        # 剂型的前10个
        _search_jx = ("xpath", "//div[@class='m_cond_con m_cond_jx']/ul/li[" + str(i) + "]/a")
        # 获取点击的剂型的名称
        text = self.get_text_loc(_search_jx)
        Log().info("搜索结果列表点击第：%s 个剂型" % i)
        self.click_loc(_search_jx)
        Log().info("搜索结果列表点击的剂型为：%s" % text)
        return text

    # 剂型后面的更多链接
    __more_of_jx = ('xpath', '//div[text()="剂型"]/..//a[@class="m_cond_more"]')
    # 剂型列表的最后一个元素
    __last_jx_in_list = ('xpath', '//div[text()="剂型"]/..//div[contains(@class, "m_cond_jx")]/ul/li[last()]/a')

    # 点击剂型后面的更多链接
    def click_more_of_jx(self):
        self.click_loc(self.__more_of_jx)

    # 获取剂型后面的更多链接的文本
    def get_text_of_jx(self):
        text = self.get_text_loc(self.__more_of_jx)
        return text

    # 判断剂型列表的最后一个元素是否显示
    def is_last_jx_dispay(self):
        result = self.is_display(self.__last_jx_in_list)
        return result

    # 生产厂家后面的更多链接
    __more_of_sccj = ('xpath', "//div[text()='生产厂家']/following-sibling::div/div/a")
    # 生产厂家列表的最后一个元素
    __last_sccj_in_list = ('xpath', "//div[text()='生产厂家']/following-sibling::div//ul/li[last()]/a")

    # 随机点击生产厂家的前6个(后面的生产厂家需要点击更多按钮)并且返回点击厂家的名称
    def click_sccj(self):
        i = random.randint(1, 6)
        # 生产厂家的前5个  //div[@class="member-list-inner"]/ul/li[6]/a
        _search_sccj = ("xpath", "//div[@class='member-list-inner']/ul/li[" + str(i) + "]/a")
        # 获取点击的生产厂家的名称
        text = self.get_text_loc(_search_sccj)
        Log().info("搜索结果列表点击第：%s 个生产厂家" % i)
        self.click_loc(_search_sccj)
        Log().info("搜索结果列表点击的生产厂家为：%s" % text)
        return text

    # 点击生产厂家后面的更多链接
    def click_more_of_sccj(self):
        self.click_loc(self.__more_of_sccj)

    # 获取生产厂家后面的更多链接的文本
    def get_text_of_sccj(self):
        text = self.get_text_loc(self.__more_of_sccj)
        return text

    # 判断生产厂家列表的最后一个元素是否显示
    def is_last_sccj_dispay(self):
        result = self.is_display(self.__last_sccj_in_list)
        return result

    # 生产厂家列表的第一个元素
    __first_sccj_in_list = ('xpath', "//div[text()='生产厂家']/following-sibling::div//ul/li[1]/a")

    # 点击生产厂家列表的第一个元素
    def click_sccj_in_list(self):
        self.click_loc(self.__first_sccj_in_list)

    # ===================================================商品列表商品信息================================================

    # 商品名称连接
    __prod_bigPicture_name = ('xpath', '//ul[@id="list_big_pic"]/li[not(div[3]!="")]/span[@class="u_goods_tit text-overflow"]/a')

    def get_prods_list(self):
        """
        获取商品列表对象
        :return: 商品列表对象的list
        """
        prod_list = []
        try:
            prod_list = self.find_elements(self.__prod_bigPicture_name)
        except TimeoutException:
            print("商品列表无数据！")
        return prod_list

    def count_of_list(self):
        """
        获取商品列表数量
        :return: 列表中商品的数量
        """
        return len(self.get_prods_list())

    def get_prodno_in_list(self):
        """
        获取商品列表中，任意一个商品的prodno
        :return: 商品编码
        """
        count = self.count_of_list()
        prodno = None
        if count > 0:
            # 获得一个商品数量的随机整数
            x = random.randint(0, count-1)
            # 拿到商品列表中的一个随机商品
            ele = self.get_prods_list()[x]
            self.js_focus_element_ele(ele)
            # 获取该商品的prodno
            attr = self.get_attribute_ele(ele, 'onclick')
            prodno = attr.split(',')[4].replace("'", '').strip()
            print("获取商品列表中，任意一个商品的prodno为%s" % prodno)
        return prodno

    def is_prod_in_list(self, prodno):
        """
        根据prodno来判断商品是否在商品列表中
        :param prodno: 商品编码
        :return: 商品在列表中，返回true，否则返回false
        """
        result = False
        if len(self.get_prods_list()) > 0:
            list_p = self.get_attribute_for_elements(self.__prod_bigPicture_name, 'onclick')
            for p in list_p:
                prod_no = p.split(',')[4].replace("'", '').strip()
                print(prod_no)
                if prodno == prod_no:
                    result = True
        return result

    # 获取搜索列表全部结果后面的分类文本
    __searchresult_prod_class_text_loc = ('xpath','//ul[@class="breadcrumb"]//li/a[@class="m_tag m_tag_l4 fixbox"]')

    def get_searchresult_prod_class_text(self):
        """获取搜索列表全部结果后面的分类文本"""
        try:
            text = self.get_text_for_elements(self.__searchresult_prod_class_text_loc)
        except:
            text = []
            Log().info('搜索结果页面无分类名称')
        return text

    # =======================================商品价格相关=======================================================

    # 商品价格
    __price_bigPicture = ('xpath', '//ul[@id="list_big_pic"]/li[not(div[3]!="")]//span[@class="Price"]/span[contains(@class,"memberPrice")]')

    def get_price_of_original(self):
        """
        获取商品的原始价格
        :return:
        """
        result = True
        if len(self.get_prods_list()) > 0:
            list_p = self.get_text_for_elements(self.__price_bigPicture)
            print(list_p)
        else:
            result = False
        return result, list_p

    def is_price_displayed(self):
        """#判断商品搜索列表中，商品价格是否显示（显示价格或者显示登录可见）"""
        result = True
        if len(self.get_prods_list()) > 0:
            list_p = self.get_text_for_elements(self.__price_bigPicture)
            for p in list_p:
                if u'登录可见' in p:
                    result = False
        else:
            result = False
        return result

    def is_price_contain(self, down, up):
        """判断搜索结果商品列表页，商品的价格区间是否为指定的区间"""
        result1, price_list = self.get_price_of_original()
        result = True
        for i in price_list:
            if down <= float(i) <= up:
                result = True
            else:
                result = False
        return result

    # =======================================商品图片或名称操作===============================================

    def click_title_random(self):
        """
        任意点击搜索结果列表中的一个商品的名称，并返回该商品prodno和prodname
        :return: 商品编码 -- prodno和商品名称 -- prodname
        """
        count = self.count_of_list()
        prodno = None
        prodname = None
        if count > 0:
            sleep(1)
            sleep(1)
            # 获得一个商品数量的随机整数
            x = random.randint(0, count-1)
            # 拿到商品列表中的一个随机商品
            ele = self.get_prods_list()[x]
            self.js_focus_element_ele(ele)
            # 获取该商品的prodno和prodname
            attr = self.get_attribute_ele(ele, 'onclick')
            prodno = attr.split(',')[4].replace("'", '').strip()
            prodname = attr.split(',')[3].replace("'", '').strip()
            # 点击该商品的title
            self.click_element(ele)
        return prodno, prodname

    #  商品图片
    __prod_pic_bigPicture = ('xpath', '//ul[@id="list_big_pic"]/li[not(div[3]!="")]/a[@class="drug_img f_fl"]')

    def click_picture_random(self):
        """
        任意点击搜索结果列表中的一个商品的图片，并返回该商品prodno和prodname
        :return: 商品编码 -- prodno和商品名称 -- prodname
        """
        count = self.count_of_list()
        prodno = None
        prodname = None
        if count > 0:
            # 获取所有商品图片
            # pictures = self.find_elements(self.__prod_pic_list_loc)
            pictures = self.find_elements_visibility(self.__prod_pic_bigPicture)
            x = random.randint(0, count-1)
            # 拿到商品列表中的一个随机商品
            ele = pictures[x]
            self.js_focus_element_ele(ele)
            # 获取该商品的prodno和prodname
            attr = self.get_attribute_ele(ele, 'onclick')
            prodno = attr.split(',')[4].replace("'", '').strip()
            prodname = attr.split(',')[3].replace("'", '').strip()
            # 点击该商品的图片
            self.click_element(ele)
        return prodno, prodname

    # =======================================加购物车，加缺货篮操作======================================

    # 加购物车按钮列表
    __add_to_cart_buttons_big = ('xpath', '//ul[@id="list_big_pic"]//a[contains(text(),"加购物车")]')
    # 加缺货栏按钮列表-大图模式
    __add_to_basket_buttons_big = ('xpath', '//ul[@id="list_big_pic"]//a[contains(text(),"到货通知")]')
    # 下一页按钮
    __next_button_loc = ('xpath', "//span[text()='下一页']")
    # 上一页按钮
    __before_button_loc = ('xpath', "//span[text()='上一页']")
    # 尾页按钮
    __last_button_loc = ('xpath', "//span[text()='尾页']")
    # 首页按钮
    __first_button_loc = ('xpath', "//span[text()='首页']")
    # 分页数量
    __page_totals_loc = ('xpath', "//span[@class='pagination-info']")

    def total_pages(self):
        """
        获取分页总数
        :return: 分页总数
        """
        # 获取文本
        text = self.get_text_loc(self.__page_totals_loc)
        # 提取出中间的数字
        pages = int(re.sub("\D", "", text))
        return pages

    def click_page_navigation_button(self, name):
        """
        点击页面导航按钮
        :param name: 导航名称：尾页，上一页，下一页，首页
        :return:
        """
        if name == "尾页":
            locator = self.__last_button_loc
        elif name == "上一页":
            locator = self.__before_button_loc
        elif name == "下一页":
            locator = self.__next_button_loc
        else:
            locator = self.__first_button_loc
        # 聚焦到按钮上
        self.js_focus_element_loc(locator)
        # 点击按钮
        self.click_loc(locator)

    def find_page_to_add_cart(self):
        """
        找出有可加购物车的搜索页面（至少有一个商品可加购物车）
        :return:
        """
        # 先从当前页面（即首页）查找,可加入购物车的商品数量
        count = len(self.__get_prods_cart())
        Log().info(("当前页面可加入购物车的商品数量为：{}".format(count)))
        if count is 0:
            # 如果数量是0，则点击下一页，直到count大于0为止
            pages = self.total_pages()
            for i in list(range(1, pages-1)):
                # 点击下一页
                self.click_page_navigation_button('下一页')
                Log().info("打开商品分页第:{}页".format(i+1) )
                # 等待页面刷新
                self.wait_result_page_refresh()
                # 获取当前页面可加入缺货篮的商品数量
                count = len(self.__get_prods_cart())
                if count > 0:
                    # 如果count大于0，跳出循环
                    break

    def find_page_to_add_basket(self):
        """
        找出有可加缺货篮的搜索页面（至少有一个商品可加缺货篮）
        :return:
        """
        # 先从当前页面（即首页）查找,可加入缺货篮的商品数量
        count = len(self.__get_prods_basket())
        Log().info(("当前页面可加入缺货栏的商品数量为：{}".format(count)))
        if count is 0:
            sleep(1)
            # 如果当前页面没有可加入缺货篮的商品，则点击尾页按钮
            self.click_page_navigation_button('尾页')
            Log().info("打开商品分页的最后一页")
            # 等待页面刷新
            self.wait_result_page_refresh()
            # 获取当前页面可加入缺货篮的商品数量
            count = len(self.__get_prods_basket())
            if count is 0:
                # 如果数量还是0，则点击上一页，直到count大于0为止
                pages = self.total_pages()
                for i in list(range(1, pages-1)):
                    # 点击上一页
                    self.click_page_navigation_button('上一页')
                    Log().info("打开商品分页倒数第%s页" % (i+1))
                    # 等待页面刷新
                    self.wait_result_page_refresh()
                    # 获取当前页面可加入缺货篮的商品数量
                    count = len(self.__get_prods_basket())
                    if count > 0:
                        # 如果count大于0，跳出循环
                        break

    def __get_prods_cart(self):
        """
        获取加购物车button列表(前提是在有可加购物车的搜索页面),为1代表列表模式，2代表大图模式
        :return: 加购物车按钮的对象列表
        """
        prod_list = []
        # 获取商品列表的模式，为1代表列表模式，2代表大图模式
        try:
            prod_list = self.find_elements(self.__add_to_cart_buttons_big)
        except TimeoutException:
            Log().info(u"当前搜索页面无商品可加入购物车！.")
        return prod_list

    def __get_prods_basket(self):
        """
        获取加缺货篮button列表(前提是在有可加缺货篮的搜索页面)
        :return: 加缺货篮按钮的对象列表
        """
        prod_list = []
        # 获取商品列表的模式，为1代表列表模式，2代表大图模式
        try:
            prod_list = self.find_elements(self.__add_to_basket_buttons_big)
        except TimeoutException:
            Log().info(u"当前搜索页面无商品可加入缺货篮！")
        return prod_list

    def find_a_prod(self):
        elements = self.__get_prods_cart()
        count = len(elements)
        if count > 0:
            # 生成0到count-1的随机数
            x = random.randint(0, count - 1)
            #  获取列表中第x个商品的加购物车/加缺货篮按钮
            element = elements[x]
            # 获取商品的onlcick属性，提取出ProdNo
            onclick = self.get_attribute_ele(element, 'onclick')
            # 商品编码
            prodno = onclick.split(',')[2].lstrip(' ').strip("'")
            return prodno

    def add_to_basket_or_cart_random(self, number, to_cart=True):
        """
        商品搜索结果页面，随机选择一个商品加购物车或者加缺货篮
        :param number: 添加缺货篮的数量
        :param to_cart: 是否加购物车，True加购物车，否则加缺货篮
        :return: 商品编码，加购物车/缺货篮数量
        """
        if to_cart:
            elements = self.__get_prods_cart()
        else:
            elements = self.__get_prods_basket()
        count = len(elements)
        if count > 0:
            # 生成0到count-1的随机数
            x = random.randint(0, count - 1)
            #  获取列表中第x个商品的加购物车/加缺货篮按钮
            element = elements[x]
            # 获取商品的onlcick属性，提取出ProdNo
            onclick = self.get_attribute_ele(element, 'onclick')
            # 商品编码
            prodno = onclick.split(',')[3].lstrip(' ').strip("'")
            Log().info("加购的商品编码为：{}".format(prodno))
            # li_parent = ('xpath', '//a[@proid="{}"]/..'.format(prodno))
            # 父节点li
            li_locator = ('xpath', './ancestor::li')
            parent = self.find_element_based_on_element(element, li_locator)
            # 数量编辑框
            input_locator = ('xpath', './/input[@type="text"]')
            input_element = self.find_element_based_on_element(parent, input_locator)
            # 大图模式，鼠标需要悬停商品区域，加购按钮才会出来
            self.move_to_element_ele(parent)
            # 数量编辑框中输入数字
            self.js_focus_element_ele(input_element)
            self.send_keys_ele(input_element, number)
            # 点击加购物车/加缺货篮按钮
            sleep(2)
            self.js_focus_element_ele(element)
            self.click_element(element)
            # 获取输入框的数字即真正加入购物车的数量
            actual_number = self.get_attribute_ele(input_element, 'value')
        else:
            Log().info(u"当前搜索页面无商品可加入购物车！")
            prodno, actual_number = None, None
        return prodno, actual_number

    def add_to_basket_or_cart_random_workflow(self, number, keyword=None, to_cart=True):
        """
        从打开搜索结果页到找到加缺货篮/购物车的分页，到随机找一个商品，编辑数量，加缺货篮/购物车
        :param number: 数量
        :param keyword: 搜索的keyword
        :param to_cart: 是否加购物车，True加购物车，否则加缺货篮
        :return: 加缺货篮/购物车的商品编码，以及加缺货篮/购物车的数量
        """
        # 打开搜索结果页面
        self.open_search_result_page(keyword=keyword)
        sleep(1)
        if to_cart:
            self.find_page_to_add_cart()
        else:
            self.find_page_to_add_basket()
        # 加购物车/缺货篮
        result = self.add_to_basket_or_cart_random(number, to_cart)
        return result

    # =====================================根据指定prodno来加购物车以及其他操作=======================================
    """商品搜索页面，用prodno搜索出有库存的测试商品，加购物车---- 列表只有一条数据"""

    # 加购物车按钮
    __add_button_loc = ('xpath', '//div[@class="m_goods_action "]/button')
    # 编辑输入框
    __edit_loc = ('xpath', '//span[@class="input-group"]//input')
    # 输入框后面的单位
    __unit_loc = ('xpath', '//div[@class="m_goods_nums_wrap"]//span[@class="u_goods_unit"]')
    # 库存
    __stock_loc = ('xpath', '//span[@class="u_goods_txt"]')
    # 加号
    __plus_loc = ('xpath', "//i[contains(@class, 'fa-plus')]")
    # 减号
    __minus_loc = ('xpath', "//i[contains(@class,'fa-minus')]")
    # 采购价
    __prod_price_loc = ('xpath', '//span[@class="u_goods_pric"]')

    def get_purchase_price(self):
        """
        获取商品的采购价
        :return:
        """
        text = self.get_text_loc(self.__prod_price_loc)
        return float(text)

    # 会员平台价
    __platform_price_loc = ('xpath', '//p[@class="m_goods_platformpric"]')

    def get_platform_price(self):
        """
        获取商品的平台价价
        :return:
        """
        text = self.get_text_loc(self.__platform_price_loc).split('¥')[1]
        return float(text)

    # 非会员登陆会员价
    __member_price_loc = ('xpath', '//p[@class="m_goods_memberpric"]')

    def get_member_price(self):
        """
        获取商品的平台价价
        :return:
        """
        text = self.get_text_loc(self.__member_price_loc).split('¥')[1]
        return float(text)

    # 获取该商品的prodno和库存
    def get_prod_info(self):
        prodno = self.get_attribute_loc(self.__edit_loc, 'id')[17:]
        stock = self.get_text_loc(self.__stock_loc)
        Log().info(u"商品搜索列表页面，测试加购物车的测试商品为：%s, 库存为：%s" % (prodno, stock))
        return prodno, stock

    # 编辑商品数量，加购物车
    def add_to_cart(self, num=None):
        """
        编辑商品数量，加入购物车
        :param num: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
        :return:
        """
        if num:
            # 编辑商品数量
            self.modify_prod_num(num)
        self.click_loc(self.__add_button_loc)
        Log().info(u"点击加入购物车按钮")

    # 大图模式下的商品
    __prod_big_name = ('xpath', '//ul[@id="list_big_pic"]/li/a[@class="drug_img f_fl"]')

    def bigpic_prod_number(self, prod, num):
        """
        大图商品数量加购数量
        :param prod: 商品编码
        :param num: 加购数量
        :return:
        """
        # 输入框定位元素
        __number_input_loc = ('xpath','//input[@id="merchandiseNumberBigPic{}"]'.format(prod))
        # 鼠标焦点移除定位
        __bigpic_delete_choose_num_loc = ('xpath', '//div[@class="kucun"]/span[1]')
        # 点击大图加购
        bigpic_add_prod_loc = ('xpath', '//a[@class="addCatBtn"]')
        # 输入框定位
        self.move_to_element(self.__prod_big_name, timeout=20)
        if num:
            self.send_keys_loc2(__number_input_loc, num)
            Log().info(u"大图模式编辑商品数量，输入： %s" % num)
            # 鼠标点击单位  ----- 将鼠标焦点从输入框移除
            self.click_loc(__bigpic_delete_choose_num_loc)
        # 点击加购
        self.click_loc(bigpic_add_prod_loc)

    def add_cart_workflow(self, prod_no, num=None,sing=None):
        """
        打开只有目标商品的搜索结果页，将该商品加入购物车
        :param num: 加购的数量，默认为None，即不编辑数量，直接以默认值加购
        :param prod_no: 加购商品
        :return:
        """
        # 打开
        self.open_search_result_page(keyword=prod_no)
        sleep(2)
        # 加购
        self.bigpic_prod_number(prod_no,num=num)

    def add_prods_to_cart_workflow(self, prod_info):
        """
        加购商品进入购物车
        :param prod_info: {'proda':12,'prodb':''}
        :return:
        """
        for item in prod_info.items():
            prod_no = item[0]
            number = item[1]
            print(prod_no, number)
            self.add_cart_workflow(prod_no, number)

    def add_cart_workflow_dic(self, **prod_info):
        """
        从搜索列表添加多个商品到购物车
        :param prod_info: {'proda':12,'prodb':''}
        :return:
        """
        prod_info_new = {}
        for item in prod_info.items():
            prod_no = item[0]
            number = item[1]
            print(prod_no, number)
            self.add_cart_workflow(prod_no, number)
            # 实际加入购物车的数量
            number = self.get_prod_num()
            prod_info_new[prod_no] = number
        return prod_info_new

    # 编辑商品数量
    def modify_prod_num(self, num):
        # 输入框输入
        self.send_keys_loc2(self.__edit_loc, num)
        Log().info(u"编辑商品数量，输入： %s" % num)
        # 鼠标点击单位  ----- 将鼠标焦点从输入框移除
        self.click_loc(self.__unit_loc)

    # 获取已输入的商品数量
    def get_prod_num(self):
        return self.get_attribute_loc(self.__edit_loc, 'value')

    # 增商品(需要做库存限制，暂未实现)
    def plus_prod(self):
        self.click_loc(self.__plus_loc)

     # 减商品
    def minus_prod(self):
        self.click_loc(self.__minus_loc)

    # =======================================商品分类操作======================================================

    # 面包屑列表
    __bread_crumb_loc = ('xpath', '//ul[@class="breadcrumb"]//li')

    def get_bread_crumb_count(self):
        """
        找出面包屑的数量
        :return:
        """
        # 找出面包屑列表
        li = self.find_elements(self.__bread_crumb_loc)
        len(li)
        return len(li) - 1

    # 面包屑文本元素
    __bread_crumb_text_loc = ('xpath', '//ul[@class="breadcrumb"]//li//a/span')

    def get_bread_crumb_content(self):
        """
        获取面包屑的内容，以/分割
        :return:
        """
        count = self.get_bread_crumb_count()
        content = ''
        if count > 0:
            texts = self.get_text_for_elements(self.__bread_crumb_text_loc)
            content = "/".join(texts)
        return content

    # 获取分类的文本
    def get_categorys_text(self, level):
        """
        获取一级，二级，三级的分类信息
        :param level: 1 - 一级分类；2 - 二级分类；3 - 三级分类
        :return:
        """
        levels = {1: "一级分类", 2: "二级分类", 3: "三级分类"}
        loc = ('xpath', '//div[text()="%s"]/following-sibling::div[1]//li' % levels[int(level)])
        try:
            content = self.get_content_text_for_elements(loc, timeout=2)
            return content
        except:
            return None

    def get_first_category(self):
        """
        获取一级分类的信息
        :return:
        """
        loc = ('xpath', '//div[text()="一级分类"]/following-sibling::div[1]//li/a')
        try:
            content = self.get_content_text_for_elements(loc, timeout=2)
            return content
        except TimeoutException:
            return None

    def get_second_category(self):
        """
        获取二级分类的信息
        :return:
        """
        loc = ('xpath', '//div[text()="二级分类"]/following-sibling::div[1]//li/a')
        try:
            content = self.get_content_text_for_elements(loc, timeout=2)
            return content
        except TimeoutException:
            return None

    def get_third_category(self):
        """
        获取二级分类的信息
        :return:
        """
        loc = ('xpath', '//div[text()="三级分类"]/following-sibling::div[1]//li/a')
        try:
            content = self.get_content_text_for_elements(loc, timeout=2)
            return content
        except TimeoutException:
            return None

    def click_first_category(self):
        """
        随机点击一个一级分类并且打印出点击的一级分类
        :return:
        """
        num = len(self.get_first_category())
        name = ''
        i = random.randint(1, num)
        print(i)
        loc_first = ('xpath', "//div[text()='一级分类']/following-sibling::div[1]//li[" + str(i) + "]/a")
        try:
            result = self.is_clickable(loc_first)
        except (TimeoutException, NoSuchElementException):
            result = False
        if result:
            # 随机点击一个一级分类并且获取分类文本信息
            name = self.get_text_loc(loc_first)
            self.click_loc(loc_first)
            print(name)
            self.wait_result_page_refresh()
        return result, name

    def click_second_category(self):
        """
        随机点击一个二级分类并且打印出点击的二级分类
        :return:
        """
        num = len(self.get_second_category())
        name = ''
        i = random.randint(1, num)
        print(i)
        loc_second = ('xpath', "//div[text()='二级分类']/following-sibling::div[1]//li[" + str(i) + "]/a")
        try:
            result = self.is_clickable(loc_second)
        except (TimeoutException, NoSuchElementException):
            result = False
        if result:
            # 随机点击一个一级分类并且获取分类文本信息
            name = self.get_text_loc(loc_second)
            self.click_loc(loc_second)
            print(name)
            self.wait_result_page_refresh()
        return result, name

    def click_third_category(self):
        """
        随机点击一个三级分类并且打印出点击的三级分类
        :return:
        """
        num = len(self.get_third_category())
        name = ''
        i = random.randint(1, num)
        print(i)
        loc_third = ('xpath', "//div[text()='三级分类']/following-sibling::div[1]//li[" + str(i) + "]/a")
        try:
            result = self.is_clickable(loc_third)
        except (TimeoutException, NoSuchElementException):
            result = False
        if result:
            # 随机点击一个三级分类并且获取分类文本信息
            name = self.get_text_loc(loc_third)
            self.click_loc(loc_third)
            print(name)
            self.wait_result_page_refresh()
        return result, name

    def fenlei_text(self, expect_text):
        """"搜索结果页一级分类显示(完全一样，适用于药品分类的一级)"""
        result=True
        msg=''
        loc_yiji= '//div[@class="m_cond_bd"]/div[@class="m_cond_con"]/ul[@class="m_cond_lst"]/li/a'
        loc= ('xpath', loc_yiji)
        actual_texts= self.get_text_for_elements(loc)
        # 打印元素的实际文本
        print(actual_texts)
        if operator.eq(actual_texts, expect_text):
            pass
        else:
            result = False
            msg = msg + "实际的文本值 ：%s 与期望的文本值 ：%s 不一致" % (actual_texts, expect_text)
        return result, msg

    def fenlei_contain_text(self, expect_text):
        """"搜索结果页一级分类显示(验证包含，适用于器械分类的一级)"""
        result=True
        msg=''
        xpath="//div[@class='m_cond_bd']/div[@class='m_cond_con']/ul[@class='m_cond_lst']/li/a"
        home_special = HomeAndSpecial(self.driver)
        yiji_rs=home_special.test_contain_texts(xpath, expect_text)
        if yiji_rs[0] is False:
            result = False
            msg = msg + yiji_rs[1]
        return result, msg

    def click_fenlei(self, xpath1,xpath2,xpath3,mianbaoxie1,mianbaoxie2,mianbaoxie3,erji_text,sanji1_text,sanji2_text):
        """搜索结果页点击各级分类验证显示（面包屑，下级分类文本）"""
        result=True
        msg = ''
        loc_yiji=('xpath', xpath1)
        loc_erji = ('xpath', xpath2)
        loc_sanji = ('xpath', xpath3)
        # 点击一级分类
        self.click_loc(loc_yiji)
        sleep(1)
        text_erji= "//div[text()='二级分类']/following-sibling::div[1]//li/a"
        text_sanji = "//div[text()='三级分类']/following-sibling::div[1]//li/a"
        text_mbx="//div[@class='col-lg-9 col-md-9']/ul/li/a/span"
        home_special= HomeAndSpecial(self.driver)
        erji_rs = home_special.test_contain_texts(text_erji, erji_text)
        sanji_rs = home_special.test_contain_texts(text_sanji, sanji1_text)
        mianbaoxie_rs = home_special.test_texts(text_mbx, mianbaoxie1)
        if erji_rs[0] is False:
            result = False
            msg = msg + erji_rs[1]
        if sanji_rs[0] is False:
            result = False
            msg = msg + sanji_rs[1]
        if mianbaoxie_rs[0] is False:
            result = False
            msg = msg + mianbaoxie_rs[1]
        if xpath2 is not '':
            self.click_loc(loc_erji)
            sleep(1)
            mianbaoxie_rs1=home_special.test_texts(text_mbx, mianbaoxie2)
            if mianbaoxie_rs1[0] is False:
                result = False
                msg = msg + mianbaoxie_rs1[1]
            sanji1_rs2=home_special.test_contain_texts(text_sanji, sanji2_text)
            if sanji1_rs2[0] is False:
                result = False
                msg = msg + sanji1_rs2[1]
        sleep(1)
        if xpath3 is not '':
            self.click_loc(loc_sanji)
            sleep(1)
            mianbaoxie_rs2=home_special.test_texts(text_mbx, mianbaoxie3)
            if mianbaoxie_rs2[0] is False:
                result = False
                msg = msg + mianbaoxie_rs2[1]
        return result, msg

    def delete_fenlei(self,xpath1,xpath3,level,mianbaoxie):
        """搜索结果页删除分类"""
        result=True
        msg=''
        # level = int(level)
        loc_yiji=('xpath',xpath1)
        self.click_loc(loc_yiji)
        sleep(1)
        loc_sanji=('xpath',xpath3)
        self.click_loc(loc_sanji)
        sleep(1)
        text_mbx = "//div[@class='col-lg-9 col-md-9']/ul/li/a/span"
        # level={4:"三级分类",3:"二级分类",2:"一级分类"}
        loc_delete=('xpath','//div[@class="col-lg-9 col-md-9"]/ul/li[%s]/a/i' % level)
        self.click_loc(loc_delete)
        sleep(1)
        home_special = HomeAndSpecial(self.driver)
        mianbaoxie_rs= home_special.test_texts(text_mbx, mianbaoxie)
        if mianbaoxie_rs[0] is False:
            result = False
            msg = msg + mianbaoxie_rs[1]
        return result, msg

    # ==================================================页面等待========================================
    def wait_result_page_refresh(self, timeout=10):
        """等待页面某元素过期，即等带页面刷新,此页面用搜索按钮判断"""
        try:
            self.wait_element_staleness(self.__search_button_loc, timeout)
        except (TimeoutException, NoSuchElementException):
            pass

    def wait_result_page_load(self, timeout=10):
        """等待搜索结果页打开"""
        try:
            self.is_title_contains(u"商品搜索列表", timeout)
        except TimeoutException:
            Log().info(u"商品搜索结果页面未打开")





















