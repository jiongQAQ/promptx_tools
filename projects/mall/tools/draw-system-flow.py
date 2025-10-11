#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
绘制系统业务流程图 - 参考图风格
横向扁平布局，左右分支，清晰的Y/N标注
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch
import os
from pathlib import Path as PathLib

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class SystemFlowDrawer:
    """系统流程图绘制器"""

    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(20, 14))
        self.ax.set_xlim(0, 200)
        self.ax.set_ylim(0, 100)
        self.ax.axis('off')

    def draw_rounded_rect(self, x, y, width, height, text):
        """绘制圆角矩形（开始/结束）"""
        rect = FancyBboxPatch(
            (x - width/2, y - height/2), width, height,
            boxstyle="round,pad=0.5",
            linewidth=2,
            edgecolor='black',
            facecolor='white'
        )
        self.ax.add_patch(rect)
        self.ax.text(x, y, text, ha='center', va='center', fontsize=11, weight='bold')

    def draw_rect(self, x, y, width, height, text):
        """绘制矩形（处理节点）"""
        rect = patches.Rectangle(
            (x - width/2, y - height/2), width, height,
            linewidth=2,
            edgecolor='black',
            facecolor='white'
        )
        self.ax.add_patch(rect)
        # 处理多行文本
        lines = text.split('\n')
        if len(lines) > 1:
            line_height = 1.5
            start_y = y + (len(lines) - 1) * line_height / 2
            for i, line in enumerate(lines):
                self.ax.text(x, start_y - i * line_height, line,
                           ha='center', va='center', fontsize=10)
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

        # 处理多行文本
        lines = text.split('\n')
        if len(lines) > 1:
            line_height = 1.2
            start_y = y + (len(lines) - 1) * line_height / 2
            for i, line in enumerate(lines):
                self.ax.text(x, start_y - i * line_height, line,
                           ha='center', va='center', fontsize=10)
        else:
            self.ax.text(x, y, text, ha='center', va='center', fontsize=10)

    def draw_arrow(self, x1, y1, x2, y2, label='', label_offset=(0, 0)):
        """绘制箭头，支持标签"""
        # 使用 annotate 方法绘制箭头，确保连接紧密
        self.ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(
                            arrowstyle='-|>',  # 简洁箭头样式
                            lw=1.5,  # 线宽
                            color='black',
                            shrinkA=0,
                            shrinkB=0,
                            mutation_scale=12  # 箭头大小
                        ))

        # 添加标签（Y/N等）
        if label:
            mid_x = (x1 + x2) / 2 + label_offset[0]
            mid_y = (y1 + y2) / 2 + label_offset[1]
            self.ax.text(mid_x, mid_y, label, ha='center', va='center',
                        fontsize=10, weight='bold',
                        bbox=dict(boxstyle='round,pad=0.3',
                                facecolor='white', edgecolor='none'))

    def save(self, filepath):
        """保存图片"""
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight',
                   facecolor='white', pad_inches=0.2)
        print(f"✅ 已保存: {filepath}")


def draw_flow():
    """绘制完整流程图"""
    d = SystemFlowDrawer()

    # ============ 顶部公共流程 ============
    # 开始
    d.draw_rounded_rect(100, 95, 12, 4, '开始')
    d.draw_arrow(100, 93, 100, 90)

    # 系统登录
    d.draw_rect(100, 88, 12, 3, '系统登录')
    d.draw_arrow(100, 86.5, 100, 84)

    # 判断：是否注册
    d.draw_diamond(100, 82, 14, 4, '是否注册?')
    d.draw_arrow(100, 80, 100, 77, label='Y')
    d.draw_arrow(107, 82, 120, 82, label='N')

    # 注册账号
    d.draw_rect(127, 82, 14, 3, '注册账号')
    d.draw_arrow(127, 80.5, 127, 74)
    d.draw_arrow(127, 74, 100, 74)
    d.draw_arrow(100, 74, 100, 75.5)

    # 判断：普通用户/管理员 - 核心分支点
    d.draw_diamond(100, 73, 18, 4, '普通用户/\n管理员?')

    # ============ 左侧：普通用户端 ============
    d.draw_arrow(91, 73, 50, 73, label='普通用户', label_offset=(0, 1))

    # 用户登录
    user_x = 50
    y = 73
    d.draw_rect(user_x, y, 16, 4, '输入用户名和\n密码获取验证码')
    d.draw_arrow(user_x, y - 2, user_x, y - 5)

    # 判断：验证合法性
    y = y - 8
    d.draw_diamond(user_x, y, 16, 4, '验证登录\n合法性?')
    d.draw_arrow(user_x, y - 2, user_x, y - 5, label='Y')
    # 重新输入循环
    d.draw_arrow(user_x - 8, y, user_x - 15, y, label='N')
    d.draw_arrow(user_x - 15, y, user_x - 15, 73)
    d.draw_arrow(user_x - 15, 73, user_x - 8, 73)
    d.ax.text(user_x - 15, 69, '重新输入', ha='center', fontsize=9)

    # 商品展示
    y = y - 7
    d.draw_rect(user_x, y, 12, 3, '商品展示')
    d.draw_arrow(user_x, y - 1.5, user_x, y - 3.5)

    # 选择商品
    y = y - 5.5
    d.draw_rect(user_x, y, 12, 3, '选择商品')
    d.draw_arrow(user_x, y - 1.5, user_x, y - 3.5)

    # 判断：是否购买
    y = y - 6
    d.draw_diamond(user_x, y, 12, 4, '是否购买?')
    d.draw_arrow(user_x, y - 2, user_x, y - 4.5, label='Y')
    d.draw_arrow(user_x + 6, y, user_x + 15, y, label='N')
    d.draw_rect(user_x + 20, y, 12, 3, '继续浏览')

    # 并行路径：直接购买 和 加入购物车
    y = y - 7
    left_x = user_x - 10
    right_x = user_x + 10

    d.ax.text(user_x - 15, y + 2, '运输', ha='center', fontsize=9)

    d.draw_rect(left_x, y, 12, 3, '直接购买商品')
    d.draw_rect(right_x, y, 12, 3, '加入购物车')

    d.draw_arrow(user_x, y + 4.5, left_x, y + 1.5)
    d.draw_arrow(user_x, y + 4.5, right_x, y + 1.5)

    d.draw_arrow(left_x, y - 1.5, left_x, y - 4)
    d.draw_arrow(right_x, y - 1.5, right_x, y - 4)

    # 第二层并行
    y = y - 6
    d.draw_rect(left_x, y, 12, 4, '是否提送货\n上门')
    d.draw_rect(right_x, y, 12, 3, '查看购物车')

    d.draw_arrow(left_x, y - 2, left_x, y - 4)
    d.draw_arrow(right_x, y - 1.5, right_x, y - 3.5)

    # 汇聚到提交订单
    y = y - 6
    d.ax.text(left_x - 3, y + 1.5, '是', ha='center', fontsize=9)
    d.draw_arrow(left_x, y + 1.5, user_x, y + 1.5)
    d.draw_arrow(right_x, y + 1.5, user_x, y + 1.5)
    d.draw_arrow(user_x, y + 1.5, user_x, y - 1)

    d.draw_rect(user_x, y, 12, 3, '提交订单')

    # ============ 右侧：管理端 ============
    d.draw_arrow(109, 73, 150, 73, label='管理员', label_offset=(0, 1))

    # 管理员登录
    admin_x = 150
    y = 73
    d.draw_rect(admin_x, y, 16, 4, '输入用户名和\n密码获取验证码')
    d.draw_arrow(admin_x, y - 2, admin_x, y - 5)

    # 判断：验证合法性
    y = y - 8
    d.draw_diamond(admin_x, y, 16, 4, '验证登录\n合法性?')
    d.draw_arrow(admin_x, y - 2, admin_x, y - 5, label='Y')
    # 重新输入循环
    d.draw_arrow(admin_x + 8, y, admin_x + 15, y, label='N')
    d.draw_arrow(admin_x + 15, y, admin_x + 15, 73)
    d.draw_arrow(admin_x + 15, 73, admin_x + 8, 73)
    d.ax.text(admin_x + 15, 69, '重新输入', ha='center', fontsize=9)

    # 用户信息管理
    y = y - 7
    d.draw_rect(admin_x, y, 14, 3, '用户信息管理')
    d.draw_arrow(admin_x, y - 1.5, admin_x, y - 3.5)

    # 商品信息管理
    y = y - 5.5
    d.draw_rect(admin_x, y, 14, 3, '商品信息管理')
    d.draw_arrow(admin_x, y - 1.5, admin_x, y - 3.5)

    # 订单管理
    y = y - 5.5
    d.draw_rect(admin_x, y, 14, 3, '订单管理')
    d.draw_arrow(admin_x, y - 1.5, admin_x, y - 4)

    # 订单管理的4个子功能（横向并行）
    y = y - 6.5
    sub1_x = admin_x - 21
    sub2_x = admin_x - 7
    sub3_x = admin_x + 7
    sub4_x = admin_x + 21

    d.draw_rect(sub1_x, y, 10, 3, '查看订单')
    d.draw_rect(sub2_x, y, 10, 3, '订单状态')
    d.draw_rect(sub3_x, y, 10, 3, '删除订单')
    d.draw_rect(sub4_x, y, 10, 3, '完成订单')

    # 从订单管理连到4个子功能
    d.draw_arrow(admin_x, y + 4, sub1_x, y + 1.5)
    d.draw_arrow(admin_x, y + 4, sub2_x, y + 1.5)
    d.draw_arrow(admin_x, y + 4, sub3_x, y + 1.5)
    d.draw_arrow(admin_x, y + 4, sub4_x, y + 1.5)

    # 4个子功能向下汇聚
    d.draw_arrow(sub1_x, y - 1.5, sub1_x, y - 4)
    d.draw_arrow(sub2_x, y - 1.5, sub2_x, y - 4)
    d.draw_arrow(sub3_x, y - 1.5, sub3_x, y - 4)
    d.draw_arrow(sub4_x, y - 1.5, sub4_x, y - 4)

    y = y - 5
    d.draw_arrow(sub1_x, y, admin_x, y)
    d.draw_arrow(sub2_x, y, admin_x, y)
    d.draw_arrow(sub3_x, y, admin_x, y)
    d.draw_arrow(sub4_x, y, admin_x, y)
    d.draw_arrow(admin_x, y, admin_x, y - 2)

    # 结果购物车（首页配置管理）
    y = y - 4
    d.draw_rect(admin_x, y, 14, 3, '首页配置管理')

    # ============ 底部汇聚 ============
    # 左侧向下延伸到底部
    final_y = 8
    d.draw_arrow(user_x, 22, user_x, final_y + 3)
    d.draw_arrow(user_x, final_y + 3, 100, final_y + 3)

    # 右侧向下延伸到底部
    d.draw_arrow(admin_x, y - 1.5, admin_x, final_y + 3)
    d.draw_arrow(admin_x, final_y + 3, 100, final_y + 3)

    d.draw_arrow(100, final_y + 3, 100, final_y + 0.5)

    # 退出登录
    d.draw_rect(100, final_y, 12, 3, '退出登录')
    d.draw_arrow(100, final_y - 1.5, 100, final_y - 4)

    # 结束
    d.draw_rounded_rect(100, final_y - 6, 12, 4, '结束')

    return d


def main():
    """主函数"""
    print(f"\n{'='*70}")
    print(f"🎨 开始生成系统业务流程图（参考图风格）")
    print(f"📐 布局: 横向扁平 | 左右分支 | Y/N标注清晰")
    print(f"{'='*70}\n")

    # 生成流程图
    drawer = draw_flow()

    # 保存文件
    output_dir = PathLib(__file__).parent.parent / 'paper' / 'assets' / 'diagrams' / 'uml'
    os.makedirs(output_dir, exist_ok=True)
    output_path = output_dir / 'system-flow-final.png'

    drawer.save(str(output_path))

    print(f"\n{'='*70}")
    print(f"✅ 生成完成！")
    print(f"📁 文件: {output_path}")
    print(f"📊 特点: 参考图风格 | 清晰Y/N标注 | 左右对称布局")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
