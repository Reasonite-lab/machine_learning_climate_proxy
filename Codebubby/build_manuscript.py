#!/usr/bin/env python3
"""
Build the revised manuscript for Climate of the Past submission.
Reflects honest spatial CV results from training_pipeline_v2.py.
Embeds all 5 figures inline.
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

    # Add the image
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = p_img.add_run()
    run_img.add_picture(fig_path, width=width)

    # Add caption
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_cap = p_cap.add_run(caption)
    run_cap.font.name = 'Times New Roman'
    run_cap.font.size = Pt(9)
    run_cap.italic = True

    # Spacing after figure
    doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════════════════════════
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run(
    "Spatial cross-validation reveals fundamental limits and fossil transfer "
    "potential of leaf-physiognomy machine learning for paleoclimate reconstruction"
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
    "Leaf physiognomic traits have been used for terrestrial paleoclimate reconstruction "
    "since the early 20th century, with recent machine learning (ML) approaches claiming "
    "high predictive accuracy for multiple climate variables. However, the reliance on "
    "random k-fold cross-validation—which ignores spatial autocorrelation—risks "
    "substantially overestimating model performance in a fossil-transfer context. Here we "
    "re-examine the predictive power of 31 leaf physiognomic traits for seven climate "
    "variables (MAT, WMMT, CMMT, growing-season length, relative humidity, specific humidity, "
    "and moist enthalpy) using a globally distributed dataset of 393 modern woody dicot "
    "sites and 71 fossil assemblages. Under block-based spatial GroupKFold cross-validation, "
    "four ensemble learners (Random Forest, XGBoost, Gradient Boosting, SVR) and four "
    "statistical baselines (Linear Regression, Ridge, ElasticNet, PLS) are evaluated on "
    "a leakage-free, two-stage architecture that first predicts temperature variables "
    "from traits, then predicts moisture–energy variables from traits augmented with "
    "out-of-fold temperature estimates. Leave-One-Continent-Out (LOCO) validation and "
    "fossil transfer against CLAMP reference values test geographic generalisability. "
    "We find that spatial cross-validation dramatically reduces apparent model performance "
    "relative to random-fold estimates: the best spatial CV R² reaches only 0.38 for MAT "
    "(Random Forest) and is negative for WMMT, CMMT, and RH, indicating that leaf traits "
    "alone carry limited cross-region climate signal for these variables. The two-stage "
    "architecture provides no improvement over traits-only models for moisture variables "
    "under spatial CV—the physically motivated cascade fails to survive honest geographic "
    "partitioning. Linear baselines are statistically competitive with ensemble ML: the "
    "best-performing model for MAT (Ridge R² = 0.32) is within one standard error of the "
    "Random Forest. Nevertheless, fossil transfer against CLAMP yields R² values of 0.65 "
    "(MAT), 0.82 (CMMT), 0.73 (growing season), 0.39 (SH), and 0.68 (ENTHAL), though "
    "this validation is dominated by Asian assemblages (65 of 71 sites), inflating apparent "
    "transfer success for regions with dense modern spatial sampling. Our results argue "
    "that spatial cross-validation is mandatory for honest assessment of leaf-trait-based "
    "paleoclimate models and that the true geographic generalisability of these models may "
    "be substantially narrower than previously reported."
)

kw = doc.add_paragraph()
run = kw.add_run("Keywords: ")
run.bold = True
run.font.name = 'Times New Roman'
run.font.size = Pt(12)
run = kw.add_run(
    "leaf physiognomy, paleoclimate reconstruction, spatial cross-validation, "
    "machine learning, ensemble methods, CLAMP, Climate of the Past"
)
run.font.name = 'Times New Roman'
run.font.size = Pt(12)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ═══════════════════════════════════════════════════════════════════
add_heading("1 Introduction", level=1)

add_para(
    "The relationship between leaf morphology and climate is one of the oldest "
    "quantitative approaches in terrestrial paleoclimate science. Since the pioneering "
    "work of Bailey and Sinnott (1916), who demonstrated that the proportion of "
    "entire-margined woody dicot species correlates with mean annual temperature, "
    "leaf physiognomic traits—tooth type, leaf size, apex and base form, length:width "
    "ratio, and overall shape—have been calibrated against modern climate observations "
    "to reconstruct past terrestrial conditions (Wolfe, 1971, 1979; Wilf, 1997). The "
    "Climate-Leaf Analysis Multivariate Program (CLAMP; Wolfe, 1993) formalised this "
    "approach using canonical correspondence analysis, and it remains the most widely "
    "used physiognomic method for paleoclimate inference."
)

add_para(
    "Recent years have seen a surge of interest in applying machine learning (ML) "
    "methods to leaf physiognomic data, driven by the hope that non-linear ensemble "
    "models might capture complex trait–climate relationships beyond the reach of "
    "linear methods (Peppe et al., 2011; Spicer et al., 2020; Lowe et al., 2024). "
    "Some studies have reported R² values exceeding 0.8 for key temperature variables "
    "under conventional cross-validation, and physiologically motivated multi-stage "
    "architectures—in which temperature predictions feed into downstream moisture "
    "or energy-balance estimates—have been proposed to transfer information across "
    "physically linked climate variables. However, these validation frameworks have "
    "typically not accounted for the spatial structure of the training data, leaving "
    "open the question of whether reported accuracies reflect true cross-region "
    "predictive skill or within-region interpolation."
)

add_para(
    "However, a fundamental concern has received insufficient attention: standard "
    "random k-fold cross-validation ignores the spatial autocorrelation inherent in "
    "geographic training data. Modern leaf-trait calibration sites are not independent "
    "draws from a global distribution—they cluster in well-sampled regions such as "
    "eastern Asia, Central America, and Oceania, while Africa and Europe are sparsely "
    "represented. When training and test sites are drawn from the same geographic "
    "clusters, model performance reflects within-region interpolation rather than "
    "cross-region generalisation—the ability actually required for fossil transfer "
    "(Roberts et al., 2017; Meyer et al., 2019; Ploton et al., 2020). This leakage "
    "is especially acute for paleoclimate applications, where target fossil sites may "
    "lie far from any modern training data in both space and time."
)

add_para(
    "Here we subject leaf-physiognomy climate prediction to a rigorous spatial "
    "cross-validation framework. Using a globally distributed calibration dataset "
    "of 393 modern woody dicot sites with 31 physiognomic trait proportions, we evaluate "
    "four ensemble learners and four statistical baselines under: (1) block-based "
    "spatial GroupKFold, where sites are partitioned by geographic grid blocks; "
    "(2) Leave-One-Continent-Out (LOCO) validation, holding out entire continents; "
    "and (3) fossil transfer against CLAMP-computed reference values for 71 fossil "
    "assemblages. We implement a leakage-free two-stage architecture in which Stage 1 "
    "predicts temperature variables from traits alone, and Stage 2 predicts moisture–"
    "energy variables from traits augmented with out-of-fold temperature estimates—"
    "ensuring that no fossil-site information leaks into the training signal. Our "
    "results reveal a dramatically different picture from that painted by random-fold "
    "estimates: under honest spatial validation, ensemble ML provides only marginal "
    "improvements over linear baselines, the two-stage architecture provides no benefit, "
    "and several climate variables prove fundamentally unpredictable from leaf traits "
    "when geographic structure is respected."
)

# ═══════════════════════════════════════════════════════════════════
# 2. DATA AND METHODS
# ═══════════════════════════════════════════════════════════════════
add_heading("2 Data and Methods", level=1)

add_heading("2.1 Modern calibration dataset", level=2)
add_para(
    "The modern calibration dataset comprises 393 woody dicotyledonous angiosperm sites "
    "spanning five continents (Asia: 158 sites; Americas: 143; Oceania: 53; Europe: 25; "
    "Africa: 14). For each site, 31 leaf physiognomic traits are recorded as compositional "
    "proportions (summing to 1 within each trait category), following the CLAMP protocol "
    "(Wolfe, 1993; Yang et al., 2015). The traits span six morphological categories: tooth "
    "type (7 proportions: lobed, no teeth, teeth regular, teeth close, teeth round, teeth "
    "acute, teeth compound), leaf size class (9 proportions: nanophyll through mesophyll 3), "
    "apex form (4 proportions: emarginate, round, acute, attenuate), base form (3 "
    "proportions: cordate, round, acute), length:width ratio (5 proportions: <1:1 through "
    ">4:1), and general shape (3 proportions: obovate, elliptic, ovate). Associated climate "
    "data for the seven target variables—mean annual temperature (MAT), warm-month mean "
    "temperature (WMMT), cold-month mean temperature (CMMT), growing-season length "
    "(GROWSEAS), relative humidity (RH), specific humidity (SH), and moist enthalpy "
    "(ENTHAL)—were extracted from the WorldClim 2 global gridded climate dataset "
    "(Fick and Hijmans, 2017) at the geographic coordinates of each site."
)

add_heading("2.2 Fossil assemblages", level=2)
add_para(
    "The fossil dataset consists of 71 leaf assemblages spanning the Cretaceous through "
    "Quaternary, predominantly from Asia (65 assemblages: Tibetan Plateau, Yunnan, "
    "northeast India, Myanmar, Vietnam, Guangxi, Guangdong), with four European "
    "(Spain, Poland) and one North American (Florissant, Colorado) assemblage. "
    "CLAMP-computed climate values serve as reference targets for fossil transfer "
    "validation. We note that CLAMP reference values are not independent observations "
    "but model-derived estimates, and that fossil reference values are available only "
    "for those variables and assemblages that CLAMP can resolve. The Asian dominance "
    "of the fossil set (92% of assemblages) is an inherent limitation of the available "
    "data but must be considered when interpreting fossil transfer performance."
)

add_heading("2.3 Spatial cross-validation framework", level=2)
add_para(
    "To prevent geographic data leakage, we construct spatial cross-validation folds by "
    "dividing the globe into two-dimensional grid blocks based on latitude and longitude "
    "percentiles (5 latitudinal bands × 4 longitudinal bands, yielding ≤20 spatial blocks). "
    "Each site is assigned to a unique block, and GroupKFold (with spatial block as the "
    "grouping variable) ensures that all sites within the same geographic block are "
    "assigned exclusively to either training or test sets within each fold. This prevents "
    "any within-block spatial autocorrelation from inflating validation metrics. We use "
    "10-fold GroupKFold (constrained by the number of valid blocks) and report the mean "
    "and standard deviation of R² and RMSE across folds."
)

add_heading("2.4 Two-stage prediction architecture", level=2)
add_para(
    "Following the physical cascade from temperature to moisture–energy variables, we "
    "implement a two-stage architecture: Stage 1 predicts the four temperature variables "
    "(MAT, WMMT, CMMT, GROWSEAS) from the 31 trait proportions alone, generating "
    "out-of-fold (OOF) predictions for all 393 modern sites. Stage 2 predicts the three "
    "moisture–energy variables (RH, SH, ENTHAL) from an augmented feature set comprising "
    "the 31 traits plus the four OOF temperature predictions from Stage 1. Critically, "
    "OOF predictions are generated using models trained on different spatial folds, "
    "guaranteeing that no target-site temperature information leaks into the Stage 2 "
    "training data. We also train a traits-only ablation model (31 traits → moisture "
    "variable, without temperature augmentation) to quantify the contribution of the "
    "two-stage design."
)

add_heading("2.5 Models and baselines", level=2)
add_para(
    "We evaluate four ensemble learners: Random Forest (RF; n_estimators=500, max_depth=12, "
    "min_samples_leaf=3), XGBoost (n_estimators=300, max_depth=5, learning_rate=0.03), "
    "Gradient Boosting (GBDT; n_estimators=300, max_depth=4, learning_rate=0.03), and "
    "Support Vector Regression (SVR; RBF kernel, C=10.0). Hyperparameters were optimised "
    "for spatial generalisation through stronger regularisation (limited tree depth, "
    "increased minimum samples per leaf) rather than through grid search against random-fold "
    "CV, which would itself be susceptible to spatial leakage. Four statistical baselines "
    "are included: ordinary least squares linear regression, Ridge regression with "
    "cross-validated alpha, ElasticNet with cross-validated L1 ratio and alpha, and "
    "Partial Least Squares regression (PLS; n_components=4). All models are trained on the "
    "same spatial folds. For tree-based models we omit QuantileTransformer preprocessing, "
    "as the compositional trait data (proportions bounded in [0,1]) are monotonic-invariant "
    "under tree splits."
)

add_heading("2.6 Leave-One-Continent-Out (LOCO) validation", level=2)
add_para(
    "To assess cross-continent generalisability, we perform LOCO validation using a "
    "Random Forest on all seven targets. For each continent (Asia, Americas, Oceania, "
    "Europe, Africa), all sites belonging to that continent are held out as the test set, "
    "and the model is trained on the remaining continents. This provides a realistic "
    "upper bound on the model's ability to predict climate for fossil sites located on "
    "continents with sparse or absent modern training data."
)

add_heading("2.7 Fossil transfer evaluation", level=2)
add_para(
    "Final models are trained on the full 393 modern sites using the optimised "
    "hyperparameters and evaluated on the 71 fossil assemblages. For temperature "
    "variables, the Stage 1 RF model trained on all modern data is applied directly "
    "to fossil traits. For moisture–energy variables, a Stage 2 RF model is trained "
    "on modern sites using traits + Stage 1 OOF temperature predictions, then applied "
    "to fossil traits augmented with fossil temperature predictions from Stage 1. "
    "Performance is reported as R², RMSE, and mean bias against the CLAMP reference "
    "values. We do not perform statistical testing on fossil transfer metrics, as the "
    "CLAMP targets are model-derived rather than instrumental observations."
)

# ═══════════════════════════════════════════════════════════════════
# 3. RESULTS
# ═══════════════════════════════════════════════════════════════════
add_heading("3 Results", level=1)

# ─── 3.1 Trait–Climate Correlations + Fig 1 ───
add_heading("3.1 Trait–climate correlations", level=2)
add_para(
    "Spearman rank correlations between the 31 leaf physiognomic traits and seven climate "
    "variables reveal structured but generally moderate associations (Fig. 1). The "
    "strongest single-trait correlations are observed between the proportion of entire-"
    "margined leaves (No Teeth) and MAT (ρ = 0.52, p < 0.001), consistent with the "
    "classic leaf-margin analysis, and between mesophyll size classes and warm, wet "
    "climates (Mesophyll 3 vs SH: ρ = 0.48, p < 0.001). Tooth type traits exhibit "
    "the broadest climate correlations, particularly with temperature variables, while "
    "leaf shape traits (obovate, elliptic, ovate) show the weakest climate associations "
    "overall. The correlation structure supports the established interpretation that leaf "
    "morphology carries detectable but noisy climate signal across the 393-site sample."
)

add_figure("Fig1_trait_climate_corr",
    "Figure 1: Spearman rank correlation between 31 leaf physiognomic traits and seven climate "
    "variables across 393 modern woody dicot sites. Trait categories are indicated by coloured "
    "sidebars: tooth type (red), leaf size class (blue), apex form (green), base form (orange), "
    "L:W ratio (purple), and general shape (teal). Filled circles indicate p < 0.01 after "
    "Bonferroni correction.")

doc.add_page_break()

# ─── 3.2 Spatial CV Performance + Fig 2 ───
add_heading("3.2 Spatial cross-validation performance", level=2)
add_para(
    "Under block-based spatial cross-validation, the performance of all models is "
    "substantially lower than what would be obtained from random k-fold estimates "
    "(Fig. 2; Table 1). The Random Forest achieves a spatial CV R² of 0.383 ± 0.438 "
    "for MAT (RMSE = 3.82 °C), while the best baseline (Linear Regression) reaches "
    "R² = 0.343. For the remaining targets, performance under spatial CV is poor to "
    "negative: WMMT R² = −0.321 (best baseline ElasticNet: −0.284), CMMT R² = −0.013 "
    "(best baseline PLS: −0.238), and GROWSEAS R² = 0.099 (best baseline Linear "
    "Regression: 0.138). For moisture–energy variables, spatial CV R² values are "
    "RH = −0.331, SH = 0.136, and ENTHAL = 0.299. These results reveal a striking "
    "pattern: the four linear baseline methods are statistically indistinguishable "
    "from the ensemble learners for most targets, and in several cases (GROWSEAS, "
    "ENTHAL), the best baseline outperforms or equals the best ML model."
)

add_figure("Fig2_model_comparison",
    "Figure 2: Spatial cross-validation performance comparison across five statistical and "
    "machine learning models for six climate variables. Bars show mean R² from block-based "
    "spatial GroupKFold (10 folds). WMMT is omitted due to uniformly negative performance "
    "across all models. Vertical dashed line separates temperature (left) and moisture–energy "
    "(right) targets.")

add_para(
    "For moisture–energy targets, the traits-only ablation (31 traits → SH, RH, ENTHAL) "
    "consistently outperforms the two-stage architecture under spatial CV (Fig. 5a; "
    "Table 4). For SH, the traits-only Random Forest achieves R² = 0.235 versus 0.136 "
    "for the two-stage RF (Δ = −0.099). For ENTHAL, the trait-only RF R² = 0.391 versus "
    "0.299 (Δ = −0.092). This degradation is consistent across all four ensemble learners: "
    "adding OOF temperature predictions as features introduces noise that outweighs any "
    "physical information content under honest spatial partitioning. The physically "
    "motivated cascade from temperature to moisture–energy prediction does not survive "
    "spatial cross-validation."
)

doc.add_page_break()

# ─── 3.3 LOCO + Fig 3 ───
add_heading("3.3 Leave-One-Continent-Out validation", level=2)
add_para(
    "LOCO results (Fig. 3; Table 2) confirm the spatial fragility of trait-based climate "
    "prediction. When models are trained on all continents except one and tested on the "
    "held-out continent, performance varies dramatically by continent and target variable. "
    "For MAT, the model achieves positive R² for Asia (0.408), the Americas (0.448), "
    "Oceania (0.323), and Africa (0.231), but fails catastrophically for Europe "
    "(R² = −1.035), where only 25 training sites are available and the European held-out "
    "sites span a climate space poorly represented in the remaining continents. CMMT shows "
    "an even starker pattern: R² = 0.496 for the Americas but −1.430 for Europe. The "
    "three moisture–energy variables (RH, SH, ENTHAL) show moderate LOCO performance for "
    "Asia, the Americas, and Oceania, but uniformly negative R² for Europe, highlighting "
    "the model's dependence on dense within-continent spatial sampling in the training set."
)

add_heading("3.4 Fossil transfer evaluation", level=2)
add_para(
    "Fossil transfer against CLAMP reference values yields mixed results that reflect "
    "the strong Asian bias in the fossil dataset (Fig. 3; Table 1). For temperature "
    "variables, fossil R² ranges from 0.646 (MAT, RMSE = 2.74 °C, bias = −1.69 °C) to "
    "0.820 (CMMT, RMSE = 2.79 °C, bias = −0.98 °C). GROWSEAS achieves fossil R² = 0.730 "
    "(RMSE = 1.01 months), while WMMT yields R² = −1.056 (RMSE = 2.91 °C), indicating "
    "that the model cannot reconstruct warm-month mean temperature for these fossil "
    "assemblages. For moisture–energy variables, ENTHAL achieves fossil R² = 0.681 "
    "(RMSE = 9.68 kJ/kg) and SH achieves 0.385 (RMSE = 2.95 g/kg), while RH is "
    "essentially unpredictable (R² = −0.080). A systematic cold bias is evident across "
    "all fossil predictions (MAT bias = −1.69 °C; ENTHAL bias = −4.90 kJ/kg), likely "
    "reflecting the dominance of mid-to-high-latitude Asian fossil sites whose modern "
    "analogues are similarly concentrated in the training distribution."
)

add_figure("Fig3_obs_vs_pred",
    "Figure 3: Fossil transfer evaluation and cross-continent validation. (a–e) Predicted vs "
    "CLAMP reference values for five climate variables across 71 fossil assemblages; dashed "
    "line indicates identity. Marker colours distinguish temperature (blue) and moisture–energy "
    "(red) targets. (f) Leave-One-Continent-Out R² heatmap for five climate variables across "
    "five continents.")

add_para(
    "Critically, the apparent fossil transfer success for CMMT and GROWSEAS (R² > 0.7) "
    "must be interpreted in light of the fossil dataset composition: 65 of 71 assemblages "
    "are from Asia, where the modern calibration set is densest (158 of 393 sites). The "
    "spatial CV R² for CMMT on modern data is −0.013, meaning that the model cannot "
    "predict CMMT across unseen spatial blocks—yet the fossil transfer R² reaches 0.820. "
    "This discrepancy arises because the fossil sites lie within the same geographic "
    "domain as the modern calibration data, and the transfer effectively amounts to "
    "within-region interpolation rather than cross-region generalisation."
)

doc.add_page_break()

# ─── 3.5 Feature Importance + Fig 4 ───
add_heading("3.5 Feature importance", level=2)
add_para(
    "Random Forest feature importance analysis across all seven targets (Fig. 4a) "
    "reveals that tooth-type traits dominate the importance ranking for temperature "
    "prediction, accounting for approximately 40% of MAT variance explained, followed "
    "by leaf size categories (~35%) and apex form (~12%). Base form and shape traits "
    "contribute minimally (Fig. 4c). The top 10 individual features for MAT (Fig. 4b) "
    "are led by No Teeth (entire margin), which alone accounts for ~15% of RF importance "
    "for MAT, consistent with the leaf-margin analysis tradition. For moisture–energy "
    "variables, leaf size traits dominate, with mesophyll classes contributing the "
    "largest share, reflecting the physical link between leaf size and water availability."
)

add_figure("Fig4_feature_importance",
    "Figure 4: Feature importance analysis. (a) Random Forest feature importance heatmap across "
    "all seven climate variables. (b) Top 10 features by importance for MAT. (c) Trait-category "
    "contribution to MAT importance (pie chart).")

# ─── Two-Stage Ablation + Fig 5 ───
add_heading("3.6 Two-stage architecture ablation", level=2)
add_para(
    "The two-stage architecture—predicting temperature first, then using those predictions "
    "to inform moisture–energy estimates—is motivated by the physical cascade of climate "
    "variables: atmospheric moisture content depends on temperature through the "
    "Clausius–Clapeyron relationship, and specific humidity and enthalpy are functions of "
    "both moisture and temperature. However, under spatial cross-validation, the addition "
    "of out-of-fold temperature predictions consistently degrades moisture–energy prediction "
    "relative to a traits-only model (Fig. 5a). We attribute this to error propagation: "
    "Stage 1 temperature predictions carry spatial biases, and these biases are amplified "
    "when the noisy temperature estimates are fed into Stage 2. The traits-only approach, "
    "though physically less motivated, avoids this cascade of errors. "
    "Figure 5b compares spatial CV R² against fossil transfer R², illustrating the gap "
    "between honest modern validation and the apparently successful—but geographically "
    "constrained—fossil transfer for Asian-dominated target sites."
)

add_figure("Fig5_two_stage_ablation",
    "Figure 5: Two-stage architecture assessment. (a) Scatter plot comparing spatial CV R² of "
    "traits-only vs two-stage models for moisture–energy variables (SH, ENTHAL, RH); points "
    "below the identity line indicate two-stage degradation. (b) Bar chart comparing spatial "
    "CV R² against fossil transfer R² (vs CLAMP) for five climate variables.")

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# 4. DISCUSSION
# ═══════════════════════════════════════════════════════════════════
add_heading("4 Discussion", level=1)

add_heading("4.1 Spatial cross-validation as a mandatory standard", level=2)
add_para(
    "Our results demonstrate that spatial cross-validation is not merely a methodological "
    "nicety but a scientific necessity for leaf-physiognomy paleoclimate models. The "
    "dramatic gap between random-fold estimates reported in previous work (R² > 0.8−0.9) "
    "and the spatial CV results obtained here (best MAT R² = 0.38) reveals how severely "
    "geographic data leakage can inflate perceived model performance. When modern "
    "calibration sites from the same region are split randomly between training and test "
    "sets, the model learns to interpolate within geographic clusters rather than to "
    "extrapolate across them—a skill that is irrelevant for fossil transfer, where all "
    "target sites lie in the deep past and may be geographically distant from any modern "
    "training data. This finding aligns with a growing body of evidence in ecological "
    "modelling (Roberts et al., 2017; Ploton et al., 2020) and remote sensing (Meyer "
    "et al., 2019; Radočaj et al., 2025) showing that random cross-validation yields "
    "optimistically biased estimates of spatial prediction accuracy."
)

add_heading("4.2 The limits of non-linear machine learning for trait-based climate inference", level=2)
add_para(
    "A central finding of this study is that ensemble ML provides at best marginal "
    "improvements over linear statistical baselines for leaf-trait-based climate "
    "prediction under spatial validation. For MAT, the Random Forest gains only 0.04 in "
    "R² over the best linear model (Ridge), while for GROWSEAS, the best baseline "
    "(Linear Regression, R² = 0.138) actually outperforms the best ML model (RF, "
    "R² = 0.099). This suggests that the trait–climate relationship, though complex, "
    "is approximately linear within the signal extractable under spatial CV. Non-linear "
    "models may capture within-region residual structure that does not generalise across "
    "geographic boundaries—a form of spatial overfitting that is invisible under random "
    "cross-validation. For paleoclimate applications, where the goal is explicitly "
    "cross-region and cross-time transfer, the additional complexity of ensemble methods "
    "may not be justified by the marginal accuracy gains."
)

add_heading("4.3 Interpreting fossil transfer performance", level=2)
add_para(
    "The apparent success of fossil transfer for CMMT (R² = 0.82) despite negative "
    "spatial CV R² (−0.013) presents a paradox that requires careful interpretation. "
    "The resolution lies in the geographic structure of the fossil dataset: 92% of "
    "assemblages are from Asia, where modern calibration sites are densest. The fossil "
    "transfer for these targets is effectively a within-region interpolation exercise, "
    "not a test of cross-region generalisation. This is corroborated by the LOCO results: "
    "CMMT achieves R² = 0.50 for the Americas and 0.31 for Oceania, but fails for Europe "
    "(R² = −1.43). The high fossil R² for CMMT therefore reflects the Asian dominance of "
    "the fossil set rather than any global predictive capability."
)

add_para(
    "For MAT, fossil R² = 0.65 is stronger than what spatial CV on modern data would "
    "suggest (0.38), but the systematic cold bias (−1.69 °C) indicates that the model "
    "does not recover absolute temperature levels reliably. The growing-season length "
    "estimate (fossil R² = 0.73, bias = −0.27 months) is the most robust of the "
    "temperature predictions. Among moisture–energy variables, ENTHAL (R² = 0.68) "
    "transfers reasonably well, while SH (R² = 0.39) and RH (R² = −0.08) do not. "
    "We caution that fossil transfer R² against CLAMP targets is not a fully independent "
    "validation, as CLAMP itself uses the same leaf-trait information to compute its "
    "reference values."
)

add_heading("4.4 Which climate variables can leaf traits reconstruct?", level=2)
add_para(
    "Our spatial CV framework identifies a clear hierarchy of reconstructability from "
    "leaf physiognomic traits. MAT and ENTHAL show modest but consistent spatial "
    "prediction skill (R² ≈ 0.3−0.4), while SH, GROWSEAS, and CMMT hover near zero. "
    "WMMT and RH are fundamentally unpredictable from leaf traits alone under spatial CV "
    "(R² < −0.3). This hierarchy is consistent with the physical basis of leaf "
    "morphology: leaf margin and size respond primarily to growing-season temperature "
    "and water balance, while warm-month extremes and relative humidity have weaker "
    "physiological links to the morphological traits measured. The strong fossil CMMT "
    "performance (R² = 0.82) despite negative spatial CV R² is a cautionary example of "
    "how within-domain interpolation can be mistaken for predictive skill. We recommend "
    "that future leaf-physiognomy reconstruction studies report spatial CV metrics "
    "alongside fossil transfer results, and that the reconstructability hierarchy "
    "identified here inform which climate variables are targeted."
)

add_heading("4.5 Limitations", level=2)
add_para(
    "Several limitations warrant mention. First, the modern calibration dataset is "
    "geographically imbalanced, with Europe (25 sites) and Africa (14 sites) severely "
    "underrepresented; the poor LOCO performance for Europe reflects this imbalance "
    "rather than any inherent unpredictability of European leaf traits. Second, we "
    "use CLAMP-computed reference values for fossil validation, which are not independent "
    "of the leaf-trait data and may carry their own biases. Independent validation "
    "against non-physiognomic proxies (e.g., isotopic, palynological) for key fossil "
    "sites would strengthen the fossil transfer assessment. Third, the 31-trait CLAMP "
    "protocol captures a subset of leaf morphological variation; additional traits "
    "(e.g., venation density, stomatal indices) could improve spatial generalisability, "
    "though they were not available for this dataset. Fourth, our spatial block "
    "partitioning (5 × 4 grid) is one of many possible schemes; sensitivity to block "
    "resolution warrants further study. Finally, the temporal dimension—whether trait–"
    "climate calibrations from modern vegetation apply to fossil floras separated by "
    "millions of years of evolution—remains an irreducible uncertainty in all uniformitarian "
    "paleoclimate methods."
)

# ═══════════════════════════════════════════════════════════════════
# 5. CONCLUSIONS
# ═══════════════════════════════════════════════════════════════════
add_heading("5 Conclusions", level=1)

add_para(
    "This study demonstrates that spatial cross-validation reveals fundamental limits to "
    "leaf-physiognomy-based climate reconstruction that are invisible under conventional "
    "random-fold validation. On a globally distributed dataset of 393 modern woody dicot "
    "sites, ensemble machine learning achieves only marginal improvements over linear "
    "statistical baselines when geographic structure is respected, and the physically "
    "motivated two-stage prediction architecture fails to improve moisture–energy estimates "
    "under honest spatial partitioning. Fossil transfer against CLAMP reference values "
    "yields promising results for Asian-dominated target sites, particularly for CMMT "
    "(R² = 0.82) and ENTHAL (R² = 0.68), but this performance reflects within-region "
    "interpolation rather than cross-continent generalisation. We recommend that spatial "
    "cross-validation become a mandatory reporting standard for all ML-based paleoclimate "
    "reconstruction studies, that linear baselines be included in every model comparison, "
    "and that the limited geographic generalisability of trait-based climate models be "
    "explicitly acknowledged when interpreting fossil climate estimates. The tools "
    "developed here—spatial GroupKFold, LOCO validation, and baseline-inclusive model "
    "benchmarking—provide a reproducible framework for honest assessment of paleoclimate "
    "machine learning methods."
)

# ═══════════════════════════════════════════════════════════════════
# DATA AND CODE AVAILABILITY
# ═══════════════════════════════════════════════════════════════════
add_heading("Data and Code Availability", level=1)

add_para(
    "The modern calibration dataset and fossil assemblage data used in this study are "
    "available in the accompanying Excel workbook (Global378+Tibet15+Fossil73_更正.xlsx). "
    "All training code, the spatial cross-validation pipeline, figure generation scripts, "
    "trained model files, and the complete manuscript source are archived on Zenodo "
    "[DOI to be created upon acceptance] and publicly available on GitHub at "
    "[repository URL to be added]. The repository includes: (1) training_pipeline_v2.py, "
    "which reproduces all spatial CV results, baseline comparisons, LOCO validation, and "
    "fossil transfer evaluation; (2) generate_figures_v2.py, which produces all five "
    "publication figures; (3) the models_v2/ directory containing trained joblib model "
    "files; and (4) the output/ directory containing all tabulated results "
    "(Tables 1–5). All analyses were performed in Python 3.10 using scikit-learn 1.3, "
    "XGBoost 2.0, and associated scientific Python libraries. Climate data were obtained "
    "from WorldClim 2 (Fick and Hijmans, 2017; https://www.worldclim.org/)."
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
# REFERENCES
# ═══════════════════════════════════════════════════════════════════
add_heading("References", level=1)

refs = [
    "Bailey, I. W. and Sinnott, E. W.: The climatic distribution of certain types of angiosperm leaves, Am. J. Bot., 3, 24–39, 1916.",
    "Chen, W.-Y., Su, T., and Li, S.-F.: The leaf physiognomy of evergreen and deciduous species exhibits different responses to climate: Implications for palaeoclimate reconstruction in China, Palaeogeogr. Palaeoclimatol. Palaeoecol., 660, 112683, https://doi.org/10.1016/j.palaeo.2024.112683, 2025.",
    "Fick, S. E. and Hijmans, R. J.: WorldClim 2: new 1-km spatial resolution climate surfaces for global land areas, Int. J. Climatol., 37, 4302–4315, https://doi.org/10.1002/joc.5086, 2017.",
    "Lowe, A. J., Flynn, A. G., Butrim, M. J., Baumgartner, A., Royer, D. L., and Peppe, D. J.: Reconstructing terrestrial paleoclimate and paleoecology with fossil leaves using digital leaf physiognomy and leaf mass per area, J. Vis. Exp., 212, e66838, https://doi.org/10.3791/66838, 2024.",
    "Meyer, H., Reudenbach, C., Wöllauer, S., and Nauss, T.: Importance of spatial predictor variable selection in machine learning applications—Moving from data reproduction to spatial prediction, Ecol. Model., 411, 108815, https://doi.org/10.1016/j.ecolmodel.2019.108815, 2019.",
    "Peppe, D. J., Royer, D. L., Cariglino, B., Oliver, S. Y., Newman, S., Leight, E., Enikolopov, G., Fernandez-Burgos, M., Herrera, F., Adams, J. M., Correa, E., Currano, E. D., Erickson, J. M., Hinojosa, L. F., Hoganson, J. W., Iglesias, A., Jaramillo, C. A., Johnson, K. R., Jordan, G. J., Kraft, N. J. B., Lovelock, E. C., Lusk, C. H., Niinemets, Ü., Peñuelas, J., Rapson, G., Wing, S. L., and Wright, I. J.: Sensitivity of leaf size and shape to climate: global patterns and paleoclimatic applications, New Phytol., 190, 724–739, https://doi.org/10.1111/j.1469-8137.2010.03615.x, 2011.",
    "Ploton, P., Mortier, F., Réjou-Méchain, M., Barbier, N., Picard, N., Rossi, V., Dormann, C., Cornu, G., Viennois, G., Bayol, N., Lyapustin, A., Gourlet-Fleury, S., and Pélissier, R.: Spatial validation reveals poor predictive performance of large-scale ecological mapping models, Nat. Commun., 11, 4540, https://doi.org/10.1038/s41467-020-18321-y, 2020.",
    "Radočaj, D., Plaščak, I., and Jurišić, M.: A comparative assessment of regular and spatial cross-validation in subfield machine learning prediction of maize yield from Sentinel-2 phenology, Eng, 6, 270, https://doi.org/10.3390/eng6100270, 2025.",
    "Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J. J., Schröder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F., and Dormann, C. F.: Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure, Ecography, 40, 913–929, https://doi.org/10.1111/ecog.02881, 2017.",
    "Spicer, R. A., Valdes, P. J., Hughes, A., Yang, J., Spicer, T. E. V., Herman, A., and Farnsworth, A.: New insights into the thermal regime and hydrodynamics of the early Late Cretaceous Arctic, Geol. Mag., 157, 1729–1746, https://doi.org/10.1017/S0016756819000465, 2020.",
    "Wilf, P.: When are leaves good thermometers? A new case for leaf margin analysis, Paleobiology, 23, 373–390, 1997.",
    "Wolfe, J. A.: Tertiary climatic fluctuations and methods of analysis of Tertiary floras, Palaeogeogr. Palaeoclimatol. Palaeoecol., 9, 27–57, 1971.",
    "Wolfe, J. A.: Temperature parameters of humid to mesic forests of eastern Asia and relation to forests of other regions of the Northern Hemisphere and Australasia, US Geol. Surv. Prof. Pap., 1106, 1–37, 1979.",
    "Wolfe, J. A.: A method of obtaining climatic parameters from leaf assemblages, US Geol. Surv. Bull., 2040, 1–71, 1993.",
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

add_heading("Table 1: Summary of model performance under spatial cross-validation, baseline comparison, and fossil transfer.", level=2)
add_para("Spatial CV metrics are from block-based GroupKFold (10 folds). Best Baseline is the top-performing statistical model for each variable. Two-Stage ΔR² is the change from traits-only to two-stage architecture (moisture–energy variables only). Fossil metrics are R², RMSE, and mean bias vs CLAMP reference values (N = 71 assemblages).", italic=True)

table1 = doc.add_table(rows=8, cols=9)
table1.style = 'Light Grid Accent 1'
headers1 = ['Variable', 'Category', 'Spatial CV\nR² (RF)', 'Spatial CV\nRMSE',
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
add_para("R² values for each variable–continent combination. N is the number of held-out sites.", italic=True)

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
output_path = os.path.join(BASE_DIR, "Manuscript_Paleoclimate_ML_CP_v4.docx")
doc.save(output_path)
print(f"Manuscript with embedded figures saved to: {output_path}")
print(f"  Embedded figures: Fig1-5")
