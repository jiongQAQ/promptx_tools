#!/usr/bin/env python3
"""
05流程监控脚本 - 监控触发文件并自动提交Claude Code指令
"""

import time
import subprocess
import os
from pathlib import Path

def main():
    project_root = Path.cwd()
    trigger_file = project_root / 'paper' / '.auto-trigger'

    print("🔍 开始监控05流程自动触发...")

    try:
        while True:
            if trigger_file.exists():
                print("🚀 检测到触发文件，自动提交'开始05流程'")

                # 删除触发文件
                trigger_file.unlink()

                # 使用Claude Code CLI提交指令
                try:
                    result = subprocess.run(
                        ["claude-code", "--prompt", "开始05流程"],
                        cwd=str(project_root),
                        capture_output=True,
                        text=True,
                        timeout=300
                    )

                    if result.returncode == 0:
                        print("✅ 指令提交成功，等待处理...")
                    else:
                        print(f"❌ 指令提交失败: {result.stderr}")

                except subprocess.TimeoutExpired:
                    print("⚠️ 指令执行超时，继续监控...")
                except Exception as e:
                    print(f"❌ 执行错误: {e}")

            time.sleep(2)  # 每2秒检查一次

    except KeyboardInterrupt:
        print("\n⏹️ 监控已停止")

if __name__ == "__main__":
    main()