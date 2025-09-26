#!/usr/bin/env python3
"""
05流程自动继续Hook - Stop Hook
当AI完成当前章节后，自动标记完成并触发下一个章节
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

def main():
    try:
        # 读取Stop Hook输入
        input_data = json.loads(sys.stdin.read())

        # 检查是否有transcript路径
        transcript_path = input_data.get("transcript_path")
        if not transcript_path or not Path(transcript_path).exists():
            output = {"continue": True}
            print(json.dumps(output))
            return

        # 读取transcript内容
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()

        # 检查是否是05流程的章节完成
        if should_continue_05_process(transcript_content):
            project_root = os.getcwd()
            progress_file = Path(project_root) / 'paper' / '.chapter-progress.json'

            if progress_file.exists():
                progress = json.loads(progress_file.read_text(encoding='utf-8'))

                # 标记当前章节为完成
                if progress.get('pending'):
                    completed_chapter = progress['pending'][0]  # 当前处理的章节

                    # 更新进度
                    progress['processed'].append(completed_chapter)
                    progress['pending'].remove(completed_chapter)
                    progress['lastUpdate'] = datetime.now().isoformat()

                    # 保存进度
                    progress_file.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding='utf-8')

                    print(f"✅ 章节 {completed_chapter} 已标记完成", file=sys.stderr)

                    # 如果还有待处理章节，阻止停止并重新提交
                    if progress['pending']:
                        # 创建一个简单的触发文件
                        trigger_file = Path(project_root) / 'paper' / '.auto-trigger'
                        trigger_file.write_text("开始05流程", encoding='utf-8')

                        output = {
                            "continue": False,
                            "stopReason": f"✅ 章节 {completed_chapter} 已完成，自动继续下一章节..."
                        }
                        print(json.dumps(output))
                        return

        # 默认允许正常停止
        output = {"continue": True}
        print(json.dumps(output))

    except Exception as e:
        # 错误情况下允许正常停止
        output = {
            "continue": True,
            "debug": f"Auto-continue error: {str(e)}"
        }
        print(json.dumps(output))

def should_continue_05_process(transcript_content):
    """检查是否应该自动继续05流程"""
    if not transcript_content:
        return False

    # 检查是否包含章节完成的标志
    completion_indicators = [
        "已完成该章节",
        "章节已处理完成",
        "text字段已更新",
        "章节内容生成完成",
        "已成功更新",
        "处理完成"
    ]

    # 检查是否提到了JSON文件更新
    file_update_indicators = [
        ".json",
        "Edit",
        "MultiEdit",
        "updated",
        "text字段"
    ]

    has_completion = any(indicator in transcript_content for indicator in completion_indicators)
    has_file_update = any(indicator in transcript_content for indicator in file_update_indicators)

    # 排除整个流程完成的情况
    final_indicators = [
        "所有章节已处理完成",
        "05流程已完成",
        "全部章节完成"
    ]

    is_final = any(indicator in transcript_content for indicator in final_indicators)

    return has_completion and has_file_update and not is_final

if __name__ == "__main__":
    main()