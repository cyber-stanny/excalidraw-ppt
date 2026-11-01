#!/usr/bin/env python3
"""
Generate complete 8-page Minimalist Presentation Slides for WorkBuddy Cloud Services (Serverless).
Design Principles:
- Standard Clear Fonts (fontFamily=2 / System Sans-serif, crisp, highly legible for lecture backdrop).
- Breathing room & high impact: Remove dense secondary explanations, focus on bold keywords & punchlines.
- Large fonts (24~56px), uncluttered card layouts, spacious margins.
"""

import json

seed_counter = [50000]

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
        "text": content, "fontSize": font_size, "fontFamily": 2, # Standard Clean Sans-serif
        "textAlign": align, "verticalAlign": "middle",
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "boundElements": None,
        "updated": 0, "link": None, "locked": False,
        "containerId": container_id, "originalText": content, "lineHeight": 1.3,
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
                         title, font_size=56, color="#111827", align="left", frame_id=frame_id))
    elements.append(line_el(f"{frame_id}_div", 100, yo + 165, 1400, 0,
                            color="#E9ECEF", width=2, frame_id=frame_id, roughness=1))
    elements.append(text(f"{frame_id}_page", 1460, yo + 840, 60, 30,
                         f"0{page_no}" if page_no < 10 else str(page_no),
                         font_size=18, color="#ADB5BD", align="right", frame_id=frame_id))


# ==============================================================================
# SLIDE 1: 什么是 Serverless（无服务器）？
# ==============================================================================
f1 = "frame_1"
y1 = 0
elements.append(frame(f1, 0, y1, 1600, 900, "01 · 什么是 Serverless"))
add_slide_header(f1, y1, "PART 01 · 认知奠基", "揭开本质：什么是 Serverless（无服务器）？", 1)

elements.extend(make_card_with_text("s1_banner", 100, y1 + 195, 1400, 65,
                                    "💡 核心心智：云服务不是买电脑，而是接入开发界的「自来水与电网」",
                                    font_size=28, bg="#F3F0FF", stroke="#7048E8", text_color="#5F3DC4",
                                    frame_id=f1, stroke_width=2))

col_w = 680
x_l = 100
x_r = 820

# Left: 传统云主机
elements.append(rect("s1_box_l", x_l, y1 + 285, col_w, 400,
                     stroke="#ADB5BD", bg="#F8F9FA", frame_id=f1, stroke_width=2))
elements.extend(make_card_with_text("s1_bh_l", x_l + 40, y1 + 315, 320, 56,
                                    "❌ 传统模式（买发电机）", font_size=24,
                                    bg="#E9ECEF", stroke="#868E96", text_color="#495057", frame_id=f1))

trad_points = [
    "• 包月交租：无人访问，费用照扣不误",
    "• 机器运维：自己装 Linux、配环境、修漏洞",
    "• 极易宕机：大半夜服务挂了得爬起来修",
    "• 扩容困难：突然来 1000 个人网站直接卡死"
]
for idx, t in enumerate(trad_points):
    py = y1 + 395 + idx * 68
    elements.append(text(f"s1_tp_{idx}", x_l + 50, py, col_w - 100, 36,
                         t, font_size=24, color="#C92A2A", frame_id=f1))

# Right: Serverless 模式
elements.append(rect("s1_box_r", x_r, y1 + 285, col_w, 400,
                     stroke="#2B8A3E", bg="#F4FBF6", frame_id=f1, stroke_width=2.5))
elements.extend(make_card_with_text("s1_bh_r", x_r + 40, y1 + 315, 320, 56,
                                    "✅ Serverless（接自来水）", font_size=24,
                                    bg="#EBFBEE", stroke="#2B8A3E", text_color="#2B8A3E", frame_id=f1))

serverless_points = [
    "✔ 按需使用：有人访问才计费，无人访问 0 成本",
    "✔ 零运维：腾讯云团队 24 小时在后台兜底",
    "✔ 开箱即用：数据库、文件存储、鉴权现成调用",
    "✔ 弹性伸缩：从 1 个人到 10 万人访问自动扩容"
]
for idx, t in enumerate(serverless_points):
    py = y1 + 395 + idx * 68
    elements.append(text(f"s1_sp_{idx}", x_r + 50, py, col_w - 100, 36,
                         t, font_size=24, color="#2B8A3E", frame_id=f1))

# Bottom Golden Takeaway
elements.append(rect("s1_bot_box", 100, y1 + 710, 1400, 90,
                     stroke="#7048E8", bg="#F3F0FF", frame_id=f1, stroke_width=2))
elements.append(text("s1_bot_txt", 140, y1 + 735, 1320, 40,
                     "🔑 金句：“Serverless 并不是没有服务器，而是让你【彻底摆脱买服务器和修服务器的苦差事】！”",
                     font_size=25, color="#5F3DC4", frame_id=f1))


# ==============================================================================
# SLIDE 2: 什么时候你的应用需要「云服务」？
# ==============================================================================
f2 = "frame_2"
y2 = 1000
elements.append(frame(f2, 0, y2, 1600, 900, "02 · 场景判别"))
add_slide_header(f2, y2, "PART 02 · 场景切入", "什么时候你的应用需要「云服务」？", 2)

elements.append(rect("s2_box_l", x_l, y2 + 195, col_w, 395,
                     stroke="#ADB5BD", bg="#F8F9FA", frame_id=f2, stroke_width=2))
elements.extend(make_card_with_text("s2_badge_l", x_l + 40, y2 + 225, 280, 56,
                                    "🚫 不需要云服务", font_size=24,
                                    bg="#E9ECEF", stroke="#868E96", text_color="#495057", frame_id=f2))
elements.append(text("s2_sub_l", x_l + 345, y2 + 238, 300, 35,
                     "纯前端 · 刷新即重置", font_size=22, color="#868E96", frame_id=f2))

no_cloud_cases = [
    ("📄 个人作品集 / 简历主页", "纯内容展示，无需记录访客数据"),
    ("🎨 活动宣传海报 / 邀请函", "单向信息触达，看完即走"),
    ("🕹️ 单机本地小游戏 / 计算器", "所有计算只在用户手机/浏览器本地运行")
]
for idx, (title, desc) in enumerate(no_cloud_cases):
    cy = y2 + 305 + idx * 88
    elements.append(text(f"s2_nc_t_{idx}", x_l + 45, cy, col_w - 90, 34,
                         title, font_size=24, color="#343A40", frame_id=f2))
    elements.append(text(f"s2_nc_d_{idx}", x_l + 45, cy + 36, col_w - 90, 26,
                         desc, font_size=18, color="#868E96", frame_id=f2))

# Right Column: 必须需要云服务
elements.append(rect("s2_box_r", x_r, y2 + 195, col_w, 395,
                     stroke="#2B8A3E", bg="#F4FBF6", frame_id=f2, stroke_width=2.5))
elements.extend(make_card_with_text("s2_badge_r", x_r + 40, y2 + 225, 280, 56,
                                    "✅ 必须需要云服务", font_size=24,
                                    bg="#EBFBEE", stroke="#2B8A3E", text_color="#2B8A3E", frame_id=f2))
elements.append(text("s2_sub_r", x_r + 345, y2 + 238, 300, 35,
                     "全栈动态 · 跨设备持久化", font_size=22, color="#2B8A3E", frame_id=f2))

need_cloud_cases = [
    ("💬 留言板 / 社区发帖互动", "多人共享：别人留的言你换台电脑也能看得到"),
    ("🎮 游戏存档 / 用户偏好设置", "跨设备同步：换个设备登录，数据依然完整"),
    ("🤖 接入大模型 AI 智能能力", "安全调用：大模型 API 必须由服务端安全代理")
]
for idx, (title, desc) in enumerate(need_cloud_cases):
    cy = y2 + 305 + idx * 88
    elements.append(text(f"s2_nd_t_{idx}", x_r + 45, cy, col_w - 90, 34,
                         title, font_size=24, color="#111827", frame_id=f2))
    elements.append(text(f"s2_nd_d_{idx}", x_r + 45, cy + 36, col_w - 90, 26,
                         desc, font_size=18, color="#2B8A3E", frame_id=f2))

# Bottom Banner: 痛点对比
elements.append(rect("s2_bot_box", 100, y2 + 615, 1400, 185,
                     stroke="#7048E8", bg="#F3F0FF", frame_id=f2, stroke_width=2))
elements.append(text("s2_bot_tag", 140, y2 + 635, 300, 30,
                     "💡 从传统运维到 WorkBuddy 革命", font_size=22, color="#7048E8", frame_id=f2))
elements.append(text("s2_bot_c1", 140, y2 + 675, 1320, 38,
                     "传统做法：买云服务器 ＋ 装数据库 ＋ 写接口 ＋ 配域名证书（熟练工程师耗时数天）",
                     font_size=24, color="#495057", frame_id=f2))
elements.append(text("s2_bot_c2", 140, y2 + 725, 1320, 42,
                     "WorkBuddy：对接腾讯 CloudBase，AI 自动打通全栈后端，点击确认即可开通！",
                     font_size=28, color="#5F3DC4", frame_id=f2))


# ==============================================================================
# SLIDE 3: WorkBuddy 云服务五大核心能力全景
# ==============================================================================
f3 = "frame_3"
y3 = 2000
elements.append(frame(f3, 0, y3, 1600, 900, "03 · 五大能力全景"))
add_slide_header(f3, y3, "PART 03 · 全局视野", "WorkBuddy 云服务五大核心能力全景", 3)

elements.extend(make_card_with_text("s3_top_banner", 100, y3 + 190, 1400, 56,
                                    "底层深度对接腾讯云 CloudBase · 开箱即用的 5 大功能积木",
                                    font_size=26, bg="#F1F3F5", stroke="#ADB5BD", text_color="#343A40",
                                    frame_id=f3, stroke_width=1.5))

pillars = [
    {
        "icon": "🗄️", "title": "数据库", "meta": "「电子记账本」",
        "stroke": "#1971C2", "bg": "#E7F5FF", "color": "#1864AB",
        "badge": "结构化中枢",
        "bullets": [
            "• 存文字、数值、时间",
            "• 按应用独立环境隔离",
            "• AI 自动建表直读直写"
        ]
    },
    {
        "icon": "📁", "title": "文件存储", "meta": "「海量大仓库」",
        "stroke": "#2B8A3E", "bg": "#EBFBEE", "color": "#2B8A3E",
        "badge": "腾讯云 COS",
        "bullets": [
            "• 托管图片、视频、附件",
            "• 免配桶名，大厂托管",
            "• 自动生成 CDN 加速外链"
        ]
    },
    {
        "icon": "🔐", "title": "身份认证", "meta": "「专属门禁卡」",
        "stroke": "#7048E8", "bg": "#F3F0FF", "color": "#5F3DC4",
        "badge": "多租户体系",
        "bullets": [
            "• 开箱即用注册与登录",
            "• 原生持久化会话状态",
            "• 张三李四数据天然隔离"
        ]
    },
    {
        "icon": "📊", "title": "数据统计", "meta": "「驾驶舱仪表盘」",
        "stroke": "#D9480F", "bg": "#FFF4E6", "color": "#D9480F",
        "badge": "业务监控",
        "bullets": [
            "• 免埋点掌控访问热度",
            "• PV / UV 独立访客走势",
            "• 存储容量与接口健康度"
        ]
    },
    {
        "icon": "🧠", "title": "内置大模型", "meta": "「外脑智囊顾问」",
        "stroke": "#C92A2A", "bg": "#FFF5F5", "color": "#C92A2A",
        "badge": "免买 API Key",
        "bullets": [
            "• 无需充值绑定信用卡",
            "• 开箱即调主流大模型",
            "• 后端代理杜绝密钥泄露"
        ]
    }
]

p_w = 260
p_gap = 25
start_x = 100
box_y = y3 + 265
box_h = 445

for i, p in enumerate(pillars):
    px = start_x + i * (p_w + p_gap)
    # Outer box (tightened from 480 to 445)
    elements.append(rect(f"s3_p_{i}", px, box_y, p_w, box_h,
                         stroke=p["stroke"], bg="#FFFFFF", frame_id=f3, stroke_width=2))
    # Icon card
    elements.extend(make_card_with_text(f"s3_ic_{i}", px + 20, box_y + 20, p_w - 40, 60,
                                        p["icon"], font_size=32,
                                        bg=p["bg"], stroke=p["stroke"], text_color=p["color"],
                                        frame_id=f3, stroke_width=1.5))
    # Title
    elements.append(text(f"s3_tt_{i}", px + 10, box_y + 92, p_w - 20, 36,
                         p["title"], font_size=28, color=p["color"], align="center", frame_id=f3))
    # Metaphor badge
    elements.append(text(f"s3_mt_{i}", px + 10, box_y + 130, p_w - 20, 26,
                         p["meta"], font_size=20, color="#E64980", align="center", frame_id=f3))
    # Tag chip
    elements.extend(make_card_with_text(f"s3_ch_{i}", px + 35, box_y + 168, p_w - 70, 34,
                                        p["badge"], font_size=17,
                                        bg=p["bg"], stroke=p["stroke"], text_color=p["color"],
                                        frame_id=f3, stroke_width=1))
    # Divider
    elements.append(line_el(f"s3_ln_{i}", px + 25, box_y + 218, p_w - 50, 0,
                            color=p["bg"], width=2, frame_id=f3))
    # 3 distinct bullet points well spaced
    for b_idx, bullet in enumerate(p["bullets"]):
        by = box_y + 238 + b_idx * 62
        elements.append(text(f"s3_b_{i}_{b_idx}", px + 18, by, p_w - 36, 52,
                             bullet, font_size=19, color="#495057", align="left", frame_id=f3))

# Bottom Action Banner (solid prominent footer card)
elements.append(rect("s3_bot_banner", 100, y3 + 730, 1400, 78,
                     stroke="#7048E8", bg="#F3F0FF", frame_id=f3, stroke_width=2))
elements.append(text("s3_bot_note", 140, y3 + 750, 1320, 38,
                     "⚡️ 只要在 WorkBuddy 里跟 AI 说做带存储的应用，点击一次确认框即在后台全部开通！",
                     font_size=24, color="#5F3DC4", align="center", frame_id=f3))


# ==============================================================================
# SLIDE 4: 能力 1 · 数据库（Database）：应用的电子记账本
# ==============================================================================
f4 = "frame_4"
y4 = 3000
elements.append(frame(f4, 0, y4, 1600, 900, "04 · 数据库能力"))
add_slide_header(f4, y4, "PART 04 · 能力拆解 ①", "数据库（Database）：应用的电子记账本", 4)

# Left Column: 三大核心特性（清晰简练，去掉冗余文字）
elements.append(rect("s4_box_l", 100, y4 + 195, 720, 580,
                     stroke="#1971C2", bg="#F8F9FA", frame_id=f4, stroke_width=2))
elements.extend(make_card_with_text("s4_h_l", 135, y4 + 225, 300, 52,
                                    "⚙️ 核心特性与优势", font_size=24,
                                    bg="#E7F5FF", stroke="#1971C2", text_color="#1864AB", frame_id=f4))

db_features = [
    ("📦 按应用严格隔离", "每个应用拥有独立数据空间，表结构互不冲突"),
    ("🪄 AI 自动建表读写", "自然语言描述需求，AI 自动设计字段并编写调用代码"),
    ("🖥️ 可视化控制台", "专属数据面板，直观查看表记录、手动改数据、备份导出")
]
for idx, (title, desc) in enumerate(db_features):
    fy = y4 + 300 + idx * 145
    elements.append(rect(f"s4_fc_{idx}", 135, fy, 650, 115,
                         stroke="#CED4DA", bg="#FFFFFF", frame_id=f4, stroke_width=1.5))
    elements.append(text(f"s4_ft_{idx}", 165, fy + 20, 590, 34,
                         title, font_size=26, color="#1971C2", frame_id=f4))
    elements.append(text(f"s4_fd_{idx}", 165, fy + 62, 590, 34,
                         desc, font_size=20, color="#495057", frame_id=f4))

# Right Column: 表模型
elements.append(rect("s4_box_r", 850, y4 + 195, 650, 580,
                     stroke="#495057", bg="#FFFFFF", frame_id=f4, stroke_width=2))
elements.extend(make_card_with_text("s4_h_r", 885, y4 + 225, 300, 52,
                                    "📊 数据表结构示例", font_size=24,
                                    bg="#F1F3F5", stroke="#495057", text_color="#212529", frame_id=f4))

elements.append(rect("s4_tbl_hdr", 885, y4 + 300, 580, 50,
                     stroke="#1971C2", bg="#E7F5FF", frame_id=f4, stroke_width=1.5))
elements.append(text("s4_tbl_ht", 905, y4 + 310, 540, 30,
                     "表名：photos（相册数据表）", font_size=22, color="#1864AB", frame_id=f4))

rows = [
    ("id", "String (UUID)", "图片唯一标识主键"),
    ("title", "String", "照片描述标题"),
    ("file_path", "String", "文件存储路径 (COS URL)"),
    ("created_at", "DateTime", "上传时间戳")
]
for idx, (fld, tp, comment) in enumerate(rows):
    ry = y4 + 360 + idx * 68
    elements.append(rect(f"s4_r_{idx}", 885, ry, 580, 58,
                         stroke="#E9ECEF", bg="#F8F9FA", frame_id=f4, stroke_width=1))
    elements.append(text(f"s4_rf_{idx}", 905, ry + 14, 130, 30,
                         fld, font_size=20, color="#111827", frame_id=f4))
    elements.append(text(f"s4_rt_{idx}", 1045, ry + 14, 150, 30,
                         tp, font_size=18, color="#7048E8", frame_id=f4))
    elements.append(text(f"s4_rc_{idx}", 1205, ry + 14, 250, 30,
                         comment, font_size=17, color="#495057", frame_id=f4))

# Bottom Rule Box: 换行并清晰对齐，不再溢出
elements.append(rect("s4_r_tip", 885, y4 + 645, 580, 100,
                     stroke="#2B8A3E", bg="#EBFBEE", frame_id=f4, stroke_width=1.5))
elements.append(text("s4_r_tipt", 905, y4 + 655, 540, 80,
                     "💡 敲黑板：记账本只存文字与网址！\n几兆的高清图片千万别硬塞进数据库！",
                     font_size=22, color="#2B8A3E", frame_id=f4))


# ==============================================================================
# SLIDE 5: 能力 2 · 文件存储（Storage）：海量多媒体大仓库
# ==============================================================================
f5 = "frame_5"
y5 = 4000
elements.append(frame(f5, 0, y5, 1600, 900, "05 · 文件存储能力"))
add_slide_header(f5, y5, "PART 04 · 能力拆解 ②", "文件存储（Storage）：海量多媒体大仓库", 5)

# Top Pipeline Banner
elements.append(rect("s5_pipe_bg", 100, y5 + 195, 1400, 240,
                     stroke="#2B8A3E", bg="#F4FBF6", frame_id=f5, stroke_width=2))
elements.append(text("s5_pipe_title", 130, y5 + 215, 600, 35,
                     "🔄 工业级标准协作：文件存储 ＋ 数据库联动机制", font_size=24, color="#2B8A3E", frame_id=f5))

step_w = 380
# Step 1
elements.append(rect("s5_st1", 130, y5 + 265, step_w, 135,
                     stroke="#495057", bg="#FFFFFF", frame_id=f5, stroke_width=2))
elements.append(text("s5_st1_t", 150, y5 + 280, step_w - 40, 30,
                     "1️⃣ 用户前端上传", font_size=22, color="#111827", frame_id=f5))
elements.append(text("s5_st1_d", 150, y5 + 322, step_w - 40, 60,
                     "用户选择照片/视频/附件\n直传腾讯云 COS 存储大仓库", font_size=20, color="#495057", frame_id=f5))

elements.append(arrow_el("s5_arr1", 525, y5 + 332, 60, 0, color="#2B8A3E", width=3, frame_id=f5))

# Step 2
elements.append(rect("s5_st2", 600, y5 + 265, step_w, 135,
                     stroke="#2B8A3E", bg="#EBFBEE", frame_id=f5, stroke_width=2))
elements.append(text("s5_st2_t", 620, y5 + 280, step_w - 40, 30,
                     "2️⃣ 云存储生成访问链接", font_size=22, color="#2B8A3E", frame_id=f5))
elements.append(text("s5_st2_d", 620, y5 + 322, step_w - 40, 60,
                     "COS 返回一条轻量 CDN 外链\n免配桶名，平台自动按应用隔离", font_size=20, color="#2B8A3E", frame_id=f5))

elements.append(arrow_el("s5_arr2", 995, y5 + 332, 60, 0, color="#2B8A3E", width=3, frame_id=f5))

# Step 3
elements.append(rect("s5_st3", 1070, y5 + 265, step_w, 135,
                     stroke="#1971C2", bg="#E7F5FF", frame_id=f5, stroke_width=2))
elements.append(text("s5_st3_t", 1090, y5 + 280, step_w - 40, 30,
                     "3️⃣ 数据库仅记录链接", font_size=22, color="#1864AB", frame_id=f5))
elements.append(text("s5_st3_d", 1090, y5 + 322, step_w - 40, 60,
                     "数据库只存 50 字节的 URL\n体积极小，查询响应极速秒开", font_size=20, color="#1864AB", frame_id=f5))

# Bottom Left: 适合放进存储
elements.append(rect("s5_btm_l", 100, y5 + 465, 680, 300,
                     stroke="#2B8A3E", bg="#FFFFFF", frame_id=f5, stroke_width=2))
elements.extend(make_card_with_text("s5_bh_l", 130, y5 + 490, 280, 50,
                                    "📁 适合放进大仓库的内容", font_size=22,
                                    bg="#EBFBEE", stroke="#2B8A3E", text_color="#2B8A3E", frame_id=f5))
store_assets = [
    "🖼️ 用户相册原图与高清缩略图",
    "👤 用户个人中心自定义头像",
    "📑 PDF 格式说明书、文档附件",
    "🎵 音频播客剪辑、短视频素材"
]
for idx, item in enumerate(store_assets):
    elements.append(text(f"s5_sa_{idx}", 140, y5 + 560 + idx * 48, 600, 32,
                         item, font_size=22, color="#343A40", frame_id=f5))

# Bottom Right: 避坑对比（精炼大字）
elements.append(rect("s5_btm_r", 820, y5 + 465, 680, 300,
                     stroke="#D9480F", bg="#FFF4E6", frame_id=f5, stroke_width=2))
elements.extend(make_card_with_text("s5_bh_r", 850, y5 + 490, 300, 50,
                                    "⚠️ 为什么不能把图片存数据库？", font_size=22,
                                    bg="#FFE8CC", stroke="#D9480F", text_color="#D9480F", frame_id=f5))
cos_benefits = [
    "❌ 错误：5MB 大图转 Base64 塞数据库 ➔ 数据库膨胀卡死",
    "✅ 正确：大图进 COS 存储 ➔ 数据库只存 URL 字符串",
    "🚀 享受红利：无需自己注册买桶，零秘钥安全配置",
    "⚡ 速度保障：腾讯云全国 CDN 节点加速下发，秒开不卡"
]
for idx, item in enumerate(cos_benefits):
    elements.append(text(f"s5_cb_{idx}", 860, y5 + 560 + idx * 48, 600, 32,
                         item, font_size=20, color="#495057", frame_id=f5))


# ==============================================================================
# SLIDE 6: 能力 3 · 身份认证（Authentication）：专属门禁卡
# ==============================================================================
f6 = "frame_6"
y6 = 5000
elements.append(frame(f6, 0, y6, 1600, 900, "06 · 身份认证能力"))
add_slide_header(f6, y6, "PART 04 · 能力拆解 ③", "身份认证（Auth）：专属门禁卡与权限体系", 6)

elements.extend(make_card_with_text("s6_top_bar", 100, y6 + 195, 1400, 60,
                                    "🔑 从「单机自嗨」迈向「商业级多人应用」的关键分水岭",
                                    font_size=26, bg="#F3F0FF", stroke="#7048E8", text_color="#5F3DC4",
                                    frame_id=f6, stroke_width=2))

elements.append(rect("s6_box_l", 100, y6 + 285, 680, 400,
                     stroke="#ADB5BD", bg="#F8F9FA", frame_id=f6, stroke_width=2))
elements.extend(make_card_with_text("s6_badge_l", 135, y6 + 315, 280, 52,
                                    "❌ 传统手写鉴权的翻车坑", font_size=24,
                                    bg="#E9ECEF", stroke="#868E96", text_color="#495057", frame_id=f6))

auth_pains = [
    "• 密码明文存储：极易造成严重用户数据泄露",
    "• 越权漏洞：改一下网页链接就能偷看别人的私密日记",
    "• 登录态丢失：刷新网页或关闭浏览器就频繁掉线",
    "• 短信验证码对接：繁琐申请、模板审核、充值耗时"
]
for idx, t in enumerate(auth_pains):
    elements.append(text(f"s6_ap_{idx}", 140, y6 + 395 + idx * 65, 600, 34,
                         t, font_size=22, color="#C92A2A", frame_id=f6))

elements.append(rect("s6_box_r", 820, y6 + 285, 680, 400,
                     stroke="#7048E8", bg="#FFFFFF", frame_id=f6, stroke_width=2))
elements.extend(make_card_with_text("s6_badge_r", 855, y6 + 315, 300, 52,
                                    "✨ WorkBuddy 内置身份认证", font_size=24,
                                    bg="#F3F0FF", stroke="#7048E8", text_color="#5F3DC4", frame_id=f6))

auth_wins = [
    "✔ 开箱即用 UI：账号密码与验证码登录组件原生集成",
    "✔ 天然多租户隔离：数据表自动绑定用户 ID，仅见自己的数据",
    "✔ 会话全自动托管：关掉浏览器重开依然保持登录",
    "✔ 灵活权限划分：一键区分普通用户与管理员后台"
]
for idx, t in enumerate(auth_wins):
    elements.append(text(f"s6_aw_{idx}", 860, y6 + 395 + idx * 65, 600, 34,
                         t, font_size=22, color="#5F3DC4", frame_id=f6))

elements.append(rect("s6_bot_box", 100, y6 + 710, 1400, 85,
                     stroke="#2B8A3E", bg="#EBFBEE", frame_id=f6, stroke_width=2))
elements.append(text("s6_bot_txt", 140, y6 + 735, 1320, 40,
                     "🔑 总结：不需要写一行后端鉴权代码，立刻拥有「张三绝对看不到李四日记」的安全体系！",
                     font_size=24, color="#2B8A3E", frame_id=f6))


# ==============================================================================
# SLIDE 7: 能力 4 · 数据统计（Analytics）：驾驶舱仪表盘
# ==============================================================================
f7 = "frame_7"
y7 = 6000
elements.append(frame(f7, 0, y7, 1600, 900, "07 · 数据统计能力"))
add_slide_header(f7, y7, "PART 04 · 能力拆解 ④", "数据统计（Analytics）：驾驶舱仪表盘", 7)

elements.extend(make_card_with_text("s7_top_bar", 100, y7 + 195, 1400, 60,
                                    "拒绝「黑盒上线」· 零代码埋点，让应用的每一次访问与资源消耗清晰可见",
                                    font_size=26, bg="#FFF4E6", stroke="#D9480F", text_color="#D9480F",
                                    frame_id=f7, stroke_width=2))

card_w = 445
card_gap = 32

metrics = [
    {
        "icon": "📈", "title": "流量与活跃看板", "sub": "Traffic & Retention",
        "stroke": "#1971C2", "bg": "#E7F5FF", "color": "#1864AB",
        "items": [
            "✔ PV (页面浏览量)：统计打开总次数",
            "✔ UV (独立访客数)：真正有多少人使用",
            "✔ 活跃高峰趋势：发现用户的访问规律"
        ]
    },
    {
        "icon": "💾", "title": "存储与资源监控", "sub": "Storage Usage",
        "stroke": "#2B8A3E", "bg": "#EBFBEE", "color": "#2B8A3E",
        "items": [
            "✔ 数据库记录总数：数据量增长走势",
            "✔ COS 文件占用量：相册素材空间监控",
            "✔ 超限预警：提前掌控容量，保障系统稳定"
        ]
    },
    {
        "icon": "⚡", "title": "API 与服务健康", "sub": "Service Health",
        "stroke": "#7048E8", "bg": "#F3F0FF", "color": "#5F3DC4",
        "items": [
            "✔ 接口请求总量：掌握每日云服务负载",
            "✔ 调用成功率/报错：第一时间捕获 BUG",
            "✔ 大模型消耗：实时追踪 AI 接口调用量"
        ]
    }
]

for idx, m in enumerate(metrics):
    mx = 100 + idx * (card_w + card_gap)
    elements.append(rect(f"s7_mc_{idx}", mx, y7 + 285, card_w, 400,
                         stroke=m["stroke"], bg="#FFFFFF", frame_id=f7, stroke_width=2))
    elements.extend(make_card_with_text(f"s7_mh_{idx}", mx + 20, y7 + 310, card_w - 40, 65,
                                        f"{m['icon']}  {m['title']}", font_size=26,
                                        bg=m["bg"], stroke=m["stroke"], text_color=m["color"],
                                        frame_id=f7))
    elements.append(text(f"s7_ms_{idx}", mx + 20, y7 + 385, card_w - 40, 25,
                         m["sub"], font_size=18, color="#868E96", align="center", frame_id=f7))
    elements.append(line_el(f"s7_ml_{idx}", mx + 30, y7 + 420, card_w - 60, 0,
                            color=m["bg"], width=2, frame_id=f7))
    for item_idx, it_t in enumerate(m["items"]):
        iy = y7 + 445 + item_idx * 70
        elements.append(text(f"s7_it_{idx}_{item_idx}", mx + 25, iy, card_w - 50, 45,
                             it_t, font_size=21, color="#212529", frame_id=f7))

elements.append(rect("s7_bot_box", 100, y7 + 715, 1400, 80,
                     stroke="#495057", bg="#F8F9FA", frame_id=f7, stroke_width=1.5))
elements.append(text("s7_bot_txt", 140, y7 + 738, 1320, 35,
                     "🎯 业务闭环：用数据说话，根据真实用户行为迭代下一代功能！",
                     font_size=23, color="#212529", frame_id=f7))


# ==============================================================================
# SLIDE 8: 能力 5 · 内置大模型能力：外脑智囊顾问
# ==============================================================================
f8 = "frame_8"
y8 = 7000
elements.append(frame(f8, 0, y8, 1600, 900, "08 · 内置大模型能力"))
add_slide_header(f8, y8, "PART 04 · 能力拆解 ⑤", "内置大模型：免申请 Key 零门槛调 AI", 8)

elements.extend(make_card_with_text("s8_top_bar", 100, y8 + 195, 1400, 60,
                                    "开箱即调 · 零配置 API Key · 后端安全代理 · 零门槛为应用注入 AI 智商",
                                    font_size=26, bg="#FFF5F5", stroke="#C92A2A", text_color="#C92A2A",
                                    frame_id=f8, stroke_width=2))

elements.append(rect("s8_box_l", 100, y8 + 285, 680, 330,
                     stroke="#ADB5BD", bg="#F8F9FA", frame_id=f8, stroke_width=2))
elements.extend(make_card_with_text("s8_bh_l", 135, y8 + 310, 280, 50,
                                    "❌ 传统接入 AI 的痛点", font_size=22,
                                    bg="#E9ECEF", stroke="#868E96", text_color="#495057", frame_id=f8))

ai_pains = [
    "• 门槛极高：去各模型平台绑卡充值、申请 API Key",
    "• 盗刷风险：Key 写在前端极易被爬虫秒级偷走",
    "• 架构繁重：必须自建中转服务做安全反向代理"
]
for idx, t in enumerate(ai_pains):
    elements.append(text(f"s8_pt_{idx}", 140, y8 + 380 + idx * 65, 600, 32,
                         t, font_size=22, color="#C92A2A", frame_id=f8))

elements.append(rect("s8_box_r", 820, y8 + 285, 680, 330,
                     stroke="#C92A2A", bg="#FFF5F5", frame_id=f8, stroke_width=2))
elements.extend(make_card_with_text("s8_bh_r", 855, y8 + 310, 280, 50,
                                    "✨ WorkBuddy 解决方案", font_size=22,
                                    bg="#FFE3E3", stroke="#C92A2A", text_color="#C92A2A", frame_id=f8))

ai_wins = [
    "✔ 免单独开通 Key：内置主流模型开箱即用",
    "✔ 原生后端安全代理：客户端零密钥暴露，绝不泄露",
    "✔ 自然语言调用：对 AI 说“点击按钮用 AI 总结”即可交付"
]
for idx, t in enumerate(ai_wins):
    elements.append(text(f"s8_wt_{idx}", 860, y8 + 380 + idx * 65, 600, 32,
                         t, font_size=22, color="#C92A2A", frame_id=f8))

# Bottom Grid: 三大落地应用场景
elements.append(rect("s8_bot_grid", 100, y8 + 640, 1400, 160,
                     stroke="#7048E8", bg="#F3F0FF", frame_id=f8, stroke_width=2))
elements.append(text("s8_bot_tag", 140, y8 + 660, 300, 30,
                     "🚀 典型 AI 实战落地场景", font_size=22, color="#7048E8", frame_id=f8))

cases = [
    ("🤖 智能对话助手", "专属知识库客服、答疑陪伴机器人"),
    ("📝 文本生成与提炼", "长文章自动提取摘要、文案一键排版"),
    ("🏷️ 智能分析与打标", "根据上传内容自动打标、语义检索分类")
]
sc_w = 410
for idx, (ct, cd) in enumerate(cases):
    cx = 140 + idx * (sc_w + 40)
    elements.append(text(f"s8_cs_t_{idx}", cx, y8 + 700, sc_w, 32,
                         ct, font_size=24, color="#5F3DC4", frame_id=f8))
    elements.append(text(f"s8_cs_d_{idx}", cx, y8 + 738, sc_w, 38,
                         cd, font_size=19, color="#495057", frame_id=f8))


# ==============================================================================
# Save JSON
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

output_path = "/Users/daipeng/Workspace/excalidraw-ppt/workbuddy-cloud-slides/workbuddy-cloud-slides.excalidraw"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)

print(f"✅ Successfully regenerated 8 clean slides with {len(elements)} elements!")
