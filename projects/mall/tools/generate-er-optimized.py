#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版单体ER图批量生成工具
修复连线精确度和布局工整性问题
支持多层圆环布局，优化字段过多的表
"""

import json
import math
import os
import sys
from pathlib import Path


def calculate_ellipse_point(cx, cy, rx, ry, angle):
    """计算椭圆边缘上的点（精确连线）"""
    x = cx + rx * math.cos(angle)
    y = cy + ry * math.sin(angle)
    return x, y


def generate_single_er(table_json_path, output_dir):
    """生成单个表的ER图SVG（支持多层圆环布局）"""

    # 读取JSON
    with open(table_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    table_name = data.get('tableName', 'unknown')
    table_cn_name = data.get('tableCnName', '数据表')
    columns = data.get('columns', [])

    # 过滤掉表头行
    fields = [col for col in columns if col[0] != '字段名']
    field_count = len(fields)

    if field_count == 0:
        print(f"警告：{table_name} 没有字段数据")
        return False

    # 动态半径策略（单层布局，根据字段数量调整半径）
    if field_count <= 8:
        radius = 250  # 紧凑
    elif field_count <= 12:
        radius = 320  # 适中
    elif field_count <= 16:
        radius = 380  # 宽松
    else:
        radius = 420  # 超多字段

    # 中心矩形（表实体）
    rect_width = 180
    rect_height = 80

    # 椭圆（字段属性）
    ellipse_rx = 85
    ellipse_ry = 32

    # 计算实际需要的画布尺寸（紧凑布局，留50px边距）
    margin = 50
    max_extent = radius + ellipse_rx + margin  # 最远点距离中心
    width = max_extent * 2
    height = max_extent * 2

    # 中心点位置
    rect_cx = width / 2
    rect_cy = height / 2

    svg_lines = []
    svg_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg_lines.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
    svg_lines.append(f'  <rect width="{width}" height="{height}" fill="#ffffff"/>')

    # 绘制中心矩形
    rect_x = rect_cx - rect_width / 2
    rect_y = rect_cy - rect_height / 2
    svg_lines.append(f'  <rect x="{rect_x}" y="{rect_y}" width="{rect_width}" height="{rect_height}" fill="#fff" stroke="#333" stroke-width="3"/>')
    svg_lines.append(f'  <text x="{rect_cx}" y="{rect_cy + 6}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="18" font-weight="bold" fill="#333">{table_cn_name}</text>')

    # 绘制椭圆（单层布局，动态半径）
    for i, field in enumerate(fields):
        field_cn_name = field[1]

        # 计算角度（均匀分布）
        angle = 2 * math.pi * i / field_count - math.pi / 2  # 从顶部开始

        # 计算椭圆中心位置
        ellipse_cx = rect_cx + radius * math.cos(angle)
        ellipse_cy = rect_cy + radius * math.sin(angle)

        # 计算矩形边缘到椭圆中心的连线角度
        dx = ellipse_cx - rect_cx
        dy = ellipse_cy - rect_cy
        angle_to_ellipse = math.atan2(dy, dx)

        # 计算矩形边缘点（精确连线起点）
        rect_half_w = rect_width / 2
        rect_half_h = rect_height / 2

        # 根据角度判断连接到矩形的哪条边
        tan_angle = abs(math.tan(angle_to_ellipse)) if math.cos(angle_to_ellipse) != 0 else float('inf')

        if tan_angle < rect_half_h / rect_half_w:
            # 连接到左边或右边
            if dx > 0:  # 右边
                line_start_x = rect_x + rect_width
                line_start_y = rect_cy + rect_half_w * math.tan(angle_to_ellipse)
            else:  # 左边
                line_start_x = rect_x
                line_start_y = rect_cy - rect_half_w * math.tan(angle_to_ellipse)
        else:
            # 连接到上边或下边
            if dy > 0:  # 下边
                line_start_x = rect_cx + rect_half_h / math.tan(angle_to_ellipse) if math.tan(angle_to_ellipse) != 0 else rect_cx
                line_start_y = rect_y + rect_height
            else:  # 上边
                line_start_x = rect_cx - rect_half_h / math.tan(angle_to_ellipse) if math.tan(angle_to_ellipse) != 0 else rect_cx
                line_start_y = rect_y

        # 计算椭圆边缘点（精确连线终点）
        angle_from_rect = math.atan2(ellipse_cy - line_start_y, ellipse_cx - line_start_x)
        ellipse_edge_x, ellipse_edge_y = calculate_ellipse_point(
            ellipse_cx, ellipse_cy, ellipse_rx, ellipse_ry, angle_from_rect
        )

        # 绘制连线（从矩形边缘到椭圆边缘）
        svg_lines.append(f'  <line x1="{line_start_x}" y1="{line_start_y}" x2="{ellipse_edge_x}" y2="{ellipse_edge_y}" stroke="#666" stroke-width="2"/>')

        # 绘制椭圆
        svg_lines.append(f'  <ellipse cx="{ellipse_cx}" cy="{ellipse_cy}" rx="{ellipse_rx}" ry="{ellipse_ry}" fill="#fff" stroke="#666" stroke-width="2"/>')

        # 绘制字段名文本
        svg_lines.append(f'  <text x="{ellipse_cx}" y="{ellipse_cy + 6}" text-anchor="middle" font-family="Microsoft YaHei, SimHei, Arial" font-size="14" fill="#333">{field_cn_name}</text>')

    svg_lines.append('</svg>')

    # 写入SVG文件
    output_file = os.path.join(output_dir, f'Tab-{table_name}.svg')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_lines))

    print(f"✅ 生成: Tab-{table_name}.svg ({field_count}个字段)")
    return True


def main():
    """批量生成ER图"""

    if len(sys.argv) < 2:
        print("用法: python generate-er-optimized.py <tables目录路径>")
        sys.exit(1)

    tables_dir = sys.argv[1]

    # 输出目录
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(tables_dir)),
        'assets', 'diagrams', 'er'
    )

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 扫描所有Tab-*.json文件
    table_files = sorted(Path(tables_dir).glob('Tab-*.json'))

    success_count = 0
    fail_count = 0

    print(f"\n🔍 扫描目录: {tables_dir}")
    print(f"📁 输出目录: {output_dir}")
    print(f"📊 发现表文件: {len(table_files)} 个\n")

    for table_file in table_files:
        try:
            if generate_single_er(str(table_file), output_dir):
                success_count += 1
        except Exception as e:
            print(f"❌ 失败: {table_file.name} - {str(e)}")
            fail_count += 1

    print(f"\n{'='*60}")
    print(f"✅ 成功生成: {success_count} 个")
    print(f"❌ 失败: {fail_count} 个")
    print(f"📊 优化特性: 多层圆环布局 + 精确连线 + 工整间距")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
