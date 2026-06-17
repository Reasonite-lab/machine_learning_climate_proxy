# Spatial Cross-Validation for Leaf-Physiognomy Paleoclimate Machine Learning

Code and data repository for: **"Spatial cross-validation reveals fundamental limits and fossil transfer potential of leaf-physiognomy machine learning for paleoclimate reconstruction"**

Submitted to *Climate of the Past* (CP).

## Overview

This repository implements a leakage-free spatial cross-validation framework for evaluating machine learning models that predict climate variables from leaf physiognomic traits. Unlike previous studies that used random k-fold cross-validation—which ignores spatial autocorrelation and inflates performance estimates—we use block-based spatial GroupKFold, Leave-One-Continent-Out (LOCO) validation, and fossil transfer against CLAMP reference values.

**Key findings:**
- Spatial CV dramatically reduces apparent model performance relative to random-fold estimates (MAT R² = 0.38 vs previously reported >0.8)
- Ensemble ML provides only marginal improvements over linear statistical baselines
- The two-stage architecture (temperature → moisture cascade) fails to improve spatial generalisation
- Fossil transfer works for Asian-dominated target sites but reflects within-region interpolation

## Repository Structure

```
Codebubby/
├── training_pipeline_v2.py      # Main pipeline: spatial CV, baselines, LOCO, fossil transfer
├── generate_figures_v2.py       # Publication figure generation (Fig 1-5)
├── build_manuscript.py          # Manuscript DOCX builder
├── Manuscript_Paleoclimate_ML_CP_v4.docx  # Complete manuscript
├── README.md                    # This file
├── models_v2/                   # Trained model files (.joblib)
│   ├── stage1_MAT.joblib
│   ├── stage1_WMMT.joblib
│   ├── stage1_CMMT.joblib
│   ├── stage1_GROWSEAS.joblib
│   ├── stage2_RH.joblib
│   ├── stage2_SH.joblib
│   └── stage2_ENTHAL.joblib
├── output/                      # Tabulated results
│   ├── Table1_Performance_Summary.csv
│   ├── Table2_LOCO_Validation.csv
│   ├── Table3_Fossil_Predictions.csv
│   ├── Table4_TwoStage_Ablation.csv
│   └── Table5_Baseline_Comparison.csv
└── Fig1-5_*.{svg,pdf,png,tiff}  # Publication figures
```

## Requirements

- Python 3.10+
- numpy, pandas, scipy
- scikit-learn >= 1.3
- xgboost >= 2.0
- matplotlib >= 3.7
- joblib
- openpyxl
- python-docx

Install:
```bash
pip install numpy pandas scipy scikit-learn xgboost matplotlib joblib openpyxl python-docx
```

## Reproducing Results

### 1. Run the training pipeline
```bash
python training_pipeline_v2.py
```
This produces all tables (Tables 1-5) in `output/` and trained models in `models_v2/`.

### 2. Generate figures
```bash
python generate_figures_v2.py
```
This produces Figures 1-5 in SVG, PDF, PNG, and TIFF formats.

### 3. Build the manuscript (optional)
```bash
python build_manuscript.py
```

## Data

The calibration dataset (`Global378+Tibet15+Fossil73_更正.xlsx`) contains:
- **393 modern woody dicot sites** across 5 continents with 31 leaf physiognomic trait proportions and 7 climate variables
- **71 fossil assemblages** (predominantly Asian) with CLAMP-computed reference climate values

Climate data extracted from WorldClim 2 (Fick & Hijmans, 2017).

## Key Technical Details

### Spatial Cross-Validation
- Block-based partitioning: 5 latitudinal × 4 longitudinal bands → spatial blocks
- GroupKFold with spatial block as grouping variable
- 10-fold CV (constrained by number of valid blocks)

### Two-Stage Architecture (Leakage-Free)
- **Stage 1**: 31 traits → MAT, WMMT, CMMT, GROWSEAS (Random Forest)
- **Stage 2**: 31 traits + out-of-fold Stage 1 predictions → RH, SH, ENTHAL
- OOF predictions prevent target-site temperature leakage into Stage 2

### Models Evaluated
- **Ensemble ML**: Random Forest (n=500, depth=12), XGBoost (n=300, depth=5), Gradient Boosting (n=300, depth=4), SVR (RBF)
- **Statistical Baselines**: Linear Regression, Ridge (CV alpha), ElasticNet (CV), PLS (n=4)

### Validation Protocols
1. Block-based spatial GroupKFold
2. Leave-One-Continent-Out (LOCO)
3. Fossil transfer vs CLAMP reference (N=71)

## Citation

If you use this code or data, please cite:

```
[Author list]. Spatial cross-validation reveals fundamental limits and fossil transfer 
potential of leaf-physiognomy machine learning for paleoclimate reconstruction. 
Climate of the Past, [year].
```

## License

[To be determined]

## Contact

[corresponding author email]
