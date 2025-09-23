// 执行控制台功能

class Executor {
    constructor() {
        this.currentProject = null;
        this.executionStatus = 'ready';
        this.commandHistory = [];
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateStatus('ready', '就绪');
    }

    // 绑定事件
    bindEvents() {
        // 项目选择器变化
        document.getElementById('current-project-console').addEventListener('change', (e) => {
            if (e.target.value) {
                this.loadProject(e.target.value);
            }
        });

        // 执行按钮
        document.getElementById('btn-init').addEventListener('click', () => {
            this.executeInit();
        });

        document.getElementById('btn-prefill').addEventListener('click', () => {
            this.executePrefill();
        });

        document.getElementById('btn-run').addEventListener('click', () => {
            this.executeRun();
        });

        // 复制命令按钮
        document.getElementById('btn-copy-command').addEventListener('click', () => {
            this.copyCurrentCommand();
        });
    }

    // 加载项目
    loadProject(projectId) {
        const project = projectManager.setCurrentProject(projectId);
        if (!project) {
            utils.showMessage('项目不存在', 'error');
            return;
        }

        this.currentProject = project;
        this.clearCommandDisplay();
        this.addLog(`已切换到项目: ${project.name}`);
        utils.showMessage(`已切换到项目: ${project.name}`, 'success');
    }

    // 执行初始化
    executeInit() {
        if (!this.currentProject) {
            utils.showMessage('请先选择项目', 'error');
            return;
        }

        this.updateStatus('running', '初始化中...');

        const command = this.generateInitCommand();
        this.displayCommand('init', command);

        this.addLog('=== 开始初始化 ===');
        this.addLog(`项目: ${this.currentProject.name}`);
        this.addLog(`路径: /projects/${this.currentProject.name}/`);
        this.addLog('正在分析源码结构...');

        // 模拟执行过程
        setTimeout(() => {
            this.simulateInitExecution();
        }, 1000);
    }

    // 模拟初始化执行
    simulateInitExecution() {
        if (!this.currentProject.sourceStructure) {
            this.addLog('❌ 错误: 未找到源码文件');
            this.updateStatus('error', '初始化失败');
            return;
        }

        this.addLog('✅ 源码分析完成');
        this.addLog(`发现 ${this.currentProject.sourceStructure.length} 个文件`);

        // 识别项目类型
        const projectType = this.detectProjectType(this.currentProject.sourceStructure);
        this.addLog(`项目类型: ${projectType}`);

        // 识别主要模块
        const modules = this.extractModules(this.currentProject.sourceStructure);
        this.addLog(`主要模块: ${modules.join(', ')}`);

        // 更新项目信息
        this.currentProject.projectType = projectType;
        this.currentProject.modules = modules;
        this.currentProject.analyzedAt = new Date().toISOString();

        projectManager.saveProject(this.currentProject);

        this.addLog('✅ 初始化完成');
        this.updateStatus('ready', '初始化完成');
    }

    // 执行预填充
    executePrefill() {
        if (!this.currentProject) {
            utils.showMessage('请先选择项目', 'error');
            return;
        }

        if (!this.currentProject.outline) {
            utils.showMessage('请先编辑项目大纲', 'error');
            return;
        }

        this.updateStatus('running', '预填充中...');

        const command = this.generatePrefillCommand();
        this.displayCommand('prefill', command);

        this.addLog('=== 开始预填充 ===');
        this.addLog('正在根据大纲生成内容计划...');

        // 模拟执行过程
        setTimeout(() => {
            this.simulatePrefillExecution();
        }, 1000);
    }

    // 模拟预填充执行
    simulatePrefillExecution() {
        if (!this.currentProject.content) {
            // 初始化内容模板
            this.currentProject.content = utils.deepClone(projectManager.templates.content);
        }

        // 从大纲同步章节
        const sections = this.extractSectionsFromOutline(this.currentProject.outline.nodes);
        let generatedCount = 0;

        sections.forEach(section => {
            if (!this.currentProject.content.contents[section.id]) {
                const sectionContent = this.generateSectionPlan(section);
                this.currentProject.content.contents[section.id] = sectionContent;
                generatedCount++;
                this.addLog(`✅ 为章节 ${section.id} 生成计划`);
            }
        });

        // 更新项目状态
        this.currentProject.status = 'planning';
        this.currentProject.prefilledAt = new Date().toISOString();

        projectManager.saveProject(this.currentProject);

        this.addLog(`✅ 预填充完成，生成了 ${generatedCount} 个章节计划`);
        this.addLog('请在内容编辑器中审核和修改计划');
        this.updateStatus('ready', '预填充完成');
    }

    // 执行生成
    executeRun() {
        if (!this.currentProject) {
            utils.showMessage('请先选择项目', 'error');
            return;
        }

        if (!this.currentProject.content) {
            utils.showMessage('请先执行预填充', 'error');
            return;
        }

        this.updateStatus('running', '生成中...');

        const command = this.generateRunCommand();
        this.displayCommand('run', command);

        this.addLog('=== 开始生成论文内容 ===');
        this.addLog('正在生成正文、图表和表格...');

        // 模拟执行过程
        setTimeout(() => {
            this.simulateRunExecution();
        }, 2000);
    }

    // 模拟运行执行
    simulateRunExecution() {
        const content = this.currentProject.content;
        let totalSections = 0;
        let generatedSections = 0;
        let figureCount = 0;
        let tableCount = 0;

        Object.keys(content.contents).forEach(sectionId => {
            if (sectionId === '__TEMPLATE_PER_SECTION__') return;

            const section = content.contents[sectionId];
            totalSections++;

            // 生成正文
            if (section.plan?.wantText) {
                section.text = this.generateMockText(section.sectionTitle, section.length?.target || 900);
                section.status = 'generated';
                generatedSections++;
                this.addLog(`✅ 生成章节 ${sectionId} 正文 (${section.text.length} 字)`);
            }

            // 生成图表
            if (section.plan?.wantFigure && section.plan.figurePlan) {
                section.figures = section.plan.figurePlan
                    .filter(plan => plan.enabled)
                    .map((plan, index) => {
                        figureCount++;
                        const figure = this.generateMockFigure(plan, sectionId, index);
                        this.addLog(`✅ 生成图表: ${figure.label}`);
                        return figure;
                    });
            }

            // 生成表格
            if (section.plan?.wantTable && section.plan.tablePlan) {
                section.tables = section.plan.tablePlan
                    .filter(plan => plan.enabled)
                    .map((plan, index) => {
                        tableCount++;
                        const table = this.generateMockTable(plan, sectionId, index);
                        this.addLog(`✅ 生成表格: ${table.label}`);
                        return table;
                    });
            }
        });

        // 更新项目状态
        this.currentProject.status = 'generated';
        this.currentProject.generatedAt = new Date().toISOString();

        projectManager.saveProject(this.currentProject);

        this.addLog('=== 生成完成 ===');
        this.addLog(`总计: ${totalSections} 个章节, ${figureCount} 个图表, ${tableCount} 个表格`);
        this.addLog('可以在导出页面查看和下载结果');
        this.updateStatus('ready', '生成完成');
    }

    // 生成命令
    generateInitCommand() {
        const projectPath = `project/${this.currentProject.name}`;
        return `/init\n请你全面阅读 ${projectPath}/source 目录下的源码，识别以下信息并总结到内存中：\n1. 使用的语言、框架、数据库、主要依赖。\n2. 项目的模块结构、关键类/函数/接口。\n3. 数据库表及其关系（如果能解析）。\n4. 系统的整体功能和业务逻辑。\n\n注意：\n- 只做总结与理解，不要写入 content.json。\n- 生成 Claude.md\n- 后续 prefill-content 和 run-paper 都会依赖你现在的理解。`;
    }

    generatePrefillCommand() {
        const projectPath = `project/${this.currentProject.name}`;
        return `/prefill-content\n请你读取 ${projectPath}/paper/outline.json 和 templates/content.template.json，\n生成 ${projectPath}/paper/content.json，要求：\n\n1. 为每个章节生成一个条目，复制模板 defaults。\n2. 每个章节都写入：\n   - status = "planning"\n   - plan.wantText = true\n   - textPrompt = 根据 defaults.textPromptTemplate 渲染，替换 {{sectionTitle}} 和 {{论文主题}}。\n3. 根据章节标题和源码理解，判断是否需要图或表：\n   - 如果标题包含 "用例图/架构/框图/ER图/时序/部署" → plan.wantFigure=true，启用 figurePlan[0] 并设置 figureTitle/figureFocus。\n   - 如果标题包含 "数据库/测试/性能/指标" → plan.wantTable=true，启用 tablePlan[0] 并设置 tableTitle/schema。\n4. figures[] 和 tables[] 留空，正文 text 留空。\n5. 保持章节 id 与 outline.json 一致。\n\n注意：\n- 不要写正文，也不要生成图表，只写 plan 和提示词。\n- 输出结果写入 content.json 文件，供我后续人工审查。`;
    }

    generateRunCommand() {
        const projectPath = `project/${this.currentProject.name}`;
        return `/run-paper\n请你读取 ${projectPath}/paper/content.json 和源码 ${projectPath}/source，\n根据 content.json.plan 配置逐章生成论文内容，要求：\n\n1. 正文生成：\n   - 对 plan.wantText = true 的章节，生成正文 text。\n   - 正文必须围绕论文主题和源码结构，语言学术化，避免空话和口语化。\n   - 正文字数参考 length.target。\n\n2. 图生成：\n   - 对每个 plan.figurePlan.enabled=true 的项：\n     a) 渲染 promptTemplate（替换 {{sectionTitle}}、{{论文主题}}、{{figureFocus}}）。\n     b) 生成合法的 PlantUML 代码，保存到 paper/exports/images/Fig-<sectionId>-<idx>.puml。\n     c) 调用鲁班 UML 工具渲染 PNG，路径 paper/exports/images/Fig-<sectionId>-<idx>.png。\n     d) 在 content.json.contents[<id>].figures[] 追加相关信息。\n\n3. 表生成：\n   - 对每个 plan.tablePlan.enabled=true 的项：\n     a) 渲染 promptTemplate（替换 {{sectionTitle}}、{{论文主题}}、{{schema}}）。\n     b) 输出 JSON 格式数据，包含 schema 和 rows。\n     c) 写入 content.json.contents[<id>].tables[] 相关信息。\n\n4. 容错：\n   - 图/表生成失败时 status=failed，不要中断，继续生成正文和其他章节。\n\n5. 导出：\n   - 调用 Word 工具，消费 content.json 和 outline.json，\n     生成 paper/exports/docx/paper.docx。\n   - 插入正文 text；图用 imagePath；表用 schema+rows 渲染三线表。\n   - 失败的图/表插入占位符。`;
    }

    // 显示命令
    displayCommand(action, command) {
        const commandOutput = document.getElementById('command-output');
        const projectPath = `/Users/pc/Documents/promptx_tools/web/project/${this.currentProject.name}`;

        commandOutput.innerHTML = `
            <div class="command-header">
                <h4>${this.getActionName(action)}</h4>
                <span class="command-time">${new Date().toLocaleTimeString()}</span>
            </div>
            <div class="command-info">
                <p><strong>项目:</strong> ${this.currentProject.name}</p>
                <p><strong>路径:</strong> ${projectPath}</p>
            </div>
            <pre class="command-text">${command}</pre>
            <div class="command-note">
                <p>💡 请复制上述命令在 Claude Code 中执行</p>
                <p>📂 确保在正确的目录下执行命令</p>
            </div>
        `;

        this.currentCommand = command;
        this.commandHistory.push({ action, command, timestamp: new Date() });
    }

    // 清空命令显示
    clearCommandDisplay() {
        const commandOutput = document.getElementById('command-output');
        commandOutput.innerHTML = '<p>选择操作后，将在此显示Claude Code命令</p>';
        this.currentCommand = null;
    }

    // 复制当前命令
    copyCurrentCommand() {
        if (this.currentCommand) {
            utils.copyToClipboard(this.currentCommand);
        } else {
            utils.showMessage('无命令可复制', 'error');
        }
    }

    // 添加日志
    addLog(message) {
        const logContainer = document.getElementById('execution-log');
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.innerHTML = `<span class="log-time">[${timestamp}]</span> ${message}`;

        logContainer.appendChild(logEntry);
        logContainer.scrollTop = logContainer.scrollHeight;
    }

    // 更新状态
    updateStatus(status, text) {
        this.executionStatus = status;
        const statusElement = document.getElementById('execution-status');
        const statusValue = document.querySelector('.status-value');

        statusElement.textContent = text;

        // 更新状态样式
        statusValue.className = 'status-value';
        if (status === 'running') {
            statusValue.classList.add('status-running');
        } else if (status === 'error') {
            statusValue.classList.add('status-error');
        } else if (status === 'ready') {
            statusValue.classList.add('status-ready');
        }

        // 更新按钮状态
        const buttons = ['btn-init', 'btn-prefill', 'btn-run'];
        buttons.forEach(btnId => {
            const btn = document.getElementById(btnId);
            btn.disabled = (status === 'running');
        });
    }

    // 获取操作名称
    getActionName(action) {
        const actionNames = {
            init: '初始化项目',
            prefill: '预填充内容',
            run: '生成论文'
        };
        return actionNames[action] || action;
    }

    // 检测项目类型
    detectProjectType(sourceStructure) {
        const files = sourceStructure.map(item => item.path.toLowerCase());

        if (files.some(f => f.includes('pom.xml'))) return 'Java Maven';
        if (files.some(f => f.includes('build.gradle'))) return 'Java Gradle';
        if (files.some(f => f.includes('package.json'))) return 'Node.js';
        if (files.some(f => f.includes('requirements.txt'))) return 'Python';
        if (files.some(f => f.includes('gemfile'))) return 'Ruby';
        if (files.some(f => f.includes('cargo.toml'))) return 'Rust';
        if (files.some(f => f.includes('.csproj'))) return 'C#';
        if (files.some(f => f.includes('go.mod'))) return 'Go';

        return '未知类型';
    }

    // 提取模块
    extractModules(sourceStructure) {
        const modules = new Set();
        const directories = sourceStructure
            .filter(item => item.isDirectory)
            .map(item => item.path);

        // 常见模块目录模式
        const modulePatterns = [
            /src\/main\/java\/.*?\/([^\/]+)$/,
            /src\/([^\/]+)$/,
            /lib\/([^\/]+)$/,
            /modules\/([^\/]+)$/,
            /packages\/([^\/]+)$/
        ];

        directories.forEach(dir => {
            modulePatterns.forEach(pattern => {
                const match = dir.match(pattern);
                if (match) {
                    modules.add(match[1]);
                }
            });
        });

        return Array.from(modules).slice(0, 10); // 限制数量
    }

    // 从大纲提取章节
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

    // 生成章节计划
    generateSectionPlan(section) {
        const template = projectManager.templates.content.contents['__TEMPLATE_PER_SECTION__'];

        // 根据章节内容判断是否需要图表
        const needsFigure = this.shouldGenerateFigure(section.title);
        const needsTable = this.shouldGenerateTable(section.title);

        const plan = {
            status: 'planning',
            sectionTitle: section.title,
            length: template.length,
            plan: {
                wantText: true,
                wantFigure: needsFigure,
                figurePlan: needsFigure ? [this.generateFigurePlan(section)] : [],
                wantTable: needsTable,
                tablePlan: needsTable ? [this.generateTablePlan(section)] : []
            },
            text: '',
            textPrompt: this.generateTextPrompt(section.title),
            figures: [],
            tables: []
        };

        return plan;
    }

    // 判断是否需要图表
    shouldGenerateFigure(title) {
        const figureKeywords = ['架构', '设计', '流程', '结构', '框图', '用例', '时序', 'ER图'];
        return figureKeywords.some(keyword => title.includes(keyword));
    }

    // 判断是否需要表格
    shouldGenerateTable(title) {
        const tableKeywords = ['测试', '需求', '对比', '数据库', '字段', '接口', '性能'];
        return tableKeywords.some(keyword => title.includes(keyword));
    }

    // 生成图表计划
    generateFigurePlan(section) {
        const figureTypes = {
            '架构': { title: '系统架构图', focus: '整体架构和模块关系' },
            '设计': { title: '设计方案图', focus: '设计思路和实现方案' },
            '流程': { title: '业务流程图', focus: '流程步骤和决策点' },
            '用例': { title: '用例图', focus: '用户角色和系统交互' }
        };

        for (const [keyword, config] of Object.entries(figureTypes)) {
            if (section.title.includes(keyword)) {
                return {
                    enabled: true,
                    figureTitle: config.title,
                    figureFocus: config.focus,
                    schema: null,
                    promptTemplate: projectManager.templates.content.defaults?.figurePromptTemplate || ''
                };
            }
        }

        return {
            enabled: true,
            figureTitle: `${section.title}示意图`,
            figureFocus: '关键要点和关系',
            schema: null,
            promptTemplate: projectManager.templates.content.defaults?.figurePromptTemplate || ''
        };
    }

    // 生成表格计划
    generateTablePlan(section) {
        const tableTypes = {
            '测试': { title: '测试用例表', schema: ['测试项', '输入', '预期输出', '实际结果'] },
            '需求': { title: '需求分析表', schema: ['需求ID', '需求描述', '优先级', '状态'] },
            '数据库': { title: '数据库设计表', schema: ['字段名', '类型', '长度', '约束', '说明'] }
        };

        for (const [keyword, config] of Object.entries(tableTypes)) {
            if (section.title.includes(keyword)) {
                return {
                    enabled: true,
                    tableTitle: config.title,
                    schema: config.schema,
                    promptTemplate: projectManager.templates.content.defaults?.tablePromptTemplate || ''
                };
            }
        }

        return {
            enabled: true,
            tableTitle: `${section.title}汇总表`,
            schema: ['项目', '内容', '说明'],
            promptTemplate: projectManager.templates.content.defaults?.tablePromptTemplate || ''
        };
    }

    // 生成文本提示词
    generateTextPrompt(sectionTitle) {
        const template = projectManager.templates.content.defaults?.textPromptTemplate ||
            '撰写《{{sectionTitle}}》，围绕"{{论文主题}}"，结合源码结构、关键模块与数据流，语言学术化，避免口语化。';

        return template
            .replace('{{sectionTitle}}', sectionTitle)
            .replace('{{论文主题}}', this.currentProject.theme || '系统开发');
    }

    // 生成模拟正文
    generateMockText(title, targetLength) {
        const mockTexts = [
            `${title}是本系统的重要组成部分，在整个系统架构中起着关键作用。`,
            `通过深入分析需求和技术调研，我们设计了一套完整的解决方案。`,
            `该模块采用了先进的技术架构，确保了系统的稳定性和可扩展性。`,
            `在实现过程中，我们遵循了软件工程的最佳实践，保证了代码质量。`,
            `测试结果表明，该设计方案能够满足预期的功能需求和性能指标。`
        ];

        let text = mockTexts.join('');
        while (text.length < targetLength) {
            text += mockTexts[Math.floor(Math.random() * mockTexts.length)];
        }

        return text.substring(0, targetLength);
    }

    // 生成模拟图表
    generateMockFigure(plan, sectionId, index) {
        return {
            label: `图${sectionId}-${index + 1} ${plan.figureTitle}`,
            title: plan.figureTitle,
            imagePath: `/projects/${this.currentProject.name}/images/fig-${sectionId}-${index + 1}.png`,
            status: 'success',
            generatedAt: new Date().toISOString()
        };
    }

    // 生成模拟表格
    generateMockTable(plan, sectionId, index) {
        const mockData = {
            headers: plan.schema || ['项目', '内容', '说明'],
            rows: [
                ['示例1', '示例内容1', '示例说明1'],
                ['示例2', '示例内容2', '示例说明2'],
                ['示例3', '示例内容3', '示例说明3']
            ]
        };

        return {
            label: `表${sectionId}-${index + 1} ${plan.tableTitle}`,
            title: plan.tableTitle,
            data: mockData,
            status: 'success',
            generatedAt: new Date().toISOString()
        };
    }
}

// 创建全局实例
window.executor = new Executor();