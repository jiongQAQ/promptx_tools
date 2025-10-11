#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成论文结构图
参考用户提供的样式，使用虚线框分隔各章节
"""

import os
from pathlib import Path


def generate_paper_structure_diagram():
    """生成论文结构图（SVG格式，黑白风格，虚线框）"""

    # 画布尺寸
    width = 1400
    height = 2400

    svg_lines = []
    svg_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg_lines.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
    svg_lines.append(f'  <rect width="{width}" height="{height}" fill="#ffffff"/>')

    # 定义样式
    svg_lines.append('  <defs>')
    svg_lines.append('    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">')
    svg_lines.append('      <polygon points="0 0, 10 3, 0 6" fill="#333"/>')
    svg_lines.append('    </marker>')
    svg_lines.append('  </defs>')

    # 论文章节结构（确保标题干净，无特殊字符）
    sections = [
        {
            "title": "绪论",
            "subsections": ["研究背景与意义", "国内外研究现状", "研究目标与内容", "论文组织结构"]
        },
        {
            "title": "系统相关技术与理论基础",
            "subsections": ["B/S架构", "Java语言简介", "MySQL数据库", "SSM框架体系",
                          "微服务架构概述", "SpringCloud技术栈", "分布式系统理论", "Vue前端技术"]
        },
        {
            "title": "系统分析与总体规划",
            "subsections": ["系统可行性分析", "功能需求分析", "非功能需求分析", "系统架构规划", "微服务拆分策略"]
        },
        {
            "title": "系统设计",
            "subsections": ["技术栈选型与总体功能设计", "数据库设计", "微服务核心功能模块设计",
                          "微服务治理与基础设施设计", "系统高并发保障设计"]
        },
        {
            "title": "系统核心功能实现",
            "subsections": ["开发环境与工具配置", "微服务基础功能模块实现",
                          "微服务治理与基础设施实现", "系统高并发保障实现"]
        },
        {
            "title": "系统测试与验证",
            "subsections": ["测试环境与策略", "功能测试", "性能测试", "可靠性测试"]
        },
        {
            "title": "结语",
            "subsections": ["研究成果总结", "系统特色与创新", "存在问题与不足", "未来发展方向"]
        }
    ]

    # 每个章节的高度和间距
    section_spacing = 50
    start_y = 50
    current_y = start_y

    for section in sections:
        # 计算当前章节需要的高度
        # 主标题框：80px，子节点：每个50px，间距：20px
        num_subsections = len(section["subsections"])
        # 根据子节点数量自适应布局
        if num_subsections <= 4:
            # 单行布局
            subsection_rows = 1
            subsections_per_row = num_subsections
        elif num_subsections <= 6:
            # 两行布局
            subsection_rows = 2
            subsections_per_row = (num_subsections + 1) // 2
        else:
            # 多行布局
            subsection_rows = 3
            subsections_per_row = (num_subsections + 2) // 3

        # 计算章节高度
        section_height = 80 + 50 + (subsection_rows * 60) + 40  # 标题+间距+子节点行+底部间距

        # 绘制虚线外框
        svg_lines.append(f'  <rect x="50" y="{current_y}" width="{width - 100}" height="{section_height}" '
                        f'fill="none" stroke="#333" stroke-width="2" stroke-dasharray="8,4" rx="0"/>')

        # 绘制章节标题框
        title_width = 500
        title_height = 80
        title_x = (width - title_width) / 2
        title_y = current_y + 20

        svg_lines.append(f'  <rect x="{title_x}" y="{title_y}" width="{title_width}" height="{title_height}" '
                        f'fill="#ffffff" stroke="#333" stroke-width="3" rx="0"/>')
        svg_lines.append(f'  <text x="{width/2}" y="{title_y + title_height/2 + 8}" text-anchor="middle" '
                        f'font-family="Microsoft YaHei, SimHei, Arial" font-size="28" font-weight="bold" fill="#333">'
                        f'{section["title"]}</text>')

        # 绘制从标题到子节点的箭头
        arrow_start_y = title_y + title_height
        subsection_start_y = arrow_start_y + 50

        # 中心垂直线
        svg_lines.append(f'  <line x1="{width/2}" y1="{arrow_start_y}" x2="{width/2}" y2="{subsection_start_y - 10}" '
                        f'stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>')

        # 绘制子节点
        subsection_width = 220
        subsection_height = 50

        for row in range(subsection_rows):
            # 计算当前行的子节点数量
            start_idx = row * subsections_per_row
            end_idx = min(start_idx + subsections_per_row, num_subsections)
            current_row_count = end_idx - start_idx

            # 计算当前行的起始X坐标（居中）
            total_width = current_row_count * subsection_width + (current_row_count - 1) * 30
            row_start_x = (width - total_width) / 2

            for i, subsection in enumerate(section["subsections"][start_idx:end_idx]):
                sub_x = row_start_x + i * (subsection_width + 30)
                sub_y = subsection_start_y + row * 60

                # 绘制子节点框
                svg_lines.append(f'  <rect x="{sub_x}" y="{sub_y}" width="{subsection_width}" height="{subsection_height}" '
                                f'fill="#ffffff" stroke="#333" stroke-width="2" rx="0"/>')

                # 绘制子节点文本（自动换行处理）
                if len(subsection) > 10:
                    # 长文本分两行
                    mid = len(subsection) // 2
                    line1 = subsection[:mid]
                    line2 = subsection[mid:]
                    svg_lines.append(f'  <text x="{sub_x + subsection_width/2}" y="{sub_y + subsection_height/2 - 5}" '
                                    f'text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="16" fill="#333">'
                                    f'{line1}</text>')
                    svg_lines.append(f'  <text x="{sub_x + subsection_width/2}" y="{sub_y + subsection_height/2 + 15}" '
                                    f'text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="16" fill="#333">'
                                    f'{line2}</text>')
                else:
                    svg_lines.append(f'  <text x="{sub_x + subsection_width/2}" y="{sub_y + subsection_height/2 + 6}" '
                                    f'text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="16" fill="#333">'
                                    f'{subsection}</text>')

        # 更新Y坐标到下一章节
        current_y += section_height + section_spacing

        # 如果不是最后一个章节，绘制章节间的箭头
        if section != sections[-1]:
            arrow_y = current_y - section_spacing / 2
            svg_lines.append(f'  <line x1="{width/2}" y1="{arrow_y - 15}" x2="{width/2}" y2="{arrow_y + 15}" '
                            f'stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>')

    svg_lines.append('</svg>')

    return '\n'.join(svg_lines)


def main():
    """主函数"""
    # 输出目录
    output_dir = Path(__file__).parent.parent / 'paper' / 'assets' / 'diagrams' / 'uml'
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*70}")
    print(f"🎨 开始生成论文结构图")
    print(f"📁 输出目录: {output_dir}")
    print(f"{'='*70}\n")

    # 生成SVG
    svg_content = generate_paper_structure_diagram()
    svg_path = output_dir / 'paper-structure.svg'

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print(f"✅ 生成: paper-structure.svg (1400x2400)")
    print(f"📊 特点: 黑白风格 | 虚线框分隔 | 7个章节 | 自适应布局")

    print(f"\n{'='*70}")
    print(f"✅ 生成完成！")
    print(f"📋 章节: 绪论 → 技术基础 → 需求分析 → 系统设计 → 功能实现 → 测试验证 → 结语")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
