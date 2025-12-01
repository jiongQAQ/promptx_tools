#!/usr/bin/env python3
"""
批量为章节文件添加docx_type样式标记

根据章节ID自动判断层级并添加对应的样式类型：
- 0.1, 0.2 (摘要/Abstract) → abstract_title
- 纯数字 (1-9) → chapter_title
- X.X → section_title
- X.X.X → subsection_title
- X.X.X.X → subsection_title

使用方法:
    python3 add-styles-to-chapters.py
"""

import json
import os
from pathlib import Path


def determine_style(chapter_id):
    """根据章节ID确定样式类型"""
    parts = chapter_id.split('.')

    # 摘要和Abstract
    if chapter_id in ['0.1', '0.2']:
        return {
            'title_style': 'abstract_title',
            'text_style': 'abstract_content'
        }

    # 一级标题（第X章）
    if len(parts) == 1 and parts[0].isdigit():
        # 特殊处理：参考文献、致谢等
        chapter_num = int(parts[0])
        if chapter_num >= 7:  # 第7章是结论，第8章是参考文献，第9章是致谢
            return {
                'title_style': 'chapter_title',
                'text_style': 'body_text'
            }
        return {
            'title_style': 'chapter_title',
            'text_style': 'body_text'
        }

    # 二级标题（X.X）
    if len(parts) == 2:
        return {
            'title_style': 'section_title',
            'text_style': 'body_text'
        }

    # 三级标题（X.X.X）
    if len(parts) == 3:
        return {
            'title_style': 'subsection_title',
            'text_style': 'body_text'
        }

    # 四级及以上标题（X.X.X.X）
    if len(parts) >= 4:
        return {
            'title_style': 'subsection_title',
            'text_style': 'body_text'
        }

    # 默认
    return {
        'title_style': 'body_text',
        'text_style': 'body_text'
    }


def add_styles_to_chapter(chapter_file):
    """为单个章节文件添加样式标记"""
    try:
        # 读取章节文件
        with open(chapter_file, 'r', encoding='utf-8') as f:
            chapter_data = json.load(f)

        # 获取章节ID
        chapter_id = chapter_data.get('id', '')
        if not chapter_id:
            print(f"  ⚠️  {chapter_file.name}: 缺少id字段，跳过")
            return False

        # 确定样式
        styles = determine_style(chapter_id)

        # 添加样式标记
        chapter_data['docx_type'] = styles['title_style']

        # 如果有content字段，添加文本样式
        if 'content' in chapter_data and chapter_data['content']:
            chapter_data['docx_type_text'] = styles['text_style']

        # 如果有text字段，也添加文本样式
        if 'text' in chapter_data and chapter_data['text']:
            chapter_data['docx_type_desc'] = styles['text_style']

        # 保存更新后的文件
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)

        print(f"  ✅ {chapter_file.name}: {chapter_id} → {styles['title_style']}")
        return True

    except Exception as e:
        print(f"  ❌ {chapter_file.name}: 处理失败 - {e}")
        return False


def main():
    """主函数"""
    print("📝 批量为章节文件添加样式标记")
    print("=" * 60)

    # 获取项目路径
    project_root = Path(__file__).parent.parent
    chapters_dir = project_root / 'paper' / 'chapters'

    if not chapters_dir.exists():
        print(f"❌ 章节目录不存在: {chapters_dir}")
        return

    # 获取所有章节JSON文件
    chapter_files = sorted(chapters_dir.glob('chapter.*.json'))

    if not chapter_files:
        print(f"❌ 未找到章节文件: {chapters_dir}")
        return

    print(f"📂 找到 {len(chapter_files)} 个章节文件")
    print()

    # 处理每个文件
    success_count = 0
    for chapter_file in chapter_files:
        if add_styles_to_chapter(chapter_file):
            success_count += 1

    print()
    print("=" * 60)
    print(f"✅ 完成！成功处理 {success_count}/{len(chapter_files)} 个文件")

    # 显示样式统计
    print()
    print("📊 样式统计:")
    style_counts = {}
    for chapter_file in chapter_files:
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                style = data.get('docx_type', 'unknown')
                style_counts[style] = style_counts.get(style, 0) + 1
        except:
            pass

    for style, count in sorted(style_counts.items()):
        print(f"  - {style}: {count} 个")


if __name__ == '__main__':
    main()
