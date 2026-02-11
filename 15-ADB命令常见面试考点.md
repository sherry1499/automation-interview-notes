# ADB 命令常见面试考点

> 适用于 APP 测试 / 移动端自动化测试岗位面试准备

---

## 一、基础连接与设备

| 命令 | 作用 |
|------|------|
| `adb devices` | 列出已连接的设备 |
| `adb connect <IP:端口>` | 通过 WiFi 连接设备（常见端口 5555） |
| `adb disconnect` | 断开连接 |
| `adb kill-server` | 结束 adb 服务 |
| `adb start-server` | 启动 adb 服务 |

---

## 二、安装与卸载

| 命令 | 作用 |
|------|------|
| `adb install xxx.apk` | 安装 APK |
| `adb install -r xxx.apk` | 覆盖安装（保留数据），常用于升级测试 |
| `adb uninstall <包名>` | 卸载应用 |
| `adb shell pm list package` | 列出所有包名 |
| `adb shell pm list package -f` | 列出包名及路径 |
| `adb shell pm list package -3` | 只列出第三方应用 |

---

## 三、日志查看（高频考点）

| 命令 | 作用 |
|------|------|
| `adb logcat` | 实时查看日志 |
| `adb logcat -c` | 清空日志缓存 |
| `adb logcat -d` | 输出当前日志后退出 |
| `adb logcat *:E` | 只看 Error 级别日志 |
| `adb logcat \| grep "关键词"` | 过滤包含关键词的日志 |
| `adb logcat -v time` | 带时间戳输出 |

### 面试常考：通过包名查进程号，再过滤日志

```bash
adb shell pm list package | findstr douyin    # 1. 查包名
adb shell ps | findstr <包名>                 # 2. 查进程 PID
adb logcat | findstr <PID>                    # 3. 过滤该进程日志
```

---

## 四、文件操作

| 命令 | 作用 |
|------|------|
| `adb push 本地路径 设备路径` | 推文件到设备 |
| `adb pull 设备路径 本地路径` | 从设备拉取文件 |
| `adb shell ls /sdcard/` | 列出设备目录 |

---

## 五、Shell 与系统信息

| 命令 | 作用 |
|------|------|
| `adb shell` | 进入设备 shell |
| `adb shell getprop ro.build.version.release` | 查看 Android 系统版本 |
| `adb shell getprop ro.product.model` | 查看设备型号 |
| `adb shell wm size` | 查看屏幕分辨率 |
| `adb shell wm density` | 查看屏幕密度 |
| `adb shell cat /proc/meminfo` | 查看内存信息 |

---

## 六、模拟操作

| 命令 | 作用 |
|------|------|
| `adb shell screencap /sdcard/abc.png` | 截图保存到设备 |
| `adb shell screenrecord /sdcard/demo.mp4` | 录屏 |
| `adb shell input tap x y` | 模拟点击坐标 |
| `adb shell input swipe x1 y1 x2 y2` | 模拟滑动 |
| `adb shell input swipe x1 y1 x2 y2 duration` | 模拟滑动（指定时长，毫秒） |
| `adb shell input text "hello"` | 模拟输入文字 |
| `adb shell input keyevent 3` | 模拟按 Home 键 |
| `adb shell input keyevent 4` | 模拟按 Back 键 |
| `adb shell input keyevent 26` | 模拟按电源键 |

---

## 七、Activity 与应用管理

| 命令 | 作用 |
|------|------|
| `adb shell dumpsys activity \| findstr "mFocusedActivity"` | 查看当前前台 Activity |
| `adb shell am start -n 包名/Activity名` | 启动指定 Activity |
| `adb shell am force-stop 包名` | 强制停止应用 |
| `adb shell am monitor` | 监控当前活动的包名 |

---

## 八、aapt 查看包信息（常和 ADB 一起考）

```bash
aapt dump badging xxx.apk
```

可获取：
- `package: name='xxx'` → **包名**
- `launchable-activity: name='xxx'` → **启动 Activity**
- `versionCode` / `versionName` → 版本信息

---

## 九、性能相关

| 命令 | 作用 |
|------|------|
| `adb shell top` | 查看 CPU 使用情况 |
| `adb shell dumpsys meminfo <包名>` | 查看指定应用内存占用 |
| `adb shell dumpsys battery` | 查看电池信息 |
| `adb shell dumpsys cpuinfo` | 查看 CPU 信息 |

---

## 十、常见面试题及参考答案

### Q1：如何查看 APP 的错误日志？

> 1. `adb shell pm list package | findstr 应用名` 查包名
> 2. `adb shell ps | findstr 包名` 查进程 PID
> 3. `adb logcat | findstr PID` 过滤该进程日志，查看错误信息

### Q2：如何判断 Bug 在 APP 端还是服务端？

> 1. 抓包分析：用 Fiddler/Charles 看请求是否发出、参数是否正确、响应数据是否正常
> 2. 日志分析：用 adb logcat 看客户端是否有异常日志或崩溃

### Q3：adb install -r 里的 -r 是什么意思？

> 覆盖安装（reinstall），保留原有数据，常用于版本升级测试

### Q4：如何获取 APP 的包名和启动 Activity？

> 方法一：`adb shell dumpsys activity | findstr "mFocusedActivity"`（运行时获取）
> 方法二：`aapt dump badging xxx.apk`（从 APK 文件获取）
> 方法三：`adb shell am monitor`（实时监控）

### Q5：如何模拟弱网环境？

> ADB 本身不直接支持弱网模拟，通常配合以下工具：
> - Fiddler / Charles 设置网络延迟
> - Chrome DevTools 调限速
> - 手机设置切换 2G/3G/4G/飞行模式

---

## 速记口诀

```
devices 查设备，install 装应用
logcat 看日志，grep 过滤关键词
push 推 pull 拉，shell 进终端
screencap 截图，input 模拟操作
am start 启 Activity，dumpsys 查当前
包名查进程，PID 过滤日志
-r 覆盖装，-3 查第三方
```

---

*可与《02-Python自动化测试常见面试题.md》《04-测试开发常见面试题.md》搭配复习，ADB 是 APP 测试的常考项。*
