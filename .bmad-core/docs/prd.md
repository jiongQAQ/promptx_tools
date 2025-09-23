# 📄 论文生成与导出系统 PRD

## 1. 项目目标
1. 搭建一个支持「论文大纲 → 内容生成 → 图表生成 → Word 导出」的完整流水线。
2. 大纲（目录结构）与章节内容解耦，保持数据一致性。
3. 支持 AI 自动生成正文、UML 图代码、三线表数据。
4. 提供全局资料库：资料只需上传一次，章节里引用 fileId + 描述词即可。
5. 支持上下文合成：选择资料、勾选上下文章节，拼接成生成输入。
6. 支持单章节重新生成，可修改 Prompt、上下文和资料。
7. 生成失败（如 UML 语法错误）不影响整体导出，Word 中用占位符标注。
8. 使用工作流配置 JSON 描述生成步骤，运行时记录状态 JSON，用于展示执行进度与错误。

---

## 2. 系统流程

1. **资料上传**
    - 文件上传到资料库（files.json），自动生成摘要 bullets 和默认调用说明。

2. **大纲编辑**
    - 编辑树形大纲（outline.json），新增/修改/删除章节。
    - 系统自动同步 content.json，保证章节内容结构和大纲一致。

3. **章节编辑**
    - 正文：设置 Prompt、目标字数，勾选资料和上下文章节 → AI 生成。
    - 图：填写 UML Prompt → AI 生成 UML 代码 → 渲染器生成 PNG/SVG → 写入 content.json。
    - 表：填写表格 Prompt 或解析 SQL → AI 或工具生成三线表数据。
    - 资料：从资料库引用 fileId + 描述词，不需重复上传。

4. **执行生成**
    - 根据 workflow.json 定义的步骤，批量或单章节执行。
    - 执行过程记录到 workflow-status.json，包括成功/失败/耗时/错误信息。

5. **导出 Word**
    - 系统打包 outline.json + content.json → manifest.json（导出清单）。
    - Word 生成器根据 manifest.json 渲染 DOCX，应用统一样式。
    - 即使有图表失败，也会导出占位符和错误提示。

---

## 3. 页面设计

### 页面 A：资料库
1. 文件上传、预览、删除。
2. 自动生成摘要 bullets，可手动编辑。
3. 编辑默认调用说明（descriptor）。
4. 标签管理，支持搜索/过滤。

### 页面 B：大纲编辑
1. 左侧：树形结构，可增删改拖拽，自动编号。
2. 右侧：节点标题编辑。
3. 保存：写入 outline.json，并同步更新 content.json。

### 页面 C：章节内容
Tabs：
1. **正文**
    - 输入目标字数。
    - 选择资料（多选）+ 描述词。
    - 勾选上下文章节。
    - 按钮：【生成正文】【重新生成】。
2. **资料**
    - 显示引用的资料（fileId、descriptor）。
    - 可批量引用资料到多个章节。
3. **图（UML）**
    - 每个图配置 label、umlPrompt。
    - 按钮：【生成代码】【渲染】【重新生成】。
    - 失败时显示错误信息。
4. **表（三线表）**
    - 每个表配置 label、dataPrompt、schema。
    - 按钮：【解析 SQL】【生成数据】【重新生成】。
    - 表格数据可人工修改。
5. **上下文设置**
    - 勾选祖先/同级/前文/附件章节。
    - 调整优先级。
    - 预览上下文块。

### 页面 D：导出
1. 显示 workflow.json 配置。
2. 显示 workflow-status.json 执行日志。
3. 按钮：【dry-run 检查】【执行工作流】【导出 DOCX】。

---

## 4. JSON 文档

1. **outline.json**：存树形大纲（章节 ID、标题、子节点）。
2. **content.json**：存每章正文、图表、资料引用、上下文设置。
3. **files.json**：全局资料库（文件元数据、摘要、默认调用说明）。
4. **manifest.json**：导出清单（拍平所有章节的正文/图/表 + 样式）。
5. **workflow.json**：工作流定义（步骤顺序、AI 调用点、并发/重试）。
6. **workflow-status.json**：执行日志（每步成功/失败/耗时/错误）。

---

## 5. 工具清单

### AI 工具
1. `/generate/text`：生成正文。
2. `/generate/uml`：生成 UML 代码。
3. `/generate/table`：生成三线表数据。

### 解析/渲染工具
1. `/tools/sql-to-single-er`：单表 ER 图解析。
2. `/tools/sql-to-three-line`：三线表解析。
3. `/tools/sql-to-er-summary`：数据库整体 ER 摘要。
4. `/tools/render-uml`：PlantUML/Mermaid 渲染 PNG/SVG。

### 工作流工具
1. `/context/compose`：上下文合成（资料+章节摘要）。
2. `/workflow/run`：执行 workflow.json。
3. `/workflow/status/:runId`：查询运行日志。
4. `/workflow/retry`：重试失败步骤。

---

## 6. 容错与重试

1. **正文失败**：保留原文，不覆盖；前端提示“生成失败”。
2. **图失败**：标记 status=failed + errorMessage，Word 中插入占位符。
3. **表失败**：同样插入表占位符，提示“生成失败”。
4. **整体导出不阻塞**：即使部分失败，manifest.json 仍可生成。
5. **重试机制**：单章节、单图表可重新执行，覆盖旧结果。

---

## 7. 整体使用逻辑

1. 资料上传 → 写入 files.json。
2. 编辑大纲 → 写入 outline.json。
3. 编辑章节 → 写入 content.json。
4. 执行工作流 → workflow-status.json 记录状态。
5. 导出清单 → manifest.json。
6. Word 生成器 → 根据 manifest.json 输出 DOCX。  