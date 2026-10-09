import pytest
from src.testqingqiu import Apiclient
from tests.test003 import response


class Test_login:
    # 测试用到的「正确」账号密码（放成类属性，方便统一维护）
    valid_username = 'admin'
    valid_password = 'HM_2023_test'

    @pytest.fixture(scope='function')

    def client(self):
        """
            夹具1：准备一个 AIPClient 客户端对象。

        yield 之前是「测试前的准备」，yield 之后是「测试后的清理」
        """
        # 实例化时传入账号密码
        client = Apiclient()# 准备：创建客户端（内部会自动建立 Session）
        yield client# 把 client 交给测试方法使用
        client.close()# 清理：测试结束后关闭会话
    @pytest.fixture(scope='function')
    def captcha_info(self, client):
        response = client.get_captcha()# 调接口拿验证码
        assert response.status_code == 200# 先确认接口调用成功
        data = response.json()# 把响应体解析成字典
        return {"uuid": data["uuid"]}# 只把 uuid 返回给用例

    # def test_login(self,client:Apiclient,captcha_info,dict):
    #用例1（正向）：正确用户名 + 正确密码 + 正确验证码 → 登录成功。
    #     username = "admin"
    #     password = "HM_2023_test"
    #     uuid = captcha_info["uuid"]
    #     response = client.login(username=username,password=password,code="2",uuid=uuid)
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["code"] == 200
    #     assert data["msg"] == "success"
    #     assert "token" in data
    #     assert data["token"] is not None and data["token"] !=""
    #     print(f"登录成功,token:{data['token']}")

    def test_login_pwd_wrong(self,client:Apiclient,captcha_info):
        username = "admin"
        password = ""
        uuid = captcha_info["uuid"]
        response = client.login(username=username,password=password,code="2",uuid=uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] =="用户不存在/密码错误"
        print(f"登录失败,{data}")

    def test_login_uuid_wrong(self,client:Apiclient,captcha_info):
        username = "admin"
        password = "HM_2023_test"
        uuid = ""
        response = client.login(username=username,password=password,code="2",uuid=uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "验证码已失效"
        print("登录失败，验证码不存在")
