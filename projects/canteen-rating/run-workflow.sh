#!/usr/bin/env bash
# 轻量：后台执行 workflows 各流程 + 可拼接自定义提示
# 兼容 macOS 自带 Bash 3.2（避免用数组/mapfile 等）

set -euo pipefail

# == 基础路径（按你的目录约定） ==
WORKDIR="$(pwd)"
WF_DIR="$WORKDIR/workflows"
LOG_DIR="$WORKDIR/.logs"
PAPER_DIR="$WORKDIR/paper"
SPLITS_DIR="$PAPER_DIR/splits"

# 可用环境变量覆盖（例如：CLAUDE_CMD="claude -m sonnet -p" ./run-workflow.sh 01）
CLAUDE_CMD="${CLAUDE_CMD:claude1 -p}"

mkdir -p "$LOG_DIR"

usage() {
  cat <<EOF
用法:
  $(basename "$0") STEP [<chapter>] [--extra "附加提示"] [--extra-file 路径]

STEP:
  01      -> 执行 "01 大纲确认与生成.txt"
  01-1    -> 执行 "01-1识别实体类.txt"
  01-2    -> 执行 "01-2单体 ER 图批量生成.txt"
  02      -> 执行 "02 基于大纲预填内容计划.txt"
  02-1    -> 执行 "02-1 content.json 按章拆分.txt"
  03 <ch> -> 执行 "03｜正文与素材生成.txt"，并附加“当前分章文件: paper/splits/content.ch<ch>.json”

可选项:
  --extra "文本"       追加一次性附加提示（论文题目/主题/受众/风格等）
  --extra-file 路径    从文件读取附加提示并追加

示例:
  $(basename "$0") 01 --extra "论文题目：健身房预约系统"
  $(basename "$0") 01-1
  $(basename "$0") 01-2
  $(basename "$0") 02 --extra-file workflows/extras/02.txt
  $(basename "$0") 02-1
  $(basename "$0") 03 1 --extra "仅生成第1章，保持学术风格"
EOF
}

# 组装最终 prompt：模板正文 + 附加提示文本/文件
# 用临时文件承载，便于复查
build_prompt() {
  wf_file="$1"; shift || true
  extra_text="${1-}"; shift || true
  extra_file="${1-}"; shift || true

  ts="$(date +%Y%m%d-%H%M%S)"
  tmp="$LOG_DIR/.prompt.$ts.$RANDOM.txt"
  : > "$tmp"

  if [ ! -f "$wf_file" ]; then
    echo "❌ 未找到工作流模板：$wf_file" >&2
    exit 1
  fi

  cat "$wf_file" >> "$tmp"

  if [ -n "${extra_file:-}" ] && [ -f "$extra_file" ]; then
    {
      echo
      echo "# 附加提示（file）"
      cat "$extra_file"
    } >> "$tmp"
  fi

  if [ -n "${extra_text:-}" ]; then
    {
      echo
      echo "# 附加提示（inline）"
      echo "$extra_text"
    } >> "$tmp"
  fi

  echo "$tmp"
}

run_bg() {
  prompt_file="$1"
  tag="$2"
  ts="$(date +%Y%m%d-%H%M%S)"
  log="$LOG_DIR/${tag}.${ts}.log"

  # 使用 eval 让包含空格的 CLAUDE_CMD 也能正确执行
  # 注意：prompt 中如有双引号，不影响这里的命令执行（已由 cat 输出）。
  eval "$CLAUDE_CMD \"\$(cat \"$prompt_file\")\" >\"$log\" 2>&1 &"
  pid=$!

  echo "✅ 已启动：$tag  PID=$pid"
  echo "📝 日志：$log"
  echo "$pid" > "$LOG_DIR/${tag}.${ts}.pid"
  # 如需清理临时 prompt，可在此 rm -f "$prompt_file"
}

# ---------------- 解析参数 ----------------
if [ $# -lt 1 ]; then usage; exit 1; fi

STEP="$1"; shift || true
CHAPTER=""
EXTRA_TEXT=""
EXTRA_FILE=""

# STEP=03 允许跟章节号
if [ "$STEP" = "03" ]; then
  if [ $# -lt 1 ]; then
    echo "❌ 03 需要指定章节号，例如：$0 03 1" >&2
    exit 1
  fi
  CHAPTER="$1"
  shift || true
fi

# 剩余选项
while [ $# -gt 0 ]; do
  case "$1" in
    --extra)
      shift || true
      [ $# -gt 0 ] || { echo "❌ --extra 需要文本"; exit 1; }
      EXTRA_TEXT="$1"
      ;;
    --extra-file)
      shift || true
      [ $# -gt 0 ] || { echo "❌ --extra-file 需要路径"; exit 1; }
      EXTRA_FILE="$1"
      ;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "❌ 未知参数：$1"; usage; exit 1;;
  esac
  shift || true
done

# ---------------- 路径映射 ----------------
WF_FILE=""
TAG=""

case "$STEP" in
  01)
    WF_FILE="$WF_DIR/01 大纲确认与生成.txt"
    TAG="01-outline"
    ;;
  01-1)
    WF_FILE="$WF_DIR/01-1识别实体类.txt"
    TAG="01-1-entities"
    ;;
  01-2)
    WF_FILE="$WF_DIR/01-2单体 ER 图批量生成.txt"
    TAG="01-2-er-batch"
    ;;
  02)
    WF_FILE="$WF_DIR/02 基于大纲预填内容计划.txt"
    TAG="02-content-plan"
    ;;
  02-1)
    WF_FILE="$WF_DIR/02-1 content.json 按章拆分.txt"
    TAG="02-1-split"
    ;;
  03)
    WF_FILE="$WF_DIR/03｜正文与素材生成.txt"
    TAG="03-generate-ch$CHAPTER"
    ;;
  *)
    echo "❌ 未知 STEP：$STEP"; usage; exit 1;;
esac

# ---------------- 组装并执行 ----------------
PROMPT_FILE="$(build_prompt "$WF_FILE" "$EXTRA_TEXT" "$EXTRA_FILE")"

# STEP=03 附加当前分章文件上下文
if [ "$STEP" = "03" ]; then
  CH_FILE="$SPLITS_DIR/content.ch${CHAPTER}.json"
  if [ ! -f "$CH_FILE" ]; then
    echo "❌ 未找到分章文件：$CH_FILE" >&2
    exit 1
  fi
  {
    echo
    echo "# 附加上下文"
    echo "当前分章文件：$CH_FILE"
  } >> "$PROMPT_FILE"
fi

run_bg "$PROMPT_FILE" "$TAG"