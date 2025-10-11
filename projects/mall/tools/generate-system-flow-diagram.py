#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成系统业务总流程图（参考图风格）
使用 matplotlib 绘制传统流程图
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patheffects as path_effects
import os
from pathlib import Path as PathLib

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class FlowchartDrawer:
    """流程图绘制器"""

    def __init__(self, fig_width=16, fig_height=22):
        self.fig, self.ax = plt.subplots(figsize=(fig_width, fig_height))
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 140)
        self.ax.axis('off')

    def draw_rounded_rect(self, x, y, width, height, text, fill=True):
        """绘制圆角矩形（开始/结束节点）"""
        rect = FancyBboxPatch(
            (x - width/2, y - height/2), width, height,
            boxstyle="round,pad=0.3",
            linewidth=2,
            edgecolor='black',
            facecolor='white' if fill else 'none'
        )
        self.ax.add_patch(rect)
        self.ax.text(x, y, text, ha='center', va='center', fontsize=12, weight='bold')

    def draw_rect(self, x, y, width, height, text):
        """绘制矩形（处理节点）"""
        rect = patches.Rectangle(
            (x - width/2, y - height/2), width, height,
            linewidth=2,
            edgecolor='black',
            facecolor='white'
        )
        self.ax.add_patch(rect)
        # 支持多行文本
        if '\n' in text:
            self.ax.text(x, y, text, ha='center', va='center', fontsize=10)
        else:
            self.ax.text(x, y, text, ha='center', va='center', fontsize=11)

    def draw_diamond(self, x, y, width, height, text):
        """绘制菱形（判断节点）"""
        diamond = Polygon([
            (x, y + height/2),  # 上
            (x + width/2, y),    # 右
            (x, y - height/2),   # 下
            (x - width/2, y)     # 左
        ], closed=True, linewidth=2, edgecolor='black', facecolor='white')
        self.ax.add_patch(diamond)
        self.ax.text(x, y, text, ha='center', va='center', fontsize=10)

    def draw_arrow(self, x1, y1, x2, y2, label='', label_pos='mid'):
        """绘制箭头"""
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle='->,head_width=0.4,head_length=0.6',
            linewidth=1.5,
            edgecolor='black',
            facecolor='black'
        )
        self.ax.add_patch(arrow)

        # 添加标签
        if label:
            if label_pos == 'mid':
                label_x, label_y = (x1 + x2) / 2, (y1 + y2) / 2
            elif label_pos == 'start':
                label_x, label_y = x1 + (x2-x1)*0.2, y1 + (y2-y1)*0.2
            else:
                label_x, label_y = (x1 + x2) / 2, (y1 + y2) / 2

            self.ax.text(label_x, label_y, label, ha='center', va='center',
                        fontsize=10, bbox=dict(boxstyle='round,pad=0.3',
                        facecolor='white', edgecolor='none'))

    def draw_line(self, x1, y1, x2, y2):
        """绘制直线（无箭头）"""
        self.ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5)

    def save(self, filepath):
        """保存图片"""
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✅ 已保存: {filepath}")


def draw_system_flow():
    """绘制系统业务总流程图"""
    drawer = FlowchartDrawer(fig_width=18, fig_height=24)

    # 起始节点
    drawer.draw_rounded_rect(50, 135, 10, 4, '开始')
    drawer.draw_arrow(50, 133, 50, 130)

    # 系统登录
    drawer.draw_rect(50, 127, 12, 4, '系统登录')
    drawer.draw_arrow(50, 125, 50, 122)

    # 判断：是否注册
    drawer.draw_diamond(50, 119, 12, 5, '是否注册?')
    drawer.draw_arrow(50, 116.5, 50, 114, label='是')
    drawer.draw_arrow(56, 119, 64, 119, label='否')

    # 注册账号
    drawer.draw_rect(70, 119, 12, 4, '注册账号')
    drawer.draw_arrow(70, 117, 70, 109)
    drawer.draw_arrow(70, 109, 50, 109)
    drawer.draw_arrow(50, 109, 50, 111.5)

    # 判断：普通用户/管理员
    drawer.draw_diamond(50, 111, 14, 5, '普通用户/\n管理员?')

    # ========== 左侧：普通用户流程 ==========
    drawer.draw_arrow(44, 111, 25, 111, label='普通用户')

    # 输入用户名和密码
    y_pos = 111
    drawer.draw_rect(18, y_pos, 14, 5, '输入用户名和\n密码获取验证码')
    drawer.draw_arrow(18, y_pos - 2.5, 18, y_pos - 5)

    # 判断：验证登录合法性
    y_pos = y_pos - 8
    drawer.draw_diamond(18, y_pos, 14, 5, '验证登录\n合法性?')
    drawer.draw_arrow(12, y_pos, 4, y_pos, label='N')
    drawer.draw_arrow(4, y_pos, 4, 119)
    drawer.draw_arrow(4, 119, 12, 119)
    drawer.ax.text(4, 115, '重新输入', ha='center', fontsize=9)
    drawer.draw_arrow(18, y_pos - 2.5, 18, y_pos - 5, label='Y')

    # 商品展示
    y_pos = y_pos - 8
    drawer.draw_rect(18, y_pos, 10, 4, '商品展示')
    drawer.draw_arrow(18, y_pos - 2, 18, y_pos - 4.5)

    # 选择商品
    y_pos = y_pos - 7
    drawer.draw_rect(18, y_pos, 10, 4, '选择商品')

    # 分支：运输/是
    drawer.draw_arrow(18, y_pos - 2, 18, y_pos - 4.5)
    y_pos = y_pos - 7
    drawer.ax.text(14, y_pos + 1, '运输', ha='center', fontsize=9)

    # 直接购买/加入购物车
    drawer.draw_rect(12, y_pos, 10, 4, '直接购买商品')
    drawer.draw_rect(24, y_pos, 10, 4, '加入购物车')

    drawer.draw_arrow(12, y_pos - 2, 12, y_pos - 5)
    drawer.draw_arrow(24, y_pos - 2, 24, y_pos - 5)

    y_pos = y_pos - 7.5
    drawer.draw_rect(12, y_pos, 10, 5, '是否提送货\n上门')
    drawer.draw_rect(24, y_pos, 10, 4, '查看购物车')

    drawer.draw_arrow(12, y_pos - 2.5, 12, y_pos - 5)
    drawer.draw_arrow(24, y_pos - 2, 24, y_pos - 5)

    # 汇聚到提交订单
    y_pos = y_pos - 7.5
    drawer.ax.text(10, y_pos + 1, '是', ha='center', fontsize=9)
    drawer.draw_arrow(12, y_pos + 1, 18, y_pos + 1)
    drawer.draw_arrow(24, y_pos + 1, 18, y_pos + 1)
    drawer.draw_arrow(18, y_pos + 1, 18, y_pos - 1.5)

    drawer.draw_rect(18, y_pos, 10, 4, '提交订单')

    # ========== 右侧：管理员流程 ==========
    drawer.draw_arrow(56, 111, 75, 111, label='管理员')

    # 输入用户名和密码验证码
    y_pos_admin = 111
    drawer.draw_rect(82, y_pos_admin, 14, 5, '输入用户名和密\n码获取验证码')
    drawer.draw_arrow(82, y_pos_admin - 2.5, 82, y_pos_admin - 5)

    # 判断：验证登录合法性
    y_pos_admin = y_pos_admin - 8
    drawer.draw_diamond(82, y_pos_admin, 14, 5, '验证登录\n合法性?')
    drawer.draw_arrow(88, y_pos_admin, 96, y_pos_admin, label='N')
    drawer.draw_arrow(96, y_pos_admin, 96, 119)
    drawer.draw_arrow(96, 119, 88, 119)
    drawer.ax.text(96, 115, '重新输入', ha='center', fontsize=9)
    drawer.draw_arrow(82, y_pos_admin - 2.5, 82, y_pos_admin - 5, label='Y')

    # 用户信息管理
    y_pos_admin = y_pos_admin - 8
    drawer.draw_rect(82, y_pos_admin, 10, 4, '用户信息管理')
    drawer.draw_arrow(82, y_pos_admin - 2, 82, y_pos_admin - 4.5)

    # 商品信息管理
    y_pos_admin = y_pos_admin - 7
    drawer.draw_rect(82, y_pos_admin, 10, 4, '商品信息管理')
    drawer.draw_arrow(82, y_pos_admin - 2, 82, y_pos_admin - 4.5)

    # 订单管理分支
    y_pos_admin = y_pos_admin - 7
    drawer.draw_rect(82, y_pos_admin, 10, 4, '订单管理')

    # 订单管理的四个子功能
    drawer.draw_arrow(82, y_pos_admin - 2, 82, y_pos_admin - 4.5)
    y_pos_admin = y_pos_admin - 7

    drawer.draw_rect(66, y_pos_admin, 8, 4, '查看订单')
    drawer.draw_rect(76, y_pos_admin, 8, 4, '订单状态')
    drawer.draw_rect(86, y_pos_admin, 8, 4, '删除订单')
    drawer.draw_rect(96, y_pos_admin, 8, 4, '完成订单')

    # 从订单管理连接到四个子功能
    drawer.draw_arrow(82, y_pos_admin + 4.5, 66, y_pos_admin + 2)
    drawer.draw_arrow(82, y_pos_admin + 4.5, 76, y_pos_admin + 2)
    drawer.draw_arrow(82, y_pos_admin + 4.5, 86, y_pos_admin + 2)
    drawer.draw_arrow(82, y_pos_admin + 4.5, 96, y_pos_admin + 2)

    # 四个子功能汇聚
    drawer.draw_arrow(66, y_pos_admin - 2, 66, y_pos_admin - 5)
    drawer.draw_arrow(76, y_pos_admin - 2, 76, y_pos_admin - 5)
    drawer.draw_arrow(86, y_pos_admin - 2, 86, y_pos_admin - 5)
    drawer.draw_arrow(96, y_pos_admin - 2, 96, y_pos_admin - 5)

    y_pos_admin = y_pos_admin - 7
    drawer.draw_arrow(66, y_pos_admin, 82, y_pos_admin)
    drawer.draw_arrow(76, y_pos_admin, 82, y_pos_admin)
    drawer.draw_arrow(86, y_pos_admin, 82, y_pos_admin)
    drawer.draw_arrow(96, y_pos_admin, 82, y_pos_admin)

    # ========== 汇聚到退出登录 ==========
    # 左侧汇聚
    final_y = 15
    drawer.draw_arrow(18, y_pos - 2, 18, final_y + 5)
    drawer.draw_arrow(18, final_y + 5, 50, final_y + 5)

    # 右侧汇聚
    drawer.draw_arrow(82, y_pos_admin, 82, final_y + 5)
    drawer.draw_arrow(82, final_y + 5, 50, final_y + 5)

    drawer.draw_arrow(50, final_y + 5, 50, final_y + 2)

    # 退出登录
    drawer.draw_rect(50, final_y, 10, 4, '退出登录')
    drawer.draw_arrow(50, final_y - 2, 50, final_y - 5)

    # 结束节点
    drawer.draw_rounded_rect(50, final_y - 8, 10, 4, '结束')

    return drawer


def main():
    """主函数"""
    print(f"\n{'='*70}")
    print(f"🎨 开始生成系统业务总流程图（Python 绘制）")
    print(f"{'='*70}\n")

    # 生成流程图
    drawer = draw_system_flow()

    # 保存文件
    output_dir = PathLib(__file__).parent.parent / 'paper' / 'assets' / 'diagrams' / 'uml'
    os.makedirs(output_dir, exist_ok=True)
    output_path = output_dir / 'system-flow-python.png'

    drawer.save(str(output_path))

    print(f"\n{'='*70}")
    print(f"✅ 生成完成！")
    print(f"📁 文件路径: {output_path}")
    print(f"📊 风格: 传统流程图 | 黑白配色 | 中文标签")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
