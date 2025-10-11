#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成框架组件选型图（SSM和SpringCloud）
黑白无颜色风格，简洁版本（无底部说明）
"""

import os
from pathlib import Path


def generate_ssm_diagram():
    """生成SSM框架组件选型图（简洁版）"""

    width = 900
    height = 350

    svg_lines = []
    svg_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg_lines.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
    svg_lines.append(f'  <rect width="{width}" height="{height}" fill="#ffffff"/>')

    # 标题框（顶部）
    title_width = 450
    title_height = 70
    title_x = (width - title_width) / 2
    title_y = 20

    svg_lines.append(f'  <rect x="{title_x}" y="{title_y}" width="{title_width}" height="{title_height}" fill="#f0f0f0" stroke="#333" stroke-width="2" rx="5"/>')
    svg_lines.append(f'  <text x="{width/2}" y="{title_y + title_height/2 + 8}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="24" font-weight="bold" fill="#333">SSM框架体系</text>')

    # 三大组件模块
    module_width = 240
    module_height = 120
    module_spacing = 40
    start_y = 170

    # 计算三个模块的起始X坐标（居中分布）
    total_width = module_width * 3 + module_spacing * 2
    start_x = (width - total_width) / 2

    modules = [
        {"name": "Spring", "desc": "IoC容器 / AOP", "x": start_x},
        {"name": "SpringMVC", "desc": "Web框架", "x": start_x + module_width + module_spacing},
        {"name": "MyBatis", "desc": "持久层框架", "x": start_x + (module_width + module_spacing) * 2}
    ]

    # 从标题到模块的连接线
    for i, module in enumerate(modules):
        line_start_x = width / 2
        line_start_y = title_y + title_height
        line_end_x = module["x"] + module_width / 2
        line_end_y = start_y

        svg_lines.append(f'  <line x1="{line_start_x}" y1="{line_start_y}" x2="{line_end_x}" y2="{line_end_y}" stroke="#666" stroke-width="2"/>')

    # 绘制三个模块
    for module in modules:
        x = module["x"]
        y = start_y

        # 模块外框
        svg_lines.append(f'  <rect x="{x}" y="{y}" width="{module_width}" height="{module_height}" fill="#fff" stroke="#333" stroke-width="2" rx="5"/>')

        # 模块名称
        svg_lines.append(f'  <text x="{x + module_width/2}" y="{y + 45}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="20" font-weight="bold" fill="#333">{module["name"]}</text>')

        # 模块描述
        svg_lines.append(f'  <text x="{x + module_width/2}" y="{y + 78}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="15" fill="#666">{module["desc"]}</text>')

    svg_lines.append('</svg>')

    return '\n'.join(svg_lines)


def generate_springcloud_diagram():
    """生成SpringCloud组件选型图（单行布局，简洁版）"""

    width = 1760
    height = 400

    svg_lines = []
    svg_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg_lines.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
    svg_lines.append(f'  <rect width="{width}" height="{height}" fill="#ffffff"/>')

    # 标题框
    title_width = 550
    title_height = 75
    title_x = (width - title_width) / 2
    title_y = 20

    svg_lines.append(f'  <rect x="{title_x}" y="{title_y}" width="{title_width}" height="{title_height}" fill="#f0f0f0" stroke="#333" stroke-width="3" rx="5"/>')
    svg_lines.append(f'  <text x="{width/2}" y="{title_y + title_height/2 + 10}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="28" font-weight="bold" fill="#333">SpringCloud组件选型</text>')

    # 7大功能模块（单行排列）
    module_width = 200
    module_height = 150
    spacing_x = 50

    modules_y = 145
    modules = [
        {"category": "服务注册中心", "components": [{"name": "Nacos", "selected": True}, {"name": "Eureka", "selected": False}]},
        {"category": "服务负载均衡", "components": [{"name": "LoadBalancer", "selected": True}, {"name": "Ribbon", "selected": False}]},
        {"category": "服务熔断降级", "components": [{"name": "Sentinel", "selected": True}, {"name": "Hystrix", "selected": False}]},
        {"category": "服务调用", "components": [{"name": "OpenFeign", "selected": True}, {"name": "Feign", "selected": False}]},
        {"category": "服务网关", "components": [{"name": "GateWay", "selected": True}, {"name": "Zuul", "selected": False}]},
        {"category": "分布式事务", "components": [{"name": "Seata", "selected": True}, {"name": "TCC", "selected": False}]},
        {"category": "服务监控", "components": [{"name": "SpringBootAdmin", "selected": True}, {"name": "Zipkin", "selected": False}]}
    ]

    # 计算起始位置（居中）
    total_width = module_width * 7 + spacing_x * 6
    start_x = (width - total_width) / 2

    # 绘制7个模块
    for i, module in enumerate(modules):
        x = start_x + i * (module_width + spacing_x)
        y = modules_y

        # 从标题连线到模块
        svg_lines.append(f'  <line x1="{width/2}" y1="{title_y + title_height}" x2="{x + module_width/2}" y2="{y - 25}" stroke="#666" stroke-width="2"/>')

        # 模块类别标签
        svg_lines.append(f'  <rect x="{x}" y="{y - 25}" width="{module_width}" height="30" fill="#e0e0e0" stroke="#666" stroke-width="1" rx="3"/>')
        svg_lines.append(f'  <text x="{x + module_width/2}" y="{y - 7}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="14" font-weight="bold" fill="#333">{module["category"]}</text>')

        # 组件选项框
        component_start_y = y + 15
        for j, comp in enumerate(module["components"]):
            comp_y = component_start_y + j * 60

            # 组件框
            fill_color = "#fff"  # 统一白色背景
            stroke_width = "2" if comp["selected"] else "1"

            svg_lines.append(f'  <rect x="{x + 10}" y="{comp_y}" width="{module_width - 20}" height="50" fill="{fill_color}" stroke="#666" stroke-width="{stroke_width}" rx="3"/>')

            # 勾选标记（已选组件）
            if comp["selected"]:
                check_x = x + 25
                check_y = comp_y + 25
                svg_lines.append(f'  <circle cx="{check_x}" cy="{check_y}" r="9" fill="none" stroke="#333" stroke-width="2"/>')
                svg_lines.append(f'  <path d="M {check_x-4} {check_y} L {check_x-1} {check_y+4} L {check_x+5} {check_y-5}" stroke="#333" stroke-width="2" fill="none"/>')
            else:
                # 未选标记
                check_x = x + 25
                check_y = comp_y + 25
                svg_lines.append(f'  <circle cx="{check_x}" cy="{check_y}" r="9" fill="none" stroke="#333" stroke-width="1"/>')
                svg_lines.append(f'  <line x1="{check_x-5}" y1="{check_y-5}" x2="{check_x+5}" y2="{check_y+5}" stroke="#333" stroke-width="1"/>')
                svg_lines.append(f'  <line x1="{check_x-5}" y1="{check_y+5}" x2="{check_x+5}" y2="{check_y-5}" stroke="#333" stroke-width="1"/>')

            # 组件名称
            text_color = "#333"  # 统一黑色文字
            font_weight = "bold" if comp["selected"] else "normal"
            svg_lines.append(f'  <text x="{x + 48}" y="{comp_y + 31}" font-family="Microsoft YaHei, SimHei, Arial" font-size="16" font-weight="{font_weight}" fill="{text_color}">{comp["name"]}</text>')

    svg_lines.append('</svg>')

    return '\n'.join(svg_lines)


def main():
    """主函数"""
    # 输出目录
    output_dir = Path(__file__).parent.parent / 'paper' / 'assets' / 'diagrams' / 'uml'
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"🎨 开始生成框架组件选型图（简洁版）")
    print(f"📁 输出目录: {output_dir}")
    print(f"{'='*60}\n")

    # 生成SSM框架图
    ssm_svg = generate_ssm_diagram()
    ssm_path = output_dir / 'SSM-Framework.svg'
    with open(ssm_path, 'w', encoding='utf-8') as f:
        f.write(ssm_svg)
    print(f"✅ 生成: SSM-Framework.svg (900x350)")

    # 生成SpringCloud框架图
    springcloud_svg = generate_springcloud_diagram()
    springcloud_path = output_dir / 'SpringCloud-Components.svg'
    with open(springcloud_path, 'w', encoding='utf-8') as f:
        f.write(springcloud_svg)
    print(f"✅ 生成: SpringCloud-Components.svg (1760x400)")

    print(f"\n{'='*60}")
    print(f"✅ 生成完成！共2个图表文件")
    print(f"🎯 优化特点: 单行布局 | 无底部说明 | 更简洁")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
