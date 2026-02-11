# Appium 常见面试考点

> 适用于移动端测试 / APP 自动化测试岗位面试准备

---

## 一、Appium 基础概念（必会）

### Appium 是什么？

> Appium 是一个**开源、跨平台**的移动端自动化测试框架，支持 Android、iOS 和 Windows 应用。基于 **WebDriver 协议**（W3C），支持多种编程语言（Python、Java、JS 等）。

### 核心特点

| 特点 | 说明 |
|------|------|
| 跨平台 | 同一套 API 测试 Android 和 iOS |
| 不需要修改 App | 不需要嵌入 SDK 或重新编译 |
| 多语言支持 | Python、Java、JavaScript、Ruby 等 |
| 基于 WebDriver | 遵循 Selenium 的 Client-Server 架构 |
| 支持多种应用类型 | 原生（Native）、混合（Hybrid）、移动网页（Web） |

### Appium vs Selenium

| 对比项 | Appium | Selenium |
|--------|--------|----------|
| 测试对象 | **移动端 APP** | **Web 浏览器** |
| 协议 | WebDriver（扩展） | WebDriver |
| 底层驱动 | UIAutomator2(Android) / XCUITest(iOS) | ChromeDriver / GeckoDriver |
| 元素定位 | 使用 APP 控件属性 | 使用 HTML DOM 属性 |
| 相同点 | 都是 Client-Server 架构，API 风格类似 |

---

## 二、Appium 架构原理（高频考点）

### 工作流程

```
测试脚本（Client）
    ↓ 发送 HTTP 请求（JSON Wire Protocol）
Appium Server（Node.js）
    ↓ 解析命令，转发给对应驱动
    ├── Android → UIAutomator2 / Espresso
    └── iOS → XCUITest
    ↓ 驱动操作手机上的 App
手机设备 / 模拟器
```

### 关键组件

| 组件 | 作用 |
|------|------|
| **Appium Client** | 测试脚本（Python/Java），发送命令 |
| **Appium Server** | Node.js 服务，接收并转发命令 |
| **UIAutomator2** | Android 底层自动化引擎（Google 提供） |
| **XCUITest** | iOS 底层自动化引擎（Apple 提供） |
| **ADB** | Appium 通过 ADB 与 Android 设备通信 |

> **面试一句话**：Appium Server 是中间人，客户端发命令给 Server，Server 再通过 UIAutomator2（Android）或 XCUITest（iOS）操作真机。

---

## 三、Desired Capabilities（必考）

### 什么是 Desired Capabilities？

> 一组键值对参数，告诉 Appium Server 你要测试什么设备、什么 App、用什么引擎。

### 常用参数

```python
from appium import webdriver

desired_caps = {
    # 平台信息
    "platformName": "Android",            # 平台：Android / iOS
    "platformVersion": "12",              # 系统版本
    "deviceName": "Pixel_6",              # 设备名称

    # App 信息
    "appPackage": "com.example.app",      # 包名
    "appActivity": ".MainActivity",       # 启动 Activity
    # 或者直接指定 APK 路径
    # "app": "/path/to/app.apk",

    # 自动化引擎
    "automationName": "UiAutomator2",     # Android 用 UiAutomator2

    # 其他常用
    "noReset": True,                      # 不重置 App（保留登录状态）
    "unicodeKeyboard": True,              # 使用 Unicode 键盘（支持中文输入）
    "resetKeyboard": True,                # 测试完恢复原键盘
    "newCommandTimeout": 300,             # 超时时间（秒）
}

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
```

### 常考参数对比

| 参数 | 作用 | 常考点 |
|------|------|--------|
| `appPackage` | APP 包名 | 用 `aapt dump badging` 获取 |
| `appActivity` | 启动 Activity | 用 `aapt` 或 `adb shell dumpsys activity` 获取 |
| `noReset` | 不重置 App 状态 | `True` = 保留数据，`False` = 每次清空重装 |
| `fullReset` | 完全重置 | 卸载后重新安装 |
| `automationName` | 自动化引擎 | Android 用 `UiAutomator2`，iOS 用 `XCUITest` |

---

## 四、元素定位方式（高频必考）

### 定位方法

| 定位方式 | 方法 | 说明 |
|---------|------|------|
| **id** | `find_element(By.ID, "com.example:id/btn")` | resource-id，**最推荐** |
| **accessibility_id** | `find_element(AppiumBy.ACCESSIBILITY_ID, "Login")` | content-desc 属性 |
| **xpath** | `find_element(By.XPATH, "//android.widget.Button[@text='登录']")` | 万能但慢 |
| **class_name** | `find_element(By.CLASS_NAME, "android.widget.Button")` | 控件类名 |
| **Android UIAutomator** | `find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("登录")')` | Android 原生定位，**强大** |
| **iOS Predicate** | `find_element(AppiumBy.IOS_PREDICATE, 'name == "Login"')` | iOS 原生定位 |
| **iOS Class Chain** | `find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "Login"`]')` | iOS 链式定位 |

### 定位优先级

```
id > accessibility_id > Android UIAutomator / iOS Predicate > xpath
```

> **面试回答**：优先用 id（resource-id），其次 accessibility_id（content-desc），再次用平台原生定位（UiAutomator / Predicate），最后才用 xpath（慢且不稳定）。

### 获取元素属性的工具

| 工具 | 平台 | 说明 |
|------|------|------|
| **Appium Inspector** | 跨平台 | Appium 官方，最常用 |
| **uiautomatorviewer** | Android | Android SDK 自带 |
| **Android Studio Layout Inspector** | Android | 开发工具 |
| **Xcode Accessibility Inspector** | iOS | Xcode 自带 |

---

## 五、常用操作

### 基本操作

```python
# 点击
element.click()

# 输入文本
element.send_keys("hello")

# 清空文本
element.clear()

# 获取文本
text = element.text

# 获取属性
attr = element.get_attribute("resource-id")

# 判断元素是否存在/显示/可点击
element.is_displayed()
element.is_enabled()
element.is_selected()
```

### 滑动操作

```python
from appium.webdriver.common.touch_action import TouchAction

# 方式一：swipe（起点坐标 → 终点坐标）
driver.swipe(start_x, start_y, end_x, end_y, duration=800)

# 上滑（从下往上）
size = driver.get_window_size()
driver.swipe(size['width']/2, size['height']*0.8,
             size['width']/2, size['height']*0.2, 800)

# 下滑（从上往下）
driver.swipe(size['width']/2, size['height']*0.2,
             size['width']/2, size['height']*0.8, 800)

# 方式二：TouchAction
action = TouchAction(driver)
action.press(x=500, y=1500).wait(500).move_to(x=500, y=500).release().perform()
```

### 手势操作

```python
from appium.webdriver.common.touch_action import TouchAction

# 长按
action = TouchAction(driver)
action.long_press(element, duration=2000).release().perform()

# 双击（通过 TouchAction）
action.tap(element).wait(100).tap(element).perform()
```

### 系统操作

```python
# 截图
driver.get_screenshot_as_file("screenshot.png")

# 返回键
driver.back()

# 切换到后台再切回
driver.background_app(5)   # 后台 5 秒

# 获取当前 Activity
driver.current_activity

# 获取当前包名
driver.current_package

# 打开通知栏
driver.open_notifications()

# 安装/卸载 App
driver.install_app("/path/to/app.apk")
driver.remove_app("com.example.app")

# 判断 App 是否安装
driver.is_app_installed("com.example.app")

# 启动其他 App
driver.start_activity("com.example.app", ".MainActivity")
```

---

## 六、等待机制（常考）

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 隐式等待（全局）
driver.implicitly_wait(10)

# 显式等待（推荐）
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "com.example:id/btn")))

# 强制等待（不推荐）
import time
time.sleep(3)
```

> 与 Selenium 一样：**优先用显式等待**，避免用 `time.sleep`

---

## 七、混合应用（Hybrid App）测试

### 什么是混合应用？

> 应用中同时包含**原生控件（Native）**和**WebView（内嵌网页）**。例如微信小程序、APP 内打开的 H5 页面。

### 切换上下文

```python
# 查看所有上下文
contexts = driver.contexts
# 输出：['NATIVE_APP', 'WEBVIEW_com.example.app']

# 切换到 WebView
driver.switch_to.context('WEBVIEW_com.example.app')
# 此时可以像 Selenium 一样用 CSS/XPath 定位网页元素

# 切回原生
driver.switch_to.context('NATIVE_APP')
```

> **面试常问**：如何测试 Hybrid App？
> → 先用 `driver.contexts` 获取上下文列表 → `switch_to.context` 切换到 WebView → 用 Web 方式定位元素 → 操作完切回 NATIVE_APP

---

## 八、Toast 弹窗处理

```python
# Toast 是 Android 特有的轻提示，显示几秒后自动消失
# Appium 2.x + UiAutomator2 可以直接用 XPath 获取

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

toast_text = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//android.widget.Toast"))
).text
```

> **注意**：Toast 存在时间很短，必须用**显式等待**来捕获

---

## 九、Page Object 模式（框架设计）

### 分层结构

```
project/
├── base/
│   └── base_page.py          # 封装通用操作（点击、输入、等待、滑动）
├── pages/
│   ├── login_page.py         # 登录页元素 + 操作
│   └── home_page.py          # 首页元素 + 操作
├── testcases/
│   ├── test_login.py         # 登录测试用例
│   └── test_home.py          # 首页测试用例
├── configs/
│   └── caps_config.py        # Desired Capabilities 配置
├── data/
│   └── test_data.yaml        # 测试数据
├── reports/                   # Allure 报告
├── conftest.py               # pytest fixture（driver 初始化）
└── pytest.ini                # pytest 配置
```

### 示例代码

```python
# base/base_page.py
class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        self.find(locator).click()

    def input(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def swipe_up(self):
        size = self.driver.get_window_size()
        self.driver.swipe(size['width']/2, size['height']*0.8,
                          size['width']/2, size['height']*0.2, 800)


# pages/login_page.py
class LoginPage(BasePage):
    username_loc = (By.ID, "com.example:id/et_username")
    password_loc = (By.ID, "com.example:id/et_password")
    login_btn_loc = (By.ID, "com.example:id/btn_login")

    def login(self, username, password):
        self.input(self.username_loc, username)
        self.input(self.password_loc, password)
        self.click(self.login_btn_loc)


# testcases/test_login.py
class TestLogin:
    def test_login_success(self, driver):
        login_page = LoginPage(driver)
        login_page.login("admin", "123456")
        # 断言...
```

---

## 十、常见问题与解决

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 找不到元素 | 页面未加载完 / 定位不对 | 加显式等待 / 检查定位表达式 |
| 中文输入失败 | 键盘问题 | 设置 `unicodeKeyboard: True` |
| Toast 抓不到 | 消失太快 | 显式等待 + XPath |
| WebView 元素找不到 | 没切换上下文 | `switch_to.context('WEBVIEW_xxx')` |
| Session 超时 | 操作间隔太长 | 增大 `newCommandTimeout` |
| App 没启动 | Capabilities 配错 | 检查 `appPackage` 和 `appActivity` |
| 滑动不生效 | 坐标算错 | 用 `get_window_size()` 动态计算 |

---

## 十一、常见面试题及参考答案

### Q1：Appium 的工作原理是什么？

> Client 发送命令到 Appium Server（HTTP 请求）→ Server 通过 UIAutomator2（Android）或 XCUITest（iOS）驱动真机执行操作 → 返回结果给 Client。

### Q2：Appium 和 Selenium 的区别？

> Appium 测试移动端 APP，Selenium 测试 Web 浏览器。两者都基于 WebDriver 协议，API 风格类似，Appium 可以看作 Selenium 在移动端的扩展。

### Q3：APP 自动化中如何定位元素？优先用哪种？

> 优先 id（resource-id）→ accessibility_id → UiAutomator / iOS Predicate → XPath。定位工具用 Appium Inspector。

### Q4：如何处理 Hybrid App？

> 用 `driver.contexts` 获取上下文 → `switch_to.context` 切换到 WebView → 用 Web 定位方式操作 → 操作完切回 NATIVE_APP。

### Q5：noReset 和 fullReset 的区别？

> `noReset=True`：不清除数据，保留登录状态；`fullReset=True`：卸载后重新安装 APP，完全干净的初始状态。

### Q6：如何处理弹窗/Toast？

> 系统弹窗用 `driver.switch_to.alert`；Toast 用显式等待 + XPath `//android.widget.Toast` 捕获。

### Q7：Appium 如何实现滑动操作？

> 用 `driver.swipe(start_x, start_y, end_x, end_y, duration)`，通过 `get_window_size()` 动态计算坐标。

### Q8：如何获取 App 的包名和启动 Activity？

> `aapt dump badging app.apk` 或 `adb shell dumpsys activity recents | grep "intent"` 获取。

---

## 速记口诀

```
Appium = Selenium 的移动端版本
架构：Client → Server → UIAutomator2(Android) / XCUITest(iOS) → 手机

Desired Caps 四要素：platformName + deviceName + appPackage + appActivity
noReset 保状态，fullReset 全清空

定位优先级：id > accessibility_id > UiAutomator > xpath
定位工具：Appium Inspector

等待：显式优先，隐式全局，强制别用
混合应用：contexts 获取 → switch_to.context 切换

框架：PO 模式 + base 封装 + conftest 管 driver
```

---

*可与《15-ADB命令常见面试考点.md》搭配复习，ADB 是 Appium 的基础，两者常一起考。*
