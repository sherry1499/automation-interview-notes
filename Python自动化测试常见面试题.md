# Python 自动化测试常见面试题总结

> 适用于自动化测试 / 测试开发岗位面试准备

---

## 一、Python 基础

### 1. `*args` 和 `**kwargs` 的区别与用法？

- **\*args**：接收任意个**位置参数**，打包成元组。
- **\*\*kwargs**：接收任意个**关键字参数**，打包成字典。

```python
def demo(*args, **kwargs):
    print(args)    # (1, 2, 3)
    print(kwargs)  # {'a': 1, 'b': 2}
demo(1, 2, 3, a=1, b=2)
```

**面试点**：在封装通用请求方法、装饰器、测试数据驱动时常用。

---

### 2. 深拷贝和浅拷贝的区别？

- **浅拷贝**：只复制第一层，嵌套对象仍是引用（`copy.copy()`、列表切片、`dict.copy()`）。
- **深拷贝**：递归复制所有层级（`copy.deepcopy()`）。

**面试点**：测试数据在用例间共享时，若修改可变对象，要注意用深拷贝避免互相污染。

---

### 3. `__new__` 和 `__init__` 的区别？

- **__new__**：创建对象时调用，返回实例；可用于单例、不可变类型定制。
- **__init__**：在 `__new__` 之后调用，对实例做初始化，不返回值。

---

### 4. 单例模式如何实现？（写一种即可）

```python
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**面试点**：连接池、Driver 复用等场景可能用到。

---

### 5. 实例方法、类方法、静态方法的区别？

| 类型       | 装饰器    | 第一个参数 | 典型用途           |
|------------|-----------|------------|--------------------|
| 实例方法   | 无        | self       | 操作实例属性       |
| 类方法     | @classmethod | cls      | 操作类属性、工厂方法 |
| 静态方法   | @staticmethod | 无      | 与类相关的工具函数   |

---

### 6. 垃圾回收机制简要说明？

- 引用计数为主：引用为 0 时回收。
- 循环引用通过**标记-清除**或**分代回收**处理。
- 面试时能说出「引用计数 + 循环引用处理」即可。

---

## 二、unittest 与 pytest

### 7. unittest 和 pytest 的区别？为什么更常用 pytest？

| 对比项     | unittest           | pytest                    |
|------------|--------------------|---------------------------|
| 来源       | 标准库             | 第三方                    |
| 用例发现   | 需继承 TestCase    | 自动发现 test_*.py / test_* |
| 前置后置   | setUp/tearDown     | fixture，作用域更灵活     |
| 参数化     | 需 subTest 等      | @pytest.mark.parametrize  |
| 断言       | self.assertEqual 等 | 直接用 assert             |
| 插件       | 少                 | 多（报告、并发、重试等）  |

**答**：pytest 语法简洁、fixture 强大、参数化方便、插件多，所以自动化项目里更常用 pytest。

---

### 8. pytest 的 fixture 作用域有哪些？

- **function**：每个用例执行一次（默认）。
- **class**：每个测试类执行一次。
- **module**：每个 .py 文件执行一次。
- **package**：每个包执行一次。
- **session**：整个测试会话一次（如只起一次浏览器）。

---

### 9. pytest 如何做参数化？写一个例子。

```python
@pytest.mark.parametrize("username,password,expected", [
    ("admin", "123456", True),
    ("wrong", "wrong", False),
])
def test_login(username, password, expected):
    assert login(username, password) == expected
```

**面试点**：数据驱动、多组输入输出校验。

---

### 10. pytest 常用插件有哪些？

- **pytest-html**：生成 HTML 报告
- **pytest-cov**：代码覆盖率
- **pytest-xdist**：多进程/多线程并发
- **pytest-rerunfailures**：失败重试
- **allure-pytest**：Allure 报告
- **pytest-ordering**：控制用例顺序（慎用）

---

## 三、Selenium Web 自动化

### 11. Selenium 有哪些元素定位方式？优先用哪种？

常见 8 种：**id、name、class_name、tag_name、link_text、partial_link_text、xpath、css_selector**。

**优先级**：**id > name > css > xpath**。  
原因：id 通常唯一稳定；xpath 易受结构变化影响，且执行较慢，尽量用相对路径或 css。

---

### 12. 三种等待机制的区别？推荐哪种？

| 方式       | 写法/含义              | 特点           |
|------------|------------------------|----------------|
| 强制等待   | time.sleep(n)          | 固定时间，不推荐 |
| 隐式等待   | driver.implicitly_wait(n) | 全局，找不到就等 n 秒再抛异常 |
| 显式等待   | WebDriverWait + expected_conditions | 等具体条件（如元素可见、可点击） |

**推荐**：**显式等待**。针对关键元素设置条件，稳定且不浪费多余时间。

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submit"))
)
```

---

### 13. 常见 Selenium 异常有哪些？

- **NoSuchElementException**：找不到元素
- **ElementNotVisibleException**：元素不可见
- **ElementNotInteractableException**：元素不可交互
- **TimeoutException**：显式等待超时
- **StaleElementReferenceException**：元素引用过期（如 DOM 刷新后仍用旧引用）

---

### 14. 如何处理多窗口 / 多 Frame？

- **多窗口**：`driver.window_handles` 获取所有句柄，`driver.switch_to.window(handle)` 切换。
- **Frame**：`driver.switch_to.frame(index/name/id/webelement)` 进入；`driver.switch_to.default_content()` 回到主文档。

---

### 15. 如何处理 Alert 弹窗？

```python
alert = driver.switch_to.alert
alert.text      # 获取文本
alert.accept()  # 确定
alert.dismiss() # 取消
alert.send_keys("输入内容")  # 若有输入框
```

---

### 16. 如何提高 Selenium 脚本稳定性？

- 少用 `time.sleep`，多用**显式等待**。
- 定位优先 **id/name/css**，xpath 用**相对路径**，避免过长绝对路径。
- 对常用定位做**二次封装**（如结合 WebDriverWait + expected_conditions）。
- 关键操作后加**简单断言**，失败早暴露。
- 必要时用 **pytest-rerunfailures** 对偶发失败重试。

---

## 四、Page Object（PO）模式

### 17. 什么是 Page Object？有什么好处？

**定义**：把每个页面封装成类，页面上的元素和操作封装成类的方法，测试用例只调方法不直接操作元素。

**好处**：
- 页面变更时只改 PO，用例改动少。
- 复用高，可读性好。
- 元素与业务分离，便于维护。

---

### 18. PO 设计原则有哪些？

- 一个页面（或一个稳定模块）一个 PO 类。
- 对外只暴露**业务方法**（如 login、search），不暴露元素定位细节。
- 方法内部**不要写断言**，断言放在测试层。
- 同一操作不同结果可拆成不同方法（如 login_success、login_fail）。

---

## 五、接口自动化

### 19. 接口自动化框架一般包含哪些部分？

- 请求封装（如对 requests 的二次封装）。
- 配置管理（环境、host、账号等）。
- 用例组织（pytest + 参数化）。
- 断言（状态码、业务码、关键字段）。
- 日志与报告（logging + pytest-html/allure）。
- 可选：数据库校验、依赖接口处理、Mock、重试、CI 集成。

---

### 20. requests 中 get 和 post 怎么传参？

- **GET**：params 字典，会拼到 URL 查询串。
- **POST**：body 常用 `data=`（表单）、`json=`（JSON），headers 里 Content-Type 要一致。

```python
r = requests.get(url, params={"key": "value"})
r = requests.post(url, json={"key": "value"}, headers={"Content-Type": "application/json"})
```

---

### 21. 接口测试如何做鉴权？（常见方式）

- **Bearer Token**：headers 里 `Authorization: Bearer <token>`。
- **Cookie/Session**：登录后保持 session 或把 cookie 带给后续请求。
- **签名**：按约定对参数排序、拼接、加密，放 query/header/body。
- **Basic Auth**：`auth=(user, pass)` 或 base64 放 header。

---

## 六、综合与项目

### 22. 什么样的项目适合做 UI 自动化？

- 需求相对稳定、界面不频繁大改。
- 回归场景多、重复执行价值高。
- 项目周期较长，能摊薄脚本开发与维护成本。
- 核心流程清晰（登录、主流程、关键校验）。

---

### 23. 自动化测试在 CI/CD 中如何集成？

- 用 **Jenkins / GitLab CI / GitHub Actions** 等触发测试（如代码提交、定时）。
- 命令示例：`pytest tests/ -v --html=report.html`。
- 可配合 **Docker + Selenium Grid** 做多浏览器/多节点。
- 报告归档、失败通知（邮件/企微/钉钉）。

---

### 24. 你用过哪些自动化相关工具/库？

可按实际回答，例如：

- **Web**：Selenium、Playwright
- **接口**：requests、httpx
- **框架**：pytest、unittest
- **报告**：pytest-html、Allure
- **持续集成**：Jenkins、GitHub Actions
- **其他**：Appium（移动端）、Fiddler/Charles（抓包）

---

### 25. 遇到过哪些难以稳定的自动化问题？怎么解决的？

**常见问题**：
- 元素找不到 → 显式等待 + 更稳的定位方式。
- 动态 id/class → 用相对 xpath、文本、父子关系等。
- 弹窗/新窗口 → switch_to.alert / switch_to.window。
- 偶发失败 → 重试、重跑、排查环境与数据。

回答时结合自己项目，说清楚**现象 → 原因 → 解决方式**即可。

---

## 七、代码与场景题（可能要求手写）

### 26. 用 pytest + Selenium 写一个简单登录用例（伪代码即可）

```python
def test_login(driver):  # driver 由 fixture 提供
    driver.get("https://example.com/login")
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.ID, "submit").click()
    assert "欢迎" in driver.page_source or driver.current_url == "https://example.com/home"
```

---

### 27. 用 requests 写一个 GET 请求并做简单断言

```python
import requests
r = requests.get("https://api.example.com/user/1")
assert r.status_code == 200
data = r.json()
assert data["username"] == "admin"
```

---

### 28. 设计一个简单的 PO：登录页（只写思路或类结构）

```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://example.com/login"

    def open(self):
        self.driver.get(self.url)

    def input_username(self, text):
        self.driver.find_element(By.ID, "username").send_keys(text)

    def input_password(self, text):
        self.driver.find_element(By.ID, "password").send_keys(text)

    def click_login(self):
        self.driver.find_element(By.ID, "submit").click()

    def login(self, username, password):
        self.open()
        self.input_username(username)
        self.input_password(password)
        self.click_login()
```

---

## 八、速记清单（考前扫一眼）

- **等待**：显式 > 隐式 > sleep
- **定位**：id > name > css > xpath（相对）
- **框架**：pytest + fixture + parametrize
- **PO**：页面即类，操作为方法，断言在用例
- **接口**：封装请求、统一断言、配置与环境分离
- **稳定性**：等待 + 稳定定位 + 重试 + 日志与报告

---

*按实际项目经验调整表述，面试时结合 STAR（情境-任务-行动-结果）回答项目题效果更好。*
