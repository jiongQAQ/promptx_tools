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

        # 检查是否为05流程相关指令
        if ('05流程' in user_prompt or '正文生成' in user_prompt or
            '处理完成' in user_prompt or '完成一批' in user_prompt or
            '继续处理' in user_prompt):
            project_root = os.getcwd()
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
                    context = generate_first_batch_context(progress, project_root)
            else:
                # 继续处理下一批
                context = prepare_next_batch(progress, progress_file, project_root)

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

def generate_first_batch_context(progress, project_root):
    """生成第一批处理的上下文"""
    context = f"🚀 开始05流程：已发现{progress['totalChapters']}个章节文件，准备分批处理。\n\n"

    # 添加工作流程文档引用
    context += "📖 **参考文档**: workflows/05 正文内容生成.md\n"
    context += "请按照该文档中的内容生成原则、特殊处理规则和质量标准执行。\n\n"

    context += generate_batch_context(progress, project_root)
    return context

def prepare_next_batch(progress, progress_file, project_root):
    """准备下一批处理"""
    if not progress['pending']:
        return "🎉 05流程已完成！所有章节内容生成完毕。\n\n📊 最终统计:\n" + \
               f"✅ 成功处理: {len(progress['processed'])}个章节\n" + \
               f"❌ 处理失败: {len(progress['failed'])}个章节"

    return generate_batch_context(progress, project_root)

def generate_batch_context(progress, project_root):
    """生成当前批次的上下文信息"""
    if not progress['pending']:
        return "🎉 所有章节已处理完成！"

    # 获取当前批次章节
    batch_size = progress['batchSize']
    current_batch = progress['pending'][:batch_size]

    context = f"📋 当前处理第{progress['currentBatch']}批章节（共{progress['totalBatches']}批）:\n\n"
    context += "需要处理的章节:\n"

    for i, chapter_id in enumerate(current_batch, 1):
        chapter_file = Path(project_root) / 'paper' / 'chapters' / f'chapter.{chapter_id}.json'
        if chapter_file.exists():
            try:
                chapter_data = json.loads(chapter_file.read_text(encoding='utf-8'))
                title = chapter_data.get('title', f'章节{chapter_id}')
                prompt = chapter_data.get('prompt', '生成正文内容')
                word_limit = chapter_data.get('word_limit', determine_word_limit(chapter_id))

                context += f"{i}. 章节 {chapter_id}: {title}\n"
                context += f"   生成要求: {prompt[:100]}{'...' if len(prompt) > 100 else ''}\n"
                context += f"   字数要求: {word_limit}字\n\n"
            except Exception as e:
                context += f"{i}. 章节 {chapter_id}: [读取失败: {str(e)}]\n\n"
        else:
            context += f"{i}. 章节 {chapter_id}: [文件不存在]\n\n"

    # 进度信息
    total_processed = len(progress['processed'])
    total_chapters = progress['totalChapters']
    percentage = (total_processed / total_chapters * 100) if total_chapters > 0 else 0

    context += f"📈 进度: {total_processed}/{total_chapters} ({percentage:.1f}%)\n\n"

    context += "🎯 处理要求（详见05工作流程文档）:\n"
    context += "1. **内容生成原则**:\n"
    context += "   - 严格按照每个章节的prompt字段生成内容\n"
    context += "   - 使用学术化表达，逻辑清晰，层次分明\n"
    context += "   - 确保技术描述准确，符合软件工程规范\n"
    context += "   - 字数控制在指定范围内（允许±10%浮动）\n\n"
    context += "2. **特殊处理规则**:\n"
    context += "   - 包含imagePath的章节：假设图片存在，正文中自然引用'如图X所示...'\n"
    context += "   - 包含tablePath的章节：假设表格完整，分析'表X展示了...'\n"
    context += "   - 代码实现章节：结合项目源码特点描述实现细节\n\n"
    context += "3. **操作要求**:\n"
    context += "   - 逐个处理章节，为每个章节生成text字段内容\n"
    context += "   - 使用MultiEdit或Edit工具更新对应的JSON文件\n"
    context += "   - 仅更新text字段，保持其他字段不变\n"
    context += "   - 处理完成后必须说'继续05流程'来自动进入下一批处理\n"

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