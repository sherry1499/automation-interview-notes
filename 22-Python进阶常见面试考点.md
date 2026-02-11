# Python 进阶常见面试考点

> 适用于中高级测试开发 / 自动化测试岗位面试准备
> 本篇聚焦：多线程、多进程、异步、装饰器进阶、生成器、设计模式等

---

## 一、多线程 threading（高频）

### 基本用法

```python
import threading
import time

def task(name):
    print(f"{name} 开始")
    time.sleep(2)
    print(f"{name} 结束")

# 创建线程
t1 = threading.Thread(target=task, args=("线程1",))
t2 = threading.Thread(target=task, args=("线程2",))

t1.start()    # 启动线程
t2.start()

t1.join()     # 等待线程执行完毕
t2.join()

print("全部完成")
```

### 线程锁（Lock）

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        lock.acquire()      # 加锁
        counter += 1
        lock.release()      # 释放锁
        # 或使用 with 语法：
        # with lock:
        #     counter += 1

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start(); t2.start()
t1.join(); t2.join()
print(counter)  # 200000（加锁后结果正确）
```

### 守护线程

```python
t = threading.Thread(target=task, daemon=True)
t.start()
# 主线程结束时，守护线程会被强制终止
```

---

## 二、GIL 全局解释器锁（必考）

### 什么是 GIL？

> GIL（Global Interpreter Lock）是 CPython 中的一个互斥锁，**同一时刻只允许一个线程执行 Python 字节码**。

### GIL 的影响

| 场景 | 多线程有效吗？ | 原因 |
|------|--------------|------|
| **IO 密集型**（网络请求、文件读写） | ✅ **有效** | IO 等待时会释放 GIL |
| **CPU 密集型**（大量计算） | ❌ **无效** | GIL 限制了并行计算 |

### 怎么解决 GIL 的限制？

| 方案 | 适用场景 |
|------|---------|
| **多进程**（multiprocessing） | CPU 密集型 |
| **多线程**（threading） | IO 密集型 |
| **协程**（asyncio） | IO 密集型（更轻量） |
| C 扩展 | 绕过 GIL |

> **面试一句话**：GIL 导致多线程无法利用多核 CPU 做并行计算。IO 密集型用多线程/协程，CPU 密集型用多进程。

---

## 三、多进程 multiprocessing

### 基本用法

```python
from multiprocessing import Process

def task(name):
    print(f"{name} 进程 PID: {os.getpid()}")

p1 = Process(target=task, args=("进程1",))
p2 = Process(target=task, args=("进程2",))

p1.start()
p2.start()
p1.join()
p2.join()
```

### 进程池

```python
from multiprocessing import Pool

def square(n):
    return n * n

with Pool(4) as pool:                    # 4 个工作进程
    results = pool.map(square, [1, 2, 3, 4, 5])
    print(results)  # [1, 4, 9, 16, 25]
```

### 进程间通信

```python
from multiprocessing import Queue

q = Queue()
q.put("hello")         # 放入数据
data = q.get()         # 取出数据
```

### 多线程 vs 多进程（必考）

| 对比项 | 多线程（threading） | 多进程（multiprocessing） |
|--------|-------------------|-------------------------|
| 内存 | 共享内存 | 独立内存空间 |
| 开销 | 轻量 | 较重（创建进程开销大） |
| GIL | 受限 | **不受限**（每个进程有自己的 GIL） |
| 适用 | **IO 密集型** | **CPU 密集型** |
| 通信 | 直接共享变量（需加锁） | 需要 Queue / Pipe |
| 稳定性 | 一个线程崩 → 整个进程崩 | 一个进程崩 → 不影响其他 |

---

## 四、协程 asyncio（加分项）

### 基本概念

> 协程是**用户态**的轻量级线程，在**单线程**内通过切换实现并发。比多线程更轻量，没有线程切换的开销。

### 基本用法

```python
import asyncio

async def fetch_data(name, delay):
    print(f"{name} 开始请求")
    await asyncio.sleep(delay)      # 模拟 IO 等待（非阻塞）
    print(f"{name} 请求完成")
    return f"{name} 的数据"

async def main():
    # 并发执行多个协程
    results = await asyncio.gather(
        fetch_data("任务1", 2),
        fetch_data("任务2", 3),
        fetch_data("任务3", 1),
    )
    print(results)

asyncio.run(main())
# 总耗时约 3 秒（不是 6 秒），因为是并发执行
```

### aiohttp（异步 HTTP 请求）

```python
import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = ["https://api.example.com/1", "https://api.example.com/2"]
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)

asyncio.run(main())
```

### 三种并发方式总结（必考）

| 方式 | 库 | 适用场景 | 并发原理 |
|------|---|---------|---------|
| 多线程 | `threading` | IO 密集型 | OS 线程切换 |
| 多进程 | `multiprocessing` | CPU 密集型 | 多核并行 |
| 协程 | `asyncio` | IO 密集型（大量请求） | 单线程事件循环 |

---

## 五、装饰器进阶

### 带参数的装饰器

```python
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)           # 执行 3 次
def say_hello():
    print("Hello!")

say_hello()
# 输出 3 次 Hello!
```

### 类装饰器

```python
class Timer:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        import time
        start = time.time()
        result = self.func(*args, **kwargs)
        print(f"耗时: {time.time() - start:.2f}s")
        return result

@Timer
def slow_function():
    time.sleep(1)

slow_function()  # 输出：耗时: 1.00s
```

### functools.wraps（保留原函数信息）

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)              # 保留原函数的 __name__、__doc__ 等
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## 六、生成器与迭代器

### 生成器（Generator）

```python
# 用 yield 创建生成器（惰性求值，节省内存）
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)

# 生成器表达式
squares = (x**2 for x in range(1000000))   # 不会立即计算
```

### 迭代器 vs 可迭代对象

| 概念 | 说明 | 举例 |
|------|------|------|
| 可迭代对象 | 实现了 `__iter__` 方法 | list、tuple、dict、str |
| 迭代器 | 实现了 `__iter__` + `__next__` 方法 | 生成器、文件对象 |

```python
# 判断是否可迭代
from collections.abc import Iterable, Iterator

isinstance([1,2,3], Iterable)   # True
isinstance([1,2,3], Iterator)   # False

gen = (x for x in range(3))
isinstance(gen, Iterator)       # True
```

### yield vs return

| 对比 | return | yield |
|------|--------|-------|
| 行为 | 返回值并**终止**函数 | 返回值并**暂停**函数 |
| 内存 | 一次返回全部数据 | 惰性求值，按需生成 |
| 适用 | 数据量小 | **数据量大**，节省内存 |

---

## 七、上下文管理器

### with 语句原理

```python
# with 语句自动调用 __enter__ 和 __exit__
with open("file.txt", "r") as f:
    content = f.read()
# 离开 with 块后，f 自动关闭（即使出现异常）
```

### 自定义上下文管理器

```python
# 方式一：类实现
class MyContext:
    def __enter__(self):
        print("进入")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("退出")
        return False    # False = 不吞掉异常

with MyContext() as ctx:
    print("执行中")

# 方式二：contextmanager 装饰器
from contextlib import contextmanager

@contextmanager
def my_context():
    print("进入")
    yield              # yield 之前 = __enter__，之后 = __exit__
    print("退出")

with my_context():
    print("执行中")
```

### 实际应用

```python
# 数据库连接管理
@contextmanager
def db_connection():
    conn = create_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

with db_connection() as conn:
    conn.execute("INSERT INTO ...")
```

---

## 八、常用设计模式（面试加分）

### 单例模式

```python
# 方式一：装饰器实现
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    pass

# 方式二：__new__ 实现
class Database:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 工厂模式

```python
class DriverFactory:
    @staticmethod
    def create_driver(browser):
        if browser == "chrome":
            return webdriver.Chrome()
        elif browser == "firefox":
            return webdriver.Firefox()
        else:
            raise ValueError(f"不支持的浏览器: {browser}")

driver = DriverFactory.create_driver("chrome")
```

> **测试中的应用**：WebDriver 工厂、测试数据工厂、Page Object 工厂

---

## 九、异常处理进阶

### 自定义异常

```python
class BusinessError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(self.message)

# 使用
try:
    raise BusinessError(400, "参数错误")
except BusinessError as e:
    print(f"错误码: {e.code}, 信息: {e.message}")
```

### 异常链

```python
try:
    result = 1 / 0
except ZeroDivisionError as e:
    raise ValueError("计算失败") from e   # 保留原始异常信息
```

---

## 十、常见面试题及参考答案

### Q1：GIL 是什么？对多线程有什么影响？

> GIL 是 CPython 的全局锁，同一时刻只有一个线程执行 Python 字节码。对 IO 密集型任务影响不大（等待 IO 时释放 GIL），但 CPU 密集型任务无法利用多核，需要用多进程。

### Q2：多线程、多进程、协程分别适合什么场景？

> 多线程适合 IO 密集型（文件/网络），多进程适合 CPU 密集型（计算），协程适合大量 IO 并发（如同时请求 1000 个接口）。

### Q3：什么是生成器？和列表有什么区别？

> 生成器用 yield 惰性求值，按需生成数据，节省内存；列表一次性加载所有数据到内存。处理大数据量时用生成器。

### Q4：装饰器的原理是什么？

> 装饰器本质是一个函数，接收一个函数作为参数，返回一个新函数。`@decorator` 等价于 `func = decorator(func)`。常用于日志、计时、权限校验。

### Q5：with 语句的原理？

> with 调用对象的 `__enter__` 进入上下文，执行完后调用 `__exit__` 退出。即使发生异常也能保证资源释放（如关闭文件、断开连接）。

### Q6：什么是单例模式？在测试中有什么应用？

> 确保一个类只有一个实例。测试中常用于：WebDriver 实例、数据库连接池、配置管理器，避免重复创建资源。

### Q7：如何实现线程安全？

> 使用 `threading.Lock()` 加锁保护共享资源。推荐用 `with lock:` 语法自动加锁释放锁，避免死锁。

### Q8：asyncio 的 await 是什么意思？

> await 表示"等待这个异步操作完成"，等待期间会释放控制权给事件循环去执行其他协程，实现非阻塞并发。

---

## 速记口诀

```
GIL 限制多线程的 CPU 并行
IO 密集 → 多线程 / 协程
CPU 密集 → 多进程

线程共享内存要加锁，进程独立内存用 Queue
协程单线程切换，最轻量

yield 暂停返回，return 终止返回
生成器 = 惰性求值省内存

with 自动管理资源：__enter__ 进 __exit__ 出
装饰器 = 函数包函数，@语法糖
单例 = 全局一个实例，__new__ 或装饰器实现
```

---

*可与《02-Python自动化测试常见面试题.md》搭配复习，基础 + 进阶 = Python 面试全覆盖。*
