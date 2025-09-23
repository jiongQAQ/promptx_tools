// 主应用程序

class App {
    constructor() {
        this.currentPage = 'projects';
        this.init();
    }

    init() {
        this.bindEvents();
        this.initializeComponents();
        this.showPage('projects');
    }

    // 绑定全局事件
    bindEvents() {
        // 导航按钮
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const page = e.target.dataset.page;
                if (page) {
                    this.switchPage(page);
                }
            });
        });

        // 模态框关闭
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-close')) {
                const modal = e.target.closest('.modal');
                if (modal) {
                    modal.classList.remove('show');
                }
            }

            // 点击模态框外部关闭
            if (e.target.classList.contains('modal')) {
                e.target.classList.remove('show');
            }
        });

        // ESC键关闭模态框
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                document.querySelectorAll('.modal.show').forEach(modal => {
                    modal.classList.remove('show');
                });
            }
        });

        // 全局快捷键
        document.addEventListener('keydown', (e) => {
            // Alt + 数字切换页面
            if (e.altKey && e.key >= '1' && e.key <= '6') {
                e.preventDefault();
                const pages = ['projects', 'templates', 'outline', 'content', 'console', 'export'];
                const pageIndex = parseInt(e.key) - 1;
                if (pages[pageIndex]) {
                    this.switchPage(pages[pageIndex]);
                }
            }
        });

        // 页面可见性变化
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.refreshCurrentPage();
            }
        });
    }

    // 初始化组件
    initializeComponents() {
        // 项目管理器已在project.js中初始化
        // 大纲编辑器已在outline.js中初始化
        // 内容编辑器已在content.js中初始化
        // 执行器已在executor.js中初始化

        // 更新项目选择器
        this.updateAllProjectSelectors();

        // 设置定时保存
        this.setupAutoSave();

        // 显示版本信息
        console.log('📄 论文生成系统 v1.0.0');
        console.log('🚀 系统初始化完成');
    }

    // 切换页面
    switchPage(pageName) {
        // 隐藏所有页面
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });

        // 显示目标页面
        const targetPage = document.getElementById(`page-${pageName}`);
        if (targetPage) {
            targetPage.classList.add('active');
        }

        // 更新导航状态
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        const targetNavBtn = document.querySelector(`[data-page="${pageName}"]`);
        if (targetNavBtn) {
            targetNavBtn.classList.add('active');
        }

        this.currentPage = pageName;

        // 页面切换后的处理
        this.onPageSwitch(pageName);

        // 更新浏览器标题
        this.updatePageTitle(pageName);
    }

    // 页面切换后的处理
    onPageSwitch(pageName) {
        switch (pageName) {
            case 'projects':
                // 刷新项目列表
                if (window.projectManager) {
                    projectManager.renderProjectList();
                }
                break;

            case 'templates':
                // 刷新模板
                if (window.projectManager) {
                    projectManager.loadTemplates();
                }
                break;

            case 'outline':
                // 更新项目选择器
                this.updateProjectSelector('current-project-outline');
                break;

            case 'content':
                // 更新项目选择器
                this.updateProjectSelector('current-project-content');
                break;

            case 'console':
                // 更新项目选择器
                this.updateProjectSelector('current-project-console');
                break;

            case 'export':
                // 更新项目选择器和导出列表
                this.updateProjectSelector('current-project-export');
                this.refreshExportList();
                break;
        }
    }

    // 更新页面标题
    updatePageTitle(pageName) {
        const pageTitles = {
            projects: '项目管理',
            templates: '模板库',
            outline: '大纲编辑',
            content: '内容编辑',
            console: '执行控制',
            export: '导出预览'
        };

        const baseTitle = '论文生成系统';
        const pageTitle = pageTitles[pageName];

        document.title = pageTitle ? `${pageTitle} - ${baseTitle}` : baseTitle;
    }

    // 显示页面（公共方法）
    showPage(pageName) {
        this.switchPage(pageName);
    }

    // 刷新当前页面
    refreshCurrentPage() {
        this.onPageSwitch(this.currentPage);
    }

    // 更新指定的项目选择器
    updateProjectSelector(selectorId) {
        if (window.projectManager) {
            projectManager.updateProjectSelectors();
        }
    }

    // 更新所有项目选择器
    updateAllProjectSelectors() {
        if (window.projectManager) {
            projectManager.updateProjectSelectors();
        }
    }

    // 设置自动保存
    setupAutoSave() {
        // 每5分钟自动保存当前编辑的内容
        setInterval(() => {
            this.autoSave();
        }, 5 * 60 * 1000);

        // 页面卸载前保存
        window.addEventListener('beforeunload', (e) => {
            this.autoSave();

            // 检查是否有未保存的内容
            if (this.hasUnsavedChanges()) {
                e.preventDefault();
                e.returnValue = '您有未保存的更改，确定要离开吗？';
                return e.returnValue;
            }
        });
    }

    // 自动保存
    autoSave() {
        try {
            // 保存大纲编辑器的内容
            if (window.outlineEditor && outlineEditor.isDirty) {
                outlineEditor.saveOutline();
                console.log('自动保存: 大纲');
            }

            // 保存内容编辑器的内容
            if (window.contentEditor && contentEditor.isDirty) {
                contentEditor.saveContent();
                console.log('自动保存: 内容');
            }
        } catch (error) {
            console.error('自动保存失败:', error);
        }
    }

    // 检查是否有未保存的更改
    hasUnsavedChanges() {
        const outlineDirty = window.outlineEditor?.isDirty || false;
        const contentDirty = window.contentEditor?.isDirty || false;

        return outlineDirty || contentDirty;
    }

    // 刷新导出列表
    refreshExportList() {
        const exportList = document.getElementById('export-list');
        if (!exportList) return;

        const currentProject = projectManager.getCurrentProject();
        if (!currentProject) {
            exportList.innerHTML = '<p>请先选择项目</p>';
            return;
        }

        // 模拟导出历史
        const mockExports = [
            {
                filename: `${currentProject.name}.docx`,
                time: currentProject.generatedAt || new Date().toISOString(),
                size: '1.2 MB',
                status: 'success'
            }
        ];

        if (mockExports.length === 0) {
            exportList.innerHTML = '<p>暂无导出记录</p>';
            return;
        }

        exportList.innerHTML = mockExports.map(exp => `
            <div class="export-item">
                <div class="export-info">
                    <h4>📄 ${exp.filename}</h4>
                    <p>导出时间: ${utils.formatDate(exp.time)}</p>
                    <p>文件大小: ${exp.size}</p>
                </div>
                <div class="export-actions">
                    <button class="btn btn-sm" onclick="app.downloadExport('${exp.filename}')">📥 下载</button>
                    <button class="btn btn-sm" onclick="app.previewExport('${exp.filename}')">👁️ 预览</button>
                </div>
            </div>
        `).join('');
    }

    // 下载导出文件
    downloadExport(filename) {
        // 模拟下载
        utils.showMessage(`开始下载: ${filename}`, 'info');

        // 实际应用中这里应该调用真实的下载API
        setTimeout(() => {
            utils.showMessage('下载完成', 'success');
        }, 2000);
    }

    // 预览导出文件
    previewExport(filename) {
        utils.showMessage('预览功能开发中', 'info');
    }

    // 获取应用状态
    getAppState() {
        return {
            currentPage: this.currentPage,
            currentProject: projectManager.getCurrentProject()?.id || null,
            hasUnsavedChanges: this.hasUnsavedChanges()
        };
    }

    // 错误处理
    handleError(error, context = '') {
        console.error(`应用错误 ${context}:`, error);

        let message = '发生未知错误';
        if (error.message) {
            message = error.message;
        }

        utils.showMessage(`错误: ${message}`, 'error');
    }

    // 显示帮助信息
    showHelp() {
        const modal = document.getElementById('modal');
        const modalBody = document.getElementById('modal-body');

        modalBody.innerHTML = `
            <h3>🔔 使用帮助</h3>

            <div class="help-section">
                <h4>📁 项目管理</h4>
                <ul>
                    <li>点击"新建项目"创建论文项目</li>
                    <li>上传源码ZIP文件进行分析</li>
                    <li>选择合适的模板</li>
                </ul>
            </div>

            <div class="help-section">
                <h4>📝 大纲编辑</h4>
                <ul>
                    <li>使用树形编辑器编辑论文结构</li>
                    <li>支持拖拽排序和层级调整</li>
                    <li>自动生成章节编号</li>
                </ul>
            </div>

            <div class="help-section">
                <h4>📄 内容编辑</h4>
                <ul>
                    <li>为每个章节配置生成计划</li>
                    <li>编辑提示词模板</li>
                    <li>管理图表和表格</li>
                </ul>
            </div>

            <div class="help-section">
                <h4>⚡ 执行控制</h4>
                <ul>
                    <li>Init: 分析项目源码</li>
                    <li>Prefill: 生成内容计划</li>
                    <li>Run: 生成最终内容</li>
                </ul>
            </div>

            <div class="help-section">
                <h4>⌨️ 快捷键</h4>
                <ul>
                    <li>Alt + 1-6: 切换页面</li>
                    <li>Ctrl/Cmd + S: 保存</li>
                    <li>ESC: 关闭模态框</li>
                </ul>
            </div>

            <div class="form-actions">
                <button class="btn btn-primary" onclick="utils.closeModal('modal')">知道了</button>
            </div>
        `;

        utils.showModal('modal');
    }
}

// 全局错误处理
window.addEventListener('error', (e) => {
    console.error('全局错误:', e.error);
    if (window.app) {
        app.handleError(e.error, '全局');
    }
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('未处理的Promise拒绝:', e.reason);
    if (window.app) {
        app.handleError(e.reason, 'Promise');
    }
});

// 导出页面相关函数
function exportProject() {
    const currentProject = projectManager.getCurrentProject();
    if (!currentProject) {
        utils.showMessage('请先选择项目', 'error');
        return;
    }

    const filename = document.getElementById('export-filename').value || 'paper.docx';

    utils.showLoading('导出中...');

    // 生成导出命令
    const projectPath = `/projects/${currentProject.name}`;
    const command = `cd ${projectPath} && word-export --content content.json --outline outline.json --out ${filename}`;

    // 显示命令
    setTimeout(() => {
        utils.hideLoading();

        const modal = document.getElementById('modal');
        const modalBody = document.getElementById('modal-body');

        modalBody.innerHTML = `
            <h3>📄 导出命令</h3>
            <p>请在 Claude Code 中执行以下命令：</p>
            <pre class="command-box">${command}</pre>
            <div class="form-actions">
                <button class="btn" onclick="utils.closeModal('modal')">关闭</button>
                <button class="btn btn-primary" onclick="utils.copyToClipboard('${command}'); utils.closeModal('modal')">复制命令</button>
            </div>
        `;

        utils.showModal('modal');
    }, 1000);
}

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    try {
        window.app = new App();
        console.log('✅ 应用初始化成功');
    } catch (error) {
        console.error('❌ 应用初始化失败:', error);
        document.body.innerHTML = `
            <div style="padding: 2rem; text-align: center;">
                <h1>❌ 初始化失败</h1>
                <p>应用无法正常启动，请刷新页面重试。</p>
                <p style="color: #666; font-size: 0.9rem;">错误信息: ${error.message}</p>
                <button onclick="location.reload()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    🔄 刷新页面
                </button>
            </div>
        `;
    }
});

// 导出全局函数
window.exportProject = exportProject;