# Docker 常见面试题总结

> 适用于测试开发 / 运维 / 后端岗位面试准备

---

## 一、Docker 基础

### 1. Docker 是什么？解决什么问题？

- **Docker** 是一个开源的**容器化**平台，基于 Linux 内核的 Cgroups、Namespace 等技术，将应用及其依赖打包成**容器**，实现「一次构建，到处运行」。
- **解决的问题**：
  - **环境一致**：开发、测试、生产环境一致，减少「在我机器上能跑」问题。
  - **隔离**：进程、网络、文件系统隔离，多应用同机互不干扰。
  - **轻量**：相比虚拟机，共享宿主机内核，启动快、占用小。
  - **交付简单**：镜像即交付物，便于 CI/CD 和版本管理。

**面试点**：容器化、环境一致性、轻量、隔离，是 DevOps/测试环境常用基础设施。

---

### 2. Docker 与虚拟机的区别？

| 对比项       | Docker 容器              | 虚拟机（VM）                |
|--------------|---------------------------|-----------------------------|
| 隔离级别     | 进程级（Namespace 等）   | 硬件级（Hypervisor）        |
| 内核         | 共享宿主机内核            | 每台 VM 独立 OS 与内核      |
| 启动速度     | 秒级                      | 分钟级                      |
| 资源占用     | 小                        | 大（完整 OS）               |
| 镜像大小     | 通常 MB 级                | 通常 GB 级                  |
| 适用场景     | 应用隔离、微服务、CI     | 强隔离、多 OS、合规场景     |

**面试点**：容器「共享内核、轻量、快」，虚拟机「完整隔离、重」。

---

### 3. Docker 核心概念：镜像、容器、仓库？

- **镜像（Image）**：只读模板，包含应用与依赖，由多层（Layer）组成，通过 Dockerfile 构建。
- **容器（Container）**：镜像的**运行实例**，可创建、启动、停止、删除；容器层在镜像层之上可写，关闭后默认不持久化（除非用卷）。
- **仓库（Registry）**：存放镜像的服务；**Docker Hub** 是公共仓库；企业常用私有仓库（Harbor、自建 Registry）。

**面试点**：镜像 = 模板，容器 = 实例；镜像只读，容器可写层临时。

---

### 4. 镜像和容器的关系？容器删除后数据会丢吗？

- **关系**：一个镜像可启动多个容器；容器 = 镜像 + 可写层（及网络、挂载等运行时配置）。
- **数据**：默认情况下，容器内产生的数据只存在「可写层」，**删除容器后数据丢失**。要持久化需用 **数据卷（Volume）** 或 **绑定挂载（Bind Mount）** 把目录挂到宿主机或命名卷。

**面试点**：无状态用默认即可；有状态或需保留数据必须用 Volume/挂载。

---

## 二、镜像与 Dockerfile

### 5. Docker 镜像分层（Layer）是什么？好处？

- **分层**：镜像由多层只读层叠加而成，每层对应 Dockerfile 的一条指令（如 RUN、COPY）；不同镜像可**共享相同层**，节省存储与拉取时间。
- **好处**：复用层、加快构建与拉取、减少重复存储。

**面试点**：能说出「分层、只读、共享」即可；写 Dockerfile 时把变化少的放前面利于利用缓存。

---

### 6. Dockerfile 常用指令及作用？

| 指令       | 作用                         |
|------------|------------------------------|
| FROM       | 基础镜像                     |
| RUN        | 在镜像内执行命令（每行一层） |
| COPY/ADD   | 复制文件到镜像（ADD 可解压） |
| WORKDIR    | 设置工作目录                 |
| ENV        | 环境变量                     |
| EXPOSE     | 声明暴露端口（仅声明）       |
| CMD/ENTRYPOINT | 容器启动时执行的命令    |
| USER       | 以指定用户运行               |

**面试点**：FROM 必选；RUN/COPY 顺序影响缓存；CMD 可被 docker run 参数覆盖。

---

### 7. CMD 和 ENTRYPOINT 的区别？

- **CMD**：容器启动时默认执行的命令；可被 `docker run` 后面的命令**完全覆盖**；可提供默认参数。
- **ENTRYPOINT**：一般作为「固定入口」，不会被 `docker run` 后面的内容覆盖，而是把 `docker run` 后的内容当作**参数**传给 ENTRYPOINT。
- **组合**：`ENTRYPOINT ["exec"]` + `CMD ["default-arg"]` 时，run 后写的参数会替换 CMD，一起传给 ENTRYPOINT。

**面试点**：要固定可执行程序用 ENTRYPOINT；要默认参数且可覆盖用 CMD。

---

### 8. 如何减小镜像体积？多阶段构建是什么？

- **手段**：选用小基础镜像（Alpine）；合并 RUN、少层；清理缓存（如 `apt clean`）；用 .dockerignore 排除无关文件；**多阶段构建**。
- **多阶段构建**：一个 Dockerfile 里多个 FROM，前一阶段只负责编译/构建，后一阶段只拷贝产物，最终镜像不包含编译工具和中间文件，体积小。

```dockerfile
# 示例：多阶段构建
FROM golang:1.20 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp .

FROM alpine:latest
COPY --from=builder /app/myapp /myapp
CMD ["/myapp"]
```

**面试点**：多阶段 = 构建阶段 + 运行阶段，最终镜像只含运行所需。

---

## 三、容器操作与常用命令

### 9. 常用 Docker 命令有哪些？

| 类型     | 命令示例 |
|----------|----------|
| 镜像     | `docker build -t name:tag .`、`docker pull`、`docker images`、`docker rmi` |
| 容器     | `docker run -d -p 宿主机:容器 --name xx image`、`docker ps -a`、`docker start/stop/rm`、`docker logs -f`、`docker exec -it xx sh` |
| 清理     | `docker system prune -a`（慎用）、`docker container prune` |

**面试点**：`run -d` 后台、`-p` 端口映射、`--name` 命名、`exec` 进容器排查。

---

### 10. docker run 常用参数？

- **-d**：后台运行。
- **-p 宿主机端口:容器端口**：端口映射。
- **--name**：容器名称。
- **-e**：环境变量。
- **-v 宿主机路径:容器路径** 或 **-v 卷名:容器路径**：挂载卷。
- **--restart=always**：退出后自动重启（如 always、on-failure）。
- **-it**：交互 + 伪终端，常用于调试（如 /bin/sh）。

**面试点**：-d -p -v -e --name --restart 是日常最常用。

---

### 11. 如何进入正在运行的容器？和 docker attach 区别？

- **docker exec -it 容器名/id /bin/sh**（或 bash）：在容器内**新开进程**执行命令，退出不影响容器继续运行，**推荐**。
- **docker attach 容器名**：连接到容器**主进程**的 stdin/stdout，退出（如 Ctrl+P Ctrl+Q 可 detach）或结束主进程会导致容器退出，一般不用于日常调试。

**面试点**：排查用 `exec`，不用 `attach` 当「进容器」用。

---

## 四、网络与数据持久化

### 12. Docker 网络模式有哪些？

| 模式       | 说明                     |
|------------|--------------------------|
| bridge     | 默认，容器有独立网络栈，通过桥接与宿主机通信，端口需 -p 映射 |
| host       | 容器直接使用宿主机网络，无独立 IP，性能好但隔离差 |
| none       | 无网络                   |
| container:name/id | 与指定容器共享网络栈 |

**面试点**：默认 bridge；要高性能或本机直连可用 host；容器间互通用同一网络或 container 模式。

---

### 13. 如何让多个容器互相访问？（如容器内访问数据库容器）

- **同一自定义网络**：`docker network create mynet`，run 时 `--network mynet`；同一网络内可用**容器名**作为主机名互相访问（Docker 内置 DNS）。
- **链接（link）**：旧方式，不推荐，用网络替代。

**面试点**：自定义 network + 容器名解析，是推荐做法。

---

### 14. 数据卷（Volume）是什么？和绑定挂载的区别？

- **Volume**：由 Docker 管理的存储，在宿主机某目录（如 /var/lib/docker/volumes/xxx），**与容器生命周期解耦**，删除容器不会删卷；多容器可挂载同一卷共享数据。
- **绑定挂载（Bind Mount）**：直接把宿主机目录挂到容器，`-v /host/path:/container/path`，依赖宿主机路径存在。
- **区别**：Volume 可只写卷名、跨平台一致；Bind 灵活但路径依赖宿主机。

**面试点**：持久化用 Volume 或 Bind；Volume 更「Docker 化」，Bind 更直观。

---

### 15. 容器与宿主机如何互传文件？

- **拷贝**：`docker cp 容器名:容器内路径 宿主机路径`；`docker cp 宿主机路径 容器名:容器内路径`。
- **挂载**：run 时用 `-v 宿主机路径:容器路径`，两边目录实时同步。

**面试点**：临时用 cp，长期共享用 -v 挂载。

---

## 五、Docker Compose

### 16. Docker Compose 是什么？解决什么问题？

- **Compose**：用 **YAML** 定义多容器应用（服务、网络、卷），一条命令 **up** 启动全部，**down** 停止删除。
- **解决问题**：本地/测试环境一键启停多服务（如 Web + DB + Redis），无需手写多个 docker run。

**面试点**：多容器编排、开发/测试环境、一个文件描述整套服务。

---

### 17. docker-compose.yml 常用字段？

- **services**：服务名 → 镜像/构建、端口、环境变量、卷、依赖等。
- **image / build**：用现成镜像或从 Dockerfile 构建。
- **ports**：端口映射。
- **environment / env_file**：环境变量。
- **volumes**：挂载卷或宿主机路径。
- **depends_on**：启动顺序（先起依赖服务）；不保证依赖「就绪」，仅保证「已启动」。
- **networks**：加入的网络，同网络内用服务名访问。

**面试点**：能写一个含 2～3 个服务（如 app + db）的 compose 即可。

---

### 18. Compose 中服务间如何通信？

- 同一 **networks** 下的服务，用 **服务名** 作为主机名访问（如 `http://db:3306`）。
- 默认 Compose 会创建一个以项目名命名的网络，所有服务都在其上，无需额外配置即可互访。

**面试点**：服务名 = 主机名，同网络即可。

---

## 六、实践与 CI/CD

### 19. 测试/CI 中 Docker 的典型用法？

- **环境一致**：用例在 Docker 镜像里跑，保证与开发/生产一致。
- **依赖隔离**：每个任务用独立容器，互不污染。
- **CI 流水线**：构建镜像 → 推仓库 → 拉镜像跑自动化（如 pytest、接口测试）；或 Jenkins/GitLab 的 Agent 本身跑在容器里。
- **一键环境**：docker-compose 拉起整套依赖（DB、MQ、Redis），再跑测试。

**面试点**：环境一致、隔离、CI 内构建与运行、Compose 搭测试环境。

---

### 20. 如何把本地镜像推到私有仓库？

- **打标签**：`docker tag 本地镜像:tag 仓库地址/镜像名:tag`（如 `registry.company.com/myapp:v1`）。
- **登录**：`docker login 仓库地址`。
- **推送**：`docker push 仓库地址/镜像名:tag`。
- 私有仓库需先部署（如 Harbor）并配置 HTTPS/认证。

**面试点**：tag → login → push；企业常用 Harbor。

---

### 21. 容器挂了如何排查？

- **日志**：`docker logs 容器名`（加 -f 实时）。
- **状态**：`docker ps -a` 看退出码；`docker inspect 容器名` 看详细配置与状态。
- **进容器**：若还能 start，用 `docker exec -it 容器名 sh` 进去看进程、文件、网络（若镜像有 sh）。
- **资源**：`docker stats` 看 CPU/内存；宿主机 `top`、`df` 等。

**面试点**：logs → ps -a / inspect → exec → 宿主机资源。

---

### 22. 容器与虚拟机相比有什么安全注意点？

- **共享内核**：内核漏洞影响所有容器；需及时打宿主机与基础镜像补丁。
- ** root**：容器内默认 root，若被突破可能影响宿主机；可 Dockerfile 里用 USER 非 root，或运行时 --user。
- **镜像**：只用可信镜像或自建；扫描漏洞（如 Trivy、 Clair）。
- **能力**：避免 --privileged；按需限制 Capabilities、只读根文件系统等。

**面试点**：内核共享、少用 root、镜像可信与扫描、最小权限。

---

## 七、小结速记

| 模块         | 关键词 |
|--------------|--------|
| 基础         | 容器化、镜像/容器/仓库、与 VM 区别（轻量、共享内核） |
| 镜像         | 分层、Dockerfile、多阶段构建、CMD/ENTRYPOINT、减小体积 |
| 命令         | run -d -p -v -e、exec 进容器、logs |
| 网络         | bridge/host、自定义网络、容器名解析 |
| 数据         | Volume、Bind Mount、持久化、docker cp |
| Compose      | 多容器、YAML、服务名通信、depends_on |
| 实践         | CI 构建与运行、私有仓库、排错 logs/inspect/exec、安全 |

---

*可与《Python自动化测试常见面试题》《JMeter自动化测试常见面试题》《测试开发常见面试题》搭配复习，Docker 是测试环境与 CI 的常考项。*
