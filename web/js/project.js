// 项目管理功能

class ProjectManager {
    constructor() {
        this.projects = utils.Storage.get('projects', []);
        this.currentProject = null;
        this.templates = {};
        this.init();
    }

    init() {
        this.loadTemplates();
        this.bindEvents();
        this.renderProjectList();
    }

    // 加载模板
    async loadTemplates() {
        try {
            console.log('正在加载模板文件...');

            // 加载大纲模板
            const outlineResponse = await fetch('/templates/outline.template.json');
            if (!outlineResponse.ok) {
                throw new Error(`无法加载大纲模板: HTTP ${outlineResponse.status}`);
            }

            const outlineText = await outlineResponse.text();
            if (outlineText.startsWith('<!DOCTYPE')) {
                throw new Error('大纲模板返回了HTML页面而不是JSON文件');
            }

            this.templates.outline = JSON.parse(outlineText);

            // 加载内容模板
            const contentResponse = await fetch('/templates/content.template.json');
            if (!contentResponse.ok) {
                throw new Error(`无法加载内容模板: HTTP ${contentResponse.status}`);
            }

            const contentText = await contentResponse.text();
            if (contentText.startsWith('<!DOCTYPE')) {
                throw new Error('内容模板返回了HTML页面而不是JSON文件');
            }

            this.templates.content = JSON.parse(contentText);

            console.log('✅ 模板加载成功');
            utils.showMessage('模板加载成功', 'success');

        } catch (error) {
            console.error('❌ 模板加载失败:', error);
            utils.showMessage(`模板加载失败: ${error.message}`, 'error');

            // 不提供后备方案，要求用户修复问题
            throw error;
        }
    }

    // 绑定事件
    bindEvents() {
        // 新建项目按钮
        document.getElementById('btn-new-project').addEventListener('click', () => {
            this.showNewProjectModal();
        });

        // 新建项目表单
        document.getElementById('new-project-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.createProject();
        });

        // 文件上传区域
        this.setupFileUpload();

        // 刷新模板按钮
        document.getElementById('btn-refresh-templates').addEventListener('click', () => {
            this.loadTemplates();
        });
    }

    // 设置文件上传
    setupFileUpload() {
        const dropZone = document.getElementById('file-drop-zone');
        const fileInput = document.getElementById('source-file');

        // 点击上传
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });

        // 文件选择
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileSelect(e.target.files[0]);
            }
        });

        // 拖拽上传
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');

            if (e.dataTransfer.files.length > 0) {
                this.handleFileSelect(e.dataTransfer.files[0]);
            }
        });
    }

    // 处理文件选择
    handleFileSelect(file) {
        if (file.type !== 'application/zip' && !file.name.endsWith('.zip')) {
            utils.showMessage('请选择ZIP文件', 'error');
            return;
        }

        const dropZone = document.getElementById('file-drop-zone');
        dropZone.innerHTML = `
            <p>📁 ${file.name}</p>
            <p>${utils.formatFileSize(file.size)}</p>
        `;

        // 存储文件引用
        this.selectedFile = file;
    }

    // 显示新建项目模态框
    showNewProjectModal() {
        utils.showModal('new-project-modal');
    }

    // 创建项目
    async createProject() {
        const projectName = document.getElementById('project-name').value.trim();
        const paperTitle = document.getElementById('paper-title').value.trim();
        const paperTheme = document.getElementById('paper-theme').value.trim();
        const templateSelect = document.getElementById('template-select').value;

        // 验证项目名称
        const nameError = utils.validateProjectName(projectName);
        if (nameError) {
            utils.showMessage(nameError, 'error');
            return;
        }

        // 检查项目是否已存在
        if (this.projects.find(p => p.name === projectName)) {
            utils.showMessage('项目名称已存在', 'error');
            return;
        }

        // 检查是否选择了文件
        if (!this.selectedFile) {
            utils.showMessage('请选择源码文件', 'error');
            return;
        }

        utils.showLoading('创建项目中...');

        try {
            // 创建项目对象
            const project = {
                id: utils.generateUUID(),
                name: projectName,
                title: paperTitle || `${projectName}系统设计与实现`,
                theme: paperTheme || '系统开发',
                template: templateSelect,
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
                status: 'planning',
                sourceFile: this.selectedFile.name,
                sourceSize: this.selectedFile.size
            };

            // 解压源码文件
            await this.extractSourceCode(project, this.selectedFile);

            // 复制模板文件
            await this.copyTemplates(project);

            // 保存项目
            this.projects.push(project);
            utils.Storage.set('projects', this.projects);

            utils.hideLoading();
            utils.showMessage('项目创建成功', 'success');
            utils.closeModal('new-project-modal');

            // 重置表单
            document.getElementById('new-project-form').reset();
            document.getElementById('file-drop-zone').innerHTML = '<p>拖拽文件到此处或点击选择</p>';
            this.selectedFile = null;

            // 刷新项目列表
            this.renderProjectList();

        } catch (error) {
            console.error('Create project failed:', error);
            utils.hideLoading();
            utils.showMessage('创建项目失败: ' + error.message, 'error');
        }
    }

    // 解压源码文件
    async extractSourceCode(project, file) {
        const arrayBuffer = await utils.readFileAsArrayBuffer(file);
        const zip = new JSZip();

        try {
            const zipData = await zip.loadAsync(arrayBuffer);

            // 解压到项目的project目录下
            const projectPath = `./project/${project.name}`;
            const sourcePath = `${projectPath}/source`;

            console.log(`解压源码到: ${sourcePath}`);
            console.log('ZIP文件内容:', Object.keys(zipData.files));

            // 由于浏览器安全限制，这里只是模拟解压过程
            // 实际的文件解压需要用户手动操作或使用File System Access API
            project.extractPath = sourcePath;
            project.sourceStructure = Object.keys(zipData.files).map(path => ({
                path,
                isDirectory: zipData.files[path].dir,
                size: zipData.files[path]._data ? zipData.files[path]._data.uncompressedSize : 0
            }));

            // 生成解压指令
            project.extractInstructions = this.generateExtractInstructions(project, zipData);

        } catch (error) {
            throw new Error('解压文件失败: ' + error.message);
        }
    }

    // 生成解压指令
    generateExtractInstructions(project, zipData) {
        const projectPath = `./project/${project.name}`;
        const sourcePath = `${projectPath}/source`;
        const absoluteProjectPath = `/Users/pc/Documents/promptx_tools/web/project/${project.name}`;
        const absoluteSourcePath = `${absoluteProjectPath}/source`;

        return {
            steps: [
                `# 创建项目目录`,
                `mkdir -p "${absoluteProjectPath}"`,
                `mkdir -p "${absoluteSourcePath}"`,
                ``,
                `# 解压源码文件到项目目录`,
                `# 请将上传的 ${project.sourceFile} 解压到以下目录:`,
                `# ${absoluteSourcePath}/`,
                ``,
                `# 或使用命令行解压:`,
                `unzip "${project.sourceFile}" -d "${absoluteSourcePath}/"`
            ],
            targetPath: absoluteSourcePath,
            fileCount: Object.keys(zipData.files).length
        };
    }

    // 复制模板文件
    async copyTemplates(project) {
        // 复制大纲模板
        const outlineTemplate = utils.deepClone(this.templates.outline);
        if (project.title) {
            outlineTemplate.title = project.title;
        }

        // 复制内容模板
        const contentTemplate = utils.deepClone(this.templates.content);
        if (project.title && project.theme) {
            contentTemplate.meta.title = project.title;
            contentTemplate.meta.theme = project.theme;
        }

        // 保存到项目中（实际应该保存到文件系统）
        project.outline = outlineTemplate;
        project.content = contentTemplate;

        console.log('Templates copied for project:', project.name);
    }

    // 渲染项目列表
    renderProjectList() {
        const container = document.getElementById('project-list');

        if (this.projects.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>暂无项目</h3>
                    <p>点击"新建项目"开始创建您的第一个论文项目</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.projects.map(project => `
            <div class="project-card" data-project-id="${project.id}">
                <h3>📁 ${project.name}</h3>
                <div class="project-meta">
                    <p><strong>题目:</strong> ${project.title}</p>
                    <p><strong>主题:</strong> ${project.theme}</p>
                    <p><strong>创建时间:</strong> ${utils.formatDate(project.createdAt)}</p>
                    <p><strong>更新时间:</strong> ${utils.formatDate(project.updatedAt)}</p>
                    <p><strong>源码文件:</strong> ${project.sourceFile} (${utils.formatFileSize(project.sourceSize)})</p>
                    ${project.extractPath ? `<p><strong>解压路径:</strong> ${project.extractPath}</p>` : ''}
                </div>
                <div class="project-status ${project.status}">${this.getStatusText(project.status)}</div>
                <div class="project-actions">
                    ${project.extractInstructions ? `<button class="btn btn-sm" onclick="projectManager.showExtractInstructions('${project.id}')">📂 解压指令</button>` : ''}
                    <button class="btn btn-sm" onclick="projectManager.editOutline('${project.id}')">📝 编辑大纲</button>
                    <button class="btn btn-sm" onclick="projectManager.editContent('${project.id}')">📄 编辑内容</button>
                    <button class="btn btn-sm" onclick="projectManager.runConsole('${project.id}')">▶️ 执行</button>
                    <button class="btn btn-sm" onclick="projectManager.exportProject('${project.id}')">📤 导出</button>
                    <button class="btn btn-sm" onclick="projectManager.deleteProject('${project.id}')" style="background: #dc3545;">🗑️ 删除</button>
                </div>
            </div>
        `).join('');
    }

    // 显示解压指令
    showExtractInstructions(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (!project || !project.extractInstructions) {
            utils.showMessage('未找到解压指令', 'error');
            return;
        }

        const modal = document.getElementById('modal');
        const modalBody = document.getElementById('modal-body');

        modalBody.innerHTML = `
            <h3>📂 源码解压指令</h3>
            <p><strong>项目:</strong> ${project.name}</p>
            <p><strong>源码文件:</strong> ${project.sourceFile}</p>
            <p><strong>目标路径:</strong> ${project.extractInstructions.targetPath}</p>
            <p><strong>文件数量:</strong> ${project.extractInstructions.fileCount} 个</p>

            <h4>解压步骤:</h4>
            <pre class="command-box">${project.extractInstructions.steps.join('\n')}</pre>

            <div class="form-actions">
                <button class="btn" onclick="utils.closeModal('modal')">关闭</button>
                <button class="btn btn-primary" onclick="utils.copyToClipboard(\`${project.extractInstructions.steps.join('\\n')}\`); utils.showMessage('指令已复制', 'success')">📋 复制指令</button>
            </div>
        `;

        utils.showModal('modal');
    }

    // 获取状态文本
    getStatusText(status) {
        const statusMap = {
            planning: '规划中',
            generated: '已生成',
            partial: '部分完成',
            failed: '生成失败'
        };
        return statusMap[status] || status;
    }

    // 编辑大纲
    editOutline(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (!project) return;

        this.currentProject = project;
        utils.showMessage(`切换到项目: ${project.name}`, 'info');

        // 切换到大纲编辑页面
        window.app.switchPage('outline');

        // 更新项目选择器
        this.updateProjectSelectors();
    }

    // 编辑内容
    editContent(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (!project) return;

        this.currentProject = project;
        utils.showMessage(`切换到项目: ${project.name}`, 'info');

        // 切换到内容编辑页面
        window.app.switchPage('content');

        // 更新项目选择器
        this.updateProjectSelectors();
    }

    // 运行控制台
    runConsole(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (!project) return;

        this.currentProject = project;
        utils.showMessage(`切换到项目: ${project.name}`, 'info');

        // 切换到执行控制页面
        window.app.switchPage('console');

        // 更新项目选择器
        this.updateProjectSelectors();

        // 同步到执行器
        if (window.executor) {
            window.executor.loadProject(projectId);
        }
    }

    // 导出项目
    exportProject(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (!project) return;

        this.currentProject = project;
        utils.showMessage(`切换到项目: ${project.name}`, 'info');

        // 切换到导出页面
        window.app.switchPage('export');

        // 更新项目选择器
        this.updateProjectSelectors();
    }

    // 删除项目
    deleteProject(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (!project) return;

        utils.showConfirm(
            `确定要删除项目 "${project.name}" 吗？此操作不可恢复。`,
            () => {
                this.projects = this.projects.filter(p => p.id !== projectId);
                utils.Storage.set('projects', this.projects);
                this.renderProjectList();
                utils.showMessage('项目删除成功', 'success');
            }
        );
    }

    // 更新项目选择器
    updateProjectSelectors() {
        const selectors = [
            'current-project-outline',
            'current-project-content',
            'current-project-console',
            'current-project-export'
        ];

        selectors.forEach(selectorId => {
            const select = document.getElementById(selectorId);
            if (select) {
                select.innerHTML = '<option value="">选择项目...</option>' +
                    this.projects.map(project =>
                        `<option value="${project.id}" ${project.id === this.currentProject?.id ? 'selected' : ''}>
                            ${project.name} - ${project.title}
                        </option>`
                    ).join('');
            }
        });
    }

    // 获取当前项目
    getCurrentProject() {
        return this.currentProject;
    }

    // 设置当前项目
    setCurrentProject(projectId) {
        this.currentProject = this.projects.find(p => p.id === projectId);
        return this.currentProject;
    }

    // 保存项目数据
    saveProject(project) {
        const index = this.projects.findIndex(p => p.id === project.id);
        if (index !== -1) {
            project.updatedAt = new Date().toISOString();
            this.projects[index] = project;
            utils.Storage.set('projects', this.projects);
            return true;
        }
        return false;
    }
}

// 模板查看和编辑功能
function viewTemplate(templateType) {
    const template = projectManager.templates[templateType];
    if (!template) {
        utils.showMessage('模板不存在', 'error');
        return;
    }

    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');

    modalBody.innerHTML = `
        <h3>${templateType === 'outline' ? '大纲模板' : '内容模板'}</h3>
        <pre style="background: #f8f9fa; padding: 1rem; border-radius: 6px; max-height: 400px; overflow: auto;">
${JSON.stringify(template, null, 2)}
        </pre>
        <div class="form-actions">
            <button class="btn" onclick="utils.closeModal('modal')">关闭</button>
            <button class="btn btn-primary" onclick="downloadTemplate('${templateType}')">下载</button>
        </div>
    `;

    utils.showModal('modal');
}

function editTemplate(templateType) {
    const template = projectManager.templates[templateType];
    if (!template) {
        utils.showMessage('模板不存在', 'error');
        return;
    }

    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');

    modalBody.innerHTML = `
        <h3>编辑${templateType === 'outline' ? '大纲模板' : '内容模板'}</h3>
        <textarea id="template-editor" style="width: 100%; height: 400px; font-family: monospace; padding: 1rem; border: 1px solid #ccc; border-radius: 6px;">
${JSON.stringify(template, null, 2)}
        </textarea>
        <div class="form-actions">
            <button class="btn" onclick="utils.closeModal('modal')">取消</button>
            <button class="btn btn-primary" onclick="saveTemplate('${templateType}')">保存</button>
        </div>
    `;

    utils.showModal('modal');
}

function downloadTemplate(templateType) {
    const template = projectManager.templates[templateType];
    const filename = `${templateType}.template.json`;
    const content = JSON.stringify(template, null, 2);
    utils.downloadFile(filename, content);
}

function saveTemplate(templateType) {
    const editor = document.getElementById('template-editor');
    try {
        const template = JSON.parse(editor.value);
        projectManager.templates[templateType] = template;
        utils.showMessage('模板保存成功', 'success');
        utils.closeModal('modal');
    } catch (error) {
        utils.showMessage('JSON格式错误: ' + error.message, 'error');
    }
}

// 创建全局实例
window.projectManager = new ProjectManager();