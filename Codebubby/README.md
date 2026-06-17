# Limited Benefits of Ensemble Machine Learning for Leaf-Physiognomy Paleoclimate Reconstruction

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Can machine learning outperform linear regression for reconstructing ancient climates from fossil leaves? Under honest spatial validation — not by much.**

This repository contains the full analysis pipeline, figures, trained models, and manuscript for a study evaluating whether ensemble machine learning methods (Random Forest, XGBoost, Gradient Boosting, SVR) provide meaningful improvements over linear baselines for leaf-physiognomy paleoclimate reconstruction.

---

## 🎯 Key Findings

| Question | Answer |
|----------|--------|
| Do ensemble ML methods beat linear models? | **No** — under space-block cross-validation, the best ensemble (Random Forest, R² = 0.38) outperforms the best linear model (OLS, R² = 0.34) by only **0.04** for MAT |
| Why do previous studies report R² > 0.8? | Random k-fold CV leaks spatial information — geographically adjacent sites end up in both train and test sets, turning **spatial extrapolation into spatial interpolation** |
| Does a two-stage cascade (predict temperature → feed into humidity prediction) help? | **No** — it consistently **degrades** prediction, because spatial biases from stage-1 propagate into stage-2 |
| Can the model predict outside its training region? | LOCO (Leave-One-Continent-Out) reveals Europe R² = **−1.035** — worse than guessing the mean |
| Is ML completely useless for this task? | **No** — if used with (i) spatial block validation, (ii) linear baselines, and (iii) awareness of fossil geographic composition, ML remains a viable tool for within-domain applications |

---

## 📂 Repository Structure

```
.
├── training_pipeline_v2.py          # Core pipeline: spatial CV, LOCO, fossil transfer
├── generate_figures_v2.py           # Generates Figures 1–5 for the manuscript
├── fig1_heatmap.py                  # Trait–climate Spearman correlation heatmap
├── build_manuscript_v7.py           # Builds the final manuscript (DOCX)
├── build_manuscript_v7_cn.py        # Chinese translation of the manuscript
├── build_pptx.py                    # Nature-style Chinese presentation (PPTX)
├── models_v2/                       # 7 trained Stage-1 & Stage-2 models (joblib)
│   ├── stage1_MAT.joblib
│   ├── stage1_WMMT.joblib
│   ├── stage1_CMMT.joblib
│   ├── stage1_GROWSEAS.joblib
│   ├── stage2_RH.joblib
│   ├── stage2_SH.joblib
│   └── stage2_ENTHAL.joblib
├── output/                          # Result tables & presentation
│   ├── performance_summary_v2.csv   # Spatial CV R², RMSE, fossil transfer R²
│   ├── loco_validation_v2.csv      # Leave-One-Continent-Out results
│   ├── fossil_predictions_v2.csv   # 71 fossil assemblage predictions
│   ├── baseline_comparison_v2.csv  # Linear baseline comparison
│   ├── two_stage_ablation_v2.csv   # Two-stage cascade ablation
│   ├── final_presentation_cn.pptx  # Chinese presentation slides
│   └── ...
├── Fig1_trait_climate_corr.*       # Figure 1: Trait–Climate correlation heatmap
├── Fig2_obs_vs_pred.*              # Figure 2: Observed vs Predicted (spatial CV)
├── Fig3_feature_importance.*       # Figure 3: Feature importance ranking
├── Fig4_model_comparison.*         # Figure 4: Model comparison (R² / RMSE)
├── Fig5_two_stage_ablation.*       # Figure 5: Two-stage cascade ablation (ΔR²)
└── Data                            # Calibration dataset
    └── Global378+Tibet15+Fossil73_更正_副本.xlsx  # 393 modern + 71 fossil sites
```

---

## 🧪 Methods Overview

### Dataset

- **393 modern woody dicot sites** across 5 continents (Asia: 158, Americas: 143, Europe: 25, Africa: 14, Oceania: 53)
- **71 fossil assemblages** (92% from Asia)
- **31 leaf physiognomic traits** (lobation, teeth types, leaf size classes, apex/base shapes, L:W ratios, shape categories)
- **7 climate variables**: MAT, WMMT, CMMT, GROWSEAS, RH, SH, ENTHAL

### Validation Strategies

| Strategy | Description | Honest? |
|----------|-------------|---------|
| **Random k-fold CV** | Randomly split sites into k folds | ❌ Spatial leakage |
| **Space-block CV** | Split by 5×4 lat/lon grid; entire blocks in train OR test | ✅ Honest |
| **LOCO** | Leave-One-Continent-Out; entire continent as test set | ✅ Extreme test |

### Models

- **Ensembles**: Random Forest, XGBoost, Gradient Boosting, SVR
- **Linear baselines**: OLS, Ridge, ElasticNet, PLS
- **Two-stage cascade**: Stage-1 predicts 4 temperature variables → OOF predictions fed into Stage-2 for 3 moisture/energy variables

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn joblib openpyxl python-docx
```

### Run the Full Pipeline

```bash
# Step 1: Train models and generate result tables
python training_pipeline_v2.py

# Step 2: Generate figures
python generate_figures_v2.py

# Step 3: Build the manuscript (optional)
python build_manuscript_v7.py
```

All outputs will be saved to `output/` and `models_v2/`.

### Load Trained Models

```python
import joblib

model = joblib.load('models_v2/stage1_MAT.joblib')
predictions = model.predict(X_fossil)
```

---

## 📊 Results Summary

### Spatial Cross-Validation (Space-Block GroupKFold)

| Variable | Best Ensemble R² | Best Linear R² | ΔR² |
|----------|-----------------|----------------|-----|
| MAT | 0.383 (RF) | 0.341 (Ridge) | +0.042 |
| WMMT | 0.216 (RF) | 0.177 (Ridge) | +0.039 |
| CMMT | −0.013 (RF) | −0.002 (Ridge) | −0.011 |
| GROWSEAS | 0.308 (RF) | 0.302 (Ridge) | +0.006 |
| SH | 0.235 (GBDT) | 0.287 (Ridge) | −0.052 |
| ENTHAL | 0.301 (RF) | 0.300 (Ridge) | +0.001 |
| RH | −0.301 (RF) | −0.253 (OLS) | −0.048 |

### LOCO Validation (Worst Case: Europe)

| Variable | Europe R² |
|----------|-----------|
| MAT | −3.424 |
| CMMT | −2.648 |
| SH | −3.482 |
| ENTHAL | −3.439 |

### Two-Stage Cascade Ablation

Adding OOF temperature predictions to moisture models consistently **degrades** R² by 0.03–0.10 across all three moisture variables.

---

## 📝 Manuscript

The final manuscript (`build_manuscript_v7.py` → `Manuscript_ML_Limitations_v7.docx`) is formatted for submission to **Climate of the Past (CP)**.

- **Title**: *Limited benefits of ensemble machine learning for leaf-physiognomy paleoclimate reconstruction*
- **25 references** in Copernicus style
- **5 embedded figures**
- Chinese translation also available (`build_manuscript_v7_cn.py`)

---

## 🔗 Citation

If you use this code or data, please cite:

> X. et al. (2025). Limited benefits of ensemble machine learning for leaf-physiognomy paleoclimate reconstruction. *In preparation for Climate of the Past.*

And the key methodological references:

- Roberts et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography*.
- Ploton et al. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. *Nature Communications*.
- Wolfe (1993). A method of obtaining climatic parameters from leaf assemblages. *USGS Bulletin*.

---

## ⚠️ Note on Token Security

If you previously used a GitHub Personal Access Token in this repository, **revoke it immediately** at [github.com/settings/tokens](https://github.com/settings/tokens) and generate a new one.
