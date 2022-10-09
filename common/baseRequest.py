# -*- coding: utf-8 -*-
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class RunMethod(object):

    def __init__(self):
        self.request = requests.Session()

    def post_main(self, url, data, timeout=120, headers=None, param_name=None):
        if param_name is "json":
            res = self.request.post(url=url, json=data, headers=headers, timeout=timeout)
        elif param_name is "data":
            res = self.request.post(url=url, data=data, headers=headers, timeout=timeout)
        else:
            res = self.request.post(url=url, params=data, headers=headers, timeout=timeout)
        return res

    def get_main(self, url, data=None, timeout=120, headers=None, param_name=None):
        if param_name is "data":
            res = self.request.get(url, data=data, headers=headers, timeout=timeout)
        else:
            res = self.request.get(url, params=data, headers=headers, timeout=timeout)
        return res

    def run_main(self, method, url, data=None, timeout=120, headers=None, param_name=None):
        if method.lower() == 'post':
            res = self.post_main(url, data, timeout, headers, param_name)
        else:
            res = self.get_main(url, data, timeout, headers, param_name)
        return res

    def get_json(self, method, url, data=None, headers=None, timeout=120):
        result = self.run_main(method, url, data, timeout,headers)
        return result.json()

    def get_json_and_status(self, method, url, data=None, headers=None, timeout=120):
        result = self.run_main(method, url, data, timeout,headers)
        return result.json(), result.status_code

    def get_headers(self, method, url, data=None, headers=None):
        result = self.run_main(method, url, data, headers)
        return result.request.headers

    def session_close(self):
        self.request.close()

    def post_multipart_form_data(self, url, input, method='post', opened_file=None, headers=None):
        """
        处理Content-Type为 multipart/form-data的数据
        :param url:
        :param input:
        :param method: 接口的请求方法
        :param opened_file: 这里要传入的参数opened_file是指已用open()方法打开的文件
        :param headers: 头部信息
        :return:
        """
        fields = {}
        if opened_file:
            # fields 加入要传入的文件信息
            fields = {
                'uploadFile0': ('filename', opened_file, 'multipart/form-data')
            }
        # fields 加入字典类型的数据
        fields.update(input)
        multipart_encoder = MultipartEncoder(fields=fields)

        # 将Content-Type设置为与multipart_encoder的Content-type一致
        if headers is None:
            headers = dict()
        headers['Content-Type'] = multipart_encoder.content_type
        # 发送请求
        if method.lower() == 'post':
            result = self.request.post(url, data=multipart_encoder, headers=headers)
        else:
            result = self.request.get(url, data=multipart_encoder, headers=headers)
        return result.json(), result.status_code

    def run_multipart_form_data(self, url, input, method='post', opened_file=None, headers=None):
        """
        处理Content-Type为 multipart/form-data的数据
        :param url:
        :param input:
        :param method: 接口的请求方法
        :param opened_file: 这里要传入的参数opened_file是指已用open()方法打开的文件
        :param headers: 头部信息
        :return:
        """
        fields = {}
        if opened_file:
            # fields 加入要传入的文件信息
            fields = {
                'uploadFile0': ('filename', opened_file, 'multipart/form-data')
            }
        # fields 加入字典类型的数据
        fields.update(input)
        multipart_encoder = MultipartEncoder(fields=fields)

        # 将Content-Type设置为与multipart_encoder的Content-type一致
        if headers is None:
            headers = dict()
        headers['Content-Type'] = multipart_encoder.content_type
        # 发送请求
        if method.lower() == 'post':
            result = self.request.post(url, data=multipart_encoder, headers=headers)
        else:
            result = self.request.get(url, data=multipart_encoder, headers=headers)
        return result

if __name__ == "__main__":
    url = "http://test.jk.com/api/auth/login_c_mobile.json"
    data = {"adcode":"420105","platform":"2","vcode":"600998","lat":"30.545979","login_name":"13871348853","lng":"114.197331"}
    b = RunMethod()
    print(b.get_json('Post', url, data))












