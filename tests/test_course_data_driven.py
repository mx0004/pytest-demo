import pytest
from data.data_course import add_course_test_data,query_course_test_data
import time
import pytest
class TestCourseAdd:
    """新增课程 测试类（数据驱动）"""

    # @pytest.mark.parametrize：参数化，把 add_course_test_data 里每条数据喂给 test_case
    @pytest.mark.parametrize("test_case", add_course_test_data)
    def test_add_course_data_driven(self, login_in_client, test_case):
        """新增课程用例。

        参数（都由 pytest 自动注入）：
          logged_in_client：conftest.py 里定义好的「已登录客户端」夹具
          test_case        ：一条测试数据（一个字典）
        """
        # ---- 第 1 步：从测试数据里取字段 ----
        test_id = test_case["id"]# 用例编号
        description = test_case["description"]# 用例描述
        course = test_case["course"]# 要添加的课程信息（字典）
        experience = test_case["experience"]# 期望结果（code / msg）
        check_exists = test_case.get("check_exists", False)# 添加后是否验证存在

        print(f"\n{'=' * 60}")   # 打印分隔线（'=' 重复 60 次）
        print(f"执行测试用例：{test_id}-{description}")
        print(f"请求参数：{course}")

        # ---- 第 2 步：发送新增课程请求 ----
        # 注意：数据里字段叫 applicableperson（无下划线），
        #       但接口参数名是 applicable_person（有下划线），这里做了映射。
        response = login_in_client.add_course(
            name=course["name"],
            subject=course["subject"],
            price=course["price"],
            applicable_person=course["applicableperson"],
            info=course.get("info", ""),  # info 是可选字段，用 get 取，缺省给空串
        )

        # ---- 第 3 步：验证响应 ----
        assert response.status_code == 200# HTTP 状态码 200
        data = response.json()# 把响应体解析成字典
        print(f"响应数据：{data}")
        print(f"{course["price"]}")

        # 断言业务状态码和提示信息，和期望一致
        assert data["code"] == experience["code"], \
            f"用例 {test_id} 失败: 期望 code={experience['code']}，实际 code={data['code']}"
        if "msg" in experience:  # 期望里写了 msg 才校验
            assert data["msg"] == experience["msg"], \
                f"用例 {test_id} 失败: 期望 msg={experience['msg']}，实际 msg={data['msg']}"

        print(f"断言通过: code={data['code']}, msg={data['msg']}")

        # ---- 第 4 步：如果需要，验证课程是否真的添加成功 ----
        if check_exists and experience["code"] == 200:
            # 用课程名称去查列表，确认能查到刚添加的课程
            list_response = login_in_client.get_course_list(name=course["name"])
            list_data = list_response.json()

            assert list_data["code"] == 200  # 查询接口业务成功
            # 列表接口返回 {"total":N, "rows":[...]}，rows 是课程数组
            assert len(list_data.get("rows", [])) > 0, \
                f"课程 '{course['name']}' 未在列表中找到"

            # 验证查到的第一条课程信息是否正确
            found_course = list_data["rows"][0]
            assert found_course["name"] == course["name"], \
                f"课程名称不匹配: {found_course['name']} != {course['name']}"
            assert found_course["price"] == course["price"], \
                f"课程价格不匹配: {found_course['price']} != {course['price']}"

            course_id = found_course["id"]
            print(f"验证通过: 课程已存在，ID={course_id}")
        print(f"用例 {test_id} 通过")

class TestCourseUpdate:
    def test_update_course(self,login_in_client,created_course_id):
        """修改课程：改名称和价格，然后查询验证。"""
        # created_course_id 夹具已经帮我们创建好一门课，直接拿到它的 id
        course_id = created_course_id



        # 1) 准备要改成的新值
        new_name = f"修改后的课程_{int(time.time())}"  # 用时间戳保证名称唯一
        new_price = 999

        print(f" 修改课程 id={course_id}")
        print(f"  新名称={new_name}，新价格={new_price}")
        # 2) 调用修改接口（PUT）
        response = login_in_client.update_course(
            course_id=course_id,
            name=new_name,
            subject="6",
            price=new_price,
            applicable_person="2",
            info="已修改",
        )
        print("AAa")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200, f"修改失败：{data.get('msg')}"
        print("    修改成功")
        print("AAa")
        print(data)
        print("bbb")

        # 3) 按 id 查询详情，验证修改是否生效
        detail = login_in_client.get_course_by_id(course_id).json()
        assert detail["code"] == 200
        assert detail["data"]["name"] == new_name, \
            f"名称没改对：{detail['data']['name']} != {new_name}"
        assert detail["data"]["price"] == new_price, \
            f"价格没改对：{detail['data']['price']} != {new_price}"
        print(f"    验证通过：名称={detail['data']['name']}，价格={detail['data']['price']}")

