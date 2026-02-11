# Allure 报告与 Mock 常见面试考点

> 适用于测试开发 / 自动化测试岗位面试准备

---

# 第一部分：Allure 测试报告

---

## 一、Allure 是什么？

> Allure 是一个**轻量灵活**的测试报告框架，支持多种测试框架（pytest、JUnit、TestNG 等），生成**美观、交互式**的 HTML 报告。

### 为什么用 Allure？

| 优势 | 说明 |
|------|------|
| 美观 | 图表化展示，比 pytest-html 更专业 |
| 交互式 | 可展开查看每一步操作详情 |
| 多维度 | 按功能/故事/严重级别等维度统计 |
| 附件 | 支持截图、日志、请求/响应数据 |
| CI 集成 | 可集成 Jenkins / GitLab CI / GitHub Actions |

---

## 二、pytest + Allure 集成

### 安装

```bash
pip install allure-pytest

# 安装 Allure 命令行工具（生成报告用）
# Windows: scoop install allure
# Mac: brew install allure
```

### 运行并生成报告

```bash
# 运行测试，生成 Allure 数据
pytest --alluredir=./allure-results

# 根据数据生成 HTML 报告并打开
allure serve ./allure-results

# 或生成静态报告
allure generate ./allure-results -o ./allure-report --clean
allure open ./allure-report
```

---

## 三、Allure 常用装饰器（面试常考）

```python
import allure

@allure.epic("用户管理模块")            # 史诗（最大分类）
@allure.feature("登录功能")             # 功能模块
@allure.story("正常登录")               # 用户故事
@allure.title("测试用户名密码正确登录")   # 用例标题
@allure.severity(allure.severity_level.CRITICAL)  # 严重级别
@allure.description("验证使用正确的用户名密码可以成功登录")
@allure.link("https://jira.example.com/PROJ-123", name="需求链接")
@allure.issue("https://jira.example.com/BUG-456", name="Bug链接")
def test_login_success():
    with allure.step("步骤1：输入用户名"):
        pass
    with allure.step("步骤2：输入密码"):
        pass
    with allure.step("步骤3：点击登录"):
        pass
    with allure.step("步骤4：验证登录成功"):
        assert True
```

### 装饰器层级关系

```
epic（史诗）
  └── feature（功能）
       └── story（故事）
            └── title（用例标题）
                 └── step（步骤）
```

### 严重级别

| 级别 | 含义 | 用途 |
|------|------|------|
| `BLOCKER` | 阻塞 | 系统无法使用 |
| `CRITICAL` | 严重 | 核心功能失败 |
| `NORMAL` | 普通 | 一般功能（默认） |
| `MINOR` | 次要 | UI 问题等 |
| `TRIVIAL` | 轻微 | 文案错误等 |

---

## 四、Allure 附件（截图/日志）

```python
import allure

# 添加文本附件
allure.attach("这是请求Body", name="请求数据", attachment_type=allure.attachment_type.TEXT)

# 添加 JSON 附件
allure.attach('{"code": 200}', name="响应数据", attachment_type=allure.attachment_type.JSON)

# 添加截图（Selenium/Appium）
allure.attach(driver.get_screenshot_as_png(), name="失败截图",
              attachment_type=allure.attachment_type.PNG)

# 添加文件附件
allure.attach.file("./log.txt", name="日志文件", attachment_type=allure.attachment_type.TEXT)
```

### 失败自动截图（conftest.py）

```python
# conftest.py
import allure
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="失败截图",
                attachment_type=allure.attachment_type.PNG
            )
```

---

## 五、Allure + CI 集成

### Jenkins 集成

```
1. 安装 Jenkins Allure 插件
2. Jenkinsfile 中添加：
   - 运行 pytest --alluredir=allure-results
   - 构建后操作：Allure Report → Path: allure-results
3. 构建完成后自动展示报告
```

### GitHub Actions 集成

```yaml
- name: Run tests
  run: pytest --alluredir=allure-results

- name: Allure Report
  uses: simple-elf/allure-report-action@master
  with:
    allure_results: allure-results

- name: Deploy report to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: allure-history
```

---

# 第二部分：Mock / 桩服务

---

## 六、Mock 基础概念

### 什么是 Mock？

> Mock 是指用**模拟对象**替代真实依赖，使测试不受外部依赖影响。

### 为什么要 Mock？

| 场景 | 说明 |
|------|------|
| 第三方接口没准备好 | 后端没开发完，前端要先测试 |
| 依赖服务不稳定 | 第三方短信/支付接口不稳定 |
| 构造异常场景 | 模拟 500 错误、超时、空数据 |
| 隔离测试 | 单元测试不依赖数据库/网络 |
| 提高速度 | 避免真实网络请求，测试更快 |

---

## 七、Python unittest.mock（最常用）

### 基本用法

```python
from unittest.mock import Mock, patch, MagicMock

# 创建 Mock 对象
mock_obj = Mock()
mock_obj.method.return_value = "模拟返回值"
print(mock_obj.method())  # "模拟返回值"

# 设置副作用（抛异常）
mock_obj.method.side_effect = ValueError("模拟异常")
```

### @patch 装饰器（最常用）

```python
from unittest.mock import patch
import requests

# 原始函数
def get_user_info(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# 测试时 Mock 掉 requests.get
@patch("requests.get")
def test_get_user_info(mock_get):
    # 设置 Mock 返回值
    mock_get.return_value.json.return_value = {"name": "张三", "age": 25}
    mock_get.return_value.status_code = 200

    result = get_user_info(1)
    assert result["name"] == "张三"

    # 验证是否调用了正确的 URL
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

### patch 作为上下文管理器

```python
def test_with_context_manager():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"code": 200}
        result = get_user_info(1)
        assert result["code"] == 200
```

### Mock 常用断言

```python
mock_obj.method.assert_called()                    # 被调用过
mock_obj.method.assert_called_once()               # 只被调用 1 次
mock_obj.method.assert_called_with(arg1, arg2)     # 用指定参数调用
mock_obj.method.assert_not_called()                # 没被调用
mock_obj.method.call_count                         # 调用次数
```

---

## 八、pytest-mock 插件

```python
# 安装：pip install pytest-mock

def test_with_mocker(mocker):
    # mocker 是 pytest-mock 提供的 fixture
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.json.return_value = {"name": "测试"}

    result = get_user_info(1)
    assert result["name"] == "测试"
```

---

## 九、接口级 Mock 工具

### 常见工具对比

| 工具 | 特点 | 适用场景 |
|------|------|---------|
| **unittest.mock** | Python 标准库，代码级 Mock | 单元测试 |
| **pytest-mock** | pytest 集成的 mock fixture | 单元测试 |
| **mitmproxy** | 中间人代理，可编程 | 接口级 Mock/抓包 |
| **WireMock** | 独立 Mock 服务器（Java） | 微服务集成测试 |
| **JSON Server** | 快速搭建 REST Mock 服务 | 前后端联调 |
| **Charles Map Local** | 本地文件替代响应 | 手动 Mock |

### mitmproxy 示例

```python
# mock_script.py（mitmproxy 脚本）
from mitmproxy import http

def response(flow: http.HTTPFlow):
    if "api.example.com/users" in flow.request.url:
        flow.response = http.Response.make(
            200,
            '{"name": "Mock用户", "age": 0}',
            {"Content-Type": "application/json"}
        )

# 运行：mitmproxy -s mock_script.py
```

### JSON Server（快速搭建）

```bash
# 安装
npm install -g json-server

# 创建 db.json
{
  "users": [
    {"id": 1, "name": "张三"},
    {"id": 2, "name": "李四"}
  ]
}

# 启动
json-server --watch db.json --port 3000

# 自动生成 RESTful API
# GET    http://localhost:3000/users
# GET    http://localhost:3000/users/1
# POST   http://localhost:3000/users
# PUT    http://localhost:3000/users/1
# DELETE http://localhost:3000/users/1
```

---

## 十、常见面试题及参考答案

### Q1：什么是 Mock？为什么要用？

> Mock 是用模拟对象替代真实依赖。当第三方接口没准备好、服务不稳定、需要构造异常场景时，用 Mock 隔离依赖，保证测试可控。

### Q2：Allure 报告的层级结构是什么？

> epic → feature → story → title → step。分别对应项目模块 → 功能 → 用户故事 → 用例标题 → 测试步骤。

### Q3：如何在 Allure 报告中添加失败截图？

> 在 conftest.py 中用 `pytest_runtest_makereport` 钩子，检测用例失败时自动调用 `allure.attach` 添加截图。

### Q4：@patch 的工作原理？

> @patch 临时替换指定模块的对象为 Mock 对象，测试结束后自动恢复。需要注意 patch 的路径是**使用位置**而非定义位置。

### Q5：Mock 的 return_value 和 side_effect 区别？

> `return_value` 设置固定返回值；`side_effect` 可以设置异常、多次不同返回值、或自定义函数逻辑。

### Q6：如何在自动化框架中集成 Allure？

> 安装 allure-pytest → 用 `--alluredir` 指定数据目录 → 用装饰器标记用例层级 → 用 `allure.step` 添加步骤 → CI 中集成 Allure 插件生成报告。

### Q7：Mock 和桩（Stub）的区别？

> Stub 只提供固定返回值，不验证调用行为；Mock 除了提供返回值外，还可以验证是否被调用、调用次数、调用参数等。

---

## 速记口诀

```
Allure 层级：epic > feature > story > title > step
报告命令：pytest --alluredir → allure serve
失败截图：conftest + pytest hook + allure.attach

Mock = 模拟依赖，隔离测试
@patch 替换模块对象，测完自动恢复
return_value 定返回，side_effect 抛异常
assert_called_once 验证调用

代码级 Mock → unittest.mock / pytest-mock
接口级 Mock → mitmproxy / WireMock / JSON Server
手动 Mock → Charles Map Local
```

---

*可与《02-Python自动化测试常见面试题.md》《05-CI_CD常见面试题.md》搭配复习，Allure 是自动化报告标配，Mock 是测试隔离的核心技能。*
