# Linux 命令常见面试考点

> 适用于测试开发 / 自动化测试 / 后端测试岗位面试准备

---

## 一、文件与目录操作（最基础，必会）

| 命令 | 作用 | 示例 |
|------|------|------|
| `ls` | 列出文件 | `ls -la`（详细+隐藏） |
| `cd` | 切换目录 | `cd /home`、`cd ..`、`cd ~` |
| `pwd` | 显示当前路径 | |
| `mkdir` | 创建目录 | `mkdir -p a/b/c`（递归创建） |
| `rm` | 删除 | `rm -rf 目录`（强制递归删除，**慎用**） |
| `cp` | 拷贝 | `cp -r 源 目标`（拷贝目录加 -r） |
| `mv` | 移动/重命名 | `mv old.txt new.txt` |
| `touch` | 创建空文件 | `touch test.txt` |
| `find` | 搜索文件 | `find /home -name "*.log"` |
| `find` | 按大小搜索 | `find . -type f -size +10k`（大于 10K 的文件） |

---

## 二、文件查看与编辑（高频）

| 命令 | 作用 | 适用场景 |
|------|------|---------|
| `cat` | 查看全部内容 | 小文件 |
| `cat -n file` | 带行号查看 | |
| `head -n 20 file` | 看前 20 行 | 快速预览 |
| `tail -n 20 file` | 看后 20 行 | 查看最新日志 |
| `tail -f file` | **实时跟踪**文件更新 | **查看实时日志（最常考）** |
| `less / more` | 分页查看 | 大文件 |
| `vi / vim` | 编辑文件 | 修改配置 |

### vim 基本操作（面试可能问）

- `i` → 进入编辑模式
- `Esc` → 退出编辑模式
- `:wq` → 保存退出
- `:q!` → 不保存退出
- `/关键词` → 搜索
- `dd` → 删除当前行
- `yy` → 复制当前行，`p` 粘贴

---

## 三、日志分析（测试岗必考）

### grep 过滤

| 命令 | 作用 |
|------|------|
| `grep "Error" app.log` | 过滤包含 Error 的行 |
| `grep -i "error" app.log` | 忽略大小写过滤 |
| `grep -c "Error" app.log` | 统计 Error 出现次数 |
| `grep -n "Error" app.log` | 显示行号 |
| `grep -A 10 "Exception" app.log` | 匹配行及**后** 10 行（After） |
| `grep -B 5 "Exception" app.log` | 匹配行及**前** 5 行（Before） |
| `grep -C 5 "Exception" app.log` | 匹配行及**前后** 5 行（Context） |
| `grep -v "DEBUG" app.log` | **排除**包含 DEBUG 的行 |
| `grep -r "Error" /var/log/` | **递归**搜索目录下所有文件 |

### 组合用法（面试常考）

```bash
# 实时跟踪日志并过滤关键词
tail -f app.log | grep "Error"

# 查看某用户昨天的操作日志
grep "zhangsan" a.log | grep "2026-02-09"

# 统计日志中有多少个 Exception
grep "Exception" a.log | wc -l

# 查看 Error 日志及其后 10 行上下文
grep -A 10 "Exception" a.log
```

---

## 四、进程管理（高频）

| 命令 | 作用 |
|------|------|
| `ps -ef` | 查看所有进程 |
| `ps -ef \| grep tomcat` | 过滤特定进程 |
| `ps -ef \| grep mysql` | 查看 mysql 进程是否启动 |
| `kill PID` | 正常终止进程 |
| `kill -9 PID` | **强制**杀死进程 |
| `top` | 实时查看系统资源（CPU、内存） |
| `free -h` | 查看内存使用情况 |
| `df -h` | 查看磁盘使用情况 |

---

## 五、网络相关（接口测试常考）

| 命令 | 作用 |
|------|------|
| `ping IP` | 测试网络连通性 |
| `curl URL` | 发送 GET 请求 |
| `curl -X POST -d '参数' URL` | 发送 POST 请求 |
| `curl -I URL` | 只看响应头 |
| `wget URL` | 下载文件 |
| `netstat -anp \| grep 3306` | 查看端口占用 |
| `lsof -i :3306` | 查看端口占用（另一种方式） |
| `telnet IP 端口` | 测试端口是否可连通 |
| `ifconfig` / `ip addr` | 查看本机 IP |

---

## 六、权限管理

| 命令 | 作用 |
|------|------|
| `chmod 755 file` | 修改文件权限 |
| `chmod 666 file` | 所有人可读可写 |
| `chmod +x file` | 添加可执行权限 |
| `chown user:group file` | 修改文件归属 |

### 权限数字含义

```
r(读)=4  w(写)=2  x(执行)=1

755 = rwxr-xr-x → 属主全权限，其他人读+执行
666 = rw-rw-rw- → 所有人读写
644 = rw-r--r-- → 属主读写，其他人只读
777 = rwxrwxrwx → 所有人全权限（一般不推荐）
```

**面试常考**：`chmod 666 /home/demo.txt` → 给所有人可读可写权限

---

## 七、管道与重定向

```bash
# 管道 |：前一个命令的输出 → 后一个命令的输入
ps -ef | grep tomcat | grep -v grep

# 重定向
echo "hello" > file.txt      # 覆盖写入（>）
echo "world" >> file.txt     # 追加写入（>>）
command > log.txt 2>&1        # 标准输出+错误都写入文件

# wc：统计
wc -l file.txt    # 统计行数
wc -w file.txt    # 统计单词数
```

---

## 八、压缩与解压

```bash
# tar（最常用）
tar -czvf archive.tar.gz 目录/    # 压缩
tar -xzvf archive.tar.gz          # 解压

# 参数含义：c=创建 x=解压 z=gzip v=显示过程 f=指定文件名
# 口诀：压缩 czvf，解压 xzvf

# zip
zip -r archive.zip 目录/
unzip archive.zip
```

---

## 九、服务与系统管理

```bash
# systemctl（CentOS 7+ / Ubuntu 16+）
systemctl start nginx       # 启动服务
systemctl stop nginx        # 停止服务
systemctl restart nginx     # 重启服务
systemctl status nginx      # 查看状态
systemctl enable nginx      # 设置开机自启

# 防火墙
systemctl stop firewalld    # 关闭防火墙
systemctl status firewalld  # 查看防火墙状态
```

---

## 十、sed 和 awk（进阶，加分项）

### sed：流编辑器

```bash
sed -i 's/old/new/g' file.txt            # 全局替换 old 为 new
sed -i '23s/test/TEST/g' test.txt        # 只替换第 23 行
sed -n '25p' file.txt                    # 只打印第 25 行
```

### awk：按列处理文本

```bash
awk '{print $1, $3}' file.txt            # 打印第 1 和第 3 列
awk -F ":" '{print $1}' /etc/passwd      # 以:为分隔符，打印第 1 列
awk 'NR==25{print $3}' file.txt          # 打印第 25 行第 3 列
```

### 综合题：查看 /web.log 第 25 行第 3 列

```bash
# 方法一：sed + cut
sed -n '25p' /web.log | cut -d " " -f3

# 方法二：awk
awk 'NR==25{print $3}' /web.log

# 方法三：head + tail + cut
head -n 25 /web.log | tail -n 1 | cut -d " " -f3
```

---

## 十一、常见面试题及参考答案

### Q1：如何查看某个端口是否被占用？

> `netstat -anp | grep 3306` 或 `lsof -i :3306`

### Q2：如何在日志中查找 Error 信息及其后 10 行？

> `grep -A 10 "Error" app.log`

### Q3：如何实时查看日志？

> `tail -f app.log`，配合过滤：`tail -f app.log | grep "Error"`

### Q4：如何查看第 25 行第 3 列的内容？

> `awk 'NR==25{print $3}' file.txt`

### Q5：如何查找 /home 目录下的 mysql.log 文件？

> `find /home -name "mysql.log"`

### Q6：如何统计 a.log 中有多少个 Exception？

> `grep "Exception" a.log | wc -l` 或 `grep -c "Exception" a.log`

### Q7：如何查找当前目录下大于 10K 的文件？

> `find . -type f -size +10k`

### Q8：如何修改 test.txt 的第 23 行 test 为 TEST？

> `sed -i '23s/test/TEST/g' test.txt`

### Q9：关闭防火墙的命令？

> `systemctl stop firewalld`

### Q10：如何杀死一个进程？

> `ps -ef | grep 进程名` 查 PID → `kill -9 PID` 强制终止

---

## 速记口诀

```
ls 看目录，cd 切路径，pwd 显当前
cat 看全部，tail -f 追实时
grep 过滤行，-A 后 -B 前 -C 前后
wc -l 数行数，-c 统计匹配数
ps 查进程，kill -9 强制杀
top 看资源，free 看内存，df 看磁盘
netstat 查端口，ping 测连通，curl 发请求
chmod 改权限，4读 2写 1执行
管道竖线连，> 覆盖 >> 追加
tar czvf 压，xzvf 解
sed 改文本，awk 取列值
find 搜文件，-name 按名 -size 按大小
```

---

*可与《04-测试开发常见面试题.md》《15-ADB命令常见面试考点.md》搭配复习，Linux 是测试岗的必考项。*
