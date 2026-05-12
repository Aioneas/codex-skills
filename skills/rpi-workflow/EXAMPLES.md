# RPI Workflow 示例

本目录包含 RPI 工作流的完整使用示例。

## 示例 1：天气展示页面

完整演示 Research → Plan → Implementation 三阶段流程。

### 用户需求

```
我需要生成一个美观的实时天气展示页面。要求：
1. 实时天气信息必须为真实信息，包含温度、湿度等
2. 用户可以选择北京、上海、深圳三个城市
3. 四种不同的基础天气（大风、降雨、晴天、下雪），有不同的页面展示
4. UI 设计极具美感，参考苹果公司的顶级前端设计
```

### 阶段 0：初始化

```bash
# 在项目目录下运行
/var/minis/skills/rpi-workflow/init.sh .

# 输出：
# ✅ RPI 工作流初始化完成！
# 📁 目录结构：
#    ./.rpi/
#    ├── proposals/
#    ├── plans/
#    ├── implementations/
#    └── config.json
```

### 阶段 1：Research

```bash
# 生成提案模板
/var/minis/skills/rpi-workflow/research.sh . "美观的实时天气展示页面"

# 输出：
# ✅ 提案文档已创建: ./.rpi/proposals/20260419-100000-weather-page.md
# 📋 提案 ID: 20260419-100000-weather-page
```

**AI 工作流程**：
1. 扫描代码库（若有）
2. 识别约束：
   - 硬约束：需要天气 API（OpenWeatherMap/和风天气）
   - 软约束：苹果风格 UI（简洁、毛玻璃、动画流畅）
3. 提出开放问题：
   - Q1: 使用哪个天气 API？
   - Q2: 是否需要响应式设计？
   - Q3: 是否需要天气动画效果？
4. 用户回答后更新提案
5. 生成成功判据

**提案文档示例**：见 `examples/weather-page/proposal.md`

**建议**：完成后清空上下文，进入 Plan 阶段。

---

### 阶段 2：Plan

```bash
# 生成执行计划模板
/var/minis/skills/rpi-workflow/plan.sh . 20260419-100000-weather-page

# 输出：
# ✅ 执行计划已创建: ./.rpi/plans/20260419-101000-20260419-100000-weather-page.md
# 📋 计划 ID: 20260419-101000-20260419-100000-weather-page
```

**AI 工作流程**：
1. 加载提案
2. 多模型分析：
   - 使用 GPT-4 检测模糊性
   - 使用 Claude 检测隐含假设
3. 用户交互解决模糊性：
   - Q: 天气图标使用自定义 SVG 还是图标库？
   - A: 使用 Iconify 图标库
4. 技术决策：
   - 前端：React + TailwindCSS + Framer Motion
   - API：和风天气 API v7
   - 图标：Iconify (mdi:weather-*)
5. 生成任务流（7 个任务，顺序执行）
6. 提取 PBT 属性（2 个属性）

**计划文档示例**：见 `examples/weather-page/plan.md`

**建议**：完成后清空上下文，进入 Implementation 阶段。

---

### 阶段 3：Implementation

```bash
# 生成实现记录模板
/var/minis/skills/rpi-workflow/implementation.sh . 20260419-101000-20260419-100000-weather-page

# 输出：
# ✅ 实现记录已创建: ./.rpi/implementations/20260419-103000-20260419-101000-20260419-100000-weather-page.md
# 📋 实现记录 ID: 20260419-103000-20260419-101000-20260419-100000-weather-page
```

**AI 工作流程**：
1. 加载计划
2. 执行任务 1：创建 React 项目结构
   - 使用 Gemini 生成原型
   - 重写为简洁结构
   - GPT-4 审查：LGTM
   - Claude 审查：LGTM
3. 执行任务 2：实现天气 API 调用模块
   - 使用 Claude 生成原型
   - 重写为生产代码
   - GPT-4 审查：建议添加缓存
   - 修改后再审查：LGTM
4. [继续执行剩余任务...]
5. 上下文监控：当前 65K，可继续
6. 所有任务完成

**实现记录示例**：见 `examples/weather-page/implementation.md`

---

## 示例 2：用户认证系统

演示复杂后端逻辑的 RPI 流程，包含 PBT 属性定义。

### 用户需求

```
实现一个安全的用户认证系统，支持：
1. 用户注册（邮箱验证）
2. 用户登录（JWT token）
3. 密码重置
4. 多设备登录管理
5. 登录失败锁定机制
```

### Research 阶段要点

**约束集**：
- 硬约束：
  - 必须使用 bcrypt 加密密码
  - JWT token 必须有过期时间
  - 邮箱验证必须有时效性
- 软约束：
  - 遵循 OWASP 安全最佳实践
  - 日志记录所有认证事件

**开放问题**：
- Q1: JWT accessToken 和 refreshToken 的 TTL？
  - A: accessToken 15分钟，refreshToken 7天
- Q2: 登录失败多少次后锁定？锁定多久？
  - A: 5次失败后锁定30分钟
- Q3: 是否支持第三方登录（OAuth）？
  - A: 暂不支持，未来可扩展

### Plan 阶段要点

**技术决策**：
- 语言：Python 3.11
- 框架：FastAPI
- 数据库：PostgreSQL + SQLAlchemy
- 缓存：Redis（存储 token 黑名单和登录尝试计数）
- 加密：bcrypt (cost factor=12)
- JWT：PyJWT，HS256 算法

**任务流**（10 个任务）：
1. 设计数据库模型（User, LoginAttempt, RefreshToken）
2. 实现密码加密/验证模块
3. 实现 JWT 生成/验证模块
4. 实现用户注册接口（含邮箱验证）
5. 实现用户登录接口（含失败锁定）
6. 实现 token 刷新接口
7. 实现密码重置接口
8. 实现多设备登录管理
9. 实现登录日志记录
10. 编写单元测试和集成测试

**PBT 属性**：
1. **密码加密幂等性**
   - 不变量：`verify(hash(password), password) == True`
   - 证伪策略：生成随机密码，验证往返
2. **JWT 往返一致性**
   - 不变量：`decode(encode(payload)) == payload`
   - 证伪策略：生成随机 payload，验证往返
3. **登录失败计数单调性**
   - 不变量：失败次数只增不减，直到成功登录或超时重置
   - 证伪策略：模拟并发登录失败，验证计数正确
4. **Token 过期时间单调性**
   - 不变量：token 的 `exp` 字段总是大于 `iat` 字段
   - 证伪策略：生成大量 token，验证时间戳顺序

### Implementation 阶段要点

**多模型协作**：
- 任务 1-3（核心逻辑）：使用 Claude 生成原型
- 任务 4-8（API 接口）：使用 GPT-4 生成原型
- 任务 9-10（测试）：使用 Claude 生成原型

**代码审查**：
- 每个任务完成后，GPT-4 和 Claude 交叉审查
- 重点检查：安全漏洞、边界条件、并发问题

**上下文管理**：
- 任务 1-5 完成后（约 70K），清空上下文
- 任务 6-10 在新上下文中继续

---

## 示例 3：数据分析管道

演示数据处理任务的 RPI 流程。

### 用户需求

```
构建一个数据分析管道，处理用户行为日志：
1. 从 S3 读取原始日志（JSON 格式）
2. 清洗数据（去重、填充缺失值、异常值处理）
3. 特征工程（提取时间特征、用户画像）
4. 生成分析报告（用户活跃度、留存率、转化漏斗）
5. 结果写入 PostgreSQL 和导出 CSV
```

### Research 阶段要点

**约束集**：
- 硬约束：
  - 日志量级：每天 1000 万条
  - 处理时效：必须在 1 小时内完成
  - 内存限制：单机 16GB
- 软约束：
  - 优先使用 Pandas/Polars
  - 代码可读性优先于性能（除非性能瓶颈）

**开放问题**：
- Q1: 使用 Pandas 还是 Polars？
  - A: Polars（更快，内存效率高）
- Q2: 是否需要增量处理？
  - A: 是，只处理新增日志
- Q3: 异常值处理策略？
  - A: 使用 IQR 方法，超出 3 倍 IQR 视为异常

### Plan 阶段要点

**技术决策**：
- 语言：Python 3.11
- 数据处理：Polars
- 存储：PostgreSQL + psycopg3
- 任务调度：Airflow（未来）

**任务流**（8 个任务）：
1. 实现 S3 读取模块（支持增量）
2. 实现数据清洗模块（去重、填充、异常值）
3. 实现特征工程模块（时间特征、用户画像）
4. 实现用户活跃度分析
5. 实现留存率分析
6. 实现转化漏斗分析
7. 实现 PostgreSQL 写入模块
8. 实现 CSV 导出模块

**PBT 属性**：
1. **数据去重幂等性**
   - 不变量：`deduplicate(deduplicate(data)) == deduplicate(data)`
   - 证伪策略：生成含重复的数据，验证多次去重结果一致
2. **特征工程可逆性**
   - 不变量：某些特征可从原始数据重新计算得到相同结果
   - 证伪策略：保存原始数据，重新计算特征，验证一致性
3. **聚合结果单调性**
   - 不变量：用户活跃度总数 = 各渠道活跃度之和
   - 证伪策略：分别计算总数和分组和，验证相等

---

## 使用技巧

### 1. 上下文管理

**监控上下文**：
```python
# 在 AI 响应中定期提示
当前上下文使用量：约 65K / 80K
建议：可继续当前任务
```

**清空时机**：
- Research 完成后
- Plan 完成后
- Implementation 中每完成 3-5 个任务后（视复杂度）

### 2. 多模型选择

**前端/UI 任务**：
- 优先：Gemini（创意强）
- 备选：GPT-4（逻辑清晰）

**后端/逻辑任务**：
- 优先：Claude（代码质量高）
- 备选：GPT-4（通用性强）

**审查任务**：
- 必须：至少两个不同模型交叉审查
- 推荐：GPT-4 + Claude

### 3. 约束集提取

**好的约束**（缩小解决方案空间）：
- ✅ "必须使用 JWT，accessToken TTL=15min"
- ✅ "5 次登录失败后锁定 30 分钟"
- ✅ "密码必须使用 bcrypt，cost factor=12"

**坏的约束**（信息堆砌）：
- ❌ "可以使用 JWT 或 session"
- ❌ "登录失败后可能需要锁定"
- ❌ "密码需要加密"

### 4. PBT 属性定义

**关注不变量**，而非具体测试用例：
- ✅ "往返一致性：encode(decode(x)) == x"
- ✅ "幂等性：f(f(x)) == f(x)"
- ❌ "测试用例 1：输入 'test'，输出 'TEST'"

### 5. 任务粒度

**合适的粒度**：
- 单个任务 1-2 小时完成
- 输入输出明确
- 可独立验证

**过粗**：
- ❌ "实现整个认证系统"

**过细**：
- ❌ "定义 User 模型的 email 字段"

**合适**：
- ✅ "实现用户登录接口（含失败锁定）"

---

## 常见问题

### Q1: 必须严格遵循三阶段吗？

**A**: 对于复杂任务，强烈建议遵循。简单任务可以跳过 Research，直接 Plan + Implementation。

### Q2: 可以在 Implementation 阶段修改 Plan 吗？

**A**: 可以，但应记录原因。如果发现 Plan 有重大缺陷，建议回到 Plan 阶段重新细化。

### Q3: 多模型调用成本高怎么办？

**A**: 
- Research 阶段：可选，复杂项目才需要
- Plan 阶段：必须，但只需 2-3 次调用
- Implementation 阶段：每个任务 2-3 次（原型 + 审查）

### Q4: 如何处理紧急需求变更？

**A**: 
1. 评估影响范围
2. 若影响 Plan，回到 Plan 阶段更新
3. 若仅影响单个任务，直接在 Implementation 中调整并记录

### Q5: .rpi/ 目录应该提交到 Git 吗？

**A**: 
- 提交：proposals/, plans/（团队协作需要）
- 可选：implementations/（可作为开发日志）
- 忽略：临时文件、敏感信息

---

## 参考资源

- 技能文档：`/var/minis/skills/rpi-workflow/SKILL.md`
- 原始项目：https://github.com/GuDaStudio/commands
- Property-Based Testing：https://hypothesis.works/
- 多模型配置：`minis-model-use list`
