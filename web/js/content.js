// 内容编辑器功能

class ContentEditor {
    constructor() {
        this.content = null;
        this.currentSection = null;
        this.currentTab = 'plan';
        this.isDirty = false;
        this.init();
    }

    init() {
        this.bindEvents();
    }

    // 绑定事件
    bindEvents() {
        // 项目选择器变化
        document.getElementById('current-project-content').addEventListener('change', (e) => {
            if (e.target.value) {
                this.loadProjectContent(e.target.value);
            }
        });

        // 保存按钮
        document.getElementById('btn-save-content').addEventListener('click', () => {
            this.saveContent();
        });

        // 选项卡切换
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // 键盘快捷键
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                if (e.key === 's') {
                    e.preventDefault();
                    this.saveContent();
                }
            }
        });
    }

    // 加载项目内容
    loadProjectContent(projectId) {
        const project = projectManager.setCurrentProject(projectId);
        if (!project) {
            utils.showMessage('项目不存在', 'error');
            return;
        }

        // 如果项目有内容数据，加载它；否则使用模板
        this.content = project.content || utils.deepClone(projectManager.templates.content);

        // 如果有大纲数据，同步章节
        if (project.outline) {
            this.syncSectionsFromOutline(project.outline);
        }

        this.renderSectionSidebar();
        this.isDirty = false;

        utils.showMessage(`已加载项目 "${project.name}" 的内容`, 'success');
    }

    // 从大纲同步章节
    syncSectionsFromOutline(outline) {
        const sections = this.extractSectionsFromOutline(outline.nodes);

        // 为新章节创建内容条目
        sections.forEach(section => {
            if (!this.content.contents[section.id]) {
                this.content.contents[section.id] = this.createDefaultSectionContent(section);
            } else {
                // 更新标题
                this.content.contents[section.id].sectionTitle = section.title;
            }
        });

        // 移除不存在的章节
        Object.keys(this.content.contents).forEach(sectionId => {
            if (sectionId !== '__TEMPLATE_PER_SECTION__' &&
                !sections.find(s => s.id === sectionId)) {
                delete this.content.contents[sectionId];
            }
        });
    }

    // 从大纲节点提取章节
    extractSectionsFromOutline(nodes, sections = []) {
        nodes.forEach(node => {
            sections.push({
                id: node.id,
                title: node.title
            });

            if (node.children) {
                this.extractSectionsFromOutline(node.children, sections);
            }
        });

        return sections;
    }

    // 创建默认章节内容
    createDefaultSectionContent(section) {
        const template = this.content.contents['__TEMPLATE_PER_SECTION__'] || {};

        return {
            status: 'planning',
            sectionTitle: section.title,
            length: template.length || { unit: 'char', target: 900 },
            plan: {
                wantText: true,
                wantFigure: false,
                figurePlan: [],
                wantTable: false,
                tablePlan: []
            },
            text: '',
            textPrompt: this.generateDefaultTextPrompt(section.title),
            figures: [],
            tables: []
        };
    }

    // 生成默认文本提示词
    generateDefaultTextPrompt(sectionTitle) {
        const defaults = this.content.defaults || {};
        const template = defaults.textPromptTemplate ||
            '撰写《{{sectionTitle}}》，围绕"{{论文主题}}"，结合源码结构、关键模块与数据流，语言学术化，避免口语化。';

        return template
            .replace('{{sectionTitle}}', sectionTitle)
            .replace('{{论文主题}}', this.content.meta?.theme || '系统开发');
    }

    // 渲染章节侧栏
    renderSectionSidebar() {
        const sidebar = document.getElementById('section-sidebar');

        if (!this.content || !this.content.contents) {
            sidebar.innerHTML = '<p>暂无内容数据</p>';
            return;
        }

        const sections = Object.keys(this.content.contents)
            .filter(key => key !== '__TEMPLATE_PER_SECTION__')
            .map(key => ({
                id: key,
                ...this.content.contents[key]
            }))
            .sort((a, b) => {
                // 简单的数字排序
                const aNum = parseFloat(a.id);
                const bNum = parseFloat(b.id);
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return aNum - bNum;
                }
                return a.id.localeCompare(b.id);
            });

        sidebar.innerHTML = `
            <h3>章节列表</h3>
            <div class="section-list">
                ${sections.map(section => `
                    <div class="section-item ${section.id === this.currentSection ? 'active' : ''}"
                         onclick="contentEditor.selectSection('${section.id}')">
                        <div class="section-status ${section.status || 'planning'}"></div>
                        <div class="section-id">${section.id}</div>
                        <div class="section-title">${section.sectionTitle || section.title || '未命名章节'}</div>
                    </div>
                `).join('')}
            </div>
            <div class="section-actions">
                <button class="btn btn-sm" onclick="contentEditor.addSection()">➕ 添加章节</button>
                <button class="btn btn-sm" onclick="contentEditor.batchEdit()">📝 批量编辑</button>
            </div>
        `;
    }

    // 选择章节
    selectSection(sectionId) {
        this.currentSection = sectionId;
        this.renderSectionSidebar();
        this.renderSectionEditor();
    }

    // 渲染章节编辑器
    renderSectionEditor() {
        const editorContainer = document.getElementById('section-editor');

        if (!this.currentSection || !this.content.contents[this.currentSection]) {
            editorContainer.innerHTML = `
                <div class="no-selection">
                    <h3>请选择章节</h3>
                    <p>从左侧章节列表中选择要编辑的章节</p>
                </div>
            `;
            return;
        }

        const section = this.content.contents[this.currentSection];

        editorContainer.innerHTML = `
            <div class="section-header">
                <h3>${section.sectionTitle || '未命名章节'} (${this.currentSection})</h3>
                <div class="section-meta">
                    <span class="status-badge ${section.status}">${this.getStatusText(section.status)}</span>
                    <span class="length-info">目标字数: ${section.length?.target || 900}</span>
                </div>
            </div>

            <div class="section-tabs">
                <button class="tab-btn ${this.currentTab === 'plan' ? 'active' : ''}"
                        onclick="contentEditor.switchTab('plan')">📋 计划</button>
                <button class="tab-btn ${this.currentTab === 'text' ? 'active' : ''}"
                        onclick="contentEditor.switchTab('text')">📝 正文</button>
                <button class="tab-btn ${this.currentTab === 'figures' ? 'active' : ''}"
                        onclick="contentEditor.switchTab('figures')">🖼️ 图表</button>
                <button class="tab-btn ${this.currentTab === 'tables' ? 'active' : ''}"
                        onclick="contentEditor.switchTab('tables')">📊 表格</button>
            </div>

            <div class="tab-content" id="tab-content">
                ${this.renderTabContent()}
            </div>
        `;
    }

    // 切换选项卡
    switchTab(tab) {
        this.currentTab = tab;
        this.renderSectionEditor();
    }

    // 渲染选项卡内容
    renderTabContent() {
        const section = this.content.contents[this.currentSection];

        switch (this.currentTab) {
            case 'plan':
                return this.renderPlanTab(section);
            case 'text':
                return this.renderTextTab(section);
            case 'figures':
                return this.renderFiguresTab(section);
            case 'tables':
                return this.renderTablesTab(section);
            default:
                return '<p>未知选项卡</p>';
        }
    }

    // 渲染计划选项卡
    renderPlanTab(section) {
        const plan = section.plan || {};

        return `
            <div class="plan-editor">
                <div class="plan-section">
                    <h4>正文设置</h4>
                    <div class="plan-toggle">
                        <input type="checkbox" id="want-text" ${plan.wantText ? 'checked' : ''}
                               onchange="contentEditor.updatePlan('wantText', this.checked)">
                        <label for="want-text">生成正文内容</label>
                    </div>
                    <div class="form-group">
                        <label>目标字数:</label>
                        <input type="number" value="${section.length?.target || 900}"
                               onchange="contentEditor.updateLength(this.value)">
                    </div>
                </div>

                <div class="plan-section">
                    <h4>图表设置</h4>
                    <div class="plan-toggle">
                        <input type="checkbox" id="want-figure" ${plan.wantFigure ? 'checked' : ''}
                               onchange="contentEditor.updatePlan('wantFigure', this.checked)">
                        <label for="want-figure">生成图表</label>
                    </div>
                    <div class="plan-list" ${plan.wantFigure ? '' : 'style="display: none;"'}>
                        ${this.renderFigurePlan(plan.figurePlan || [])}
                        <button class="plan-add-btn" onclick="contentEditor.addFigurePlan()">➕ 添加图表</button>
                    </div>
                </div>

                <div class="plan-section">
                    <h4>表格设置</h4>
                    <div class="plan-toggle">
                        <input type="checkbox" id="want-table" ${plan.wantTable ? 'checked' : ''}
                               onchange="contentEditor.updatePlan('wantTable', this.checked)">
                        <label for="want-table">生成表格</label>
                    </div>
                    <div class="plan-list" ${plan.wantTable ? '' : 'style="display: none;"'}>
                        ${this.renderTablePlan(plan.tablePlan || [])}
                        <button class="plan-add-btn" onclick="contentEditor.addTablePlan()">➕ 添加表格</button>
                    </div>
                </div>
            </div>
        `;
    }

    // 渲染图表计划
    renderFigurePlan(figurePlan) {
        return figurePlan.map((figure, index) => `
            <div class="plan-item">
                <div class="plan-item-header">
                    <input type="checkbox" class="plan-item-enabled" ${figure.enabled ? 'checked' : ''}
                           onchange="contentEditor.updateFigurePlan(${index}, 'enabled', this.checked)">
                    <input type="text" class="plan-item-title" value="${figure.figureTitle || ''}"
                           placeholder="图表标题"
                           onchange="contentEditor.updateFigurePlan(${index}, 'figureTitle', this.value)">
                    <button class="plan-item-remove" onclick="contentEditor.removeFigurePlan(${index})">删除</button>
                </div>
                <textarea class="plan-item-focus" placeholder="图表重点描述"
                          onchange="contentEditor.updateFigurePlan(${index}, 'figureFocus', this.value)">${figure.figureFocus || ''}</textarea>
            </div>
        `).join('');
    }

    // 渲染表格计划
    renderTablePlan(tablePlan) {
        return tablePlan.map((table, index) => `
            <div class="plan-item">
                <div class="plan-item-header">
                    <input type="checkbox" class="plan-item-enabled" ${table.enabled ? 'checked' : ''}
                           onchange="contentEditor.updateTablePlan(${index}, 'enabled', this.checked)">
                    <input type="text" class="plan-item-title" value="${table.tableTitle || ''}"
                           placeholder="表格标题"
                           onchange="contentEditor.updateTablePlan(${index}, 'tableTitle', this.value)">
                    <button class="plan-item-remove" onclick="contentEditor.removeTablePlan(${index})">删除</button>
                </div>
                <textarea class="plan-item-schema" placeholder="表格字段（逗号分隔）"
                          onchange="contentEditor.updateTablePlan(${index}, 'schema', this.value.split(','))">${(table.schema || []).join(',')}</textarea>
            </div>
        `).join('');
    }

    // 渲染正文选项卡
    renderTextTab(section) {
        return `
            <div class="text-editor-container">
                <div class="text-prompt">
                    <h4>提示词</h4>
                    <textarea id="text-prompt" placeholder="输入正文生成提示词..."
                              onchange="contentEditor.updateTextPrompt(this.value)">${section.textPrompt || ''}</textarea>
                </div>

                <div class="text-stats">
                    <div>
                        <span>当前字数: <strong>${(section.text || '').length}</strong></span>
                        <span>目标字数: <strong>${section.length?.target || 900}</strong></span>
                    </div>
                    <div>
                        <button class="btn btn-sm" onclick="contentEditor.generateText()">🤖 生成正文</button>
                    </div>
                </div>

                <div class="text-editor">
                    <textarea id="section-text" placeholder="正文内容将在此显示..."
                              onchange="contentEditor.updateText(this.value)">${section.text || ''}</textarea>
                </div>
            </div>
        `;
    }

    // 渲染图表选项卡
    renderFiguresTab(section) {
        const figures = section.figures || [];

        return `
            <div class="figures-container">
                <div class="figures-header">
                    <h4>图表列表</h4>
                    <button class="btn btn-sm" onclick="contentEditor.generateFigures()">🖼️ 生成图表</button>
                </div>

                <div class="figure-list">
                    ${figures.length === 0 ? '<p>暂无图表</p>' : figures.map((figure, index) => `
                        <div class="figure-item">
                            <div class="figure-header">
                                <span class="figure-label">${figure.label || `图${index + 1}`}</span>
                                <span class="figure-status ${figure.status || 'pending'}">${this.getStatusText(figure.status)}</span>
                            </div>
                            ${figure.imagePath ? `<img src="${figure.imagePath}" class="figure-preview" alt="${figure.label}">` : ''}
                            ${figure.error ? `<div class="error-message">${figure.error}</div>` : ''}
                            <div class="figure-actions">
                                <button class="btn btn-sm" onclick="contentEditor.regenerateFigure(${index})">🔄 重新生成</button>
                                <button class="btn btn-sm" onclick="contentEditor.deleteFigure(${index})">🗑️ 删除</button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // 渲染表格选项卡
    renderTablesTab(section) {
        const tables = section.tables || [];

        return `
            <div class="tables-container">
                <div class="tables-header">
                    <h4>表格列表</h4>
                    <button class="btn btn-sm" onclick="contentEditor.generateTables()">📊 生成表格</button>
                </div>

                <div class="table-list">
                    ${tables.length === 0 ? '<p>暂无表格</p>' : tables.map((table, index) => `
                        <div class="table-item">
                            <div class="table-header">
                                <span class="table-label">${table.label || `表${index + 1}`}</span>
                                <span class="table-status ${table.status || 'pending'}">${this.getStatusText(table.status)}</span>
                            </div>
                            ${table.data ? this.renderTablePreview(table.data) : ''}
                            ${table.error ? `<div class="error-message">${table.error}</div>` : ''}
                            <div class="table-actions">
                                <button class="btn btn-sm" onclick="contentEditor.regenerateTable(${index})">🔄 重新生成</button>
                                <button class="btn btn-sm" onclick="contentEditor.deleteTable(${index})">🗑️ 删除</button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // 渲染表格预览
    renderTablePreview(data) {
        if (!data || !data.headers || !data.rows) return '';

        return `
            <div class="table-preview">
                <table>
                    <thead>
                        <tr>
                            ${data.headers.map(header => `<th>${header}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${data.rows.map(row => `
                            <tr>
                                ${row.map(cell => `<td>${cell}</td>`).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    // 获取状态文本
    getStatusText(status) {
        const statusMap = {
            planning: '规划中',
            generated: '已生成',
            partial: '部分完成',
            failed: '生成失败',
            pending: '待生成',
            success: '成功',
            error: '错误'
        };
        return statusMap[status] || status;
    }

    // 更新计划
    updatePlan(field, value) {
        if (!this.currentSection) return;

        const section = this.content.contents[this.currentSection];
        if (!section.plan) section.plan = {};

        section.plan[field] = value;
        this.markDirty();

        // 重新渲染以显示/隐藏相关选项
        this.renderSectionEditor();
    }

    // 更新长度设置
    updateLength(target) {
        if (!this.currentSection) return;

        const section = this.content.contents[this.currentSection];
        if (!section.length) section.length = { unit: 'char' };

        section.length.target = parseInt(target) || 900;
        this.markDirty();
    }

    // 添加图表计划
    addFigurePlan() {
        if (!this.currentSection) return;

        const section = this.content.contents[this.currentSection];
        if (!section.plan.figurePlan) section.plan.figurePlan = [];

        section.plan.figurePlan.push({
            enabled: true,
            figureTitle: '',
            figureFocus: '',
            schema: null,
            promptTemplate: this.content.defaults?.figurePromptTemplate || ''
        });

        this.markDirty();
        this.renderSectionEditor();
    }

    // 更新图表计划
    updateFigurePlan(index, field, value) {
        if (!this.currentSection) return;

        const section = this.content.contents[this.currentSection];
        if (section.plan.figurePlan && section.plan.figurePlan[index]) {
            section.plan.figurePlan[index][field] = value;
            this.markDirty();
        }
    }

    // 删除图表计划
    removeFigurePlan(index) {
        if (!this.currentSection) return;

        const section = this.content.contents[this.currentSection];
        if (section.plan.figurePlan) {
            section.plan.figurePlan.splice(index, 1);
            this.markDirty();
            this.renderSectionEditor();
        }
    }

    // 添加表格计划
    addTablePlan() {
        if (!this.currentSection) return;

        const section = this.content.contents[this.currentSection];
        if (!section.plan.tablePlan) section.plan.tablePlan = [];

        section.plan.tablePlan.push({
            enabled: true,
            tableTitle: '',
            schema: [],
            promptTemplate: this.content.defaults?.tablePromptTemplate || ''
        });

        this.markDirty();
        this.renderSectionEditor();
    }

    // 更新表格计划
    updateTablePlan(index, field, value) {
        if (!this.currentSection) return;

        const section = this.content.contents[this.currentSection];
        if (section.plan.tablePlan && section.plan.tablePlan[index]) {
            section.plan.tablePlan[index][field] = value;
            this.markDirty();
        }
    }

    // 删除表格计划
    removeTablePlan(index) {
        if (!this.currentSection) return;

        const section = this.content.contents[this.currentSection];
        if (section.plan.tablePlan) {
            section.plan.tablePlan.splice(index, 1);
            this.markDirty();
            this.renderSectionEditor();
        }
    }

    // 更新文本提示词
    updateTextPrompt(prompt) {
        if (!this.currentSection) return;

        const section = this.content.contents[this.currentSection];
        section.textPrompt = prompt;
        this.markDirty();
    }

    // 更新正文内容
    updateText(text) {
        if (!this.currentSection) return;

        const section = this.content.contents[this.currentSection];
        section.text = text;
        this.markDirty();
    }

    // 生成正文（占位功能）
    generateText() {
        utils.showMessage('生成正文功能将在执行控制台中实现', 'info');
    }

    // 生成图表（占位功能）
    generateFigures() {
        utils.showMessage('生成图表功能将在执行控制台中实现', 'info');
    }

    // 生成表格（占位功能）
    generateTables() {
        utils.showMessage('生成表格功能将在执行控制台中实现', 'info');
    }

    // 标记为已修改
    markDirty() {
        this.isDirty = true;
        document.getElementById('btn-save-content').textContent = '💾 保存内容 *';
    }

    // 保存内容
    saveContent() {
        const project = projectManager.getCurrentProject();
        if (!project) {
            utils.showMessage('请先选择项目', 'error');
            return;
        }

        if (!this.content) {
            utils.showMessage('无内容数据可保存', 'error');
            return;
        }

        project.content = utils.deepClone(this.content);

        if (projectManager.saveProject(project)) {
            this.isDirty = false;
            document.getElementById('btn-save-content').textContent = '💾 保存内容';
            utils.showMessage('内容保存成功', 'success');
        } else {
            utils.showMessage('保存失败', 'error');
        }
    }
}

// 创建全局实例
window.contentEditor = new ContentEditor();