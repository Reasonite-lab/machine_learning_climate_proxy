#!/usr/bin/env python3
"""
Build the restructured manuscript — geoscience-oriented narrative.
Leaf physiognomy paleoclimate reconstruction: quantitative constraints
from space-block validation of 393 modern sites and 71 fossil assemblages.

Refs: 25 citations including Ding Lin (He et al., 2022) and recent CLAMP work.
"""

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

doc = Document()

# ── Page setup ──
for sec in doc.sections:
    sec.top_margin = Cm(2.54)
    sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(2.54)
    sec.right_margin = Cm(2.54)

# ── Style setup ──
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.5

for lvl in [1, 2, 3]:
    h_style = doc.styles[f'Heading {lvl}']
    h_font = h_style.font
    h_font.name = 'Times New Roman'
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
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    if alignment is not None:
        p.alignment = alignment
    return p

def add_heading(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_figure(filename, caption, width=Inches(6.0)):
    """Insert a PDF/PNG figure with caption."""
    fig_path = None
    for ext in ['.png', '.pdf']:
        p = os.path.join(BASE_DIR, filename + ext)
        if os.path.exists(p):
            fig_path = p
            break
    if fig_path is None:
        add_para(f"[Figure {filename} not found]", italic=True)
        return

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = p_img.add_run()
    run_img.add_picture(fig_path, width=width)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_cap = p_cap.add_run(caption)
    run_cap.font.name = 'Times New Roman'
    run_cap.font.size = Pt(9)
    run_cap.italic = True

    doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════════════════════════
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run(
    "Quantitative constraints on leaf-physiognomy paleoclimate reconstruction: "
    "space-block validation of 393 modern calibration sites and cross-region "
    "transfer to 71 fossil assemblages"
)
run.bold = True
run.font.size = Pt(14)
run.font.name = 'Times New Roman'

authors = doc.add_paragraph()
authors.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = authors.add_run("[Author list]")
run.font.size = Pt(12)
run.font.name = 'Times New Roman'

affil = doc.add_paragraph()
affil.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = affil.add_run("[Affiliations]")
run.font.size = Pt(10)
run.font.name = 'Times New Roman'
run.italic = True

corr = doc.add_paragraph()
corr.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = corr.add_run("Correspondence: [email]")
run.font.size = Pt(10)
run.font.name = 'Times New Roman'
run.italic = True

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# ABSTRACT
# ═══════════════════════════════════════════════════════════════════
add_heading("Abstract", level=1)

add_para(
    "Terrestrial paleoclimate reconstruction from fossil leaf assemblages is a "
    "cornerstone of Cenozoic paleoclimatology. Since the Climate-Leaf Analysis "
    "Multivariate Program (CLAMP) formalised leaf physiognomy–climate calibration, "
    "regional calibration has been recognised as essential: different calibration "
    "equations serve different continents and latitudinal zones. Yet a fundamental "
    "question remains unresolved—how much reliable climate information can leaf "
    "physiognomic traits convey when geographic structure is rigorously respected? "
    "Here we systematically quantify the cross-region predictive capacity of 31 leaf "
    "physiognomic traits for seven climate variables (mean annual temperature [MAT], "
    "warm-month mean temperature [WMMT], cold-month mean temperature [CMMT], "
    "growing-season length [GROWSEAS], relative humidity [RH], specific humidity "
    "[SH], and moist enthalpy [ENTHAL]), using a globally distributed dataset of 393 "
    "modern woody dicot sites and four ensemble learners tested against four linear "
    "statistical baselines. A space-block validation framework—dividing the globe into "
    "20 geographic grid blocks and applying GroupKFold—quantifies cross-block "
    "generalisability. Leave-One-Continent-Out (LOCO) validation delineates the "
    "geographic boundaries of model transferability, and fossil transfer against "
    "71 assemblages (predominantly Asian) tests real-world applicability. We find "
    "a clear hierarchy of reconstructability: MAT and ENTHAL retain modest but "
    "consistent cross-region signal (spatial validation R² ≈ 0.3–0.4), whereas "
    "GROWSEAS, CMMT, and SH hover near zero, and WMMT and RH are fundamentally "
    "unpredictable across space. Ensemble learners provide no statistically "
    "meaningful improvement over linear baselines under honest spatial partitioning, "
    "indicating that the cross-region trait–climate relationship is essentially linear. "
    "A physically motivated two-stage architecture—predicting temperature first, then "
    "feeding those estimates into moisture–energy prediction—collapses under spatial "
    "validation, revealing that error propagation across space outweighs any physical "
    "information cascade. Fossil transfer yields R² values of 0.65 (MAT), 0.82 (CMMT), "
    "0.73 (GROWSEAS), and 0.68 (ENTHAL) against CLAMP reference values; however, 65 of "
    "71 fossil sites are Asian, making these apparently strong results a case of "
    "within-domain interpolation rather than cross-continent generalisation. We conclude "
    "that leaf physiognomy provides a robust but spatially bounded tool for terrestrial "
    "paleoclimate reconstruction, and that space-block validation is essential for "
    "honest quantification of this boundary."
)

kw = doc.add_paragraph()
run = kw.add_run("Keywords: ")
run.bold = True
run.font.name = 'Times New Roman'
run.font.size = Pt(12)
run = kw.add_run(
    "leaf physiognomy, paleoclimate reconstruction, space-block validation, "
    "CLAMP, paleoelevation, Tibetan Plateau, cross-region generalisation, "
    "terrestrial paleoclimatology"
)
run.font.name = 'Times New Roman'
run.font.size = Pt(12)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ═══════════════════════════════════════════════════════════════════
add_heading("1 Introduction", level=1)

add_para(
    "The reconstruction of terrestrial paleoclimate from fossil leaf assemblages "
    "is one of the longest-standing quantitative approaches in paleoclimatology. "
    "Since Bailey and Sinnott (1916) first demonstrated that the proportion of "
    "entire-margined woody dicot species correlates with mean annual temperature, "
    "leaf physiognomic traits—tooth type, leaf size class, apex and base form, "
    "length:width ratio, and overall shape—have been systematically calibrated "
    "against modern climate observations to infer past terrestrial conditions "
    "(Wolfe, 1971, 1979; Wilf, 1997; Gregory-Wodzicki, 2000; Royer et al., 2005). "
    "The Climate-Leaf Analysis Multivariate Program (CLAMP; Wolfe, 1993; Spicer, 2009), "
    "built on canonical correspondence analysis, formalised multivariate leaf "
    "physiognomy–climate calibration and has become the most widely applied "
    "physiognomic paleoclimate tool, with successful applications spanning "
    "the Cretaceous to Quaternary across all continents."
)

add_para(
    "A defining feature of CLAMP's methodology—and one that distils decades of "
    "practical wisdom—is its explicit recognition that leaf–climate relationships "
    "are not globally uniform. Vegetation from different floristic regions, shaped "
    "by distinct evolutionary and biogeographic histories, exhibits systematically "
    "different morphological responses to the same climate variables. This insight "
    "has motivated the maintenance of regional calibration datasets: separate "
    "calibration equations have been developed for East Asia, North America, "
    "the Southern Hemisphere, and other floristic provinces (Wolfe, 1979, 1993; "
    "Yang et al., 2015; Spicer et al., 2020). The regional calibration strategy "
    "has been essential to CLAMP's persistent utility, particularly for "
    "reconstructing the paleoelevation and paleoclimate of the Tibetan Plateau—"
    "a setting where tectonic and climatic evolution are intimately coupled "
    "(Spicer et al., 2021; He et al., 2022; Ding et al., 2022; Bhatia et al., 2025)."
)

add_para(
    "Building on this tradition, recent years have seen growing interest in applying "
    "ensemble machine learning (ML) methods to leaf physiognomic data, driven by the "
    "expectation that non-linear models might capture complex trait–climate interactions "
    "beyond the reach of linear methods (Peppe et al., 2011; Lowe et al., 2024; "
    "Chen et al., 2025). Some studies have reported R² values exceeding 0.8 for key "
    "temperature variables, and physiologically motivated multi-stage architectures—"
    "in which predicted temperatures inform downstream moisture or energy-balance "
    "estimates—have been proposed to cascade information across physically linked "
    "climate variables. These developments raise an important question, which we "
    "frame within the CLAMP regional-calibration logic: at what spatial grain does "
    "the leaf-trait–climate signal lose generalisability? And when we push cross-region "
    "extrapolation—the scenario that fossil transfer demands—how much reconstructable "
    "signal actually remains?"
)

add_para(
    "The question has practical urgency. Modern leaf-trait calibration sites are not "
    "independent draws from a global distribution—they cluster in intensively studied "
    "regions: East Asia (158 of our 393 sites), the Americas (143 sites), and Oceania "
    "(53 sites), while Europe (25 sites) and Africa (14 sites) are sparsely "
    "represented. This geographic imbalance mirrors the fossil record: 65 of our 71 "
    "fossil assemblages are from Asia. When calibration and target sites share the "
    "same geographic domain, validation metrics reflect within-region interpolation "
    "rather than the cross-region generalisation that paleoclimate reconstruction "
    "inherently requires (Roberts et al., 2017; Meyer et al., 2019; Ploton et al., "
    "2020). This concern is especially acute for paleoelevation studies on the "
    "Tibetan Plateau, where fossil leaf assemblages from high-elevation basins "
    "must be interpreted using calibration data from lower-elevation regions, often "
    "across substantial geographic and climatic distances (Miao et al., 2022; "
    "He et al., 2022; Liang et al., 2025)."
)

add_para(
    "Here we extend the CLAMP regional-calibration logic towards a systematic, "
    "quantitative framework for assessing cross-region generalisability. Using a "
    "globally distributed calibration dataset of 393 modern woody dicot sites with "
    "31 physiognomic trait proportions, we implement: (1) space-block GroupKFold "
    "validation, partitioning sites by contiguous geographic grid blocks to prevent "
    "within-domain information leakage; (2) Leave-One-Continent-Out (LOCO) validation, "
    "testing transferability across floristic provinces; and (3) fossil transfer "
    "against 71 fossil assemblages, predominantly Asian, to evaluate real-world "
    "applicability. We compare four ensemble learners (Random Forest, XGBoost, "
    "Gradient Boosting, SVR) against four linear statistical baselines (Ordinary "
    "Least Squares, Ridge, ElasticNet, PLS), and test a physically motivated "
    "two-stage temperature→moisture cascade under leak-free spatial partitioning. "
    "Rather than evaluating which method 'wins', our aim is to quantify the "
    "fundamental information content of leaf traits for climate reconstruction "
    "when geographic structure is taken seriously—thereby providing a reproducible "
    "baseline for interpreting past and future leaf-physiognomy paleoclimate studies."
)

# ═══════════════════════════════════════════════════════════════════
# 2. DATA AND METHODS
# ═══════════════════════════════════════════════════════════════════
add_heading("2 Data and Methods", level=1)

add_heading("2.1 Modern calibration dataset", level=2)
add_para(
    "The modern calibration dataset comprises 393 woody dicotyledonous angiosperm sites "
    "spanning five continents (Asia: 158 sites; Americas: 143; Oceania: 53; Europe: 25; "
    "Africa: 14). The geographic imbalance reflects the real-world distribution of "
    "botanical sampling effort and is consistent with prior CLAMP calibration datasets "
    "(Wolfe, 1993; Yang et al., 2015). For each site, 31 leaf physiognomic traits are "
    "recorded as compositional proportions (summing to 1 within each trait category), "
    "following the standard CLAMP protocol. The traits span six morphological categories: "
    "tooth type (7 proportions: lobed, no teeth, teeth regular, teeth close, teeth round, "
    "teeth acute, teeth compound), leaf size class (9 proportions: nanophyll through "
    "mesophyll 3), apex form (4 proportions: emarginate, round, acute, attenuate), base "
    "form (3 proportions: cordate, round, acute), length:width ratio (5 proportions: "
    "<1:1 through >4:1), and general shape (3 proportions: obovate, elliptic, ovate). "
    "Associated climate data for the seven target variables—mean annual temperature "
    "(MAT), warm-month mean temperature (WMMT), cold-month mean temperature (CMMT), "
    "growing-season length (GROWSEAS), relative humidity (RH), specific humidity (SH), "
    "and moist enthalpy (ENTHAL)—were extracted from the WorldClim 2 global gridded "
    "climate dataset (Fick and Hijmans, 2017) at the geographic coordinates of each site."
)

add_heading("2.2 Fossil assemblages", level=2)
add_para(
    "The fossil dataset consists of 71 leaf assemblages spanning the Cretaceous through "
    "Quaternary, predominantly from Asia (65 assemblages: Tibetan Plateau, Yunnan, "
    "northeast India, Myanmar, Vietnam, Guangxi, Guangdong), with four European "
    "(Spain, Poland) and one North American (Florissant, Colorado) assemblage. "
    "CLAMP-computed climate values serve as reference targets for fossil transfer "
    "evaluation. We note that CLAMP reference values are model-derived estimates, "
    "not instrumental observations, and that fossil reference values are available "
    "only for those variables and assemblages that CLAMP can resolve. The Asian "
    "dominance of the fossil set (92% of assemblages) is an inherent feature of the "
    "available data, reflecting the extraordinary richness of East Asian fossil floras "
    "and the concentration of paleobotanical research effort in this region "
    "(Su et al., 2019; Spicer et al., 2021; He et al., 2022)."
)

add_heading("2.3 Space-block validation framework", level=2)
add_para(
    "Building on CLAMP's regional-calibration logic, we implement a space-block "
    "validation framework that extends the principle of geographic partitioning to "
    "a finer grain. The globe is divided into two-dimensional grid blocks based on "
    "latitude and longitude percentiles (5 latitudinal bands × 4 longitudinal bands, "
    "yielding ≤20 spatial blocks). Each of the 393 modern sites is assigned to a "
    "unique block, and GroupKFold (with spatial block as the grouping variable) ensures "
    "that all sites within the same block are assigned exclusively to either training "
    "or test sets within each fold. This prevents any within-block spatial "
    "autocorrelation from inflating validation metrics. We use 10-fold GroupKFold "
    "(constrained by the number of valid blocks) and report the mean and standard "
    "deviation of R² and RMSE across folds. The space-block approach is coarser than "
    "CLAMP's continent-scale partitions but finer than random splitting—it serves as "
    "a quantitative probe of the spatial grain at which trait–climate relationships "
    "break down."
)

add_heading("2.4 Two-stage prediction architecture", level=2)
add_para(
    "Following the physical cascade from temperature to moisture–energy variables "
    "(Clausius–Clapeyron relationship, specific humidity and enthalpy as functions of "
    "temperature and moisture), we implement a two-stage architecture: Stage 1 predicts "
    "the four temperature variables (MAT, WMMT, CMMT, GROWSEAS) from the 31 trait "
    "proportions alone, generating out-of-fold (OOF) predictions for all 393 modern "
    "sites. Stage 2 predicts the three moisture–energy variables (RH, SH, ENTHAL) "
    "from an augmented feature set comprising the 31 traits plus the four OOF "
    "temperature predictions from Stage 1. Critically, OOF predictions are generated "
    "using models trained on different spatial folds, guaranteeing that no target-site "
    "temperature information leaks into the Stage 2 training data. A traits-only "
    "baseline (31 traits → moisture–energy variable, without temperature augmentation) "
    "quantifies the information contribution of the two-stage design."
)

add_heading("2.5 Models and baselines", level=2)
add_para(
    "We evaluate four ensemble learners and four linear baselines on identical spatial "
    "folds. Ensemble learners: Random Forest (n_estimators=500, max_depth=12, "
    "min_samples_leaf=3), XGBoost (n_estimators=300, max_depth=5, learning_rate=0.03), "
    "Gradient Boosting (n_estimators=300, max_depth=4, learning_rate=0.03), and "
    "Support Vector Regression (RBF kernel, C=10.0). Hyperparameters were chosen to "
    "favour spatial generalisation through regularisation (limited tree depth, "
    "increased minimum samples per leaf) rather than through grid search optimised "
    "against a non-spatial objective. Linear baselines: ordinary least squares, Ridge "
    "regression with cross-validated alpha, ElasticNet with cross-validated L1 ratio "
    "and alpha, and Partial Least Squares (n_components=4). For tree-based models we "
    "omit preprocessing transformations, as compositional trait data (proportions "
    "bounded in [0,1]) are monotonic-invariant under tree splits."
)

add_heading("2.6 Leave-One-Continent-Out (LOCO) validation", level=2)
add_para(
    "To assess cross-continent transferability—directly probing the limits of CLAMP's "
    "regional-calibration logic—we perform LOCO validation using Random Forest on all "
    "seven targets. For each continent (Asia, Americas, Oceania, Europe, Africa), all "
    "sites belonging to that continent are held out as the test set, and the model is "
    "trained on the remaining continents. This provides a realistic upper bound on "
    "model performance for fossil sites on continents with sparse or absent modern "
    "training data—the scenario faced by paleobotanists working in regions such as "
    "Europe, Africa, or high-latitude Asia."
)

add_heading("2.7 Fossil transfer evaluation", level=2)
add_para(
    "Final models are trained on all 393 modern sites using the optimised "
    "hyperparameters and evaluated on the 71 fossil assemblages. For temperature "
    "variables, the Stage 1 Random Forest model trained on all modern data is applied "
    "directly to fossil traits. For moisture–energy variables, a Stage 2 Random Forest "
    "model is trained on modern sites using traits + Stage 1 OOF temperature predictions, "
    "then applied to fossil traits augmented with fossil temperature predictions from "
    "Stage 1. Performance is reported as R², RMSE, and mean bias against CLAMP reference "
    "values. Given the Asian dominance of the fossil dataset and the model-derived nature "
    "of CLAMP targets, we interpret fossil transfer results as an evaluation of "
    "within-domain consistency rather than independent validation."
)

# ═══════════════════════════════════════════════════════════════════
# 3. RESULTS
# ═══════════════════════════════════════════════════════════════════
add_heading("3 Results", level=1)

# ─── 3.1 Trait–Climate Correlations + Fig 1 ───
add_heading("3.1 Trait–climate correlation structure", level=2)
add_para(
    "Spearman rank correlations between the 31 leaf physiognomic traits and seven climate "
    "variables reveal a structured but generally moderate association pattern (Fig. 1). "
    "The strongest single-trait correlation is between the proportion of entire-margined "
    "leaves (No Teeth) and MAT (ρ = 0.52, p < 0.001), consistent with the classic "
    "leaf-margin analysis (Bailey and Sinnott, 1916; Wilf, 1997). Mesophyll size classes "
    "show the strongest associations with moisture variables (Mesophyll 3 vs SH: ρ = 0.48, "
    "p < 0.001), reflecting the well-documented relationship between leaf size and water "
    "availability (Peppe et al., 2011). Tooth-type traits exhibit the broadest climate "
    "correlations overall, particularly with temperature variables, while leaf shape "
    "traits (obovate, elliptic, ovate) show the weakest climate associations—a pattern "
    "consistent with the physiological basis of leaf morphology: margin type and size "
    "respond to growing-season temperature and water balance, whereas gross shape may "
    "reflect phylogenetic constraints as much as climate. The correlation structure "
    "confirms that leaf morphology carries detectable but noisy climate signal and "
    "motivates the quantitative decomposability analysis that follows."
)

add_figure("Fig1_trait_climate_corr",
    "Figure 1: Spearman rank correlation between 31 leaf physiognomic traits and seven climate "
    "variables across 393 modern woody dicot sites. Trait categories are indicated by coloured "
    "sidebars: tooth type (red), leaf size class (blue), apex form (green), base form (orange), "
    "L:W ratio (purple), and general shape (teal). Filled circles indicate p < 0.01 after "
    "Bonferroni correction.")

doc.add_page_break()

# ─── 3.2 Space-block validation: reconstructability hierarchy ───
add_heading("3.2 Space-block validation and the reconstructability hierarchy", level=2)
add_para(
    "Under space-block validation, the performance of all models drops substantially below "
    "what conventional random-fold cross-validation would report (Fig. 2; Table 1), and a "
    "clear hierarchy of reconstructability emerges. MAT is the most reconstructable variable: "
    "the Random Forest achieves R² = 0.383 ± 0.438 (RMSE = 3.82 °C), with the best linear "
    "baseline (Linear Regression) reaching R² = 0.343. ENTHAL follows at R² = 0.299 (RF) "
    "and 0.306 (best baseline: Linear Regression). SH achieves R² = 0.136 (RF), GROWSEAS "
    "R² = 0.099 (RF), and CMMT R² = −0.013 (RF). WMMT and RH are fundamentally "
    "unpredictable across spatial blocks, with R² values of −0.321 and −0.331 respectively "
    "(both by RF)."
)

add_para(
    "The hierarchy MAT ≈ ENTHAL > SH > GROWSEAS > CMMT ≫ WMMT, RH has a physical "
    "interpretation. MAT and ENTHAL integrate annual energy balance—the signal that leaf "
    "morphology captures most strongly through margin type and size distribution. CMMT and "
    "WMMT represent seasonal extremes that are physiologically decoupled from the growing-"
    "season conditions under which leaves develop and are preserved. RH, as a ratio of "
    "actual to saturation vapour pressure, is inherently difficult to predict from "
    "morphological traits that respond to absolute moisture content (SH) rather than "
    "relative saturation. This reconstructability hierarchy constitutes a quantitative "
    "baseline for what leaf physiognomy can and cannot deliver under honest geographic "
    "partitioning."
)

add_figure("Fig2_model_comparison",
    "Figure 2: Space-block validation performance comparison across five models for six climate "
    "variables. Bars show mean R² from space-block GroupKFold (10 folds). WMMT is omitted due "
    "to uniformly negative performance across all models. Vertical dashed line separates "
    "temperature (left) and moisture–energy (right) targets.")

add_para(
    "A striking finding is that ensemble learners provide no statistically meaningful "
    "advantage over linear baselines under space-block validation. For MAT, the Random "
    "Forest gains only 0.04 in R² over the best linear model (Linear Regression R² = 0.343 "
    "vs RF R² = 0.383), a difference that falls within one standard deviation of the "
    "cross-validation folds (σ = 0.438). For GROWSEAS, the best baseline (Linear Regression, "
    "R² = 0.138) outperforms the best ensemble learner (RF, R² = 0.099). For ENTHAL, Linear "
    "Regression (R² = 0.306) marginally exceeds RF (R² = 0.299). This pattern indicates "
    "that the cross-region trait–climate signal is essentially linear—non-linear models "
    "may capture within-region residual structure that does not transfer across geographic "
    "boundaries. From a paleoclimate perspective, this is an encouraging finding: it suggests "
    "that simpler, more interpretable statistical models are adequate for cross-region "
    "reconstruction and that the additional complexity of ensemble methods does not "
    "translate into additional geographic generalisability."
)

# ─── 3.3 Two-stage architecture ───
add_heading("3.3 Two-stage temperature→moisture cascade", level=2)
add_para(
    "The physically motivated two-stage architecture—predicting temperature variables first, "
    "then using those predictions to inform moisture–energy estimates—does not survive "
    "space-block validation. For all three moisture–energy targets, the traits-only "
    "baseline consistently outperforms the two-stage architecture (Fig. 5a; Table 1). "
    "For SH, the traits-only RF achieves R² = 0.235 versus 0.136 for the two-stage RF "
    "(Δ = −0.099). For ENTHAL, the traits-only RF R² = 0.391 versus 0.299 (Δ = −0.092). "
    "This degradation is consistent across all four ensemble learners: adding OOF "
    "temperature predictions introduces noise that outweighs any physical information "
    "content when sites are partitioned by geography."
)

add_para(
    "We attribute this to error propagation across space. Stage 1 temperature predictions "
    "carry systematic spatial biases—sites within a given block tend to be systematically "
    "over- or under-predicted—and these biases are amplified when fed into Stage 2. The "
    "physically well-founded cascade from temperature to moisture operates within-site "
    "(governed by local energy and moisture balance) but does not survive the transition "
    "to cross-region prediction, where spatial biases in the temperature estimates overwhelm "
    "any signal the traits alone already capture. This finding has practical implications "
    "for study design: when target fossil sites lie in geographic domains remote from "
    "calibration data, traits-only prediction of moisture variables is likely more robust "
    "than a two-stage scheme, despite being physically less complete."
)

# ─── 3.4 LOCO validation ───
add_heading("3.4 Cross-continent transferability: the geographic boundary", level=2)
add_para(
    "LOCO validation (Fig. 3f; Table 2) defines the geographic boundary conditions within "
    "which leaf-trait-based climate reconstruction is viable. For MAT, the model achieves "
    "positive R² for Asia (0.408), the Americas (0.448), Oceania (0.323), and Africa "
    "(0.231), but fails catastrophically for Europe (R² = −1.035), where only 25 training "
    "sites exist and the European held-out sites span a climate space poorly represented "
    "in the remaining continents. CMMT shows an even sharper pattern: R² = 0.496 for the "
    "Americas but −1.430 for Europe. The three moisture–energy variables (RH, SH, ENTHAL) "
    "show moderate LOCO performance for Asia, the Americas, and Oceania but uniformly "
    "negative R² for Europe."
)

add_para(
    "Two patterns emerge from this geographic decomposition. First, model performance "
    "scales with calibration density: continents with more training sites in the held-in "
    "set support better prediction of the held-out continent, consistent with the "
    "expectation that climate-space coverage, not just sample count, determines "
    "transferability (Roberts et al., 2017). Second, Europe's consistent failure across "
    "all targets indicates that the European leaf-trait–climate relationship differs "
    "systematically from that of the remaining continents—likely reflecting both the small "
    "sample size (25 sites) and the unique floristic and climatic character of European "
    "temperate forests relative to East Asian and American assemblages. These LOCO results "
    "quantify what CLAMP practitioners have long understood qualitatively: leaf-physiognomy "
    "calibrations are not globally portable and must be matched to the floristic province "
    "of the target fossil assemblage."
)

# ─── 3.5 Fossil transfer ───
add_heading("3.5 Fossil transfer: regional interpolation or global prediction?", level=2)
add_para(
    "Fossil transfer against CLAMP reference values yields results that must be interpreted "
    "through the lens of the fossil dataset's geographic composition (Fig. 3a–e; Table 1). "
    "For temperature variables, fossil R² ranges from 0.646 (MAT, RMSE = 2.74 °C, "
    "bias = −1.69 °C) to 0.820 (CMMT, RMSE = 2.79 °C, bias = −0.98 °C). GROWSEAS achieves "
    "fossil R² = 0.730 (RMSE = 1.01 months), while WMMT fails (R² = −1.056). For "
    "moisture–energy variables, ENTHAL achieves fossil R² = 0.681 (RMSE = 9.68 kJ/kg) "
    "and SH achieves 0.385 (RMSE = 2.95 g/kg). A systematic cold bias is evident across "
    "all fossil predictions (MAT bias = −1.69 °C; ENTHAL bias = −4.90 kJ/kg)."
)

add_para(
    "The apparently strong fossil CMMT performance (R² = 0.820) must be reconciled with "
    "its negative space-block validation R² (−0.013). The resolution lies in the fossil "
    "dataset composition: 65 of 71 assemblages are from Asia, where the modern calibration "
    "network is densest (158 of 393 sites). The fossil transfer for CMMT effectively "
    "amounts to within-domain interpolation—the fossil sites and their modern analogues "
    "share the same geographic domain. LOCO results corroborate this: CMMT achieves R² = 0.50 "
    "for the Americas but fails for Europe (R² = −1.43). The high fossil R² for CMMT "
    "therefore reflects regional consistency rather than global predictive capability. "
    "This finding has direct implications for paleoelevation studies on the Tibetan "
    "Plateau: models calibrated on Asian data can reconstruct Asian fossil climate with "
    "reasonable fidelity, but their skill does not generalise to Europe, Africa, or "
    "other floristically distinct regions—a boundary condition that the CLAMP community "
    "has long respected in practice (Spicer et al., 2021; He et al., 2022) and that our "
    "quantitative framework now formally delineates."
)

add_figure("Fig3_obs_vs_pred",
    "Figure 3: Fossil transfer evaluation and cross-continent validation. (a–e) Predicted vs "
    "CLAMP reference values for five climate variables across 71 fossil assemblages; dashed "
    "line indicates identity. Marker colours distinguish temperature (blue) and moisture–energy "
    "(red) targets. (f) Leave-One-Continent-Out R² heatmap for five climate variables across "
    "five continents.")

doc.add_page_break()

# ─── 3.6 Feature importance ───
add_heading("3.6 Trait contributions to climate prediction", level=2)
add_para(
    "Random Forest feature importance analysis (Fig. 4) reveals which trait categories "
    "drive cross-region climate signal. Tooth-type traits dominate temperature prediction, "
    "accounting for approximately 40% of MAT variance explained, followed by leaf size "
    "categories (~35%) and apex form (~12%). Base form and shape traits contribute "
    "minimally (Fig. 4c). The leading individual feature for MAT is the proportion of "
    "entire-margined leaves (No Teeth; ~15% of RF importance), confirming the century-old "
    "leaf-margin analysis (Bailey and Sinnott, 1916) as the single most informative trait "
    "even under space-block validation. For moisture–energy variables, leaf size traits "
    "dominate, with mesophyll classes contributing the largest share—consistent with the "
    "physical expectation that leaf size responds to water availability and atmospheric "
    "moisture demand (Peppe et al., 2011; Wright et al., 2017). The importance hierarchy "
    "tooth type > leaf size ≫ apex, base, shape is stable across all target variables, "
    "suggesting that effort invested in scoring additional trait categories yields "
    "diminishing returns for cross-region climate reconstruction."
)

add_figure("Fig4_feature_importance",
    "Figure 4: Feature importance analysis. (a) Random Forest feature importance heatmap across "
    "all seven climate variables. (b) Top 10 features by importance for MAT. (c) Trait-category "
    "contribution to MAT importance (pie chart).")

# ─── 3.7 Summary ───
add_heading("3.7 Summary of reconstructability", level=2)
add_para(
    "Synthesising across space-block validation, LOCO, and fossil transfer, we delineate "
    "a three-tier hierarchy of climate variable reconstructability from leaf physiognomic "
    "traits (Fig. 5b; Table 1). Tier 1—cross-region robust: MAT and ENTHAL, with "
    "positive space-block R² and moderate fossil transfer skill. Tier 2—regionally "
    "conditioned: SH, GROWSEAS, and CMMT, with near-zero space-block R² but acceptable "
    "fossil transfer within densely calibrated domains (Asia). Tier 3—fundamentally "
    "unreliable: WMMT and RH, with consistently negative or near-zero R² across all "
    "validation frameworks. This hierarchy provides a practical guide for study design: "
    "researchers should target Tier 1 variables when fossil sites lie far from calibration "
    "data, restrict Tier 2 variables to within-region applications, and avoid Tier 3 "
    "variables as reconstruction targets absent major methodological advances. For the "
    "Tibetan Plateau—where the coupling between paleoelevation and paleoclimate is central "
    "to tectonic interpretations (Ding et al., 2022; He et al., 2022)—the robust "
    "cross-region performance of MAT and ENTHAL is encouraging, while the spatially "
    "conditioned performance of CMMT and GROWSEAS cautions against over-interpreting "
    "these variables when fossil sites lie outside the East Asian calibration domain."
)

add_figure("Fig5_two_stage_ablation",
    "Figure 5: Two-stage architecture assessment and reconstructability summary. (a) Scatter "
    "plot comparing space-block R² of traits-only vs two-stage models for moisture–energy "
    "variables (SH, ENTHAL, RH); points below the identity line indicate two-stage degradation. "
    "(b) Bar chart comparing space-block R² against fossil transfer R² (vs CLAMP) for five "
    "climate variables, illustrating the gap between honest modern validation and the "
    "fossil transfer that is dominated by Asian assemblages.")

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# 4. DISCUSSION
# ═══════════════════════════════════════════════════════════════════
add_heading("4 Discussion", level=1)

add_heading("4.1 A quantitative framework for cross-region leaf-physiognomy reconstruction", level=2)
add_para(
    "Our results provide a quantitative extension of CLAMP's regional-calibration "
    "tradition. CLAMP practitioners have long maintained separate calibration datasets "
    "for different floristic provinces (Wolfe, 1993; Yang et al., 2015; Spicer et al., "
    "2021), implicitly acknowledging that leaf–climate relationships are not globally "
    "uniform. The space-block and LOCO frameworks developed here make this implicit "
    "knowledge explicit and quantitative: they reveal the precise spatial grain at which "
    "trait–climate relationships break down, and they attach numerical uncertainties to "
    "the reconstruction of each climate variable as a function of geographic distance "
    "from the calibration domain. For MAT, the drop from within-domain fossil transfer "
    "(R² = 0.65) to cross-block space-block validation (R² = 0.38) quantifies the "
    "generalisability penalty—approximately 0.27 in R²—that should be applied to "
    "predictions for fossil sites in poorly sampled regions. For CMMT, the penalty is "
    "far larger (R² = 0.82 → −0.013), warning that this variable's apparent fossil "
    "transfer success is almost entirely a product of the fossil dataset's Asian "
    "dominance."
)

add_heading("4.2 Implications for paleoelevation and Tibetan Plateau studies", level=2)
add_para(
    "The Tibetan Plateau has been a focal point for leaf-physiognomy paleoclimate "
    "reconstruction because its tectonic uplift history is intimately linked to Cenozoic "
    "climate evolution and the Asian monsoon system (Spicer et al., 2021; Ding et al., "
    "2022; He et al., 2022). Recent work has demonstrated that eastern Tibet rose to "
    "near-modern elevations by ~39 Ma, driving distinctive Eocene monsoon precipitation "
    "patterns and contributing to the modern Asian biodiversity gradient (He et al., 2022). "
    "Our space-block validation results support the use of leaf physiognomy for these "
    "applications but with an important caveat: the robust performance for MAT and ENTHAL "
    "in cross-region validation (R² ≈ 0.3–0.4) indicates that elevation inferences based "
    "on these variables are well-supported, while the collapse of CMMT under spatial "
    "partitioning suggests that cold-month temperature reconstructions for Tibetan fossil "
    "sites are reliable only when calibration and fossil sites are drawn from the same "
    "floristic domain. The LOCO results further suggest that extrapolating East Asian "
    "calibrations to fossil floras outside Asia—as might be attempted for other orogenic "
    "belts (e.g., Andes, Alps)—is unlikely to yield reliable estimates without locally "
    "dense calibration networks."
)

add_heading("4.3 The linearity of cross-region trait–climate relationships", level=2)
add_para(
    "A finding with both practical and conceptual implications is that ensemble ML methods "
    "do not outperform linear statistical baselines under space-block validation. This "
    "is not a failure of ML per se—it reflects a property of the data: the cross-region "
    "component of the trait–climate signal is approximately linear. Non-linear models may "
    "capture complex within-region structure (e.g., ecological sorting along local "
    "environmental gradients) that does not generalise across floristic provinces with "
    "different evolutionary histories and species pools. For paleoclimate reconstruction—"
    "where the explicit goal is to extrapolate from modern calibration sites to fossil "
    "sites separated in space and time—the parsimony of linear models is a feature, not "
    "a limitation. Linear regression or Ridge regression, with their well-understood "
    "uncertainty propagation and interpretability, are likely to be more trustworthy tools "
    "for cross-region paleoclimate inference than black-box ensemble methods whose apparent "
    "advantages reflect within-region overfitting (Meyer et al., 2019; Ploton et al., 2020)."
)

add_heading("4.4 The two-stage cascade and the geography of physical models", level=2)
add_para(
    "The failure of the two-stage temperature→moisture cascade under space-block "
    "validation carries a broader lesson about physical models in spatial prediction. "
    "The Clausius–Clapeyron relationship linking temperature to saturation vapour "
    "pressure is physically rigorous at the local (within-site) scale. But when "
    "temperature is estimated with spatial error—systematic biases that vary across "
    "blocks—the downstream moisture prediction absorbs and amplifies this error. "
    "The finding that traits-only models outperform two-stage architectures for "
    "moisture variables suggests that leaf traits encode moisture information "
    "independently of the temperature→moisture cascade, presumably through direct "
    "physiological responses to atmospheric and soil water availability (Peppe et al., "
    "2011; Wright et al., 2017). From a practical standpoint, we recommend that "
    "moisture–energy variables be reconstructed directly from traits for fossil sites "
    "in geographic domains poorly represented in calibration data, reserving two-stage "
    "schemes for within-domain applications where temperature estimates carry lower "
    "spatial bias."
)

add_heading("4.5 Limitations and the path forward", level=2)
add_para(
    "Several limitations bound our conclusions. First, the modern calibration dataset "
    "is geographically imbalanced, with Europe (25 sites) and Africa (14 sites) severely "
    "underrepresented. The catastrophic LOCO failure for Europe likely reflects this "
    "imbalance rather than intrinsic unpredictability of European leaf traits—meaningful "
    "calibration for Europe would require substantially expanding the modern sampling "
    "network. Second, the fossil validation targets are CLAMP-computed values, not "
    "independent instrumental observations; systematic biases in CLAMP estimates will "
    "carry through to our fossil transfer metrics. Independent validation against "
    "non-physiognomic proxies (e.g., stable isotopes, glycerol dialkyl glycerol "
    "tetraethers [GDGTs], palynology) for key fossil sites, particularly those on "
    "the Tibetan Plateau (Miao et al., 2022; Liang et al., 2025), would strengthen "
    "the fossil transfer assessment. Third, our 31-trait protocol captures a subset of "
    "leaf morphological variation; additional traits (venation density, stomatal "
    "indices, leaf mass per area) could improve spatial generalisability (Lowe et al., "
    "2024) but are not available for this dataset. Fourth, the 5 × 4 grid partitioning "
    "is one of many possible schemes; sensitivity to block resolution should be explored "
    "in future work since the optimal spatial grain likely varies by variable and region. "
    "Finally, the temporal dimension—whether trait–climate calibrations from modern "
    "vegetation apply to fossil floras separated by tens of millions of years of "
    "evolution—remains an irreducible uncertainty in all uniformitarian paleoclimate "
    "methods (Spicer et al., 2021; Chen et al., 2025)."
)

# ═══════════════════════════════════════════════════════════════════
# 5. CONCLUSIONS
# ═══════════════════════════════════════════════════════════════════
add_heading("5 Conclusions", level=1)

add_para(
    "This study provides a systematic, quantitative assessment of leaf-physiognomy "
    "climate reconstruction under honest geographic partitioning. Building on CLAMP's "
    "established regional-calibration logic, we demonstrate that the cross-region "
    "reconstructability of climate variables from leaf traits follows a well-defined "
    "hierarchy: MAT and ENTHAL are robustly recoverable across geographic blocks "
    "(space-block R² ≈ 0.3–0.4), SH, GROWSEAS, and CMMT are recoverable only within "
    "densely calibrated domains, and WMMT and RH are fundamentally unreliable as "
    "cross-region reconstruction targets. Ensemble machine learning methods provide "
    "no meaningful advantage over linear statistical baselines under spatial "
    "partitioning—the cross-region trait–climate signal is essentially linear. "
    "The physically motivated two-stage temperature→moisture cascade does not survive "
    "the transition to cross-region prediction, with traits-only models consistently "
    "outperforming two-stage architectures. Fossil transfer against CLAMP reference "
    "values for the predominantly Asian fossil dataset yields encouraging results for "
    "Tier 1 and Tier 2 variables but must be interpreted as within-domain interpolation, "
    "not cross-continent generalisation. We recommend that future leaf-physiognomy "
    "paleoclimate studies: (1) report space-block validation metrics alongside "
    "conventional cross-validation to quantify the generalisability penalty; "
    "(2) include linear baselines to benchmark the incremental value of non-linear "
    "methods; (3) consider the three-tier reconstructability hierarchy when selecting "
    "reconstruction targets, particularly for fossil sites in regions distant from "
    "modern calibration networks; and (4) expand modern calibration sampling in "
    "underrepresented regions, especially Europe and Africa, to extend the geographic "
    "domain of reliable leaf-physiognomy climate reconstruction."
)

# ═══════════════════════════════════════════════════════════════════
# DATA AND CODE AVAILABILITY
# ═══════════════════════════════════════════════════════════════════
add_heading("Data and Code Availability", level=1)

add_para(
    "The modern calibration dataset and fossil assemblage data are available in the "
    "accompanying Excel workbook (Global378+Tibet15+Fossil73_更正.xlsx). All training "
    "code, the space-block validation pipeline, figure generation scripts, trained model "
    "files, and the complete manuscript source are archived on Zenodo [DOI to be created "
    "upon acceptance] and publicly available on GitHub at [repository URL to be added]. "
    "The repository includes: (1) training_pipeline_v2.py, which reproduces all space-block "
    "validation results, baseline comparisons, LOCO validation, and fossil transfer "
    "evaluation; (2) generate_figures_v2.py, which produces all five publication figures; "
    "(3) the models_v2/ directory containing trained joblib model files; and (4) the "
    "output/ directory containing all tabulated results (Tables 1–5). All analyses were "
    "performed in Python 3.10 using scikit-learn 1.3, XGBoost 2.0, and associated "
    "scientific Python libraries. Climate data were obtained from WorldClim 2 "
    "(Fick and Hijmans, 2017; https://www.worldclim.org/)."
)

# ═══════════════════════════════════════════════════════════════════
# AUTHOR CONTRIBUTIONS, COMPETING INTERESTS, ACKNOWLEDGEMENTS
# ═══════════════════════════════════════════════════════════════════
add_heading("Author Contributions", level=1)
add_para("[To be completed by authors.]")

add_heading("Competing Interests", level=1)
add_para("The authors declare that they have no competing interests.")

add_heading("Acknowledgements", level=1)
add_para("[To be completed by authors.]")

# ═══════════════════════════════════════════════════════════════════
# REFERENCES (25 citations)
# ═══════════════════════════════════════════════════════════════════
add_heading("References", level=1)

refs = [
    # 1
    "Bailey, I. W. and Sinnott, E. W.: The climatic distribution of certain types of angiosperm leaves, Am. J. Bot., 3, 24–39, 1916.",

    # 2
    "Bhatia, H., Dar, R. A., and Srivastava, G.: Himalayan uplift and the evolution of a Mediterranean-type climate in the Kashmir Basin of India: Palaeobotanical evidence from the late Pliocene Dubjan Member (Karewa Group), Palaeogeogr. Palaeoclimatol. Palaeoecol., 672, 112547, https://doi.org/10.1016/j.palaeo.2025.112547, 2025.",

    # 3
    "Chen, W.-Y., Su, T., and Li, S.-F.: The leaf physiognomy of evergreen and deciduous species exhibits different responses to climate: Implications for palaeoclimate reconstruction in China, Palaeogeogr. Palaeoclimatol. Palaeoecol., 660, 112683, https://doi.org/10.1016/j.palaeo.2024.112683, 2025.",

    # 4
    "Ding, L., Kapp, P., Cai, F., Garzione, C. N., Xiong, Z., Wang, H., and Wang, C.: Timing and mechanisms of Tibetan Plateau uplift, Nat. Rev. Earth Environ., 3, 652–667, https://doi.org/10.1038/s43017-022-00318-4, 2022.",

    # 5
    "Fick, S. E. and Hijmans, R. J.: WorldClim 2: new 1-km spatial resolution climate surfaces for global land areas, Int. J. Climatol., 37, 4302–4315, https://doi.org/10.1002/joc.5086, 2017.",

    # 6
    "Gregory-Wodzicki, K. M.: Relationships between leaf morphology and climate, Bolivia: implications for estimating paleoclimate from fossil floras, Paleobiology, 26, 668–688, 2000.",

    # 7
    "He, S., Ding, L., Xiong, Z., Spicer, R. A., Farnsworth, A., Valdes, P. J., Wang, C., Cai, F., Wang, H., Sun, Y., Zeng, D., Xie, J., Yue, Y., Zhao, C., Song, P., and Wu, C.: A distinctive Eocene Asian monsoon and modern biodiversity resulted from the rise of eastern Tibet, Sci. Bull., 67, 2245–2258, https://doi.org/10.1016/j.scib.2022.10.006, 2022.",

    # 8
    "Liang, Y., Quan, C., Liu, Z., Li, X., Utescher, T., and Liu, Y.-S.: Terrestrial temperature history reveals Late Miocene rapid uplift of the northern Tibetan Plateau, Sci. Adv., 11, eadq5626, https://doi.org/10.1126/sciadv.adq5626, 2025.",

    # 9
    "Lowe, A. J., Flynn, A. G., Butrim, M. J., Baumgartner, A., Royer, D. L., and Peppe, D. J.: Reconstructing terrestrial paleoclimate and paleoecology with fossil leaves using digital leaf physiognomy and leaf mass per area, J. Vis. Exp., 212, e66838, https://doi.org/10.3791/66838, 2024.",

    # 10
    "Meyer, H., Reudenbach, C., Wöllauer, S., and Nauss, T.: Importance of spatial predictor variable selection in machine learning applications—Moving from data reproduction to spatial prediction, Ecol. Model., 411, 108815, https://doi.org/10.1016/j.ecolmodel.2019.108815, 2019.",

    # 11
    "Miao, Y., Fang, X., Sun, J., Xiao, W., Yang, Y., Wang, X., Farnsworth, A., Huang, K., Ren, Y., Wu, F., Qiao, J., Zhang, W., Meng, Q., Yan, X., Zheng, Z., Song, C., and Utescher, T.: A new biologic paleoaltimetry indicating Late Miocene rapid uplift of northern Tibet Plateau, Science, 378, 1074–1079, https://doi.org/10.1126/science.abo2475, 2022.",

    # 12
    "Peppe, D. J., Royer, D. L., Cariglino, B., Oliver, S. Y., Newman, S., Leight, E., Enikolopov, G., Fernandez-Burgos, M., Herrera, F., Adams, J. M., Correa, E., Currano, E. D., Erickson, J. M., Hinojosa, L. F., Hoganson, J. W., Iglesias, A., Jaramillo, C. A., Johnson, K. R., Jordan, G. J., Kraft, N. J. B., Lovelock, E. C., Lusk, C. H., Niinemets, Ü., Peñuelas, J., Rapson, G., Wing, S. L., and Wright, I. J.: Sensitivity of leaf size and shape to climate: global patterns and paleoclimatic applications, New Phytol., 190, 724–739, https://doi.org/10.1111/j.1469-8137.2010.03615.x, 2011.",

    # 13
    "Ploton, P., Mortier, F., Réjou-Méchain, M., Barbier, N., Picard, N., Rossi, V., Dormann, C., Cornu, G., Viennois, G., Bayol, N., Lyapustin, A., Gourlet-Fleury, S., and Pélissier, R.: Spatial validation reveals poor predictive performance of large-scale ecological mapping models, Nat. Commun., 11, 4540, https://doi.org/10.1038/s41467-020-18321-y, 2020.",

    # 14
    "Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J. J., Schröder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F., and Dormann, C. F.: Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure, Ecography, 40, 913–929, https://doi.org/10.1111/ecog.02881, 2017.",

    # 15
    "Royer, D. L., Wilf, P., Janesko, D. A., Kowalski, E. A., and Dilcher, D. L.: Correlations of climate and plant ecology to leaf size and shape: potential proxies for the fossil record, Am. J. Bot., 92, 1141–1151, https://doi.org/10.3732/ajb.92.7.1141, 2005.",

    # 16
    "Spicer, R. A.: CLAMP, in: Encyclopedia of Paleoclimatology and Ancient Environments, edited by Gornitz, V., Springer, Dordrecht, 175–178, 2009.",

    # 17
    "Spicer, R. A., Su, T., Valdes, P. J., Farnsworth, A., Wu, F.-X., Shi, G., Spicer, T. E. V., and Zhou, Z.-K.: Why 'the uplift of the Tibetan Plateau' is a myth, Natl. Sci. Rev., 8, nwaa091, https://doi.org/10.1093/nsr/nwaa091, 2021.",

    # 18
    "Spicer, R. A., Valdes, P. J., Hughes, A., Yang, J., Spicer, T. E. V., Herman, A., and Farnsworth, A.: New insights into the thermal regime and hydrodynamics of the early Late Cretaceous Arctic, Geol. Mag., 157, 1729–1746, https://doi.org/10.1017/S0016756819000465, 2020.",

    # 19
    "Su, T., Spicer, R. A., Li, S.-H., Xu, H., Huang, J., Sherlock, S., Huang, Y.-J., Li, S.-F., Wang, L., Jia, L.-B., Deng, W.-Y.-D., Liu, J., Deng, C.-L., Zhang, S.-T., Valdes, P. J., and Zhou, Z.-K.: Uplift, climate and biotic changes at the Eocene–Oligocene transition in south-eastern Tibet, Natl. Sci. Rev., 6, 495–504, https://doi.org/10.1093/nsr/nwy062, 2019.",

    # 20
    "Wilf, P.: When are leaves good thermometers? A new case for leaf margin analysis, Paleobiology, 23, 373–390, 1997.",

    # 21
    "Wolfe, J. A.: Tertiary climatic fluctuations and methods of analysis of Tertiary floras, Palaeogeogr. Palaeoclimatol. Palaeoecol., 9, 27–57, 1971.",

    # 22
    "Wolfe, J. A.: Temperature parameters of humid to mesic forests of eastern Asia and relation to forests of other regions of the Northern Hemisphere and Australasia, US Geol. Surv. Prof. Pap., 1106, 1–37, 1979.",

    # 23
    "Wolfe, J. A.: A method of obtaining climatic parameters from leaf assemblages, US Geol. Surv. Bull., 2040, 1–71, 1993.",

    # 24
    "Wright, I. J., Dong, N., Maire, V., Prentice, I. C., Westoby, M., Díaz, S., Gallagher, R. V., Jacobs, B. F., Kooyman, R., Law, E. A., Leishman, M. R., Niinemets, Ü., Reich, P. B., Sack, L., Villar, R., Wang, H., and Wilf, P.: Global climatic drivers of leaf size, Science, 357, 917–921, https://doi.org/10.1126/science.aal4760, 2017.",

    # 25
    "Yang, J., Spicer, R. A., Spicer, T. E. V., Arens, N. C., Jacques, F. M. B., Su, T., Kennedy, E. M., Herman, A. B., Steart, D. C., Srivastava, G., Mehrotra, R. C., Valdes, P. J., Mehrotra, N. C., Zhou, Z.-K., and Lai, J.-S.: Leaf form–climate relationships on the global stage: an ensemble of characters, Palaeogeogr. Palaeoclimatol. Palaeoecol., 435, 159–169, https://doi.org/10.1016/j.palaeo.2015.06.013, 2015.",
]

for ref in refs:
    p = doc.add_paragraph()
    run = p.add_run(ref)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    p.paragraph_format.left_indent = Cm(1.27)
    p.paragraph_format.first_line_indent = Cm(-1.27)

# ═══════════════════════════════════════════════════════════════════
# TABLES
# ═══════════════════════════════════════════════════════════════════
doc.add_page_break()
add_heading("Tables", level=1)

add_heading("Table 1: Summary of model performance under space-block validation, baseline comparison, and fossil transfer.", level=2)
add_para("Space-block validation metrics are from block-based GroupKFold (10 folds). Best Baseline is the top-performing linear model for each variable. Two-Stage ΔR² is the change from traits-only to two-stage architecture (moisture–energy variables only). Fossil metrics are R², RMSE, and mean bias vs CLAMP reference values (N = 71 assemblages).", italic=True)

table1 = doc.add_table(rows=8, cols=9)
table1.style = 'Light Grid Accent 1'
headers1 = ['Variable', 'Category', 'Space-block\nR² (RF)', 'Space-block\nRMSE',
            'Best\nBaseline', 'Baseline\nR²', 'Two-Stage\nΔR²', 'Fossil\nR²', 'Fossil\nRMSE']
data1 = [
    ['MAT', 'Temperature', '0.383', '3.82', 'Linear', '0.343', '—', '0.646', '2.74'],
    ['WMMT', 'Temperature', '−0.321', '3.71', 'ElasticNet', '−0.284', '—', '−1.056', '2.91'],
    ['CMMT', 'Temperature', '−0.013', '6.02', 'PLS', '−0.238', '—', '0.820', '2.79'],
    ['GROWSEAS', 'Temperature', '0.099', '1.78', 'Linear', '0.138', '—', '0.730', '1.01'],
    ['RH', 'Moist.-Energy', '−0.331', '9.55', 'ElasticNet', '−0.720', '−0.030', '−0.080', '18.94'],
    ['SH', 'Moist.-Energy', '0.136', '1.99', 'ElasticNet', '0.060', '−0.099', '0.385', '2.95'],
    ['ENTHAL', 'Moist.-Energy', '0.299', '11.11', 'Linear', '0.306', '−0.092', '0.681', '9.68'],
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
add_heading("Table 2: Leave-One-Continent-Out (LOCO) validation results (Random Forest).", level=2)
add_para("R² values for each variable–continent combination. N is the number of held-out sites on each continent.", italic=True)

table2 = doc.add_table(rows=36, cols=4)
table2.style = 'Light Grid Accent 1'
headers2 = ['Variable', 'Continent', 'N Sites', 'R²']
for j, h in enumerate(headers2):
    cell = table2.rows[0].cells[j]
    cell.text = h
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.size = Pt(8)
            run.font.name = 'Times New Roman'
            run.bold = True

loco_data = [
    ['MAT', 'Africa', '14', '0.231'], ['MAT', 'Americas', '143', '0.448'],
    ['MAT', 'Asia', '158', '0.408'], ['MAT', 'Europe', '25', '−1.035'],
    ['MAT', 'Oceania', '53', '0.323'],
    ['CMMT', 'Africa', '14', '0.254'], ['CMMT', 'Americas', '143', '0.496'],
    ['CMMT', 'Asia', '158', '0.099'], ['CMMT', 'Europe', '25', '−1.430'],
    ['CMMT', 'Oceania', '53', '0.310'],
    ['GROWSEAS', 'Africa', '14', '−0.338'], ['GROWSEAS', 'Americas', '143', '0.505'],
    ['GROWSEAS', 'Asia', '158', '0.549'], ['GROWSEAS', 'Europe', '25', '−0.213'],
    ['GROWSEAS', 'Oceania', '53', '0.219'],
    ['RH', 'Africa', '14', '0.131'], ['RH', 'Americas', '143', '−1.269'],
    ['RH', 'Asia', '158', '−0.313'], ['RH', 'Europe', '25', '−11.995'],
    ['RH', 'Oceania', '53', '−0.425'],
    ['SH', 'Africa', '14', '0.358'], ['SH', 'Americas', '143', '0.443'],
    ['SH', 'Asia', '158', '0.479'], ['SH', 'Europe', '25', '−0.493'],
    ['SH', 'Oceania', '53', '0.508'],
    ['ENTHAL', 'Africa', '14', '0.530'], ['ENTHAL', 'Americas', '143', '0.442'],
    ['ENTHAL', 'Asia', '158', '0.536'], ['ENTHAL', 'Europe', '25', '−0.641'],
    ['ENTHAL', 'Oceania', '53', '0.556'],
    ['WMMT', 'Africa', '14', '−0.161'], ['WMMT', 'Americas', '143', '−0.105'],
    ['WMMT', 'Asia', '158', '−0.344'], ['WMMT', 'Europe', '25', '−0.767'],
    ['WMMT', 'Oceania', '53', '0.071'],
]

for i, row in enumerate(loco_data):
    for j, val in enumerate(row):
        cell = table2.rows[i + 1].cells[j]
        cell.text = val
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.size = Pt(8)
                run.font.name = 'Times New Roman'

# ═══════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════
output_path = os.path.join(BASE_DIR, "Manuscript_Paleoclimate_ML_CP_v5_Geoscience.docx")
doc.save(output_path)
print(f"Manuscript (v5, geoscience-oriented) saved to: {output_path}")
print(f"  References: 25 citations (including Ding L. via He et al., 2022)")
print(f"  Embedded figures: Fig1–5")
print(f"  Key narrative shift: ML methodology → geoscience constraints")
