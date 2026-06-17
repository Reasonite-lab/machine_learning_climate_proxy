#!/usr/bin/env python3
"""
Generate publication-quality figures for CP submission.
Python / matplotlib backend following Nature-figure conventions.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd
import os
from scipy.stats import spearmanr

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
    "legend.fontsize": 6.5,
    "axes.labelsize": 7.5,
    "axes.titlesize": 8,
    "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5,
})

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "Global378+Tibet15+Fossil73_更正.xlsx")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

FEATURE_LABELS = [
    'Lobed', 'No Teeth', 'Teeth Reg.', 'Teeth Close', 'Teeth Round',
    'Teeth Acute', 'Teeth Comp.', 'Nanophyll', 'Leptophyll', 'Leptophyll 2',
    'Microphyll 1', 'Microphyll 2', 'Microphyll 3', 'Mesophyll 1', 'Mesophyll 2',
    'Mesophyll 3', 'Apex Emarg.', 'Apex Round', 'Apex Acute', 'Apex Atten.',
    'Base Cordate', 'Base Round', 'Base Acute', 'L:W <1:1', 'L:W 1-2:1',
    'L:W 2-3:1', 'L:W 3-4:1', 'L:W >4:1', 'Obovate', 'Elliptic', 'Ovate'
]

TARGET_LABELS = ['MAT\n(°C)', 'WMMT\n(°C)', 'CMMT\n(°C)', 'GROWSEAS\n(months)',
                  'RH\n(%)', 'SH\n(g/kg)', 'ENTHAL\n(kJ/kg)']

# ---- Palette ----
CLR_TEMP = '#2475A0'      # blue for temperature
CLR_MOIST = '#C0392B'     # red for moisture-energy
CLR_GREEN = '#27AE60'
CLR_ORANGE = '#E67E22'
CLR_PURPLE = '#8E44AD'
CLR_GREY = '#7F8C8D'
CLR_DARK = '#2C3E50'
CLR_LIGHT = '#ECF0F1'
PALETTE_MODELS = ['#2475A0', '#E67E22', '#27AE60', '#C0392B', '#8E44AD']
MODEL_NAMES = ['Linear', 'Ridge', 'PLS', 'RF', 'XGBoost']

def save_pub(fig, name, dpi=600):
    for ext in ['svg', 'pdf', 'png', 'tiff']:
        fig.savefig(os.path.join(FIG_DIR, f"{name}.{ext}"), 
                    dpi=dpi, bbox_inches='tight')
    print(f"  Saved {name}.{{svg,pdf,png,tiff}}")

# Load data
df_plants = pd.read_excel(DATA_FILE, sheet_name="plants")
lat_col = ' Latitude        '
df_plants['LAT'] = df_plants[lat_col]
df_plants['LON'] = df_plants['Longitude']
df_fossil = pd.read_excel(DATA_FILE, sheet_name="fossils")
df_fossil['LAT'] = df_fossil['Latitude']
df_fossil['LON'] = df_fossil['Longitude']

X = df_plants[FEATURE_COLS].values.astype(np.float64)

# Load pipeline results
perf_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'Table1_Performance_Summary.csv'))
loco_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'Table2_LOCO_Validation.csv'))
fossil_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'Table3_Fossil_Predictions.csv'))
abl_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'Table4_TwoStage_Ablation.csv'))
bl_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'Table5_Baseline_Comparison.csv'))

print("Figures for CP submission")
print("=" * 60)

# ═══════════════════════════════════════════════════════════════
# Fig 1: Trait-Climate Correlation Heatmap
# Nature-figure design: color as primary encoding, significance markers,
# clean subtle grid, category sidebar via separate axes, square cells.
# ═══════════════════════════════════════════════════════════════
print("\nFig 1: Trait-Climate Correlation")

corr_matrix = np.zeros((len(FEATURE_COLS), len(ALL_TARGETS)))
p_matrix = np.zeros_like(corr_matrix)
for i, feat in enumerate(FEATURE_COLS):
    for j, target in enumerate(ALL_TARGETS):
        r, p = spearmanr(df_plants[feat].values, df_plants[target].values)
        corr_matrix[i, j] = r
        p_matrix[i, j] = p

# Category definitions
categories = [
    ('Tooth',     0,  6, '#E74C3C'),
    ('Leaf Size', 7, 15, '#3498DB'),
    ('Apex',     16, 19, '#2ECC71'),
    ('Base',     20, 22, '#F39C12'),
    ('L:W Ratio',23, 27, '#9B59B6'),
    ('Shape',    28, 30, '#1ABC9C'),
]
n_rows, n_cols = len(FEATURE_LABELS), len(ALL_TARGETS)

# Two-column layout: narrow sidebar + heatmap
fig = plt.figure(figsize=(7.8, 9.5))
gs = gridspec.GridSpec(1, 2, width_ratios=[0.06, 0.94], wspace=0.02,
                       left=0.06, right=0.92, bottom=0.05, top=0.95)
ax_cat = fig.add_subplot(gs[0, 0])   # category color bar
ax      = fig.add_subplot(gs[0, 1])   # heatmap

# --- Category sidebar ---
for cat_name, r0, r1, clr in categories:
    y_span = r1 - r0 + 1
    ax_cat.add_patch(plt.Rectangle(
        (0, r0 - 0.5), 1, y_span, facecolor=clr, edgecolor='white',
        linewidth=0.3, alpha=0.85, transform=ax_cat.transData))
ax_cat.set_xlim(0, 1)
ax_cat.set_ylim(n_rows - 0.5, -0.5)
ax_cat.set_xticks([])
ax_cat.set_yticks([])
for spine in ax_cat.spines.values():
    spine.set_visible(False)

# --- Heatmap ---
im = ax.imshow(corr_matrix, cmap='RdBu_r', aspect='equal',
               vmin=-0.8, vmax=0.8, interpolation='nearest')

# Subtle white grid lines behind the heatmap
for i in range(n_rows + 1):
    ax.axhline(y=i - 0.5, color='white', linewidth=0.4, zorder=0)
for j in range(n_cols + 1):
    ax.axvline(x=j - 0.5, color='white', linewidth=0.4, zorder=0)

# Significance markers: ★ p<0.001,  ● p<0.01
for i in range(n_rows):
    for j in range(n_cols):
        p_val = p_matrix[i, j]
        if p_val < 0.001:
            marker, fs = '●', 6.0
        elif p_val < 0.01:
            marker, fs = '●', 4.0
        else:
            continue
        # Adaptive contrast: white marker on dark cells
        abs_r = abs(corr_matrix[i, j])
        text_color = 'white' if abs_r > 0.5 else 'black'
        ax.text(j, i, marker, ha='center', va='center', fontsize=fs,
                color=text_color, zorder=5)

# X axis: climate-variable labels with group annotation
ax.set_xticks(range(n_cols))
ax.set_xticklabels(TARGET_LABELS, fontsize=6.5, rotation=0)

# Add temperature / moisture group labels
temp_x  = np.mean(range(4))   # 0,1,2,3 → MAT,WMMT,CMMT,GROWSEAS
moist_x = np.mean(range(4, 7))  # 4,5,6 → RH,SH,ENTHAL
ax.text(temp_x, -0.55, 'Temperature', ha='center', va='top',
        fontsize=6.5, fontweight='bold', color=CLR_TEMP, transform=ax.transData)
ax.text(moist_x, -0.55, 'Moisture–Energy', ha='center', va='top',
        fontsize=6.5, fontweight='bold', color=CLR_MOIST, transform=ax.transData)
# Thin bracket lines
ax.plot([-0.4, 3.4], [-0.35, -0.35], color=CLR_TEMP, linewidth=0.6,
        transform=ax.transData, clip_on=False)
ax.plot([3.6, 6.4], [-0.35, -0.35], color=CLR_MOIST, linewidth=0.6,
        transform=ax.transData, clip_on=False)

# Y axis: trait labels
ax.set_yticks(range(n_rows))
ax.set_yticklabels(FEATURE_LABELS, fontsize=6.5)
# Category labels on the right side of y-axis
for cat_name, r0, r1, clr in categories:
    y_mid = (r0 + r1) / 2
    ax.text(n_cols + 0.6, y_mid, cat_name, fontsize=6, ha='left', va='center',
            color=clr, fontweight='bold', transform=ax.transData, clip_on=False)

ax.set_xlim(-0.5, n_cols - 0.5)
ax.tick_params(axis='both', length=2, pad=2)

# Colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.75, pad=0.015, aspect=35)
cbar.set_label('Spearman ρ', fontsize=7)
cbar.ax.tick_params(labelsize=6)

ax.set_title('Leaf trait–climate correlation matrix',
             fontsize=8.5, fontweight='bold', pad=12)
save_pub(fig, 'Fig1_trait_climate_corr')

# ═══════════════════════════════════════════════════════════════
# Fig 2: Spatial CV Performance — Model Comparison
# ═══════════════════════════════════════════════════════════════
print("\nFig 2: Spatial CV Model Comparison")

# Parse data
targets_list = [ALL_TARGETS[i] for i in [0, 2, 3, 4, 5, 6]]  # skip WMMT
targets_short = ['MAT', 'CMMT', 'GROWSEAS', 'RH', 'SH', 'ENTHAL']

# Extract R2 values from baseline comparison
model_data = {m: [] for m in MODEL_NAMES}
for target in targets_short:
    for model in MODEL_NAMES:
        row = bl_df[(bl_df['Variable'] == target) & (bl_df['Model'] == model)]
        if len(row) > 0:
            r2 = float(row['R2_mean'].values[0])
        else:
            r2 = np.nan
        model_data[model].append(r2)

fig, ax = plt.subplots(figsize=(7, 3.5))
x = np.arange(len(targets_short))
width = 0.15
bars = []
for i, (model, clr) in enumerate(zip(MODEL_NAMES, PALETTE_MODELS)):
    vals = model_data[model]
    bar = ax.bar(x + i * width - width * 2, vals, width, label=model,
                 color=clr, edgecolor='white', linewidth=0.3, alpha=0.9)
    bars.append(bar)
    # Add value labels
    for j, v in enumerate(vals):
        if not np.isnan(v) and v > 0:
            ax.text(x[j] + i * width - width * 2, v + 0.02, f'{v:.2f}',
                    ha='center', fontsize=5, rotation=90)

ax.axhline(y=0, color='grey', linewidth=0.5, linestyle='--')
ax.set_xticks(x)
ax.set_xticklabels(targets_short, fontsize=7)
ax.set_ylabel('Spatial CV R²', fontsize=7.5)
ax.legend(ncol=5, fontsize=6, loc='upper left', bbox_to_anchor=(0, 1.15))
ax.set_ylim(-1.2, 0.6)
ax.set_title('Fig 2: Spatial cross-validation performance comparison', 
             fontsize=8, fontweight='bold')

# Add category separators
ax.axvline(x=2.5, color=CLR_GREY, linewidth=0.5, linestyle=':')
ax.text(1, ax.get_ylim()[0] + 0.1, 'Temperature', ha='center', fontsize=6, color=CLR_TEMP)
ax.text(4, ax.get_ylim()[0] + 0.1, 'Moisture-Energy', ha='center', fontsize=6, color=CLR_MOIST)

plt.tight_layout()
save_pub(fig, 'Fig2_model_comparison')

# ═══════════════════════════════════════════════════════════════
# Fig 3: Observed vs Predicted — Fossil Transfer + CV
# ═══════════════════════════════════════════════════════════════
print("\nFig 3: Observed vs Predicted")

fig, axes = plt.subplots(2, 4, figsize=(8.5, 5))
axes = axes.flatten()

plot_targets = ['MAT', 'CMMT', 'GROWSEAS', 'SH', 'ENTHAL']
for idx, target in enumerate(plot_targets):
    ax = axes[idx]
    y_ref = df_fossil[target].values
    y_pred = fossil_df[f'{target}_pred'].values
    r2 = np.corrcoef(y_ref, y_pred)[0, 1] ** 2
    rmse = np.sqrt(np.mean((y_ref - y_pred) ** 2))
    
    ax.scatter(y_ref, y_pred, s=20, alpha=0.6, c=CLR_TEMP if target in T_TARGETS else CLR_MOIST,
               edgecolors='white', linewidth=0.3)
    
    lims = [min(y_ref.min(), y_pred.min()) - 2, max(y_ref.max(), y_pred.max()) + 2]
    ax.plot(lims, lims, 'k--', linewidth=0.5, alpha=0.5)
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_xlabel('CLAMP Reference', fontsize=6)
    ax.set_ylabel('ML Prediction', fontsize=6)
    ax.set_title(f'{target}\nR² = {r2:.2f}  RMSE = {rmse:.1f}', fontsize=7, fontweight='bold')
    ax.set_aspect('equal')

# Last subplot: map or spatial distribution
ax = axes[5]
# Show LOCO R2 as heatmap-like
loco_wide = loco_df[loco_df['Variable'].isin(['MAT', 'CMMT', 'GROWSEAS', 'SH', 'ENTHAL'])].pivot(
    index='Continent', columns='Variable', values='R2')
continents = ['Asia', 'Americas', 'Oceania', 'Africa', 'Europe']
loco_wide = loco_wide.reindex(continents)
loco_data = loco_wide.values.astype(float)

im = ax.imshow(loco_data, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=0.7)
ax.set_xticks(range(len(plot_targets)))
ax.set_xticklabels(plot_targets, fontsize=6, rotation=45, ha='right')
ax.set_yticks(range(len(continents)))
ax.set_yticklabels(continents, fontsize=6)
for i in range(len(continents)):
    for j in range(len(plot_targets)):
        val = loco_data[i, j]
        ax.text(j, i, f'{val:.2f}', ha='center', va='center', fontsize=5,
                color='white' if abs(val) > 0.4 else 'black')
ax.set_title('Leave-One-Continent-Out R²', fontsize=7, fontweight='bold')

# Remaining axes: hide
for idx in [6, 7]:
    axes[idx].set_visible(False)

fig.suptitle('Fig 3: Fossil transfer performance vs CLAMP reference and cross-continent validation',
             fontsize=8, fontweight='bold', y=1.01)
plt.tight_layout()
save_pub(fig, 'Fig3_obs_vs_pred')

# ═══════════════════════════════════════════════════════════════
# Fig 4: Feature Importance
# ═══════════════════════════════════════════════════════════════
print("\nFig 4: Feature Importance")

from sklearn.ensemble import RandomForestRegressor

fig, axes = plt.subplots(1, 3, figsize=(8, 5), gridspec_kw={'width_ratios': [3, 3, 2]})

# Panel A: Feature importance across targets (heatmap)
importance_matrix = np.zeros((len(FEATURE_COLS), len(ALL_TARGETS)))
for j, target in enumerate(ALL_TARGETS):
    y = df_plants[target].values
    rf = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    importance_matrix[:, j] = rf.feature_importances_

ax = axes[0]
im = ax.imshow(importance_matrix, cmap='YlOrRd', aspect='auto')
ax.set_xticks(range(len(ALL_TARGETS)))
ax.set_xticklabels(ALL_TARGETS, fontsize=6, rotation=45, ha='right')
ax.set_yticks(range(len(FEATURE_COLS)))
ax.set_yticklabels(FEATURE_LABELS, fontsize=5)
ax.set_title('a) RF Feature Importance', fontsize=7.5, fontweight='bold')
cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.ax.tick_params(labelsize=5)

# Panel B: Top 10 features for MAT (bar chart)
y_mat = df_plants['MAT'].values
rf_mat = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
rf_mat.fit(X, y_mat)
imp_mat = pd.DataFrame({'Feature': FEATURE_COLS, 'Importance': rf_mat.feature_importances_})
imp_mat = imp_mat.sort_values('Importance', ascending=True).tail(10)

ax = axes[1]
colors = plt.cm.Blues(np.linspace(0.3, 0.9, 10))
ax.barh(range(10), imp_mat['Importance'].values, color=colors, edgecolor='white', linewidth=0.3)
ax.set_yticks(range(10))
ax.set_yticklabels(imp_mat['Feature'].values, fontsize=6)
ax.set_xlabel('Importance', fontsize=7)
ax.set_title('b) Top 10 — MAT', fontsize=7.5, fontweight='bold')

# Panel C: Trait category contributions
cats = {
    'Tooth': ['Lobed', 'No Teeth', 'Teeth Regul', 'Teeth Close', 'Teeth Round', 'Teeth Acute', 'Teeth Compo'],
    'Leaf Size': ['Nanophyl', 'Leptophyl', 'Leptophyl 2', 'Microphyl 1', 'Microphyl 2', 'Microphyl 3', 
                  'Mesophyl 1', 'Mesophyl 2', 'Mesophyl 3'],
    'Apex': ['Apex Emargi', 'Apex Round', 'Apex Acute', 'Apex Attenu'],
    'Base': ['Base Cordat', 'Base Round', 'Base Acute'],
    'L:W': ['L:W <1:1', 'L:W 1-2:1', 'L:W 2-3:1', 'L:W 3-4:1', 'L:W >4:1'],
    'Shape': ['Obovate', 'Elliptic', 'Ovate'],
}
cat_contrib = {}
for cat, feats in cats.items():
    idxs = [FEATURE_COLS.index(f) for f in feats if f in FEATURE_COLS]
    cat_contrib[cat] = rf_mat.feature_importances_[idxs].sum()

ax = axes[2]
cat_names = list(cat_contrib.keys())
cat_vals = list(cat_contrib.values())
colors_pie = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#1ABC9C']
wedges, texts, autotexts = ax.pie(cat_vals, labels=cat_names, autopct='%1.0f%%',
                                    colors=colors_pie, textprops={'fontsize': 5.5},
                                    pctdistance=0.75, labeldistance=1.15)
for at in autotexts:
    at.set_fontsize(5)
ax.set_title('c) Category Share (MAT)', fontsize=7.5, fontweight='bold')

fig.suptitle('Fig 4: Feature importance analysis', fontsize=8, fontweight='bold', y=1.01)
plt.tight_layout()
save_pub(fig, 'Fig4_feature_importance')

# ═══════════════════════════════════════════════════════════════
# Fig 5: Two-Stage Ablation Analysis
# ═══════════════════════════════════════════════════════════════
print("\nFig 5: Two-Stage Ablation")

fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.5))

# Panel A: Two-stage vs traits-only for moisture variables
ax = axes[0]
for target, marker, clr in [('SH', 'o', CLR_ORANGE), ('ENTHAL', 's', CLR_PURPLE), ('RH', '^', CLR_GREY)]:
    sub = abl_df[abl_df['Variable'] == target]
    trait_vals = [float(sub[sub['Model'] == m]['Traits_Only_R2'].values[0]) for m in ['RF', 'XGBoost', 'GBDT', 'SVR']]
    two_vals = [float(sub[sub['Model'] == m]['Two_Stage_R2'].values[0]) for m in ['RF', 'XGBoost', 'GBDT', 'SVR']]
    ax.scatter(trait_vals, two_vals, s=60, marker=marker, label=target,
               c=clr, edgecolors='white', linewidth=0.5, zorder=5)

lim_min = -0.6
lim_max = 0.6
ax.plot([lim_min, lim_max], [lim_min, lim_max], 'k--', linewidth=0.5, alpha=0.3)
ax.axhline(y=0, color='grey', linewidth=0.3)
ax.axvline(x=0, color='grey', linewidth=0.3)
ax.set_xlim(lim_min, lim_max)
ax.set_ylim(lim_min, lim_max)
ax.set_xlabel('Spatial CV R² (traits only)', fontsize=7)
ax.set_ylabel('Spatial CV R² (two-stage)', fontsize=7)
ax.legend(fontsize=6)
ax.set_title('a) Two-Stage vs Traits-Only', fontsize=7.5, fontweight='bold')
ax.set_aspect('equal')

# Panel B: Fossil transfer performance summary
ax = axes[1]
# Compare spatial CV R2 vs fossil transfer R2
var_list = ['MAT', 'CMMT', 'GROWSEAS', 'SH', 'ENTHAL']
cv_r2 = []
fos_r2 = []
for target in var_list:
    row = perf_df[perf_df['Variable'] == target]
    cv_r2.append(float(row['Spatial_CV_R2_RF'].values[0]))
    fos_r2.append(float(row['Fossil_R2_vs_CLAMP'].values[0]))

x_pos = np.arange(len(var_list))
width = 0.35
bars1 = ax.bar(x_pos - width/2, cv_r2, width, label='Spatial CV R²', 
               color=CLR_TEMP, edgecolor='white', linewidth=0.3)
bars2 = ax.bar(x_pos + width/2, fos_r2, width, label='Fossil Transfer R² (vs CLAMP)',
               color=CLR_GREEN, edgecolor='white', linewidth=0.3)

# Add value labels
for bar in [bars1, bars2]:
    for rect in bar:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, h + 0.02, f'{h:.2f}',
                ha='center', fontsize=5, rotation=90)

ax.axhline(y=0, color='grey', linewidth=0.5, linestyle='--')
ax.set_xticks(x_pos)
ax.set_xticklabels(var_list, fontsize=7)
ax.set_ylabel('R²', fontsize=7)
ax.legend(fontsize=6, loc='upper left')
ax.set_title('b) Spatial CV vs Fossil Transfer', fontsize=7.5, fontweight='bold')

fig.suptitle('Fig 5: Two-stage architecture assessment', fontsize=8, fontweight='bold', y=1.02)
plt.tight_layout()
save_pub(fig, 'Fig5_two_stage_ablation')

print("\nAll figures generated successfully!")
print(f"Saved to: {FIG_DIR}/")
