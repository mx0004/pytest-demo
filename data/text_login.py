login_text_data = [
    {
        "id":"test001",
        "description":"正确的用户名+正确的密码+正确的验证码，登陆成功",
        "username":"admin",
        "password":"HM_2023_test",
        "code_type":"correct",
        "expected_code":200,
        "expected_msg":"操作成功",
        "check_token":True

    },
    {
        "id":"test002",
        "description":"错误的用户名+正确的密码+正确的验证码，登陆成功",
        "username":"da阿萨大大",
        "password":"HM_2023_test",
        "code_type":"correct",
        "expected_code":500,
        "expected_msg":"用户不存在/密码错误",
        "check_token":False

    },
    {
        "id":"test002",
        "description":"错误的用户名+错误的密码+正确的验证码，登陆成功",
        "username":"da阿萨大大",
        "password":"sada",
        "code_type":"correct",
        "expected_code":500,
        "expected_msg":"用户不存在/密码错误",
        "check_token":False

    },
    {
        "id":"test002",
        "description":"错误的用户名+错误的密码+不对验证码，登陆成功",
        "username":"da阿萨大大",
        "password":"HM_2023_test",
        "code_type":"23",
        "expected_code":500,
        "expected_msg":"验证码错误",
        "check_token":False

    },
]