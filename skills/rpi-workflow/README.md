# RPI Workflow

Research-Plan-Implementation 工作流技能，用于复杂项目的结构化开发。

## 文件说明

- `SKILL.md` - 完整技能文档（16KB，核心理念 + 详细流程）
- `QUICKREF.md` - 快速参考卡片（9KB，命令速查 + 检查清单）
- `EXAMPLES.md` - 使用示例（11KB，3 个完整案例）
- `init.sh` - 项目初始化脚本
- `research.sh` - Research 阶段辅助脚本
- `plan.sh` - Plan 阶段辅助脚本
- `implementation.sh` - Implementation 阶段辅助脚本

## 快速开始

```bash
# 1. 初始化项目
/var/minis/skills/rpi-workflow/init.sh <项目目录>

# 2. 开始 Research
/var/minis/skills/rpi-workflow/research.sh <项目目录> "<需求描述>"

# 3. 进入 Plan（清空上下文后）
/var/minis/skills/rpi-workflow/plan.sh <项目目录> <提案ID>

# 4. 执行 Implementation（清空上下文后）
/var/minis/skills/rpi-workflow/implementation.sh <项目目录> <计划ID>
```

## 核心理念

1. **上下文专注**：每阶段清空上下文，保持 ≤ 80K tokens
2. **约束驱动**：Research 生成约束集，而非信息堆砌
3. **零决策执行**：Plan 消除所有决策点，Implementation 纯机械执行
4. **多模型协作**：利用不同模型优势，交叉审查发现盲点

## 适用场景

- ✅ 复杂、长期的开发任务
- ✅ 需求模糊，需要深度分析
- ✅ 多模块、多依赖的项目
- ✅ 对代码质量要求高的场景
- ❌ 简单、快速的一次性任务

## 目录结构

项目初始化后会创建 `.rpi/` 目录：

```
.rpi/
├── proposals/          # 需求提案（Research 输出）
├── constraints/        # 约束集（可选）
├── plans/             # 执行计划（Plan 输出）
├── implementations/   # 实现记录（Implementation 输出）
├── config.json        # 项目配置
├── README.md          # 说明文档
└── .gitignore         # Git 忽略规则
```

## 版本

- **版本**: 1.0.0
- **创建时间**: 2026-04-19
- **基于**: GuDaStudio/commands (https://github.com/GuDaStudio/commands)
- **适配**: Minis iOS

## 许可

MIT License - 基于原项目 GuDaStudio/commands
