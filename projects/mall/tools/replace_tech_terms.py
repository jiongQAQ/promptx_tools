#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量替换论文章节中的技术名词空格
"""

import json
import os
from pathlib import Path

# 定义需要替换的技术名词映射（带空格 -> 不带空格）
TECH_TERMS_MAP = {
    "Spring Cloud": "SpringCloud",
    "Spring Boot": "SpringBoot",
    "Spring Security": "SpringSecurity",
    "Spring Framework": "SpringFramework",
    "Vue.js": "Vue",
    "My Batis": "MyBatis",
    "MyBatis Plus": "MyBatisPlus",
    "API Gateway": "API Gateway",  # 保持不变
    "MySql": "MySQL",
    "mysql": "MySQL",
    "MYSQL": "MySQL",
}


def replace_tech_terms_in_text(text):
    """替换文本中的技术名词"""
    if not text:
        return text

    result = text
    for old_term, new_term in TECH_TERMS_MAP.items():
        result = result.replace(old_term, new_term)

    return result


def process_chapter_file(file_path):
    """处理单个章节文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        modified = False

        # 替换 content 字段
        if 'content' in data and isinstance(data['content'], str):
            original = data['content']
            data['content'] = replace_tech_terms_in_text(original)
            if data['content'] != original:
                modified = True

        # 替换 text 字段
        if 'text' in data and isinstance(data['text'], str):
            original = data['text']
            data['text'] = replace_tech_terms_in_text(original)
            if data['text'] != original:
                modified = True

        # 替换 title 字段
        if 'title' in data and isinstance(data['title'], str):
            original = data['title']
            data['title'] = replace_tech_terms_in_text(original)
            if data['title'] != original:
                modified = True

        # 替换 items 数组中的内容
        if 'items' in data and isinstance(data['items'], list):
            for item in data['items']:
                if isinstance(item, dict):
                    if 'text' in item and isinstance(item['text'], str):
                        original = item['text']
                        item['text'] = replace_tech_terms_in_text(original)
                        if item['text'] != original:
                            modified = True

                    if 'content' in item and isinstance(item['content'], str):
                        original = item['content']
                        item['content'] = replace_tech_terms_in_text(original)
                        if item['content'] != original:
                            modified = True

                    if 'title' in item and isinstance(item['title'], str):
                        original = item['title']
                        item['title'] = replace_tech_terms_in_text(original)
                        if item['title'] != original:
                            modified = True

        # 如果有修改，写回文件
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, file_path.name

        return False, file_path.name

    except Exception as e:
        print(f"❌ 处理文件失败: {file_path.name} - {str(e)}")
        return False, file_path.name


def main():
    """主函数"""
    # 获取章节目录
    chapters_dir = Path(__file__).parent.parent / 'paper' / 'chapters'

    if not chapters_dir.exists():
        print(f"❌ 章节目录不存在: {chapters_dir}")
        return

    # 获取所有JSON文件
    chapter_files = sorted(chapters_dir.glob('chapter.*.json'))

    print(f"\n{'='*60}")
    print(f"🔍 开始批量替换技术名词空格")
    print(f"📁 章节目录: {chapters_dir}")
    print(f"📊 发现文件: {len(chapter_files)} 个")
    print(f"{'='*60}\n")

    print("📝 替换规则:")
    for old_term, new_term in TECH_TERMS_MAP.items():
        if old_term != new_term:
            print(f"   {old_term} → {new_term}")
    print()

    modified_count = 0
    unchanged_count = 0

    for chapter_file in chapter_files:
        modified, filename = process_chapter_file(chapter_file)
        if modified:
            print(f"✅ 已修改: {filename}")
            modified_count += 1
        else:
            unchanged_count += 1

    print(f"\n{'='*60}")
    print(f"✅ 修改完成: {modified_count} 个文件")
    print(f"⚪ 无需修改: {unchanged_count} 个文件")
    print(f"📊 总计: {len(chapter_files)} 个文件")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
