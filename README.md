# 🎨 Excalidraw PPT 极简手绘演讲文稿库

本项目基于 **Excalidraw** 打造极简手绘风（Minimalist Hand-drawn Backdrop Style）的演讲幻灯片库。专为公开课、技术分享和课堂授课设计，强调**大屏视觉锚点、高对比度、大字号留白与清晰的逻辑骨架**，拒绝密密麻麻的技术长文。

---

## 🖥️ 快速上手：在 VS Code 中预览与编辑

无需复杂的幻灯片制作软件，在 VS Code 中即可获得极佳的所见即所得体验：

1. **安装插件**：
   * 在 VS Code 插件市场（Extensions）搜索并安装 **`Excalidraw`**（推荐安装 `pomdtr.excalidraw-editor` 插件）。
2. **预览与编辑**：
   * 在左侧文件树中直接点击任意 `.excalidraw` 文件（例如 `agent-skills-slides.excalidraw`）。
   * 即可直接在 VS Code 编辑器窗口中沉浸式**可视化预览、缩放、框选并手动调整元素排版**。
3. **导出课件**：
   * 画布支持一键导出为高清 PNG 或矢量 SVG 格式，方便投影大屏演示或嵌入教学课件。

---

## 📚 课件主题目录

| 主题目录 | 课件名称 | 幻灯片文件 | 包含材料 |
| :--- | :--- | :--- | :--- |
| 🤖 [`agent-skills-slides/`](./agent-skills-slides/) | **智能体技能底层原理与核心认知** | [`agent-skills-slides.excalidraw`](./agent-skills-slides/agent-skills-slides.excalidraw) | 大纲规划、Excalidraw 画布、讲师逐页授课指南 (`SPEAKER_NOTES.md`) |
| ☁️ [`workbuddy-cloud-slides/`](./workbuddy-cloud-slides/) | **WorkBuddy 云服务核心认知与实战** | [`workbuddy-cloud-slides.excalidraw`](./workbuddy-cloud-slides/workbuddy-cloud-slides.excalidraw) | 大纲规划、Excalidraw 画布、导出高清图、讲师指南 (`SPEAKER_NOTES.md`) |
| 🧠 [`ai-basics-slides/`](./ai-basics-slides/) | **大模型与提示词入门到进阶** | [`ai-basics-slides.excalidraw`](./ai-basics-slides/ai-basics-slides.excalidraw) | 大纲规划、Excalidraw 画布、导出图片 |

---

## 🛠️ 项目协作与设计规范

所有参与本项目维护的开发者与 AI 助手均需严格遵守 [AGENTS.md](./AGENTS.md) 规范：

1. **🔴 严禁全量重写**：严禁运行任何全量覆写脚本或全量替换已有人工编辑的 `.excalidraw` 文件。
2. **🔴 Backdrop 视觉留白原则**：
   * **单页文字绝对克制**：PPT 只是大屏演讲的“视觉锚点”，每页只呈现核心关键词、流程箭头与强反差对比；
   * **长文分流机制**：详细的来龙去脉、案例与台词一律写入 `SPEAKER_NOTES.md`，交给讲师现场发挥。
3. **安全局部更新**：若需程序化调整，必须先生成带时间戳的备份文件，并通过精准的 element id 定位局部 Patch。
