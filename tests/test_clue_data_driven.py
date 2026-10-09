import pytest
from data.data_clue import add_clue_test_data
import time
import pytest
import random
import allure

@allure.feature("线索管理")

class TestClueAdd:
    @allure.story("添加线索")  # 添加用户故事
    @allure.title("{test_case[id]} - {test_case[description]}")

    @pytest.mark.parametrize("test_case", add_clue_test_data,ids=[case["id"] for case in add_clue_test_data])

    def test_add_clue_data_driven(self,login_in_client,test_case):
        test_id = test_case["id"]  # 用例编号
        description = test_case["description"]  # 用例描述
        clue = test_case["clue"]  # 要添加的线索信息（字典）
        experience = test_case["experience"]  # 期望结果（code / msg）
        check_exists = test_case.get("check_exists", False)  # 添加后是否验证存在

        print(f"\n{'=' * 60}")  # 打印分隔线（'=' 重复 60 次）
        print(f"执行测试用例：{test_id}-{description}")
        print(f"请求参数：{clue}")

        def gen_phone():
            # 以 1 开头，第二位 3-9，后面 9 位随机
            return "1" + random.choice("3456789") + "".join(str(random.randint(0, 9)) for _ in range(9))
        new_phone = gen_phone()
        response = login_in_client.add_system(
            name=clue["name"],
            phone=new_phone,
            channel=clue["channel"],
            age=clue["age"],
            weixin=clue["weixin"],
            qq=clue["qq"]
        )
        assert response.status_code == 200  # HTTP 状态码 200
        data = response.json()
        allure.attach(
            str(data),
            name="响应数据",
            attachment_type=allure.attachment_type.JSON
        )
        # 把响应体解析成字典
        print(f"响应数据：{data}")
        print(f"{clue['channel']}")

        assert data["code"] == experience["code"], \
            f"用例 {test_id} 失败: 期望 code={experience['code']}，实际 code={data['code']}"
        if "msg" in experience:  # 期望里写了 msg 才校验
            assert data["msg"] == experience["msg"], \
                f"用例 {test_id} 失败: 期望 msg={experience['msg']}，实际 msg={data['msg']}"

        print(f"断言通过: code={data['code']}, msg={data['msg']}")

        if check_exists and experience["code"] == 200:
            # 用线索去查列表，确认能查到刚添加的线索
            list_response = login_in_client.get_clue_list(phone=new_phone)
            list_data = list_response.json()

            assert list_data["code"] == 200  # 查询接口业务成功
            # 列表接口返回 {"total":N, "rows":[...]}，rows 是课程数组
            assert len(list_data.get("rows", [])) > 0, \
                f"课程 '{clue['name']}' 未在列表中找到"

            # 验证查到的第一条课程信息是否正确
            found_clue = list_data["rows"][0]
            assert found_clue["name"] == clue["name"], \
                f"线索名称不匹配: {found_clue['name']} != {clue['name']}"
            assert found_clue["channel"] == clue["channel"], \
                f"线索活动不匹配: {found_clue['channel']} != {clue['channel']}"

            clue_id = found_clue["id"]
            print(f"验证通过: 线索已存在，ID={clue_id}")
        print(f"用例 {test_id} 通过")

