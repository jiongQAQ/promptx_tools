#!/usr/bin/env python3
"""
Word to Screenshots 简化版
将Word文档转换为PNG图片（每页一张）

依赖:
    - LibreOffice: brew install --cask libreoffice
    - Poppler: brew install poppler

使用方法:
    python3 word-to-screenshots.py <word文件路径> [输出目录] [DPI]

示例:
    python3 word-to-screenshots.py paper.docx
    python3 word-to-screenshots.py paper.docx reference-papers/ 300
"""

import subprocess
import os
import sys
import shutil
from pathlib import Path


def check_dependencies():
    """检查必要的依赖是否已安装"""
    errors = []

    # 检查 LibreOffice
    soffice_paths = [
        '/Applications/LibreOffice.app/Contents/MacOS/soffice',
        '/usr/bin/soffice',
        shutil.which('soffice')
    ]

    soffice = None
    for path in soffice_paths:
        if path and os.path.exists(path):
            soffice = path
            break

    if not soffice:
        errors.append("❌ LibreOffice未安装")
        errors.append("   安装命令: brew install --cask libreoffice")

    # 检查 pdftoppm
    pdftoppm = shutil.which('pdftoppm')
    if not pdftoppm:
        errors.append("❌ Poppler未安装")
        errors.append("   安装命令: brew install poppler")

    if errors:
        print("\n".join(errors))
        return False, None, None

    return True, soffice, pdftoppm


def word_to_screenshots(word_file, output_dir=None, dpi=300):
    """
    将Word文档转换为截图

    参数:
        word_file: Word文档路径
        output_dir: 输出目录（默认为reference-papers）
        dpi: 分辨率（默认300）

    返回:
        bool: 转换是否成功
    """
    # 验证Word文件
    word_path = Path(word_file)
    if not word_path.exists():
        print(f"❌ 文件不存在: {word_file}")
        return False

    if not (word_file.endswith('.docx') or word_file.endswith('.doc')):
        print(f"❌ 仅支持.docx或.doc格式")
        return False

    # 检查依赖
    deps_ok, soffice, pdftoppm = check_dependencies()
    if not deps_ok:
        return False

    # 创建输出目录
    if output_dir is None:
        output_dir = Path.cwd() / 'reference-papers'
    else:
        output_dir = Path(output_dir)

    base_name = word_path.stem
    screenshots_dir = output_dir / f"{base_name}_screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    print(f"📦 开始处理: {word_file}")
    print(f"📂 输出目录: {screenshots_dir}")
    print(f"🎯 分辨率: {dpi} DPI")

    # 临时PDF文件
    temp_pdf = screenshots_dir / f"{base_name}_temp.pdf"

    try:
        # 步骤1: Word → PDF
        print(f"\n🔄 步骤1: 转换Word为PDF...")
        result = subprocess.run(
            [soffice, '--headless', '--convert-to', 'pdf',
             '--outdir', str(screenshots_dir), str(word_path)],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"❌ PDF转换失败: {result.stderr}")
            return False

        # LibreOffice会生成 basename.pdf
        generated_pdf = screenshots_dir / f"{base_name}.pdf"
        if generated_pdf.exists() and generated_pdf != temp_pdf:
            generated_pdf.rename(temp_pdf)

        if not temp_pdf.exists():
            print("❌ PDF文件未生成")
            return False

        print("✅ PDF生成成功")

        # 步骤2: PDF → PNG
        print(f"\n🔄 步骤2: 转换PDF为图片...")
        output_prefix = screenshots_dir / 'page'

        result = subprocess.run(
            ['pdftoppm', '-png', '-r', str(dpi),
             str(temp_pdf), str(output_prefix)],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            print(f"❌ 图片转换失败: {result.stderr}")
            return False

        print("✅ 图片生成成功")

        # 重命名图片文件
        print(f"\n📝 重命名图片文件...")
        image_files = sorted(screenshots_dir.glob('page-*.png'))
        renamed_files = []

        for idx, img_file in enumerate(image_files, 1):
            new_name = f"page-{str(idx).zfill(3)}.png"
            new_path = screenshots_dir / new_name
            img_file.rename(new_path)
            renamed_files.append(new_path)

        # 清理临时PDF
        if temp_pdf.exists():
            temp_pdf.unlink()
            print("🗑️  清理临时文件")

        # 统计信息
        total_size = sum(f.stat().st_size for f in renamed_files)

        print(f"\n📊 统计信息:")
        print(f"  - 总页数: {len(renamed_files)}")
        print(f"  - 总大小: {total_size / 1024 / 1024:.2f} MB")
        print(f"  - 分辨率: {dpi} DPI")
        print(f"  - 输出目录: {screenshots_dir.name}")

        print("\n🎉 转换完成！")
        print(f"\n📂 图片位置: {screenshots_dir}")

        return True

    except subprocess.TimeoutExpired:
        print("❌ 转换超时（文件可能过大）")
        return False
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print(f"  python3 {sys.argv[0]} <word文件路径> [输出目录] [DPI]")
        print("\n示例:")
        print(f"  python3 {sys.argv[0]} paper.docx")
        print(f"  python3 {sys.argv[0]} paper.docx reference-papers/")
        print(f"  python3 {sys.argv[0]} paper.docx reference-papers/ 300")
        print("\n默认输出目录: reference-papers/")
        print("默认DPI: 300")
        sys.exit(1)

    word_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300

    success = word_to_screenshots(word_file, output_dir, dpi)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()