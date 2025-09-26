#!/usr/bin/env python3
"""
05流程PostToolUse Hook - 检测JSON文件更新并自动触发下一章节
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

def main():
    try:
        # 读取PostToolUse Hook输入
        input_data = json.loads(sys.stdin.read())

        # 检查是否是Edit工具且操作JSON文件
        tool_name = input_data.get("tool_name", "")
        if tool_name not in ["Edit", "MultiEdit"]:
            # 非编辑工具，允许执行
            output = {"continue": True}
            print(json.dumps(output))
            return

        # 检查是否操作了chapter文件
        tool_input = input_data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")

        if "chapter" not in file_path or not file_path.endswith(".json"):
            # 不是chapter文件，允许执行
            output = {"continue": True}
            print(json.dumps(output))
            return

        # 是chapter文件编辑，检查05流程进度
        project_root = os.getcwd()
        progress_file = Path(project_root) / 'paper' / '.chapter-progress.json'

        if not progress_file.exists():
            # 没有进度文件，允许执行
            output = {"continue": True}
            print(json.dumps(output))
            return

        # 读取进度信息
        progress = json.loads(progress_file.read_text(encoding='utf-8'))

        # 提取当前处理的章节ID
        chapter_filename = Path(file_path).name
        if chapter_filename.startswith("chapter.") and chapter_filename.endswith(".json"):
            chapter_id = chapter_filename[8:-5]  # 去掉 "chapter." 和 ".json"

            # 检查是否是当前待处理的章节
            if progress.get('pending') and chapter_id == progress['pending'][0]:
                # 标记该章节为完成
                progress['processed'].append(chapter_id)
                progress['pending'].remove(chapter_id)
                progress['lastUpdate'] = datetime.now().isoformat()

                # 保存进度
                progress_file.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding='utf-8')

                print(f"✅ 章节 {chapter_id} 已标记完成", file=sys.stderr)

                # 如果还有待处理章节，创建触发文件
                if progress['pending']:
                    trigger_file = Path(project_root) / 'paper' / '.auto-trigger'
                    trigger_file.write_text("开始05流程", encoding='utf-8')
                    print(f"🔄 已创建触发文件，将自动处理下一章节", file=sys.stderr)

        # 允许工具执行
        output = {"continue": True}
        print(json.dumps(output))

    except Exception as e:
        # 错误情况下允许工具执行
        output = {
            "continue": True,
            "debug": f"PostToolUse hook error: {str(e)}"
        }
        print(json.dumps(output))

if __name__ == "__main__":
    main()