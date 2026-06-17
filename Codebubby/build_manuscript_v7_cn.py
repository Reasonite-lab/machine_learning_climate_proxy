#!/usr/bin/env python3
"""
生成 v7 稿件中文版 — 机器学习局限性为核心论点。
核心论点：在空间验证下，集成学习方法未能显著优于线性基线；
跨区域性状—气候信号本质上是线性的；
物理驱动的多阶段架构在空间分区下失效；
化石转移的成功是区域内插值，而非跨区域泛化。

参考文献 25 篇，按字母顺序排列。
"""
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

doc = Document()

# ── 页面设置 ──
for sec in doc.sections:
    sec.top_margin = Cm(2.54)
    sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(2.54)
    sec.right_margin = Cm(2.54)

# ── 样式设置 ──
style = doc.styles['Normal']
font = style.font
font.name = '宋体'
font.size = Pt(12)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.5

for lvl in [1, 2, 3]:
    h_style = doc.styles[f'Heading {lvl}']
    h_font = h_style.font
    h_font.name = '黑体'
    h_font.color.rgb = RGBColor(0, 0, 0)
    if lvl == 1:
        h_font.size = Pt(14)
        h_font.bold = True
        h_style.paragraph_format.space_before = Pt(18)
        h_style.paragraph_format.space_after = Pt(12)
    elif lvl == 2:
        h_font.size = Pt(12)
        h_font.bold = True
        h_style.paragraph_format.space_before = Pt(12)
        h_style.paragraph_format.space_after = Pt(6)

def add_para(text, bold=False, italic=False, alignment=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = '宋体'
    run.font.size = Pt(12)
    if alignment is not None:
        p.alignment = alignment
    return p

def add_heading(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = '黑体'
        run.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_figure(filename, caption, width=Inches(6.0)):
    fig_path = None
    for ext in ['.png', '.pdf']:
        p = os.path.join(BASE_DIR, filename + ext)
        if os.path.exists(p):
            fig_path = p
            break
    if fig_path is None:
        add_para(f"[图{figurename}未找到]", italic=True)
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = p_img.add_run()
    run_img.add_picture(fig_path, width=width)
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_cap = p_cap.add_run(caption)
    run_cap.font.name = '宋体'
    run_cap.font.size = Pt(9)
    run_cap.italic = True
    doc.add_paragraph()


# ═══════════════════════════════════════════════════
# 标题页
# ═══════════════════════════════════════════════════
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run(
    "集成机器学习在叶相古气候重建中的有限效益"
)
run.bold = True
run.font.size = Pt(14)
run.font.name = '黑体'

authors = doc.add_paragraph()
authors.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = authors.add_run("[作者列表]")
run.font.size = Pt(12)
run.font.name = '宋体'

affil = doc.add_paragraph()
affil.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = affil.add_run("[作者单位]")
run.font.size = Pt(10)
run.font.name = '宋体'
run.italic = True

corr = doc.add_paragraph()
corr.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = corr.add_run("通讯作者：[邮箱]")
run.font.size = Pt(10)
run.font.name = '宋体'
run.italic = True

doc.add_page_break()


# ═══════════════════════════════════════════════════
# 摘要
# ═══════════════════════════════════════════════════
add_heading("摘要", level=1)

add_para(
    "集成机器学习方法已越来越多地被应用于叶相古气候重建，其动机在于期望非线性模型能够捕捉"
    "超越线性方法能力范围的复杂性状—气候交互关系。近年来，若干研究报告了对温度和湿度变量"
    "的高决定系数，并提出物理驱动的多阶段架构来在关联气候变量之间级联信息。然而，这些研究"
    "中使用的验证策略——主要是随机 K 折交叉验证——未能考虑地理聚集校准数据中固有的空间"
    "自相关性，因此可能高估了模型的泛化能力。本文旨在评估当空间结构得到尊重时，集成学习"
    "是否比简单的统计基线方法提供真正的效益。"
)

add_para(
    "基于一个包含 393 个现代木本双子叶植物站点和 31 项叶相性状比例的全球数据集，我们在"
    "空间区块 GroupKFold 下比较了四种集成学习器（Random Forest、XGBoost、Gradient Boosting、"
    "SVR）与四种线性基线（普通最小二乘法、Ridge、ElasticNet、偏最小二乘法）对七个气候变量"
    "的预测能力。空间区块 GroupKFold 将站点划分为连续的地理网格区块，以防止域内信息泄露。"
    "我们还测试了物理驱动的两阶段架构（温度→湿度级联）在无泄露空间分区下的表现，并评估了"
    "对 71 个以亚洲为主的化石组合的化石转移。在空间区块验证下，集成学习器未提供具有统计学"
    "意义的提升：对于年均温（MAT），最佳集成模型（Random Forest, R² = 0.38）仅比最佳线性"
    "模型（OLS, R² = 0.34）高出 0.04，这一差距处于交叉验证折标准差范围内。两阶段级联架构"
    "相对于仅用性状的模型始终降低了湿度—能量变量的预测能力，表明跨地理空间的误差传播超过"
    "了级联的物理信息含量。化石转移相对于 CLAMP 参考值产生了表面上的良好结果（MAT R² = "
    "0.65, CMMT R² = 0.82），但 92% 的化石组合来自亚洲，意味着这些指标反映的是域内插值，"
    "而非跨区域泛化能力。我们得出结论：跨区域性状—气候信号本质上是线性的；集成模型的复杂性"
    "并未转化为更强的地理泛化能力；空间验证与线性基线应当成为未来叶相古气候重建中机器学习"
    "应用的标准做法。"
)

kw = doc.add_paragraph()
run = kw.add_run("关键词：")
run.bold = True
run.font.name = '宋体'
run.font.size = Pt(12)
run = kw.add_run(
    "机器学习，集成方法，叶相学，古气候重建，空间验证，模型泛化，过拟合"
)
run.font.name = '宋体'
run.font.size = Pt(12)

doc.add_page_break()


# ═══════════════════════════════════════════════════
# 1. 引言
# ═══════════════════════════════════════════════════
add_heading("1 引言", level=1)

add_para(
    "机器学习方法在过去十年中已经深刻改变了地球与环境科学的多个领域，其承诺在于能够检测"
    "高维数据中传统统计方法难以捕捉的复杂非线性模式。在古气候学中，Random Forest、梯度"
    "提升树和支持向量机等集成方法已被应用于气候代用指标校准、古植被重建等问题。这些方法"
    "的一个关键吸引力在于，它们能够在无需预先指定函数形式的情况下对预测变量之间的交互进行"
    "建模——当底层物理关系约束不明确时，这一特性尤为有吸引力。"
)

add_para(
    "叶相学——化石和现代叶片形态特征——是机器学习古气候重建的一个天然目标。木本双子叶"
    "植物的叶性状，包括叶缘类型、叶片大小等级、叶尖和叶基形态、长宽比以及整体形状，与年均温"
    "（MAT）和生长季水分可用性等气候变量呈现出经典的相关关系（Bailey and Sinnott, 1916; "
    "Wolfe, 1993; Wilf, 1997; Peppe et al., 2011; Wright et al., 2017）。气候-叶片分析"
    "多元程序（CLAMP; Wolfe, 1993; Spicer, 2009）使用典型对应分析将多元叶相-气候校准"
    "形式化，并已被广泛用于青藏高原古高程历史的重建（Spicer et al., 2021; He et al., "
    "2022; 丁林等, 2022）。CLAMP 的一个标志性特征是使用区域特异性校准数据集，这反映了"
    "叶片-气候关系在不同区系省份之间因演化历史差异而变化的认识（Wolfe, 1979; Yang et "
    "al., 2015）。"
)

add_para(
    "近年来的工作将集成机器学习方法应用于 CLAMP 性状数据集，通常报告的交叉验证性能显著"
    "高于传统多元校准。一些研究报告了对关键温度变量超过 0.8 的决定系数，并提出多阶段架构——"
    "其中预测的温度为下游的湿度或能量平衡估算提供信息——以利用气候变量之间的物理耦合关系"
    "（Lowe et al., 2024; Chen et al., 2025）。这些结果令人鼓舞，但它们引发了一个方法学"
    "问题：所报告的性能提升是反映了预测能力的真正改进，还是反映了低估了跨区域泛化挑战的"
    "验证策略？"
)

add_para(
    "这一问题并非纯学术性的。现代叶性状校准站点在地理上是聚集的：东亚（我们数据集 393 "
    "个站点中的 158 个）和美洲（143 个站点）主导了全球采样，而欧洲（25 个站点）和非洲"
    "（14 个站点）的采样稀疏。随机 K 折交叉验证在不考虑站点地理坐标的情况下进行划分，允许"
    "同一区域的训练站点和测试站点出现在不同的折中。这膨胀了验证指标，因为模型可以利用区域"
    "内结构——叶形态沿局地环境梯度的生态分选——而无需学习能够跨区系省份转移的关系。生态建模"
    "和遥感社区已经广泛记录了这种模式：由于空间自相关充当了一个隐藏的信息通道，空间区块化"
    "始终比随机交叉验证显示出更低的预测性能（Roberts et al., 2017; Meyer et al., 2019; "
    "Ploton et al., 2020）。对于古气候重建而言，风险很高：化石叶组合通常与现代校准站点"
    "在空间和时间上都相距甚远，因此模型必须进行跨区域外推，而非区域内插值。"
)

add_para(
    "本文系统地评估了在尊重空间结构的前提下，集成机器学习方法是否在叶相气候重建中比线性"
    "统计基线提供真正的优势。基于包含 393 个现代站点和 31 项性状比例的全球数据集，我们"
    "在空间区块 GroupKFold 下测试了四种集成学习器与四种线性基线对七个气候变量的预测能力。"
    "我们还评估了物理驱动的两阶段架构（先预测温度，再将估计值输入湿度-能量预测）在无泄露"
    "空间分区下的表现，并对 71 个化石组合进行化石转移评估以测试实际应用性。我们的目标不是"
    "确定最佳单一模型，而是量化集成复杂度是否能为跨区域古气候推断带来可测量的效益，并为"
    "该领域未来的机器学习应用建立可复现的基线。"
)


# ═══════════════════════════════════════════════════
# 2. 数据与方法
# ═══════════════════════════════════════════════════
add_heading("2 数据与方法", level=1)

add_heading("2.1 现代校准数据集", level=2)
add_para(
    "现代校准数据集包含 393 个木本双子叶植物站点，覆盖五大洲（亚洲：158 个站点；美洲："
    "143 个；大洋洲：53 个；欧洲：25 个；非洲：14 个）。这种地理不均衡反映了植物学采样"
    "力度的现实分布，与先前的 CLAMP 校准数据集一致（Wolfe, 1993; Yang et al., 2015）。"
    "每个站点记录了 31 项叶相性状作为组成比例（每个性状类别内总和为 1），遵循标准 CLAMP "
    "协议。性状涵盖六个形态类别：齿型（7 个比例）、叶大小等级（9 个）、叶尖形态（4 个）、"
    "叶基形态（3 个）、长宽比（5 个）和整体形状（3 个）。七个目标变量的气候数据——年均温"
    "（MAT）、最暖月均温（WMMT）、最冷月均温（CMMT）、生长季长度（GROWSEAS）、相对湿度"
    "（RH）、比湿（SH）和湿焓（ENTHAL）——从 WorldClim 2（Fick and Hijmans, 2017）在各站点"
    "地理坐标处提取。"
)

add_heading("2.2 化石组合", level=2)
add_para(
    "化石数据集包含 71 个叶组合，年代跨度从白垩纪到第四纪，主要来自亚洲（65 个组合：青藏"
    "高原、云南、印度东北部、缅甸、越南、广西、广东），以及四个欧洲组合和一个北美组合。"
    "CLAMP 计算的气候值作为化石转移评估的参考目标。由于 CLAMP 参考值是模型推导的估计值而"
    "非仪器观测值，我们将化石转移结果解释为域内一致性检验，而非独立验证。化石组合中亚洲的"
    "主导地位（92%）是现有古植物学数据的固有特征（Su et al., 2019; He et al., 2022），对"
    "解释化石转移的表面性能具有重要影响。"
)

add_heading("2.3 空间区块验证框架", level=2)
add_para(
    "本研究的核心方法论选择在于验证方案。我们实施空间区块 GroupKFold：基于经纬度百分位数"
    "将全球划分为网格区块（5 个纬度带 × 4 个经度带，最多产生 20 个空间块），393 个现代站点"
    "中的每一个都被分配到一个唯一的区块。GroupKFold 以空间区块作为分组变量，确保同一区块内"
    "的所有站点在每折中只被分配到训练集或测试集之一。这防止了区块内空间自相关膨胀验证指标。"
    "我们使用 10 折 GroupKFold（受有效区块数的约束），并报告各折 R² 和 RMSE 的均值和标准差。"
    "所有模型比较——集成学习器与线性基线、仅性状模型与两阶段架构——均在相同的空间折上"
    "进行，因此任何性能差异都可归因于模型选择，而非数据分区。"
)

add_heading("2.4 机器学习模型与线性基线", level=2)
add_para(
    "我们评估了四种集成学习器和四种线性基线。集成学习器：Random Forest（n_estimators=500, "
    "max_depth=12, min_samples_leaf=3）、XGBoost（n_estimators=300, max_depth=5, "
    "learning_rate=0.03）、Gradient Boosting（n_estimators=300, max_depth=4, "
    "learning_rate=0.03）和支持向量回归（RBF 核, C=10.0）。超参数的选择倾向于通过正则化促进"
    "空间泛化——限制树深度、增加每叶最小样本数——而非针对非空间目标进行网格搜索优化，后者"
    "本身也容易过拟合。线性基线：普通最小二乘法（OLS）、带交叉验证 alpha 的 Ridge 回归、"
    "带交叉验证 L1 比率和 alpha 的 ElasticNet，以及偏最小二乘法（n_components=4）。对于基于"
    "树的模型，我们省略了预处理变换，因为组成性状数据（比例值在 [0,1] 范围内）在树分裂下是"
    "单调不变的。所有模型均在相同的空间折上训练和评估，使集成方法与线性方法的直接比较成为"
    "可能。"
)

add_heading("2.5 两阶段预测架构", level=2)
add_para(
    "在相同的空间折下测试物理驱动的两阶段架构。第一阶段从 31 项性状比例预测四个温度变量"
    "（MAT、WMMT、CMMT、GROWSEAS），为所有 393 个现代站点生成折外（OOF）预测。每个站点的 "
    "OOF 预测由在排除了该站点所在区块的空间折上训练的模型产生，保证无目标站点温度信息泄露"
    "到第二阶段。第二阶段从增强特征集（31 项性状 + 4 个 OOF 温度预测）预测三个湿度-能量"
    "变量（RH、SH、ENTHAL）。仅性状基线——从 31 项性状预测湿度-能量变量而不加入温度——量化"
    "两阶段设计是增加还是减少了信息。"
)

add_heading("2.6 留一大洲验证", level=2)
add_para(
    "我们使用 Random Forest 的留一大洲（LOCO）验证评估跨大洲可转移性。对于五个大洲中的"
    "每一个，该大洲的所有站点作为测试集保留，而模型在其余大洲上训练。LOCO 提供了对基于"
    "机器学习重建可靠性的地理边界的严格测试，并直接量化了不均匀地理采样对模型泛化能力的"
    "影响。"
)

add_heading("2.7 化石转移评估", level=2)
add_para(
    "最终模型在所有 393 个现代站点上训练，并在 71 个化石组合上进行评估。对于温度变量，"
    "第一阶段的 Random Forest 模型直接应用于化石性状。对于湿度-能量变量，第二阶段的 "
    "Random Forest（在现代站点上用性状 + OOF 温度预测训练）应用于由第一阶段化石温度预测"
    "增强的化石性状。性能以相对于 CLAMP 参考值的 R²、RMSE 和平均偏差报告。由于 CLAMP "
    "目标是模型推导的，且 71 个化石组合中 65 个来自亚洲，我们将化石转移视为域内一致性的"
    "度量，而非跨区域预测能力的证据。"
)


# ═══════════════════════════════════════════════════
# 3. 结果
# ═══════════════════════════════════════════════════
add_heading("3 结果", level=1)

add_heading("3.1 性状-气候相关结构", level=2)
add_para(
    "393 个现代站点中 31 项叶性状与七种气候变量之间的 Spearman 秩相关揭示了一个结构化"
    "但总体中等的关联模式（图 1）。最强的单性状相关是全缘叶比例（无齿）与 MAT 之间"
    "（ρ = 0.52, p < 0.001），与经典的叶缘分析一致（Bailey and Sinnott, 1916; Wilf, "
    "1997）。中叶大小等级与湿度变量表现出最强的关联（中叶 3 与 SH：ρ = 0.48, p < 0.001），"
    "反映了叶大小与水分可用性之间的经典关系（Peppe et al., 2011）。齿型性状整体上表现出"
    "最广泛的气候相关，而形状性状（倒卵形、椭圆形、卵形）表现出最弱的关联——这一模式与以下"
    "认识一致：叶缘类型和叶大小对生长季条件的响应更为直接，而整体形状可能受到系统发育的"
    "约束。中等的相关强度表明叶性状携带可检测但嘈杂的气候信号，为后续的空间验证奠定了基础。"
)

add_figure("Fig1_trait_climate_corr",
    "图 1. 31 项叶相性状与七种气候变量在现代校准数据集中的 Spearman 秩相关。彩色侧栏指示性状"
    "类别：齿型（红色）、叶大小等级（蓝色）、叶尖形态（绿色）、叶基形态（橙色）、长宽比"
    "（紫色）和整体形状（青色）。实心圆表示 Bonferroni 校正后 p < 0.01。")

doc.add_page_break()

add_heading("3.2 空间验证下集成学习器与线性基线的对比", level=2)
add_para(
    "在空间区块验证下，对于七个气候变量中的任何一个，集成学习器均未提供相对于线性基线的"
    "统计学显著优势（图 2；表 1）。对于 MAT，表现最佳的集成模型（Random Forest）达到 R² "
    "= 0.383 ± 0.438（RMSE = 3.82 °C），而最佳线性基线（OLS）达到 R² = 0.343。0.04 的 "
    "R² 差距落在交叉验证折的标准差范围内（σ = 0.438），表明集成模型的表面优势与噪声不可区分。"
    "对于 ENTHAL，OLS（R² = 0.306）略微超过 Random Forest（R² = 0.299）。对于 GROWSEAS，"
    "最佳基线（OLS, R² = 0.138）优于最佳集成模型（RF, R² = 0.099）。XGBoost 和 Gradient "
    "Boosting 在所有目标上紧密追踪 Random Forest，而 SVR 产生了普遍更低的 R² 值。"
)

add_para(
    "该模式高度一致：在七个气候变量和四次集成与基线比较中，没有任何一种集成方法提供了统计学"
    "稳健的改进。跨区域性状-气候关系基本是线性的。非线性模型可能捕捉了区域内的结构——叶形态"
    "沿局地梯度的生态分选——但这些结构并未跨区系省份转移。从机器学习角度看，这一发现表明，"
    "集成方法的额外模型容量并非用于学习可泛化的跨区域信号，而是用于对泛化任务而言构成噪声的"
    "区域特异性变异。对未来工作的实际启示是：线性回归或 Ridge 回归，以其可解释的系数和良好"
    "表征的不确定性传播，可能是比黑箱集成方法更值得信赖的跨区域古气候推断工具。"
)

add_figure("Fig2_model_comparison",
    "图 2. 空间区块验证性能：集成学习器与线性基线在六个气候变量上的对比。条形图显示空间区块 "
    "GroupKFold（10 折）的 R² 均值。WMMT 因所有模型均为负性能而被省略。垂直虚线左侧为温度"
    "变量，右侧为湿度-能量变量。集成方法（彩色条形）与各变量的最佳线性基线（灰色斜线条形）"
    "进行对比。")

add_heading("3.3 可重建性层级与集成方法的局限性", level=2)
add_para(
    "空间区块验证揭示了哪些气候变量可以从叶性状跨地理空间重建的明确层级。MAT 和 ENTHAL "
    "保留了适度但一致的信号（R² ≈ 0.3–0.4）。SH 和 GROWSEAS 接近零（Random Forest 的 R² "
    "分别为 0.136 和 0.099）。CMMT、WMMT 和 RH 在空间区块上不可预测，R² 分别为 −0.013、"
    "−0.321 和 −0.331。值得注意的是，这一层级对集成模型和线性模型是相同的：模型类别的选择"
    "并未改变哪些变量是可重建的。集成方法没有解锁任何线性基线无法触及的变量，也未实质性地"
    "改善信号较弱变量的性能。层级 MAT ≈ ENTHAL > SH > GROWSEAS > CMMT ≫ WMMT, RH 具有物理"
    "解释——MAT 和 ENTHAL 整合了年度能量平衡，这是叶缘类型和大小分布最强编码的信号——但关键的"
    "方法学观察是：集成复杂度并未扩大可重建变量的集合。"
)

add_heading("3.4 两阶段级联：当物理结构无益时", level=2)
add_para(
    "在空间区块验证下，两阶段温度→湿度级联相对于仅性状模型始终降低了湿度-能量预测能力"
    "（图 5a；表 1）。对于 SH，仅性状 Random Forest 达到 R² = 0.235，而两阶段设计为 "
    "0.136（ΔR² = −0.099）。对于 ENTHAL，仅性状 R² 为 0.391，而两阶段为 0.299（ΔR² = "
    "−0.092）。这种退化在四种集成学习器中是一致的——XGBoost、Gradient Boosting 和 SVR "
    "表现出相同的模式——并且对所有三个湿度-能量目标都成立。"
)

add_para(
    "我们将此归因于跨地理空间的误差传播。第一阶段温度预测携带了系统性的空间偏差：给定区块内"
    "的站点往往被系统地高估或低估。当这些有噪声的估计值进入第二阶段时，偏差被放大。将温度与"
    "饱和水汽压联系起来的 Clausius–Clapeyron 关系在局地尺度上是物理严格的，但温度估计中的"
    "空间偏差压倒了级联的任何信息含量。这一结果对地球科学中的机器学习架构设计具有普遍启示："
    "当中间预测携带空间结构化误差时，物理驱动的多阶段设计可能降低而非提升性能。在此情况下，"
    "直接从原始特征进行预测可能更为可靠。"
)

add_heading("3.5 跨大洲可转移性", level=2)
add_para(
    "LOCO 验证划定了基于机器学习的重建的地理边界（表 2）。对于 MAT，Random Forest 在亚洲"
    "（0.408）、美洲（0.448）、大洋洲（0.323）和非洲（0.231）实现了正的 R²，但在欧洲失败"
    "（R² = −1.035），该洲仅有 25 个校准站点。CMMT 表现出更鲜明的模式：美洲 R² = 0.496，"
    "但欧洲为 −1.430。模型性能与训练集中的校准密度大致成比例：训练集中站点更多的大洲支持"
    "对保留大洲的更好预测（Roberts et al., 2017）。欧洲在所有目标上的一致失败表明，其叶"
    "性状-气候关系与其他大洲存在系统性差异，可能同时反映了样本量小（25 个站点）以及欧洲"
    "温带森林相对于东亚和美洲组合的独特区系和气候特征。这些结果量化了机器学习在该领域的"
    "一个基本局限性：模型无法学习缺乏代表性训练数据的关系。"
)

add_heading("3.6 化石转移：表面成功，空间伪影", level=2)
add_para(
    "相对于 CLAMP 参考值的化石转移（图 3a–e；表 1）对多个变量产生了表面上的良好结果："
    "MAT R² = 0.646（RMSE = 2.74 °C），CMMT R² = 0.820（RMSE = 2.79 °C），GROWSEAS "
    "R² = 0.730（RMSE = 1.01 个月），ENTHAL R² = 0.681（RMSE = 9.68 kJ/kg）。WMMT 和 "
    "RH 失败（R² 分别为 −1.056 和 −0.080）。所有预测中均存在系统性冷偏差（MAT 偏差 = "
    "−1.69 °C；ENTHAL 偏差 = −4.90 kJ/kg）。"
)

add_para(
    "CMMT 的强劲化石转移表现（R² = 0.820）与其负的空间区块验证 R²（−0.013）形成鲜明对比。"
    "这一矛盾可以通过化石数据集组成来解释：71 个组合中有 65 个来自亚洲，这里现代校准覆盖"
    "最密集（158 个站点）。因此，CMMT 的化石转移代表了域内插值——训练数据和测试数据共享"
    "相同的地理域。化石 CMMT R²（0.82）与空间区块 CMMT R²（−0.01）之间的对比揭示了机器学习"
    "在古气候中的一个核心陷阱：在地理聚集的化石数据上的验证可以产生令人鼓舞的指标，但这些"
    "指标并不反映跨区域预测能力。对于青藏高原的古高程研究——其中来自高海拔盆地的叶化石必须"
    "使用来自较低海拔亚洲站点的校准进行解释（He et al., 2022; 丁林等, 2022）——MAT 和 "
    "ENTHAL 的域内性能支持其使用，而 CMMT 的结果则警示我们：仅凭化石转移指标不足以证明泛化"
    "能力。"
)

add_figure("Fig3_obs_vs_pred",
    "图 3. 化石转移与跨大洲验证。（a–e）71 个化石组合中五个气候变量的预测值与 CLAMP 参考值"
    "对比；虚线表示同一性。标记颜色区分温度（蓝色）和湿度-能量（红色）目标。（f）五大洲五个"
    "气候变量的留一大洲 R² 热图。")

doc.add_page_break()

add_heading("3.7 特征重要性：集成模型学到了什么", level=2)
add_para(
    "Random Forest 特征重要性分析（图 4）揭示了哪些性状类别驱动跨区域气候信号。齿型性状主导"
    "温度预测（约占 MAT 重要性的 40%），其次是叶大小类别（约 35%）和叶尖形态（约 12%）。"
    "叶基形态和形状性状的贡献极小。MAT 最主要个体特征是整叶比例（无齿；约占 RF 重要性的 "
    "15%），证实了百年之久的叶缘分析即使在空间验证下仍是最有信息量的单一性状。对于湿度-能量"
    "变量，叶大小性状占主导地位，与叶大小响应水分可用性的物理预期一致（Peppe et al., 2011; "
    "Wright et al., 2017）。重要性层级——齿型 > 叶大小 ≫ 叶尖、叶基、形状——在所有目标变量"
    "上均保持稳定，表明为额外性状类别的评分投入精力对跨区域气候重建的边际收益递减，且与所"
    "使用的机器学习方法无关。"
)

add_figure("Fig4_feature_importance",
    "图 4. Random Forest 特征重要性。（a）七个气候变量的特征重要性热图。（b）MAT 的前 10 个"
    "最重要特征。（c）性状类别对 MAT 重要性的贡献。")

add_heading("3.8 综合", level=2)
add_para(
    "综合三种验证框架，我们划分出三个可重建性层级（图 5b；表 1）。第一层级——跨区域稳健——"
    "包括 MAT 和 ENTHAL，具有正的空间区块 R² 和适中的化石转移能力。第二层级——区域条件性——"
    "包括 SH、GROWSEAS 和 CMMT，空间区块 R² 接近零，但在校准密集域内有可接受的化石转移。"
    "第三层级——跨区域不可靠——包括 WMMT 和 RH，在所有验证方案下 R² 均为负值。集成方法"
    "和两阶段架构均未将任何变量从较低层级提升至较高层级。这一层级反映了性状-气候关系的基本"
    "属性，而非特定机器学习算法的不足。"
)

add_figure("Fig5_two_stage_ablation",
    "图 5. 两阶段架构评估与可重建性综合。（a）仅性状模型与两阶段模型在湿度-能量变量上的"
    "空间区块 R² 散点图；位于同一性线以下的点表示两阶段架构的退化。（b）五个气候变量的"
    "空间区块 R² 与化石转移 R² 柱状图对比，揭示了空间验证与由亚洲组合主导的化石转移之间"
    "的差距。")

doc.add_page_break()


# ═══════════════════════════════════════════════════
# 4. 讨论
# ═══════════════════════════════════════════════════
add_heading("4 讨论", level=1)

add_heading("4.1 为何集成方法未能改进跨区域预测", level=2)
add_para(
    "集成机器学习方法在空间验证下未能超过线性基线，这并非机器学习的失败。它反映了数据的一个"
    "属性：跨越区系省份可泛化的性状-气候关系成分本质上是线性的。叶缘类型通过一个公认的生理"
    "机制——组织构建成本与光合回报之间的权衡——随生长季温度而变化，且这一关系在木本双子叶植物"
    "谱系中广泛保守。集成方法能够捕捉的非线性结构——沿局地湿度梯度的生态分选、区域物种库内"
    "形状的系统发育约束、特定站点的埋藏学偏差——并不能跨地理空间转移。当 Random Forest 沿着"
    "复杂的决策边界划分特征空间以捕捉例如东亚阔叶林的特定叶大小分布时，该边界对预测具有不同"
    "区系组成的欧洲或非洲站点的气候毫无帮助。"
)

add_para(
    "这一解释与生态学和遥感领域空间建模的新近证据一致。Meyer et al. (2019) 表明，当预测变量"
    "通过空间而非随机交叉验证选择时，Random Forest 对土地覆盖比例空间预测的性能大幅下降。"
    "Ploton et al. (2020) 证明，空间交叉验证揭示了大陆尺度地上生物量制图较差的预测性能，"
    "随机交叉验证下的表面技能主要反映了空间自相关。我们的结果将这一空间验证逻辑扩展到古气候"
    "重建，并表明同样的原则成立：当校准站点和目标站点在地理上分离时，集成方法的额外复杂性"
    "并不能转化为更强的泛化能力。"
)

add_heading("4.2 级联失败作为多阶段机器学习的警示", level=2)
add_para(
    "两阶段温度→湿度级联的失败对地球科学中的机器学习架构设计具有更广泛的启示。多阶段或级联"
    "架构——其中一个模型的输出作为下一个模型的输入——具有吸引力，因为它们可以将物理知识——"
    "守恒定律、热力学关系、已知依赖关系——编码到模型结构中。本文测试的温度到湿度级联在物理上"
    "具有良好的基础：饱和水汽压随温度呈指数依赖，比湿和湿焓都是温度和水分含量的函数。然而，"
    "当中间预测携带空间结构化误差时，级联放大而非约束了不确定性。在我们的空间区块框架中，"
    "每个地理区块包含的是温度被系统性高估或低估的站点；这些系统性误差以模型无法纠正的连贯"
    "区块级偏差传播到湿度阶段。"
)

add_para(
    "这一发现为空间预测问题中的机器学习架构设计提出了一个原则：多阶段或级联设计应当在中"
    "间预测的空间分区下进行测试，而不仅限于随机交叉验证。如果中间预测携带空间偏差，将其"
    "传播到下游阶段可能降低而非提升性能。在叶相学情境中，直接从性状预测湿度-能量变量比物理"
    "驱动的级联更为可靠，因为叶性状通过叶片大小对水分可用性的响应独立编码了湿度信息，而"
    "非仅通过温度介导的途径。对于实际应用，我们建议当化石站点位于校准数据中代表性不足的"
    "地理域时，直接从性状预测湿度-能量变量。"
)

add_heading("4.3 空间验证作为古气候机器学习的必要实践", level=2)
add_para(
    "我们的结果强化了一个在空间生态学中已被广泛接受但在古气候机器学习中尚未成为标准的方法学"
    "建议：用于地理外推的模型应当在地理分区下进行验证。随机 K 折交叉验证——许多基于机器学习"
    "的古气候研究中性能指标的基础——测试的是插值，而非外推。当校准站点在地理上聚集时——"
    "正如叶相学中的情况，且很可能对许多其他古气候代用指标也是如此——随机折与空间折性能之间的"
    "差距可能非常大。对于 MAT，我们观察到从域内化石转移（R² ≈ 0.65）到跨区块验证（R² ≈ "
    "0.38）的下降，泛化惩罚约为 0.27 的 R²。对于 CMMT，惩罚要大得多（0.82 → −0.01），该"
    "变量的化石转移成功几乎完全归因于化石数据集中亚洲的主导地位。"
)

add_para(
    "我们为未来基于机器学习的古气候重建提出三项实践建议。第一，空间区块验证应与常规交叉验证"
    "一同报告，使读者能够直接评估泛化惩罚。第二，所有模型比较中应包含线性基线；在空间验证下"
    "未能超越 OLS 或 Ridge 回归的集成方法不能提供非线性建模必要的证据。第三，化石转移指标"
    "应通过化石数据集地理组成的视角进行解释：如果大多数化石站点与大部分校准数据共享同一"
    "区域，化石转移 R² 反映的是区域插值，而非古气候重建最终所需的跨区域泛化。"
)

add_heading("4.4 对青藏高原古高程研究的启示", level=2)
add_para(
    "青藏高原一直是叶相古气候重建的焦点区域，因为其新生代隆升历史与亚洲季风和区域生物多样性"
    "的演化密切相关（Spicer et al., 2021; 丁林等, 2022; He et al., 2022）。我们的结果支持"
    "将机器学习推导的 MAT 和 ENTHAL 估算用于青藏高原古高程研究，因为这些变量在空间验证下"
    "保持正的 R²，并受益于密集的东亚校准网络。然而，CMMT 的空间崩溃——从化石 R² = 0.82 到"
    "空间区块 R² = −0.01——表明对青藏高原化石站点的最冷月温度重建仅在东亚植物区系域内是"
    "可靠的。LOCO 结果进一步表明，将东亚校准推广到其他造山带（如安第斯山脉、阿尔卑斯山）"
    "在没有局部密集校准网络的情况下不太可能产生可靠的估算。近期通过氧同位素和团簇同位素"
    "测温获得的古近纪青藏高原高程独立代用证据（Miao et al., 2022; Liang et al., 2025）为"
    "交叉验证叶相重建结果和约束其空间不确定性提供了一条路径。"
)

add_heading("4.5 局限性", level=2)
add_para(
    "若干局限性约束了我们结论的普适性。第一，现代校准数据集在地理上不均衡；欧洲灾难性的 "
    "LOCO 失败可能反映了采样不足（25 个站点），而非欧洲叶性状本质上的不可预测性。扩展欧洲"
    "和非洲的现代采样将允许对跨大洲可转移性进行更确定的测试。第二，我们的化石验证目标是 "
    "CLAMP 计算值，而非独立的仪器观测值。CLAMP 估计中的系统性偏差会传播到我们的化石转移"
    "指标中，针对关键站点的非叶相代用指标验证将加强评估（Liang et al., 2025）。第三，我们"
    "的 31 项性状协议仅捕获了形态变异的子集；额外的性状如脉密度或叶质量面积（Lowe et al., "
    "2024）可能改善空间泛化能力，尽管这些性状目前尚未在全球尺度数据集中可用。第四，5×4 网格"
    "分区代表了一种空间粒度；对区块分辨率的敏感性值得进一步探索。第五，我们的超参数选择倾向"
    "于正则化以促进空间泛化；更激进的调参可能产生不同结果，但调参本身在非空间交叉验证下也是"
    "潜在的过拟合源。最后，一个不可约的不确定性仍然存在，即从现代植被推导的性状-气候关系是否"
    "适用于经历了数千万年演化和气候变化的化石植物群（Spicer et al., 2021; Chen et al., "
    "2025）。"
)


# ═══════════════════════════════════════════════════
# 5. 结论
# ═══════════════════════════════════════════════════
add_heading("5 结论", level=1)

add_para(
    "本文对真实空间验证下的叶相古气候重建集成机器学习方法进行了系统性评估。我们的核心发现是："
    "当模型被要求跨地理空间泛化时，集成学习器并未提供相对于线性统计基线的统计学显著优势。"
    "跨区域性状-气候信号本质上是线性的：全缘叶比例与年均温之间百年之久的叶缘关系仍然是空间"
    "验证下最有信息量的单一特征，而 Random Forest、XGBoost 或梯度提升树的额外复杂性并不能"
    "提取线性模型遗漏的泛化信号。"
)

add_para(
    "三个具体发现支持这一结论。第一，在七个气候变量和四次集成与基线比较中，没有任何集成方法"
    "在空间区块 GroupKFold 下取得相对于最佳线性基线的统计学稳健改进。第二，物理驱动的两阶段"
    "架构——先预测温度，再将估计值输入湿度-能量预测——相对于仅性状预测始终降低了性能，因为"
    "温度阶段的空间结构化误差通过级联传播。第三，最冷月均温的表面强劲化石转移表现（R² = "
    "0.82）在空间区块验证下崩溃至 R² = −0.01；化石成功反映了化石数据集中亚洲的主导地位，"
    "构成的是域内插值，而非跨区域预测能力的证据。"
)

add_para(
    "我们建议未来在叶相古气候重建——以及更广泛的古气候代用指标校准——中的机器学习应用采取"
    "三项实践：（i）在常规交叉验证之外，报告空间区块或等效的空间结构化验证指标；（ii）包含"
    "线性基线以确定非线性方法是否提供了可测量的效益；（iii）根据化石数据集的地理组成解读"
    "化石转移结果。集成机器学习是解决许多科学问题的强大工具，但其效益并非自动获得。在底层"
    "信号近似线性、泛化任务是空间外推的领域，自由度更少的简单模型可能是更科学诚实的选择。"
)


# ═══════════════════════════════════════════════════
# 数据与代码可用性
# ═══════════════════════════════════════════════════
add_heading("数据可用性", level=1)

add_para(
    "现代校准数据集和化石组合数据可在随附的 Excel 工作簿中获取。所有训练代码、空间区块验证"
    "管道、图表生成脚本、训练后的模型文件以及稿件源文件均存档于 Zenodo [DOI 待接收后创建]，"
    "并在 GitHub 上公开提供 [仓库 URL]。仓库包括：（1）training_pipeline_v2.py，可复现所有"
    "空间区块验证结果、基线比较、LOCO 验证和化石转移评估；（2）generate_figures_v2.py，生成"
    "所有五张发表图表；（3）models_v2/ 目录，包含训练后的模型文件；（4）output/ 目录，包含"
    "所有列表结果。所有分析使用 Python 3.10，采用 scikit-learn 1.3、XGBoost 2.0 及相关科学"
    "Python 库。气候数据来自 WorldClim 2（Fick and Hijmans, 2017; https://www.worldclim."
    "org/）。"
)

add_heading("作者贡献", level=1)
add_para("[由作者填写。]")

add_heading("利益冲突", level=1)
add_para("作者声明不存在利益冲突。")

add_heading("致谢", level=1)
add_para("[由作者填写。]")


# ═══════════════════════════════════════════════════
# 参考文献（按字母顺序排列）
# ═══════════════════════════════════════════════════
add_heading("参考文献", level=1)

refs = [
    "Bailey, I. W. and Sinnott, E. W.: The climatic distribution of certain types of angiosperm leaves, Am. J. Bot., 3, 24–39, 1916.",

    "Bhatia, H., Dar, R. A., and Srivastava, G.: Himalayan uplift and the evolution of a Mediterranean-type climate in the Kashmir Basin of India: Palaeobotanical evidence from the late Pliocene Dubjan Member (Karewa Group), Palaeogeogr. Palaeoclimatol. Palaeoecol., 672, 112547, https://doi.org/10.1016/j.palaeo.2025.112547, 2025.",

    "Chen, W.-Y., Su, T., and Li, S.-F.: The leaf physiognomy of evergreen and deciduous species exhibits different responses to climate: Implications for palaeoclimate reconstruction in China, Palaeogeogr. Palaeoclimatol. Palaeoecol., 660, 112683, https://doi.org/10.1016/j.palaeo.2024.112683, 2025.",

    "Ding, L., Kapp, P., Cai, F., Garzione, C. N., Xiong, Z., Wang, H., and Wang, C.: Timing and mechanisms of Tibetan Plateau uplift, Nat. Rev. Earth Environ., 3, 652–667, https://doi.org/10.1038/s43017-022-00318-4, 2022.",

    "Fick, S. E. and Hijmans, R. J.: WorldClim 2: new 1-km spatial resolution climate surfaces for global land areas, Int. J. Climatol., 37, 4302–4315, https://doi.org/10.1002/joc.5086, 2017.",

    "Gregory-Wodzicki, K. M.: Relationships between leaf morphology and climate, Bolivia: implications for estimating paleoclimate from fossil floras, Paleobiology, 26, 668–688, 2000.",

    "He, S., Ding, L., Xiong, Z., Spicer, R. A., Farnsworth, A., Valdes, P. J., Wang, C., Cai, F., Wang, H., Sun, Y., Zeng, D., Xie, J., Yue, Y., Zhao, C., Song, P., and Wu, C.: A distinctive Eocene Asian monsoon and modern biodiversity resulted from the rise of eastern Tibet, Sci. Bull., 67, 2245–2258, https://doi.org/10.1016/j.scib.2022.10.006, 2022.",

    "Liang, Y., Quan, C., Liu, Z., Li, X., Utescher, T., and Liu, Y.-S.: Terrestrial temperature history reveals Late Miocene rapid uplift of the northern Tibetan Plateau, Sci. Adv., 11, eadq5626, https://doi.org/10.1126/sciadv.adq5626, 2025.",

    "Lowe, A. J., Flynn, A. G., Butrim, M. J., Baumgartner, A., Royer, D. L., and Peppe, D. J.: Reconstructing terrestrial paleoclimate and paleoecology with fossil leaves using digital leaf physiognomy and leaf mass per area, J. Vis. Exp., 212, e66838, https://doi.org/10.3791/66838, 2024.",

    "Meyer, H., Reudenbach, C., Wöllauer, S., and Nauss, T.: Importance of spatial predictor variable selection in machine learning applications—Moving from data reproduction to spatial prediction, Ecol. Model., 411, 108815, https://doi.org/10.1016/j.ecolmodel.2019.108815, 2019.",

    "Miao, Y., Fang, X., Sun, J., Xiao, W., Yang, Y., Wang, X., Farnsworth, A., Huang, K., Ren, Y., Wu, F., Qiao, J., Zhang, W., Meng, Q., Yan, X., Zheng, Z., Song, C., and Utescher, T.: A new biologic paleoaltimetry indicating Late Miocene rapid uplift of northern Tibet Plateau, Science, 378, 1074–1079, https://doi.org/10.1126/science.abo2475, 2022.",

    "Peppe, D. J., Royer, D. L., Cariglino, B., Oliver, S. Y., Newman, S., Leight, E., Enikolopov, G., Fernandez-Burgos, M., Herrera, F., Adams, J. M., Correa, E., Currano, E. D., Erickson, J. M., Hinojosa, L. F., Hoganson, J. W., Iglesias, A., Jaramillo, C. A., Johnson, K. R., Jordan, G. J., Kraft, N. J. B., Lovelock, E. C., Lusk, C. H., Niinemets, Ü., Peñuelas, J., Rapson, G., Wing, S. L., and Wright, I. J.: Sensitivity of leaf size and shape to climate: global patterns and paleoclimatic applications, New Phytol., 190, 724–739, https://doi.org/10.1111/j.1469-8137.2010.03615.x, 2011.",

    "Ploton, P., Mortier, F., Réjou-Méchain, M., Barbier, N., Picard, N., Rossi, V., Dormann, C., Cornu, G., Viennois, G., Bayol, N., Lyapustin, A., Gourlet-Fleury, S., and Pélissier, R.: Spatial validation reveals poor predictive performance of large-scale ecological mapping models, Nat. Commun., 11, 4540, https://doi.org/10.1038/s41467-020-18321-y, 2020.",

    "Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J. J., Schröder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F., and Dormann, C. F.: Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure, Ecography, 40, 913–929, https://doi.org/10.1111/ecog.02881, 2017.",

    "Royer, D. L., Wilf, P., Janesko, D. A., Kowalski, E. A., and Dilcher, D. L.: Correlations of climate and plant ecology to leaf size and shape: potential proxies for the fossil record, Am. J. Bot., 92, 1141–1151, https://doi.org/10.3732/ajb.92.7.1141, 2005.",

    "Spicer, R. A.: CLAMP, in: Encyclopedia of Paleoclimatology and Ancient Environments, edited by Gornitz, V., Springer, Dordrecht, 175–178, 2009.",

    "Spicer, R. A., Su, T., Valdes, P. J., Farnsworth, A., Wu, F.-X., Shi, G., Spicer, T. E. V., and Zhou, Z.-K.: Why 'the uplift of the Tibetan Plateau' is a myth, Natl. Sci. Rev., 8, nwaa091, https://doi.org/10.1093/nsr/nwaa091, 2021.",

    "Spicer, R. A., Valdes, P. J., Hughes, A., Yang, J., Spicer, T. E. V., Herman, A., and Farnsworth, A.: New insights into the thermal regime and hydrodynamics of the early Late Cretaceous Arctic, Geol. Mag., 157, 1729–1746, https://doi.org/10.1017/S0016756819000465, 2020.",

    "Su, T., Spicer, R. A., Li, S.-H., Xu, H., Huang, J., Sherlock, S., Huang, Y.-J., Li, S.-F., Wang, L., Jia, L.-B., Deng, W.-Y.-D., Liu, J., Deng, C.-L., Zhang, S.-T., Valdes, P. J., and Zhou, Z.-K.: Uplift, climate and biotic changes at the Eocene–Oligocene transition in south-eastern Tibet, Natl. Sci. Rev., 6, 495–504, https://doi.org/10.1093/nsr/nwy062, 2019.",

    "Wilf, P.: When are leaves good thermometers? A new case for leaf margin analysis, Paleobiology, 23, 373–390, 1997.",

    "Wolfe, J. A.: Tertiary climatic fluctuations and methods of analysis of Tertiary floras, Palaeogeogr. Palaeoclimatol. Palaeoecol., 9, 27–57, 1971.",

    "Wolfe, J. A.: Temperature parameters of humid to mesic forests of eastern Asia and relation to forests of other regions of the Northern Hemisphere and Australasia, US Geol. Surv. Prof. Pap., 1106, 1–37, 1979.",

    "Wolfe, J. A.: A method of obtaining climatic parameters from leaf assemblages, US Geol. Surv. Bull., 2040, 1–71, 1993.",

    "Wright, I. J., Dong, N., Maire, V., Prentice, I. C., Westoby, M., Díaz, S., Gallagher, R. V., Jacobs, B. F., Kooyman, R., Law, E. A., Leishman, M. R., Niinemets, Ü., Reich, P. B., Sack, L., Villar, R., Wang, H., and Wilf, P.: Global climatic drivers of leaf size, Science, 357, 917–921, https://doi.org/10.1126/science.aal4760, 2017.",

    "Yang, J., Spicer, R. A., Spicer, T. E. V., Arens, N. C., Jacques, F. M. B., Su, T., Kennedy, E. M., Herman, A. B., Steart, D. C., Srivastava, G., Mehrotra, R. C., Valdes, P. J., Mehrotra, N. C., Zhou, Z.-K., and Lai, J.-S.: Leaf form–climate relationships on the global stage: an ensemble of characters, Palaeogeogr. Palaeoclimatol. Palaeoecol., 435, 159–169, https://doi.org/10.1016/j.palaeo.2015.06.013, 2015.",
]

for ref in refs:
    p = doc.add_paragraph()
    run = p.add_run(ref)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    p.paragraph_format.left_indent = Cm(1.27)
    p.paragraph_format.first_line_indent = Cm(-1.27)


# ═══════════════════════════════════════════════════
# 表格
# ═══════════════════════════════════════════════════
doc.add_page_break()
add_heading("表格", level=1)

add_heading("表 1. 空间区块验证、基线比较和化石转移下的模型性能汇总", level=2)
add_para("空间区块验证指标来自基于区块的 GroupKFold（10 折）。最佳基线是各变量表现最佳的线性模型。两阶段 ΔR² 是仅性状模型到两阶段架构的变化（仅湿度-能量变量）。化石指标为相对于 CLAMP 参考值的 R²、RMSE 和平均偏差（N = 71 个组合）。", italic=True)

table1 = doc.add_table(rows=8, cols=9)
table1.style = 'Light Grid Accent 1'
headers1 = ['变量', '类别', '空间区块\nR² (RF)', '空间区块\nRMSE',
            '最佳\n基线', '基线\nR²', '两阶段\nΔR²', '化石\nR²', '化石\nRMSE']
data1 = [
    ['MAT', '温度', '0.383', '3.82', 'OLS', '0.343', '—', '0.646', '2.74'],
    ['WMMT', '温度', '−0.321', '3.71', 'ElasticNet', '−0.284', '—', '−1.056', '2.91'],
    ['CMMT', '温度', '−0.013', '6.02', 'PLS', '−0.238', '—', '0.820', '2.79'],
    ['GROWSEAS', '温度', '0.099', '1.78', 'OLS', '0.138', '—', '0.730', '1.01'],
    ['RH', '湿度-能量', '−0.331', '9.55', 'ElasticNet', '−0.720', '−0.030', '−0.080', '18.94'],
    ['SH', '湿度-能量', '0.136', '1.99', 'ElasticNet', '0.060', '−0.099', '0.385', '2.95'],
    ['ENTHAL', '湿度-能量', '0.299', '11.11', 'OLS', '0.306', '−0.092', '0.681', '9.68'],
]

for j, h in enumerate(headers1):
    cell = table1.rows[0].cells[j]
    cell.text = h
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.size = Pt(8)
            run.font.name = 'Times New Roman'
            run.bold = True

for i, row in enumerate(data1):
    for j, val in enumerate(row):
        cell = table1.rows[i + 1].cells[j]
        cell.text = val
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.size = Pt(8)
                run.font.name = 'Times New Roman'

add_para("")
add_heading("表 2. 留一大洲（LOCO）验证结果（Random Forest）", level=2)
add_para("各变量-大洲组合的 R² 值。N 是各大洲的保留站点数。", italic=True)

table2 = doc.add_table(rows=36, cols=4)
table2.style = 'Light Grid Accent 1'
headers2 = ['变量', '大洲', '站点数', 'R²']
for j, h in enumerate(headers2):
    cell = table2.rows[0].cells[j]
    cell.text = h
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.size = Pt(8)
            run.font.name = 'Times New Roman'
            run.bold = True

loco_data = [
    ['MAT', '非洲', '14', '0.231'], ['MAT', '美洲', '143', '0.448'],
    ['MAT', '亚洲', '158', '0.408'], ['MAT', '欧洲', '25', '−1.035'],
    ['MAT', '大洋洲', '53', '0.323'],
    ['CMMT', '非洲', '14', '0.254'], ['CMMT', '美洲', '143', '0.496'],
    ['CMMT', '亚洲', '158', '0.099'], ['CMMT', '欧洲', '25', '−1.430'],
    ['CMMT', '大洋洲', '53', '0.310'],
    ['GROWSEAS', '非洲', '14', '−0.338'], ['GROWSEAS', '美洲', '143', '0.505'],
    ['GROWSEAS', '亚洲', '158', '0.549'], ['GROWSEAS', '欧洲', '25', '−0.213'],
    ['GROWSEAS', '大洋洲', '53', '0.219'],
    ['RH', '非洲', '14', '0.131'], ['RH', '美洲', '143', '−1.269'],
    ['RH', '亚洲', '158', '−0.313'], ['RH', '欧洲', '25', '−11.995'],
    ['RH', '大洋洲', '53', '−0.425'],
    ['SH', '非洲', '14', '0.358'], ['SH', '美洲', '143', '0.443'],
    ['SH', '亚洲', '158', '0.479'], ['SH', '欧洲', '25', '−0.493'],
    ['SH', '大洋洲', '53', '0.508'],
    ['ENTHAL', '非洲', '14', '0.530'], ['ENTHAL', '美洲', '143', '0.442'],
    ['ENTHAL', '亚洲', '158', '0.536'], ['ENTHAL', '欧洲', '25', '−0.641'],
    ['ENTHAL', '大洋洲', '53', '0.556'],
    ['WMMT', '非洲', '14', '−0.161'], ['WMMT', '美洲', '143', '−0.105'],
    ['WMMT', '亚洲', '158', '−0.344'], ['WMMT', '欧洲', '25', '−0.767'],
    ['WMMT', '大洋洲', '53', '0.071'],
]

for i, row in enumerate(loco_data):
    for j, val in enumerate(row):
        cell = table2.rows[i + 1].cells[j]
        cell.text = val
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.size = Pt(8)
                run.font.name = 'Times New Roman'


# ═══════════════════════════════════════════════════
# 保存
# ═══════════════════════════════════════════════════
output_path = os.path.join(BASE_DIR, "Manuscript_ML_Limitations_v7_CN.docx")
doc.save(output_path)
print(f"中文版稿件 (v7, ML局限性) 已保存至: {output_path}")
print(f"  标题: 集成机器学习在叶相古气候重建中的有限效益")
print(f"  核心论点: 空间验证下机器学习未优于线性基线")
print(f"  参考文献: 25 篇，按字母顺序排列")
print(f"  嵌入图表: Fig1–5")
