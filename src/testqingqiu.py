from idlelib.rpc import response_queue

import requests
import random
from test003 import header


class Apiclient():
    base_url = 'https://kdtx-test.itheima.net'

    def __init__(self):
        self.session = requests.Session()
        self.header = {
            "user-Agent":"Mozilla/5.0",
            "Content-Type":"application/json"
        }
        self.token = ""

    def set_token(self, token):
        """登录成功后，把 token 存起来，并放进请求头。

        后续所有需要登录的接口，请求头都会自动带上：
            Authorization: Bearer <token>
        服务器看到这个头，才知道「你是谁」。
        """
        self.token = token  # 存 token
        self.header["Authorization"] = f"Bearer {self.token}"  # 放进请求头
    def get_captcha(self):
        url = self.base_url + "/api/captchaImage"
        response = self.session.get(url,headers=self.header)
        return response

    def login(self,username,password,code,uuid):
        url = self.base_url + "/api/login"
        data = {
            "username":username,
            "password":password,
            "code":code,
            "uuid":uuid
        }
        response = self.session.post(url,json=data,headers=self.header)
        return response

    # ==================== 课程管理接口 ====================
    def add_course(self,name,subject,price,applicable_person,info=""):
        """新增课程（需先登录）。
                参数：
                  name             : 课程名称
                  subject          : 学科
                  price            : 价格
                  applicable_person: 适用人群
                  info             : 课程介绍（可选，默认空字符串）
                """
        url = self.base_url + '/api/clues/course'
        data = {
            "name":name,
            "subject":subject,
            "price":price,
            "applicable_person":applicable_person,
            "info":info
        }
        response = self.session.post(url,json=data,headers=self.header)
        return response

    def get_course_list(self,name="", subject="", price="", applicable_person="", info=""):
        """查询课程列表（需先登录）。

                所有参数都是可选的：传了就按条件过滤，不传就查全部。
                """
        url = self.base_url + '/api/clues/course/list'
        params = {}
        if name:
            params["name"] = name
        if subject:
            params["subject"] = subject
        if price is not None:
            params["price"] = price
        if applicable_person:
            params["applicable_person"] = applicable_person
        if info:
            params["info"] = info

        response = self.session.get(url,params=params,headers=self.header)
        return response

    def get_course_by_id(self,course_id):
        url = self.base_url + f'/api/clues/course/{course_id}'
        response = self.session.get(url,headers=self.header)
        return response

    def update_course(self,course_id,name=None,subject=None,price=None,applicable_person=None,info=None):
        """修改课程（需先登录）。
        参数：
          course_id        : 课程 id（必填，指定要修改哪门课）
          name             : 新的课程名称
          subject          : 新的课程学科
          price            : 新的课程价格
          applicable_person: 新的适用人群
          info             : 新的课程介绍
        """
        url = self.base_url + "/api/clues/course"
        data = {
            "id":course_id,
            "name":name,
            "subject":subject,
            "price":price,
            "applicable_person":applicable_person,
            "info":info
        }
        response = self.session.put(url,json=data,headers=self.header)
        print(response)
        return response

    def add_system(self,name,phone,channel,age,weixin,qq):

        """新增线索（需先登录）。
            参数：
              id                : 线索 id（可通过id查询）
              name              : 新的线索姓名
              phone             : 新的线索手机（必填）
              channel           : 新的线索渠道（必填）
              age               : 新的线索年龄
              weixin            : 新的线索weixin
              qq                :新的线索qq
        """

        url = self.base_url + '/api/clues/clue'
        data = {
            "name":name,
            "phone":phone,
            "channel":channel,
            "age":age,
            "weixin":weixin,
            "qq":qq
        }
        response = self.session.post(url,json=data,headers=self.header)
        print(response)
        return response

    def update_clue(self,name=None,phone=None,channel=None,age=None,weixin=None,qq=None):

        url = self.base_url + "/api/clues/clue"
        data = {
            "name":name,
            "phone":phone,
            "channel":channel,
            "age":age,
            "weixin":weixin,
            "qq":qq
        }
        response = self.session.put(url,json=data,headers=self.header)
        print(response)
        return response

    def get_clue_by_id(self,clue_id):
        url = self.base_url + f'/api/clues/clue/{clue_id}'
        response = self.session.get(url,headers=self.header)
        return response

    def get_clue_list(self,name="", phone="", channel="", age="", weixin="",qq=""):
        url = self.base_url + '/api/clues/clue/list'
        params = {}
        if name:
            params["name"] = name
        if phone:
            params["phone"] = phone
        if channel is not None:
            params["channel"] = channel
        if age:
            params["age"] = age
        if weixin:
            params["weixin"] = weixin
        if qq:
            params["qq"] = qq

        response = self.session.get(url, params=params, headers=self.header)
        return response

    def close(self):
        self.session.close()
