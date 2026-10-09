import pytest
from src.testqingqiu import Apiclient
git add tests/conftest.py

@pytest.fixture(scope="function")
def client():
    client = Apiclient()
    yield client
    client.close()

@pytest.fixture(scope="function")
def captcha_info(client:Apiclient):
    response = client.get_captcha()
    assert response.status_code == 200
    data = response.json()
    return {
        "code":"2",
        "uuid":data["uuid"]
    }

@pytest.fixture(scope="function")
def login_in_client(client:Apiclient,captcha_info:dict):
    code = captcha_info["code"]
    uuid = captcha_info["uuid"]

    response = client.login(
        "admin",
        "HM_2023_test",code,uuid
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200

    client.set_token(data["token"])
    print(f"\n自动登陆成功,token:{client.token[:30]}")

    return client

@pytest.fixture(scope="function")
def created_course_id(login_in_client):
    """创建一个课程，返回它的ID，给  查询/删除/修改使用"""
    import time
    course_name = f"test课程_{int(time.time())}"
    #1.新增课程
    response = login_in_client.add_course(
        name = course_name,
        subject = "6",
        price = 899,
        applicable_person = "2",
        info = "由fixture创建的测试课程"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    #2.按照课程名称查找、拿到新创建的课程ID
    list_response = login_in_client.get_course_list(name = course_name)
    list_data = list_response.json()


    if list_data.get("rows") and len(list_data.get("rows"))>0:
        course_id = list_data.get("rows")[0].get("id")
        print(f"\n创建测试课程成功,ID{course_id}")
        return course_id
    else:
        pytest.fail("无法获取新的课程ID")

@pytest.fixture(scope="function")
def created_clue_id(login_in_client):
    """创建一个线索，返回它的ID，给  查询/删除/修改使用"""
    import time
    clue_name = f"test线索_{int(time.time())}"
    response = login_in_client.add_system(
        name = clue_name,
        phone = 14332502452,
        channel = "1",
        age=15,
        weixin="sdafdw",
        qq=1234435
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    list_response = login_in_client.get_clue_list(name=clue_name)
    list_data = list_response.json()
    if list_data.get("rows") and len(list_data.get("rows"))>0:
        clue_id = list_data.get("rows")[0].get("id")
        print(f"\n创建线索成功,ID{clue_id}")
        return clue_id
    else:
        pytest.fail("无法获取新的线索ID")
