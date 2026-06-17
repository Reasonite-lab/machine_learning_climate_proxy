#!/usr/bin/env python3
"""
Build manuscript v7 — ML-limitations focus.
Core argument: Ensemble ML does not improve leaf-physiognomy paleoclimate
reconstruction under honest spatial validation. The cross-region signal is
essentially linear, physically-motivated multi-stage architectures collapse
under spatial partitioning, and apparent fossil transfer success reflects
regional interpolation rather than generalisable prediction.

Refs: 25 citations, alphabetical order.
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


# ═══════════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════════
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run(
    "Limited benefits of ensemble machine learning for "
    "leaf-physiognomy paleoclimate reconstruction"
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


# ═══════════════════════════════════════════════════
# ABSTRACT
# ═══════════════════════════════════════════════════
add_heading("Abstract", level=1)

add_para(
    "Ensemble machine learning methods have been increasingly applied to leaf-physiognomy "
    "paleoclimate reconstruction, motivated by the expectation that non-linear models can "
    "capture complex trait–climate interactions beyond the reach of linear methods. Several "
    "recent studies have reported high coefficients of determination for temperature and "
    "moisture variables, and physically motivated multi-stage architectures have been proposed "
    "to cascade information across linked climate variables. However, the validation strategies "
    "used in these studies—primarily random k-fold cross-validation—do not account for the "
    "spatial autocorrelation inherent in geographically clustered calibration data, and may "
    "therefore overstate model generalisability. We evaluate whether ensemble learning provides "
    "genuine benefits over simpler statistical baselines when spatial structure is respected."
)

add_para(
    "Using a global dataset of 393 modern woody dicot sites with 31 leaf physiognomic traits, "
    "we compare four ensemble learners (Random Forest, XGBoost, Gradient Boosting, SVR) against "
    "four linear baselines (ordinary least squares, Ridge, ElasticNet, PLS) for predicting seven "
    "climate variables. All models are evaluated under space-block GroupKFold, which partitions "
    "sites into contiguous geographic blocks to prevent within-domain information leakage. We also "
    "test a physically motivated two-stage architecture (temperature→moisture cascade) under "
    "leak-free spatial partitioning, and evaluate fossil transfer against 71 predominantly Asian "
    "assemblages. Under space-block validation, ensemble learners provide no statistically "
    "meaningful improvement over linear baselines: for mean annual temperature (MAT), the best "
    "ensemble (Random Forest, R² = 0.38) outperforms the best linear model (OLS, R² = 0.34) by "
    "only 0.04, a difference within one standard deviation of the cross-validation folds. The "
    "two-stage cascade consistently degrades moisture–energy prediction relative to traits-only "
    "models, indicating that error propagation across geographic space outweighs any physical "
    "information content of the cascade. Fossil transfer against CLAMP reference values yields "
    "apparently strong results (MAT R² = 0.65, CMMT R² = 0.82), but 92% of fossil assemblages "
    "are Asian, meaning these metrics reflect within-domain interpolation, not cross-region "
    "generalisability. We conclude that the cross-region trait–climate signal is essentially "
    "linear, that ensemble complexity does not translate into greater geographic generalisability, "
    "and that spatial validation with linear baselines should be standard practice for future "
    "machine learning applications in leaf-physiognomy paleoclimate reconstruction."
)

kw = doc.add_paragraph()
run = kw.add_run("Keywords: ")
run.bold = True
run.font.name = 'Times New Roman'
run.font.size = Pt(12)
run = kw.add_run(
    "machine learning, ensemble methods, leaf physiognomy, paleoclimate reconstruction, "
    "spatial validation, model generalisability, overfitting"
)
run.font.name = 'Times New Roman'
run.font.size = Pt(12)

doc.add_page_break()


# ═══════════════════════════════════════════════════
# 1. INTRODUCTION
# ═══════════════════════════════════════════════════
add_heading("1 Introduction", level=1)

add_para(
    "Machine learning (ML) methods have transformed numerous fields of Earth and environmental "
    "science over the past decade, offering the promise of detecting complex, non-linear patterns "
    "in high-dimensional data that escape classical statistical approaches. In paleoclimatology, "
    "ensemble methods such as Random Forest, gradient-boosted trees, and support vector machines "
    "have been applied to problems ranging from climate-proxy calibration to paleovegetation "
    "reconstruction. A key appeal of these methods is their capacity to model interactions among "
    "predictor variables without pre-specifying their functional form—a property that is "
    "particularly attractive when the underlying physical relationships are poorly constrained."
)

add_para(
    "Leaf physiognomy—the morphological characteristics of fossil and modern leaves—represents "
    "a natural target for ML-based paleoclimate reconstruction. Woody dicot leaf traits, including "
    "margin type, size class, apex and base form, length-to-width ratio, and overall shape, exhibit "
    "well-documented correlations with climate variables such as mean annual temperature (MAT) and "
    "growing-season moisture availability (Bailey and Sinnott, 1916; Wolfe, 1993; Wilf, 1997; "
    "Peppe et al., 2011; Wright et al., 2017). The Climate-Leaf Analysis Multivariate Program "
    "(CLAMP; Wolfe, 1993; Spicer, 2009) formalised multivariate leaf physiognomy–climate calibration "
    "using canonical correspondence analysis and has been widely applied, particularly for "
    "reconstructing the paleoelevation history of the Tibetan Plateau (Spicer et al., 2021; "
    "He et al., 2022; Ding et al., 2022). A defining feature of CLAMP is its use of region-specific "
    "calibration datasets, reflecting the recognition that leaf–climate relationships vary across "
    "floristic provinces with distinct evolutionary histories (Wolfe, 1979; Yang et al., 2015)."
)

add_para(
    "Recent work has applied ensemble ML methods to the CLAMP trait dataset, often reporting "
    "substantially higher cross-validated performance than traditional multivariate calibration. "
    "Some studies have reported coefficients of determination exceeding 0.8 for key temperature "
    "variables, and multi-stage architectures—in which predicted temperatures inform downstream "
    "moisture or energy-balance estimates—have been proposed to exploit physical coupling among "
    "climate variables (Lowe et al., 2024; Chen et al., 2025). These results are encouraging, "
    "but they raise a methodological question: do the reported performance gains reflect genuine "
    "improvements in predictive power, or do they reflect validation strategies that underestimate "
    "the challenge of cross-region generalisation?"
)

add_para(
    "The question is not merely academic. Modern leaf-trait calibration sites are geographically "
    "clustered: East Asia (158 of 393 sites in our dataset) and the Americas (143 sites) dominate "
    "global sampling, while Europe (25 sites) and Africa (14 sites) are sparsely represented. "
    "Random k-fold cross-validation partitions sites irrespective of their geographic coordinates, "
    "allowing training and test sites from the same region to appear in different folds. This inflates "
    "validation metrics because the model can exploit within-region structure—the ecological sorting "
    "of leaf forms along local environmental gradients—without learning relationships that transfer "
    "across floristic provinces. The ecological modelling and remote-sensing communities have "
    "documented this pattern extensively: spatial blocking consistently reveals substantially lower "
    "predictive performance than random cross-validation, because spatial autocorrelation acts as "
    "a hidden information channel (Roberts et al., 2017; Meyer et al., 2019; Ploton et al., 2020). "
    "For paleoclimate reconstruction, the stakes are high: fossil leaf assemblages are typically "
    "distant from modern calibration sites in both space and time, so models must extrapolate across "
    "regions, not interpolate within them."
)

add_para(
    "Here we systematically evaluate whether ensemble ML methods provide genuine advantages over "
    "linear statistical baselines for leaf-physiognomy climate reconstruction when spatial structure "
    "is respected. Using a global dataset of 393 modern woody dicot sites with 31 physiognomic "
    "trait proportions, we test four ensemble learners (Random Forest, XGBoost, Gradient Boosting, "
    "SVR) against four linear baselines (ordinary least squares, Ridge, ElasticNet, PLS) for "
    "predicting seven climate variables under space-block GroupKFold. We also evaluate a physically "
    "motivated two-stage architecture—predicting temperature first, then feeding those estimates "
    "into moisture–energy prediction—under leak-free spatial partitioning, and assess fossil transfer "
    "against 71 assemblages to test real-world applicability. Our aim is not to identify the best "
    "single model, but to quantify whether ensemble complexity yields measurable benefits for "
    "cross-region paleoclimate inference, and to establish a reproducible baseline for future "
    "ML applications in this domain."
)


# ═══════════════════════════════════════════════════
# 2. DATA AND METHODS
# ═══════════════════════════════════════════════════
add_heading("2 Data and methods", level=1)

add_heading("2.1 Modern calibration dataset", level=2)
add_para(
    "The modern calibration dataset comprises 393 woody dicotyledonous angiosperm sites across "
    "five continents (Asia: 158 sites; Americas: 143; Oceania: 53; Europe: 25; Africa: 14). "
    "This geographic imbalance reflects the real-world distribution of botanical sampling effort "
    "and is consistent with prior CLAMP calibration datasets (Wolfe, 1993; Yang et al., 2015). "
    "For each site, 31 leaf physiognomic traits are recorded as compositional proportions summing "
    "to 1 within each trait category. The traits span six morphological categories: tooth type "
    "(7 proportions), leaf size class (9), apex form (4), base form (3), length:width ratio (5), "
    "and general shape (3), following the standard CLAMP protocol. Climate data for the seven "
    "target variables—mean annual temperature (MAT), warm-month mean temperature (WMMT), cold-month "
    "mean temperature (CMMT), growing-season length (GROWSEAS), relative humidity (RH), specific "
    "humidity (SH), and moist enthalpy (ENTHAL)—were extracted from WorldClim 2 (Fick and Hijmans, "
    "2017) at each site's geographic coordinates."
)

add_heading("2.2 Fossil assemblages", level=2)
add_para(
    "The fossil dataset contains 71 leaf assemblages spanning the Cretaceous through Quaternary, "
    "predominantly from Asia (65 assemblages: Tibetan Plateau, Yunnan, northeast India, Myanmar, "
    "Vietnam, Guangxi, Guangdong), with four European and one North American assemblage. CLAMP-computed "
    "climate values serve as reference targets for fossil transfer evaluation. Because CLAMP reference "
    "values are model-derived estimates rather than instrumental observations, we interpret fossil "
    "transfer results as a within-domain consistency check rather than independent validation. "
    "The Asian dominance of the fossil set (92% of assemblages) is an inherent feature of the "
    "available paleobotanical data (Su et al., 2019; He et al., 2022) and has important consequences "
    "for interpreting apparent fossil transfer performance."
)

add_heading("2.3 Space-block validation framework", level=2)
add_para(
    "The central methodological choice in this study is the validation scheme. We implement "
    "space-block GroupKFold: the globe is divided into grid blocks based on latitude and longitude "
    "percentiles (5 latitudinal bands × 4 longitudinal bands, yielding up to 20 spatial blocks), "
    "and each of the 393 modern sites is assigned to a unique block. GroupKFold, with spatial block "
    "as the grouping variable, ensures that all sites within the same block are placed exclusively "
    "in either training or test sets. This prevents any within-block spatial autocorrelation from "
    "inflating validation metrics. We use 10-fold GroupKFold (constrained by the number of valid "
    "blocks) and report mean and standard deviation of R² and RMSE across folds. All model "
    "comparisons—ensemble learners versus linear baselines, traits-only versus two-stage "
    "architectures—are conducted on identical spatial folds, so any performance differences "
    "are attributable to model choice rather than data partitioning."
)

add_heading("2.4 ML models and linear baselines", level=2)
add_para(
    "We evaluate four ensemble learners and four linear baselines. Ensemble learners: Random Forest "
    "(n_estimators=500, max_depth=12, min_samples_leaf=3), XGBoost (n_estimators=300, max_depth=5, "
    "learning_rate=0.03), Gradient Boosting (n_estimators=300, max_depth=4, learning_rate=0.03), "
    "and Support Vector Regression (RBF kernel, C=10.0). Hyperparameters were chosen to favour "
    "spatial generalisation through regularisation—limited tree depth, increased minimum samples "
    "per leaf—rather than through grid search optimised against a non-spatial objective, which would "
    "itself be vulnerable to overfitting. Linear baselines: ordinary least squares (OLS), Ridge "
    "regression with cross-validated alpha, ElasticNet with cross-validated L1 ratio and alpha, "
    "and Partial Least Squares (n_components=4). For tree-based models, we omit preprocessing "
    "transformations because compositional trait data (proportions bounded in [0,1]) are monotonic-"
    "invariant under tree splits. All models are trained and evaluated on identical spatial folds, "
    "enabling direct comparison of ensemble versus linear performance."
)

add_heading("2.5 Two-stage prediction architecture", level=2)
add_para(
    "A physically motivated two-stage architecture is tested under the same spatial folds. Stage 1 "
    "predicts the four temperature variables (MAT, WMMT, CMMT, GROWSEAS) from the 31 trait "
    "proportions, generating out-of-fold (OOF) predictions for all 393 modern sites. Each site's OOF "
    "prediction is produced by a model trained on spatial folds that exclude the site's block, "
    "guaranteeing that no target-site temperature information leaks into Stage 2. Stage 2 predicts "
    "the three moisture–energy variables (RH, SH, ENTHAL) from an augmented feature set comprising "
    "the 31 traits plus the four OOF temperature predictions. A traits-only baseline—predicting "
    "moisture–energy variables from the 31 traits without temperature augmentation—quantifies "
    "whether the two-stage design adds or subtracts information."
)

add_heading("2.6 Leave-One-Continent-Out validation", level=2)
add_para(
    "We evaluate cross-continent transferability using Leave-One-Continent-Out (LOCO) validation "
    "with Random Forest. For each of the five continents, all sites on that continent are held out "
    "as the test set while the model trains on the remaining continents. LOCO provides a stringent "
    "test of the geographic boundaries within which ML-based reconstruction is reliable, and directly "
    "quantifies the consequences of uneven geographic sampling for model generalisability."
)

add_heading("2.7 Fossil transfer evaluation", level=2)
add_para(
    "Final models are trained on all 393 modern sites and evaluated on the 71 fossil assemblages. "
    "For temperature variables, the Stage 1 Random Forest model is applied directly to fossil traits. "
    "For moisture–energy variables, a Stage 2 Random Forest trained on modern sites (traits + OOF "
    "temperature predictions) is applied to fossil traits augmented with Stage 1 fossil temperature "
    "predictions. Performance is reported as R², RMSE, and mean bias against CLAMP reference values. "
    "Because CLAMP targets are model-derived and 65 of 71 fossil assemblages are Asian, we treat "
    "fossil transfer as a measure of within-domain consistency, not as evidence of cross-region "
    "predictive capability."
)


# ═══════════════════════════════════════════════════
# 3. RESULTS
# ═══════════════════════════════════════════════════
add_heading("3 Results", level=1)

add_heading("3.1 Trait–climate correlation structure", level=2)
add_para(
    "Spearman rank correlations between the 31 leaf traits and seven climate variables across 393 "
    "modern sites revealed a structured but generally moderate association pattern (Fig. 1). The "
    "strongest single-trait correlation was between the proportion of entire-margined leaves (no "
    "teeth) and MAT (ρ = 0.52, p < 0.001), consistent with the classic leaf-margin analysis (Bailey "
    "and Sinnott, 1916; Wilf, 1997). Mesophyll size classes showed the strongest associations with "
    "moisture variables (mesophyll 3 vs. SH: ρ = 0.48, p < 0.001), reflecting the relationship "
    "between leaf size and water availability (Peppe et al., 2011). Tooth-type traits exhibited the "
    "broadest climate correlations overall, while shape traits (obovate, elliptic, ovate) showed "
    "the weakest associations—a pattern consistent with the expectation that margin type and size "
    "respond more directly to growing-season conditions than gross shape, which may be phylogenetically "
    "constrained. The moderate correlation magnitudes indicate that leaf traits carry detectable but "
    "noisy climate signal, setting the stage for the spatial validation that follows."
)

add_figure("Fig1_trait_climate_corr",
    "Figure 1. Spearman rank correlation between 31 leaf physiognomic traits and seven climate "
    "variables across the modern calibration dataset. Trait categories are indicated by coloured "
    "sidebars: tooth type (red), leaf size class (blue), apex form (green), base form (orange), "
    "L:W ratio (purple), and general shape (teal). Filled circles indicate p < 0.01 after "
    "Bonferroni correction.")

doc.add_page_break()

add_heading("3.2 Ensemble learners versus linear baselines under spatial validation", level=2)
add_para(
    "Under space-block validation, ensemble learners provided no statistically meaningful advantage "
    "over linear baselines for any of the seven climate variables (Fig. 2; Table 1). For MAT, the "
    "best-performing ensemble (Random Forest) achieved R² = 0.383 ± 0.438 (RMSE = 3.82 °C), while "
    "the best linear baseline (OLS) reached R² = 0.343. The difference of 0.04 in R² falls within "
    "one standard deviation of the cross-validation folds (σ = 0.438), indicating that the apparent "
    "ensemble advantage is not distinguishable from noise. For ENTHAL, OLS (R² = 0.306) marginally "
    "exceeded Random Forest (R² = 0.299). For GROWSEAS, the best baseline (OLS, R² = 0.138) "
    "outperformed the best ensemble (RF, R² = 0.099). XGBoost and Gradient Boosting tracked Random "
    "Forest closely across all targets, and SVR produced uniformly lower R² values."
)

add_para(
    "The pattern was consistent: across seven climate variables and four ensemble-versus-baseline "
    "comparisons, no ensemble method provided a statistically robust improvement. The cross-region "
    "trait–climate relationship appeared essentially linear. Non-linear models may have captured "
    "within-region structure—ecological sorting along local gradients in leaf form—that did not "
    "transfer across floristic provinces. From an ML perspective, this finding indicates that the "
    "additional model capacity of ensemble methods was not directed at learnable cross-region signal, "
    "but at region-specific variation that acts as noise for the generalisation task. The practical "
    "implication for future work is that linear or Ridge regression, with interpretable coefficients "
    "and well-characterised uncertainty propagation, may be more trustworthy tools for cross-region "
    "paleoclimate inference than black-box ensemble methods."
)

add_figure("Fig2_model_comparison",
    "Figure 2. Space-block validation performance: ensemble learners versus linear baselines across "
    "six climate variables. Bars show mean R² from space-block GroupKFold (10 folds). WMMT is omitted "
    "due to uniformly negative performance. The vertical dashed line separates temperature (left) from "
    "moisture–energy (right) targets. Ensemble methods (coloured bars) are compared against the best "
    "linear baseline (grey hatched bar) for each variable.")

add_heading("3.3 Reconstructability hierarchy and ensemble limitations", level=2)
add_para(
    "Space-block validation revealed a clear hierarchy of which climate variables are reconstructable "
    "from leaf traits across geographic space. MAT and ENTHAL retained modest but consistent signal "
    "(R² ≈ 0.3–0.4). SH and GROWSEAS hovered near zero (R² = 0.136 and 0.099, respectively, by "
    "Random Forest). CMMT, WMMT, and RH were not predictable across spatial blocks, with R² values "
    "of −0.013, −0.321, and −0.331. Notably, this hierarchy was the same for both ensemble and "
    "linear models: the choice of model class did not alter which variables could be reconstructed. "
    "The ensemble methods did not unlock any variable that was inaccessible to linear baselines, "
    "nor did they substantially improve performance for variables with weak signal. The hierarchy "
    "MAT ≈ ENTHAL > SH > GROWSEAS > CMMT ≫ WMMT, RH admits a physical interpretation—MAT and "
    "ENTHAL integrate annual energy balance, the signal most strongly encoded in margin type and "
    "size distribution—but the key methodological observation is that ensemble complexity did not "
    "expand the set of reconstructable variables."
)

add_heading("3.4 The two-stage cascade: when physical structure does not help", level=2)
add_para(
    "The two-stage temperature→moisture cascade consistently degraded moisture–energy prediction "
    "relative to traits-only models under space-block validation (Fig. 5a; Table 1). For SH, the "
    "traits-only Random Forest achieved R² = 0.235 versus 0.136 for the two-stage design "
    "(ΔR² = −0.099). For ENTHAL, the traits-only R² was 0.391 versus 0.299 (ΔR² = −0.092). "
    "This degradation was consistent across all four ensemble learners—XGBoost, Gradient Boosting, "
    "and SVR showed the same pattern—and held for all three moisture–energy targets."
)

add_para(
    "We attribute this to error propagation across geographic space. Stage 1 temperature predictions "
    "carried systematic spatial biases: sites within a given block tended to be systematically over- "
    "or under-predicted. These biases were amplified when the noisy estimates fed into Stage 2. The "
    "Clausius–Clapeyron relationship linking temperature to saturation vapour pressure is physically "
    "rigorous at the local scale, but the spatial biases in temperature estimates overwhelmed any "
    "information content of the cascade. This result carries a general lesson for ML architectures "
    "in the geosciences: physically motivated multi-stage designs may degrade rather than improve "
    "performance when intermediate predictions carry spatially structured error. In such cases, "
    "direct prediction from the original features may be more reliable."
)

add_heading("3.5 Cross-continent transferability", level=2)
add_para(
    "LOCO validation delineated the geographic boundaries of ML-based reconstruction (Table 2). "
    "For MAT, the Random Forest achieved positive R² for Asia (0.408), the Americas (0.448), "
    "Oceania (0.323), and Africa (0.231), but failed for Europe (R² = −1.035), where only 25 "
    "calibration sites exist. CMMT showed a starker pattern: R² = 0.496 for the Americas but "
    "−1.430 for Europe. Model performance scaled broadly with calibration density in the training "
    "set: continents with more held-in sites supported better prediction of the held-out continent "
    "(Roberts et al., 2017). Europe's consistent failure across all targets indicated that its "
    "leaf-trait–climate relationship differs systematically from that of the other continents, "
    "likely reflecting both small sample size and the distinct floristic and climatic character "
    "of European temperate forests. These results quantify a fundamental limitation of ML in this "
    "domain: models cannot learn relationships for which they lack representative training data."
)

add_heading("3.6 Fossil transfer: apparent success, spatial artifact", level=2)
add_para(
    "Fossil transfer against CLAMP reference values (Fig. 3a–e; Table 1) yielded apparently strong "
    "results for several variables: MAT R² = 0.646 (RMSE = 2.74 °C), CMMT R² = 0.820 (RMSE = 2.79 "
    "°C), GROWSEAS R² = 0.730 (RMSE = 1.01 months), and ENTHAL R² = 0.681 (RMSE = 9.68 kJ/kg). "
    "WMMT and RH failed (R² = −1.056 and −0.080, respectively). A systematic cold bias was present "
    "across all predictions (MAT bias = −1.69 °C; ENTHAL bias = −4.90 kJ/kg)."
)

add_para(
    "The strong fossil CMMT performance (R² = 0.820) stands in marked contrast to its negative "
    "space-block validation R² (−0.013). This discrepancy is explained by the fossil dataset "
    "composition: 65 of 71 assemblages are from Asia, where modern calibration coverage is densest "
    "(158 sites). Fossil transfer for CMMT therefore represents within-domain interpolation—both "
    "training and test data share the same geographic domain. The contrast between fossil CMMT "
    "R² (0.82) and space-block CMMT R² (−0.01) illustrates a central pitfall in ML for "
    "paleoclimate: validation on geographically clustered fossil data can produce encouraging "
    "metrics that do not reflect cross-region predictive capacity. For paleoelevation studies on "
    "the Tibetan Plateau, where leaf fossils from high-elevation basins must be interpreted using "
    "calibrations from lower-elevation Asian sites (He et al., 2022; Ding et al., 2022), the "
    "within-domain performance of MAT and ENTHAL supports their use, while the CMMT results caution "
    "that fossil transfer metrics alone are insufficient evidence of generalisability."
)

add_figure("Fig3_obs_vs_pred",
    "Figure 3. Fossil transfer and cross-continent validation. (a–e) Predicted versus CLAMP reference "
    "values for five climate variables across 71 fossil assemblages; the dashed line indicates "
    "identity. Marker colours distinguish temperature (blue) and moisture–energy (red) targets. "
    "(f) Leave-One-Continent-Out R² heatmap for five climate variables across five continents.")

doc.add_page_break()

add_heading("3.7 Feature importance: what ensemble models learn", level=2)
add_para(
    "Random Forest feature importance analysis (Fig. 4) revealed which trait categories drive "
    "cross-region climate signal. Tooth-type traits dominated temperature prediction (~40% of MAT "
    "importance), followed by leaf size categories (~35%) and apex form (~12%). Base form and shape "
    "traits contributed minimally. The leading individual feature for MAT was the proportion of "
    "entire-margined leaves (no teeth; ~15% of RF importance), confirming the century-old leaf-margin "
    "analysis as the single most informative trait even under spatial validation. For moisture–energy "
    "variables, leaf size traits dominated, consistent with the physical expectation that leaf size "
    "responds to water availability (Peppe et al., 2011; Wright et al., 2017). The importance "
    "hierarchy—tooth type > leaf size ≫ apex, base, shape—was stable across all targets, suggesting "
    "that effort invested in scoring additional trait categories yields diminishing returns for "
    "cross-region climate reconstruction, regardless of the ML method used."
)

add_figure("Fig4_feature_importance",
    "Figure 4. Random Forest feature importance. (a) Feature importance heatmap across all seven "
    "climate variables. (b) Top 10 features by importance for MAT. (c) Trait-category contribution "
    "to MAT importance.")

add_heading("3.8 Synthesis", level=2)
add_para(
    "Synthesising across all three validation frameworks, we delineate three tiers of reconstructability "
    "(Fig. 5b; Table 1). Tier 1—cross-region robust—comprises MAT and ENTHAL, with positive "
    "space-block R² and moderate fossil transfer. Tier 2—regionally conditioned—comprises SH, "
    "GROWSEAS, and CMMT, with near-zero space-block R² but acceptable fossil transfer within densely "
    "calibrated domains. Tier 3—cross-region unreliable—comprises WMMT and RH, with consistently "
    "negative R². Neither ensemble methods nor the two-stage architecture elevated any variable from "
    "a lower tier to a higher one. The hierarchy reflects fundamental properties of the trait–climate "
    "relationship, not shortcomings of particular ML algorithms."
)

add_figure("Fig5_two_stage_ablation",
    "Figure 5. Two-stage architecture assessment and reconstructability summary. (a) Space-block R² "
    "of traits-only versus two-stage models for moisture–energy variables; points below the identity "
    "line indicate two-stage degradation. (b) Bar chart comparing space-block R² against fossil "
    "transfer R² for five climate variables, illustrating the gap between spatial validation and "
    "fossil transfer dominated by Asian assemblages.")

doc.add_page_break()


# ═══════════════════════════════════════════════════
# 4. DISCUSSION
# ═══════════════════════════════════════════════════
add_heading("4 Discussion", level=1)

add_heading("4.1 Why ensemble methods did not improve cross-region prediction", level=2)
add_para(
    "The finding that ensemble ML methods did not outperform linear baselines under spatial "
    "validation is not a failure of ML. It reflects a property of the data: the component of the "
    "trait–climate relationship that generalises across floristic provinces is approximately linear. "
    "Leaf margin type scales with growing-season temperature through a well-understood physiological "
    "mechanism—the cost–benefit trade-off between tissue construction and photosynthetic return—and "
    "this relationship is broadly conserved across woody dicot lineages. The non-linear structure "
    "that ensemble methods can capture—ecological sorting along local moisture gradients, phylogenetic "
    "constraints on shape within regional species pools, site-specific taphonomic biases—does not "
    "transfer across geographic space. When a Random Forest partitions the feature space along a "
    "complex decision boundary that captures, for example, the particular leaf-size distribution of "
    "East Asian broadleaf forests, that boundary provides no advantage for predicting climate at "
    "European or African sites with different floristic compositions."
)

add_para(
    "This interpretation is consistent with a growing body of evidence from spatial modelling in "
    "ecology and remote sensing. Meyer et al. (2019) showed that Random Forest performance for "
    "spatial prediction of land-cover fractions dropped substantially when predictor variables were "
    "selected by spatial rather than random cross-validation. Ploton et al. (2020) demonstrated that "
    "spatial cross-validation revealed poor predictive performance for aboveground biomass mapping "
    "at continental scales, and that apparent skill under random cross-validation largely reflected "
    "spatial autocorrelation. Our results extend this spatial-validation logic to paleoclimate "
    "reconstruction and show that the same principle applies: when calibration and target sites are "
    "geographically separated, the additional complexity of ensemble methods does not translate into "
    "greater generalisability."
)

add_heading("4.2 The cascade failure as a cautionary tale for multi-stage ML", level=2)
add_para(
    "The failure of the two-stage temperature→moisture cascade carries broader implications for ML "
    "architecture design in the geosciences. Multi-stage or cascaded architectures, in which the "
    "outputs of one model serve as inputs to the next, are attractive because they can encode "
    "physical knowledge—conservation laws, thermodynamic relationships, known dependencies—into the "
    "model structure. The temperature-to-moisture cascade tested here is physically well-founded: "
    "saturation vapour pressure depends exponentially on temperature, and both specific humidity and "
    "moist enthalpy are functions of temperature and moisture content. However, when the intermediate "
    "predictions carry spatially structured error, the cascade amplifies rather than constrains "
    "uncertainty. Each geographic block in our space-block framework contained sites that were "
    "systematically over- or under-predicted for temperature; these systematic errors propagated "
    "into the moisture stage as coherent, block-level biases that the model could not correct."
)

add_para(
    "This finding suggests a design principle for ML architectures in spatial prediction problems: "
    "multi-stage or cascaded designs should be tested under spatial partitioning of the intermediate "
    "predictions, not only under random cross-validation. If the intermediate predictions carry "
    "spatial bias, propagating them through downstream stages may degrade rather than improve "
    "performance. In the leaf-physiognomy context, direct prediction of moisture–energy variables "
    "from traits proved more reliable than the physically motivated cascade, because leaf traits "
    "encode moisture information independently—through size responses to water availability—rather "
    "than only through the temperature-mediated pathway. For practical application, we recommend "
    "that moisture–energy variables be predicted directly from traits when fossil sites lie in "
    "geographic domains poorly represented in calibration data."
)

add_heading("4.3 Spatial validation as an essential ML practice in paleoclimate", level=2)
add_para(
    "Our results reinforce a methodological recommendation that is widely accepted in spatial "
    "ecology but not yet standard in paleoclimate ML: models intended for geographic extrapolation "
    "should be validated under geographic partitioning. Random k-fold cross-validation, which "
    "underlies the performance metrics reported in many ML-based paleoclimate studies, tests "
    "interpolation, not extrapolation. When calibration sites are geographically clustered—as they "
    "are for leaf physiognomy, and as they likely are for many other paleoclimate proxies—the gap "
    "between random-fold and spatial-fold performance can be substantial. For MAT, we observed a "
    "drop from within-domain fossil transfer (R² ≈ 0.65) to cross-block validation (R² ≈ 0.38), "
    "a generalisability penalty of approximately 0.27 in R². For CMMT, the penalty was far larger "
    "(0.82 → −0.01), and fossil transfer success for this variable was almost entirely attributable "
    "to the Asian dominance of the fossil dataset."
)

add_para(
    "We suggest three practices for ML-based paleoclimate reconstruction going forward. First, "
    "spatial-block validation should be reported alongside conventional cross-validation, so that "
    "readers can assess the generalisability penalty directly. Second, linear baselines should be "
    "included in all model comparisons; an ensemble method that does not outperform OLS or Ridge "
    "regression under spatial validation provides no evidence that non-linear modelling is warranted. "
    "Third, fossil transfer metrics should be interpreted through the lens of the fossil dataset's "
    "geographic composition: if most fossil sites share the same region as the bulk of the calibration "
    "data, fossil transfer R² reflects regional interpolation, not the cross-region generalisation "
    "that paleoclimate reconstruction ultimately requires."
)

add_heading("4.4 Implications for Tibetan Plateau paleoelevation studies", level=2)
add_para(
    "The Tibetan Plateau has been a focal point for leaf-physiognomy paleoclimate reconstruction "
    "because its Cenozoic uplift history is coupled to the evolution of the Asian monsoon and "
    "regional biodiversity (Spicer et al., 2021; Ding et al., 2022; He et al., 2022). Our results "
    "support the use of ML-derived MAT and ENTHAL estimates for Tibetan paleoelevation studies, as "
    "these variables maintain positive R² under spatial validation and benefit from the dense East "
    "Asian calibration network. However, the spatial collapse of CMMT—from fossil R² = 0.82 to "
    "space-block R² = −0.01—indicates that cold-month temperature reconstructions for Tibetan "
    "fossil sites are reliable only within the East Asian floristic domain. The LOCO results further "
    "suggest that exporting East Asian calibrations to other orogenic belts, such as the Andes or "
    "the Alps, is unlikely to yield reliable estimates without locally dense calibration networks. "
    "Recent independent proxy evidence for Paleogene Tibetan elevation from oxygen isotopes and "
    "clumped-isotope thermometry (Miao et al., 2022; Liang et al., 2025) offers a path toward "
    "cross-validating leaf-physiognomy reconstructions and constraining their spatial uncertainty."
)

add_heading("4.5 Limitations", level=2)
add_para(
    "Several limitations constrain the generality of our conclusions. First, the modern calibration "
    "dataset is geographically imbalanced; the catastrophic LOCO failure for Europe likely reflects "
    "insufficient sampling (25 sites) rather than any intrinsic unpredictability of European leaf "
    "traits. Expanding modern sampling in Europe and Africa would allow more definitive tests of "
    "cross-continent transferability. Second, our fossil validation targets are CLAMP-computed values, "
    "not independent instrumental observations. Systematic biases in CLAMP estimates propagate into "
    "our fossil transfer metrics, and validation against non-physiognomic proxies at key sites would "
    "strengthen the assessment (Liang et al., 2025). Third, our 31-trait protocol captures only a "
    "subset of morphological variation; additional traits such as venation density or leaf mass per "
    "area (Lowe et al., 2024) could improve spatial generalisability, although these traits are not "
    "currently available at the global scale of our dataset. Fourth, the 5 × 4 grid partitioning "
    "represents one spatial grain; sensitivity to block resolution should be explored. Fifth, our "
    "hyperparameter choices favour regularisation to promote spatial generalisation; more aggressive "
    "tuning could yield different results, but tuning itself is a potential source of overfitting "
    "when not spatially cross-validated. Finally, an irreducible uncertainty remains in whether "
    "trait–climate relationships derived from modern vegetation apply to fossil floras separated by "
    "tens of millions of years of evolution and climate change (Spicer et al., 2021; Chen et al., "
    "2025)."
)


# ═══════════════════════════════════════════════════
# 5. CONCLUSIONS
# ═══════════════════════════════════════════════════
add_heading("5 Conclusions", level=1)

add_para(
    "We have presented a systematic evaluation of ensemble machine learning methods for "
    "leaf-physiognomy paleoclimate reconstruction under honest spatial validation. Our central "
    "finding is that ensemble learners provide no statistically meaningful advantage over linear "
    "statistical baselines when models are asked to generalise across geographic space. The "
    "cross-region component of the trait–climate signal is essentially linear: the century-old "
    "leaf-margin relationship between entire-margined leaf proportion and mean annual temperature "
    "remains the most informative single feature under spatial validation, and the additional "
    "complexity of Random Forest, XGBoost, or gradient-boosted trees does not extract "
    "generalisable signal that linear models miss."
)

add_para(
    "Three specific findings support this conclusion. First, across seven climate variables and "
    "four ensemble-versus-baseline comparisons, no ensemble method achieved a statistically robust "
    "improvement over the best linear baseline under space-block GroupKFold. Second, a physically "
    "motivated two-stage architecture—predicting temperature first, then feeding those estimates "
    "into moisture–energy prediction—consistently degraded performance relative to traits-only "
    "prediction, because spatially structured errors in the temperature stage propagated through "
    "the cascade. Third, apparently strong fossil transfer performance for cold-month mean "
    "temperature (R² = 0.82) collapsed to R² = −0.01 under space-block validation; the fossil "
    "success reflected the Asian dominance of the fossil dataset and constituted within-domain "
    "interpolation, not evidence of cross-region predictive capacity."
)

add_para(
    "We recommend that future ML applications in leaf-physiognomy paleoclimate reconstruction—and "
    "in paleoclimate proxy calibration more broadly—adopt three practices: (i) report space-block "
    "or equivalent spatially structured validation metrics alongside conventional cross-validation; "
    "(ii) include linear baselines to establish whether non-linear methods provide measurable "
    "benefit; and (iii) interpret fossil transfer results in light of the geographic composition "
    "of the fossil dataset. Ensemble machine learning is a powerful tool for many scientific "
    "problems, but its benefits are not automatic. In domains where the underlying signal is "
    "approximately linear and the generalisation task is spatial extrapolation, simpler models "
    "with fewer degrees of freedom may be the more scientifically honest choice."
)


# ═══════════════════════════════════════════════════
# DATA AND CODE AVAILABILITY
# ═══════════════════════════════════════════════════
add_heading("Data availability", level=1)

add_para(
    "The modern calibration dataset and fossil assemblage data are available in the accompanying "
    "Excel workbook. All training code, the space-block validation pipeline, figure generation "
    "scripts, trained model files, and the manuscript source are archived on Zenodo [DOI to be "
    "created upon acceptance] and publicly available on GitHub at [repository URL]. The repository "
    "includes: (1) training_pipeline_v2.py, which reproduces all space-block validation results, "
    "baseline comparisons, LOCO validation, and fossil transfer evaluation; (2) "
    "generate_figures_v2.py, which produces all publication figures; (3) the models_v2/ directory "
    "containing trained model files; and (4) the output/ directory containing all tabulated results. "
    "Analyses were performed in Python 3.10 using scikit-learn 1.3, XGBoost 2.0, and associated "
    "scientific Python libraries. Climate data were obtained from WorldClim 2 (Fick and Hijmans, "
    "2017; https://www.worldclim.org/)."
)

add_heading("Author contributions", level=1)
add_para("[To be completed by authors.]")

add_heading("Competing interests", level=1)
add_para("The authors declare that they have no competing interests.")

add_heading("Acknowledgements", level=1)
add_para("[To be completed by authors.]")


# ═══════════════════════════════════════════════════
# REFERENCES (alphabetical)
# ═══════════════════════════════════════════════════
add_heading("References", level=1)

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
# TABLES
# ═══════════════════════════════════════════════════
doc.add_page_break()
add_heading("Tables", level=1)

add_heading("Table 1. Summary of model performance under space-block validation, baseline comparison, and fossil transfer.", level=2)
add_para("Space-block validation metrics are from block-based GroupKFold (10 folds). Best Baseline is the top-performing linear model for each variable. Two-Stage ΔR² is the change from traits-only to two-stage architecture (moisture–energy variables only). Fossil metrics are R², RMSE, and mean bias versus CLAMP reference values (N = 71 assemblages).", italic=True)

table1 = doc.add_table(rows=8, cols=9)
table1.style = 'Light Grid Accent 1'
headers1 = ['Variable', 'Category', 'Space-block\nR² (RF)', 'Space-block\nRMSE',
            'Best\nBaseline', 'Baseline\nR²', 'Two-Stage\nΔR²', 'Fossil\nR²', 'Fossil\nRMSE']
data1 = [
    ['MAT', 'Temperature', '0.383', '3.82', 'OLS', '0.343', '—', '0.646', '2.74'],
    ['WMMT', 'Temperature', '−0.321', '3.71', 'ElasticNet', '−0.284', '—', '−1.056', '2.91'],
    ['CMMT', 'Temperature', '−0.013', '6.02', 'PLS', '−0.238', '—', '0.820', '2.79'],
    ['GROWSEAS', 'Temperature', '0.099', '1.78', 'OLS', '0.138', '—', '0.730', '1.01'],
    ['RH', 'Moist.–Energy', '−0.331', '9.55', 'ElasticNet', '−0.720', '−0.030', '−0.080', '18.94'],
    ['SH', 'Moist.–Energy', '0.136', '1.99', 'ElasticNet', '0.060', '−0.099', '0.385', '2.95'],
    ['ENTHAL', 'Moist.–Energy', '0.299', '11.11', 'OLS', '0.306', '−0.092', '0.681', '9.68'],
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
add_heading("Table 2. Leave-One-Continent-Out (LOCO) validation results (Random Forest).", level=2)
add_para("R² values for each variable–continent combination. N is the number of held-out sites per continent.", italic=True)

table2 = doc.add_table(rows=36, cols=4)
table2.style = 'Light Grid Accent 1'
headers2 = ['Variable', 'Continent', 'N sites', 'R²']
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


# ═══════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════
output_path = os.path.join(BASE_DIR, "Manuscript_ML_Limitations_v7.docx")
doc.save(output_path)
print(f"Manuscript (v7, ML-limitations focus) saved to: {output_path}")
print(f"  Title: 'Limited benefits of ensemble machine learning for leaf-physiognomy paleoclimate reconstruction'")
print(f"  Core argument: ML does not improve over linear baselines under spatial validation")
print(f"  References: 25 citations, alphabetical order")
print(f"  Embedded figures: Fig1–5")
