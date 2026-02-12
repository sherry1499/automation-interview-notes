import requests
import pytest

# 接口地址
BASE_URL = "https://ai.qingxiang.tech:20000/api/LoginService/login"

# 请求头
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*"
}


class TestLoginAPI:
    """登录接口测试"""

    # 用例1：正确的用户名和密码，登录成功
    def test_login_success(self):
        data = {"username": "19900000001", "password": "123", "org_id": "default"}
        resp = requests.post(BASE_URL, json=data, headers=HEADERS, verify=False)
        assert resp.status_code == 200
        result = resp.json()
        print(f"登录成功响应: {result}")
        # 根据实际返回调整断言，比如：
        # assert result["code"] == 0
        # assert "token" in result["data"]

    # 用例2：密码错误
    def test_login_wrong_password(self):
        data = {"username": "19900000001", "password": "wrong_password", "org_id": "default"}
        resp = requests.post(BASE_URL, json=data, headers=HEADERS, verify=False)
        assert resp.status_code == 200
        result = resp.json()
        print(f"密码错误响应: {result}")
        # 预期返回错误提示，根据实际返回调整：
        # assert result["code"] != 0

    # 用例3：用户名不存在
    def test_login_user_not_exist(self):
        data = {"username": "00000000000", "password": "123", "org_id": "default"}
        resp = requests.post(BASE_URL, json=data, headers=HEADERS, verify=False)
        assert resp.status_code == 200
        result = resp.json()
        print(f"用户不存在响应: {result}")

    # 用例4：用户名为空
    def test_login_empty_username(self):
        data = {"username": "", "password": "123", "org_id": "default"}
        resp = requests.post(BASE_URL, json=data, headers=HEADERS, verify=False)
        result = resp.json()
        print(f"用户名为空响应: {result}")

    # 用例5：密码为空
    def test_login_empty_password(self):
        data = {"username": "19900000001", "password": "", "org_id": "default"}
        resp = requests.post(BASE_URL, json=data, headers=HEADERS, verify=False)
        result = resp.json()
        print(f"密码为空响应: {result}")

    # 用例6：缺少 org_id 字段
    def test_login_missing_org_id(self):
        data = {"username": "19900000001", "password": "123"}
        resp = requests.post(BASE_URL, json=data, headers=HEADERS, verify=False)
        result = resp.json()
        print(f"缺少org_id响应: {result}")

    # 用例7：所有字段为空
    def test_login_all_empty(self):
        data = {"username": "", "password": "", "org_id": ""}
        resp = requests.post(BASE_URL, json=data, headers=HEADERS, verify=False)
        result = resp.json()
        print(f"全部为空响应: {result}")


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])