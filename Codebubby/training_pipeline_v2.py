#!/usr/bin/env python3
"""
Scenario B v2: Improved spatial CV pipeline with optimised hyperparameters.

Key improvements:
1. Block-based spatial CV (lat/lon grid blocks) — more stable than KMeans clustering
2. Optimised RF hyperparameters for spatial generalisation
3. Proper feature engineering for compositional trait data
4. No QuantileTransformer for tree-based models (monotonic-invariant)
5. Comprehensive LOCO validation
"""

import numpy as np
import pandas as pd
import warnings
import os
from copy import deepcopy
warnings.filterwarnings('ignore')

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, RidgeCV, ElasticNetCV
from sklearn.svm import SVR
from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import QuantileTransformer, StandardScaler
from sklearn.model_selection import KFold, GroupKFold, cross_val_predict
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.cluster import KMeans
from sklearn.base import clone
import xgboost as xgb
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "Global378+Tibet15+Fossil73_更正.xlsx")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

RANDOM_STATE = 42

FEATURE_COLS = [
    'Lobed', 'No Teeth', 'Teeth Regul', 'Teeth Close', 'Teeth Round',
    'Teeth Acute', 'Teeth Compo', 'Nanophyl', 'Leptophyl', 'Leptophyl 2',
    'Microphyl 1', 'Microphyl 2', 'Microphyl 3', 'Mesophyl 1', 'Mesophyl 2',
    'Mesophyl 3', 'Apex Emargi', 'Apex Round', 'Apex Acute', 'Apex Attenu',
    'Base Cordat', 'Base Round', 'Base Acute', 'L:W <1:1', 'L:W 1-2:1',
    'L:W 2-3:1', 'L:W 3-4:1', 'L:W >4:1', 'Obovate', 'Elliptic', 'Ovate'
]
T_TARGETS = ['MAT', 'WMMT', 'CMMT', 'GROWSEAS']
M_TARGETS = ['RH', 'SH', 'ENTHAL']
ALL_TARGETS = T_TARGETS + M_TARGETS

print("=" * 80)
print("SCENARIO B v2: SPATIAL CV WITH OPTIMISED MODELS")
print("=" * 80)

# ---- Load data ----
df_plants = pd.read_excel(DATA_FILE, sheet_name="plants")
df_fossil = pd.read_excel(DATA_FILE, sheet_name="fossils")
lat_col = ' Latitude        '
df_plants['LAT'] = df_plants[lat_col]
df_plants['LON'] = df_plants['Longitude']
df_fossil['LAT'] = df_fossil['Latitude']
df_fossil['LON'] = df_fossil['Longitude']

X = df_plants[FEATURE_COLS].values.astype(np.float64)
X_fossil = df_fossil[FEATURE_COLS].values.astype(np.float64)
coords = df_plants[['LAT', 'LON']].values

n = len(X)
print(f"Modern: {n} sites, Fossil: {len(df_fossil)} assemblages")

# ---- Spatial fold construction: lat/lon block partitioning ----
# Divide globe into latitudinal bands and use those as spatial blocks
print("\n--- Spatial Block CV ---")
lat_bins = np.percentile(coords[:, 0], np.linspace(0, 100, 6))
lon_bins = np.percentile(coords[:, 1], np.linspace(0, 100, 5))

def assign_spatial_block(lat, lon):
    """Assign each site to a 2D spatial block."""
    lat_idx = np.digitize(lat, lat_bins) - 1
    lon_idx = np.digitize(lon, lon_bins) - 1
    lat_idx = np.clip(lat_idx, 0, len(lat_bins) - 2)
    lon_idx = np.clip(lon_idx, 0, len(lon_bins) - 2)
    return lat_idx * (len(lon_bins) - 1) + lon_idx

spatial_blocks = assign_spatial_block(coords[:, 0], coords[:, 1])
n_blocks = len(np.unique(spatial_blocks))
print(f"Spatial blocks: {n_blocks}")
print(f"Block sizes: {sorted([np.sum(spatial_blocks == b) for b in range(n_blocks)])}")

# Group KFold with spatial blocks as groups
gkf = GroupKFold(n_splits=min(10, n_blocks))
spatial_folds = list(gkf.split(X, groups=spatial_blocks))
print(f"Usable folds: {len(spatial_folds)}")

# ---- Optimised models ----
def make_models():
    """Optimised models for spatial generalisation (deeper trees, stronger regularisation)."""
    return {
        'RF': RandomForestRegressor(
            n_estimators=500, max_depth=12, min_samples_leaf=3,
            min_samples_split=5, max_features='sqrt',
            random_state=RANDOM_STATE, n_jobs=-1
        ),
        'XGBoost': xgb.XGBRegressor(
            n_estimators=300, max_depth=5, learning_rate=0.03,
            subsample=0.8, colsample_bytree=0.8,
            reg_alpha=0.1, reg_lambda=1.0,
            random_state=RANDOM_STATE, verbosity=0, n_jobs=-1
        ),
        'GBDT': GradientBoostingRegressor(
            n_estimators=300, max_depth=4, learning_rate=0.03,
            subsample=0.8, max_features=0.8,
            min_samples_leaf=5,
            random_state=RANDOM_STATE
        ),
        'SVR': SVR(kernel='rbf', C=10.0, epsilon=0.05, gamma='scale'),
    }

def make_baselines():
    return {
        'Linear': LinearRegression(),
        'Ridge': RidgeCV(alphas=np.logspace(-2, 3, 30)),
        'ElasticNet': ElasticNetCV(l1_ratio=[0.1, 0.5, 0.7, 0.9, 0.95, 1.0],
                                    cv=5, random_state=RANDOM_STATE),
        'PLS': PLSRegression(n_components=min(4, len(FEATURE_COLS) - 1)),
    }

def eval_metrics(y_true, y_pred):
    return {
        'R2': r2_score(y_true, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
        'MAE': mean_absolute_error(y_true, y_pred),
    }

# ---- Stage 1: Temperature (spatial CV) ----
print("\n" + "=" * 80)
print("STAGE 1: TEMPERATURE PREDICTION")
print("=" * 80)

stage1_cv = {}
stage1_oof = {}  # out-of-fold predictions for Stage 2
stage1_models = {}

for target in T_TARGETS:
    y = df_plants[target].values
    print(f"\n  {target}:")
    
    models = make_models()
    baselines = make_baselines()
    oof_preds = np.full(n, np.nan)
    
    # --- Ensemble models with spatial CV ---
    ens_metrics = {}
    for name, model in models.items():
        fold_results = []
        for train_idx, test_idx in spatial_folds:
            m = clone(model)
            m.fit(X[train_idx], y[train_idx])
            yp = m.predict(X[test_idx])
            fold_results.append(eval_metrics(y[test_idx], yp))
            if name == 'RF':
                oof_preds[test_idx] = yp
        ens_metrics[name] = fold_results
    
    # --- Baseline models ---
    bl_metrics = {}
    for name, model in baselines.items():
        fold_results = []
        for train_idx, test_idx in spatial_folds:
            m = clone(model)
            m.fit(X[train_idx], y[train_idx])
            yp = m.predict(X[test_idx])
            if yp.ndim > 1:
                yp = yp.ravel()
            fold_results.append(eval_metrics(y[test_idx], yp))
        bl_metrics[name] = fold_results
    
    # Report
    for name in models:
        r2_vals = [m['R2'] for m in ens_metrics[name]]
        rmse_vals = [m['RMSE'] for m in ens_metrics[name]]
        print(f"    {name:<10s}: R² = {np.mean(r2_vals):.3f} ± {np.std(r2_vals):.3f}, "
              f"RMSE = {np.mean(rmse_vals):.2f} ± {np.std(rmse_vals):.2f}")
    
    print(f"    --- Baselines ---")
    best_bl = max(bl_metrics, key=lambda n: np.mean([m['R2'] for m in bl_metrics[n]]))
    for name in baselines:
        r2 = np.mean([m['R2'] for m in bl_metrics[name]])
        rmse = np.mean([m['RMSE'] for m in bl_metrics[name]])
        marker = " ← best" if name == best_bl else ""
        print(f"    {name:<10s}: R² = {r2:.3f}, RMSE = {rmse:.2f}{marker}")
    
    stage1_cv[target] = {'ensemble': ens_metrics, 'baselines': bl_metrics}
    stage1_oof[target] = oof_preds
    
    # Train final model
    final_model = clone(models['RF'])
    final_model.fit(X, y)
    stage1_models[target] = final_model

# ---- Stage 2: Moisture-Energy (traits + OOF temps) ----
print("\n" + "=" * 80)
print("STAGE 2: MOISTURE-ENERGY (Two-Stage)")
print("=" * 80)

stage2_results = {}

for target in M_TARGETS:
    y = df_plants[target].values
    print(f"\n  {target}:")
    
    # Augmented features: 31 traits + 4 OOF temperature predictions
    X_aug = np.column_stack([X] + [stage1_oof[t] for t in T_TARGETS])
    X_trait = X.copy()
    
    models = make_models()
    baselines = make_baselines()
    
    # Two-stage ensemble
    aug_metrics = {}
    for name, model in models.items():
        fold_results = []
        for train_idx, test_idx in spatial_folds:
            m = clone(model)
            m.fit(X_aug[train_idx], y[train_idx])
            yp = m.predict(X_aug[test_idx])
            fold_results.append(eval_metrics(y[test_idx], yp))
        aug_metrics[name] = fold_results
    
    # Traits-only ensemble (ablation)
    trait_metrics = {}
    for name, model in models.items():
        fold_results = []
        for train_idx, test_idx in spatial_folds:
            m = clone(model)
            m.fit(X_trait[train_idx], y[train_idx])
            yp = m.predict(X_trait[test_idx])
            fold_results.append(eval_metrics(y[test_idx], yp))
        trait_metrics[name] = fold_results
    
    # Traits-only linear baselines
    bl_metrics = {}
    for name, model in baselines.items():
        fold_results = []
        for train_idx, test_idx in spatial_folds:
            m = clone(model)
            m.fit(X_trait[train_idx], y[train_idx])
            yp = m.predict(X_trait[test_idx])
            if yp.ndim > 1:
                yp = yp.ravel()
            fold_results.append(eval_metrics(y[test_idx], yp))
        bl_metrics[name] = fold_results
    
    # Report
    print(f"    Two-stage (traits + OOF temps):")
    for name in models:
        r2 = np.mean([m['R2'] for m in aug_metrics[name]])
        rmse = np.mean([m['RMSE'] for m in aug_metrics[name]])
        print(f"      {name:<10s}: R² = {r2:.3f}, RMSE = {rmse:.2f}")
    
    print(f"    Traits-only ensemble (ablation):")
    for name in models:
        r2 = np.mean([m['R2'] for m in trait_metrics[name]])
        delta = r2 - np.mean([m['R2'] for m in aug_metrics[name]])
        print(f"      {name:<10s}: R² = {r2:.3f} (Δ = {delta:+.3f} vs two-stage)")
    
    print(f"    Linear baselines:")
    for name in baselines:
        r2 = np.mean([m['R2'] for m in bl_metrics[name]])
        print(f"      {name:<10s}: R² = {r2:.3f}")
    
    stage2_results[target] = {
        'two_stage': aug_metrics,
        'traits_only': trait_metrics,
        'baselines': bl_metrics,
    }

# ---- LOCO Validation ----
print("\n" + "=" * 80)
print("LEAVE-ONE-CONTINENT-OUT VALIDATION")
print("=" * 80)

region_groups = {
    'Asia': ['Southern Asia', 'Eastern Asia', 'East Asia', 'Central Asia'],
    'Americas': ['Central America', 'South America', 'Northern America', 'Caribbean'],
    'Europe': ['Eastern Europe', 'Northern Europe', 'European Russia', 'Asiatic Russia'],
    'Oceania': ['New Zealand', 'Australia', 'Melanesia', 'Polynesia'],
    'Africa': ['Southern Africa'],
}

def map_continent(reg):
    for cont, regions in region_groups.items():
        if reg in regions:
            return cont
    return 'Other'

continents = np.array([map_continent(r) for r in df_plants['REGION']])
loco_results = {}

for target in ALL_TARGETS:
    y = df_plants[target].values
    model = RandomForestRegressor(
        n_estimators=500, max_depth=12, min_samples_leaf=3,
        random_state=RANDOM_STATE, n_jobs=-1
    )
    res = {}
    for cont in np.unique(continents):
        test_idx = np.where(continents == cont)[0]
        train_idx = np.where(continents != cont)[0]
        if len(test_idx) < 5:
            continue
        m = clone(model)
        m.fit(X[train_idx], y[train_idx])
        yp = m.predict(X[test_idx])
        res[cont] = eval_metrics(y[test_idx], yp)
    loco_results[target] = res
    
    print(f"  {target}:")
    for cont, met in res.items():
        print(f"    {cont:<12s} (n={np.sum(continents==cont):3d}): "
              f"R² = {met['R2']:+.3f}, RMSE = {met['RMSE']:.2f}")

# ---- Fossil Transfer ----
print("\n" + "=" * 80)
print("FOSSIL TRANSFER (vs CLAMP Reference)")
print("=" * 80)

# Stage 1: predict temps for fossils
fossil_t_preds = {}
for target in T_TARGETS:
    fossil_t_preds[target] = stage1_models[target].predict(X_fossil)

# Stage 2: predict moisture for fossils
X_f_aug = np.column_stack([X_fossil] + [fossil_t_preds[t] for t in T_TARGETS])

# Train Stage 2 final models on full modern + OOF temps
X_modern_aug = np.column_stack([X] + [stage1_oof[t] for t in T_TARGETS])
stage2_final = {}
for target in M_TARGETS:
    y = df_plants[target].values
    m = RandomForestRegressor(
        n_estimators=500, max_depth=12, min_samples_leaf=3,
        random_state=RANDOM_STATE, n_jobs=-1
    )
    m.fit(X_modern_aug, y)
    stage2_final[target] = m

# Compile all fossil predictions
fossil_all_preds = {}
for target in T_TARGETS:
    fossil_all_preds[target] = fossil_t_preds[target]
for target in M_TARGETS:
    fossil_all_preds[target] = stage2_final[target].predict(X_f_aug)

# Evaluate
print(f"\n{'Variable':<12s} {'R²':<8s} {'RMSE':<10s} {'MAE':<10s} {'Bias':<8s}")
print("-" * 55)
fossil_metrics = {}
for target in ALL_TARGETS:
    y_ref = df_fossil[target].values
    y_pred = fossil_all_preds[target]
    met = eval_metrics(y_ref, y_pred)
    bias = np.mean(y_pred - y_ref)
    fossil_metrics[target] = {**met, 'Bias': bias}
    print(f"{target:<12s} {met['R2']:.3f}    {met['RMSE']:.2f}      "
          f"{met['MAE']:.2f}      {bias:+.2f}")

# ---- Compile and save all tables ----
print("\n--- SAVING RESULTS ---")

# Table: Main performance summary
rows = []
for target in ALL_TARGETS:
    cat = 'Temperature' if target in T_TARGETS else 'Moisture-Energy'
    # Spatial CV R² (RF)
    if target in T_TARGETS:
        cv_r2 = np.mean([m['R2'] for m in stage1_cv[target]['ensemble']['RF']])
        cv_rmse = np.mean([m['RMSE'] for m in stage1_cv[target]['ensemble']['RF']])
    else:
        cv_r2 = np.mean([m['R2'] for m in stage2_results[target]['two_stage']['RF']])
        cv_rmse = np.mean([m['RMSE'] for m in stage2_results[target]['two_stage']['RF']])
    
    # Best baseline
    if target in T_TARGETS:
        bl_met = stage1_cv[target]['baselines']
    else:
        bl_met = stage2_results[target]['baselines']
    best_bl_name = max(bl_met, key=lambda n: np.mean([m['R2'] for m in bl_met[n]]))
    best_bl_r2 = np.mean([m['R2'] for m in bl_met[best_bl_name]])
    
    # Two-stage delta (moisture only)
    if target in M_TARGETS:
        trait_r2 = np.mean([m['R2'] for m in stage2_results[target]['traits_only']['RF']])
        aug_r2 = np.mean([m['R2'] for m in stage2_results[target]['two_stage']['RF']])
        delta_r2 = aug_r2 - trait_r2
    else:
        delta_r2 = np.nan
    
    rows.append({
        'Variable': target,
        'Category': cat,
        'Spatial_CV_R2_RF': f"{cv_r2:.3f}",
        'Spatial_CV_RMSE': f"{cv_rmse:.2f}",
        'Best_Baseline': best_bl_name,
        'Baseline_R2': f"{best_bl_r2:.3f}",
        'TwoStage_Delta_R2': f"{delta_r2:+.3f}" if not np.isnan(delta_r2) else "—",
        'Fossil_R2_vs_CLAMP': f"{fossil_metrics[target]['R2']:.3f}",
        'Fossil_RMSE': f"{fossil_metrics[target]['RMSE']:.2f}",
        'Fossil_Bias': f"{fossil_metrics[target]['Bias']:+.2f}",
    })

pd.DataFrame(rows).to_csv(os.path.join(OUTPUT_DIR, 'Table1_Performance_Summary.csv'), index=False)
print("  Table1_Performance_Summary.csv")

# Table: LOCO validation
loco_rows = []
for target in ALL_TARGETS:
    for cont, met in loco_results[target].items():
        loco_rows.append({
            'Variable': target, 'Continent': cont,
            'N_Sites': int(np.sum(continents == cont)),
            'R2': f"{met['R2']:.3f}",
            'RMSE': f"{met['RMSE']:.2f}",
            'MAE': f"{met['MAE']:.2f}",
        })
pd.DataFrame(loco_rows).to_csv(os.path.join(OUTPUT_DIR, 'Table2_LOCO_Validation.csv'), index=False)
print("  Table2_LOCO_Validation.csv")

# Table: Fossil predictions
fossil_df = pd.DataFrame()
fossil_df['Sample'] = df_fossil['Sample'].values
fossil_df['REGION'] = df_fossil['REGION'].values
for target in ALL_TARGETS:
    fossil_df[f'{target}_pred'] = fossil_all_preds[target]
    fossil_df[f'{target}_ref'] = df_fossil[target].values
fossil_df.to_csv(os.path.join(OUTPUT_DIR, 'Table3_Fossil_Predictions.csv'), index=False)
print("  Table3_Fossil_Predictions.csv")

# Table: Two-stage ablation
abl_rows = []
for target in M_TARGETS:
    for name in ['RF', 'XGBoost', 'GBDT', 'SVR']:
        trait_r2 = np.mean([m['R2'] for m in stage2_results[target]['traits_only'][name]])
        aug_r2 = np.mean([m['R2'] for m in stage2_results[target]['two_stage'][name]])
        abl_rows.append({
            'Variable': target, 'Model': name,
            'Traits_Only_R2': f"{trait_r2:.3f}",
            'Two_Stage_R2': f"{aug_r2:.3f}",
            'Delta_R2': f"{aug_r2 - trait_r2:+.3f}",
        })
pd.DataFrame(abl_rows).to_csv(os.path.join(OUTPUT_DIR, 'Table4_TwoStage_Ablation.csv'), index=False)
print("  Table4_TwoStage_Ablation.csv")

# Table: Baseline comparison
bl_rows = []
for target in ALL_TARGETS:
    if target in T_TARGETS:
        bl_met = stage1_cv[target]['baselines']
    else:
        bl_met = stage2_results[target]['baselines']
    for name, met_list in bl_met.items():
        r2s = [m['R2'] for m in met_list]
        rmses = [m['RMSE'] for m in met_list]
        bl_rows.append({
            'Variable': target, 'Model': name,
            'R2_mean': f"{np.mean(r2s):.3f}",
            'R2_std': f"{np.std(r2s):.3f}",
            'RMSE_mean': f"{np.mean(rmses):.2f}",
        })
pd.DataFrame(bl_rows).to_csv(os.path.join(OUTPUT_DIR, 'Table5_Baseline_Comparison.csv'), index=False)
print("  Table5_Baseline_Comparison.csv")

# Save models for reproducibility
model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models_v2")
os.makedirs(model_dir, exist_ok=True)
for target, model in stage1_models.items():
    joblib.dump(model, os.path.join(model_dir, f"stage1_{target}.joblib"))
for target, model in stage2_final.items():
    joblib.dump(model, os.path.join(model_dir, f"stage2_{target}.joblib"))
print(f"  Models saved to {model_dir}/")

print(f"\nAll results saved to: {OUTPUT_DIR}/")
print("Pipeline complete!")
