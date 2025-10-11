#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用SVG绘制系统业务流程图
精确控制，完美对齐
"""

import os
from pathlib import Path as PathLib


def create_svg_flowchart():
    """创建SVG流程图"""

    # SVG画布大小
    width = 2000
    height = 1400

    svg_lines = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        '<defs>',
        # 定义箭头标记
        '<marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">',
        '<polygon points="0 0, 10 5, 0 10" fill="black"/>',
        '</marker>',
        '</defs>',
        # 白色背景
        f'<rect width="{width}" height="{height}" fill="white"/>',
    ]

    # 样式定义
    rect_style = 'fill:white;stroke:black;stroke-width:2'
    diamond_style = 'fill:white;stroke:black;stroke-width:2'
    rounded_style = 'fill:white;stroke:black;stroke-width:2'
    text_style = 'font-family:Microsoft YaHei,SimHei,Arial;font-size:16px;text-anchor:middle'
    line_style = 'stroke:black;stroke-width:2;fill:none;marker-end:url(#arrowhead)'
    label_style = 'font-family:Microsoft YaHei,SimHei,Arial;font-size:14px;font-weight:bold;text-anchor:middle'

    # ============ 辅助函数 ============
    def rect(x, y, w, h, text, text_dy=0):
        """绘制矩形"""
        svg_lines.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" style="{rect_style}"/>')
        if '\n' in text:
            lines = text.split('\n')
            for i, line in enumerate(lines):
                ty = y + (i - (len(lines)-1)/2) * 20
                svg_lines.append(f'<text x="{x}" y="{ty + 5}" style="{text_style}">{line}</text>')
        else:
            svg_lines.append(f'<text x="{x}" y="{y + 6 + text_dy}" style="{text_style}">{text}</text>')

    def rounded_rect(x, y, w, h, text):
        """绘制圆角矩形"""
        svg_lines.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="15" ry="15" style="{rounded_style}"/>')
        svg_lines.append(f'<text x="{x}" y="{y + 6}" style="{text_style}">{text}</text>')

    def diamond(x, y, w, h, text):
        """绘制菱形"""
        points = f"{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}"
        svg_lines.append(f'<polygon points="{points}" style="{diamond_style}"/>')
        if '\n' in text:
            lines = text.split('\n')
            for i, line in enumerate(lines):
                ty = y + (i - (len(lines)-1)/2) * 18
                svg_lines.append(f'<text x="{x}" y="{ty + 5}" style="{text_style};font-size:15px">{line}</text>')
        else:
            svg_lines.append(f'<text x="{x}" y="{y + 5}" style="{text_style};font-size:15px">{text}</text>')

    def arrow(x1, y1, x2, y2, label='', label_offset=(0, 0)):
        """绘制箭头"""
        svg_lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="{line_style}"/>')
        if label:
            lx = (x1 + x2) / 2 + label_offset[0]
            ly = (y1 + y2) / 2 + label_offset[1]
            svg_lines.append(f'<text x="{lx}" y="{ly}" style="{label_style}">{label}</text>')

    # ============ 绘制流程图 ============

    # 顶部公共流程
    rounded_rect(1000, 80, 120, 50, '开始')
    arrow(1000, 105, 1000, 140)

    rect(1000, 165, 120, 50, '系统登录')
    arrow(1000, 190, 1000, 225)

    diamond(1000, 255, 140, 60, '是否注册?')
    arrow(1000, 285, 1000, 320, label='Y')
    arrow(1070, 255, 1200, 255, label='N')

    rect(1270, 255, 140, 50, '注册账号')
    arrow(1270, 280, 1270, 340)
    arrow(1270, 340, 1000, 340)
    arrow(1000, 340, 1000, 320)

    # 核心分支点：普通用户/管理员
    diamond(1000, 365, 180, 60, '普通用户/\n管理员?')

    # ========== 左侧：普通用户端 ==========
    user_x = 500
    arrow(910, 365, user_x + 150, 365, label='普通用户', label_offset=(0, -15))

    y = 365
    rect(user_x, y, 160, 60, '输入用户名和\n密码获取验证码')
    arrow(user_x, y + 30, user_x, y + 75)

    y = y + 110
    diamond(user_x, y, 160, 60, '验证登录\n合法性?')
    arrow(user_x, y + 30, user_x, y + 75, label='Y')
    # 重新输入循环
    arrow(user_x - 80, y, user_x - 150, y, label='N')
    arrow(user_x - 150, y, user_x - 150, 365)
    arrow(user_x - 150, 365, user_x - 80, 365)
    svg_lines.append(f'<text x="{user_x - 150}" y="{(y + 365)/2}" style="{label_style};font-size:12px">重新输入</text>')

    y = y + 105
    rect(user_x, y, 120, 50, '商品展示')
    arrow(user_x, y + 25, user_x, y + 65)

    y = y + 90
    rect(user_x, y, 120, 50, '选择商品')
    arrow(user_x, y + 25, user_x, y + 65)

    y = y + 90
    diamond(user_x, y, 120, 60, '是否购买?')
    arrow(user_x, y + 30, user_x, y + 75, label='Y')
    arrow(user_x + 60, y, user_x + 150, y, label='N')
    rect(user_x + 200, y, 120, 50, '继续浏览')

    # 并行路径
    y = y + 105
    left_x = user_x - 100
    right_x = user_x + 100

    svg_lines.append(f'<text x="{user_x - 150}" y="{y - 20}" style="{label_style};font-size:12px">运输</text>')

    rect(left_x, y, 120, 50, '直接购买商品')
    rect(right_x, y, 120, 50, '加入购物车')

    arrow(user_x, y - 75, left_x, y - 25)
    arrow(user_x, y - 75, right_x, y - 25)

    arrow(left_x, y + 25, left_x, y + 75)
    arrow(right_x, y + 25, right_x, y + 75)

    y = y + 100
    rect(left_x, y, 120, 60, '是否提送货\n上门')
    rect(right_x, y, 120, 50, '查看购物车')

    arrow(left_x, y + 30, left_x, y + 75)
    arrow(right_x, y + 25, right_x, y + 70)

    # 汇聚
    y = y + 100
    svg_lines.append(f'<text x="{left_x - 30}" y="{y - 15}" style="{label_style};font-size:12px">是</text>')
    arrow(left_x, y - 15, user_x, y - 15)
    arrow(right_x, y - 15, user_x, y - 15)
    arrow(user_x, y - 15, user_x, y - 50)

    rect(user_x, y, 120, 50, '提交订单')

    # ========== 右侧：管理端 ==========
    admin_x = 1500
    arrow(1090, 365, admin_x - 150, 365, label='管理员', label_offset=(0, -15))

    y = 365
    rect(admin_x, y, 160, 60, '输入用户名和\n密码获取验证码')
    arrow(admin_x, y + 30, admin_x, y + 75)

    y = y + 110
    diamond(admin_x, y, 160, 60, '验证登录\n合法性?')
    arrow(admin_x, y + 30, admin_x, y + 75, label='Y')
    # 重新输入循环
    arrow(admin_x + 80, y, admin_x + 150, y, label='N')
    arrow(admin_x + 150, y, admin_x + 150, 365)
    arrow(admin_x + 150, 365, admin_x + 80, 365)
    svg_lines.append(f'<text x="{admin_x + 150}" y="{(y + 365)/2}" style="{label_style};font-size:12px">重新输入</text>')

    y = y + 105
    rect(admin_x, y, 140, 50, '用户信息管理')
    arrow(admin_x, y + 25, admin_x, y + 65)

    y = y + 90
    rect(admin_x, y, 140, 50, '商品信息管理')
    arrow(admin_x, y + 25, admin_x, y + 65)

    y = y + 90
    rect(admin_x, y, 140, 50, '订单管理')
    arrow(admin_x, y + 25, admin_x, y + 75)

    # 4个并行子功能
    y = y + 105
    sub1_x = admin_x - 210
    sub2_x = admin_x - 70
    sub3_x = admin_x + 70
    sub4_x = admin_x + 210

    rect(sub1_x, y, 100, 50, '查看订单')
    rect(sub2_x, y, 100, 50, '订单状态')
    rect(sub3_x, y, 100, 50, '删除订单')
    rect(sub4_x, y, 100, 50, '完成订单')

    arrow(admin_x, y - 75, sub1_x, y - 25)
    arrow(admin_x, y - 75, sub2_x, y - 25)
    arrow(admin_x, y - 75, sub3_x, y - 25)
    arrow(admin_x, y - 75, sub4_x, y - 25)

    arrow(sub1_x, y + 25, sub1_x, y + 70)
    arrow(sub2_x, y + 25, sub2_x, y + 70)
    arrow(sub3_x, y + 25, sub3_x, y + 70)
    arrow(sub4_x, y + 25, sub4_x, y + 70)

    y = y + 95
    arrow(sub1_x, y, admin_x, y)
    arrow(sub2_x, y, admin_x, y)
    arrow(sub3_x, y, admin_x, y)
    arrow(sub4_x, y, admin_x, y)
    arrow(admin_x, y, admin_x, y + 40)

    y = y + 65
    rect(admin_x, y, 140, 50, '首页配置管理')

    # ========== 底部汇聚 ==========
    final_y = 1200
    arrow(user_x, 930, user_x, final_y - 60)
    arrow(user_x, final_y - 60, 1000, final_y - 60)

    arrow(admin_x, y + 25, admin_x, final_y - 60)
    arrow(admin_x, final_y - 60, 1000, final_y - 60)

    arrow(1000, final_y - 60, 1000, final_y - 90)

    rect(1000, final_y, 120, 50, '退出登录')
    arrow(1000, final_y + 25, 1000, final_y + 65)

    rounded_rect(1000, final_y + 100, 120, 50, '结束')

    # 结束SVG
    svg_lines.append('</svg>')

    return '\n'.join(svg_lines)


def main():
    """主函数"""
    print(f"\n{'='*70}")
    print(f"🎨 开始生成系统业务流程图（SVG精确绘制）")
    print(f"📐 特点: 完美对齐 | 清晰箭头 | 专业样式")
    print(f"{'='*70}\n")

    # 生成SVG
    svg_content = create_svg_flowchart()

    # 保存SVG文件
    output_dir = PathLib(__file__).parent.parent / 'paper' / 'assets' / 'diagrams' / 'uml'
    os.makedirs(output_dir, exist_ok=True)
    svg_path = output_dir / 'system-flow-final.svg'

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print(f"✅ 生成SVG: {svg_path}")

    # 转换为PNG（需要cairosvg库）
    try:
        import cairosvg
        png_path = output_dir / 'system-flow-final.png'
        cairosvg.svg2png(bytestring=svg_content.encode('utf-8'),
                        write_to=str(png_path), scale=1.5)
        print(f"✅ 生成PNG: {png_path}")
    except ImportError:
        print(f"⚠️  未安装 cairosvg，跳过PNG转换")
        print(f"   安装命令: pip install cairosvg")

    print(f"\n{'='*70}")
    print(f"✅ 生成完成！")
    print(f"📊 SVG矢量图 | 精确控制 | 完美对齐")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
