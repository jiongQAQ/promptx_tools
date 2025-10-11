#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成系统高并发保障设计图
专业版本：线条严格垂直对齐，尺寸足够大确保清晰度
"""

import os
from pathlib import Path


def generate_high_concurrency_diagram():
    """生成高并发保障设计图（SVG格式，高清大尺寸，黑白风格，基于源码）"""

    # 大尺寸确保清晰度
    width = 2000
    height = 1300

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

    # 标题
    title_y = 60
    svg_lines.append(f'  <text x="{width/2}" y="{title_y}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="36" font-weight="bold" fill="#333">系统高并发保障设计</text>')

    # 整体布局：上方客户端，中间网关，下方四大保障模块

    # ===== 顶部：客户端层 =====
    client_y = 150
    client_width = 200
    client_height = 80
    client_x = width / 2 - client_width / 2

    svg_lines.append(f'  <rect x="{client_x}" y="{client_y}" width="{client_width}" height="{client_height}" fill="#ffffff" stroke="#333" stroke-width="3" rx="8"/>')
    svg_lines.append(f'  <text x="{width/2}" y="{client_y + 35}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="24" font-weight="bold" fill="#333">客户端请求</text>')
    svg_lines.append(f'  <text x="{width/2}" y="{client_y + 60}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="16" fill="#666">高并发流量</text>')

    # 垂直线从客户端到网关（严格垂直）
    line1_x = width / 2
    line1_y1 = client_y + client_height
    line1_y2 = 320
    svg_lines.append(f'  <line x1="{line1_x}" y1="{line1_y1}" x2="{line1_x}" y2="{line1_y2}" stroke="#333" stroke-width="3" marker-end="url(#arrowhead)"/>')

    # ===== 中间：API网关层 =====
    gateway_y = 320
    gateway_width = 320
    gateway_height = 100
    gateway_x = width / 2 - gateway_width / 2

    svg_lines.append(f'  <rect x="{gateway_x}" y="{gateway_y}" width="{gateway_width}" height="{gateway_height}" fill="#f5f5f5" stroke="#333" stroke-width="3" rx="8"/>')
    svg_lines.append(f'  <text x="{width/2}" y="{gateway_y + 40}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="26" font-weight="bold" fill="#333">API网关</text>')
    svg_lines.append(f'  <text x="{width/2}" y="{gateway_y + 70}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="18" fill="#666">SpringCloud Gateway</text>')

    # ===== 底部：四大保障模块（水平排列）=====
    module_y = 550
    module_width = 380
    module_height = 650
    module_spacing = 80

    # 计算四个模块的起始位置（居中）
    total_width = module_width * 4 + module_spacing * 3
    start_x = (width - total_width) / 2

    # 基于源码的实际技术
    modules = [
        {
            "title": "Sentinel限流",
            "x": start_x,
            "items": [
                {"name": "SentinelWebInterceptor", "desc": "Web拦截器"},
                {"name": "流量控制", "desc": "QPS限流"},
                {"name": "熔断降级", "desc": "快速失败"},
                {"name": "系统保护", "desc": "负载保护"}
            ]
        },
        {
            "title": "Redis缓存",
            "x": start_x + module_width + module_spacing,
            "items": [
                {"name": "Token缓存", "desc": "7天过期"},
                {"name": "用户信息缓存", "desc": "减少DB查询"},
                {"name": "RedisTemplate", "desc": "统一操作接口"},
                {"name": "Jedis连接池", "desc": "连接复用"}
            ]
        },
        {
            "title": "RabbitMQ异步",
            "x": start_x + (module_width + module_spacing) * 2,
            "items": [
                {"name": "延迟队列", "desc": "订单超时"},
                {"name": "死信队列", "desc": "自动取消"},
                {"name": "库存恢复", "desc": "异步处理"},
                {"name": "消息确认机制", "desc": "可靠投递"}
            ]
        },
        {
            "title": "数据库优化",
            "x": start_x + (module_width + module_spacing) * 3,
            "items": [
                {"name": "HikariCP连接池", "desc": "最大15连接"},
                {"name": "服务拆分隔离", "desc": "5个独立库"},
                {"name": "索引优化", "desc": "查询加速"},
                {"name": "MyBatis缓存", "desc": "SQL优化"}
            ]
        }
    ]

    # 从网关到四个模块的垂直连接线（严格垂直）
    gateway_bottom_y = gateway_y + gateway_height
    connector_y = module_y - 50  # 中间转折点

    for i, module in enumerate(modules):
        module_center_x = module["x"] + module_width / 2

        # 垂直线段1：从网关底部中心向下
        if i == 0:
            svg_lines.append(f'  <line x1="{width/2}" y1="{gateway_bottom_y}" x2="{width/2}" y2="{connector_y}" stroke="#333" stroke-width="3"/>')

        # 水平分支线：从中心点到各模块顶部
        svg_lines.append(f'  <line x1="{width/2}" y1="{connector_y}" x2="{module_center_x}" y2="{connector_y}" stroke="#333" stroke-width="3"/>')

        # 垂直线段2：从分支点到模块顶部（严格垂直）
        svg_lines.append(f'  <line x1="{module_center_x}" y1="{connector_y}" x2="{module_center_x}" y2="{module_y}" stroke="#333" stroke-width="3" marker-end="url(#arrowhead)"/>')

    # 绘制四个模块
    for module in modules:
        x = module["x"]

        # 模块外框（黑白风格）
        svg_lines.append(f'  <rect x="{x}" y="{module_y}" width="{module_width}" height="{module_height}" fill="#f9f9f9" stroke="#333" stroke-width="4" rx="10"/>')

        # 模块标题
        title_y = module_y + 50
        svg_lines.append(f'  <text x="{x + module_width/2}" y="{title_y}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="28" font-weight="bold" fill="#333">{module["title"]}</text>')

        # 分隔线
        sep_y = title_y + 30
        svg_lines.append(f'  <line x1="{x + 30}" y1="{sep_y}" x2="{x + module_width - 30}" y2="{sep_y}" stroke="#666" stroke-width="2"/>')

        # 策略列表
        item_start_y = sep_y + 60
        item_height = 120

        for j, item in enumerate(module["items"]):
            item_y = item_start_y + j * item_height

            # 策略框（黑白风格）
            svg_lines.append(f'  <rect x="{x + 30}" y="{item_y}" width="{module_width - 60}" height="100" fill="#ffffff" stroke="#666" stroke-width="2" rx="6"/>')

            # 策略名称
            svg_lines.append(f'  <text x="{x + module_width/2}" y="{item_y + 35}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="20" font-weight="bold" fill="#333">{item["name"]}</text>')

            # 策略描述
            svg_lines.append(f'  <text x="{x + module_width/2}" y="{item_y + 65}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="16" fill="#666">{item["desc"]}</text>')

    svg_lines.append('</svg>')

    return '\n'.join(svg_lines)


def main():
    """主函数"""
    # 输出目录
    output_dir = Path(__file__).parent.parent / 'paper' / 'assets' / 'diagrams' / 'uml'
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*70}")
    print(f"🎨 开始生成系统高并发保障设计图（高清专业版）")
    print(f"📁 输出目录: {output_dir}")
    print(f"{'='*70}\n")

    # 生成SVG
    svg_content = generate_high_concurrency_diagram()
    svg_path = output_dir / 'high-concurrency-design.svg'

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print(f"✅ 生成: high-concurrency-design.svg (2000x1300)")
    print(f"📊 特点: 黑白风格 | 基于源码 | 线条严格垂直 | 高清大尺寸")

    # 同时保留PNG作为备份（后续可以用工具转换）
    print(f"\n💡 提示: SVG格式已生成，可导出为高清PNG")
    print(f"   命令: 使用图像工具将SVG转为PNG（推荐分辨率2000x1400以上）")

    print(f"\n{'='*70}")
    print(f"✅ 生成完成！")
    print(f"🎯 改进: 黑白配色 | 源码验证 | 线条垂直 | 尺寸2000x1300")
    print(f"📋 技术: Sentinel | Redis | RabbitMQ | HikariCP（均基于源码）")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
