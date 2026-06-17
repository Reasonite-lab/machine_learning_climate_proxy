#!/usr/bin/env python3
"""
Figure 1: Trait–Climate Spearman Correlation Heatmap.
Nature-figure conventions. Python / matplotlib backend.

Core conclusion:
  Leaf physiognomic traits show structured but moderate Spearman correlations
  with climate variables across 393 modern woody dicot sites — tooth and
  leaf-size traits dominate the signal, moisture-energy variables show the
  weakest associations.

Archetype: quantitative grid — single-panel heatmap with category sidebar.
Target journal: Climate of the Past.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import spearmanr

# ═══════════════════════════════════════════════════════════════════════
# MANDATORY: editable SVG/PDF text
# ═══════════════════════════════════════════════════════════════════════
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['font.size'] = 7
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['legend.frameon'] = False

# ═══════════════════════════════════════════════════════════════════════
# PALETTE (from skill API)
# ═══════════════════════════════════════════════════════════════════════
PALETTE = {
    "blue_main":      "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_3":        "#8BCF8B",
    "red_strong":     "#B64342",
    "neutral_light":  "#CFCECE",
    "neutral_mid":    "#767676",
    "neutral_dark":   "#4D4D4D",
    "neutral_black":  "#272727",
    "teal":           "#42949E",
    "violet":         "#9A4D8E",
}
# Category colors — warm sequence for distinct trait groups
CAT_COLORS = {
    'Tooth':       '#E74C3C',
    'Leaf Size':   '#3498DB',
    'Apex':        '#2ECC71',
    'Base':        '#F39C12',
    'L:W Ratio':   '#9B59B6',
    'Shape':       '#1ABC9C',
}

# ═══════════════════════════════════════════════════════════════════════
# Paths
# ═══════════════════════════════════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent
DATAFILE = BASE_DIR / "Global378+Tibet15+Fossil73_更正_副本.xlsx"
OUTNAME  = "Fig1_trait_climate_corr"

# ═══════════════════════════════════════════════════════════════════════
# Data definitions
# ═══════════════════════════════════════════════════════════════════════
FEATURE_COLS = [
    'Lobed', 'No Teeth', 'Teeth Regul', 'Teeth Close', 'Teeth Round',
    'Teeth Acute', 'Teeth Compo', 'Nanophyl', 'Leptophyl', 'Leptophyl 2',
    'Microphyl 1', 'Microphyl 2', 'Microphyl 3', 'Mesophyl 1', 'Mesophyl 2',
    'Mesophyl 3', 'Apex Emargi', 'Apex Round', 'Apex Acute', 'Apex Attenu',
    'Base Cordat', 'Base Round', 'Base Acute', 'L:W <1:1', 'L:W 1-2:1',
    'L:W 2-3:1', 'L:W 3-4:1', 'L:W >4:1', 'Obovate', 'Elliptic', 'Ovate'
]

FEATURE_LABELS = [
    'Lobed', 'No Teeth', 'Teeth Regul', 'Teeth Close', 'Teeth Round',
    'Teeth Acute', 'Teeth Compo', 'Nanophyll', 'Leptophyll', 'Leptophyll 2',
    'Microphyll 1', 'Microphyll 2', 'Microphyll 3', 'Mesophyll 1', 'Mesophyll 2',
    'Mesophyll 3', 'Apex Emargi', 'Apex Round', 'Apex Acute', 'Apex Attenu',
    'Base Cordate', 'Base Round', 'Base Acute', 'L:W <1:1', 'L:W 1–2:1',
    'L:W 2–3:1', 'L:W 3–4:1', 'L:W >4:1', 'Obovate', 'Elliptic', 'Ovate'
]

ALL_TARGETS = ['MAT', 'WMMT', 'CMMT', 'GROWSEAS', 'RH', 'SH', 'ENTHAL']
TARGET_LABELS = [
    'MAT\n(°C)', 'WMMT\n(°C)', 'CMMT\n(°C)',
    'GROWSEAS\n(mo)', 'RH\n(%)', 'SH\n(g/kg)', 'ENTHAL\n(kJ/kg)'
]

# Trait categories: (name, start_idx, end_idx_inclusive, color)
CATEGORIES = [
    ('Tooth',       0,  6, CAT_COLORS['Tooth']),
    ('Leaf Size',   7, 15, CAT_COLORS['Leaf Size']),
    ('Apex',       16, 19, CAT_COLORS['Apex']),
    ('Base',       20, 22, CAT_COLORS['Base']),
    ('L:W Ratio',  23, 27, CAT_COLORS['L:W Ratio']),
    ('Shape',      28, 30, CAT_COLORS['Shape']),
]

# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════
def is_dark(hex_color, threshold=128):
    c = hex_color.lstrip('#')
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) < threshold

def save_pub(fig, name, dpi_tiff=600, dpi_png=300):
    fig.savefig(BASE_DIR / f"{name}.svg", bbox_inches="tight")
    fig.savefig(BASE_DIR / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(BASE_DIR / f"{name}.tiff", dpi=dpi_tiff, bbox_inches="tight",
                pil_kwargs={"compression": "tiff_lzw"})
    fig.savefig(BASE_DIR / f"{name}.png", dpi=dpi_png, bbox_inches="tight")
    print(f"  Saved: {name}.{{svg, pdf, tiff, png}}")

# ═══════════════════════════════════════════════════════════════════════
# Load data & compute Spearman correlations
# ═══════════════════════════════════════════════════════════════════════
print("Loading data...")
df = pd.read_excel(DATAFILE, sheet_name='plants')
n_samples = len(df)

n_rows = len(FEATURE_COLS)
n_cols = len(ALL_TARGETS)

corr_matrix = np.zeros((n_rows, n_cols))
p_matrix = np.zeros_like(corr_matrix)

for i, feat in enumerate(FEATURE_COLS):
    for j, target in enumerate(ALL_TARGETS):
        r, p = spearmanr(df[feat].values, df[target].values)
        corr_matrix[i, j] = r
        p_matrix[i, j] = p

print(f"  N = {n_samples} sites")
print(f"  Spearman ρ range: [{corr_matrix.min():.3f}, {corr_matrix.max():.3f}]")
print(f"  Mean |ρ| = {np.abs(corr_matrix).mean():.3f}")

# ═══════════════════════════════════════════════════════════════════════
# Build Figure
# ═══════════════════════════════════════════════════════════════════════
print("\nBuilding Figure 1: Trait–Climate Spearman Heatmap ...")

# Layout: wide left sidebar (category colors + labels) + heatmap
# Left sidebar is wider so color blocks span the trait-name region
fig = plt.figure(figsize=(9.5, 8.5))
gs = gridspec.GridSpec(
    1, 2, width_ratios=[0.12, 0.88], wspace=0.02,
    left=0.06, right=0.93, bottom=0.07, top=0.95
)
ax_cat = fig.add_subplot(gs[0, 0])  # category color bar + labels
ax     = fig.add_subplot(gs[0, 1])  # heatmap

# ── Left sidebar: colored bands + category names (no bracket lines) ──
for cat_name, r0, r1, clr in CATEGORIES:
    y_bottom = r0 - 0.5
    y_top = r1 + 0.5
    y_mid = (r0 + r1) / 2
    # Color band
    ax_cat.add_patch(plt.Rectangle(
        (0, y_bottom), 1, y_top - y_bottom,
        facecolor=clr, edgecolor='white', linewidth=0.3, alpha=0.88,
        transform=ax_cat.transData
    ))
    # Category name placed far left to avoid overlapping trait labels (smaller font, flush-left)
    ax_cat.text(0.05, y_mid, cat_name,
                ha='left', va='center', fontsize=5.5, fontweight='bold',
                color='white', transform=ax_cat.transData,
                zorder=10)

ax_cat.set_xlim(0, 1)
ax_cat.set_ylim(n_rows - 0.5, -0.5)
ax_cat.set_xticks([])
ax_cat.set_yticks([])
for spine in ax_cat.spines.values():
    spine.set_visible(False)

# ── Heatmap ──
vlim = 0.8  # symmetric
im = ax.imshow(corr_matrix, cmap='RdBu_r', aspect='auto',
               vmin=-vlim, vmax=vlim, interpolation='nearest')

# Subtle white grid lines
for i in range(n_rows + 1):
    ax.axhline(y=i - 0.5, color='white', linewidth=0.4, zorder=0)
for j in range(n_cols + 1):
    ax.axvline(x=j - 0.5, color='white', linewidth=0.4, zorder=0)

# Numeric values (Bonferroni significance determined but shown via bold text, not dots)
n_tests = n_rows * n_cols  # 217
p_threshold = 0.01 / n_tests
print(f"  Bonferroni threshold = 0.01 / {n_tests} = {p_threshold:.2e}")
n_sig_bonf = 0
for i in range(n_rows):
    for j in range(n_cols):
        r_val = corr_matrix[i, j]
        abs_r = abs(r_val)
        p_val = p_matrix[i, j]
        is_sig = p_val < p_threshold
        if is_sig:
            n_sig_bonf += 1
        # Text color: white on dark cells, bold + underlined for significance
        text_color = 'white' if abs_r > 0.5 else PALETTE["neutral_dark"]
        fw = 'bold' if is_sig else 'normal'
        # Use asterisk to mark Bonferroni-significant values
        val_str = f'{r_val:.2f}*' if is_sig else f'{r_val:.2f}'
        ax.text(j, i, val_str, ha='center', va='center',
                fontsize=5.8, fontweight=fw, color=text_color, zorder=6)
print(f"  Significant after Bonferroni: {n_sig_bonf} / {n_tests}")

# ── Axis labels ──
ax.set_xticks(range(n_cols))
ax.set_xticklabels(TARGET_LABELS, fontsize=7, rotation=0)
ax.set_yticks(range(n_rows))
ax.set_yticklabels(FEATURE_LABELS, fontsize=6.5)
ax.set_xlim(-0.5, n_cols - 0.5)

# ── Colorbar ──
cbar = plt.colorbar(im, ax=ax, shrink=0.7, pad=0.02, aspect=35)
cbar.set_label('Spearman ρ', fontsize=7, color=PALETTE["neutral_black"])
cbar.ax.tick_params(labelsize=6)
cbar.set_ticks([-0.8, -0.4, 0, 0.4, 0.8])

# ── Title ──
ax.set_title(
    'Leaf trait–climate Spearman correlations\n(n = 393 modern woody dicot sites)',
    fontsize=8.5, fontweight='bold', pad=10, color=PALETTE["neutral_black"],
    linespacing=1.3
)

# ── Footer legend (above bottom margin, not overlapping x labels) ──
legend_text = (
    '* Bold = p < 0.01 (Bonferroni-corrected; 217 tests)'
)
fig.text(0.5, 0.02, legend_text, ha='center', fontsize=6,
         color=PALETTE["neutral_mid"], fontstyle='italic')

# ═══════════════════════════════════════════════════════════════════════
# Export
# ═══════════════════════════════════════════════════════════════════════
print("Exporting ...")
save_pub(fig, OUTNAME)
plt.close(fig)
print(f"\n✅ Figure 1 regenerated: {OUTNAME}.{{svg, pdf, tiff, png}}")
print("   Spearman ρ | N=393 | 31 traits × 7 climate variables")
print("   Category sidebar: Tooth | Leaf Size | Apex | Base | L:W Ratio | Shape")
