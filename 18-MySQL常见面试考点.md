# MySQL 常见面试考点

> 适用于测试开发 / 自动化测试 / 后端测试岗位面试准备

---

## 一、基础操作（必会）

### 数据库与表操作

```sql
-- 创建数据库
CREATE DATABASE test_db DEFAULT CHARSET utf8mb4;

-- 使用数据库
USE test_db;

-- 查看所有数据库
SHOW DATABASES;

-- 创建表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INT DEFAULT 0,
    email VARCHAR(100) UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 查看表结构
DESC users;

-- 修改表：添加列
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- 修改表：修改列类型
ALTER TABLE users MODIFY COLUMN phone VARCHAR(30);

-- 删除表
DROP TABLE users;

-- 清空表（保留结构，自增归零）
TRUNCATE TABLE users;
```

---

## 二、增删改查 CRUD（每场面试必考）

### INSERT 插入

```sql
-- 插入单条
INSERT INTO users (name, age, email) VALUES ('张三', 25, 'zhangsan@test.com');

-- 插入多条
INSERT INTO users (name, age, email) VALUES
('李四', 30, 'lisi@test.com'),
('王五', 28, 'wangwu@test.com');
```

### SELECT 查询

```sql
-- 查询所有
SELECT * FROM users;

-- 条件查询
SELECT name, age FROM users WHERE age > 25;

-- 模糊查询
SELECT * FROM users WHERE name LIKE '张%';    -- 以"张"开头
SELECT * FROM users WHERE name LIKE '%三';    -- 以"三"结尾
SELECT * FROM users WHERE name LIKE '%张%';   -- 包含"张"

-- IN 查询
SELECT * FROM users WHERE age IN (25, 28, 30);

-- BETWEEN 范围查询
SELECT * FROM users WHERE age BETWEEN 20 AND 30;

-- NULL 判断
SELECT * FROM users WHERE email IS NULL;
SELECT * FROM users WHERE email IS NOT NULL;

-- 去重
SELECT DISTINCT age FROM users;

-- 排序
SELECT * FROM users ORDER BY age ASC;         -- 升序（默认）
SELECT * FROM users ORDER BY age DESC;        -- 降序

-- 分页（LIMIT）
SELECT * FROM users LIMIT 10;                 -- 前10条
SELECT * FROM users LIMIT 10 OFFSET 20;      -- 跳过20条取10条（第3页）
SELECT * FROM users LIMIT 20, 10;             -- 同上写法
```

### UPDATE 更新

```sql
-- 更新数据（一定要加 WHERE，否则全表更新！）
UPDATE users SET age = 26 WHERE name = '张三';

-- 同时更新多个字段
UPDATE users SET age = 26, email = 'new@test.com' WHERE id = 1;
```

### DELETE 删除

```sql
-- 删除数据（一定要加 WHERE，否则全表删除！）
DELETE FROM users WHERE id = 1;
```

> **面试重点**：UPDATE 和 DELETE 一定要强调 WHERE 条件，否则会造成数据灾难！

---

## 三、聚合函数与分组（高频）

### 常用聚合函数

| 函数 | 作用 | 示例 |
|------|------|------|
| `COUNT(*)` | 统计行数 | `SELECT COUNT(*) FROM users;` |
| `COUNT(列)` | 统计非 NULL 行数 | `SELECT COUNT(email) FROM users;` |
| `SUM(列)` | 求和 | `SELECT SUM(age) FROM users;` |
| `AVG(列)` | 平均值 | `SELECT AVG(age) FROM users;` |
| `MAX(列)` | 最大值 | `SELECT MAX(age) FROM users;` |
| `MIN(列)` | 最小值 | `SELECT MIN(age) FROM users;` |

### GROUP BY 分组

```sql
-- 按年龄分组统计人数
SELECT age, COUNT(*) AS cnt FROM users GROUP BY age;

-- 分组后过滤（HAVING，不能用 WHERE）
SELECT age, COUNT(*) AS cnt FROM users GROUP BY age HAVING cnt > 2;
```

> **面试重点**：`WHERE` 在分组前过滤，`HAVING` 在分组后过滤

### 执行顺序（必考）

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

> **口诀**：从哪里 → 先过滤 → 再分组 → 分组后过滤 → 选列 → 排序 → 分页

---

## 四、多表联查 JOIN（重点必考）

### 准备数据

```sql
-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    dept_id INT
);

-- 部门表
CREATE TABLE departments (
    id INT PRIMARY KEY,
    dept_name VARCHAR(50)
);
```

### JOIN 类型

```sql
-- INNER JOIN（内连接）：只返回两表都匹配的行
SELECT u.name, d.dept_name
FROM users u
INNER JOIN departments d ON u.dept_id = d.id;

-- LEFT JOIN（左连接）：返回左表所有行，右表没匹配的补 NULL
SELECT u.name, d.dept_name
FROM users u
LEFT JOIN departments d ON u.dept_id = d.id;

-- RIGHT JOIN（右连接）：返回右表所有行，左表没匹配的补 NULL
SELECT u.name, d.dept_name
FROM users u
RIGHT JOIN departments d ON u.dept_id = d.id;
```

### 图解记忆

```
INNER JOIN：  A ∩ B        → 只取交集
LEFT JOIN：   A（全部）+ B  → 左表全部，右表匹配不上为 NULL
RIGHT JOIN：  A + B（全部） → 右表全部，左表匹配不上为 NULL
```

### 面试常见写法

```sql
-- 查询每个部门的员工人数（包含 0 人的部门）
SELECT d.dept_name, COUNT(u.id) AS emp_count
FROM departments d
LEFT JOIN users u ON d.id = u.dept_id
GROUP BY d.dept_name;

-- 查询没有分配部门的员工
SELECT u.name
FROM users u
LEFT JOIN departments d ON u.dept_id = d.id
WHERE d.id IS NULL;
```

---

## 五、子查询（常考）

```sql
-- 标量子查询：查询年龄最大的用户
SELECT * FROM users WHERE age = (SELECT MAX(age) FROM users);

-- IN 子查询：查询"技术部"的所有员工
SELECT * FROM users
WHERE dept_id IN (SELECT id FROM departments WHERE dept_name = '技术部');

-- EXISTS 子查询：查询有员工的部门
SELECT * FROM departments d
WHERE EXISTS (SELECT 1 FROM users u WHERE u.dept_id = d.id);
```

> **面试常问**：IN vs EXISTS 的区别？
> - **IN**：先执行子查询，适合子查询结果集**小**的情况
> - **EXISTS**：逐行检查外层，适合子查询结果集**大**的情况

---

## 六、索引（高频考点）

### 什么是索引？

> 索引就像书的目录，加快数据查找速度。没有索引 = 全表扫描（逐页翻书）。

### 索引类型

| 类型 | 说明 | 语法 |
|------|------|------|
| 主键索引 | 唯一 + 非空，自动创建 | `PRIMARY KEY` |
| 唯一索引 | 值唯一，允许 NULL | `UNIQUE INDEX` |
| 普通索引 | 最基本的索引 | `INDEX` |
| 联合索引 | 多列组合索引 | `INDEX(a, b, c)` |
| 全文索引 | 用于文本搜索 | `FULLTEXT INDEX` |

### 索引操作

```sql
-- 创建索引
CREATE INDEX idx_name ON users(name);

-- 创建联合索引
CREATE INDEX idx_name_age ON users(name, age);

-- 查看索引
SHOW INDEX FROM users;

-- 删除索引
DROP INDEX idx_name ON users;
```

### 最左前缀原则（必考）

联合索引 `INDEX(a, b, c)` 的生效规则：

| 查询条件 | 是否走索引 | 说明 |
|----------|-----------|------|
| `WHERE a = 1` | ✅ 是 | 用到 a |
| `WHERE a = 1 AND b = 2` | ✅ 是 | 用到 a, b |
| `WHERE a = 1 AND b = 2 AND c = 3` | ✅ 是 | 全部用到 |
| `WHERE b = 2` | ❌ 否 | 跳过了 a |
| `WHERE b = 2 AND c = 3` | ❌ 否 | 跳过了 a |
| `WHERE a = 1 AND c = 3` | ⚠️ 部分 | 只用到 a |

> **口诀**：联合索引从最左开始匹配，中间不能跳列

### 索引失效场景（常考）

```sql
-- 1. 对索引列使用函数 → 失效
WHERE YEAR(created_at) = 2026     ❌
WHERE created_at >= '2026-01-01'  ✅

-- 2. 对索引列做运算 → 失效
WHERE age + 1 = 26  ❌
WHERE age = 25      ✅

-- 3. 使用 LIKE 以 % 开头 → 失效
WHERE name LIKE '%张'   ❌
WHERE name LIKE '张%'   ✅

-- 4. 隐式类型转换 → 失效
-- phone 是 VARCHAR，传入数字
WHERE phone = 13800000000  ❌（隐式转换）
WHERE phone = '13800000000' ✅

-- 5. OR 条件（如果某个列没索引）→ 可能失效
-- 6. IS NULL / IS NOT NULL → 视情况，可能失效
-- 7. != / NOT IN → 可能失效
```

### EXPLAIN 分析执行计划

```sql
EXPLAIN SELECT * FROM users WHERE name = '张三';
```

| 关键字段 | 含义 |
|---------|------|
| `type` | 访问类型（从好到差：`const > eq_ref > ref > range > index > ALL`） |
| `key` | 实际使用的索引 |
| `rows` | 扫描行数（越少越好） |
| `Extra` | 额外信息（`Using index`=覆盖索引好、`Using filesort`=需优化） |

> **面试常问**：type = ALL 说明什么？→ 全表扫描，没走索引，需要优化

---

## 七、事务 ACID（必考）

### 四大特性

| 特性 | 英文 | 含义 | 记忆 |
|------|------|------|------|
| **原子性** | **A**tomicity | 事务要么全部成功，要么全部回滚 | 要么做完，要么没做 |
| **一致性** | **C**onsistency | 事务前后数据保持一致（如转账总额不变） | 钱的总数不变 |
| **隔离性** | **I**solation | 并发事务互不干扰 | 互不影响 |
| **持久性** | **D**urability | 提交后的数据永久保存 | 写入磁盘 |

> **口诀**：原一隔持（ACID），I 是隔离不是完整

### 事务操作

```sql
-- 开启事务
START TRANSACTION;  -- 或 BEGIN;

-- 执行操作
UPDATE accounts SET balance = balance - 100 WHERE name = 'A';
UPDATE accounts SET balance = balance + 100 WHERE name = 'B';

-- 提交
COMMIT;

-- 回滚（出错时）
ROLLBACK;
```

### 隔离级别（中高级常考）

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|---------|------|-----------|------|
| READ UNCOMMITTED（读未提交） | ✅ 可能 | ✅ 可能 | ✅ 可能 |
| READ COMMITTED（读已提交） | ❌ 解决 | ✅ 可能 | ✅ 可能 |
| **REPEATABLE READ**（可重复读） | ❌ 解决 | ❌ 解决 | ✅ 可能 |
| SERIALIZABLE（串行化） | ❌ 解决 | ❌ 解决 | ❌ 解决 |

> **MySQL 默认隔离级别**：REPEATABLE READ（可重复读）

**三种问题解释**：
- **脏读**：读到别人还没提交的数据（万一回滚了呢）
- **不可重复读**：同一事务内两次读同一数据，结果不同（被别人改了）
- **幻读**：同一事务内两次查询，记录数不同（被别人插了新数据）

---

## 八、锁（中高级）

| 锁类型 | 说明 |
|--------|------|
| 行锁 | 锁定某一行，并发高 |
| 表锁 | 锁定整张表，并发低 |
| 共享锁（S 锁 / 读锁） | 多个事务可同时读 |
| 排他锁（X 锁 / 写锁） | 独占，其他事务不能读写 |

```sql
-- 加共享锁
SELECT * FROM users WHERE id = 1 LOCK IN SHARE MODE;

-- 加排他锁
SELECT * FROM users WHERE id = 1 FOR UPDATE;
```

**死锁**：
- 两个事务互相等待对方释放锁
- MySQL 会自动检测并回滚其中一个
- 预防：按固定顺序访问表、减少事务持有锁的时间

---

## 九、SQL 优化（高频场景题）

### 慢 SQL 排查流程

```
1. 开启慢查询日志（slow_query_log）
2. 找到慢 SQL
3. 用 EXPLAIN 分析执行计划
4. 检查是否走索引（type = ALL？）
5. 优化：加索引 / 改写 SQL / 减少数据量
```

### 常见优化手段

| 优化方式 | 说明 |
|---------|------|
| 加索引 | 对 WHERE、JOIN、ORDER BY 的列建索引 |
| 避免 SELECT * | 只查需要的列，减少 IO |
| 小表驱动大表 | IN 适合子查询小，EXISTS 适合子查询大 |
| 避免索引失效 | 不要在索引列上用函数、运算、LIKE '%xxx' |
| 分页优化 | `LIMIT 100000, 10` → 用 `WHERE id > 上次最大ID LIMIT 10` |
| 避免大事务 | 事务尽量短，减少锁竞争 |
| 读写分离 | 主库写、从库读 |

---

## 十、DELETE vs TRUNCATE vs DROP（必考）

| 对比项 | DELETE | TRUNCATE | DROP |
|--------|--------|----------|------|
| 作用 | 删除数据（可加 WHERE） | 清空全部数据 | 删除整张表 |
| 表结构 | 保留 | 保留 | **不保留** |
| 自增 ID | 不重置 | **重置为 0** | 表没了 |
| 可回滚 | ✅ 可以（在事务中） | ❌ 不可以 | ❌ 不可以 |
| 速度 | 慢（逐行删除） | **快** | 最快 |
| 触发器 | 触发 | 不触发 | 不触发 |

> **口诀**：DELETE 慢可回滚，TRUNCATE 快不可回滚，DROP 连表都没了

---

## 十一、常见面试题及参考答案

### Q1：INNER JOIN、LEFT JOIN、RIGHT JOIN 的区别？

> INNER JOIN 只返回两表匹配的行；LEFT JOIN 返回左表全部 + 右表匹配（不匹配为 NULL）；RIGHT JOIN 反过来。

### Q2：WHERE 和 HAVING 的区别？

> WHERE 在 GROUP BY 之前过滤，不能用聚合函数；HAVING 在 GROUP BY 之后过滤，可以用聚合函数。

### Q3：什么是索引？为什么不是越多越好？

> 索引加快查询速度，但会降低插入/更新速度（要维护索引），还占存储空间。频繁更新的列不适合建索引。

### Q4：什么是最左前缀原则？

> 联合索引 (a,b,c) 查询时必须从最左列 a 开始匹配，中间不能跳列，否则后面的列不走索引。

### Q5：ACID 是什么？MySQL 默认隔离级别？

> 原子性、一致性、隔离性、持久性。MySQL 默认 REPEATABLE READ（可重复读）。

### Q6：如何排查慢 SQL？

> 开启慢查询日志 → 找到慢 SQL → EXPLAIN 分析 → 检查是否全表扫描 → 加索引或改写 SQL。

### Q7：DELETE、TRUNCATE、DROP 的区别？

> DELETE 逐行删可回滚；TRUNCATE 清空快不可回滚，自增归零；DROP 直接删除整张表。

### Q8：SQL 中 NULL 怎么判断？

> 不能用 `= NULL`，必须用 `IS NULL` 或 `IS NOT NULL`。`COUNT(列)` 不统计 NULL，`COUNT(*)` 统计所有行。

### Q9：如何查询每个部门人数最多的前 3 名员工？

```sql
SELECT * FROM (
    SELECT u.*, d.dept_name,
           ROW_NUMBER() OVER (PARTITION BY u.dept_id ORDER BY u.score DESC) AS rn
    FROM users u
    JOIN departments d ON u.dept_id = d.id
) tmp
WHERE rn <= 3;
```

### Q10：索引什么时候会失效？

> 函数操作列、列上做运算、LIKE 以 % 开头、隐式类型转换、OR 条件有非索引列、!= / NOT IN 等情况。

---

## 十二、手写 SQL 练习题

### 题目 1：查询分数大于 80 的学生姓名和分数，按分数降序排列

```sql
SELECT name, score FROM students WHERE score > 80 ORDER BY score DESC;
```

### 题目 2：查询每个班级的平均分，只显示平均分大于 70 的班级

```sql
SELECT class_id, AVG(score) AS avg_score
FROM students
GROUP BY class_id
HAVING avg_score > 70;
```

### 题目 3：查询选修了所有课程的学生

```sql
SELECT student_id
FROM scores
GROUP BY student_id
HAVING COUNT(DISTINCT course_id) = (SELECT COUNT(*) FROM courses);
```

### 题目 4：查询没有下过订单的用户

```sql
SELECT u.name
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

### 题目 5：查询第 2 高的工资

```sql
SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1, 1;

-- 或者用子查询
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

---

## 速记口诀

```
增 INSERT，删 DELETE，改 UPDATE，查 SELECT
WHERE 先过滤，GROUP BY 再分组，HAVING 分组后过滤
ORDER BY 排序，LIMIT 分页

JOIN 三兄弟：INNER 取交集，LEFT 左全右匹配，RIGHT 右全左匹配

索引最左匹配，函数运算会失效
LIKE 百分号开头不走索引
EXPLAIN 看 type，ALL 全扫描要优化

ACID：原一隔持
默认隔离级别：可重复读

DELETE 慢可回滚，TRUNCATE 快归零，DROP 连表删
COUNT(*) 算所有，COUNT(列) 跳 NULL
NULL 用 IS 判断，不能用等号
```

---

*可与《04-测试开发常见面试题.md》《07-测试中间件常见面试题.md》搭配复习，SQL 是测试岗每场面试的必考题。*
