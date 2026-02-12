import requests
import pytest
import time

BASE_URL = "https://ai.qingxiang.tech:20000"
LOGIN_URL = f"{BASE_URL}/api/LoginService/login"
ADD_USER_URL = f"{BASE_URL}/api/UserService/add_user"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*"
}


class TestAddUserAPI:
    """添加用户接口测试"""

    @classmethod
    def setup_class(cls):
        """登录获取 token"""
        login_data = {"username": "19900000001", "password": "123", "org_id": "default"}
        resp = requests.post(LOGIN_URL, json=login_data, headers=HEADERS, verify=False)
        cls.token = resp.headers.get("refresh-token", "")
        print(f"\n获取到 token: {cls.token[:50]}..." if cls.token else "未获取到 token")

    def _get_headers(self, token=None):
        """构造带 token 的请求头"""
        h = HEADERS.copy()
        h["access-token"] = token if token else self.token
        return h

    # ===== 正常场景 =====

    # 用例1：正常添加用户
    def test_add_user_success(self):
        # 用时间戳生成唯一用户名，避免重复
        unique_id = f"test_{int(time.time())}"
        data = {"user_id": unique_id, "password": "123", "name": "测试用户", "desc": "自动化测试创建"}
        resp = requests.post(ADD_USER_URL, json=data, headers=self._get_headers(), verify=False)
        assert resp.status_code == 200
        result = resp.json()
        print(f"正常添加用户响应: {result}")

    # 用例2：重复添加同一用户
    def test_add_user_duplicate(self):
        data = {"user_id": "19900000035", "password": "123", "name": "", "desc": ""}
        # 第一次添加（可能已存在）
        requests.post(ADD_USER_URL, json=data, headers=self._get_headers(), verify=False)
        # 第二次添加，预期应该报错
        resp = requests.post(ADD_USER_URL, json=data, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"重复添加用户响应: {result}")

    # ===== 认证相关 =====

    # 用例3：不带 token
    def test_add_user_no_token(self):
        h = HEADERS.copy()
        h["access-token"] = ""
        data = {"user_id": "no_token_user", "password": "123", "name": "", "desc": ""}
        resp = requests.post(ADD_USER_URL, json=data, headers=h, verify=False)
        result = resp.json()
        print(f"无token响应: {result}")

    # 用例4：错误的 token
    def test_add_user_invalid_token(self):
        data = {"user_id": "invalid_token_user", "password": "123", "name": "", "desc": ""}
        resp = requests.post(ADD_USER_URL, json=data, headers=self._get_headers(token="invalid_token"), verify=False)
        result = resp.json()
        print(f"错误token响应: {result}")

    # ===== 参数异常 =====

    # 用例5：user_id 为空
    def test_add_user_empty_user_id(self):
        data = {"user_id": "", "password": "123", "name": "", "desc": ""}
        resp = requests.post(ADD_USER_URL, json=data, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"空user_id响应: {result}")

    # 用例6：password 为空
    def test_add_user_empty_password(self):
        data = {"user_id": f"empty_pwd_{int(time.time())}", "password": "", "name": "", "desc": ""}
        resp = requests.post(ADD_USER_URL, json=data, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"空密码响应: {result}")

    # 用例7：缺少 user_id 字段
    def test_add_user_missing_user_id(self):
        data = {"password": "123", "name": "", "desc": ""}
        resp = requests.post(ADD_USER_URL, json=data, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"缺少user_id响应: {result}")

    # 用例8：缺少 password 字段
    def test_add_user_missing_password(self):
        data = {"user_id": f"no_pwd_{int(time.time())}", "name": "", "desc": ""}
        resp = requests.post(ADD_USER_URL, json=data, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"缺少password响应: {result}")

    # 用例9：请求体为空
    def test_add_user_empty_body(self):
        resp = requests.post(ADD_USER_URL, json={}, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"空请求体响应: {result}")

    # 用例10：user_id 含特殊字符
    def test_add_user_special_chars(self):
        data = {"user_id": "<script>alert(1)</script>", "password": "123", "name": "", "desc": ""}
        resp = requests.post(ADD_USER_URL, json=data, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"特殊字符user_id响应: {result}")


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
