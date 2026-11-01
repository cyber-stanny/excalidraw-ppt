#!/usr/bin/env python3
"""
Generate complete 5-page Minimalist Presentation Slides for Agent Skills Principles.
Topic: 智能体技能（Agent Skills）底层原理与核心认知
Strict Backdrop Design Rules:
- 严格克制单页字数：拒绝密密麻麻的小字长句，只留核心要点、关键词与逻辑骨架！
- 演讲大屏 Backdrop 风格：留白足、呼吸感强、大字号（正文 22~32px，大标题 52~56px）。
- 详细案例与解释分流到 SPEAKER_NOTES.md。
"""

import json
import os

seed_counter = [80000]

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
        "text": content, "fontSize": font_size, "fontFamily": 2, # Clean Sans-serif
        "textAlign": align, "verticalAlign": "middle",
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "boundElements": None,
        "updated": 0, "link": None, "locked": False,
        "containerId": container_id, "originalText": content, "lineHeight": 1.35,
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

def make_card_with_text(prefix, x, y, w, h, content, font_size=28,
                         bg="#F8F9FA", stroke="#1E1E1E", text_color="#1E1E1E",
                         frame_id=None, stroke_width=2, roughness=1):
    rect_id = prefix
    txt_id = prefix + "_t"
    th = int(font_size * 1.35)
    ty = y + (h - th) // 2
    return [
        rect(rect_id, x, y, w, h, stroke=stroke, bg=bg,
             frame_id=frame_id, rounded=True, roughness=roughness,
             stroke_width=stroke_width, bound_text_id=txt_id),
        text(txt_id, x + 10, ty, w - 20, th, content,
             font_size=font_size, color=text_color, align="center",
             frame_id=frame_id, container_id=rect_id)
    ]

elements = []

def add_slide_header(frame_id, yo, category, title, page_no):
    elements.append(text(f"{frame_id}_cat", 100, yo + 45, 600, 30,
                         category, font_size=22, color="#7048E8", align="left", frame_id=frame_id))
    elements.append(text(f"{frame_id}_title", 100, yo + 80, 1400, 75,
                         title, font_size=52, color="#111827", align="left", frame_id=frame_id))
    elements.append(line_el(f"{frame_id}_div", 100, yo + 165, 1400, 0,
                            color="#E9ECEF", width=2, frame_id=frame_id, roughness=1))
    elements.append(text(f"{frame_id}_page", 1460, yo + 840, 60, 30,
                         f"0{page_no}" if page_no < 10 else str(page_no),
                         font_size=18, color="#ADB5BD", align="right", frame_id=frame_id))


# ==============================================================================
# SLIDE 1: 认知奠基：从“聊天通才”到“岗位专家”
# ==============================================================================
f1 = "frame_1"
y1 = 0
elements.append(frame(f1, 0, y1, 1600, 900, "01 · 认知奠基：从聊天通才到岗位专家"))
add_slide_header(f1, y1, "PART 01 · 认知奠基", "认知奠基：从“聊天通才”到“岗位专家”", 1)

elements.extend(make_card_with_text("s1_banner", 100, y1 + 195, 1400, 65,
                                    "💡 核心心智：大模型是大脑，技能（Skill）是配备的【标准化岗位 SOP + 工具包】！",
                                    font_size=26, bg="#F3F0FF", stroke="#7048E8", text_color="#5F3DC4",
                                    frame_id=f1, stroke_width=2))

c_w = 440
gap = 40
x_start = 100

# Col 1: Prompt
x_c1 = x_start
elements.append(rect("s1_box_1", x_c1, y1 + 290, c_w, 395,
                     stroke="#CED4DA", bg="#F8F9FA", frame_id=f1, stroke_width=2))
elements.extend(make_card_with_text("s1_h_1", x_c1 + 30, y1 + 315, c_w - 60, 52,
                                    "💬 Prompt（单次指令）", font_size=23,
                                    bg="#E9ECEF", stroke="#868E96", text_color="#495057", frame_id=f1))
p1_items = [
    ("定位", "口头临时交代（像发微信语音）"),
    ("特点", "单次有效，换个窗口就失忆"),
    ("局限", "缺乏沉淀，每次都得从零唠叨")
]
for idx, (lbl, val) in enumerate(p1_items):
    iy = y1 + 395 + idx * 80
    elements.append(text(f"s1_p1_l_{idx}", x_c1 + 35, iy, c_w - 70, 25,
                         f"【{lbl}】", font_size=20, color="#868E96", frame_id=f1))
    elements.append(text(f"s1_p1_v_{idx}", x_c1 + 35, iy + 28, c_w - 70, 32,
                         val, font_size=22, color="#343A40", frame_id=f1))

# Col 2: Tool
x_c2 = x_start + c_w + gap
elements.append(rect("s1_box_2", x_c2, y1 + 290, c_w, 395,
                     stroke="#4DABF7", bg="#F8FBFE", frame_id=f1, stroke_width=2))
elements.extend(make_card_with_text("s1_h_2", x_c2 + 30, y1 + 315, c_w - 60, 52,
                                    "🔧 Tool（原子工具）", font_size=23,
                                    bg="#E7F5FF", stroke="#339AF0", text_color="#1971C2", frame_id=f1))
p2_items = [
    ("定位", "单点原子功能（螺丝刀/计算器）"),
    ("特点", "提供手脚，执行特定单步操作"),
    ("局限", "有工具，但不知道按何种业务规范用")
]
for idx, (lbl, val) in enumerate(p2_items):
    iy = y1 + 395 + idx * 80
    elements.append(text(f"s1_p2_l_{idx}", x_c2 + 35, iy, c_w - 70, 25,
                         f"【{lbl}】", font_size=20, color="#1971C2", frame_id=f1))
    elements.append(text(f"s1_p2_v_{idx}", x_c2 + 35, iy + 28, c_w - 70, 32,
                         val, font_size=22, color="#1864AB", frame_id=f1))

# Col 3: Skill (Highlight)
x_c3 = x_start + (c_w + gap) * 2
elements.append(rect("s1_box_3", x_c3, y1 + 290, c_w, 395,
                     stroke="#2B8A3E", bg="#F4FBF6", frame_id=f1, stroke_width=2.5))
elements.extend(make_card_with_text("s1_h_3", x_c3 + 30, y1 + 315, c_w - 60, 52,
                                    "📦 Skill（复合技能）★", font_size=23,
                                    bg="#EBFBEE", stroke="#2B8A3E", text_color="#2B8A3E", frame_id=f1))
p3_items = [
    ("定位", "【方法论 SOP + 工具组合】能力包"),
    ("特点", "即插即用、按需唤醒、永久复用"),
    ("跃迁", "让 AI 具备特定岗位的专业交付力！")
]
for idx, (lbl, val) in enumerate(p3_items):
    iy = y1 + 395 + idx * 80
    elements.append(text(f"s1_p3_l_{idx}", x_c3 + 35, iy, c_w - 70, 25,
                         f"【{lbl}】", font_size=20, color="#2B8A3E", frame_id=f1))
    elements.append(text(f"s1_p3_v_{idx}", x_c3 + 35, iy + 28, c_w - 70, 32,
                         val, font_size=22, color="#237032", frame_id=f1))

# Bottom Takeaway
elements.append(rect("s1_bot_box", 100, y1 + 715, 1400, 85,
                     stroke="#7048E8", bg="#F3F0FF", frame_id=f1, stroke_width=2))
elements.append(text("s1_bot_txt", 130, y1 + 740, 1340, 38,
                     "🔑 名校高材生隐喻：纯模型像懂通识但不懂业务规矩的应届生；技能是独门 SOP，让其进门直接独当一面！",
                     font_size=23, color="#5F3DC4", frame_id=f1))


# ==============================================================================
# SLIDE 2: 技能解剖学：一个标准技能内部的三层构造
# ==============================================================================
f2 = "frame_2"
y2 = 1000
elements.append(frame(f2, 0, y2, 1600, 900, "02 · 技能解剖学：技能内部三层结构"))
add_slide_header(f2, y2, "PART 02 · 技能解剖学", "解剖一只“麻雀”：一个标准技能内部长什么样？", 2)

elements.extend(make_card_with_text("s2_banner", 100, y2 + 195, 1400, 65,
                                    "💡 破除黑盒神秘感：技能不是高深代码，而是一份条理清晰的结构化 Markdown 说明书！",
                                    font_size=25, bg="#F3F0FF", stroke="#7048E8", text_color="#5F3DC4",
                                    frame_id=f2, stroke_width=2))

layers = [
    {
        "num": "第 1 层",
        "name": "元数据路由层 (Frontmatter)",
        "badge": "🏷️ 门牌与身份证（常驻极轻量）",
        "bg": "#FFF9DB", "stroke": "#F59F00", "txt_c": "#D9480F",
        "core": "核心字段：name + description（触发意图描述）",
        "role": "🎯 作用：仅占几十 Token，常驻大模型待命区，专门负责意图路由！"
    },
    {
        "num": "第 2 层",
        "name": "标准作业规范层 (Instructions)",
        "badge": "📜 操作指南与行为护栏（核心正文）",
        "bg": "#EBFBEE", "stroke": "#2B8A3E", "txt_c": "#237032",
        "core": "包含要素：执行步骤 (SOP) ＋ 禁忌红线 (Do & Don't) ＋ 自检清单",
        "role": "🛡️ 作用：动态按需载入，收敛大模型的随机发散，锁定专业级确定性交付！"
    },
    {
        "num": "第 3 层",
        "name": "资产与工具支撑层 (Resources)",
        "badge": "🧰 随身弹药与执行工具（扩展支持）",
        "bg": "#E7F5FF", "stroke": "#339AF0", "txt_c": "#1864AB",
        "core": "包含要素：辅助脚本 (Python/Shell) ＋ 行业报表模板 ＋ 优质范例",
        "role": "⚡ 作用：供技能内部按需执行与参考，赋能大模型精确搞定严苛任务！"
    }
]

ly_h = 145
ly_gap = 22
ly_start = y2 + 285

for idx, item in enumerate(layers):
    cur_y = ly_start + idx * (ly_h + ly_gap)
    # Box
    elements.append(rect(f"s2_box_{idx}", 100, cur_y, 1400, ly_h,
                         stroke=item["stroke"], bg=item["bg"], frame_id=f2, stroke_width=2))
    
    # Left: Header badges
    elements.append(text(f"s2_num_{idx}", 130, cur_y + 25, 120, 32,
                         item["num"], font_size=24, color=item["txt_c"], frame_id=f2))
    elements.append(text(f"s2_name_{idx}", 240, cur_y + 25, 450, 32,
                         item["name"], font_size=24, color="#111827", frame_id=f2))
    elements.append(text(f"s2_badge_{idx}", 720, cur_y + 25, 600, 32,
                         item["badge"], font_size=22, color=item["txt_c"], align="right", frame_id=f2))
    
    # Divider line
    elements.append(line_el(f"s2_div_{idx}", 130, cur_y + 65, 1340, 0,
                            color=item["stroke"], width=1, frame_id=f2))
    
    # Bottom details (Bold & clear)
    elements.append(text(f"s2_core_{idx}", 130, cur_y + 75, 1340, 30,
                         item["core"], font_size=20, color="#212529", frame_id=f2))
    elements.append(text(f"s2_role_{idx}", 130, cur_y + 105, 1340, 30,
                         item["role"], font_size=20, color="#495057", frame_id=f2))

# Bottom Takeaway
elements.append(rect("s2_bot_box", 100, y2 + 785, 1400, 55,
                     stroke="#7048E8", bg="#F3F0FF", frame_id=f2, stroke_width=1.5))
elements.append(text("s2_bot_txt", 130, y2 + 798, 1340, 30,
                     "📌 结构决定机制：正因为有第 1 层轻量门牌，AI 才能在不读完整手册的情况下，秒级识别该翻哪一本！",
                     font_size=21, color="#5F3DC4", frame_id=f2))


# ==============================================================================
# SLIDE 3: 核心全景大图：5个技能场景下的“渐进式加载”全流程
# ==============================================================================
f3 = "frame_3"
y3 = 2000
elements.append(frame(f3, 0, y3, 1600, 900, "03 · 核心全景大图：5个技能渐进式加载全流程"))
add_slide_header(f3, y3, "PART 03 · 核心运转机制", "核心全景图：5 个技能场景下的“渐进式加载”全流程", 3)

elements.extend(make_card_with_text("s3_banner", 100, y3 + 195, 1400, 60,
                                    "💡 场景设定：已安装 5 个技能，用户输入一句提示词，看智能体如何两阶段精准按需加载！",
                                    font_size=24, bg="#F3F0FF", stroke="#7048E8", text_color="#5F3DC4",
                                    frame_id=f3, stroke_width=2))

step_w = 320
step_gap = 40
sx_base = 100

steps_data = [
    {
        "num": "STEP 01", "title": "常驻待命区",
        "bg": "#F8F9FA", "stroke": "#ADB5BD", "head_bg": "#E9ECEF", "head_c": "#495057",
        "badges": [
            ("A: PDF结构化解析", False),
            ("B: 爆款文案润色", False),
            ("C: 数据图表绘制 ★", True),
            ("D: 自动化邮件收发", False),
            ("E: 代码规范审查", False)
        ],
        "highlight": "仅挂载 Name+Desc 门牌\nToken 底噪极低 (~200 字)"
    },
    {
        "num": "STEP 02", "title": "意图路由决策",
        "bg": "#FFF9DB", "stroke": "#F59F00", "head_bg": "#FFF3BF", "head_c": "#D9480F",
        "badges": [
            ("💬 用户输入：", False),
            ("“分析财报并绘制走势图”", True),
            ("🧠 大脑扫描 5 块门牌", False),
            ("🎯 命中【技能 C：图表】", True),
            ("其余 4 个技能完全休眠", False)
        ],
        "highlight": "毫秒级意图匹配\n无需加载任何无关技能"
    },
    {
        "num": "STEP 03", "title": "渐进式按需加载",
        "bg": "#EBFBEE", "stroke": "#2B8A3E", "head_bg": "#D3F9D8", "head_c": "#2B8A3E",
        "badges": [
            ("📖 动态翻开技能 C 手册", True),
            ("载入绘图 SOP 步骤规范", False),
            ("载入配色标准与自检红线", False),
            ("准备 Python 绘图依赖", False),
            ("仅技能 C 注入活跃记忆", True)
        ],
        "highlight": "Progressive Disclosure\n用时才读，绝不浪费脑容量"
    },
    {
        "num": "STEP 04", "title": "标准化交付",
        "bg": "#E7F5FF", "stroke": "#339AF0", "head_bg": "#D0EBFF", "head_c": "#1864AB",
        "badges": [
            ("1. 提取财报季度指标", False),
            ("2. 依规生成绘图脚本", False),
            ("3. 调用工具渲染折线图", True),
            ("4. 质量自检单位与标注", False),
            ("📊 高质量图表交付！", True)
        ],
        "highlight": "确定性专业交付\n老手式的稳定高水准产出"
    }
]

for idx, st in enumerate(steps_data):
    st_x = sx_base + idx * (step_w + step_gap)
    st_y = y3 + 275
    
    # Outer box
    elements.append(rect(f"s3_b_{idx}", st_x, st_y, step_w, 470,
                         stroke=st["stroke"], bg=st["bg"], frame_id=f3, stroke_width=2))
    
    # Header
    elements.append(rect(f"s3_h_{idx}", st_x, st_y, step_w, 60,
                         stroke=st["stroke"], bg=st["head_bg"], frame_id=f3, rounded=True, stroke_width=1.5))
    elements.append(text(f"s3_ht_{idx}", st_x + 10, st_y + 16, step_w - 20, 28,
                         st["num"] + " · " + st["title"], font_size=21, color=st["head_c"], align="center", frame_id=f3))
    
    # Badges list
    for b_idx, (b_txt, is_hi) in enumerate(st["badges"]):
        by = st_y + 75 + b_idx * 55
        badge_bg = "#EBFBEE" if is_hi else "#FFFFFF"
        badge_border = "#2B8A3E" if is_hi else "#DEE2E6"
        badge_tc = "#2B8A3E" if is_hi else "#343A40"
        
        elements.append(rect(f"s3_bg_{idx}_{b_idx}", st_x + 15, by, step_w - 30, 46,
                             stroke=badge_border, bg=badge_bg, frame_id=f3, rounded=True, stroke_width=1.5 if is_hi else 1))
        elements.append(text(f"s3_bt_{idx}_{b_idx}", st_x + 20, by + 9, step_w - 40, 28,
                             b_txt, font_size=16, color=badge_tc, align="center", frame_id=f3))
    
    # Footer highlight card
    elements.append(rect(f"s3_fb_{idx}", st_x + 15, st_y + 365, step_w - 30, 85,
                         stroke=st["stroke"], bg="#FFFFFF", frame_id=f3, rounded=True, stroke_width=1.5))
    elements.append(text(f"s3_ft_{idx}", st_x + 20, st_y + 375, step_w - 40, 65,
                         st["highlight"], font_size=16, color=st["head_c"], align="center", frame_id=f3))
    
    # Arrow to next step
    if idx < 3:
        arr_x = st_x + step_w + 5
        elements.append(arrow_el(f"s3_arr_{idx}", arr_x, st_y + 235, 30, 0,
                                 color="#7048E8", width=3, frame_id=f3))

# Bottom Takeaway
elements.append(rect("s3_bot_box", 100, y3 + 765, 1400, 75,
                     stroke="#2B8A3E", bg="#EBFBEE", frame_id=f3, stroke_width=2))
elements.append(text("s3_bot_txt", 130, y3 + 788, 1340, 35,
                     "🌟 渐进式加载核心精髓：未被点中的技能在待命区零噪音待机；一旦需要，秒级调入专属 SOP 精准破局！",
                     font_size=23, color="#237032", frame_id=f3))


# ==============================================================================
# SLIDE 4: 深度辨析：为什么必须“渐进式加载”？
# ==============================================================================
f4 = "frame_4"
y4 = 3000
elements.append(frame(f4, 0, y4, 1600, 900, "04 · 深度原理解析：为什么必须渐进式？"))
add_slide_header(f4, y4, "PART 04 · 深度原理解析", "深度辨析：为什么不能把所有技能一次性全塞给 AI？", 4)

elements.extend(make_card_with_text("s4_banner", 100, y4 + 195, 1400, 65,
                                    "💡 核心发问：既然技能这么有用，为什么不把 5 个、50 个技能的 SOP 一次性全塞进上下文？",
                                    font_size=25, bg="#F3F0FF", stroke="#7048E8", text_color="#5F3DC4",
                                    frame_id=f4, stroke_width=2))

col_w4 = 680
x4_l = 100
x4_r = 820

# Left: 全量硬塞
elements.append(rect("s4_box_l", x4_l, y4 + 290, col_w4, 415,
                     stroke="#E03131", bg="#FFF5F5", frame_id=f4, stroke_width=2.5))
elements.extend(make_card_with_text("s4_bh_l", x4_l + 40, y4 + 315, col_w4 - 80, 52,
                                    "❌ 全量硬塞（巨石方案 All-in-Prompt）", font_size=23,
                                    bg="#FFE3E3", stroke="#E03131", text_color="#C92A2A", frame_id=f4))

bad_items = [
    ("💸 Token 爆炸与天价账单", "50 个技能几十万字，哪怕只说句“你好”，都在重复烧钱"),
    ("😵 注意力迷失 (Lost in the Middle)", "规则堆积成山，多技能规则相互打架冲突，输出严重翻车"),
    ("💥 可扩展性彻底瘫痪", "每多加一个技能系统就变慢一倍，装到十几个技能直接宕机")
]
for idx, (t, d) in enumerate(bad_items):
    py = y4 + 390 + idx * 95
    elements.append(text(f"s4_bt_{idx}", x4_l + 40, py, col_w4 - 80, 30,
                         t, font_size=23, color="#C92A2A", frame_id=f4))
    elements.append(text(f"s4_bd_{idx}", x4_l + 40, py + 34, col_w4 - 80, 35,
                         d, font_size=19, color="#495057", frame_id=f4))

# Right: 渐进式加载
elements.append(rect("s4_box_r", x4_r, y4 + 290, col_w4, 415,
                     stroke="#2B8A3E", bg="#F4FBF6", frame_id=f4, stroke_width=2.5))
elements.extend(make_card_with_text("s4_bh_r", x4_r + 40, y4 + 315, col_w4 - 80, 52,
                                    "✅ 渐进式按需加载（Progressive Disclosure）", font_size=23,
                                    bg="#EBFBEE", stroke="#2B8A3E", text_color="#2B8A3E", frame_id=f4))

good_items = [
    ("💰 极致轻量与零待机成本", "平时常驻只有极简门牌（几百 Token），命中才翻开正文"),
    ("🎯 注意力绝对聚焦 (Laser Focus)", "执行时上下文纯净，只专注当前 1 个专属 SOP，稳定无干扰"),
    ("🚀 无限横向扩展 (Infinite Scaling)", "装 5 个技能和装 500 个技能一样轻快！随时增删插拔")
]
for idx, (t, d) in enumerate(good_items):
    py = y4 + 390 + idx * 95
    elements.append(text(f"s4_gt_{idx}", x4_r + 40, py, col_w4 - 80, 30,
                         t, font_size=23, color="#2B8A3E", frame_id=f4))
    elements.append(text(f"s4_gd_{idx}", x4_r + 40, py + 34, col_w4 - 80, 35,
                         d, font_size=19, color="#212529", frame_id=f4))

# Bottom Golden Takeaway
elements.append(rect("s4_bot_box", 100, y4 + 735, 1400, 80,
                     stroke="#7048E8", bg="#F3F0FF", frame_id=f4, stroke_width=2))
elements.append(text("s4_bot_txt", 130, y4 + 760, 1340, 35,
                     "🔑 架构黄金法则：“高明的智能体架构不是比拼塞了多少东西，而是比拼如何在正确的时间只调入最需要的信息！”",
                     font_size=23, color="#5F3DC4", frame_id=f4))


# ==============================================================================
# SLIDE 5: 设计心智：什么样的技能才能被 AI “准确选中并可靠执行”？
# ==============================================================================
f5 = "frame_5"
y5 = 4000
elements.append(frame(f5, 0, y5, 1600, 900, "05 · 进阶设计心智：如何写好技能"))
add_slide_header(f5, y5, "PART 05 · 进阶设计心智", "设计心智：什么样的技能才能被 AI “准确选中并执行”？", 5)

elements.extend(make_card_with_text("s5_banner", 100, y5 + 195, 1400, 65,
                                    "💡 从原理反推设计：掌握三大心智，人人都能成为能写出高水准技能的“架构师”！",
                                    font_size=25, bg="#F3F0FF", stroke="#7048E8", text_color="#5F3DC4",
                                    frame_id=f5, stroke_width=2))

c5_w = 440
gap5 = 40

minds = [
    {
        "title": "心智 ① · 路由开关",
        "sub": "Description 不是吹嘘，是触发条件",
        "bg": "#FFF9DB", "stroke": "#F59F00", "head_bg": "#FFF3BF", "head_c": "#D9480F",
        "wrong_t": "❌ 自吹自擂：",
        "wrong_d": "“这是史上最强大的分析神器！”\n➔ 模型不知何时该调用",
        "right_t": "✅ 明确触发场景：",
        "right_d": "“当需要绘制走势图或分析财报时调用”\n➔ 精准匹配用户意图"
    },
    {
        "title": "心智 ② · 防呆护栏",
        "sub": "SOP 立硬红线，用自检收敛随机性",
        "bg": "#EBFBEE", "stroke": "#2B8A3E", "head_bg": "#D3F9D8", "head_c": "#2B8A3E",
        "wrong_t": "❌ 空泛说教：",
        "wrong_d": "“请尽量让输出变得美观专业”\n➔ 模型理解发散，屡屡翻车",
        "right_t": "✅ 确定性约束：",
        "right_d": "“必须标注单位；交付前核对自检清单”\n➔ 规则确定性收敛随机性"
    },
    {
        "title": "心智 ③ · 单一职责",
        "sub": "坚持小而美，拒绝巨石航空母舰",
        "bg": "#E7F5FF", "stroke": "#339AF0", "head_bg": "#D0EBFF", "head_c": "#1864AB",
        "wrong_t": "❌ 贪大求全：",
        "wrong_d": "企图把搜索、分析、写代码全包揽\n➔ 过于臃肿，极易混淆",
        "right_t": "✅ 积木式组装：",
        "right_d": "一个技能只专注干好一件事！\n➔ 多个小技能自由路由倍增威力"
    }
]

for idx, m in enumerate(minds):
    mx = 100 + idx * (c5_w + gap5)
    my = y5 + 290
    
    # Outer box
    elements.append(rect(f"s5_box_{idx}", mx, my, c5_w, 410,
                         stroke=m["stroke"], bg=m["bg"], frame_id=f5, stroke_width=2))
    
    # Card Header
    elements.append(rect(f"s5_h_{idx}", mx, my, c5_w, 65,
                         stroke=m["stroke"], bg=m["head_bg"], frame_id=f5, rounded=True, stroke_width=1.5))
    elements.append(text(f"s5_ht_{idx}", mx + 10, my + 10, c5_w - 20, 26,
                         m["title"], font_size=22, color=m["head_c"], align="center", frame_id=f5))
    elements.append(text(f"s5_hs_{idx}", mx + 10, my + 38, c5_w - 20, 20,
                         m["sub"], font_size=15, color="#495057", align="center", frame_id=f5))
    
    # Wrong Box
    elements.append(rect(f"s5_wb_{idx}", mx + 20, my + 85, c5_w - 40, 125,
                         stroke="#FFA8A8", bg="#FFF5F5", frame_id=f5, rounded=True, stroke_width=1))
    elements.append(text(f"s5_wt_lbl_{idx}", mx + 30, my + 95, c5_w - 60, 25,
                         m["wrong_t"], font_size=18, color="#C92A2A", frame_id=f5))
    elements.append(text(f"s5_wt_{idx}", mx + 30, my + 125, c5_w - 60, 75,
                         m["wrong_d"], font_size=17, color="#C92A2A", frame_id=f5))
    
    # Right Box
    elements.append(rect(f"s5_rb_{idx}", mx + 20, my + 230, c5_w - 40, 140,
                         stroke="#8CE99A", bg="#F4FBF6", frame_id=f5, rounded=True, stroke_width=1.5))
    elements.append(text(f"s5_rt_lbl_{idx}", mx + 30, my + 240, c5_w - 60, 25,
                         m["right_t"], font_size=18, color="#237032", frame_id=f5))
    elements.append(text(f"s5_rt_{idx}", mx + 30, my + 270, c5_w - 60, 85,
                         m["right_d"], font_size=17, color="#237032", frame_id=f5))

# Bottom Golden Formula
elements.append(rect("s5_bot_box", 100, y5 + 725, 1400, 90,
                     stroke="#7048E8", bg="#F3F0FF", frame_id=f5, stroke_width=2))
elements.append(text("s5_bot_txt", 130, y5 + 750, 1340, 42,
                     "🌟 技能架构黄金公式：高质量技能 ＝ 明确触发场景（精准路由） ＋ 严密作业标准（稳定交付） ＋ 单一专注场景（灵活拼装）！",
                     font_size=23, color="#5F3DC4", frame_id=f5))


# ==============================================================================
# Save Excalidraw JSON
# ==============================================================================
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

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent-skills-slides.excalidraw")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)

print(f"✅ Successfully regenerated 5 clean & breathing slides with {len(elements)} elements to {output_path}!")
