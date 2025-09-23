# 📄 论文生成系统 - Web界面

基于 JSON + 工作流的论文生成系统的前端界面，完全无后端设计，配合 Claude Code 使用。

## 🚀 快速开始

### 1. 启动本地服务器

由于浏览器的安全限制，需要通过HTTP服务器访问：

```bash
# 进入web目录
cd web

# 使用Python启动简单服务器
python3 -m http.server 8080

# 或使用Node.js (如果安装了http-server)
npx http-server -p 8080

# 或使用VS Code Live Server扩展
```

### 2. 访问系统

打开浏览器访问：`http://localhost:8080`

## 📋 功能模块

### 1. 项目管理
- ✅ 创建新论文项目
- ✅ 上传源码ZIP文件
- ✅ 选择论文模板
- ✅ 项目列表管理

### 2. 模板库
- ✅ 查看大纲模板
- ✅ 查看内容模板
- ✅ 在线编辑模板
- ✅ 下载模板文件

### 3. 大纲编辑
- ✅ 树形结构编辑
- ✅ 拖拽排序
- ✅ 自动生成章节ID
- ✅ 占位符支持

### 4. 内容编辑
- ✅ 章节计划配置
- ✅ 图表计划设置
- ✅ 表格计划设置
- ✅ 提示词编辑

### 5. 执行控制台
- ✅ Init 命令生成
- ✅ Prefill 命令生成
- ✅ Run 命令生成
- ✅ 执行日志显示

### 6. 导出预览
- ✅ 导出命令生成
- ✅ 导出历史记录
- ✅ 文件下载链接

## 🔧 使用流程

### 第一步：创建项目
1. 点击"新建项目"
2. 输入项目名称、论文题目、主题
3. 上传源码ZIP文件
4. 选择模板
5. 点击"创建项目"

### 第二步：编辑大纲
1. 切换到"大纲编辑"页面
2. 选择项目
3. 编辑论文结构
4. 保存大纲

### 第三步：配置内容
1. 切换到"内容编辑"页面
2. 为每个章节配置计划
3. 设置是否需要图表
4. 编辑提示词模板
5. 保存内容

### 第四步：执行生成
1. 切换到"执行控制"页面
2. 依次点击：Init → Prefill → Run
3. 复制生成的命令到Claude Code执行
4. 查看执行日志

### 第五步：导出文档
1. 切换到"导出预览"页面
2. 点击"导出Word"
3. 复制命令到Claude Code执行
4. 下载生成的文档

## 🎯 Claude Code 命令

系统会生成以下命令供Claude Code执行：

```bash
# 初始化项目
cd /projects/my-project && cc -p init

# 预填充内容
cd /projects/my-project && cc -p prefill-content

# 生成论文
cd /projects/my-project && cc -p run-paper

# 导出Word
cd /projects/my-project && word-export --content content.json --outline outline.json --out paper.docx
```

## 📁 目录结构

```
web/
├── index.html          # 主页面
├── css/
│   ├── main.css       # 主样式
│   └── editor.css     # 编辑器样式
├── js/
│   ├── app.js         # 主应用
│   ├── utils.js       # 工具函数
│   ├── project.js     # 项目管理
│   ├── outline.js     # 大纲编辑
│   ├── content.js     # 内容编辑
│   └── executor.js    # 执行控制
├── lib/
│   └── jszip.min.js   # ZIP文件处理
└── README.md          # 说明文档
```

## ⌨️ 快捷键

- `Alt + 1-6`: 切换页面
- `Ctrl/Cmd + S`: 保存当前编辑内容
- `ESC`: 关闭模态框

## 🔒 数据存储

- 项目数据存储在浏览器 localStorage
- 源码文件通过 File API 处理
- 无需后端服务器
- 数据完全本地化

## 🐛 故障排除

### 文件上传失败
- 确保上传的是ZIP格式文件
- 检查文件大小是否合理
- 刷新页面重试

### 模板加载失败
- 确保templates目录存在
- 检查模板文件格式是否正确
- 使用HTTP服务器而非file://协议

### 项目选择器为空
- 先创建至少一个项目
- 检查localStorage是否被清空
- 刷新页面重新加载

## 🔄 更新日志

### v1.0.0 (2025-09-23)
- ✅ 完成所有核心功能模块
- ✅ 实现完整的用户界面
- ✅ 支持项目管理和模板编辑
- ✅ 集成Claude Code工作流

## 📞 技术支持

如有问题，请检查：
1. 浏览器控制台是否有错误信息
2. 网络连接是否正常
3. 文件格式是否正确
4. localStorage是否可用

## 🎨 界面预览

系统采用现代化设计，包含：
- 响应式布局
- 直观的导航栏
- 树形编辑器
- 实时状态反馈
- 命令行集成
- 模态框交互

---

**注意**: 这是一个纯前端系统，所有数据处理都在浏览器中完成。实际的论文生成需要配合Claude Code使用。