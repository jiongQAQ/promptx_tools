# 07 UML图表生成

## 路径规范
projectRoot 取当前工作目录（pwd）的绝对路径

## 功能说明
自动扫描pngs目录下的**所有JSON文件**（确保无遗漏），**严格基于每个JSON文件的content字段内容和源码分析生成个性化的UML图表**，使用luban-uml工具将PlantUML源码渲染为图片，并按照imagePath或imagePathSequence字段指定的路径进行命名。**每个图表都是独特的，完全反映对应JSON文件描述的具体业务场景，绝不使用通用模板**。支持批量处理所有符合条件的UML图表，保留整体ER图生成功能。

## 目标任务
1. **源码真相验证**：**首先读取** `<projectRoot>/paper/source-truth.json` 文件，获取项目真实技术栈和限制清单
2. **JSON文件扫描**：**完整扫描** `<projectRoot>/paper/pngs/` 目录下的**每一个JSON文件**，确保无遗漏
3. **图表类型识别**：根据文件名、content内容和图片路径字段识别图表类型：
   - `activity-*`：**双图生成** - 每个文件生成活动图（imagePath）+ 时序图（imagePathSequence）
   - `usecase-*`：用例图（处理imagePath字段）
   - `software-architecture`：软件架构图（处理imagePath字段）
   - `system-function-*`：系统功能图（处理imagePath字段）
   - `er-overview`：**整体ER关系图（保留生成）**
   - `test-*`：**测试用例三线表生成**（处理tablePath字段，生成测试用例表格JSON）
   - `perf-*`：**性能指标三线表生成**（处理tablePath字段，生成性能测试表格JSON）
   - `compat-*`：**兼容性测试三线表生成**（处理tablePath字段，生成兼容性矩阵表格JSON）
   - `Tab-*`：数据表图（跳过，不是UML图表）
   - `implementation-*`：实现图（跳过，不是UML图表）
3. **双图片字段支持**：**所有activity文件都支持双图生成**，同时处理imagePath（活动图）和imagePathSequence（时序图）
4. **动态图表数量计算**：根据实际项目文件自动计算
   - activity文件数 × 2（每个文件生成活动图+时序图）
   - usecase文件数 × 1（用例图）
   - 架构和功能类文件数 × 1（对应图表类型）
   - ER总图：1个（如果存在er-overview文件）
   - test文件数 × 1（测试用例三线表JSON）
   - perf文件数 × 1（性能指标三线表JSON）
   - compat文件数 × 1（兼容性矩阵三线表JSON）
5. **批量处理模式**：类似chapter-batch-processor，支持全量扫描和批处理所有符合条件的UML图表
6. **PlantUML源码生成**：**严格基于每个JSON文件的content字段内容生成个性化的PlantUML语法，绝不使用通用模板**
7. **图片渲染**：使用luban-uml工具将PlantUML渲染为PNG/SVG格式
8. **文件命名**：按照imagePath或imagePathSequence字段的文件名进行输出命名

## 输入要求
- **JSON目录**：`<projectRoot>/paper/pngs/`
- **源码目录**：`<projectRoot>/source/` （AI自动分析项目技术栈和架构）

## 输出结构

### 1. 图片文件输出
- **存放路径**：`<projectRoot>/paper/assets/diagrams/uml/`
- **文件命名**：按照JSON文件中imagePath字段的basename命名
- **文件格式**：PNG或SVG（默认PNG）

### 2. PlantUML源码保存
- **存放路径**：`<projectRoot>/paper/assets/plantuml/`
- **文件命名**：`{图表名}.puml`
- **用途**：便于后续修改和维护

### 3. 测试用例三线表输出
- **存放路径**：`<projectRoot>/paper/assets/tables/`
- **文件命名**：按照JSON文件中tablePath字段的basename命名
- **表格格式**：标准三线表JSON格式，包含测试用例、预期结果、实际结果等字段
- **支持类型**：
  - `test-*`：功能测试用例表（测试场景、输入、预期输出、实际结果、结论）
  - `perf-*`：性能测试指标表（指标名称、目标值、实际值、通过状态、备注）
  - `compat-*`：兼容性测试矩阵表（平台/浏览器、版本、功能状态、问题描述、解决方案）

### 4. 生成报告（stdout单行JSON）
```json
{
  "status": "success",
  "project": "<projectName>",
  "inputDir": "<projectRoot>/paper/pngs/",
  "outputDir": "<projectRoot>/paper/assets/diagrams/uml/",
  "processedCount": 12,
  "skippedCount": 5,
  "generatedImages": [
    {"file": "activity-user-auth.json", "output": "activity-user-auth.png", "type": "activity"},
    {"file": "software-architecture.json", "output": "software-architecture.png", "type": "architecture"}
  ],
  "generatedTables": [
    {"file": "test-module-a.json", "output": "test-module-a.json", "type": "test-cases"},
    {"file": "perf-metrics.json", "output": "perf-metrics.json", "type": "performance"},
    {"file": "compat-matrix.json", "output": "compat-matrix.json", "type": "compatibility"}
  ],
  "skippedFiles": [
    {"file": "entity-users.json", "reason": "单体实体图已存在"},
    {"file": "implementation-user-auth.json", "reason": "实现图不是UML图表"}
  ],
  "failedFiles": [
    {"file": "some-file.json", "reason": "PlantUML语法错误", "error": "..."}
  ]
}
```

### 5. 人类可读处理报告
- 扫描到的JSON文件总数
- 按图表类型分类的文件列表
- 成功生成的图片清单（文件名 → 输出路径）
- 成功生成的测试用例表清单（文件名 → 输出路径）
- 跳过的文件及原因（单体实体图、实现图等）
- 失败的文件及错误信息
- PlantUML源码保存位置
- 测试用例三线表保存位置
- 下一步建议

## 图表类型与样式规范（仅提供样式模板，内容必须基于content生成）

**⚠️ 重要说明：以下仅为样式模板，图表的具体内容必须完全基于对应JSON文件的content字段生成！**

### Activity Diagram（活动图）样式模板
**适用文件**：`activity-*.json`
**样式框架**（内容需基于content生成）：
```plantuml
@startuml
!theme plain
skinparam backgroundColor White
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0277BD
  FontSize 12
}
skinparam arrow {
  Color #0277BD
  FontSize 10
}
skinparam diamond {
  BackgroundColor #FFF3E0
  BorderColor #F57C00
  FontSize 11
}
skinparam linetype ortho

start
// 此处必须基于JSON文件的content字段内容生成具体的活动流程
// 不能使用通用的"用户请求"、"系统验证"等抽象描述
// 必须反映content中描述的具体业务操作步骤
stop
@enduml
```

### Architecture Diagram（架构图）样式模板
**适用文件**：`software-architecture.json`、`system-function-*.json`
**样式框架**（内容需基于content生成）：
```plantuml
@startuml
!theme plain
skinparam componentStyle rectangle
skinparam backgroundColor White
skinparam component {
  BackgroundColor #F5F5F5
  BorderColor #424242
  FontSize 12
}
skinparam package {
  BackgroundColor #E3F2FD
  BorderColor #1976D2
  FontSize 13
}
skinparam arrow {
  Color #1976D2
  FontSize 10
}
skinparam linetype ortho

// 此处必须基于JSON文件的content字段内容生成具体的架构组件
// 组件名称、层次结构、交互关系都必须来自content描述
// 技术栈信息需要结合源码验证
@enduml
```

### Use Case Diagram（用例图）样式模板
**适用文件**：`usecase-*.json`
**样式框架**（内容需基于content生成）：
```plantuml
@startuml
!theme plain
skinparam backgroundColor White
skinparam usecase {
  BackgroundColor #E8F5E8
  BorderColor #2E7D32
  FontSize 12
}
skinparam actor {
  BackgroundColor #FFF3E0
  BorderColor #F57C00
  FontSize 12
}
skinparam arrow {
  Color #2E7D32
  FontSize 10
}
skinparam linetype ortho

// 此处必须基于JSON文件的content字段内容生成具体的用例
// 角色、用例名称、系统边界都必须来自content描述
// 不能使用通用的角色和功能名称
@enduml
```

### Sequence Diagram（时序图）样式模板
**适用文件**：处理imagePathSequence字段的详细设计图
**样式框架**（内容需基于content生成）：
```plantuml
@startuml
!theme plain
skinparam backgroundColor White
skinparam sequence {
  ArrowColor #0277BD
  LifeLineBorderColor #0277BD
  LifeLineBackgroundColor #E1F5FE
  ParticipantBorderColor #0277BD
  ParticipantBackgroundColor #E1F5FE
  ParticipantFontSize 12
  MessageAlignment center
}
skinparam note {
  BackgroundColor #FFF9C4
  BorderColor #F57F17
}
skinparam linetype ortho

// 此处必须基于JSON文件的content字段内容生成具体的时序交互
// 参与者、消息序列、交互过程都必须来自content描述
// 需要体现content中提到的具体技术实现细节
@enduml
```

### ER Diagram（实体关系图）样式模板
**适用文件**：`er-overview.json`
**样式框架**（内容需基于content和源码生成）：
```plantuml
@startuml
!theme plain
skinparam backgroundColor White
skinparam entity {
  BackgroundColor #F3E5F5
  BorderColor #7B1FA2
  FontSize 12
}
skinparam arrow {
  Color #7B1FA2
  FontSize 10
}
skinparam linetype ortho

// 此处必须基于JSON文件的content字段和源码entity目录生成具体的实体关系
// 实体名称、属性、关系都必须来自真实的数据库设计
// 约束条件需要反映content中描述的业务规则
@enduml
```

### Test Case Table（测试用例三线表）格式模板
**适用文件**：`test-*.json`、`perf-*.json`、`compat-*.json`
**三线表JSON格式**（内容需基于content生成）：

#### 功能测试用例表（test-*）
```json
{
  "tableName": "test_module_a",
  "tableCnName": "模块A功能测试用例表",
  "columns": [
    ["测试用例ID", "测试场景", "输入数据", "操作步骤", "预期结果", "实际结果", "测试状态", "备注"],
    ["TC001", "用户正常登录", "用户名:admin,密码:123456", "1.输入用户名密码 2.点击登录", "登录成功,跳转首页", "登录成功,跳转首页", "通过", ""],
    ["TC002", "用户密码错误", "用户名:admin,密码:wrong", "1.输入错误密码 2.点击登录", "提示密码错误", "提示密码错误", "通过", ""],
    ["TC003", "用户名为空", "用户名:空,密码:123456", "1.用户名留空 2.点击登录", "提示用户名不能为空", "提示用户名不能为空", "通过", ""]
  ]
}
```

#### 性能测试指标表（perf-*）
```json
{
  "tableName": "perf_metrics",
  "tableCnName": "系统性能测试指标表",
  "columns": [
    ["性能指标", "目标值", "实际值", "测试环境", "并发用户数", "测试结果", "是否达标", "备注"],
    ["响应时间", "≤2秒", "1.5秒", "测试服务器", "100用户", "页面加载平均1.5秒", "达标", ""],
    ["吞吐量", "≥500TPS", "650TPS", "测试服务器", "200用户", "每秒处理650个事务", "达标", ""],
    ["并发处理", "≥1000用户", "1200用户", "测试服务器", "1200用户", "系统稳定运行", "达标", ""],
    ["CPU使用率", "≤80%", "65%", "测试服务器", "500用户", "峰值CPU使用率65%", "达标", ""]
  ]
}
```

#### 兼容性测试矩阵表（compat-*）
```json
{
  "tableName": "compat_matrix",
  "tableCnName": "系统兼容性测试矩阵表",
  "columns": [
    ["平台/浏览器", "版本", "操作系统", "核心功能", "UI显示", "交互操作", "测试结果", "问题描述", "解决方案"],
    ["Chrome", "119.0", "Windows 10", "正常", "正常", "正常", "通过", "", ""],
    ["Firefox", "118.0", "Windows 10", "正常", "正常", "正常", "通过", "", ""],
    ["Safari", "17.0", "macOS 14", "正常", "正常", "正常", "通过", "", ""],
    ["Edge", "119.0", "Windows 11", "正常", "正常", "正常", "通过", "", ""],
    ["Mobile Chrome", "119.0", "Android 13", "正常", "响应式适配", "触摸正常", "通过", "", ""]
  ]
}
```

**⚠️ 重要说明：**
1. **基于content生成**：所有测试用例内容必须基于JSON文件的content字段描述生成
2. **真实性验证**：测试场景必须对应source-truth.json中的实际功能模块
3. **数据真实性**：测试数据应反映实际业务场景和用户操作流程
4. **结果可信性**：测试结果应基于实际执行或合理的预期评估

## 智能源码分析

### AI自主分析原则
- **无预设限制**：不限制具体的技术栈（Java、Python、Node.js等）
- **自动识别**：AI根据源码结构自动识别项目架构和技术选型
- **内容驱动**：主要基于JSON中的content描述，源码作为辅助验证
- **灵活适应**：根据实际项目情况灵活生成对应的UML图表

## 🔒 源码真相验证机制

### ⚠️ 防编造设计原则
**禁止在UML图中使用任何未在源码中实际存在的技术、框架或架构模式！**

### 验证流程
1. **读取真相文件**：在生成任何UML图前，必须先读取 `<projectRoot>/paper/source-truth.json`
2. **技术栈白名单验证**：只能使用 `allowedBackend` 和 `allowedFrontend` 中列出的技术
3. **架构模式验证**：只能使用 `allowedPatterns` 中列出的架构模式
4. **禁用技术检查**：严禁使用 `prohibitedTechnologies` 中列出的任何技术
5. **实际模块验证**：只能引用 `actualModules` 中确实存在的功能模块

### source-truth.json 字段说明
```json
{
  "allowedBackend": ["Spring Boot 2.7.18", "MySQL 8.3.0", "MyBatis Plus", ...],
  "allowedFrontend": ["Vue 3.3.4", "Element Plus 2.3.8", "Pinia", ...],
  "allowedPatterns": ["MVC Architecture", "RESTful API", "Monolithic Architecture"],
  "prohibitedTechnologies": ["microservices", "GraphQL", "Redis", "Docker", ...],
  "actualModules": [...], // 只能引用这些真实存在的模块
  "entities": [...] // 只能引用这些真实的数据库实体
}
```

### 严格验证规则
#### ❌ 绝对禁止的内容
- 微服务架构相关：API Gateway、Service Registry、Config Server
- 容器化技术：Docker、Kubernetes、容器编排
- 分布式技术：Redis缓存、消息队列、分布式事务
- 非项目技术：GraphQL、MongoDB、PostgreSQL、React、Angular
- 过度设计：性能监控、链路追踪、服务网格

#### ✅ 必须使用的技术（基于source-truth.json）
- **后端限定**：Spring Boot 2.7.18 + MySQL 8.3.0 + MyBatis Plus
- **前端限定**：Vue 3 + Element Plus + Pinia + Vite
- **架构限定**：单体架构 + MVC模式 + RESTful API
- **认证限定**：Spring Security + JWT Token
- **数据访问**：MyBatis Plus ORM + 逻辑删除

### PlantUML内容检查点
1. **组件命名检查**：所有组件名必须来自真实的类名或模块名
2. **技术栈检查**：每个技术标签都必须在允许清单中
3. **架构模式检查**：不能出现微服务、分布式等禁用架构
4. **数据库检查**：只能使用MySQL，不能出现Redis、MongoDB等
5. **部署检查**：不能出现Docker、K8s等容器化内容

### 验证失败处理
- **技术不匹配**：拒绝生成，记录违规技术到failedFiles
- **架构过度设计**：简化为允许的单体架构模式
- **模块不存在**：只使用actualModules中确实存在的模块
- **实体不匹配**：只引用entities中的真实数据库表

## PlantUML生成规则

### 🎯 核心原则：内容驱动，真相验证，精准映射
**每个UML图表必须完全基于对应JSON文件的content字段内容生成，严格通过source-truth.json验证，绝不能使用通用模板和编造技术！**

### 内容处理原则（增强版）
1. **source-truth验证优先**：生成前必须通过source-truth.json验证技术栈和架构合规性
2. **content字段精确解析**：PlantUML内容必须完全基于JSON文件中的content字段描述
3. **技术栈严格限制**：只能使用allowedBackend和allowedFrontend中明确列出的技术
4. **架构模式约束**：只能使用allowedPatterns中的架构模式，严禁微服务等禁用架构
5. **真实模块映射**：只能引用actualModules中确实存在的功能模块
6. **实体关系验证**：数据库相关图表只能使用entities中的真实表结构
7. **避免过度设计**：严禁添加source-truth.json中未定义的任何技术组件

### 🔍 不同图表类型的content解析策略

#### Activity Diagram（活动图）
- **解析重点**：从content中提取具体的操作步骤、决策点、条件分支
- **生成要求**：
  - 每个活动节点对应content中描述的具体操作
  - 决策菱形反映content中的判断条件
  - 分支路径体现content中的不同业务场景
  - 错误处理对应content中的异常情况描述

#### Sequence Diagram（时序图）
- **解析重点**：从content中识别参与者、交互顺序、消息传递过程
- **生成要求**：
  - 参与者基于content中提到的系统组件或角色
  - 消息序列严格按照content描述的交互流程
  - 激活框反映content中的处理时间段
  - 返回消息对应content中的响应和结果

#### Use Case Diagram（用例图）
- **解析重点**：从content中识别用户角色、功能用例、系统边界
- **生成要求**：
  - 角色基于content中明确提到的用户类型
  - 用例对应content中描述的具体功能
  - 关系反映content中的依赖和扩展描述

#### Architecture Diagram（架构图）
- **解析重点**：从content中提取系统层次、组件关系、技术选型
- **生成要求**：
  - 组件基于content中明确提到的技术栈和模块
  - 层次结构反映content中的架构设计理念
  - 连接关系对应content中的交互和依赖描述

#### ER Diagram（实体关系图）
- **解析重点**：从content中识别实体、属性、关系约束
- **生成要求**：
  - 实体基于源码中的实际数据库表结构
  - 关系反映content中描述的业务关联
  - 约束对应content中的数据一致性要求

### 命名规范
- **类名**：使用源码中的实际类名（如UserController、UserService）
- **方法名**：使用实际的方法签名（如authenticateUser、findByUsername）
- **流程节点**：直接使用content中的业务描述文字
- **参与者**：使用content中提到的具体角色或系统组件名称
- **实体名**：使用源码entity目录中的实际实体类名

### 颜色和样式规范
- **活动图**：蓝色系（#E1F5FE背景，#0277BD边框）
- **架构图**：中性色（白色背景，矩形组件）
- **用例图**：绿色系（#E8F5E8背景，#2E7D32边框）
- **时序图**：蓝色系（#E1F5FE背景，#0277BD箭头和边框）
- **类图**：紫色系（#F3E5F5背景，#7B1FA2边框）

### 图表清晰度要求
- **直线布局**：优先使用直线连接，避免弯曲和混乱的布线
- **对齐排列**：元素按网格对齐，保持整齐的视觉效果
- **简洁明了**：避免过多装饰，突出核心信息和流程
- **统一间距**：保持一致的元素间距和边距
- **清晰标签**：使用简洁明确的标签和说明文字

## 执行流程

### Phase 1: 批量扫描与分类
1. **全量扫描**：递归扫描paper/pngs目录下**每一个JSON文件**，确保100%覆盖无遗漏
2. **字段解析**：读取每个文件的content、imagePath、imagePathSequence和tablePath字段
3. **类型识别**：根据文件名模式自动识别图表类型
4. **智能过滤**：仅排除entity-*和implementation-*类型，**保留er-overview整体ER图**
5. **分批组织**：将符合条件的文件按类型分组，准备批处理

### Phase 2: 源码真相分析与验证
1. **加载真相文件**：读取并解析`<projectRoot>/paper/source-truth.json`文件
2. **技术栈白名单**：加载允许的后端、前端技术和架构模式清单
3. **禁用技术黑名单**：加载严禁使用的技术和过度设计模式
4. **真实模块清单**：获取项目中实际存在的功能模块和数据实体
5. **源码结构验证**：验证source-truth.json与实际源码的一致性
6. **业务映射约束**：在允许的技术范围内理解业务需求和流程

### Phase 3: 受限PlantUML内容生成（防编造增强版）
1. **预验证检查**：基于source-truth.json验证content中提到的技术是否在允许清单中
2. **深度内容解析**：逐字分析每个JSON文件的content字段，提取关键业务流程和操作步骤
3. **技术栈合规检查**：确保所有技术组件都在allowedBackend/allowedFrontend范围内
4. **架构模式验证**：检查架构设计是否符合allowedPatterns，拒绝微服务等禁用模式
5. **真实模块映射**：只使用actualModules中确实存在的功能模块，拒绝编造模块
6. **实体关系验证**：数据库图表只能引用entities中的真实表和字段
7. **个性化图表生成**：在验证通过的前提下，为每个JSON文件生成符合业务场景的PlantUML源码
8. **双图协同生成**：对详细设计，基于同一content和相同技术约束生成相互呼应的活动图和时序图
9. **最终合规检查**：检查生成的PlantUML是否包含prohibitedTechnologies中的任何内容
10. **测试用例表生成**：对test-*、perf-*、compat-*类型文件，基于content生成对应的三线表JSON
11. **质量验证保存**：验证生成的PlantUML语法正确性和技术合规性，保存到plantuml目录；验证三线表格式正确性，保存到tables目录

#### 🎯 关键生成策略（防编造增强版）
- **source-truth强制约束**：所有图表内容必须严格符合source-truth.json的技术限制
- **避免模板复用**：每个图表都基于特定content生成，不使用通用模板
- **业务逻辑准确性**：确保UML图表准确反映content描述的业务流程
- **技术实现一致性**：图表中的技术细节与源码实现和允许清单保持一致
- **架构设计约束**：严禁出现微服务、分布式等禁用架构模式
- **模块存在性验证**：只能引用actualModules中确实存在的功能模块
- **图表互补性**：活动图展示业务流程，时序图展示系统交互，两者内容呼应但视角不同且技术栈一致
- **测试真实性**：测试用例必须基于实际功能模块，测试数据反映真实业务场景

### Phase 4: 批量图片渲染
1. **并行渲染**：使用luban-uml工具批量渲染PNG/SVG格式
2. **智能命名**：按照imagePath或imagePathSequence字段指定的文件名保存
3. **质量检查**：验证生成图片的完整性和清晰度
4. **报告生成**：生成详细的处理报告和统计信息

### Phase 5: 结果整理与反馈
1. **文件统计**：统计处理成功、失败和跳过的文件数量
2. **错误处理**：记录和分析处理失败的原因
3. **质量评估**：检查生成图表的视觉效果和信息完整性
4. **建议输出**：提供后续改进和调整的建议

## 容错机制
- **文件不存在**：跳过并记录到skippedFiles
- **PlantUML语法错误**：记录错误信息，继续处理其他文件
- **渲染失败**：重试一次，失败则记录到failedFiles
- **输出目录不存在**：自动创建目录结构

## 使用场景
- 论文图表自动化生成
- 系统设计文档可视化
- 代码架构图自动生成
- 技术文档图表更新

## 前置条件
- 执行前确保在项目根目录下运行
- paper/pngs目录存在且包含JSON文件
- source目录包含源码文件
- 网络连接正常（PlantUML在线服务）

## 批量处理实现

### 类似chapter-batch-processor的批处理架构
采用类似chapter-batch-processor的设计模式，实现UML图表的智能批量生成：

1. **文件发现与分组**：
   - 扫描paper/pngs目录，按图表类型自动分组
   - 识别双图字段（imagePath + imagePathSequence）
   - 过滤排除单体实体图和实现图，保留整体ER图

2. **批处理队列管理**：
   - 按依赖关系排序处理顺序
   - 并行处理无依赖的图表类型
   - 实时监控处理进度和错误状态

3. **智能错误恢复**：
   - 失败重试机制（最多3次）
   - 部分失败继续处理机制
   - 详细错误日志和诊断信息

4. **进度反馈与报告**：
   - 实时显示处理进度百分比
   - 生成详细的成功/失败统计报告
   - 提供后续调整建议

### 批处理命令示例
```bash
# 批量生成所有UML图表
./uml-batch-generator.sh

# 仅生成特定类型图表
./uml-batch-generator.sh --type activity,sequence,usecase

# 重新生成失败的图表
./uml-batch-generator.sh --retry-failed

# 清理并重新生成所有图表
./uml-batch-generator.sh --clean --regenerate
```

## 下一步流程
生成完成后，可以：
1. 将图片嵌入到论文文档中
2. 使用thesis-to-docx工具生成完整的Word文档
3. 根据需要调整PlantUML源码重新生成
4. 使用批处理模式定期更新所有图表