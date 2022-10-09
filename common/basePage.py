# coding: utf-8

"""封装浏览器操作"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from common.log import Log
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep


def browser(browser='firefox'):
    """打开浏览器函数，'firefox','chrome','ie',默认为firefox"""
    try:
        if browser == "firefox":
            driver = webdriver.Firefox()
            return driver
        elif browser == "chrome":
            chrome_options = Options()
            chrome_options.add_argument('start-maximized')
            driver = webdriver.Chrome(options=chrome_options)

            return driver
        elif browser == "ie":
            driver = webdriver.Ie()
            return driver
        elif browser == "edge":
            driver = webdriver.Edge()
            return driver
        else:
            Log().warning("Not found this browser, You can enter 'firefox','chrome','ie'")
    except Exception as msg:
        print("%s" % msg)
        Log().error("%s" % msg)


class Action(object):

    """
    BasePage封装所有页面都公用的方法，例如driver, url ，FindElement等，,各个页面相关的类都继承该类
    """

    # 初始化driver、url、等
    def __init__(self, selenium_driver):
        self.driver = selenium_driver
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    # 重写switch_frame方法
    def switch_frame(self, loc):
        frame = self.find_element(loc)
        self.driver.switch_to.frame(frame)

    def back_to_default_window(self):
        """
        跳出当前frame，回到默认的窗口
        :return:
        """
        self.driver.switch_to.default_content()

    # 使用current_url获取当前窗口Url地址，进行与配置地址作比较，返回比较结果（True False）
    def on_page(self, pagetitle):
        return pagetitle in self.driver.title

    # 定义script方法，用于执行js脚本，范围执行结果
    def script(self, src):
        self.driver.execute_script(src)

    def get(self, url):
        """打开页面，参数为URL"""
        self.driver.get(url)

    def open(self, url, title='', timeout=10):
        """使用get打开url后，最大化窗口，判断title符合预期"""
        # self.driver.maximize_window()
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))
        except TimeoutException:
            Log().info("open %s title error" % url)
        except Exception as msg:
            Log().info("Error:%s" % msg)

    def find_element(self, locator, timeout=20):
        """
        定位单个元素, 参数locatoer是元祖类型，元素必须可见
        Usage:
        locator = ("id", "xxxx")
        driver.find_element(locator)
        by_id= "id"
        by_xpath = "xpath"
        by_link_text = "link text"
        by_partial_text = "partial link text"
        by_name = "name"
        by_tag_name = "tag name"
        by_class_name = "class name"
        by_css_selector = "css selector"
        """
        # 元素必须可见
        element = WebDriverWait(self.driver, timeout, 0.5).until(EC.visibility_of_element_located(locator))
        return element

    def find_element_presence(self, locator, timeout=20):
        """元素只需要在dom树中即可"""
        element = WebDriverWait(self.driver, timeout, 0.5).until(EC.presence_of_element_located(locator))
        return element

    def find_elements(self, locator, timeout=20):
        """定位一组元素，元素在dom里面"""
        elements = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_all_elements_located(locator))
        return elements

    def find_elements_visibility(self, locator, timeout=10):
        """定位一组元素，元素需可见"""
        elements = WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_all_elements_located(locator))
        return elements

    def find_element_based_on_element(self, element, locator, timeout=10):
        """找到的元素的基础上，找另外一个元素。一般是在元素内部找子元素"""
        ele = element.find_element(locator[0], locator[1])
        return ele

    def find_elements_based_on_element(self, element, locator):
        """找到的元素的基础上，找另外一组元素。一般是在元素内部找子元素"""
        eles = element.find_elements(locator[0], locator[1])
        return eles

    def click_loc(self, locator, timeout=40):
        """点击操作"""
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()

    def click_element(self, element):
        """在已知的元素上做点击操作，参数为元素element"""
        element.click()

    def send_keys_element(self, element):
        """元素被覆盖，无法点击,使用用Enter代替click操作，参数为元素element"""
        element.send_keys(Keys.ENTER)

    def send_keys_loc(self, locator, text, clear_first=True, click_first=False):
        """清空后输入文本"""
        element = self.find_element(locator)
        if click_first:
            element.click()
        if clear_first:
            element.clear()
        element.send_keys(text)

    def send_keys_loc2(self, locator, text, clear_first=True, click_first=False):
        """适用用element.clear()方法无效时，用双击替代"""
        element = self.find_element(locator)
        if click_first:
            element.click()
        if clear_first:
            # 双击事件替代clear有时无法清除数据
            action_chains = ActionChains(self.driver)
            action_chains.double_click(element).perform()
        element.send_keys(text)

    def send_keys_ele(self, element, text, clear_first=True, click_first=False):
        """清空后输入文本"""
        if click_first:
            element.click()
        if clear_first:
            element.clear()
        element.send_keys(text)

    def is_text_in_element(self, locator, text, timeout=10):
        """
        判断文本元素在元素里，没定位到元素返回False,定位到返回判断结果布尔值
        """
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            print("元素没定位到： "+str(locator))
            return False
        else:
            return result

    def is_text_in_value(self, locator, text, timeout=10):
        """
        判断元素的value值，没定位到元素返回false，定位到返回判断结果布尔值
        """
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(EC.text_to_be_present_in_element_value(locator, text))
        except TimeoutException:
            print("元素没定位到： "+str(locator))
            return False
        else:
            return result

    def is_title(self, title, timeout=10):
        """
        判断title完全等于，返回布尔值
        """
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_is(title))
        return result

    def is_title_contains(self, title, timeout=10):
        """
        判断title包含，返回布尔值
        """
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))
        return result

    def is_selected(self, locator, timeout=10):
        """
        判断元素是否被选中，返回布尔值
        """
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_to_be_selected(locator))
        return result

    def is_selected_be(self, locator, selected=True, timeout=10):
        """
        判断元素的状态，selected是期望的参数True/False
        返回布尔值
        """
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_selection_state_to_be(locator, selected))
        return result

    def is_alert_present(self, timeout=10):
        """
        判断页面是否有alert
        有 -- 返回alert
        没有 -- 返回false
        """
        result = WebDriverWait(self.driver, timeout, 1).until((EC.alert_is_present()))
        return result

    def is_visibility(self, locator, timeout=10):
        """"元素可见返回本身，不可见返回False"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(locator))
        return result

    def is_invisibility(self, locator, timeout=10):
        """元素可见返回本身， 不可见返回True, 没找到元素也返回True"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.invisibility_of_element_located(locator))
        return result

    def visibility_of(self, element, timeout):
        """元素科可见返回本身，不可见返回False, 参数为元素element"""
        WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of(element))

    def is_display(self, locator, timeout=20):
        """元素是否显示"""
        ele = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))
        return ele.is_displayed()

    def is_display_all(self, locator, timeout=20):
        """一组元素是否存在"""
        ele = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_all_elements_located(locator))
        return ele

    def is_clickable(self, locator, timeout=20):
        """元素可以点击，返回本身， 不可点击返回FALSE"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_to_be_clickable(locator))
        return result

    def is_located(self, locator, timeout=10, is_all=False):
        """
        判断元素有没有被定位到（并不意味着可见），定位到返回element，没定位到返回false
        """
        try:
            if is_all:
                # is_all 为true时，是判断一组元素
                result = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_all_elements_located(locator))
            else:
                # is_all 为false时，是判断一个元素.默认是判断单个元素
                result = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            result = False
        return result

    def move_to_element(self, locator,timeout=20):
        """鼠标悬停操作"""
        element = self.find_element(locator,timeout=timeout)
        ActionChains(self.driver).move_to_element(element).perform()

    def move_to_element_ele(self, element):
        """鼠标悬停操作，参数为element"""
        ActionChains(self.driver).move_to_element(element).perform()

    def click_by_mouse(self, locator):
        """鼠标点击元素操作"""
        element = self.find_element(locator)
        ActionChains(self.driver).click(element).perform()

    def back(self):
        """后退"""
        self.driver.back()

    def forward(self):
        """前进"""
        self.driver.forward()

    def close(self):
        """关闭浏览器"""
        self.driver.close()

    def refresh(self):
        """刷新页面"""
        self.driver.refresh()

    def quit(self):
        """关闭driver"""
        self.driver.quit()

    def get_title(self):
        """获取当前页面的title"""
        return self.driver.title

    def wait_title_change(self, title, timeout=20):
        return WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))

    def wait_url_contains(self, url, timeout=30):
        return WebDriverWait(self.driver, timeout, 1).until(EC.url_contains(url))

    def get_attribute_loc(self, locator, name, timeout=10):
        """获取属性 - 参数为locator"""
        # element = self.find_element(locator)
        element = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))
        return element.get_attribute(name)

    def get_attribute_ele(self, element, name):
        """获取属性 - 参数为element"""
        return element.get_attribute(name)

    def get_attribute_visibility(self, locator, name, timeout=20):
        """获取属性 - 参数为locator"""
        element = WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(locator))
        return element.get_attribute(name)

    def get_attribute_for_elements(self, locator, name):
        """获取一组元素的某属性的值"""
        elements = self.find_elements(locator)
        props = []
        for ele in elements:
            prop = ele.get_attribute(name)
            props.append(prop)
        return props

    def get_text_for_elements(self, locator, timeout=30):
        """获取一组元素的text"""
        elements = self.find_elements(locator, timeout)
        # elements = self.driver.find_elements(locator[0], locator[1])
        values = []
        for ele in elements:
            value = ele.text
            values.append(value)
        return values

    def get_content_text_for_elements(self, locator, timeout=30):
        """获取一组元素的text"""
        elements = self.find_elements(locator, timeout)
        values = []
        for ele in elements:
            value = ele.get_attribute('textContent')
            values.append(value)
        return values

    def get_text_loc(self, locator, timeout=3):
        """获取文本 - 参数为locator"""
        element = self.find_element(locator, timeout)
        return element.text

    def get_text_ele(self, ele):
        """获取文本 - 参数为element"""
        return ele.text

    def get_text_content_ele(self, ele):
        """获取隐藏元素的文本"""
        text = ele.get_attribute('textContent')
        return text

    def get_text_content_loc(self, locator):
        """获取隐藏元素的文本"""
        ele = self.find_element_presence(locator)
        text = ele.get_attribute('textContent')
        return text

    def js_execute(self, js):
        """执行js"""
        return self.driver.execute_script(js)

    def js_focus_element_loc(self, locator, bottom=True):
        """聚焦元素，将滚动条滚到显示指定的元素"""
        target = self.find_element(locator)
        if bottom is True:
            # 元素element对象的“底端”与当前窗口的“底部”对齐
            self.driver.execute_script("arguments[0].scrollIntoView(false);", target)
        else:
            # 元素element对象的“顶端”与当前窗口的“顶部”对齐
            self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def js_focus_element_ele(self, element, bottom=True):
        """聚焦元素，将滚动条滚到显示指定的元素，参数为element"""
        if bottom is True:
            # 元素element对象的“底端”与当前窗口的“底部”对齐
            self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
        else:
            # 元素element对象的“顶端”与当前窗口的“顶部”对齐
            self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def js_scroll_top(self):
        """滚动到顶部"""
        js = "windows.scrollTo(0,0)"
        self.js_execute(js)

    def js_scroll_end(self):
        """滚动到底部"""
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.js_execute(js)

    def get_input_value(self, loc, timeout):
        ele = self.find_element(loc, timeout)
        return self.driver.execute_script("return arguments[0].value;", ele)

    def page_down(self):
        ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()

    def open_in_new_tab(self, url, timeout=5):
        """
        在新窗口打开url，并切换到新打开的窗口上
        :param url: url地址
        :param timeout: 超时时间
        :return:
        """
        js = 'window.open("%s");' % url
        self.js_execute(js)
        self.wait_and_switch_window(timeout=timeout)

    def select_by_index(self, locator, index):
        """通过索引选择，index是索引第几个，从0开始"""
        element = self.find_element(locator)
        Select(element).select_by_index(index)

    def select_by_value(self, locator, text):
        """通过value属性来选择"""
        element = self.find_element(locator)
        Select(element).select_by_value(text)

    def get_url(self):
        """获取当前链接的url"""
        import urllib.parse
        url = self.driver.current_url
        url = urllib.parse.unquote(url)
        return url

    def wait_until_windows_open(self, timeout=5):
        """等待新窗口打开，即等待有2个窗口出现"""
        WebDriverWait(self.driver, timeout, 0.5).until(WindowsExist())

    def switch_window(self, num=-1):
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[num])

    def wait_and_switch_window(self, num=-1, timeout=20):
        """等待新窗口打开，并切换到新窗口"""
        self.wait_until_windows_open(timeout)
        self.switch_window(num)

    def switch_appoint_window(self, num):
        """
        切换指定的窗口
        :param num:这个是列表索引值
        :return:
        """
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[num])

    def get_windows_num(self):
        """获取当前窗口数量"""
        return len(self.driver.window_handles)

    def close_and_switch_window(self, num=-1):
        """关闭当前页面，切换到最后面一个窗口"""
        self.close()
        self.switch_window(num)

    def enter_key(self, locator):
        """模拟enter键"""
        ele = self.find_element(locator)
        ele.send_keys(Keys.ENTER)

    def down_key(self, locator):
        """模拟向下键"""
        ele = self.find_element(locator)
        ele.send_keys(Keys.ARROW_DOWN)

    def up_key(self, locator):
        """模拟向上键"""
        ele = self.find_element(locator)
        ele.send_keys(Keys.ARROW_UP)

    def wait_element_staleness(self, locator, timeout=10):
        """等待某个元素过期"""
        old_page = self.driver.find_element(locator[0], locator[1])
        WebDriverWait(self.driver, timeout, 0.5).until(EC.staleness_of(old_page))

    def wait_element_staleness_ele(self, element, timeout=10):
        WebDriverWait(self.driver, timeout, 0.5).until(EC.staleness_of(element))


    def wait_invisibility_of_all_elements(self, locator, timeout=10):
        """等待一组元素，所有元素都不可见"""
        WebDriverWait(self.driver, timeout, 1).until_not(EC.visibility_of_any_elements_located(locator))

    # def wait_new_window_open(self, num,timeout):
    #     """
    #     :param timeout:
    #     :return:
    #     """
    #     WebDriverWait(self.driver, timeout, 0.5).until(EC.new_window_is_opened(num))

    #   该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
    def isElementExist(self, element):
        flag = True
        try:
            self.driver.find_element_by_xpath(element)
            return flag
        except:
            flag = False
            return flag


class WindowsExist(object):
    """判断当前是否有新窗口"""

    def __call__(self, driver, num=2):
        handles = driver.window_handles
        num_current = len(handles)
        if num_current >= num:
            return True
        else:
            return False










