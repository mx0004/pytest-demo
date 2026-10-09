import pytest
from src.testqingqiu import Apiclient
from data.text_login import login_text_data


class Test_login:
    correct_captcha = "2"

    @pytest.fixture(scope="function")
    def login_client(self):
        login_client = Apiclient()
        yield login_client
        login_client.close()

    @pytest.fixture(scope="function")
    def captcha_client(self,login_client):
        response = login_client.get_captcha()
        assert response.status_code == 200
        data = response.json()
        return {"uuid":data["uuid"]}

    @pytest.mark.parametrize("test_case",login_text_data)
    def test_login_case(self,login_client:Apiclient,captcha_client:dict,test_case):
        test_id = test_case["id"]
        description = test_case["description"]
        username = test_case["username"]
        password = test_case["password"]
        code_type = test_case["code_type"]
        expected_code = test_case["expected_code"]
        expected_msg = test_case.get("expected_msg")
        check_token = test_case.get("check_token")

        code = self.correct_captcha if code_type == "correct" else 9999
        uuid = captcha_client["uuid"]
        print(f"\n执行用例:{test_id} - {description}")
        response = login_client.login(
            username=username,
            password=password,
            uuid=uuid,
            code=code,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == expected_code,\
            f"用例{test_id}失败:期望 code = {expected_code},实际:{data["code"]}"
        if expected_msg:
            assert data["msg"] == expected_msg, \
                f"用例{test_id}失败：期望 msg={expected_msg}，实际 msg={data['msg']}"

        if check_token:
            assert "token" in data
            assert data["token"] is not None and data["token"] != ""
            print(f"token:{data['token'][:30]}")

        print(f"用例{test_id}通过")

