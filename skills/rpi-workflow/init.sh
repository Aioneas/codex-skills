#!/bin/sh
# RPI Workflow - 初始化脚本
# 为项目创建 RPI 工作目录结构

set -e

PROJECT_DIR="${1:-.}"
RPI_DIR="$PROJECT_DIR/.rpi"

echo "🚀 初始化 RPI 工作流..."
echo "项目目录: $PROJECT_DIR"

# 创建目录结构
mkdir -p "$RPI_DIR/proposals"
mkdir -p "$RPI_DIR/constraints"
mkdir -p "$RPI_DIR/plans"
mkdir -p "$RPI_DIR/implementations"

# 检测可用模型
echo ""
echo "📋 检测可用模型..."
MODELS=$(minis-model-use list --compact 2>/dev/null || echo "[]")

# 检测项目信息
echo ""
echo "🔍 检测项目信息..."

PROJECT_NAME=$(basename "$PROJECT_DIR")
PROJECT_TYPE="unknown"
LANGUAGES="[]"
FRAMEWORKS="[]"

# 检测语言
if [ -f "$PROJECT_DIR/package.json" ]; then
    LANGUAGES='["javascript"]'
    if grep -q "typescript" "$PROJECT_DIR/package.json" 2>/dev/null; then
        LANGUAGES='["javascript","typescript"]'
    fi
fi

if [ -f "$PROJECT_DIR/requirements.txt" ] || [ -f "$PROJECT_DIR/pyproject.toml" ]; then
    if [ "$LANGUAGES" = "[]" ]; then
        LANGUAGES='["python"]'
    else
        LANGUAGES='["javascript","typescript","python"]'
    fi
fi

if [ -f "$PROJECT_DIR/go.mod" ]; then
    LANGUAGES='["go"]'
fi

# 检测框架
if [ -f "$PROJECT_DIR/package.json" ]; then
    if grep -q "react" "$PROJECT_DIR/package.json" 2>/dev/null; then
        FRAMEWORKS='["react"]'
    elif grep -q "vue" "$PROJECT_DIR/package.json" 2>/dev/null; then
        FRAMEWORKS='["vue"]'
    elif grep -q "next" "$PROJECT_DIR/package.json" 2>/dev/null; then
        FRAMEWORKS='["nextjs"]'
    fi
fi

# 生成配置文件
cat > "$RPI_DIR/config.json" <<EOF
{
  "project_name": "$PROJECT_NAME",
  "project_type": "$PROJECT_TYPE",
  "languages": $LANGUAGES,
  "frameworks": $FRAMEWORKS,
  "codebase_paths": ["./src", "./lib", "./app"],
  "available_models": $MODELS,
  "context_limit": 80000,
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

# 创建 README
cat > "$RPI_DIR/README.md" <<'EOF'
# RPI 工作流目录

本目录由 RPI Workflow 技能自动生成，用于管理复杂项目的开发流程。

## 目录结构

- `proposals/` - 需求提案（Research 阶段输出）
- `constraints/` - 约束集（从提案中提取）
- `plans/` - 执行计划（Plan 阶段输出）
- `implementations/` - 实现记录（Implementation 阶段输出）
- `config.json` - 项目配置

## 工作流程

1. **Research**：需求分析 → 生成提案
2. **Plan**：提案细化 → 生成执行计划
3. **Implementation**：执行计划 → 生成实现记录

## 使用建议

- 每个阶段完成后清空上下文，保持专注
- 所有文档使用 Markdown 格式
- 提案和计划应版本控制（Git）
- 实现记录可选择性提交

## 参考

- 技能文档：/var/minis/skills/rpi-workflow/SKILL.md
- 原始项目：https://github.com/GuDaStudio/commands
EOF

# 创建 .gitignore
cat > "$RPI_DIR/.gitignore" <<'EOF'
# 实现记录（可选择性提交）
implementations/

# 临时文件
*.tmp
*.log
EOF

echo ""
echo "✅ RPI 工作流初始化完成！"
echo ""
echo "📁 目录结构："
echo "   $RPI_DIR/"
echo "   ├── proposals/          # 需求提案"
echo "   ├── constraints/        # 约束集"
echo "   ├── plans/             # 执行计划"
echo "   ├── implementations/   # 实现记录"
echo "   ├── config.json        # 配置文件"
echo "   ├── README.md          # 说明文档"
echo "   └── .gitignore         # Git 忽略规则"
echo ""
echo "📋 项目信息："
cat "$RPI_DIR/config.json"
echo ""
echo "💡 下一步："
echo "   1. 描述你的需求，开始 Research 阶段"
echo "   2. 或查看技能文档了解详细流程"
