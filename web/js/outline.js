// 大纲编辑器功能

class OutlineEditor {
    constructor() {
        this.outline = null;
        this.selectedNode = null;
        this.isDirty = false;
        this.init();
    }

    init() {
        this.bindEvents();
    }

    // 绑定事件
    bindEvents() {
        // 项目选择器变化
        document.getElementById('current-project-outline').addEventListener('change', (e) => {
            if (e.target.value) {
                this.loadProjectOutline(e.target.value);
            }
        });

        // 保存按钮
        document.getElementById('btn-save-outline').addEventListener('click', () => {
            this.saveOutline();
        });

        // 键盘快捷键
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                if (e.key === 's') {
                    e.preventDefault();
                    this.saveOutline();
                } else if (e.key === 'Enter') {
                    e.preventDefault();
                    this.addNode();
                } else if (e.key === 'Delete' || e.key === 'Backspace') {
                    if (this.selectedNode) {
                        e.preventDefault();
                        this.deleteNode();
                    }
                }
            }
        });
    }

    // 加载项目大纲
    loadProjectOutline(projectId) {
        const project = projectManager.setCurrentProject(projectId);
        if (!project) {
            utils.showMessage('项目不存在', 'error');
            return;
        }

        // 如果项目有大纲数据，加载它；否则使用模板
        this.outline = project.outline || utils.deepClone(projectManager.templates.outline);
        this.renderOutlineTree();
        this.isDirty = false;

        utils.showMessage(`已加载项目 "${project.name}" 的大纲`, 'success');
    }

    // 渲染大纲树
    renderOutlineTree() {
        const container = document.getElementById('outline-tree');

        if (!this.outline || !this.outline.nodes) {
            container.innerHTML = '<p>暂无大纲数据</p>';
            return;
        }

        container.innerHTML = `
            <div class="outline-header">
                <h3 contenteditable="true" class="outline-title" onblur="outlineEditor.updateTitle(this.textContent)">
                    ${this.outline.title || '论文大纲'}
                </h3>
            </div>
            <div class="outline-nodes">
                ${this.renderNodes(this.outline.nodes)}
            </div>
        `;

        // 绑定节点事件
        this.bindNodeEvents();
    }

    // 渲染节点
    renderNodes(nodes, level = 0) {
        if (!nodes || nodes.length === 0) return '';

        return nodes.map(node => `
            <div class="tree-node" data-node-id="${node.id}" style="margin-left: ${level * 20}px">
                <div class="node-content" onclick="outlineEditor.selectNode('${node.id}')">
                    <span class="node-toggle" onclick="outlineEditor.toggleNode('${node.id}', event)">
                        ${node.children && node.children.length > 0 ? '▼' : ''}
                    </span>
                    <span class="node-id">${node.id}</span>
                    <input type="text" class="node-title" value="${node.title}"
                           onchange="outlineEditor.updateNodeTitle('${node.id}', this.value)"
                           onkeypress="outlineEditor.handleTitleKeyPress(event, '${node.id}')">
                    <div class="node-actions">
                        <button class="node-action add" onclick="outlineEditor.addChildNode('${node.id}')" title="添加子节点">
                            ➕
                        </button>
                        <button class="node-action add" onclick="outlineEditor.addSiblingNode('${node.id}')" title="添加同级节点">
                            ↩️
                        </button>
                        <button class="node-action delete" onclick="outlineEditor.deleteNodeById('${node.id}')" title="删除节点">
                            🗑️
                        </button>
                    </div>
                </div>
                <div class="node-children ${node.collapsed ? 'collapsed' : ''}">
                    ${this.renderNodes(node.children || [], level + 1)}
                </div>
            </div>
        `).join('');
    }

    // 绑定节点事件
    bindNodeEvents() {
        // 拖拽功能（简化版）
        const nodes = document.querySelectorAll('.tree-node');
        nodes.forEach(node => {
            node.draggable = true;
            node.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', node.dataset.nodeId);
                node.classList.add('dragging');
            });

            node.addEventListener('dragend', () => {
                node.classList.remove('dragging');
            });

            node.addEventListener('dragover', (e) => {
                e.preventDefault();
                node.classList.add('drag-over');
            });

            node.addEventListener('dragleave', () => {
                node.classList.remove('drag-over');
            });

            node.addEventListener('drop', (e) => {
                e.preventDefault();
                node.classList.remove('drag-over');
                const sourceId = e.dataTransfer.getData('text/plain');
                const targetId = node.dataset.nodeId;
                this.moveNode(sourceId, targetId);
            });
        });
    }

    // 选择节点
    selectNode(nodeId) {
        // 清除之前的选择
        document.querySelectorAll('.node-content.selected').forEach(el => {
            el.classList.remove('selected');
        });

        // 选择当前节点
        const nodeElement = document.querySelector(`[data-node-id="${nodeId}"] .node-content`);
        if (nodeElement) {
            nodeElement.classList.add('selected');
            this.selectedNode = nodeId;
        }
    }

    // 切换节点展开/折叠
    toggleNode(nodeId, event) {
        event.stopPropagation();
        const node = this.findNode(this.outline.nodes, nodeId);
        if (node) {
            node.collapsed = !node.collapsed;
            this.renderOutlineTree();
            this.markDirty();
        }
    }

    // 更新大纲标题
    updateTitle(title) {
        this.outline.title = title;
        this.markDirty();
    }

    // 更新节点标题
    updateNodeTitle(nodeId, title) {
        const node = this.findNode(this.outline.nodes, nodeId);
        if (node) {
            node.title = title;
            this.markDirty();
        }
    }

    // 处理标题输入框键盘事件
    handleTitleKeyPress(event, nodeId) {
        if (event.key === 'Enter') {
            event.preventDefault();
            event.target.blur();
            this.addSiblingNode(nodeId);
        }
    }

    // 添加节点（工具栏按钮）
    addNode() {
        if (this.selectedNode) {
            this.addChildNode(this.selectedNode);
        } else {
            // 添加到根级别
            this.addRootNode();
        }
    }

    // 添加根节点
    addRootNode() {
        const newId = this.generateNextId(this.outline.nodes);
        const newNode = {
            id: newId,
            title: '新章节',
            children: []
        };

        this.outline.nodes.push(newNode);
        this.renderOutlineTree();
        this.selectNode(newId);
        this.markDirty();
    }

    // 添加子节点
    addChildNode(parentId) {
        const parentNode = this.findNode(this.outline.nodes, parentId);
        if (!parentNode) return;

        if (!parentNode.children) {
            parentNode.children = [];
        }

        const newId = this.generateNextChildId(parentId, parentNode.children);
        const newNode = {
            id: newId,
            title: '新子节点',
            children: []
        };

        parentNode.children.push(newNode);
        parentNode.collapsed = false; // 展开父节点
        this.renderOutlineTree();
        this.selectNode(newId);
        this.markDirty();
    }

    // 添加同级节点
    addSiblingNode(siblingId) {
        const parentNodes = this.findParentAndIndex(this.outline.nodes, siblingId);
        if (!parentNodes) return;

        const { parent, index } = parentNodes;
        const siblings = parent ? parent.children : this.outline.nodes;
        const parentId = parent ? parent.id : '';

        const newId = this.generateNextSiblingId(parentId, siblings, index);
        const newNode = {
            id: newId,
            title: '新节点',
            children: []
        };

        siblings.splice(index + 1, 0, newNode);
        this.renderOutlineTree();
        this.selectNode(newId);
        this.markDirty();
    }

    // 删除节点（工具栏按钮）
    deleteNode() {
        if (this.selectedNode) {
            this.deleteNodeById(this.selectedNode);
        }
    }

    // 根据ID删除节点
    deleteNodeById(nodeId) {
        utils.showConfirm(
            '确定要删除此节点及其所有子节点吗？',
            () => {
                if (this.removeNode(this.outline.nodes, nodeId)) {
                    this.renderOutlineTree();
                    this.selectedNode = null;
                    this.markDirty();
                    utils.showMessage('节点删除成功', 'success');
                }
            }
        );
    }

    // 移动节点
    moveNode(sourceId, targetId) {
        if (sourceId === targetId) return;

        const sourceNode = this.findNode(this.outline.nodes, sourceId);
        if (!sourceNode) return;

        // 移除源节点
        this.removeNode(this.outline.nodes, sourceId);

        // 添加到目标位置
        const targetNode = this.findNode(this.outline.nodes, targetId);
        if (targetNode) {
            if (!targetNode.children) {
                targetNode.children = [];
            }
            targetNode.children.push(sourceNode);
            targetNode.collapsed = false;
        }

        // 更新节点ID
        this.updateNodeIds(sourceNode, targetId);

        this.renderOutlineTree();
        this.markDirty();
        utils.showMessage('节点移动成功', 'success');
    }

    // 生成下一个ID
    generateNextId(nodes) {
        const maxId = Math.max(...nodes.map(n => parseInt(n.id) || 0));
        return (maxId + 1).toString();
    }

    // 生成下一个子节点ID
    generateNextChildId(parentId, children) {
        const maxSubId = Math.max(...children.map(n => {
            const parts = n.id.split('.');
            return parseInt(parts[parts.length - 1]) || 0;
        }));
        return `${parentId}.${maxSubId + 1}`;
    }

    // 生成下一个同级节点ID
    generateNextSiblingId(parentId, siblings, currentIndex) {
        const currentNode = siblings[currentIndex];
        const currentParts = currentNode.id.split('.');
        const currentNum = parseInt(currentParts[currentParts.length - 1]);

        if (parentId) {
            return `${parentId}.${currentNum + 1}`;
        } else {
            return (currentNum + 1).toString();
        }
    }

    // 查找节点
    findNode(nodes, nodeId) {
        for (const node of nodes) {
            if (node.id === nodeId) {
                return node;
            }
            if (node.children) {
                const found = this.findNode(node.children, nodeId);
                if (found) return found;
            }
        }
        return null;
    }

    // 查找父节点和索引
    findParentAndIndex(nodes, nodeId, parent = null) {
        for (let i = 0; i < nodes.length; i++) {
            const node = nodes[i];
            if (node.id === nodeId) {
                return { parent, index: i };
            }
            if (node.children) {
                const found = this.findParentAndIndex(node.children, nodeId, node);
                if (found) return found;
            }
        }
        return null;
    }

    // 移除节点
    removeNode(nodes, nodeId) {
        for (let i = 0; i < nodes.length; i++) {
            if (nodes[i].id === nodeId) {
                nodes.splice(i, 1);
                return true;
            }
            if (nodes[i].children && this.removeNode(nodes[i].children, nodeId)) {
                return true;
            }
        }
        return false;
    }

    // 更新节点ID
    updateNodeIds(node, newParentId) {
        // 简化版：保持原有ID结构
        // 实际应用中可能需要重新生成完整的ID层次结构
    }

    // 展开所有节点
    expandAll() {
        this.setAllNodesCollapsed(this.outline.nodes, false);
        this.renderOutlineTree();
    }

    // 折叠所有节点
    collapseAll() {
        this.setAllNodesCollapsed(this.outline.nodes, true);
        this.renderOutlineTree();
    }

    // 设置所有节点的折叠状态
    setAllNodesCollapsed(nodes, collapsed) {
        nodes.forEach(node => {
            if (node.children && node.children.length > 0) {
                node.collapsed = collapsed;
                this.setAllNodesCollapsed(node.children, collapsed);
            }
        });
    }

    // 标记为已修改
    markDirty() {
        this.isDirty = true;
        document.getElementById('btn-save-outline').textContent = '💾 保存大纲 *';
    }

    // 保存大纲
    saveOutline() {
        const project = projectManager.getCurrentProject();
        if (!project) {
            utils.showMessage('请先选择项目', 'error');
            return;
        }

        if (!this.outline) {
            utils.showMessage('无大纲数据可保存', 'error');
            return;
        }

        // 验证大纲
        const validation = this.validateOutline();
        if (!validation.valid) {
            utils.showMessage('大纲验证失败: ' + validation.errors.join(', '), 'error');
            return;
        }

        project.outline = utils.deepClone(this.outline);

        if (projectManager.saveProject(project)) {
            this.isDirty = false;
            document.getElementById('btn-save-outline').textContent = '💾 保存大纲';
            utils.showMessage('大纲保存成功', 'success');

            // 触发内容同步
            this.syncToContent();
        } else {
            utils.showMessage('保存失败', 'error');
        }
    }

    // 验证大纲
    validateOutline() {
        const errors = [];
        const usedIds = new Set();

        const validateNodes = (nodes, level = 0) => {
            nodes.forEach(node => {
                // 检查ID唯一性
                if (usedIds.has(node.id)) {
                    errors.push(`重复的节点ID: ${node.id}`);
                } else {
                    usedIds.add(node.id);
                }

                // 检查标题非空
                if (!node.title || node.title.trim() === '') {
                    errors.push(`节点 ${node.id} 标题不能为空`);
                }

                // 递归检查子节点
                if (node.children) {
                    validateNodes(node.children, level + 1);
                }
            });
        };

        if (this.outline.nodes) {
            validateNodes(this.outline.nodes);
        }

        return {
            valid: errors.length === 0,
            errors
        };
    }

    // 同步到内容编辑器
    syncToContent() {
        // 这里应该通知内容编辑器更新章节列表
        console.log('Outline synced, should update content editor');
    }
}

// 工具栏函数
function addNode() {
    outlineEditor.addNode();
}

function deleteNode() {
    outlineEditor.deleteNode();
}

function expandAll() {
    outlineEditor.expandAll();
}

function collapseAll() {
    outlineEditor.collapseAll();
}

// 创建全局实例
window.outlineEditor = new OutlineEditor();