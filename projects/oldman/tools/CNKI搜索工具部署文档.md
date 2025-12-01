# CNKI 搜索工具部署文档

## 工具简介

基于 Puppeteer 的知网（CNKI）论文搜索爬虫工具，支持关键词搜索并获取论文标题、作者、来源期刊、发表日期等信息。

**核心特性：**
- 使用真实浏览器模拟人类操作，绕过反爬机制
- 自动检测系统 Chrome 浏览器路径
- 支持自定义搜索结果数量
- 返回标准学术引用格式数据

**技术栈：**
- Node.js
- Puppeteer 21.0.0+
- Chrome/Chromium 浏览器

---

## 一、本地部署（macOS/Windows）

### 1.1 环境要求

- **Node.js**: 14.x 或更高版本
- **Chrome 浏览器**: 已安装在标准路径
- **PromptX 系统**: 工具运行平台

### 1.2 安装步骤

#### 步骤1：复制工具文件

```bash
# 创建工具目录
mkdir -p ~/.promptx/resource/tool/cnki-search

# 复制工具文件
cp tools/cnki-search.tool.js ~/.promptx/resource/tool/cnki-search/
```

#### 步骤2：安装依赖（可选）

首次运行时会自动安装依赖，也可以手动预安装：

```bash
cd ~/.promptx/resource/tool/cnki-search
npm install puppeteer@^21.0.0
```

#### 步骤3：验证 Chrome 路径

工具会自动检测以下路径：

**macOS:**
```
/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
```

**Windows:**
```
C:\Program Files\Google\Chrome\Application\chrome.exe
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
```

检查 Chrome 是否存在：
```bash
# macOS
ls -la "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Windows (PowerShell)
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

### 1.3 使用方法

#### 基础搜索（返回10篇）
```bash
mcp__promptx__toolx @tool://cnki-search --parameters '{"keyword": "人工智能"}'
```

#### 自定义数量
```bash
mcp__promptx__toolx @tool://cnki-search --parameters '{"keyword": "深度学习", "limit": 20}'
```

#### 调试模式（显示浏览器窗口）
```bash
mcp__promptx__toolx @tool://cnki-search --parameters '{"keyword": "机器学习", "headless": false}'
```

---

## 二、Linux 服务器部署

### 2.1 系统依赖安装

#### Ubuntu/Debian

```bash
# 更新包列表
sudo apt update

# 安装 Chrome 浏览器
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

# 或安装 Chromium
sudo apt install chromium-browser

# 安装 Puppeteer 依赖库
sudo apt install -y \
  ca-certificates \
  fonts-liberation \
  libappindicator3-1 \
  libasound2 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libc6 \
  libcairo2 \
  libcups2 \
  libdbus-1-3 \
  libexpat1 \
  libfontconfig1 \
  libgbm1 \
  libgcc1 \
  libglib2.0-0 \
  libgtk-3-0 \
  libnspr4 \
  libnss3 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libstdc++6 \
  libx11-6 \
  libx11-xcb1 \
  libxcb1 \
  libxcomposite1 \
  libxcursor1 \
  libxdamage1 \
  libxext6 \
  libxfixes3 \
  libxi6 \
  libxrandr2 \
  libxrender1 \
  libxss1 \
  libxtst6 \
  lsb-release \
  wget \
  xdg-utils
```

#### CentOS/RHEL

```bash
# 安装 Chromium
sudo yum install chromium

# 安装依赖库
sudo yum install -y \
  alsa-lib \
  atk \
  cups-libs \
  gtk3 \
  libXcomposite \
  libXcursor \
  libXdamage \
  libXext \
  libXi \
  libXrandr \
  libXScrnSaver \
  libXtst \
  pango \
  xorg-x11-fonts-100dpi \
  xorg-x11-fonts-75dpi \
  xorg-x11-fonts-cyrillic \
  xorg-x11-fonts-misc \
  xorg-x11-fonts-Type1 \
  xorg-x11-utils
```

### 2.2 无界面服务器配置

如果是无显示环境（headless server），需要虚拟显示：

```bash
# 安装 Xvfb
sudo apt install xvfb  # Ubuntu/Debian
sudo yum install xorg-x11-server-Xvfb  # CentOS/RHEL

# 启动虚拟显示
Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &
export DISPLAY=:99

# 持久化配置（添加到 ~/.bashrc）
echo 'export DISPLAY=:99' >> ~/.bashrc
```

### 2.3 工具安装

```bash
# 创建工具目录
mkdir -p ~/.promptx/resource/tool/cnki-search

# 复制工具文件
cp cnki-search.tool.js ~/.promptx/resource/tool/cnki-search/

# 安装依赖
cd ~/.promptx/resource/tool/cnki-search
npm install puppeteer@^21.0.0
```

### 2.4 验证部署

```bash
# 检查 Chrome 是否可用
which google-chrome
google-chrome --version

# 或检查 Chromium
which chromium-browser
chromium-browser --version

# 测试工具
mcp__promptx__toolx @tool://cnki-search --parameters '{"keyword": "测试"}'
```

---

## 三、Docker 部署（推荐）

### 3.1 Dockerfile

创建 `Dockerfile`:

```dockerfile
FROM node:18-slim

# 安装 Chrome 和依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxss1 \
    libxtst6 \
    lsb-release \
    xdg-utils \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制工具文件
COPY cnki-search.tool.js package.json ./

# 安装依赖
RUN npm install

# 运行工具
CMD ["node", "index.js"]
```

### 3.2 构建和运行

```bash
# 构建镜像
docker build -t cnki-search-tool .

# 运行容器
docker run --rm cnki-search-tool

# 交互式运行
docker run -it --rm cnki-search-tool /bin/bash
```

---

## 四、配置说明

### 4.1 参数配置

工具支持以下参数：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| keyword | string | 是 | - | 搜索关键词 |
| limit | number | 否 | 10 | 返回结果数量（1-50） |
| headless | boolean | 否 | true | 是否无界面模式 |

**示例：**
```json
{
  "keyword": "深度学习",
  "limit": 20,
  "headless": true
}
```

### 4.2 自定义 Chrome 路径

如果 Chrome 安装在非标准路径，编辑 `cnki-search.tool.js`:

```javascript
const chromePaths = [
  // macOS
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',

  // Windows
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',

  // Linux
  '/usr/bin/google-chrome',
  '/usr/bin/chromium-browser',
  '/usr/bin/chromium',
  '/snap/bin/chromium',

  // 添加你的自定义路径
  '/your/custom/path/to/chrome'
];
```

---

## 五、常见问题

### 5.1 Chrome 启动失败

**问题：** `Error: Failed to launch the browser process`

**解决方案：**
```bash
# 检查缺失的依赖库
ldd /usr/bin/google-chrome | grep "not found"

# 安装缺失的库
sudo apt install <missing-library>
```

### 5.2 权限错误

**问题：** `Running as root without --no-sandbox is not supported`

**解决方案：**
工具已自动添加 `--no-sandbox` 参数，如果仍有问题，检查用户权限：

```bash
# 不要用 root 用户运行
sudo useradd -m cnki-user
sudo su - cnki-user
```

### 5.3 内存不足

**问题：** `Allocation failed - JavaScript heap out of memory`

**解决方案：**
```bash
# 增加 Node.js 内存限制
export NODE_OPTIONS="--max-old-space-size=2048"

# 或在工具启动参数中添加
args: ['--max-old-space-size=512']
```

### 5.4 搜索结果为空

**问题：** 返回 `[]` 空数组

**可能原因：**
- 关键词太窄，知网无结果
- 知网页面结构变化
- 网络连接问题

**解决方案：**
```bash
# 1. 尝试更通用的关键词
{"keyword": "人工智能"}  # 而非 "基于深度学习的XXX系统"

# 2. 开启调试模式查看
{"keyword": "测试", "headless": false}

# 3. 检查网络连接
curl https://kns.cnki.net
```

### 5.5 Puppeteer 下载 Chromium 超时

**问题：** `RequestError: socket hang up`

**解决方案：**
工具已配置使用系统 Chrome，避免下载 Chromium。如果仍需下载，配置代理：

```bash
# 设置代理
export HTTPS_PROXY=http://your-proxy:port

# 或跳过下载
export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
```

---

## 六、性能优化

### 6.1 批量搜索优化

```bash
# 避免短时间大量请求（防止被封IP）
# 建议每次搜索间隔 3-5 秒
```

### 6.2 内存优化

```javascript
// 在工具中添加浏览器关闭逻辑
await browser.close();  // 已包含
```

### 6.3 并发控制

如需并发搜索，使用进程池限制：

```bash
# 最多同时运行 3 个实例
parallel -j 3 mcp__promptx__toolx @tool://cnki-search --parameters ::: \
  '{"keyword": "AI"}' \
  '{"keyword": "ML"}' \
  '{"keyword": "DL"}'
```

---

## 七、安全注意事项

1. **遵守知网使用协议**：不要用于商业爬取或大规模采集
2. **频率限制**：建议每次搜索间隔 3-5 秒
3. **数据用途**：仅用于学术研究和个人学习
4. **IP 保护**：避免短时间大量请求导致 IP 被封

---

## 八、技术原理

### 8.1 为什么用 Puppeteer？

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| HTTP 请求 | 快速、轻量 | 无法执行 JS、易被反爬 | 静态页面 |
| **Puppeteer** | 真实浏览器、绕过反爬 | 慢、资源消耗大 | 动态页面、反爬网站 |

知网使用 JavaScript 动态渲染内容，必须用真实浏览器。

### 8.2 工作流程

```
1. 启动 Chrome 浏览器（无界面模式）
   ↓
2. 访问知网搜索页面
   ↓
3. 输入关键词并点击搜索
   ↓
4. 等待页面加载完成（waitForSelector）
   ↓
5. 执行 JavaScript 解析 DOM 结构
   ↓
6. 提取论文数据（标题、作者、来源、日期）
   ↓
7. 关闭浏览器，返回结构化数据
```

### 8.3 反爬策略

- 使用真实浏览器 User-Agent
- 模拟人类操作延迟
- 随机化操作间隔
- 限制请求频率

---

## 九、更新日志

### v3.1.0 (2024-09-30)
- ✅ 支持系统 Chrome 自动检测
- ✅ 避免下载 Chromium
- ✅ 优化搜索结果解析
- ✅ 添加 GB/T 7714-2015 引用格式

### v3.0.0 (2024-09-29)
- ✅ 从 HTTP 请求迁移到 Puppeteer
- ✅ 实现真实浏览器爬取

---

## 十、技术支持

**工具位置：** `tools/cnki-search.tool.js`
**文档位置：** 本文档
**作者：** 鲁班（PromptX 工具专家）

如有问题，请检查：
1. Chrome 是否正确安装
2. 系统依赖是否完整
3. 网络连接是否正常
4. 关键词是否合理

---

**最后更新：** 2024-09-30