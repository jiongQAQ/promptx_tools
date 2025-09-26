#!/usr/bin/env python3
"""
Claude Code UserPromptSubmit Hook for 05 Chapter Content Generation
This hook automatically injects context for batch processing chapter content generation.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

def main():
    try:
        # 读取用户输入
        input_data = json.loads(sys.stdin.read())
        user_prompt = input_data.get('prompt', '')

        # 检查触发文件或05流程指令
        project_root = os.getcwd()
        trigger_file = Path(project_root) / 'paper' / '.auto-trigger'

        is_05_command = '05流程' in user_prompt or '正文生成' in user_prompt
        has_trigger_file = trigger_file.exists()

        if is_05_command or has_trigger_file:
            # 删除触发文件
            if has_trigger_file:
                trigger_file.unlink()

            # 如果是通过触发文件触发的，修改用户提示
            if has_trigger_file and not is_05_command:
                user_prompt = "开始05流程"

            progress_file = Path(project_root) / 'paper' / '.chapter-progress.json'

            # 读取或初始化进度状态
            progress = load_progress(progress_file)

            if not progress['initialized']:
                # 初始化：扫描章节文件
                chapters = scan_chapter_files(Path(project_root) / 'paper' / 'chapters')
                if not chapters:
                    context = "❌ 错误：未找到chapter目录或章节文件。请确保已执行04章节切割流程。"
                else:
                    progress = initialize_progress(chapters, progress_file)
                    context = generate_single_chapter_context(progress, project_root)
            else:
                # 检查是否已完成
                if not progress['pending']:
                    context = "🎉 05流程已完成！所有章节内容生成完毕。"
                else:
                    # 自动更新进度：检查是否有章节已完成
                    updated_progress = update_progress_from_files(progress, project_root)
                    if updated_progress != progress:
                        progress_file.write_text(json.dumps(updated_progress, indent=2, ensure_ascii=False), encoding='utf-8')
                        progress = updated_progress

                    context = generate_single_chapter_context(progress, project_root)

            # 返回增强的上下文
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": context
                }
            }
            print(json.dumps(output))

        # 其他情况不做处理，让提示正常执行

    except Exception as e:
        # 错误处理：输出错误信息但不阻塞正常流程
        error_output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"⚠️ Hook处理错误: {str(e)}"
            }
        }
        print(json.dumps(error_output))

def load_progress(progress_file):
    """加载或创建进度状态"""
    if progress_file.exists():
        try:
            return json.loads(progress_file.read_text(encoding='utf-8'))
        except:
            pass

    return {
        "initialized": False,
        "currentBatch": 1,
        "batchSize": 4,
        "processed": [],
        "pending": [],
        "failed": [],
        "lastUpdate": datetime.now().isoformat()
    }

def scan_chapter_files(chapter_dir):
    """扫描并排序章节文件"""
    if not chapter_dir.exists():
        return []

    chapters = []
    for file in chapter_dir.glob('chapter.*.json'):
        chapter_id = file.stem.replace('chapter.', '')
        chapters.append(chapter_id)

    # 按章节编号排序
    return sorted(chapters, key=lambda x: parse_chapter_id(x))

def parse_chapter_id(chapter_id):
    """解析章节ID用于排序"""
    parts = []
    for part in chapter_id.split('.'):
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(part)
    return parts

def initialize_progress(chapters, progress_file):
    """初始化进度状态"""
    progress = {
        "initialized": True,
        "currentBatch": 1,
        "batchSize": 4,
        "totalChapters": len(chapters),
        "processed": [],
        "pending": chapters.copy(),
        "failed": [],
        "totalBatches": (len(chapters) + 3) // 4,  # 向上取整
        "lastUpdate": datetime.now().isoformat()
    }

    # 确保目录存在
    progress_file.parent.mkdir(parents=True, exist_ok=True)
    progress_file.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding='utf-8')
    return progress

def generate_single_chapter_context(progress, project_root):
    """生成单个章节的处理上下文"""
    remaining_chapters = progress['pending']

    if not remaining_chapters:
        return "🎉 所有章节已处理完成！"

    # 只取第一个待处理章节
    current_chapter = remaining_chapters[0]

    total_chapters = progress['totalChapters']
    processed_count = len(progress['processed'])

    context = f"📝 处理单个章节：{current_chapter}\n\n"

    # 获取章节详细信息
    chapter_file = Path(project_root) / 'paper' / 'chapters' / f'chapter.{current_chapter}.json'

    if chapter_file.exists():
        try:
            chapter_data = json.loads(chapter_file.read_text(encoding='utf-8'))
            title = chapter_data.get('title', f'章节{current_chapter}')
            prompt = chapter_data.get('prompt', '生成正文内容')
            word_limit = chapter_data.get('word_limit', determine_word_limit(current_chapter))

            context += f"📖 章节信息：\n"
            context += f"- ID: {current_chapter}\n"
            context += f"- 标题: {title}\n"
            context += f"- 字数要求: {word_limit}字\n"
            context += f"- 生成要求: {prompt}\n\n"

        except Exception as e:
            context += f"❌ 读取章节文件失败: {str(e)}\n\n"
    else:
        context += f"❌ 章节文件不存在: {chapter_file}\n\n"

    # 进度信息
    percentage = (processed_count / total_chapters * 100) if total_chapters > 0 else 0
    context += f"📈 当前进度: {processed_count}/{total_chapters} ({percentage:.1f}%)\n\n"

    # 添加工作流程文档引用
    context += "📖 **参考文档**: workflows/05 正文内容生成.md\n"
    context += "请按照该文档中的内容生成原则、特殊处理规则和质量标准执行。\n\n"

    context += "🎯 当前任务：\n"
    context += f"请专注处理章节 {current_chapter}，为其生成text字段内容。\n\n"

    context += "操作要求：\n"
    context += "1. 激活promptx的pra角色进行专业论文写作\n"
    context += "2. 严格按照章节的prompt要求生成内容\n"
    context += "3. 控制字数在指定范围内（允许±10%浮动）\n"
    context += "4. 避免代码片段和文件路径描述\n"
    context += "5. 使用Edit工具更新对应的JSON文件\n"
    context += "6. 仅更新text字段，保持其他字段不变\n"
    context += "7. 完成后简单报告该章节已完成\n\n"

    context += "⚠️ 重要：只处理这一个章节，完成后Stop Hook会自动触发下一章节！\n"

    return context


def determine_word_limit(chapter_id):
    """根据章节层级自动确定字数"""
    levels = chapter_id.count('.')
    if levels == 0:  # 一级章节
        return 800
    elif levels == 1:  # 二级章节
        return 600
    elif levels == 2:  # 三级章节
        return 500
    else:  # 四级及以下
        return 400

def update_progress_after_completion(progress, progress_file, completed_chapters):
    """更新处理完成后的进度"""
    progress['processed'].extend(completed_chapters)
    progress['pending'] = [ch for ch in progress['pending'] if ch not in completed_chapters]
    progress['currentBatch'] += 1
    progress['lastUpdate'] = datetime.now().isoformat()

    progress_file.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding='utf-8')

if __name__ == "__main__":
    main()