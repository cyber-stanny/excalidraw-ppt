#!/usr/bin/env python3
"""
Generate complete 6-page Lecture Backdrop PPT in Excalidraw format.
Design Philosophy:
- "Backdrop Style" for speaker presentation: High-impact keywords, clean hierarchy, no walls of text.
- Large fonts (36~64px+ for key concepts) so students in the back row can easily read.
- Hand-drawn minimalist aesthetic (Excalifont fontFamily=5, roughness=1, elegant muted palette).
- Proper Excalidraw container binding with exact vertical & horizontal text centering.
"""

import json

seed_counter = [20000]

def ns():
    seed_counter[0] += 1
    return seed_counter[0]

def frame(id, x, y, w, h, name):
    return {
        "id": id, "type": "frame",
        "x": x, "y": y, "width": w, "height": h,
        "strokeColor": "#D0D7DE", "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "boundElements": [],
        "updated": 0, "link": None, "locked": False,
        "name": name
    }

def rect(id, x, y, w, h, stroke="#1E1E1E", bg="transparent",
         frame_id=None, rounded=True, roughness=1, stroke_width=2,
         bound_text_id=None):
    el = {
        "id": id, "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": "solid", "strokeWidth": stroke_width,
        "strokeStyle": "solid", "roughness": roughness,
        "opacity": 100, "angle": 0,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False,
        "boundElements": [{"id": bound_text_id, "type": "text"}] if bound_text_id else [],
        "updated": 0, "link": None, "locked": False,
    }
    if rounded:
        el["roundness"] = {"type": 3}
    if frame_id:
        el["frameId"] = frame_id
    return el

def text(id, x, y, w, h, content, font_size=24, color="#1E1E1E",
         align="left", frame_id=None, container_id=None):
    el = {
        "id": id, "type": "text",
        "x": x, "y": y, "width": w, "height": h,
        "text": content, "fontSize": font_size, "fontFamily": 5,
        "textAlign": align, "verticalAlign": "middle",
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "boundElements": None,
        "updated": 0, "link": None, "locked": False,
        "containerId": container_id, "originalText": content, "lineHeight": 1.25,
    }
    if frame_id:
        el["frameId"] = frame_id
    return el

def line_el(id, x, y, dx, dy, color="#DEE2E6", width=2, frame_id=None, roughness=1):
    el = {
        "id": id, "type": "line",
        "x": x, "y": y, "width": abs(dx) if dx else 0, "height": abs(dy) if dy else 0,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": width, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "angle": 0,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "boundElements": None,
        "updated": 0, "link": None, "locked": False,
        "points": [[0, 0], [dx, dy]],
    }
    if frame_id:
        el["frameId"] = frame_id
    return el

def arrow_el(id, x, y, dx, dy, color="#495057", width=3, frame_id=None, roughness=1):
    el = {
        "id": id, "type": "arrow",
        "x": x, "y": y, "width": abs(dx) if dx else 0, "height": abs(dy) if dy else 0,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": width, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "angle": 0,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "boundElements": None,
        "updated": 0, "link": None, "locked": False,
        "points": [[0, 0], [dx, dy]],
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow",
    }
    if frame_id:
        el["frameId"] = frame_id
    return el

def make_card_with_text(prefix, x, y, w, h, content, font_size=32,
                        bg="#F8F9FA", stroke="#1E1E1E", text_color="#1E1E1E",
                        frame_id=None, stroke_width=2, roughness=1):
    """Create a box with perfectly bound and centered text."""
    rect_id = prefix
    txt_id = prefix + "_t"
    th = int(font_size * 1.3)
    ty = y + (h - th) // 2
    return [
        rect(rect_id, x, y, w, h, stroke=stroke, bg=bg,
             frame_id=frame_id, rounded=True, roughness=roughness,
             stroke_width=stroke_width, bound_text_id=txt_id),
        text(txt_id, x + 10, ty, w - 20, th, content,
             font_size=font_size, color=text_color, align="center",
             frame_id=frame_id, container_id=rect_id)
    ]

# Global element collector
elements = []

def add_slide_header(frame_id, yo, category, title, page_no):
    """Standard lecture backdrop header with large prominent titles."""
    # Category / Tag
    elements.append(text(f"{frame_id}_cat", 100, yo + 45, 600, 30,
                         category, font_size=22, color="#7048E8", align="left", frame_id=frame_id))
    # Big Main Title
    elements.append(text(f"{frame_id}_title", 100, yo + 80, 1400, 75,
                         title, font_size=58, color="#111827", align="left", frame_id=frame_id))
    # Subtle divider
    elements.append(line_el(f"{frame_id}_div", 100, yo + 165, 1400, 0,
                            color="#E9ECEF", width=2, frame_id=frame_id, roughness=1))
    # Page Indicator
    elements.append(text(f"{frame_id}_page", 1460, yo + 840, 60, 30,
                         f"0{page_no}" if page_no < 10 else str(page_no),
                         font_size=18, color="#ADB5BD", align="right", frame_id=frame_id))


# ==============================================================================
# SLIDE 1: 认识 LLM：从名字到本质
# ==============================================================================
f1 = "frame_1"
y1 = 0
elements.append(frame(f1, 0, y1, 1600, 900, "01 · 认识 LLM"))
add_slide_header(f1, y1, "PART 01 · 揭开面纱", "LLM：大型语言模型", 1)

# Full name banner
elements.extend(make_card_with_text("s1_fullname", 100, y1 + 190, 1400, 76,
                                    "Large Language Model", font_size=36,
                                    bg="#F3F0FF", stroke="#7048E8", text_color="#5F3DC4",
                                    frame_id=f1, stroke_width=2))

# Left Card: 国内主流
elements.append(rect("s1_box_l", 100, y1 + 290, 685, 290,
                     stroke="#1971C2", bg="#F8F9FA", frame_id=f1, stroke_width=2))
elements.append(text("s1_lbl_l", 140, y1 + 315, 300, 36,
                     "🇨🇳  国内主流", font_size=28, color="#1971C2", frame_id=f1))

cn_models = [
    ("DeepSeek", "#2B8A3E", "#EBFBEE"),
    ("Qwen (通义千问)", "#D9480F", "#FFE8CC"),
    ("Kimi", "#5F3DC4", "#F3F0FF"),
    ("GLM (智谱清言)", "#1864AB", "#E7F5FF"),
    ("MiniMax", "#C92A2A", "#FFF5F5")
]
# Row 1 (2 tags)
elements.extend(make_card_with_text("s1_cn_0", 140, y1 + 375, 280, 70, cn_models[0][0],
                                    font_size=26, bg=cn_models[0][2], stroke=cn_models[0][1],
                                    text_color=cn_models[0][1], frame_id=f1))
elements.extend(make_card_with_text("s1_cn_1", 440, y1 + 375, 305, 70, cn_models[1][0],
                                    font_size=24, bg=cn_models[1][2], stroke=cn_models[1][1],
                                    text_color=cn_models[1][1], frame_id=f1))
# Row 2 (3 tags)
elements.extend(make_card_with_text("s1_cn_2", 140, y1 + 470, 180, 70, cn_models[2][0],
                                    font_size=26, bg=cn_models[2][2], stroke=cn_models[2][1],
                                    text_color=cn_models[2][1], frame_id=f1))
elements.extend(make_card_with_text("s1_cn_3", 340, y1 + 470, 245, 70, cn_models[3][0],
                                    font_size=24, bg=cn_models[3][2], stroke=cn_models[3][1],
                                    text_color=cn_models[3][1], frame_id=f1))
elements.extend(make_card_with_text("s1_cn_4", 605, y1 + 470, 140, 70, cn_models[4][0],
                                    font_size=24, bg=cn_models[4][2], stroke=cn_models[4][1],
                                    text_color=cn_models[4][1], frame_id=f1))

# Right Card: 国外主流
elements.append(rect("s1_box_r", 815, y1 + 290, 685, 290,
                     stroke="#495057", bg="#F8F9FA", frame_id=f1, stroke_width=2))
elements.append(text("s1_lbl_r", 855, y1 + 315, 300, 36,
                     "🌍  国外主流", font_size=28, color="#495057", frame_id=f1))

global_models = [
    ("Claude", "#D9480F", "#FFE8CC"),
    ("ChatGPT (GPT)", "#2B8A3E", "#EBFBEE"),
    ("Gemini", "#1864AB", "#E7F5FF"),
    ("Grok", "#343A40", "#F1F3F5")
]
# Row 1
elements.extend(make_card_with_text("s1_gl_0", 855, y1 + 375, 290, 70, global_models[0][0],
                                    font_size=28, bg=global_models[0][2], stroke=global_models[0][1],
                                    text_color=global_models[0][1], frame_id=f1))
elements.extend(make_card_with_text("s1_gl_1", 1165, y1 + 375, 300, 70, global_models[1][0],
                                    font_size=26, bg=global_models[1][2], stroke=global_models[1][1],
                                    text_color=global_models[1][1], frame_id=f1))
# Row 2
elements.extend(make_card_with_text("s1_gl_2", 855, y1 + 470, 290, 70, global_models[2][0],
                                    font_size=28, bg=global_models[2][2], stroke=global_models[2][1],
                                    text_color=global_models[2][1], frame_id=f1))
elements.extend(make_card_with_text("s1_gl_3", 1165, y1 + 470, 300, 70, global_models[3][0],
                                    font_size=28, bg=global_models[3][2], stroke=global_models[3][1],
                                    text_color=global_models[3][1], frame_id=f1))

# Bottom Core Takeaway: 本质
elements.append(rect("s1_bottom_rect", 100, y1 + 610, 1400, 190,
                     stroke="#D9480F", bg="#FFF4E6", frame_id=f1, stroke_width=2.5))
elements.append(text("s1_bot_tag", 140, y1 + 630, 200, 30,
                     "⚡️ 核心本质", font_size=22, color="#D9480F", frame_id=f1))
elements.append(text("s1_bot_core", 140, y1 + 675, 1320, 65,
                     "它不是百科全书，本质是「预测下一个 Token」",
                     font_size=42, color="#D9480F", frame_id=f1))
elements.append(text("s1_bot_sub", 140, y1 + 745, 1320, 35,
                     "输入前面的文字 → 概率计算 → 吐出最可能接上的下一个词",
                     font_size=22, color="#495057", frame_id=f1))


# ==============================================================================
# SLIDE 2: 什么是 Token？（AI 眼中的世界）
# ==============================================================================
f2 = "frame_2"
y2 = 1100
elements.append(frame(f2, 0, y2, 1600, 900, "02 · 什么是 Token"))
add_slide_header(f2, y2, "PART 01 · 揭开面纱", "什么是 Token？", 2)

# Central Visual Concept: 人类眼中的词 vs AI 眼中的 Token
elements.extend(make_card_with_text("s2_raw_box", 100, y2 + 200, 420, 100,
                                    "“我喜欢编程”", font_size=40,
                                    bg="#F8F9FA", stroke="#495057", text_color="#212529",
                                    frame_id=f2, stroke_width=2))

elements.append(arrow_el("s2_split_arr", 545, y2 + 250, 100, 0,
                         color="#7048E8", width=4, frame_id=f2))
elements.append(text("s2_split_lbl", 555, y2 + 205, 80, 30,
                     "分词 (Tokenizer)", font_size=18, color="#7048E8", align="center", frame_id=f2))

# Tokens as colorful distinct units
elements.extend(make_card_with_text("s2_tk_1", 670, y2 + 200, 140, 100,
                                    "[ 我 ]", font_size=36,
                                    bg="#EBFBEE", stroke="#2B8A3E", text_color="#2B8A3E",
                                    frame_id=f2, stroke_width=2.5))
elements.extend(make_card_with_text("s2_tk_2", 830, y2 + 200, 180, 100,
                                    "[ 喜欢 ]", font_size=36,
                                    bg="#E7F5FF", stroke="#1864AB", text_color="#1864AB",
                                    frame_id=f2, stroke_width=2.5))
elements.extend(make_card_with_text("s2_tk_3", 1030, y2 + 200, 180, 100,
                                    "[ 编程 ]", font_size=36,
                                    bg="#FFF4E6", stroke="#D9480F", text_color="#D9480F",
                                    frame_id=f2, stroke_width=2.5))
elements.extend(make_card_with_text("s2_tk_sum", 1230, y2 + 200, 270, 100,
                                    "= 3 Tokens", font_size=34,
                                    bg="#F3F0FF", stroke="#7048E8", text_color="#5F3DC4",
                                    frame_id=f2, stroke_width=2))

# 3 Big Keyword Pillars across bottom
col_w = 445
col_gap = 32

# Pillar 1: 计费单位
x_p1 = 100
elements.append(rect("s2_p1", x_p1, y2 + 340, col_w, 460,
                     stroke="#2B8A3E", bg="#F8F9FA", frame_id=f2, stroke_width=2))
elements.extend(make_card_with_text("s2_p1_h", x_p1 + 25, y2 + 370, col_w - 50, 70,
                                    "💰  计费单位", font_size=32,
                                    bg="#EBFBEE", stroke="#2B8A3E", text_color="#2B8A3E",
                                    frame_id=f2))
elements.append(text("s2_p1_t1", x_p1 + 35, y2 + 480, col_w - 70, 60,
                     "输入 Token 计费", font_size=28, color="#111827", frame_id=f2))
elements.append(text("s2_p1_t2", x_p1 + 35, y2 + 550, col_w - 70, 60,
                     "输出 Token 计费", font_size=28, color="#111827", frame_id=f2))
elements.append(text("s2_p1_t3", x_p1 + 35, y2 + 630, col_w - 70, 120,
                     "按千/百万 Token 算钱\n（生成往往比输入更贵）", font_size=22, color="#495057", frame_id=f2))

# Pillar 2: 记忆极限
x_p2 = x_p1 + col_w + col_gap
elements.append(rect("s2_p2", x_p2, y2 + 340, col_w, 460,
                     stroke="#1864AB", bg="#F8F9FA", frame_id=f2, stroke_width=2))
elements.extend(make_card_with_text("s2_p2_h", x_p2 + 25, y2 + 370, col_w - 50, 70,
                                    "🧠  记忆上限", font_size=32,
                                    bg="#E7F5FF", stroke="#1864AB", text_color="#1864AB",
                                    frame_id=f2))
elements.append(text("s2_p2_t1", x_p2 + 35, y2 + 480, col_w - 70, 60,
                     "上下文窗口限制", font_size=28, color="#111827", frame_id=f2))
elements.append(text("s2_p2_t2", x_p2 + 35, y2 + 550, col_w - 70, 60,
                     "Context Window", font_size=26, color="#495057", frame_id=f2))
elements.append(text("s2_p2_t3", x_p2 + 35, y2 + 630, col_w - 70, 120,
                     "超出长度便会遗忘\n（4K · 32K · 128K · 1M）", font_size=22, color="#495057", frame_id=f2))

# Pillar 3: 中英文差异
x_p3 = x_p2 + col_w + col_gap
elements.append(rect("s2_p3", x_p3, y2 + 340, col_w, 460,
                     stroke="#D9480F", bg="#F8F9FA", frame_id=f2, stroke_width=2))
elements.extend(make_card_with_text("s2_p3_h", x_p3 + 25, y2 + 370, col_w - 50, 70,
                                    "🌐  中英差异", font_size=32,
                                    bg="#FFE8CC", stroke="#D9480F", text_color="#D9480F",
                                    frame_id=f2))
elements.append(text("s2_p3_t1", x_p3 + 35, y2 + 480, col_w - 70, 60,
                     "英文 ≈ 1 词 1.3 Token", font_size=28, color="#111827", frame_id=f2))
elements.append(text("s2_p3_t2", x_p3 + 35, y2 + 550, col_w - 70, 60,
                     "中文 ≈ 1 字 1~2 Token", font_size=28, color="#111827", frame_id=f2))
elements.append(text("s2_p3_t3", x_p3 + 35, y2 + 630, col_w - 70, 120,
                     "国内模型中文词表大\n更便宜、更快速、更懂语境", font_size=22, color="#495057", frame_id=f2))


# ==============================================================================
# SLIDE 3: 什么是 Prompt？（提示词的本质）
# ==============================================================================
f3 = "frame_3"
y3 = 2200
elements.append(frame(f3, 0, y3, 1600, 900, "03 · 什么是 Prompt"))
add_slide_header(f3, y3, "PART 02 · 驾驭工具", "什么是 Prompt？", 3)

# Core Metaphor Banner: 交代任务
elements.extend(make_card_with_text("s3_banner", 100, y3 + 195, 1400, 95,
                                    "Prompt ＝ 你给 AI 下达的「任务指令」", font_size=42,
                                    bg="#F3F0FF", stroke="#7048E8", text_color="#5F3DC4",
                                    frame_id=f3, stroke_width=2.5))

# Contrast Section: 糟糕指令 vs 优秀指令
half_w = 680
# Left: 模糊指令
elements.append(rect("s3_bad_box", 100, y3 + 325, half_w, 350,
                     stroke="#FA5252", bg="#FFF5F5", frame_id=f3, stroke_width=2))
elements.extend(make_card_with_text("s3_bad_lbl", 130, y3 + 350, 260, 56,
                                    "❌  模糊敷衍", font_size=26,
                                    bg="#FFE3E3", stroke="#FA5252", text_color="#C92A2A",
                                    frame_id=f3))
elements.append(text("s3_bad_q", 140, y3 + 430, 600, 80,
                     "“帮我写个活动方案”", font_size=36, color="#111827", frame_id=f3))
elements.append(text("s3_bad_sub", 140, y3 + 520, 600, 120,
                     "AI 感受：没有预算、没有受众、没有目标\n只能给你泛泛而谈的废话套话",
                     font_size=24, color="#C92A2A", frame_id=f3))

# Right: 清晰指令
elements.append(rect("s3_good_box", 820, y3 + 325, half_w, 350,
                     stroke="#40C057", bg="#EBFBEE", frame_id=f3, stroke_width=2))
elements.extend(make_card_with_text("s3_good_lbl", 850, y3 + 350, 260, 56,
                                    "✅  清晰具体", font_size=26,
                                    bg="#D3F9D8", stroke="#40C057", text_color="#2B8A3E",
                                    frame_id=f3))
elements.append(text("s3_good_q", 860, y3 + 430, 600, 80,
                     "“你是资深运营，策划 100 人户外团建…”", font_size=30, color="#111827", frame_id=f3))
elements.append(text("s3_good_sub", 860, y3 + 520, 600, 120,
                     "包含目标、受众、预算、输出格式\nAI 瞬间化身专业得力助手，直接交付",
                     font_size=24, color="#2B8A3E", frame_id=f3))

# Bottom Golden Rule
elements.extend(make_card_with_text("s3_golden", 100, y3 + 705, 1400, 100,
                                    "💡  输入质量的上限，就是 AI 输出质量的上限",
                                    font_size=34, bg="#FFF4E6", stroke="#D9480F", text_color="#D9480F",
                                    frame_id=f3, stroke_width=2))


# ==============================================================================
# SLIDE 4: 写好 Prompt 的黄金框架
# ==============================================================================
f4 = "frame_4"
y4 = 3300
elements.append(frame(f4, 0, y4, 1600, 900, "04 · 黄金框架"))
add_slide_header(f4, y4, "PART 02 · 驾驭工具", "写好 Prompt 的黄金框架", 4)

# 4 Core Component Cards (横向 4 块积木)
card_w = 325
gap = 33

cards = [
    ("角色", "Role", "你是谁？", "例：资深文案、Python专家", "#1864AB", "#E7F5FF"),
    ("背景", "Context", "来龙去脉", "例：受众是谁、前因后果", "#5F3DC4", "#F3F0FF"),
    ("任务", "Task", "具体做什么", "例：产出5个小红书爆款标题", "#D9480F", "#FFE8CC"),
    ("格式", "Format", "输出长啥样", "例：用 Markdown 表格呈现", "#2B8A3E", "#EBFBEE"),
]

for i, (c_zh, c_en, c_desc, c_eg, c_stroke, c_bg) in enumerate(cards):
    cx = 100 + i * (card_w + gap)
    # Card outer
    elements.append(rect(f"s4_c_{i}", cx, y4 + 195, card_w, 400,
                         stroke=c_stroke, bg=c_bg, frame_id=f4, stroke_width=2.5))
    # Chinese Title (Very Big)
    elements.append(text(f"s4_cz_{i}", cx + 25, y4 + 230, card_w - 50, 60,
                         c_zh, font_size=48, color=c_stroke, align="center", frame_id=f4))
    # English Subtitle
    elements.append(text(f"s4_ce_{i}", cx + 25, y4 + 295, card_w - 50, 30,
                         c_en, font_size=24, color="#495057", align="center", frame_id=f4))
    # Horizontal line
    elements.append(line_el(f"s4_cl_{i}", cx + 30, y4 + 345, card_w - 60, 0,
                            color=c_stroke, width=2, frame_id=f4))
    # Meaning
    elements.append(text(f"s4_cd_{i}", cx + 20, y4 + 375, card_w - 40, 50,
                         c_desc, font_size=28, color="#111827", align="center", frame_id=f4))
    # Example
    elements.append(text(f"s4_cg_{i}", cx + 20, y4 + 450, card_w - 40, 100,
                         c_eg, font_size=20, color="#495057", align="center", frame_id=f4))

# Bottom Metaphor Box: 换位思考法则
elements.append(rect("s4_rule_box", 100, y4 + 630, 1400, 175,
                     stroke="#111827", bg="#F8F9FA", frame_id=f4, stroke_width=2))
elements.append(text("s4_rule_tag", 140, y4 + 655, 300, 32,
                     "🎯 换位思考法则（自检心法）", font_size=24, color="#7048E8", frame_id=f4))
elements.append(text("s4_rule_core", 140, y4 + 705, 1320, 65,
                     "“如果把这段话发给刚入职的实习生，他知道要做什么吗？缺少必要信息吗？”",
                     font_size=32, color="#111827", frame_id=f4))


# ==============================================================================
# SLIDE 5: 好的提示词，不是一次就能写出来的（多轮协作）
# ==============================================================================
f5 = "frame_5"
y5 = 4400
elements.append(frame(f5, 0, y5, 1600, 900, "05 · 多轮协作"))
add_slide_header(f5, y5, "PART 02 · 驾驭工具", "好的提示词，不是一次就能写出来的", 5)

# Large Subtitle Concept
elements.append(text("s5_slogan", 100, y5 + 185, 1400, 50,
                     "不要指望一句话解决所有问题",
                     font_size=34, color="#495057", frame_id=f5))

# 3 Step Progressive Flow:
# 1轮: 快速抛出起点 -> 2轮: 反客为主提问 (先让AI反问补充信息) -> 3轮: 精准追问调优 (出结果后打磨)
step_w = 440
step_gap = 40

s5_steps = [
    ("第 1 轮", "快速抛出起点", "先给基础想法，让 AI 抛砖引玉\n不要怕粗糙，先拿到第一版", "#1864AB", "#E7F5FF"),
    ("第 2 轮", "反客为主提问", "让 AI 主动反问你缺什么\n“为了达到最好效果，你还需要什么信息？”", "#5F3DC4", "#F3F0FF"),
    ("第 3 轮", "精准追问调优", "指出不足，补充约束细节\n“太官方了，语气再接地气一点”", "#D9480F", "#FFE8CC"),
]

for i, (s_tag, s_main, s_detail, s_stroke, s_bg) in enumerate(s5_steps):
    sx = 100 + i * (step_w + step_gap)
    elements.append(rect(f"s5_step_{i}", sx, y5 + 260, step_w, 360,
                         stroke=s_stroke, bg=s_bg, frame_id=f5, stroke_width=2))
    # Round badge
    elements.extend(make_card_with_text(f"s5_badge_{i}", sx + 30, y5 + 295, 140, 50,
                                        s_tag, font_size=24, bg="#FFFFFF",
                                        stroke=s_stroke, text_color=s_stroke, frame_id=f5))
    # Title
    elements.append(text(f"s5_st_{i}", sx + 30, y5 + 375, step_w - 60, 50,
                         s_main, font_size=34, color="#111827", frame_id=f5))
    # Divider
    elements.append(line_el(f"s5_sl_{i}", sx + 30, y5 + 440, step_w - 60, 0,
                            color=s_stroke, width=1.5, frame_id=f5))
    # Details
    elements.append(text(f"s5_sd_{i}", sx + 30, y5 + 465, step_w - 60, 120,
                         s_detail, font_size=22, color="#495057", frame_id=f5))

# Connecting arrows between steps
elements.append(arrow_el("s5_arr_1", 545, y5 + 440, 30, 0, color="#7048E8", width=3, frame_id=f5))
elements.append(arrow_el("s5_arr_2", 1025, y5 + 440, 30, 0, color="#7048E8", width=3, frame_id=f5))

# Bottom Mindset Card
elements.extend(make_card_with_text("s5_mindset", 100, y5 + 665, 1400, 130,
                                    "💬  最好的 Prompt，是在对话中「聊」出来的！",
                                    font_size=40, bg="#EBFBEE", stroke="#2B8A3E", text_color="#2B8A3E",
                                    frame_id=f5, stroke_width=2.5))


# ==============================================================================
# SLIDE 6: 智能体（Agent）vs 网页端聊天（豆包/DeepSeek）
# ==============================================================================
f6 = "frame_6"
y6 = 5500
elements.append(frame(f6, 0, y6, 1600, 900, "06 · 智能体与聊天框"))
add_slide_header(f6, y6, "PART 03 · 认知跃迁", "智能体 vs 网页端聊天框", 6)

# Left Side: 传统聊天框 (豆包/DeepSeek)
box_half = 680
elements.append(rect("s6_chat_box", 100, y6 + 200, box_half, 595,
                     stroke="#495057", bg="#F8F9FA", frame_id=f6, stroke_width=2))

elements.extend(make_card_with_text("s6_chat_badge", 140, y6 + 235, 340, 60,
                                    "💬 网页端聊天 (纯 LLM)", font_size=26,
                                    bg="#E9ECEF", stroke="#495057", text_color="#343A40",
                                    frame_id=f6))

elements.append(text("s6_chat_motto", 140, y6 + 325, 600, 50,
                     "“智囊军师”：动脑动嘴，不能动手",
                     font_size=32, color="#111827", frame_id=f6))

chat_points = [
    ("🧠 纯大脑思考", "拥有极其丰富的常识与推理能力"),
    ("🪟 困在网页框里", "无法感知你的本地电脑与软件"),
    ("🚫 无法执行落地", "给出步骤后，需要人类复制粘贴去操作"),
    ("⏳ 单次问答模式", "不问不答，没有主动规划与多步纠错")
]
for idx, (cp_t, cp_d) in enumerate(chat_points):
    py = y6 + 400 + idx * 90
    elements.append(text(f"s6_cp_t_{idx}", 140, py, 600, 35,
                         cp_t, font_size=26, color="#495057", frame_id=f6))
    elements.append(text(f"s6_cp_d_{idx}", 140, py + 38, 600, 30,
                         cp_d, font_size=20, color="#868E96", frame_id=f6))


# Right Side: 智能体 (Agent)
elements.append(rect("s6_agent_box", 820, y6 + 200, box_half, 595,
                     stroke="#7048E8", bg="#F3F0FF", frame_id=f6, stroke_width=2.5))

elements.extend(make_card_with_text("s6_agent_badge", 860, y6 + 235, 340, 60,
                                    "🤖 智能体 (AI Agent)", font_size=26,
                                    bg="#D0BFFF", stroke="#7048E8", text_color="#5F3DC4",
                                    frame_id=f6))

elements.append(text("s6_agent_motto", 860, y6 + 325, 600, 50,
                     "“全能员工”：大脑 ＋ 眼睛 ＋ 手脚",
                     font_size=32, color="#5F3DC4", frame_id=f6))

agent_points = [
    ("🧠 思考规划 (Plan)", "把大任务自主拆解为执行步骤"),
    ("👀 眼睛感知 (Observation)", "查看终端报错、读取本地文件、搜索实时网络"),
    ("🦾 动手执行 (Action)", "调工具：运行 Python、改代码、调 API、写文件"),
    ("🔄 闭环反思 (Loop)", "遇到报错自动修改重试，直到完整交付")
]
for idx, (ap_t, ap_d) in enumerate(agent_points):
    py = y6 + 400 + idx * 90
    elements.append(text(f"s6_ap_t_{idx}", 860, py, 600, 35,
                         ap_t, font_size=26, color="#5F3DC4", frame_id=f6))
    elements.append(text(f"s6_ap_d_{idx}", 860, py + 38, 600, 30,
                         ap_d, font_size=20, color="#495057", frame_id=f6))


# Assemble JSON Output
doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "excalidraw-diagram-generator",
    "elements": elements,
    "appState": {
        "viewBackgroundColor": "#FFFFFF",
        "gridSize": 20
    },
    "files": {}
}

output_path = "/Users/daipeng/Workspace/excalidraw-ppt/ai-basics-slides/ai-basics-slides.excalidraw"

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)

print(f"✅ Successfully created full 6 slides with {len(elements)} elements!")
print(f"📁 Output file: {output_path}")
