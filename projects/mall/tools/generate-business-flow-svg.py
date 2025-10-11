#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成系统业务总流程图（SVG格式）
参考图风格：横向扁平布局，左右对称，精确对齐
"""

import os
from pathlib import Path as PathLib


class SVGFlowChart:
    """SVG流程图生成器"""

    def __init__(self, width=2200, height=1270):
        self.width = width
        self.height = height
        self.elements = []

        # 样式定义
        self.styles = {
            'rect': 'fill:white;stroke:black;stroke-width:2',
            'diamond': 'fill:white;stroke:black;stroke-width:2',
            'rounded': 'fill:white;stroke:black;stroke-width:2',
            'text': 'font-family:Microsoft YaHei,SimHei,Arial;font-size:18px;text-anchor:middle;dominant-baseline:middle',
            'text_small': 'font-family:Microsoft YaHei,SimHei,Arial;font-size:16px;text-anchor:middle;dominant-baseline:middle',
            'label': 'font-family:Microsoft YaHei,SimHei,Arial;font-size:16px;font-weight:bold;text-anchor:middle',
            'line': 'stroke:black;stroke-width:2;fill:none;marker-end:url(#arrow)',
            'line_no_arrow': 'stroke:black;stroke-width:2;fill:none'
        }

    def add_header(self):
        """添加SVG头部"""
        self.elements.append(f'<?xml version="1.0" encoding="UTF-8"?>')
        self.elements.append(f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">')
        self.elements.append('<defs>')
        self.elements.append('  <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">')
        self.elements.append('    <polygon points="0 0, 10 5, 0 10" fill="black"/>')
        self.elements.append('  </marker>')
        self.elements.append('</defs>')
        self.elements.append(f'<rect width="{self.width}" height="{self.height}" fill="white"/>')

    def add_footer(self):
        """添加SVG尾部"""
        self.elements.append('</svg>')

    def rounded_rect(self, x, y, w, h, text):
        """圆角矩形（开始/结束）"""
        self.elements.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="20" style="{self.styles["rounded"]}"/>')
        self.elements.append(f'<text x="{x}" y="{y}" style="{self.styles["text"]}">{text}</text>')

    def rect(self, x, y, w, h, text):
        """矩形（处理步骤）"""
        self.elements.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" style="{self.styles["rect"]}"/>')

        # 处理多行文本
        if '\n' in text:
            lines = text.split('\n')
            line_height = 22
            start_y = y - (len(lines) - 1) * line_height / 2
            for i, line in enumerate(lines):
                self.elements.append(f'<text x="{x}" y="{start_y + i * line_height}" style="{self.styles["text_small"]}">{line}</text>')
        else:
            self.elements.append(f'<text x="{x}" y="{y}" style="{self.styles["text"]}">{text}</text>')

    def diamond(self, x, y, w, h, text):
        """菱形（判断）"""
        points = f"{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}"
        self.elements.append(f'<polygon points="{points}" style="{self.styles["diamond"]}"/>')

        # 处理多行文本
        if '\n' in text:
            lines = text.split('\n')
            line_height = 20
            start_y = y - (len(lines) - 1) * line_height / 2
            for i, line in enumerate(lines):
                self.elements.append(f'<text x="{x}" y="{start_y + i * line_height}" style="{self.styles["text_small"]}">{line}</text>')
        else:
            self.elements.append(f'<text x="{x}" y="{y}" style="{self.styles["text"]}">{text}</text>')

    def arrow(self, x1, y1, x2, y2, label=''):
        """箭头连线"""
        self.elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="{self.styles["line"]}"/>')
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.elements.append(f'<text x="{mx}" y="{my - 8}" style="{self.styles["label"]}">{label}</text>')

    def line_no_arrow(self, x1, y1, x2, y2):
        """无箭头连线（用于中间段）"""
        self.elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="{self.styles["line_no_arrow"]}"/>')

    def text_label(self, x, y, text, small=False):
        """独立文本标签"""
        style = self.styles["text_small"] if small else self.styles["label"]
        self.elements.append(f'<text x="{x}" y="{y}" style="{style}">{text}</text>')

    def generate(self):
        """生成完整SVG"""
        self.add_header()

        # 中心X坐标
        cx = self.width / 2

        # ========== 顶部公共流程 ==========
        y = 60
        self.rounded_rect(cx, y, 140, 60, '开始')
        self.arrow(cx, 90, cx, 120)

        y = 150
        self.rect(cx, y, 140, 60, '系统登录')
        self.arrow(cx, 180, cx, 210)

        y = 245
        y_diamond_bottom = 280  # 判断框底部
        self.diamond(cx, y, 160, 70, '是否注册?')

        # 注册分支 - 向右到注册框
        reg_x = cx + 400  # 注册框中心X（拉长距离）
        reg_y = 245
        reg_bottom = 275  # 注册框底部

        self.arrow(cx + 80, 245, reg_x - 70, 245, 'N')
        self.rect(reg_x, reg_y, 140, 60, '注册账号')

        # 注册后向下再向左回到主流程（三条线精确连接）
        turn_y = 295  # 转折点Y坐标（在两个判断框之间）
        self.line_no_arrow(reg_x, reg_bottom, reg_x, turn_y)  # 向下
        self.line_no_arrow(reg_x, turn_y, cx, turn_y)  # 向左
        self.line_no_arrow(cx, turn_y, cx, y_diamond_bottom)  # 向上到判断框底部（无箭头）

        # Y分支：从"是否注册?"判断框底部到"普通用户/管理员?"判断框顶部
        next_diamond_top = 305  # 下一个判断框顶部
        self.arrow(cx, y_diamond_bottom, cx, next_diamond_top, 'Y')

        y = 340
        self.diamond(cx, y, 200, 70, '普通用户/\n管理员?')

        # ========== 左侧：普通用户 ==========
        user_x = 550
        user_box_width = 180
        user_box_right = user_x + user_box_width / 2  # 框的右边缘

        # 从判断框左边缘到输入框右边缘（精确连接）
        self.arrow(cx - 100, 340, user_box_right, 340, '普通用户')

        uy = 340
        self.rect(user_x, uy, user_box_width, 70, '输入用户名和\n密码获取验证码')
        self.arrow(user_x, 375, user_x, 410)

        uy = 445
        self.diamond(user_x, uy, 170, 70, '验证登录\n合法性?')
        self.arrow(user_x, 480, user_x, 510, 'Y')

        # 重新输入循环
        self.arrow(user_x - 85, 445, user_x - 180, 445, 'N')
        self.line_no_arrow(user_x - 180, 445, user_x - 180, 340)
        self.arrow(user_x - 180, 340, user_x - 90, 340)
        self.text_label(user_x - 180, 392, '重新输入', small=True)

        uy = 540
        self.rect(user_x, uy, 140, 60, '商品展示')
        self.arrow(user_x, 570, user_x, 600)

        uy = 630
        self.rect(user_x, uy, 140, 60, '选择商品')

        # 购买分支
        left_x = user_x - 120
        right_x = user_x + 120

        uy = 730
        self.rect(left_x, uy, 140, 60, '直接购买商品')
        self.rect(right_x, uy, 140, 60, '加入购物车')

        self.arrow(user_x, 660, left_x, 700)
        self.arrow(user_x, 660, right_x, 700)

        # 直接购买 → 向下再向右到提交订单
        self.arrow(left_x, 760, left_x, 830)

        # 加入购物车 → 查看购物车
        self.arrow(right_x, 760, right_x, 800)

        uy = 830
        self.rect(right_x, uy, 140, 60, '查看购物车')

        # 查看购物车 → 向下再向左到提交订单
        self.arrow(right_x, 860, right_x, 920)

        # 汇聚到提交订单
        uy = 950
        self.line_no_arrow(left_x, 830, left_x, uy)
        self.line_no_arrow(left_x, uy, user_x, uy)
        self.line_no_arrow(right_x, 920, user_x, 920)
        self.line_no_arrow(user_x, 920, user_x, uy)
        self.arrow(user_x, uy, user_x, 980)

        uy = 1010
        self.rect(user_x, uy, 140, 60, '提交订单')

        # ========== 右侧：管理员 ==========
        admin_x = 1650
        admin_box_width = 180
        admin_box_left = admin_x - admin_box_width / 2  # 框的左边缘

        # 从判断框右边缘到输入框左边缘（精确连接）
        self.arrow(cx + 100, 340, admin_box_left, 340, '管理员')

        ay = 340
        self.rect(admin_x, ay, admin_box_width, 70, '输入用户名和\n密码获取验证码')
        self.arrow(admin_x, 375, admin_x, 410)

        ay = 445
        self.diamond(admin_x, ay, 170, 70, '验证登录\n合法性?')
        self.arrow(admin_x, 480, admin_x, 510, 'Y')

        # 重新输入循环
        self.arrow(admin_x + 85, 445, admin_x + 180, 445, 'N')
        self.line_no_arrow(admin_x + 180, 445, admin_x + 180, 340)
        self.arrow(admin_x + 180, 340, admin_x + 90, 340)
        self.text_label(admin_x + 180, 392, '重新输入', small=True)

        ay = 540
        self.rect(admin_x, ay, 160, 60, '用户信息管理')
        self.arrow(admin_x, 570, admin_x, 600)

        ay = 630
        self.rect(admin_x, ay, 160, 60, '商品信息管理')
        self.arrow(admin_x, 660, admin_x, 690)

        ay = 720
        self.rect(admin_x, ay, 160, 60, '订单管理')

        # 4个并行订单功能 - 用实线大框包含
        ay = 840
        box_top = 790
        box_bottom = 890

        # 绘制实线大框（包含4个子功能）
        self.elements.append(f'<rect x="{admin_x - 280}" y="{box_top}" width="560" height="100" style="fill:none;stroke:black;stroke-width:2"/>')

        # 从订单管理连到大框（精确到边缘）
        self.arrow(admin_x, 750, admin_x, box_top)

        # 4个子功能
        sub_positions = [
            (admin_x - 210, '查看订单'),
            (admin_x - 70, '订单状态'),
            (admin_x + 70, '删除订单'),
            (admin_x + 210, '完成订单')
        ]

        for sx, slabel in sub_positions:
            self.rect(sx, ay, 110, 60, slabel)

        # 从大框连到首页配置管理（精确到边缘）
        self.arrow(admin_x, box_bottom, admin_x, 940)

        ay = 970
        self.rect(admin_x, ay, 160, 60, '首页配置管理')

        # ========== 底部汇聚 ==========
        final_y = 1140

        # 左侧到底部
        self.line_no_arrow(user_x, 1040, user_x, final_y)
        self.line_no_arrow(user_x, final_y, cx, final_y)

        # 右侧到底部
        self.line_no_arrow(admin_x, 1000, admin_x, final_y)
        self.line_no_arrow(admin_x, final_y, cx, final_y)

        # 向上到退出登录（修正箭头方向）
        self.arrow(cx, final_y, cx, 1110)

        final_y = 1080
        self.rect(cx, final_y, 140, 60, '退出登录')
        self.arrow(cx, 1110, cx, 1170)

        self.rounded_rect(cx, 1200, 140, 60, '结束')

        self.add_footer()
        return '\n'.join(self.elements)


def main():
    """主函数"""
    print(f"\n{'='*80}")
    print(f"🎨 生成系统业务总流程图（参考图风格）")
    print(f"📐 横向扁平布局 | 左右对称 | 精确对齐")
    print(f"{'='*80}\n")

    # 创建流程图
    chart = SVGFlowChart(width=2200, height=1270)
    svg_content = chart.generate()

    # 保存文件
    output_dir = PathLib(__file__).parent.parent / 'paper' / 'assets' / 'diagrams' / 'uml'
    os.makedirs(output_dir, exist_ok=True)

    svg_path = output_dir / 'system-business-flow.svg'
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print(f"✅ SVG文件已生成")
    print(f"📁 路径: {svg_path}")
    print(f"📊 尺寸: 2200x1270px")
    print(f"💾 大小: {len(svg_content)} bytes")

    print(f"\n{'='*80}")
    print(f"✅ 完成！")
    print(f"🎯 参考图风格 | 清晰Y/N标注 | 完美对齐")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
