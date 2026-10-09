

import requests

#===============第一步：发请求
url = "https://kdtx-test.itheima.net/api/captchaImage"
# responses = requests.get(url)

#===============定义请求头
header = {
    "user-Agent":"Mozilla/5.0",#告诉服务器我是浏览器访问
    "Content-Type":"application/json"
}

#===============发送请求
response = requests.get(url,headers=header)

#===============查看请求结果
print("=" *50)
print("状态码",response.status_code)
print("响应头",response.headers)
print("状态码",response.text[:200])
print("状态码",response.json())

#===============如果返回的是json，解析成字典
if response.status_code==200:
    try:
        data = response.json()#将文件格式转换为字典，这样才可以用对应的key获得值
        print("json数据：",data)

        #从字典提取想要的字段
        code = data.get("code")
        uuid = data["uuid"]
        print(f"验证文字：{code}")
        print(f"唯一标识：{uuid}")
    except Exception as e:
        print("json解析失败",e)
else:
    print(f"请求失败，状态码{response.status_code}")

print("=" * 50)


#======================登录
login_url = "https://kdtx-test.itheima.net/api/login"

#登录的参数
login_data = {
    "username":"admin",
    "password":"HM_2023_test",
    "code":2,
    "uuid":uuid
}

login_response = requests.post(login_url,json=login_data,headers=header)
print("=" * 50)
print("登录状态",login_response.status_code)
print("登录的结果",login_response.json())

if login_response.status_code==200:
    login_result = login_response.json()
    if login_result.get("code")==200:
        token = login_result.get("token")
        print(f"登录成功:{token}")
    else:
        print("登录失败",login_result.get("mag"))

