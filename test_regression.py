"""
业务流程回归测试
- 业务线1（user_manage）：登录 → 添加用户
- 业务线2（dialogue）：登录 → 提问
"""
import requests
import pytest
import time

BASE_URL = "https://ai.qingxiang.tech:20000"
LOGIN_URL = f"{BASE_URL}/api/LoginService/login"
ADD_USER_URL = f"{BASE_URL}/api/UserService/add_user"
ASK_URL = f"{BASE_URL}/api/DialogService/ask"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*"
}


# ==================== 业务线1：登录 → 添加用户 ====================

@pytest.mark.user_manage
class TestUserManageFlow:
    """业务线1：用户管理流程（登录 → 添加用户）"""

    token = ""

    def test_step1_login(self):
        """第1步：登录获取 token"""
        login_data = {"username": "19900000001", "password": "123", "org_id": "default"}
        resp = requests.post(LOGIN_URL, json=login_data, headers=HEADERS, verify=False)
        assert resp.status_code == 200
        result = resp.json()
        assert result["code"] == 200, f"登录失败: {result}"

        # 从响应头获取 token
        TestUserManageFlow.token = resp.headers.get("refresh-token", "")
        assert TestUserManageFlow.token, "未获取到 token"
        print(f"\n[业务线1] 登录成功，token: {TestUserManageFlow.token[:50]}...")

    def test_step2_add_user(self):
        """第2步：使用 token 添加用户"""
        assert TestUserManageFlow.token, "前置步骤登录未成功，无法继续"

        h = HEADERS.copy()
        h["access-token"] = TestUserManageFlow.token

        # 用时间戳生成唯一用户名
        unique_id = f"reg_test_{int(time.time())}"
        data = {"user_id": unique_id, "password": "123", "name": "回归测试用户", "desc": "业务线1自动创建"}

        resp = requests.post(ADD_USER_URL, json=data, headers=h, verify=False)
        assert resp.status_code == 200
        result = resp.json()
        print(f"[业务线1] 添加用户响应: {result}")
        print(f"[业务线1] 流程完成：登录 ✓ → 添加用户 ✓")


# ==================== 业务线2：登录 → 提问 ====================

@pytest.mark.dialogue
class TestDialogueFlow:
    """业务线2：智能对话流程（登录 → 提问）"""

    token = ""

    def test_step1_login(self):
        """第1步：登录获取 token"""
        login_data = {"username": "19900000001", "password": "123", "org_id": "default"}
        resp = requests.post(LOGIN_URL, json=login_data, headers=HEADERS, verify=False)
        assert resp.status_code == 200
        result = resp.json()
        assert result["code"] == 200, f"登录失败: {result}"

        # 从响应头获取 token
        TestDialogueFlow.token = resp.headers.get("refresh-token", "")
        assert TestDialogueFlow.token, "未获取到 token"
        print(f"\n[业务线2] 登录成功，token: {TestDialogueFlow.token[:50]}...")

    def test_step2_ask(self):
        """第2步：使用 token 进行提问"""
        assert TestDialogueFlow.token, "前置步骤登录未成功，无法继续"

        h = HEADERS.copy()
        h["access-token"] = TestDialogueFlow.token

        data = {
            "question": {
                "did": "20260212104008476ddd38",
                "cid": f"regression_test_{int(time.time())}",
                "ask": {
                    "knowledge": "000211104710061034",
                    "question": "你好，这是回归测试的提问",
                    "attachment": [],
                    "style": "minimalist",
                    "skill": "dialogue",
                    "entry": "dialogue",
                    "tool_invokes": []
                }
            }
        }

        resp = requests.post(ASK_URL, json=data, headers=h, verify=False)
        assert resp.status_code == 200
        result = resp.json()
        assert result["code"] == 200, f"提问失败: {result}"
        print(f"[业务线2] 提问响应: {result}")
        print(f"[业务线2] 流程完成：登录 ✓ → 提问 ✓")


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
