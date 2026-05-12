#!/bin/sh
# RPI Workflow - Research 阶段辅助脚本
# 用于并行探索代码库并生成提案

set -e

if [ $# -lt 2 ]; then
    echo "用法: $0 <项目目录> <需求描述>"
    echo "示例: $0 . '实现用户认证功能'"
    exit 1
fi

PROJECT_DIR="$1"
REQUIREMENT="$2"
RPI_DIR="$PROJECT_DIR/.rpi"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
TITLE=$(echo "$REQUIREMENT" | tr ' ' '-' | tr -cd '[:alnum:]-' | cut -c1-30)
PROPOSAL_FILE="$RPI_DIR/proposals/$TIMESTAMP-$TITLE.md"

if [ ! -d "$RPI_DIR" ]; then
    echo "❌ 错误：未找到 .rpi 目录，请先运行初始化脚本"
    exit 1
fi

echo "🔍 Research 阶段开始..."
echo "需求: $REQUIREMENT"
echo ""

# 快速代码库扫描
echo "📂 扫描代码库结构..."
CODEBASE_SUMMARY=$(mktemp)

# 统计文件类型
find "$PROJECT_DIR" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" -o -name "*.java" \) 2>/dev/null | head -100 > "$CODEBASE_SUMMARY" || true

FILE_COUNT=$(wc -l < "$CODEBASE_SUMMARY")
echo "   发现 $FILE_COUNT 个代码文件（最多显示 100 个）"

# 检测主要目录
MAIN_DIRS=$(find "$PROJECT_DIR" -maxdepth 2 -type d \( -name "src" -o -name "lib" -o -name "app" -o -name "components" -o -name "services" -o -name "models" \) 2>/dev/null | sort)

if [ -n "$MAIN_DIRS" ]; then
    echo ""
    echo "📁 主要目录："
    echo "$MAIN_DIRS" | while read -r dir; do
        echo "   - $(basename "$dir")"
    done
fi

# 生成提案模板
echo ""
echo "📝 生成提案文档..."

cat > "$PROPOSAL_FILE" <<EOF
# 提案：$REQUIREMENT

**创建时间**: $(date +"%Y-%m-%d %H:%M:%S")  
**状态**: Draft

---

## 用户需求（原始）

$REQUIREMENT

---

## 代码库概览

### 文件统计
- 代码文件数量: $FILE_COUNT
- 主要目录: $(echo "$MAIN_DIRS" | wc -l)

### 目录结构
\`\`\`
$(echo "$MAIN_DIRS" | sed 's|^|  |')
\`\`\`

---

## 约束集

### 硬约束
<!-- 技术限制、不可违反的现有模式 -->
- [ ] 待补充

### 软约束
<!-- 约定、偏好、风格指南 -->
- [ ] 待补充

### 依赖关系
<!-- 跨模块依赖，影响实现顺序 -->
- [ ] 待补充

---

## 开放问题

<!-- 需要用户澄清的模糊点 -->
1. [ ] 待补充

---

## 风险与缓解

### 风险 1
- **描述**: 待补充
- **影响**: 待补充
- **缓解策略**: 待补充

---

## 成功判据

<!-- 可验证的成功标准 -->
- [ ] 待补充

---

## 探索记录

### 探索边界 1: [待定义]
- **现有结构**: 待补充
- **现有约定**: 待补充
- **发现的约束**: 待补充

---

## 下一步

- [ ] 完成代码库深度探索
- [ ] 解决所有开放问题
- [ ] 用户确认约束集
- [ ] 进入 Plan 阶段

EOF

echo "✅ 提案文档已创建: $PROPOSAL_FILE"
echo ""
echo "📋 提案 ID: $TIMESTAMP-$TITLE"
echo ""
echo "💡 下一步："
echo "   1. 手动或通过 AI 完成提案中的待补充内容"
echo "   2. 使用多模型分析代码库（可选）"
echo "   3. 与用户交互解决开放问题"
echo "   4. 完成后进入 Plan 阶段"

# 清理临时文件
rm -f "$CODEBASE_SUMMARY"
