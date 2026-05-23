---
name: wiki-onboarding
description: Guide users through first-time Wiki initialization and verification.
---

# Wiki Onboarding Skill

## Trigger

用户说以下任意一句时触发：
- "初始化 wiki"
- "setup wiki"
- "wiki 首次配置"
- "开始用 wiki"
- "帮我配置知识库"
- "quick start"
- 新会话首次提到 wiki 且未初始化过

## Goal

引导用户完成 Personal Knowledge Base 的首次初始化和验证，确保：
1. 环境就绪（git、python、runtime 脚本）
2. 本地私有配置已创建（USER.md、taxonomy.yaml）
3. Wiki 核心目录结构完整
4. 基础测试通过（Context Pack、Graph Insights、语法检查）
5. 首次导入测试可选完成

## Precondition

执行前必须先读取：
1. `AGENTS.md` — 操作规则和 Skill 路由
2. `QUICK_START.md` 或 `QUICK_START.zh-CN.md` — 快速上手指南
3. `wiki/1_Index/master_index.md` — 当前索引状态
4. `wiki/log.md` — 已有操作记录

若 `USER.md` 已存在且非模板状态，跳过用户引导填写步骤。

## Execution

### Step 1: 环境检查

执行以下检查，**先调用工具，后汇报结果**：

```bash
git --version
python3 --version
test -f AGENTS.md && echo "AGENTS.md OK"
test -f wiki/1_Index/master_index.md && echo "master_index.md OK"
python3 wiki/4_Tools/runtime/search/kb_context_pack.py "agent workflow" --top 3
python3 wiki/4_Tools/runtime/graph/kb_graph_insights.py
python3 -c "import ast, pathlib; [ast.parse(pathlib.Path(p).read_text()) for p in ['wiki/4_Tools/runtime/search/kb_context_pack.py','wiki/4_Tools/runtime/graph/kb_graph_insights.py']]; print('syntax ok')"
```

预期结果：git 和 python3 正常、AGENTS.md 存在、master_index.md 存在、Context Pack 返回结果、Graph Insights 返回节点统计、syntax ok。

如有失败，先修环境问题，再往下走。

### Step 2: 初始化本地私有配置

检查并初始化：

- 若 `USER.md` 不存在或仍是模板状态（Role 为空），执行：
  ```bash
  cp config/user_profile.example.md USER.md
  ```
  然后**通过对话引导用户填写 USER.md**，至少确认：角色/方向、技术栈、关心的话题、输出风格偏好、协作偏好。

- 若 `config/taxonomy.yaml` 不存在，执行：
  ```bash
  cp config/taxonomy.example.yaml config/taxonomy.yaml
  ```

### Step 3: 目录结构确认

确认以下目录存在（不存在则创建）：

```
wiki/0_Raw/inbox/
wiki/0_Raw/archive/
wiki/0_Raw/attachments/
wiki/0_Raw/queues/
wiki/0_Raw/reviews/
wiki/1_Index/
wiki/2_Concepts/
wiki/3_Synthesis/
wiki/4_Tools/
```

### Step 4: 更新日志

在 `wiki/log.md` 顶部追加：

```markdown
## [YYYY-MM-DD] onboarding | Wiki initialization completed
- Status: env OK, config initialized, structure verified
- Touched: USER.md, config/taxonomy.yaml, wiki/log.md
```

### Step 5: 用户确认与下一步

向用户汇报初始化结果，包括：
- 环境状态
- 已创建/确认的配置文件
- 当前 wiki 中的概念卡数量

然后问用户下一步：
1. 开始第一次真实摄入（放资料到 inbox 然后处理）
2. 先调整分类体系（taxonomy.yaml）
3. 查看现有概念卡和索引

## Constraints

- **不要跳过环境检查**。如果 runtime 脚本报错，先排查再往下。
- **不要覆盖已有的 USER.md**。若已存在且已填写，只确认不覆盖。
- **不要凭空编造用户信息**。引导用户亲口确认或填写。
- **每次执行后必须更新 wiki/log.md**。
- **用 todo_write 追踪多步骤进度**，让用户实时看到进行到哪一步。

## Output Format

最终汇报格式：

```
Wiki 初始化完成 ✅

环境: git x.x.x, python x.x.x, runtime OK
配置: USER.md [已填写/待填写], taxonomy.yaml [已激活]
结构: N 个概念卡, 索引已更新
日志: wiki/log.md 已记录

下一步建议：[根据用户画像给 1-2 个选项]
```

## Postcondition

- 环境检查全部通过
- `USER.md` 已创建或已确认（非模板状态）
- `config/taxonomy.yaml` 已存在
- Wiki 目录结构完整
- `wiki/log.md` 已追加 onboarding 记录
- 用户已收到初始化结果汇报和下一步选项
