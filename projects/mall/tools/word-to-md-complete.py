#!/usr/bin/env python3
"""
Word to Markdown 完整转换工具
一次性输出正确的MD格式，包含图片引用

使用方法:
    python3 word-to-md-complete.py <word文件路径> [输出目录]

示例:
    python3 word-to-md-complete.py paper.docx  # 输出到 reference-papers/ 目录
    python3 word-to-md-complete.py paper.docx custom-dir/  # 自定义输出目录
"""

import zipfile
import os
import sys
import shutil
import re
from pathlib import Path
import subprocess


def word_to_markdown_complete(word_file, output_dir=None):
    """
    完整的Word转Markdown转换

    参数:
        word_file: Word文档路径
        output_dir: 输出目录（可选，默认为reference-papers）

    返回:
        bool: 转换是否成功
    """
    # 验证Word文件
    word_path = Path(word_file)
    if not word_path.exists():
        print(f"❌ 文件不存在: {word_file}")
        return False

    if not word_file.endswith('.docx'):
        print(f"❌ 仅支持.docx格式")
        return False

    # 创建输出目录，默认为reference-papers
    if output_dir is None:
        output_dir = Path.cwd() / 'reference-papers'
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)

    # 获取文件基础名
    base_name = word_path.stem

    print(f"📦 开始处理: {word_file}")
    print(f"📂 输出目录: {output_dir}")

    # 1. 提取图片
    images_dir = output_dir / f"{base_name}_images"
    if images_dir.exists():
        shutil.rmtree(images_dir)
    images_dir.mkdir()

    image_map = {}
    try:
        with zipfile.ZipFile(word_file, 'r') as zip_ref:
            image_files = [f for f in zip_ref.namelist() if f.startswith('word/media/')]
            print(f"🖼️  找到 {len(image_files)} 个图片")

            for idx, img_file in enumerate(image_files, 1):
                ext = os.path.splitext(img_file)[1] or '.png'
                new_name = f"图{idx}{ext}"

                # 提取图片
                zip_ref.extract(img_file, output_dir)
                old_path = output_dir / img_file
                new_path = images_dir / new_name

                shutil.move(str(old_path), str(new_path))
                image_map[idx] = new_name

            # 清理临时目录
            word_dir = output_dir / 'word'
            if word_dir.exists():
                shutil.rmtree(word_dir)

    except Exception as e:
        print(f"❌ 图片提取失败: {e}")
        return False

    # 2. 转换Word为HTML (使用macOS的textutil)
    try:
        html_file = output_dir / f"{base_name}.html"
        result = subprocess.run(
            ['textutil', '-convert', 'html', str(word_path), '-output', str(html_file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ HTML转换失败: {result.stderr}")
            return False

        print(f"✅ HTML转换成功")

    except Exception as e:
        print(f"❌ HTML转换失败: {e}")
        print(f"💡 提示: 此工具需要macOS的textutil命令")
        return False

    # 3. HTML转Markdown并插入图片
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()

        # 提取CSS样式定义
        css_match = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
        font_size_map = {}
        if css_match:
            css = css_match.group(1)
            # 提取每个段落类的字体大小
            for match in re.finditer(r'p\.(p\d+)\s*\{[^}]*font:\s*(\d+\.?\d*)px', css):
                class_name = match.group(1)
                font_size = float(match.group(2))
                font_size_map[class_name] = font_size

        # 提取body内容
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
        if body_match:
            html = body_match.group(1)

        # 处理表格
        def parse_table(table_html):
            rows = []
            # 移除tbody标签，处理tr
            for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', table_html, re.DOTALL):
                cells = []
                # 处理每个td单元格
                for td in re.finditer(r'<td[^>]*>(.*?)</td>', tr.group(1), re.DOTALL):
                    # 提取单元格内的所有文本，移除所有HTML标签
                    cell_html = td.group(1)
                    # 移除所有标签，只保留文本
                    cell_text = re.sub(r'<[^>]+>', ' ', cell_html)
                    # 清理多余空格和换行
                    cell_text = ' '.join(cell_text.split()).strip()
                    # 如果单元格为空，用空格代替
                    if not cell_text:
                        cell_text = ' '
                    cells.append(cell_text)
                if cells:
                    rows.append(cells)

            if not rows:
                return ""

            # 生成Markdown表格
            md_lines = []
            if rows:
                # 表头
                md_lines.append('| ' + ' | '.join(rows[0]) + ' |')
                md_lines.append('| ' + ' | '.join(['---'] * len(rows[0])) + ' |')
                # 数据行
                for row in rows[1:]:
                    md_lines.append('| ' + ' | '.join(row) + ' |')

            return '\n'.join(md_lines)

        # 按顺序处理HTML元素（段落、表格、列表）
        lines = []
        pos = 0

        # 找到所有元素及其位置
        elements = []

        # 查找所有段落
        for p_match in re.finditer(r'<p[^>]*class="([^"]*)"[^>]*>.*?</p>', html, re.DOTALL):
            elements.append(('p', p_match.start(), p_match.end(), p_match))

        # 查找所有表格
        for t_match in re.finditer(r'<table[^>]*>.*?</table>', html, re.DOTALL):
            elements.append(('table', t_match.start(), t_match.end(), t_match))

        # 查找所有列表
        for ul_match in re.finditer(r'<ul[^>]*>.*?</ul>', html, re.DOTALL):
            elements.append(('ul', ul_match.start(), ul_match.end(), ul_match))

        # 按位置排序
        elements.sort(key=lambda x: x[1])

        # 按顺序处理每个元素
        for elem_type, start, end, match in elements:
            if elem_type == 'p':
                class_name = match.group(1)
                content = match.group(0)
                # 提取段落内容
                text_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
                if text_match:
                    text = re.sub(r'<[^>]+>', '', text_match.group(1)).strip()
                    if text and not text.startswith('table.') and not text.startswith('span.'):
                        # 根据字体大小判断标题级别
                        if class_name in font_size_map:
                            font_size = font_size_map[class_name]
                            if font_size >= 24:
                                text = f'## {text}'
                            elif font_size >= 18:
                                text = f'### {text}'
                            elif font_size >= 16:
                                text = f'#### {text}'
                        lines.append(text)

            elif elem_type == 'table':
                table_md = parse_table(match.group(0))
                if table_md:
                    lines.append('')
                    lines.append(table_md)
                    lines.append('')

            elif elem_type == 'ul':
                for li in re.finditer(r'<li[^>]*>(.*?)</li>', match.group(0), re.DOTALL):
                    text = re.sub(r'<[^>]+>', '', li.group(1)).strip()
                    if text:
                        lines.append(f'- {text}')

        # 4. 智能插入图片引用
        new_lines = []
        img_counter = 1

        for i, line in enumerate(lines):
            new_lines.append(line)

            # 检测图表标题（图X-X 或 图X- X 格式）
            if re.match(r'^图\s*\d+[-\s]*\d+', line):
                # 插入图片引用
                if img_counter in image_map:
                    img_name = image_map[img_counter]
                    img_path = f"{base_name}_images/{img_name}"

                    new_lines.append('')
                    new_lines.append(f'![{line}]({img_path})')
                    new_lines.append('')

                    img_counter += 1

        # 组合Markdown内容
        markdown = '\n'.join(new_lines)

        # 5. 保存Markdown文件
        md_file = output_dir / f"{base_name}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"✅ Markdown生成成功")
        print(f"📄 文件: {md_file}")
        print(f"🖼️  插入图片: {img_counter - 1} 个")

        # 统计信息
        lines_count = len(markdown.split('\n'))
        img_refs = markdown.count('![图')
        heading_count = markdown.count('\n## ') + markdown.count('\n### ') + markdown.count('\n#### ')
        table_count = markdown.count('| --- |')
        list_count = markdown.count('\n- ')
        file_size = len(markdown) / 1024  # KB

        print(f"\n📊 统计信息:")
        print(f"  - 总行数: {lines_count}")
        print(f"  - 标题数: {heading_count}")
        print(f"  - 表格数: {table_count}")
        print(f"  - 列表项: {list_count}")
        print(f"  - 图片引用: {img_refs}")
        print(f"  - 图片文件: {len(image_map)}")
        print(f"  - MD大小: {file_size:.1f} KB")
        print(f"  - 图片目录: {images_dir.name}")

        return True

    except Exception as e:
        print(f"❌ Markdown生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print(f"  python3 {sys.argv[0]} <word文件路径> [输出目录]")
        print("\n示例:")
        print(f"  python3 {sys.argv[0]} paper.docx")
        print(f"  python3 {sys.argv[0]} paper.docx custom-output/")
        print("\n默认输出目录: reference-papers/")
        sys.exit(1)

    word_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    success = word_to_markdown_complete(word_file, output_dir)

    if success:
        print("\n🎉 转换完成！")
        sys.exit(0)
    else:
        print("\n❌ 转换失败！")
        sys.exit(1)


if __name__ == '__main__':
    main()