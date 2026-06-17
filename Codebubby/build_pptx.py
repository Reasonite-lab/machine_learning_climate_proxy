#!/usr/bin/env python3
"""Build Nature-style Chinese PPTX from leaf physiognomy ML manuscript."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

OUTDIR = "/Users/xubk/Desktop/机器学习古气候计/Codebubby"
FIGDIR = OUTDIR
ASSETDIR = os.path.join(OUTDIR, "output", "assets", "figures")

# ── Colour palette (Nature-inspired, restrained) ──
CLR_DARK   = RGBColor(0x1A, 0x1A, 0x2E)  # deep navy
CLR_BODY   = RGBColor(0x2D, 0x2D, 0x2D)
CLR_ACCENT = RGBColor(0x2B, 0x5C, 0x8A)  # blue-grey
CLR_BLUE   = RGBColor(0x24, 0x75, 0xA0)
CLR_RED    = RGBColor(0xC0, 0x39, 0x2B)
CLR_GREEN  = RGBColor(0x27, 0xAE, 0x60)
CLR_GREY   = RGBColor(0x88, 0x88, 0x88)
CLR_LIGHT  = RGBColor(0xF5, 0xF5, 0xF5)
CLR_WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

# ── Helper functions ──
def add_blank_slide():
    layout = prs.slide_layouts[6]  # blank
    return prs.slides.add_slide(layout)

def add_textbox(slide, left, top, width, height, text="", font_size=14,
                bold=False, color=CLR_BODY, align=PP_ALIGN.LEFT,
                font_name="Microsoft YaHei", anchor=MSO_ANCHOR.TOP):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    txBox.text_frame.word_wrap = True
    txBox.text_frame.auto_size = None
    tf = txBox.text_frame
    tf.paragraphs[0].alignment = align
    if text:
        run = tf.paragraphs[0].add_run()
        run.text = text
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = font_name
    return txBox

def add_labeled_textbox(slide, left, top, width, height, label, value,
                        label_size=10, value_size=20, color=CLR_BODY):
    """Compact label:value pair."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    # label
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = label
    r.font.size = Pt(label_size)
    r.font.color.rgb = CLR_GREY
    r.font.name = "Microsoft YaHei"
    # value
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.LEFT
    r2 = p2.add_run()
    r2.text = value
    r2.font.size = Pt(value_size)
    r2.font.bold = True
    r2.font.color.rgb = color
    r2.font.name = "Arial"
    return txBox

def add_body(slide, left, top, width, height, bullets, font_size=13, color=CLR_BODY):
    """Add bulleted body text."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, txt in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(6)
        p.line_spacing = Pt(18)
        r = p.add_run()
        r.text = txt
        r.font.size = Pt(font_size)
        r.font.color.rgb = color
        r.font.name = "Microsoft YaHei"
    return txBox

def add_speaker_note(slide, text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = text

def add_line(slide, left, top, width, color=CLR_ACCENT, thickness=1.5):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Pt(thickness)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_rect(slide, left, top, width, height, fill_color=CLR_LIGHT, border_color=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    if fill_color is not None:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(0.5)
    else:
        shape.line.fill.background()
    return shape

def add_slide_number(slide, num):
    add_textbox(slide, 12.5, 7.05, 0.6, 0.3, str(num),
                font_size=9, color=CLR_GREY, align=PP_ALIGN.RIGHT)

def add_title(slide, text, top=0.3):
    add_line(slide, 0.5, top + 0.72, 2.0, CLR_ACCENT, 2.5)
    add_textbox(slide, 0.5, top, 12.0, 0.75, text, font_size=26, bold=True,
                color=CLR_DARK)
    return top + 1.2

def add_source(slide, text, top=6.9, left=0.5, width=5.0):
    add_textbox(slide, left, top, width, 0.3, text,
                font_size=7, color=CLR_GREY, align=PP_ALIGN.LEFT)

def add_figure(slide, filename, left, top, width, height=None):
    path = os.path.join(FIGDIR, filename)
    if not os.path.exists(path):
        add_textbox(slide, left, top, 3, 0.5, f"[{filename} 不存在]", font_size=10, color=CLR_RED)
        return None
    if height is None:
        height = width * 0.65
    return slide.shapes.add_picture(path, Inches(left), Inches(top),
                                     Inches(width), Inches(height))

# ================================================================
# SLIDE 1 — TITLE PAGE
# ================================================================
s = add_blank_slide()
# Dark top band
add_rect(s, 0, 0, 13.333, 3.8, CLR_DARK)
add_textbox(s, 0.8, 0.5, 11.5, 0.35, "Climate of the Past  ·  学术报告",
            font_size=11, color=CLR_GREY, align=PP_ALIGN.LEFT)
add_textbox(s, 0.8, 1.2, 11.5, 1.0,
            "叶相特征集成机器学习\n古气候重建",
            font_size=38, bold=True, color=CLR_WHITE)
add_textbox(s, 0.8, 2.45, 11.5, 0.6,
            "—— 两阶段温度感知框架与热力学气候目标",
            font_size=18, color=CLR_WHITE)
# Bottom meta
add_textbox(s, 0.8, 5.0, 5.0, 0.3, "目标期刊：Climate of the Past (CP)",
            font_size=11, color=CLR_GREY)
add_textbox(s, 0.8, 5.4, 5.0, 0.3, "论文类型：Research Article  ·  2026",
            font_size=11, color=CLR_GREY)
# Key numbers band
add_rect(s, 8.5, 4.8, 4.2, 2.0, fill_color=None, border_color=CLR_GREY)
add_labeled_textbox(s, 8.8, 4.9, 1.8, 0.7, "现代训练集", "393 样本", 8, 16, CLR_BODY)
add_labeled_textbox(s, 10.8, 4.9, 1.8, 0.7, "化石验证集", "71 组合", 8, 16, CLR_BODY)
add_labeled_textbox(s, 8.8, 5.55, 1.8, 0.7, "叶片性状", "31 项", 8, 16, CLR_BODY)
add_labeled_textbox(s, 10.8, 5.55, 1.8, 0.7, "气候变量", "7 类", 8, 16, CLR_BODY)
add_labeled_textbox(s, 8.8, 6.2, 3.8, 0.7, "最佳性能", "CMMT R² = 0.802", 8, 16, CLR_GREEN)
add_speaker_note(s, "标题页：介绍论文基本信息。本文提出基于31项叶相特征的集成机器学习框架，采用两阶段温度感知架构，重建7个气候变量。训练集覆盖393个现代植物群落样本，验证集包含71个化石叶片组合。")
add_slide_number(s, 1)

# ================================================================
# SLIDE 2 — BACKGROUND (claim-led)
# ================================================================
s = add_blank_slide()
y = add_title(s, "研究背景：传统古气候重建方法的瓶颈")
add_body(s, 0.5, y, 7.0, 3.5, [
    "● 叶相特征是成功的陆地古气候代用指标 (Wolfe, 1979; Wilf, 1997)",
    "● CLAMP / LMA / DLP 等主流方法依赖线性统计（CCA / 线性回归）",
    "● 无法捕捉叶相—气候间的非线性关系 (Wright et al., 2017)",
    "● 目标变量局限于温度与降水，缺失热力学水分-能量参数",
    "● 化石训练集地理聚类 → 空间外推至新气候区时可靠性存疑",
], font_size=14)
# Right side: three limitation cards
card_x = 7.8
card_w = 5.0
cards = [
    ("01  线性假设限制", "CCA/线性回归无法建模复杂非线性响应", CLR_RED),
    ("02  变量覆盖不足", "缺少比湿(SH)、焓值(ENTHAL)等热力学目标", CLR_ACCENT),
    ("03  空间外推风险", "地理聚类数据 → 对新气候区泛化能力不足", CLR_BLUE),
]
for i, (title, desc, clr) in enumerate(cards):
    cy = y + i * 1.35
    add_rect(s, card_x, cy, card_w, 1.1, CLR_LIGHT)
    add_line(s, card_x, cy, card_w, clr, 3)
    add_textbox(s, card_x + 0.2, cy + 0.15, card_w - 0.4, 0.35, title,
                font_size=12, bold=True, color=clr)
    add_textbox(s, card_x + 0.2, cy + 0.55, card_w - 0.4, 0.45, desc,
                font_size=10, color=CLR_BODY)
add_speaker_note(s, "介绍研究背景。传统方法包括CLAMP（叶相-气候多元分析）、LMA（叶缘分析）和DLP（数字叶相学），它们主要依赖线性统计方法，且目标变量有限。三个核心瓶颈：线性假设、变量覆盖不足、空间外推能力弱。")
add_source(s, "References: Wolfe 1979, 1993; Wilf 1997; Peppe et al. 2011, 2024; Wright et al. 2017; Spicer et al. 2004", 7.0)
add_slide_number(s, 2)

# ================================================================
# SLIDE 3 — CORE QUESTIONS (claim-led)
# ================================================================
s = add_blank_slide()
y = add_title(s, "核心科学问题：三个挑战")
add_body(s, 0.5, y, 12.5, 5.0, [
    "挑战 1｜非线性建模",
    "   → RF / XGBoost / GBDT 集成模型能否优于传统线性方法，捕捉叶相—气候间的复杂非线性关系？",
    "",
    "挑战 2｜变量扩展",
    "   → 能否通过两阶段温度感知架构，首次从叶相特征中约束大气水分与能量含量（RH, SH, ENTHAL）？",
    "",
    "挑战 3｜空间泛化",
    "   → 严格的10折空间交叉验证下，模型能否可靠迁移至跨洲际化石组合（亚洲65 + 欧洲4 + 北美2）？",
], font_size=14)
# Right summary box
add_rect(s, 9.0, y, 3.8, 2.5, CLR_DARK)
add_textbox(s, 9.3, y + 0.2, 3.2, 2.0,
            "研究目标\n\n以 31 项叶相性状\n+ 393 现代样本\n→ 同时重建 7 个气候变量\n→ 量化不确定性",
            font_size=13, bold=False, color=CLR_WHITE, align=PP_ALIGN.LEFT)
add_speaker_note(s, "论文围绕三个具体挑战展开：(1) 非线性建模——集成ML能否超越CCA等线性方法；(2) 变量扩展——首次尝试从叶相重建比湿和焓值等热力学参数；(3) 空间泛化——严格空间交叉验证确保化石迁移可靠性。")
add_slide_number(s, 3)

# ================================================================
# SLIDE 4 — ARCHITECTURE OVERVIEW (process-wide)
# ================================================================
s = add_blank_slide()
y = add_title(s, "方法总览：两阶段集成学习框架")
# Process flow
stages = [
    ("31 叶相性状", "齿型 7项\n叶级 9项\n叶形 15项", CLR_BODY),
    ("QuantileTransformer\n归一化", "映射至标准正态\n稳健于异常值", CLR_ACCENT),
    ("阶段1：温度预测", "MAT / WMMT\nCMMT / GROWSEAS\n加权集成 (RF+XGB+GBDT+SVR)", CLR_BLUE),
    ("阶段2：水分-能量预测", "35维特征\n(31 性状 + 4 预测温度)\nRH / SH / ENTHAL", CLR_GREEN),
    ("自适应融合", "α = min(0.5, max(0.1,\n2×(CVₑ − CV_b)))\n防误差传播", CLR_RED),
]
box_w = 2.2
gap = 0.4
start_x = (13.333 - (len(stages) * box_w + (len(stages) - 1) * gap)) / 2
for i, (title, desc, clr) in enumerate(stages):
    cx = start_x + i * (box_w + gap)
    cy = y + 0.3
    add_rect(s, cx, cy, box_w, 2.6, CLR_LIGHT, clr)
    add_line(s, cx, cy, box_w, clr, 4)
    add_textbox(s, cx + 0.15, cy + 0.2, box_w - 0.3, 0.6, title,
                font_size=11, bold=True, color=clr, align=PP_ALIGN.CENTER)
    add_textbox(s, cx + 0.15, cy + 1.0, box_w - 0.3, 1.4, desc,
                font_size=9, color=CLR_BODY, align=PP_ALIGN.CENTER)
    # Arrow between boxes
    if i < len(stages) - 1:
        ax = cx + box_w
        add_textbox(s, ax, cy + 0.9, gap, 0.4, "→",
                    font_size=18, bold=True, color=CLR_GREY, align=PP_ALIGN.CENTER)

# Bottom metrics
add_line(s, 0.5, y + 3.2, 3.0, CLR_ACCENT, 1.0)
metrics = [
    ("RF 权重", "0.40"), ("XGB 权重", "0.25"), ("GBDT 权重", "0.25"),
    ("SVR 权重", "0.10"), ("10折空间CV", "防信息泄漏")
]
for i, (lab, val) in enumerate(metrics):
    add_labeled_textbox(s, 0.5 + i * 2.5, y + 3.5, 2.3, 0.8, lab, val, 8, 14)

add_speaker_note(s, "框架总览：(1) 31项叶相性状输入 → (2) QuantileTransformer归一化 → (3) 阶段1：RF+XGB+GBDT+SVR加权集成预测4个温度变量 → (4) 阶段2：将预测温度作为辅助特征（35维），预测水分-能量变量 → (5) 自适应融合系数α防止阶段1误差传播。")
add_slide_number(s, 4)

# ================================================================
# SLIDE 5 — DATA (process-wide)
# ================================================================
s = add_blank_slide()
y = add_title(s, "数据集：从现代训练到化石验证")
# Top row: two dataset cards
add_rect(s, 0.5, y, 5.8, 2.5, CLR_LIGHT, CLR_BLUE)
add_rect(s, 6.9, y, 5.8, 2.5, CLR_LIGHT, CLR_GREEN)
# Modern dataset
add_textbox(s, 0.8, y + 0.15, 5.2, 0.35, "现代训练集", font_size=16, bold=True, color=CLR_BLUE)
add_body(s, 0.8, y + 0.6, 5.2, 1.6, [
    "• 393 植物群落样本",
    "• 全球375 + 青藏高原15（高海拔冷适应）",
    "• 31 项叶相性状（比例数据，[0,1]）",
    "• 7 个气候目标变量",
], font_size=12)
# Fossil dataset
add_textbox(s, 7.2, y + 0.15, 5.2, 0.35, "化石验证集", font_size=16, bold=True, color=CLR_GREEN)
add_body(s, 7.2, y + 0.6, 5.2, 1.6, [
    "• 71 化石叶片组合",
    "• 亚洲 65 / 欧洲 4 / 北美 2",
    "• 相同 31 项性状测量",
    "• 用于迁移性能评估",
], font_size=12)
# Trait categories
add_line(s, 0.5, y + 2.8, 3.0, CLR_ACCENT, 1.0)
add_textbox(s, 0.5, y + 3.0, 3.0, 0.4, "31项性状分5大类", font_size=12, bold=True, color=CLR_DARK)
cats = [
    ("齿型 (7)", "有齿/无齿/锯齿\n规则齿/圆齿/锐齿/复齿"),
    ("叶级 (9)", "Raunkiaer-Webb 分类\n纳米叶 → 大叶3级"),
    ("叶尖 (4)", "微凹/圆/锐尖/渐尖"),
    ("叶基 (3)", "心形/圆/锐尖"),
    ("长宽比 (5)", "<1:1 至 >4:1\n5个等级"),
    ("通用叶形 (3)", "倒卵形/椭圆形/卵形"),
]
for i, (title, desc) in enumerate(cats):
    cx = 0.5 + i * 2.14
    add_rect(s, cx, y + 3.4, 1.85, 1.5, CLR_WHITE, CLR_GREY)
    add_textbox(s, cx + 0.1, 0, 1.7, 0.3, title, font_size=10, bold=True, color=CLR_BLUE)
    # Need absolute positioning
    shp = add_textbox(s, cx + 0.1, y + 3.4 + 0.15, 1.7, 0.25, title, font_size=10, bold=True, color=CLR_BLUE)
    add_textbox(s, cx + 0.1, y + 3.4 + 0.45, 1.7, 0.9, desc, font_size=8, color=CLR_BODY)

# Climate targets
add_line(s, 0.5, y + 5.2, 3.0, CLR_RED, 1.0)
add_textbox(s, 0.5, y + 5.35, 12.0, 0.5,
            "7个气候目标：温度变量 (MAT, WMMT, CMMT, GROWSEAS) ｜ 水分-能量变量 (RH, SH, ENTHAL)",
            font_size=11, color=CLR_BODY)

add_speaker_note(s, "数据集介绍：训练集393个样本来自全球植被样方（378）加青藏高原补充（15）；化石验证集71个样品以亚洲为主。31项叶相性状分为5类：齿型7、叶级9、叶尖4、叶基3、长宽比5、通用叶形3。7个气候目标分为温度类和热力学水分-能量类。")
add_slide_number(s, 5)

# ================================================================
# SLIDE 6 — KEY DESIGN 1: Ensemble (comparison)
# ================================================================
s = add_blank_slide()
y = add_title(s, "关键设计 1：四模型加权集成与空间交叉验证")
# Four model cards
models = [
    ("随机森林\nRandom Forest", "500棵树\nmax depth=10\nmin leaf=5", "w = 0.40", CLR_BLUE),
    ("XGBoost", "200轮\nmax depth=4\nlr=0.05", "w = 0.25", CLR_ACCENT),
    ("梯度提升\nGBDT", "200轮\nmax depth=3", "w = 0.25", CLR_GREEN),
    ("支持向量回归\nSVR", "RBF核\nC=1.0, ε=0.1", "w = 0.10", CLR_GREY),
]
card_w = 2.8
gap = 0.35
start_x = 0.5
for i, (name, params, weight, clr) in enumerate(models):
    cx = start_x + i * (card_w + gap)
    add_rect(s, cx, y, card_w, 2.1, CLR_LIGHT, clr)
    add_line(s, cx, y, card_w, clr, 4)
    add_textbox(s, cx + 0.15, y + 0.15, card_w - 0.3, 0.7, name,
                font_size=12, bold=True, color=clr, align=PP_ALIGN.CENTER)
    add_textbox(s, cx + 0.15, y + 0.9, card_w - 0.3, 0.7, params,
                font_size=10, color=CLR_BODY, align=PP_ALIGN.CENTER)
    add_textbox(s, cx + 0.15, y + 1.6, card_w - 0.3, 0.35, weight,
                font_size=14, bold=True, color=clr, align=PP_ALIGN.CENTER)

# CV explanation
add_line(s, 0.5, y + 2.5, 3.0, CLR_RED, 1.5)
add_textbox(s, 0.5, y + 2.6, 11.0, 0.4, "10折空间分层交叉验证 —— 防止地理邻近样本的信息泄漏",
            font_size=13, bold=True, color=CLR_DARK)
add_body(s, 0.5, y + 3.1, 12.0, 2.0, [
    "• 网格搜索优化各模型权重，最小化交叉验证 RMSE",
    "• 每个fold的预测为各模型输出的加权平均",
    "• 评估指标：R²、RMSE（均方根误差）、MAE（平均绝对误差）",
    "• QuantileTransformer 归一化：映射至标准正态分布，稳健于成分数据的异常值与非正态分布",
], font_size=12)
add_speaker_note(s, "四个基模型的关键参数和权重分配。RF权重最高(0.40)，因其在多个变量上表现稳健；SVR权重最低(0.10)，因其对多数变量预测性能差。空间交叉验证是关键设计，防止同一地理区域的样本同时出现在训练集和验证集中。")
add_slide_number(s, 6)

# ================================================================
# SLIDE 7 — KEY DESIGN 2: Two-stage (process-wide)
# ================================================================
s = add_blank_slide()
y = add_title(s, "关键设计 2：两阶段温度感知架构")

# Stage 1 box
add_rect(s, 0.5, y, 5.5, 2.0, CLR_LIGHT, CLR_BLUE)
add_textbox(s, 0.8, y + 0.1, 5.0, 0.35, "阶段 1：温度预测", font_size=14, bold=True, color=CLR_BLUE)
add_body(s, 0.8, y + 0.5, 5.0, 1.3, [
    "输入：31 项叶相性状",
    "输出：MAT, WMMT, CMMT, GROWSEAS",
    "模型：RF+XGB+GBDT+SVR 加权集成",
], font_size=12)

# Arrow
add_textbox(s, 6.0, y + 0.6, 1.5, 0.5, "━━━━━→", font_size=18, bold=True, color=CLR_GREY, align=PP_ALIGN.CENTER)

# Stage 2 box
add_rect(s, 7.3, y, 5.5, 2.0, CLR_LIGHT, CLR_GREEN)
add_textbox(s, 7.6, y + 0.1, 5.0, 0.35, "阶段 2：水分-能量预测", font_size=14, bold=True, color=CLR_GREEN)
add_body(s, 7.6, y + 0.5, 5.0, 1.3, [
    "输入：31 性状 + 4 预测温度 = 35 维",
    "输出：RH, SH, ENTHAL (热力学耦合)",
    "原理：Clausius-Clapeyron 关系",
], font_size=12)

# Adaptive blending explanation
add_line(s, 0.5, y + 2.3, 3.0, CLR_RED, 1.5)
add_textbox(s, 0.5, y + 2.5, 12.0, 0.4, "自适应融合机制 —— 防误差传播",
            font_size=13, bold=True, color=CLR_DARK)
add_rect(s, 0.5, y + 3.0, 12.3, 1.4, CLR_DARK)
add_textbox(s, 0.8, y + 3.15, 11.7, 1.0,
            "α = min(0.5, max(0.1, 2 × (CV增强 − CV基线)))\n\n温度增强提升CV R² → 倾向增强预测 | 温度增强降低CV R² → 回退至仅性状基线",
            font_size=13, color=CLR_WHITE, align=PP_ALIGN.CENTER)

add_speaker_note(s, "两阶段架构的核心创新：(1) 阶段1用31个性状预测温度；(2) 阶段2将预测温度与原始性状拼接，利用Clausius-Clapeyron关系约束水分-能量变量；(3) 自适应融合系数α根据交叉验证性能动态调整，当温度信息有助于预测时使用增强模型，否则回退到基线模型。")
add_slide_number(s, 7)

# ================================================================
# SLIDE 8 — RESULT 1: Temperature (figure-dominant + table)
# ================================================================
s = add_blank_slide()
y = add_title(s, "主要结果 1：温度变量的化石迁移性能")
# Result highlights
add_rect(s, 0.5, y, 3.5, 1.5, CLR_GREEN)
add_rect(s, 0.5, y, 0.15, 1.5, CLR_GREEN)  # make it a solid bar look
add_textbox(s, 0.8, y + 0.1, 3.0, 0.3, "✓ 最佳：CMMT", font_size=12, bold=True, color=CLR_WHITE)
add_textbox(s, 0.8, y + 0.45, 3.0, 0.5, "R² = 0.802\nRMSE = 2.92°C", font_size=16, bold=True, color=CLR_WHITE)

add_rect(s, 0.5, y + 1.7, 3.5, 1.0, CLR_BLUE)
add_rect(s, 0.5, y + 1.7, 0.15, 1.0, CLR_BLUE)
add_textbox(s, 0.8, y + 1.8, 3.0, 0.3, "GROWSEAS R² = 0.608", font_size=12, bold=True, color=CLR_WHITE)
add_textbox(s, 0.8, y + 2.15, 3.0, 0.3, "MAT R² = 0.579", font_size=12, bold=True, color=CLR_WHITE)

add_rect(s, 0.5, y + 2.9, 3.5, 1.0, CLR_RED)
add_rect(s, 0.5, y + 2.9, 0.15, 1.0, CLR_RED)
add_textbox(s, 0.8, y + 3.0, 3.0, 0.3, "✗ 不可用：WMMT", font_size=12, bold=True, color=CLR_WHITE)
add_textbox(s, 0.8, y + 3.35, 3.0, 0.3, "R² = -1.045", font_size=16, bold=True, color=CLR_WHITE)

# Figure 2
add_figure(s, "Fig2_obs_vs_pred.png", 4.3, y, 8.5, 5.0)
add_source(s, "Source: Fig. 2 (Observed vs. Ensemble-Predicted)", left=4.3, top=6.9, width=4.0)

add_speaker_note(s, "温度变量结果：CMMT表现最好(R²=0.802)，与叶齿型与冷季温度的强关联一致；GROWSEAS(R²=0.608)和MAT(R²=0.579)次之；WMMT(R²=-1.045)完全失败，原因是叶片形态主要整合生长季条件，而非单月极端温度。Fig.2展示了4个代表变量的观测vs预测散点图。")
add_slide_number(s, 8)

# ================================================================
# SLIDE 9 — RESULT 2: Moisture-energy (figure-dominant)
# ================================================================
s = add_blank_slide()
y = add_title(s, "主要结果 2：两阶段架构对水分-能量变量的提升")
# Stage comparison
add_rect(s, 0.5, y, 5.8, 1.8, CLR_LIGHT, CLR_RED)
add_textbox(s, 0.8, y + 0.1, 5.2, 0.3, "基线（仅叶相性状）", font_size=12, bold=True, color=CLR_RED)
add_body(s, 0.8, y + 0.5, 5.2, 1.1, [
    "RH  R² ≈ 0        不可预测",
    "SH  R² ≈ 0        无信息",
    "ENTHAL  R² ≈ 0    无信号",
], font_size=12)

add_textbox(s, 6.35, y + 0.5, 1.2, 0.5, "→", font_size=24, bold=True, color=CLR_ACCENT, align=PP_ALIGN.CENTER)

add_rect(s, 7.3, y, 5.5, 1.8, CLR_LIGHT, CLR_GREEN)
add_textbox(s, 7.6, y + 0.1, 5.0, 0.3, "增强（+ 预测温度）", font_size=12, bold=True, color=CLR_GREEN)
add_body(s, 7.6, y + 0.5, 5.0, 1.1, [
    "RH  R² = -0.072   仍不可预测",
    "SH  R² = 0.329    ΔR² = +0.33  △",
    "ENTHAL  R² = 0.459  ΔR² = +0.46  △",
], font_size=12)

# Figure 5
add_figure(s, "Fig5_two_stage_residuals.png", 0.5, y + 2.1, 6.2, 2.7)
add_figure(s, "Fig1_trait_climate_corr.png", 6.9, y + 2.1, 5.9, 2.7)

add_source(s, "Source: Fig. 5 (Two-stage performance & residuals) & Fig. 1 (trait-climate correlations)", 6.9, 0.5, 6.0)
add_speaker_note(s, "两阶段架构的关键发现：(1) RH始终不可预测——它同时受水分含量和温度控制，对局地过程敏感；(2) SH和ENTHAL从几乎为零提升至中等水平(R²=0.329和0.459)，证实了温度信息通过Clausius-Clapeyron关系提供了热力学约束；(3) 这种从叶相到大气水分的信号重建在叶相学文献中尚无先例。")
add_slide_number(s, 9)

# ================================================================
# SLIDE 10 — FEATURE IMPORTANCE (figure-dominant)
# ================================================================
s = add_blank_slide()
y = add_title(s, "特征重要性：叶片齿型占据主导地位")
# Figure 3
add_figure(s, "Fig3_feature_importance.png", 0.3, y, 7.5, 4.0)
# Right side: top features
add_textbox(s, 8.2, y, 4.5, 0.4, "Top 5 最重要性状", font_size=14, bold=True, color=CLR_DARK)
top5 = [
    ("#1  密齿 (Teeth Close)", "25.5%", CLR_RED),
    ("#2  无齿 (No Teeth)", "13.1%", CLR_BLUE),
    ("#3  复齿 (Teeth Compo)", "11.0%", CLR_ACCENT),
    ("#4  中 叶 2 级", "6.5%", CLR_GREEN),
    ("#5  微叶 1 级", "4.4%", CLR_GREY),
]
for i, (name, pct, clr) in enumerate(top5):
    add_rect(s, 8.2, y + 0.6 + i * 0.55, 4.5, 0.45, CLR_LIGHT, clr)
    add_textbox(s, 8.4, y + 0.62 + i * 0.55, 3.0, 0.35, name, font_size=10, bold=True, color=clr)
    add_textbox(s, 11.2, y + 0.62 + i * 0.55, 1.3, 0.35, pct, font_size=12, bold=True, color=clr, align=PP_ALIGN.RIGHT)

add_line(s, 8.2, y + 3.5, 2.0, CLR_ACCENT, 1.0)
add_body(s, 8.2, y + 3.7, 4.5, 1.5, [
    "• 齿型性状贡献 >50% 总重要性",
    "• 与 LMA 方法的生态学原理一致",
    "• 叶级中等级别贡献，叶尖/叶基 <3%",
    "• RF 贡献 40% R²，XGB/GBDT 各 25%",
], font_size=11)

add_source(s, "Source: Fig. 3 (Feature importance & model composition)", left=8.2, top=6.9, width=4.5)
add_speaker_note(s, "特征重要性分析：齿型相关性状占据主导（密齿25.5%、无齿13.1%、复齿11.0%），这一结果与叶片齿型作为温度代用指标的经典认识完全一致。叶尖和叶基性状的重要性最低（<3%），表明这些性状可能更多受系统发育约束，而非气候适应。随机森林贡献了40%的正R²。")
add_slide_number(s, 10)

# ================================================================
# SLIDE 11 — MODEL COMPARISON (comparison)
# ================================================================
s = add_blank_slide()
y = add_title(s, "模型对比：集成 vs. 单一模型")
# Figure 4
add_figure(s, "Fig4_model_comparison.png", 0.3, y, 7.0, 4.5)
# Table 2 summary
add_textbox(s, 7.8, y, 5.0, 0.4, "化石 R² 对比（表2摘要）", font_size=13, bold=True, color=CLR_DARK)
# Simple table visualization with rectangles
headers = ["模型", "MAT", "CMMT", "GROWSEAS", "SH", "ENTHAL"]
data = [
    ["RF", "0.664", "0.769", "0.703", "0.353", "0.562"],
    ["XGBoost", "0.593", "0.802", "0.641", "0.409", "0.510"],
    ["GBDT", "0.598", "0.710", "0.529", "0.376", "0.499"],
    ["SVR", "0.010", "0.426", "-0.024", "0.127", "-0.052"],
    ["Ensemble", "0.579", "0.802", "0.608", "0.329", "0.459"],
]
col_w = [1.2, 0.85, 0.85, 1.05, 0.75, 0.8]
table_x = 7.5
for j, h in enumerate(headers):
    cx = table_x + sum(col_w[:j])
    add_rect(s, cx, y + 0.55, col_w[j], 0.35, CLR_DARK)
    add_textbox(s, cx, y + 0.55, col_w[j], 0.35, h, font_size=8, bold=True, color=CLR_WHITE, align=PP_ALIGN.CENTER)
for i, row in enumerate(data):
    for j, val in enumerate(row):
        cx = table_x + sum(col_w[:j])
        bg = CLR_LIGHT if i == 4 else CLR_WHITE
        add_rect(s, cx, y + 0.9 + i * 0.35, col_w[j], 0.35, bg, CLR_GREY)
        vcolor = CLR_GREEN if (j > 0 and float(val) > 0.5) else (CLR_RED if (j > 0 and float(val) < 0) else CLR_BODY)
        add_textbox(s, cx, y + 0.9 + i * 0.35, col_w[j], 0.35, val,
                    font_size=8, bold=(i==4), color=vcolor, align=PP_ALIGN.CENTER)

add_body(s, 7.5, y + 3.0, 5.0, 2.0, [
    "• 集成并非在每个变量上都最优,",
    "  但提供最均衡的多变量表现",
    "• SVR 在多数变量上 R² < 0",
    "• WMMT & RH 所有模型均失败",
    "  → 弱性状信号，非模型不足",
], font_size=10)
add_source(s, "Source: Fig. 4 & Table 2", left=7.5, top=6.9, width=4.0)
add_speaker_note(s, "模型对比：RF在多数温度变量上略优于集成，但集成提供了最均衡的性能。SVR即使赋权0.10，在SH和ENTHAL的表现仍差。关键发现：WMMT和RH对所有模型R² < 0 → 问题在于性状信号弱，而非模型能力不足。")
add_slide_number(s, 11)

# ================================================================
# SLIDE 12 — COMPARISON WITH CLAMP (discussion)
# ================================================================
s = add_blank_slide()
y = add_title(s, "与CLAMP等传统方法的对比与优势")
# Comparison table
add_textbox(s, 0.5, y, 5.5, 0.35, "性能对比", font_size=14, bold=True, color=CLR_DARK)
comp_headers = ["方法", "MAT R²", "CMMT R²", "变量数", "非线性"]
comp_data = [
    ["CLAMP (CCA)", "0.7–0.8", "0.7–0.8", "3–5", "✗"],
    ["DLP (线性回归)", "0.5–0.7", "—", "2", "✗"],
    ["本研究 (集成ML)", "0.579", "0.802", "7", "✓"],
]
comp_cw = [1.8, 1.1, 1.1, 0.8, 0.7]
for j, h in enumerate(comp_headers):
    cx = 0.5 + sum(comp_cw[:j])
    add_rect(s, cx, y + 0.5, comp_cw[j], 0.35, CLR_DARK)
    add_textbox(s, cx, y + 0.5, comp_cw[j], 0.35, h, font_size=9, bold=True, color=CLR_WHITE, align=PP_ALIGN.CENTER)
for i, row in enumerate(comp_data):
    for j, val in enumerate(row):
        cx = 0.5 + sum(comp_cw[:j])
        bg = CLR_LIGHT if i == 2 else CLR_WHITE
        add_rect(s, cx, y + 0.85 + i * 0.35, comp_cw[j], 0.35, bg, CLR_GREY)
        vc = CLR_GREEN if i == 2 and j > 0 else CLR_BODY
        add_textbox(s, cx, y + 0.85 + i * 0.35, comp_cw[j], 0.35, val,
                    font_size=9, bold=(i==2), color=vc, align=PP_ALIGN.CENTER)

# Key advantages
add_line(s, 0.5, y + 2.2, 2.0, CLR_GREEN, 2.0)
add_textbox(s, 0.5, y + 2.4, 6.0, 0.35, "本研究的三个独特优势", font_size=13, bold=True, color=CLR_GREEN)
advs = [
    ("非线性建模", "捕捉复杂性状—气候关系，不预设函数形式"),
    ("扩展目标变量", "首次从叶相约束 SH 与 ENTHAL（热力学参数）"),
    ("内部一致性", "统一特征集 → 同时预测7变量，满足热力学约束"),
]
for i, (title, desc) in enumerate(advs):
    add_rect(s, 0.5 + i * 2.2, y + 2.9, 2.0, 1.5, CLR_LIGHT, CLR_GREEN)
    add_textbox(s, 0.5 + i * 2.2, y + 2.9, 2.0, 0.35, title, font_size=11, bold=True, color=CLR_DARK, align=PP_ALIGN.CENTER)
    add_textbox(s, 0.5 + i * 2.2, y + 3.3, 2.0, 0.85, desc, font_size=9, color=CLR_BODY, align=PP_ALIGN.CENTER)

# Complement, not replace
add_line(s, 7.5, y + 2.2, 2.0, CLR_ACCENT, 1.5)
add_textbox(s, 7.5, y + 2.4, 5.5, 0.35, "互补而非替代", font_size=13, bold=True, color=CLR_ACCENT)
add_body(s, 7.5, y + 2.9, 5.3, 2.5, [
    "• 为同一化石组合提供独立重建",
    "• 可交叉验证 CLAMP 估计结果",
    "• 预测 CLAMP 未覆盖的气候变量",
    "• 所有代码、模型、预测结果开源",
], font_size=12)
add_speaker_note(s, "对比分析：(1) CMMT R²=0.802达到或超过CLAMP报道值；(2) MAT R²=0.579略低于CLAMP，可能因为化石数据地理多样性大（含高海拔青藏高原样点）；(3) 额外预测了GROWSEAS和热力学变量。本研究框架旨在补充而非替代CLAMP。")
add_slide_number(s, 12)

# ================================================================
# SLIDE 13 — LIMITATIONS (discussion)
# ================================================================
s = add_blank_slide()
y = add_title(s, "局限性与未来方向")
lims = [
    ("地理偏差", "化石验证集以亚洲为主 (65/71)，\n欧美代表性不足 → 降低全球泛化信心", CLR_RED),
    ("信号弱变量", "WMMT (R²=-1.045) 和 RH (R²=-0.072)\n所有模型均失败 → 核心性状信号缺失", CLR_ACCENT),
    ("误差传播", "两阶段架构继承阶段1温度预测误差，\n自适应α无法完全纠正系统性偏差", CLR_ACCENT),
    ("训练集规模", "393样本对ML而言偏小，\n缺少寒带/热带干旱/地中海灌丛数据", CLR_BLUE),
]
for i, (title, desc, clr) in enumerate(lims):
    lx = 0.5 + i * 3.2
    add_rect(s, lx, y, 2.9, 2.2, CLR_LIGHT, clr)
    add_line(s, lx, y, 2.9, clr, 3)
    add_textbox(s, lx + 0.15, y + 0.15, 2.6, 0.35, title, font_size=13, bold=True, color=clr)
    add_textbox(s, lx + 0.15, y + 0.6, 2.6, 1.4, desc, font_size=10, color=CLR_BODY)

add_line(s, 0.5, y + 2.5, 3.0, CLR_GREEN, 2.0)
add_textbox(s, 0.5, y + 2.7, 12.0, 0.4, "未来改进方向", font_size=14, bold=True, color=CLR_GREEN)
add_body(s, 0.5, y + 3.2, 12.0, 2.5, [
    "• 扩展化石组合的地理覆盖（非亚洲地区）→ 增强泛化能力",
    "• 增加叶脉密度、角质层特征等新性状 → 改进 WMMT 预测",
    "• 替代架构：多任务学习共享特征表示 / 物理信息神经网络嵌入 Clausius-Clapeyron 约束 → 提升水分-能量预测",
    "• 扩充训练数据：纳入寒带森林、热带干旱林、地中海灌丛等欠代表生物群系 → 覆盖全气候空间",
], font_size=12)
add_speaker_note(s, "四个关键局限：(1) 化石地理偏差；(2) WMMT和RH的信号弱；(3) 两阶段误差传播；(4) 训练数据量偏小。未来方向：扩展化石覆盖、增加新性状类型、采用物理信息神经网络、扩充训练集覆盖不够的生物群系。")
add_slide_number(s, 13)

# ================================================================
# SLIDE 14 — SUMMARY (claim-led)
# ================================================================
s = add_blank_slide()
add_rect(s, 0, 0, 13.333, 3.0, CLR_DARK)
add_textbox(s, 0.8, 0.5, 11.5, 0.6,
            "总结与贡献",
            font_size=32, bold=True, color=CLR_WHITE)
add_textbox(s, 0.8, 1.4, 11.5, 0.8,
            "叶相特征集成机器学习古气候重建 —— 两阶段温度感知框架",
            font_size=18, color=CLR_WHITE)

# Three contribution cards
add_body(s, 0.8, 3.5, 11.5, 3.5, [
    "1  非线性集成框架 —— RF + XGBoost + GBDT + SVR 加权集成，以统一特征集同时预测7个气候变量，",
    "   CMMT R² = 0.802，GROWSEAS R² = 0.608，MAT R² = 0.579，性能达到或超过 CLAMP",
    "",
    "2  两阶段温度感知架构 —— 首次从叶相特征部分重建大气水分与能量含量",
    "   SH R² = 0.329 (Δ+0.33)，ENTHAL R² = 0.459 (Δ+0.46)，填补了叶相学文献空白",
    "",
    "3  开源可复现 —— 所有代码、训练模型、化石预测结果已作为补充材料提供",
    "   面向：古气候研究者可交叉验证 CLAMP 估计、获取 CLAMP 未覆盖的新变量预测",
], font_size=12)
add_line(s, 0.8, 6.2, 2.0, CLR_GREEN, 2.5)
add_textbox(s, 0.8, 6.4, 5.0, 0.35, "谢谢！", font_size=16, bold=True, color=CLR_DARK)
add_speaker_note(s, "总结：(1) 31项叶相性状+集成ML可可靠重建3个温度变量(CMMT最佳)；(2) 两阶段架构首次从叶相约束了比湿和焓值——这在叶相学文献中无先例；(3) 目标不是替代CLAMP，而是提供能交叉验证和扩展变量覆盖的互补工具。")
add_slide_number(s, 14)

# ── SAVE ──
output_path = os.path.join(OUTDIR, "output", "final_presentation_cn.pptx")
prs.save(output_path)
print(f"✅ PPTX saved: {output_path}")
print(f"   Slides: {len(prs.slides)}")
print(f"   Figures embedded: Fig1-5")
