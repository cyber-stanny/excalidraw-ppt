# Excalidraw PPT 项目协作与修改规范

本项目包含人类用户在 Excalidraw 画布上的手动排版、文字修改以及 AI 助手的辅助支持。为了彻底杜绝任何形式的数据丢失与手动修改被冲掉的问题，所有参与本项目的 AI 助手必须严格遵守以下规范。

---

## 核心红线原则

### 🔴 严禁全量重写 / 严禁运行全量生成脚本
- **严禁**运行任何全量生成/覆写脚本（如 `generate_full_slides.py` 等）。
- **严禁**使用 `write_file(Overwrite=True)` 或类似全量覆写工具直接替换 `.excalidraw` 文件。
- 一旦用户已经在画布上手动编辑、保存过内容，该文件即成为**不可被程序全量覆盖的生产主干**。

### 🔴 严禁页面文字过密 / 必须保持极简大屏视觉（Backdrop 原则）
- **单页文字绝对克制**：严禁密密麻麻堆砌大段长句。PPT 是大屏演讲的“视觉锚点”，不是教材或白皮书。
- **突出要点与逻辑骨架**：每页只呈现核心关键词、流程箭头与强反差对比，字号大、留白足、呼吸感强。
- **内容合理分流**：详细的台词、原理解释、生活案例一律移至 `SPEAKER_NOTES.md`，交给讲解人现场发挥。
- **制作前强制审查**：后续在写大纲和生成/修改任何 PPT 前，AI 必须首先 review 本条原则，自检页面信息密度。

---

## 标准修改规范

### 1. 修改权限归属
- **排版、字号微调、内容表达**：以用户在 Excalidraw 画布中的直接编辑为最高优先级。
- **AI 助手角色**：仅在用户明确提出“请帮我批量修改某项”时介入。

### 2. 精准局部修改机制（Selective Patching Only）
若用户明确要求 AI 修改某个特定文本或属性：
1. **自动备份**：在执行任何修改前，必须先自动生成带时间戳的备份文件，例如：
   ```bash
   cp ai-basics-slides.excalidraw ai-basics-slides.excalidraw.bak
   ```
2. **只读解析 + 局部更新**：读取现有的 `.excalidraw` JSON 文件，**仅且只能修改**目标元素（通过特定 `id` 定位），保留所有其余 100% 的元素属性、位置坐标和用户手动新增的对象。
3. **安全写回**：只写回更新后的 JSON，不丢弃任何未知字段或用户新增字段。

### 3. 生成脚本生命周期
- 任何用于从 0 到 1 快速搭建骨架的 Python/JS 脚本，在骨架搭建完成后即归档为只读模板/历史工具，不得再次对活跃中的工作文件运行覆写。

---

## 飞书在线教学文档联动与精准更新规范（Lark-CLI 工作流）

当用户要求将课件资产、截图或复盘内容同步/更新到飞书在线教学文档（Wiki / Docx）时，必须严格遵守以下规范：

### 1. 工具与环境保障
- 本机已配置并授权官方工具 **`lark-cli`**，支持直接调用飞书开放平台 OpenAPI。
- 非交互式执行环境下，若未识别到命令，可动态载入用户环境下的 Node/nvm bin 路径：
  ```bash
  export PATH="$(find $HOME/.nvm/versions/node -maxdepth 2 -name bin 2>/dev/null | tail -n 1):$PATH"
  ```

### 2. 核心红线：严禁破坏既有内容（零越权修改）
- **严禁全量覆写**：绝对禁止对飞书文档使用 `overwrite`，严禁改动任何未被明确授权的已有章节。
- **只动标记区**：仅且只能修改用户明确标记了 `【TODO】` 或明确指定的单点 block。

### 3. 标准化 5 步精准更新工作流
1. **解析节点**：若用户提供的是 Wiki 链接，先执行 `lark-cli wiki +node-get --node-token <token>` 获取底层的 `obj_token`（docx 类型）。
2. **定位目标 Block**：使用 `lark-cli docs +fetch --doc <token> --detail with-ids`（可配合 `--scope keyword --keyword "TODO"`），获取目标段落专属的唯一 `id`（如 `id="FkZbdrj..."`）。
3. **载荷编写（XML 优先）**：
   - 优先采用 XML 格式，富文本及高亮块表达力更强；
   - 插入本地图片直接使用 `<img path="@path/to/image.png" caption="..."/>`，CLI 会自动调度 Drive 接口完成上传与块绑定；
   - 临时 XML 文件必须保存在当前工作目录或 `/tmp/` 目录下（受 CLI 安全白名单限制）。
4. **Dry-Run 校验与精准替换**：
   - 复杂更新先追加 `--dry-run` 预览 API 调用链；
   - 执行局部单块替换：
     ```bash
     lark-cli docs +update --doc <token> --command block_replace --block-id <target_id> --content '@/tmp/blocks.xml'
     ```
5. **分步更新与 Fetch 验证（Verify）**：
   - 若文档中存在多个待处理的 TODO，**严禁使用同一轮 fetch 出的旧 ID 连续替换**；
   - 必须每修改一处后重新 fetch 文档，确认生效并刷新剩余 TODO 的最新 block ID，再进行下一处修改。

