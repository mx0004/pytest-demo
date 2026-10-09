add_course_test_data = [
    {
        "id": "TEST_COURSE_ADD_001",
        "description": "正常添加课程--成功",
        # 要添加的课程信息。注意字段名：applicableperson（接口里叫 applicable_person）
        "course": {
            "name": "自动化测试实战课01234",   # 课程名称
            "subject": "6",              # 学科
            "price": 899,                # 价格
            "applicableperson": "2",     # 适用人群
            "info": "从零开始学习自动化测试",  # 课程介绍
        },
        # 期望结果：接口返回 code=200、msg=操作成功
        "experience": {
            "code": 200,
            "msg": "操作成功",
        },
        "check_exists": True,  # 添加后再去查询验证课程是否存在
    },
    {
        "id": "TEST_COURSE_ADD_002",
        "description": "正常添加课程--失败",
        # 要添加的课程信息。注意字段名：applicableperson（接口里叫 applicable_person）
        "course": {
            "name": "测试开发提升课012356",   # 课程名称
            "subject":"",              # 学科
            "price": 899,                # 价格
            "applicableperson": "2",     # 适用人群
            "info": "从零开始学习自动化测试",  # 课程介绍
        },
        # 期望结果：接口返回 code=200、msg=操作成功
        "experience": {
            "code": 200,
            "msg": "操作成功",
        },
        "check_exists": True,  # 添加后再去查询验证课程是否存在
    },
]

# ==================== 查询课程测试数据 ====================
query_course_test_data = [
    {
        "id": "TEST_COURSE_ADD_001",
        "description": "查询所有课程--成功（不传任何参数）",
        "params": {},  # 查询参数（空 = 查全部）
        "experience": {
            "code": 200,
            "msg": "查询成功",
            "has_data": True,  # 期望能查到数据
        },
    },
    {
        "id": "TEST_COURSE_ADD_002",
        "description": "按课程名称查询--成功",
        "params": {
            "name": "",  # 按课程名过滤
        },
        "experience": {
            "code": 200,
            "msg": "查询失败",
            "has_data": False,
        },
    },
]