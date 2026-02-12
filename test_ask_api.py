import requests
import pytest

BASE_URL = "https://ai.qingxiang.tech:20000"
LOGIN_URL = f"{BASE_URL}/api/LoginService/login"
ASK_URL = f"{BASE_URL}/api/DialogService/ask"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*"
}


class TestAskAPI:
    """对话接口测试"""

    @classmethod
    def setup_class(cls):
        """所有用例执行前，先登录获取 token（token 在响应头里）"""
        login_data = {"username": "19900000001", "password": "123", "org_id": "default"}
        resp = requests.post(LOGIN_URL, json=login_data, headers=HEADERS, verify=False)
        # token 在响应头的 refresh-token 字段里
        cls.token = resp.headers.get("refresh-token", "")
        print(f"\n获取到 token: {cls.token[:50]}..." if cls.token else "未获取到 token")

    def _get_headers(self, token=None):
        """构造带 token 的请求头"""
        h = HEADERS.copy()
        h["access-token"] = token if token else self.token
        return h

    def _build_ask_data(self, question="你好", did="20260212104008476ddd38",
                        cid="177088698630934zmnjgwuz278beb5a5-2b79-4bf0-8d2e-67f267ed616d",
                        knowledge="000211104710061034"):
        """构造请求体"""
        return {
            "question": {
                "did": did,
                "cid": cid,
                "ask": {
                    "knowledge": knowledge,
                    "question": question,
                    "attachment": [],
                    "style": "minimalist",
                    "skill": "dialogue",
                    "entry": "dialogue",
                    "tool_invokes": []
                }
            }
        }

    # ===== 正常场景 =====

    # 用例1：正常提问
    def test_ask_success(self):
        data = self._build_ask_data(question="你好")
        resp = requests.post(ASK_URL, json=data, headers=self._get_headers(), verify=False)
        assert resp.status_code == 200
        result = resp.json()
        print(f"正常提问响应: {result}")

    # 用例2：提问较长内容
    def test_ask_long_question(self):
        data = self._build_ask_data(question="请详细介绍一下Python的装饰器是什么，有什么用途")
        resp = requests.post(ASK_URL, json=data, headers=self._get_headers(), verify=False)
        assert resp.status_code == 200
        result = resp.json()
        print(f"长问题响应: {result}")

    # ===== 认证相关 =====

    # 用例3：不带 token
    def test_ask_no_token(self):
        h = HEADERS.copy()
        h["access-token"] = ""
        data = self._build_ask_data(question="你好")
        resp = requests.post(ASK_URL, json=data, headers=h, verify=False)
        result = resp.json()
        print(f"无token响应: {result}")
        # 预期应该返回未授权错误

    # 用例4：错误的 token
    def test_ask_invalid_token(self):
        data = self._build_ask_data(question="你好")
        resp = requests.post(ASK_URL, json=data, headers=self._get_headers(token="invalid_token_123"), verify=False)
        result = resp.json()
        print(f"错误token响应: {result}")

    # ===== 参数异常 =====

    # 用例5：问题为空
    def test_ask_empty_question(self):
        data = self._build_ask_data(question="")
        resp = requests.post(ASK_URL, json=data, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"空问题响应: {result}")

    # 用例6：did 为空
    def test_ask_empty_did(self):
        data = self._build_ask_data(question="你好", did="")
        resp = requests.post(ASK_URL, json=data, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"空did响应: {result}")

    # 用例7：cid 为空
    def test_ask_empty_cid(self):
        data = self._build_ask_data(question="你好", cid="")
        resp = requests.post(ASK_URL, json=data, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"空cid响应: {result}")

    # 用例8：knowledge 为空
    def test_ask_empty_knowledge(self):
        data = self._build_ask_data(question="你好", knowledge="")
        resp = requests.post(ASK_URL, json=data, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"空knowledge响应: {result}")

    # 用例9：不存在的 did
    def test_ask_invalid_did(self):
        data = self._build_ask_data(question="你好", did="not_exist_did_12345")
        resp = requests.post(ASK_URL, json=data, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"无效did响应: {result}")

    # 用例10：请求体为空
    def test_ask_empty_body(self):
        resp = requests.post(ASK_URL, json={}, headers=self._get_headers(), verify=False)
        result = resp.json()
        print(f"空请求体响应: {result}")


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])