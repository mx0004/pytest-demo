add_clue_test_data = [
    {
        "id": "TEST_CLUE_ADD_001",
        "description": "正常添加线索--成功",
        # 要添加的信息
        "clue": {
            "name":"神人",
            "phone":14339342452,
            "channel":"1",
            "age":15,
            "weixin":"sdvbjhw",
            "qq":1234435
        },
        # 期望结果：接口返回 code=200、msg=操作成功
        "experience": {
            "code": 200,
            "msg": "操作成功",
        },
        "check_exists": True,  # 添加后再去查询验证课程是否存在
    },

]

# ==================== 查询线索测试数据 ====================
