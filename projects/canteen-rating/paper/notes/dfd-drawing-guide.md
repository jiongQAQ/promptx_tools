# 数据流图绘制参考

## 问题记录

### 问题1：PlantUML无法实现水平布局
- **现象**：使用`left to right direction`后仍然是垂直布局
- **尝试方案**：
  - 使用`left to right direction` ❌
  - 使用`-[hidden]right-`强制布局 ❌
  - 使用`!pragma layout smetana` ✅ 但有弯曲线条

### 问题2：PlantUML线条弯曲
- **现象**：使用smetana引擎后线条是曲线而非直线
- **尝试方案**：
  - 添加`skinparam linetype ortho` ❌ 无效
  - 调整nodesep和ranksep ❌ 线条依然弯曲

### 问题3：文字标签重叠
- **现象**：数据流标签重叠在一起
- **解决方案**：
  - 增大padding和间距
  - 简化标签文字
  - 使用Graphviz的xlabel属性

## 最终解决方案

### 使用Graphviz DOT格式

**优点：**
- ✅ 完全直线布局（ortho模式）
- ✅ 精确控制节点间距
- ✅ 标签位置灵活

**核心代码：**
```dot
digraph dfd_top_level {
    graph [
        rankdir=LR              // 水平布局
        nodesep=2.5             // 节点间距
        ranksep=4.0             // 等级间距
        pad=1.5                 // 边距留白
        splines=ortho           // 直线布局！
    ];

    // 外部实体（矩形）
    Admin [shape=box, style=rounded];

    // 处理过程（椭圆）
    System [shape=ellipse];

    // 数据流（使用xlabel避免重叠）
    Admin -> System [xlabel="管理员指令"];
}
```

## 渲染命令

```bash
# 生成PNG
dot -Tpng dfd.dot -o dfd.png

# 高分辨率
dot -Tpng -Gdpi=300 dfd.dot -o dfd.png
```

## 关键参数说明

| 参数 | 作用 | 推荐值 |
|------|------|--------|
| `rankdir=LR` | 水平布局 | LR（左到右） |
| `splines=ortho` | 直线模式 | ortho |
| `nodesep` | 同级节点间距 | 2.0-3.0 |
| `ranksep` | 不同级间距 | 3.0-4.0 |
| `pad` | 图片边距 | 1.0-1.5 |
| `xlabel` | 外部标签 | 用于ortho模式 |

## 经验总结

1. **直线布局必须用Graphviz**，PlantUML无法实现真正的ortho直线
2. **标签使用xlabel**，label在ortho模式下不支持
3. **留白很重要**，pad、nodesep、ranksep都要设置足够大
4. **中文字体**记得设置`fontname="Microsoft YaHei"`

## 文件位置

- DOT源文件：`paper/assets/diagrams/dfd/dfd-top-level.dot`
- PNG输出：`paper/assets/diagrams/dfd/dfd-top-level.png`
- PlantUML备份：`paper/assets/plantuml/dfd-top-level.puml`（仅作参考）