# JMeter 自动化测试常见面试题总结

> 适用于性能测试 / 自动化测试岗位面试准备

---

## 一、JMeter 基础

### 1. JMeter 是什么？主要用来做什么？

- **JMeter** 是 Apache 开源的基于 Java 的性能测试工具。
- **主要用途**：接口测试、性能/压力测试、负载测试、并发测试。
- 支持 HTTP、HTTPS、FTP、JDBC、JMS、SOAP 等多种协议，可通过插件扩展。

**面试点**：强调「性能测试」「多协议」「开源可扩展」。

---

### 2. JMeter 与 Postman、LR 的区别？

| 对比项     | JMeter              | Postman           | LoadRunner        |
|------------|---------------------|-------------------|-------------------|
| 定位       | 性能 + 接口         | 接口调试/自动化   | 企业级性能测试    |
| 并发/压测  | 支持，内置          | 较弱/需 Newman    | 强                |
| 开源       | 是                  | 部分              | 否，商业          |
| 脚本       | GUI/XML             | Collection/JS     | 专有脚本          |
| 报告       | 丰富（图表、HTML）  | 一般              | 非常丰富          |

**面试点**：JMeter 适合做接口自动化 + 性能测试一体化，成本低。

---

### 3. JMeter 的测试计划结构（主要元件类型）？

- **线程组**：模拟用户/并发，是执行的基本单位。
- **取样器（Sampler）**：发请求，如 HTTP Request、JDBC Request。
- **逻辑控制器**：控制执行顺序，如 If、Loop、Once Only。
- **监听器**：收集结果，如 View Results Tree、Summary Report。
- **断言**：校验响应，如 Response Assertion、JSON Assertion。
- **定时器**：控制节奏，如 Constant Throughput、Think Time。
- **配置元件**：全局/局部配置，如 CSV、User Defined Variables。
- **前置/后置处理器**：在取样器前后执行，如 JSR223、正则提取。

**面试点**：能说出「线程组 → 取样器 → 断言 → 监听器」这条主链路即可。

---

## 二、元件作用域与执行顺序

### 4. JMeter 元件的作用域规则？

- 元件的**作用域**由其在树中的**层级位置**决定。
- **父节点**下的元件会作用于该父节点及其**所有子节点**。
- 同一层级多个相同类型元件，按**从上到下**顺序生效（如多个断言都生效）。

**面试点**：配置元件、断言、定时器等放在线程组下，则对该线程组内所有请求生效。

---

### 5. JMeter 请求执行顺序？

1. **配置元件**（如 CSV Data Set、User Defined Variables）
2. **前置处理器**（Pre Processors）
3. **定时器**（Timers）
4. **取样器**（Samplers）
5. **后置处理器**（Post Processors，仅在成功响应后）
6. **断言**（Assertions）
7. **监听器**（Listeners）

**面试点**：参数化在配置元件，提取在后置处理器，校验在断言。

---

## 三、参数化与关联

### 6. JMeter 有哪些参数化方式？

| 方式                   | 适用场景                     |
|------------------------|------------------------------|
| User Defined Variables | 全局常量、环境变量           |
| CSV Data Set Config    | 大量测试数据、多用户/多数据  |
| 函数 __Random、__time  | 随机数、时间戳等简单动态值   |
| 用户参数（User Parameters） | 每线程不同参数         |

**面试点**：实际项目中最常用 **CSV Data Set Config** 做数据驱动。

---

### 7. CSV Data Set Config 常用配置项？

- **Filename**：CSV 文件路径（相对或绝对）。
- **Variable Names**：变量名，逗号分隔，与列一一对应。
- **Delimiter**：分隔符，默认逗号。
- **Recycle on EOF?**：文件读完是否从头再读（True/False）。
- **Stop thread on EOF?**：读完是否停止线程（多与 Recycle 配合）。
- **Sharing mode**：All threads / Current thread group / Current thread 等，控制多线程如何共享文件。

**面试点**：能说出「变量名对应列」「Recycle/Stop 控制数据循环」即可。

---

### 8. 什么是关联？JMeter 如何做关联？

- **关联**：从上一个请求的响应中取出数据，作为后续请求的参数（如 token、sessionId）。
- **做法**：
  - **后置处理器**提取：正则提取器（Regular Expression Extractor）、JSON 提取器（JSON Extractor）、边界提取器等。
  - 提取到的值存到 **JMeter 变量**（如 `token`），在下一个请求中用 `${token}` 引用。

**面试点**：流程是「发请求 → 后置处理器提取 → 存变量 → 下个请求引用」。

---

### 9. 正则提取器常用配置？

- **Apply to**：作用范围（主样本、子样本等）。
- **Field to check**：响应体、响应头、URL 等。
- **Name of created variable**：变量名。
- **Regular Expression**：正则，用括号表示捕获组。
- **Template**：`$1$` 表示取第 1 个捕获组，`$2$` 表示第 2 个。
- **Match No.**：第几个匹配（0 随机，1 第一个，-1 全部等）。
- **Default Value**：匹配失败时的默认值。

**面试点**：至少能写简单正则，如 `"token":"([^"]+)"`，Template `$1$`。

---

## 四、断言与监听器

### 10. 常用断言类型及使用场景？

| 断言类型           | 适用场景                     |
|--------------------|------------------------------|
| Response Assertion | 状态码、响应文本、响应时间   |
| JSON Assertion     | JSON 路径 + 期望值           |
| Duration Assertion | 响应时间是否在指定时间内     |
| Size Assertion     | 响应大小                     |

**面试点**：接口自动化常用 **Response Assertion** 和 **JSON Assertion**。

---

### 11. 做性能测试时为什么建议少用或禁用 View Results Tree？

- View Results Tree 会记录**每个请求的详细请求/响应**，占用大量内存和 I/O。
- 线程数多、运行时间长时，容易导致 **JMeter 本机 OOM 或卡顿**，影响压测结果真实性。
- 建议：调试时用，压测时用 **Summary Report、Aggregate Report** 等汇总型监听器，或把结果写到文件（如 CSV），事后分析。

**面试点**：区分「调试用」和「压测用」监听器，避免监听器成为瓶颈。

---

### 12. Summary Report 和 Aggregate Report 区别？

- **Summary Report**：各 sampler 的汇总（TPS、平均响应时间、错误率等），相对简单。
- **Aggregate Report**：更细，可看**百分位**（如 90%、95%、99% 响应时间）、中位数、吞吐量等，做性能分析更常用。

**面试点**：性能分析时更关注 **百分位响应时间** 和 **TPS/吞吐量**。

---

## 五、性能测试概念（在 JMeter 中的体现）

### 13. 什么是并发、TPS、QPS？在 JMeter 中如何理解？

- **并发**：同一时刻同时在执行的用户/线程数；JMeter 中由**线程数**和** ramp-up** 共同决定。
- **TPS**：每秒事务数（Transaction Per Second），JMeter 中可理解为每秒完成的请求数（与事务控制器有关）。
- **QPS**：每秒查询/请求数，和 TPS 在单请求场景下常混用。

**面试点**：JMeter 里「线程数」不等于「每秒请求数」，还受 ramp-up、思考时间、响应时间影响。

---

### 14. Ramp-up 时间是什么？如何设置？

- **Ramp-up**：所有线程从启动到全部启动完成的**时间**（秒）。
- 若线程数 100，Ramp-up 50s，则大约每 0.5 秒启动 1 个线程，避免瞬时全部启动对被测系统造成冲击。
- 设置建议：根据业务和目的，一般可设为总线程数的 1/10～1 倍，或根据目标 QPS 反推。

**面试点**：Ramp-up 太小会形成瞬时尖峰，太大则达到目标并发的时间过长。

---

### 15. 什么是思考时间（Think Time）？JMeter 如何模拟？

- **思考时间**：用户操作之间的间隔（如看完页面再点下一步）。
- JMeter 用 **定时器（Timer）** 模拟：如 **Constant Timer** 固定延迟、**Random Timer** 随机延迟、**Uniform Random Timer** 等。
- 加思考时间会**降低**相同线程数下的 TPS，但更接近真实用户行为。

**面试点**：性能测试有时会做「带思考时间」和「不带思考时间」的对比。

---

## 六、逻辑控制器与脚本结构

### 16. 常用逻辑控制器及作用？

| 控制器           | 作用                           |
|------------------|--------------------------------|
| Loop Controller  | 循环执行子元件 N 次或永远      |
| If Controller    | 条件为真时执行子元件          |
| Once Only Controller | 每个线程只执行一次        |
| Transaction Controller | 把多个请求包成一个事务，统计总时间 |
| Throughput Controller | 控制子元件的执行比例（百分比或每秒次数） |

**面试点**：事务控制器用于把多个请求合并为一个「业务事务」做 TPS 统计。

---

### 17. 如何用 JMeter 模拟一个用户登录后多次操作？

- 线程组下：先放**登录**请求。
- 登录请求下加**后置处理器**（如 JSON/正则提取器）提取 token。
- 再放 **Loop Controller**，循环里放后续业务请求，请求中用 `${token}`。
- 若需「每个用户只登录一次」，可在登录请求外包一层 **Once Only Controller**（或把登录放循环外）。

**面试点**：关联 + 循环 + 只执行一次登录，是常见业务场景。

---

## 七、分布式与监控

### 18. JMeter 分布式测试原理？如何配置？

- **原理**：一台**控制机（Master）** 把测试计划下发到多台**压力机（Slave）**，压力机执行并回传结果到控制机汇总。
- **配置**：
  - 各压力机启动：`jmeter-server`（或 `jmeter -n -t xx.jmx` 的 slave 模式）。
  - 控制机 `jmeter.properties` 中配置 `remote_hosts=ip1:port,ip2:port`。
  - 用 GUI 或命令行 `jmeter -n -t xx.jmx -R ip1,ip2 -l result.jtl` 远程启动。

**面试点**：单机线程数/带宽有限时，用分布式增加总压力。

---

### 19. 如何分析 JMeter 结果？常用报告？

- **命令行生成 HTML 报告**：  
  `jmeter -n -t plan.jmx -l result.jtl -e -o report_dir`
- 报告内容：Dashboard（概览）、APDEX、响应时间分布、错误率、TPS 等。
- 也可用 **JTL/CSV** 结果文件在 Excel 或分析工具中做二次分析。

**面试点**：`-e -o` 生成 HTML 报告是当前常用方式。

---

## 八、实践与问题排查

### 20. JMeter 脚本如何在非 GUI 下运行？为什么压测要用非 GUI？

- **命令**：`jmeter -n -t 脚本.jmx -l 结果.jtl -j 日志.log`
- **原因**：GUI 模式会消耗大量资源（界面、监听器实时刷新），影响压测数据准确性；非 GUI（nogui）资源占用小，适合正式压测。

**面试点**：压测一律用 **-n**（nogui）模式。

---

### 21. 遇到 "Out of Memory" 怎么处理？

- 调大 JVM 堆内存：修改 `jmeter` 或 `jmeter.bat` 中的 `HEAP`（如 `-Xms1g -Xmx4g`）。
- 减少监听器：关闭或禁用 View Results Tree，少用「保存完整响应」的监听器。
- 结果写入文件时用 CSV，且不要勾选「保存响应数据」等大字段。
- 分布式：把压力分散到多台机器，单机线程数不要过大。

**面试点**：先减监听器与结果数据量，再考虑加内存和分布式。

---

### 22. 如何做接口依赖（如先登录再调业务接口）？

- 线程组内顺序放：**登录请求** → **后置处理器提取 token/session** → **业务请求**（引用 `${变量名}`）。
- 若业务有多步，用 **Transaction Controller** 或 **Loop Controller** 组织步骤。
- 需要不同用户不同数据时，用 **CSV Data Set Config** 准备多组账号，每线程取一行。

**面试点**：关联（提取 + 引用）+ 数据驱动（CSV）是接口依赖的常规做法。

---

### 23. 你用过哪些 JMeter 插件？为什么用？

- **Plugins Manager**：管理插件安装。
- **Custom Thread Groups**：如 **Stepping Thread Group**、**Ultimate Thread Group**，做阶梯增压、波浪型负载。
- **3 Basic Graphs**、**Response Times Over Time** 等：更丰富的实时图表。
- **Dummy Sampler**：模拟请求，不真实发请求，用于调试脚本结构。

**面试点**：根据项目说 1～2 个即可，如阶梯加压、更好看的报告。

---

### 24. 如何保证 JMeter 脚本可维护性？

- **使用变量**：主机、端口、环境等用 User Defined Variables，一处修改全局生效。
- **模块化**：把重复请求（如登录、公共头）做成**模块控制器**或**Include Controller** 引用。
- **命名规范**：线程组、请求、断言命名清晰（如 01_登录、02_查询列表）。
- **注释**：用 **Test Fragment** 或注释说明业务场景和参数含义。
- **版本管理**：jmx 和 CSV 数据文件放 Git，避免直接改生产用脚本。

**面试点**：变量化、模块化、命名、版本管理。

---

## 九、小结速记

| 主题       | 关键词 |
|------------|--------|
| 参数化     | User Defined Variables、CSV Data Set Config、函数 |
| 关联       | 后置处理器（正则/JSON 提取）→ 变量 → `${变量}` |
| 执行顺序   | 配置 → 前置 → 定时器 → 取样器 → 后置 → 断言 → 监听器 |
| 性能注意   | 压测用 nogui、少用 View Results Tree、合理 Ramp-up |
| 分布式     | Master-Slave、remote_hosts、jmeter-server |
| 报告       | `-n -t -l -e -o` 生成 HTML 报告 |

---

*文档风格与《Python自动化测试常见面试题》保持一致，便于一起复习。*
