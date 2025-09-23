# 论文生成与导出系统 Product Requirements Document (PRD)

## Goals and Background Context

### Goals
- 建立端到端的AI论文创作平台，实现"思路→大纲→内容→发布"的完整闭环
- 提供数据一致性保障的解耦架构，确保大纲与内容的独立性和同步性
- 集成多模态AI生成能力（文本、UML图、数据表），提升论文质量和效率
- 建立可复用的资料库系统，支持资料的一次上传、多次引用
- 提供灵活的工作流引擎，支持批量生成和容错处理
- 为商家提供高质量论文辅导工具，输出90%可直接使用的论文内容

### Background Context
传统论文写作面临效率低、格式不统一、资料管理混乱等痛点。本系统通过AI技术和工程化方法，将论文创作标准化为可复现的工作流程，显著提升学术写作的质量和效率。系统采用JSON数据驱动的架构，实现了大纲、内容、资料、工作流的完全解耦。

目标用户为商家，用于辅导学生论文写作，要求生成的论文内容达到90%可直接使用的质量标准。

### Change Log
| Date | Version | Description | Author |
|------|---------|-------------|---------|
| 2025-09-23 | v1.0 | 初始PRD创建，定义论文生成系统需求 | John (PM) |

## Requirements

### Functional

**工具化架构需求:**
- FR1: 系统采用全栈JavaScript工具化架构，每个功能模块封装为独立的.tool.js文件
- FR2: 支持服务端函数和API Routes两种调用方式，便于前端和后端调用
- FR3: 工作流引擎仅负责调度和状态管理，具体业务逻辑封装在工具中

**项目与数据管理功能:**
- FR4: 项目管理工具 - 创建论文项目时自动生成独立目录结构
- FR5: 大纲管理工具 - 提供树形结构的CRUD操作，自动同步content.json
- FR6: 资料库工具 - 文件上传、手动添加描述说明、标签管理、项目内独立存储
- FR7: 内容存储工具 - 章节内容的版本化存储和检索

**AI生成功能:**
- FR8: 文本生成工具 - 集成ChatGPT-4o-mini，支持自定义baseURL和API key
- FR9: UML代码生成工具 - 专门生成PlantUML/Mermaid代码的AI工具
- FR10: 数据表生成工具 - 生成三线表数据，支持AI和SQL两种模式

**渲染处理功能:**
- FR11: UML渲染工具 - PlantUML/Mermaid代码转PNG/SVG图片
- FR12: 表格渲染工具 - 数据转换为标准三线表格式
- FR13: 文档样式工具 - 应用学术论文格式规范

**核心业务功能:**
- FR14: 上下文合成工具 - 将选定资料的描述和章节内容拼接为AI生成的prompt输入
- FR15: 单章节重新生成，允许修改Prompt、上下文和资料
- FR16: 容错机制 - 生成失败不影响整体导出，使用占位符处理
- FR17: 工作流配置 - 通过JSON定义生成步骤和执行策略

**导出功能:**
- FR18: Manifest生成工具 - 合并大纲和内容生成导出清单
- FR19: Word导出工具 - 根据manifest.json生成符合学术规范的DOCX

**扩展性功能:**
- FR20: 模板管理工具 - 支持论文、开题报告等不同文档模板（预留）
- FR21: 论文补充工具 - 基于已有论文进行内容扩展（预留接口）
- FR22: 用户认证工具 - 预留用户管理和权限控制（预留接口）

### Non Functional

**工具化架构要求:**
- NFR1: 每个工具提供标准化的函数接口和API Routes
- NFR2: 工具间通信仅通过JSON数据交换，无直接依赖
- NFR3: 工具支持独立配置，支持热重载
- NFR4: 工具故障不能影响其他工具的正常运行
- NFR5: 新工具可通过配置注册到工作流，无需修改核心代码

**性能和质量要求:**
- NFR6: AI生成工具的输出质量要求90%可直接使用
- NFR7: 单个工具调用响应时间不超过30秒
- NFR8: 工具支持并发调用，最大并发数可配置
- NFR9: ChatGPT API配置支持热更新，无需重启系统

**数据和存储要求:**
- NFR10: 工具间数据传递使用标准JSON Schema验证
- NFR11: 系统支持单文档最大50章节，每章节最多20个图表
- NFR12: JSON数据文件大小限制：outline.json < 1MB, content.json < 10MB
- NFR13: 所有工具操作记录详细日志，支持审计和调试

## User Interface Design Goals

### Overall UX Vision
商用级论文创作工作台，强调效率和专业性。界面简洁直观，支持高效的论文创作workflow。

### Key Interaction Paradigms
- **拖拽式大纲编辑**: 支持章节的拖拽重排和层级调整
- **实时预览**: 内容生成过程可视化，提供进度反馈
- **模块化面板**: 每个工具对应独立的操作面板
- **标签页模式**: 章节编辑采用正文/图表/表格标签页

### Core Screens and Views
- 项目管理页面: 创建、切换、删除项目，项目模板选择
- 资料库管理页面: 文件上传、预览、标签管理（项目级别）
- 大纲编辑页面: 树形结构编辑器
- 章节编辑页面: 正文/图表/表格编辑(标签页模式)
- 工作流执行页面: 批量生成和状态监控
- 导出预览页面: 最终文档预览和下载

### Accessibility: WCAG AA
支持基础可访问性要求，确保键盘导航和屏幕阅读器兼容

### Branding
学术风格设计，采用简洁的学术论文排版风格，配色以蓝白为主

### Target Device and Platforms: Web Responsive
桌面优先设计，兼容平板设备。主要支持现代浏览器。

## Technical Assumptions

### Repository Structure: Monorepo
使用单一代码仓库，包含前端、后端、工具模块等所有组件

### Service Architecture
全栈JavaScript架构(Next.js/Nuxt.js)，支持服务端渲染和API Routes。工具采用模块化设计，支持服务端函数和Web API双重调用方式。

### Testing Requirements
单元测试覆盖所有工具模块，集成测试覆盖工作流执行，端到端测试覆盖完整的论文生成流程。

### Additional Technical Assumptions and Requests
- AI服务集成ChatGPT-4o-mini，支持自定义baseURL和API key配置
- 数据存储使用JSON文件系统，确保跨会话数据一致性
- UML渲染支持PlantUML和Mermaid两种格式
- Word导出基于Office Open XML标准
- 工具化架构支持动态加载和热插拔
- 预留多租户架构空间，为未来用户管理做准备
- **工具开发方式**: 使用promptx MCP的鲁班功能编写各个.tool.js文件，完成后复制一份提供web调用版本

## Epic List

### Epic 1: 基础架构与工具框架
建立项目基础设施，实现工具化架构框架，提供项目管理和基础文件管理能力

### Epic 2: 核心数据管理
实现大纲管理、资料库管理、内容存储等核心数据操作工具

### Epic 3: AI生成引擎
集成ChatGPT API，实现文本、UML、表格的AI生成能力

### Epic 4: 渲染与导出系统
实现UML渲染、表格格式化、Word文档导出等功能

### Epic 5: 工作流引擎与用户界面
构建工作流调度引擎和完整的用户操作界面

## Epic 1: 基础架构与工具框架

建立项目基础设施和工具化架构，为后续功能开发提供稳固的技术基础。

### Story 1.1: 项目管理工具 (project-manager.tool.js)

As a 用户,
I want 为每篇论文创建独立的项目目录,
so that 可以同时管理多个论文项目而不会混淆数据。

#### Acceptance Criteria
1. 创建项目时自动生成独立目录结构（outline.json, content.json, files.json等）
2. 支持项目列表查看和切换功能
3. 实现项目模板系统（论文、报告、开题报告等）
4. 项目删除时安全清理所有相关文件
5. 提供项目导入导出功能（便于备份和迁移）

### Story 1.2: 项目初始化与基础配置

As a 开发者,
I want 建立Next.js项目基础架构,
so that 为论文生成系统提供技术基础。

#### Acceptance Criteria
1. 创建Next.js项目，配置TypeScript支持
2. 建立基础目录结构：tools/、pages/api/、components/、types/
3. 配置ESLint、Prettier代码规范
4. 建立基础的环境变量配置（ChatGPT API配置）
5. 创建基础的错误处理和日志记录机制

### Story 1.3: 工具化架构框架

As a 开发者,
I want 建立标准化的工具调用框架,
so that 所有工具都遵循统一的接口规范。

#### Acceptance Criteria
1. 创建ToolBase基类，定义标准接口（execute、validate、getConfig）
2. 实现工具注册机制，支持动态加载工具
3. 建立API Routes路由规则：/api/tools/{toolName}
4. 实现统一的输入验证和错误处理机制
5. 创建工具配置管理（支持热重载）

### Story 1.4: 基础文件管理工具

As a 用户,
I want 上传和管理资料文件,
so that 可以为论文生成提供参考资料。

#### Acceptance Criteria
1. 实现文件上传API（支持PDF、Word、TXT格式）
2. 生成文件唯一ID和hash值
3. 创建files.json数据结构管理
4. 实现基础文件操作（上传、删除、查询）
5. 支持文件大小和格式验证

## Epic 2: 核心数据管理

实现论文结构化数据的管理，包括大纲、内容、资料的CRUD操作和数据同步。

### Story 2.1: 大纲管理工具 (outline-manager.tool.js)

As a 用户,
I want 创建和编辑论文大纲,
so that 可以构建论文的层次结构。

#### Acceptance Criteria
1. 实现树形节点的增删改操作
2. 支持节点拖拽重排和层级调整
3. 自动生成章节编号（1, 1.1, 1.1.1格式）
4. 实现outline.json与content.json的自动同步
5. 提供大纲数据的验证和修复功能

### Story 2.2: 资料库管理工具 (file-manager.tool.js)

As a 用户,
I want 管理论文相关的参考资料,
so that 可以在写作过程中引用和使用。

#### Acceptance Criteria
1. 支持文件上传到项目独立目录（uploads/）
2. 为每个文件提供描述说明输入框，用于添加资料使用说明
3. 支持标签系统，便于资料分类和检索
4. 实现文件引用计数和依赖关系跟踪
5. 提供资料搜索和过滤功能（按文件名、标签、描述内容）
6. 支持多种文件格式（PDF、Word、TXT、图片）
7. 显示文件上传时间、大小、引用次数等元信息
8. 文件列表支持预览和描述编辑功能

### Story 2.3: 内容存储工具 (content-manager.tool.js)

As a 用户,
I want 管理各章节的内容数据,
so that 可以存储和检索论文的详细内容。

#### Acceptance Criteria
1. 实现章节内容的结构化存储（正文、图表、表格）
2. 支持内容版本管理和历史记录
3. 实现章节间的上下文关联配置
4. 提供内容完整性验证
5. 支持批量内容操作（复制、移动、删除）

## Epic 3: AI生成引擎

集成AI服务，实现文本、图表、表格的智能生成功能。

### Story 3.1: ChatGPT API集成工具 (chatgpt-client.tool.js)

As a 系统,
I want 集成ChatGPT API服务,
so that 可以提供AI文本生成能力。

#### Acceptance Criteria
1. 实现ChatGPT API客户端，支持自定义baseURL和API key
2. 支持API配置的热更新（无需重启）
3. 实现请求重试机制和错误处理
4. 记录API调用日志（请求时间、token消耗、响应时间）
5. 支持多种模型参数配置（temperature、max_tokens等）

### Story 3.2: 文本生成工具 (text-generator.tool.js)

As a 用户,
I want AI帮助生成章节正文,
so that 可以高效完成论文写作。

#### Acceptance Criteria
1. 根据章节标题和上下文生成高质量正文内容
2. 支持目标字数控制（字符数或词数）
3. 集成上下文合成，包含相关资料和章节信息
4. 输出内容质量达到90%可直接使用标准
5. 支持重新生成和内容微调

### Story 3.3: UML代码生成工具 (uml-generator.tool.js)

As a 用户,
I want AI生成UML图代码,
so that 可以在论文中插入专业的图表。

#### Acceptance Criteria
1. 支持PlantUML和Mermaid两种格式生成
2. 根据描述prompt生成语法正确的UML代码
3. 实现语法验证和错误提示
4. 支持多种图表类型（流程图、时序图、类图等）
5. 生成的代码可直接用于渲染

### Story 3.4: 表格生成工具 (table-generator.tool.js)

As a 用户,
I want AI生成论文所需的数据表格,
so that 可以展示研究数据和分析结果。

#### Acceptance Criteria
1. 支持AI模式：根据描述生成表格数据
2. 支持SQL模式：解析SQL语句生成表格
3. 输出标准三线表格式（适合学术论文）
4. 支持表头自定义和数据类型验证
5. 生成的表格数据支持手动编辑和修正

## Epic 4: 渲染与导出系统

实现多媒体内容的渲染处理和最终文档的导出功能。

### Story 4.1: UML渲染工具 (uml-renderer.tool.js)

As a 用户,
I want 将UML代码渲染为图片,
so that 可以在论文中展示可视化图表。

#### Acceptance Criteria
1. 支持PlantUML和Mermaid代码渲染
2. 输出PNG和SVG两种格式
3. 支持自定义图片尺寸和主题样式
4. 实现渲染缓存机制，提升性能
5. 渲染失败时提供详细错误信息

### Story 4.2: 文档样式工具 (doc-styler.tool.js)

As a 用户,
I want 应用标准的学术论文格式,
so that 导出的文档符合学术规范。

#### Acceptance Criteria
1. 定义学术论文标准样式（字体、字号、行距、页边距）
2. 支持多级标题格式化
3. 实现图表标题和编号的自动管理
4. 支持参考文献格式化
5. 提供样式配置的可定制性

### Story 4.3: Manifest生成工具 (manifest-builder.tool.js)

As a 系统,
I want 生成导出清单,
so that 可以整合所有内容为统一的导出格式。

#### Acceptance Criteria
1. 合并outline.json和content.json数据
2. 按大纲顺序拍平所有章节内容
3. 验证内容完整性（检查缺失的图表、表格）
4. 生成包含样式信息的完整manifest.json
5. 支持部分内容失败时的占位符处理

### Story 4.4: Word导出工具 (docx-exporter.tool.js)

As a 用户,
I want 导出标准的Word文档,
so that 可以获得可直接使用的论文文档。

#### Acceptance Criteria
1. 根据manifest.json生成格式规范的DOCX文件
2. 正确插入图片和表格，保持版式美观
3. 应用学术论文标准格式（字体、样式、页面设置）
4. 生成目录和图表索引
5. 支持导出进度显示和文件下载

## Epic 5: 工作流引擎与用户界面

构建智能工作流系统和直观的用户操作界面。

### Story 5.1: 工作流引擎 (workflow-engine.tool.js)

As a 用户,
I want 自动化执行论文生成流程,
so that 可以批量完成内容创建和处理。

#### Acceptance Criteria
1. 解析workflow.json配置，生成执行计划
2. 支持并发执行和依赖管理
3. 实现实时状态更新和进度跟踪
4. 记录详细的执行日志到workflow-status.json
5. 支持失败重试和断点续传

### Story 5.2: 上下文合成工具 (context-composer.tool.js)

As a 系统,
I want 将资料描述和章节内容拼接为AI prompt,
so that 可以为文本生成提供完整的上下文。

#### Acceptance Criteria
1. 将选定资料的描述说明拼接到prompt中
2. 提取相关章节的内容作为上下文参考
3. 按优先级顺序组织prompt结构（资料描述 + 章节上下文 + 生成要求）
4. 控制prompt总长度，避免token超限
5. 提供prompt内容的预览和编辑功能

### Story 5.3: 资料库管理界面

As a 用户,
I want 通过界面管理参考资料,
so that 可以方便地组织和使用资料库。

#### Acceptance Criteria
1. 文件拖拽上传界面，支持批量操作和进度显示
2. 上传后显示文件信息，提供描述说明输入框
3. 资料列表展示（缩略图、描述说明、标签、文件信息）
4. 描述说明的内联编辑功能（双击编辑模式）
5. 标签管理和多条件搜索过滤功能（文件名、标签、描述内容）
6. 资料详情面板（完整描述、引用情况、关联章节）
7. 批量操作功能（批量打标签、批量删除）
8. 资料引用状态和关联章节显示
9. 支持复制资料描述到剪贴板（便于手动使用）

### Story 5.4: 大纲编辑界面

As a 用户,
I want 通过可视化界面编辑论文大纲,
so that 可以直观地构建论文结构。

#### Acceptance Criteria
1. 树形结构展示，支持折叠/展开
2. 拖拽重排功能，实时更新编号
3. 右键菜单（添加、删除、复制章节）
4. 章节标题的内联编辑
5. 大纲与内容的同步状态显示

### Story 5.5: 章节编辑界面

As a 用户,
I want 编辑具体章节的内容,
so that 可以管理正文、图表、表格等多种内容。

#### Acceptance Criteria
1. 标签页模式（正文、图表、表格、资料、上下文）
2. 正文编辑器，支持富文本和Markdown
3. 图表配置界面，支持UML代码编辑和预览
4. 表格编辑器，支持可视化编辑和数据导入
5. AI生成按钮和进度指示器

### Story 5.6: 工作流执行界面

As a 用户,
I want 监控和控制论文生成流程,
so that 可以了解执行状态并及时处理问题。

#### Acceptance Criteria
1. 工作流步骤的可视化展示
2. 实时进度条和状态更新
3. 错误信息展示和重试控制
4. 执行日志的详细查看
5. 支持暂停、继续、取消操作

### Story 5.7: 导出预览界面

As a 用户,
I want 预览和下载最终的论文文档,
so that 可以检查内容质量并获取成果。

#### Acceptance Criteria
1. 论文内容的在线预览（接近Word效果）
2. 导出选项配置（格式、样式、范围）
3. 导出进度显示和状态反馈
4. 文档下载链接和历史记录
5. 导出质量检查和错误提示

## Checklist Results Report

PRD创建完成，等待执行pm-checklist进行质量检查。

## Next Steps

### UX Expert Prompt
请基于此PRD创建用户体验设计方案，重点关注论文创作工作流的用户体验优化。

### Architect Prompt
请基于此PRD设计系统技术架构，重点关注工具化架构的技术实现和扩展性设计。