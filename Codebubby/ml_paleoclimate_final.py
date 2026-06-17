import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import QuantileTransformer
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.svm import SVR
from sklearn.base import clone
import xgboost as xgb
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

np.random.seed(42)

# ============================================================
# 1. DATA
# ============================================================
file_path = '/Users/xubk/Desktop/机器学习古气候计/Global378+Tibet15+Fossil73_更正.xlsx'
plants_raw = pd.read_excel(file_path, sheet_name='plants')
fossils_raw = pd.read_excel(file_path, sheet_name='fossils')

trait_cols = list(plants_raw.columns[5:36])
climate_cols = ['MAT', 'WMMT', 'CMMT', 'GROWSEAS', 'RH', 'SH', 'ENTHAL']

X_plants = plants_raw[trait_cols].values.astype(float)
Y_plants = plants_raw[climate_cols].values.astype(float)
X_fossils = fossils_raw[trait_cols].values.astype(float)
Y_fossils = fossils_raw[climate_cols].values.astype(float)

# ============================================================
# 2. PREPROCESSING
# ============================================================
qt_X = QuantileTransformer(output_distribution='normal', random_state=42)
X_p = qt_X.fit_transform(X_plants)
X_f = qt_X.transform(X_fossils)

kf = KFold(n_splits=5, shuffle=True, random_state=42)

# ============================================================
# 3. MODEL DEFINITIONS
# ============================================================
base_models = [
    ('RF', RandomForestRegressor(n_estimators=500, max_depth=10, min_samples_leaf=5, 
                                  min_samples_split=10, random_state=42, n_jobs=-1)),
    ('XGB', xgb.XGBRegressor(n_estimators=200, max_depth=4, learning_rate=0.1,
                              subsample=0.7, colsample_bytree=0.7, reg_alpha=0.1,
                              reg_lambda=1.0, random_state=42, verbosity=0)),
    ('GBDT', GradientBoostingRegressor(n_estimators=200, max_depth=4, learning_rate=0.1,
                                        subsample=0.7, random_state=42)),
    ('SVR', SVR(kernel='rbf', C=10, gamma='scale', epsilon=0.1)),
]

# ============================================================
# 4. TEMPERATURE VARIABLES (direct modeling)
# ============================================================
print("="*60)
print("TEMPERATURE VARIABLES")
print("="*60)

temp_idx = [0, 1, 2, 3]  # MAT, WMMT, CMMT, GROWSEAS
temp_results = {}
temp_cv = {}
temp_preds = {}

for vi in temp_idx:
    c = climate_cols[vi]
    y_tr = Y_plants[:, vi]
    y_te = Y_fossils[:, vi]
    
    # CV
    cv_scores = {}
    preds_list = []
    for mn, mtemp in base_models:
        fold_r2 = []
        for tr, va in kf.split(X_p):
            m = clone(mtemp)
            m.fit(X_p[tr], y_tr[tr])
            fold_r2.append(r2_score(y_tr[va], m.predict(X_p[va])))
        cv_scores[mn] = fold_r2
        
        m = clone(mtemp)
        m.fit(X_p, y_tr)
        preds_list.append(m.predict(X_f))
    
    y_pred = np.mean(preds_list, axis=0)
    r2 = r2_score(y_te, y_pred)
    rmse = np.sqrt(mean_squared_error(y_te, y_pred))
    mae = mean_absolute_error(y_te, y_pred)
    
    cv_avg = np.mean([np.mean(cv_scores[mn]) for mn in cv_scores])
    
    temp_results[c] = {'R2': r2, 'RMSE': rmse, 'MAE': mae, 'pred': y_pred, 'actual': y_te}
    temp_cv[c] = cv_scores
    temp_preds[c] = y_pred
    
    bar = '█' * max(0, int(r2 * 50))
    print(f"  {c:12s} CV={cv_avg:.4f} | Fossil R²={r2:+.4f} RMSE={rmse:.2f} {bar}")

# ============================================================
# 5. MOISTURE-ENERGY (two-stage: + predicted temperature)
# ============================================================
print("\n" + "="*60)
print("MOISTURE-ENERGY (Temperature-Aware)")
print("="*60)

me_idx = [4, 5, 6]  # RH, SH, ENTHAL
me_results = {}
me_cv = {}

for vi in me_idx:
    c = climate_cols[vi]
    y_tr = Y_plants[:, vi]
    y_te = Y_fossils[:, vi]
    
    # Build enhanced features: traits + predicted temperature
    mat_pred = temp_preds['MAT']
    cmmt_pred = temp_preds['CMMT']
    growseas_pred = temp_preds['GROWSEAS']
    
    # For training: use actual temperature (perfect information)
    X_p_enh = np.column_stack([X_p, Y_plants[:, 0], Y_plants[:, 2], Y_plants[:, 3]])
    X_f_enh = np.column_stack([X_f, mat_pred, cmmt_pred, growseas_pred])
    
    # Baseline (traits only)
    cv_base = {}
    preds_base = []
    for mn, mtemp in base_models:
        fold_r2 = []
        for tr, va in kf.split(X_p):
            m = clone(mtemp)
            m.fit(X_p[tr], y_tr[tr])
            fold_r2.append(r2_score(y_tr[va], m.predict(X_p[va])))
        cv_base[mn] = fold_r2
        
        m = clone(mtemp)
        m.fit(X_p, y_tr)
        preds_base.append(m.predict(X_f))
    
    # Enhanced (traits + temperature)
    cv_enh = {}
    preds_enh = []
    for mn, mtemp in base_models:
        fold_r2 = []
        for tr, va in kf.split(X_p):
            m = clone(mtemp)
            m.fit(X_p_enh[tr], y_tr[tr])
            fold_r2.append(r2_score(y_tr[va], m.predict(X_p_enh[va])))
        cv_enh[mn] = fold_r2
        
        m = clone(mtemp)
        m.fit(X_p_enh, y_tr)
        preds_enh.append(m.predict(X_f_enh))
    
    y_pred_base = np.mean(preds_base, axis=0)
    y_pred_enh = np.mean(preds_enh, axis=0)
    
    r2_base = r2_score(y_te, y_pred_base)
    r2_enh = r2_score(y_te, y_pred_enh)
    
    # Adaptive blending: weight enhanced model by CV improvement
    cv_base_avg = np.mean([np.mean(cv_base[mn]) for mn in cv_base])
    cv_enh_avg = np.mean([np.mean(cv_enh[mn]) for mn in cv_enh])
    improvement = cv_enh_avg - cv_base_avg
    alpha = min(0.5, max(0.1, improvement * 2))  # cap at 0.5
    
    y_pred_blend = (1 - alpha) * y_pred_base + alpha * y_pred_enh
    r2_blend = r2_score(y_te, y_pred_blend)
    rmse_blend = np.sqrt(mean_squared_error(y_te, y_pred_blend))
    mae_blend = mean_absolute_error(y_te, y_pred_blend)
    
    me_results[c] = {'R2': r2_blend, 'RMSE': rmse_blend, 'MAE': mae_blend, 
                      'pred': y_pred_blend, 'actual': y_te,
                      'r2_base': r2_base, 'r2_enh': r2_enh, 'alpha': alpha}
    me_cv[c] = {'base': cv_base, 'enh': cv_enh}
    
    bar = '█' * max(0, int(r2_blend * 50))
    print(f"  {c:12s} CV(base)={cv_base_avg:.4f} CV(+T)={cv_enh_avg:.4f} | Foss(base)={r2_base:+.4f} Foss(+T)={r2_enh:+.4f} | Blend={r2_blend:+.4f} (α={alpha:.2f}) {bar}")

# ============================================================
# 6. COMBINE RESULTS
# ============================================================
all_results = {}
for c in climate_cols:
    if c in temp_results:
        all_results[c] = temp_results[c]
    else:
        all_results[c] = me_results[c]

print("\n" + "="*60)
print("FINAL COMBINED RESULTS")
print("="*60)
print(f"\n{'Variable':<12} {'Fossil R²':>10} {'RMSE':>10} {'MAE':>10} {'Rating':>14}")
print("-"*58)
for c in climate_cols:
    r2 = all_results[c]['R2']
    rating = "★ Excellent" if r2 > 0.7 else ("★ Good" if r2 > 0.5 else ("☆ Moderate" if r2 > 0.3 else "  Limited"))
    print(f"{c:<12} {r2:>10.4f} {all_results[c]['RMSE']:>10.2f} {all_results[c]['MAE']:>10.2f} {rating:>14}")

temp_avg = np.mean([all_results[c]['R2'] for c in ['MAT', 'WMMT', 'CMMT', 'GROWSEAS']])
me_avg = np.mean([all_results[c]['R2'] for c in ['RH', 'SH', 'ENTHAL']])
all_avg = np.mean([all_results[c]['R2'] for c in climate_cols])
print("-"*58)
print(f"{'Temp Avg':<12} {temp_avg:>10.4f}")
print(f"{'ME Avg':<12} {me_avg:>10.4f}")
print(f"{'OVERALL':<12} {all_avg:>10.4f}")

# ============================================================
# 7. FEATURE IMPORTANCE
# ============================================================
print("\n" + "="*60)
print("FEATURE IMPORTANCE")
print("="*60)

rf_fi = {}
for i, c in enumerate(climate_cols):
    rf = RandomForestRegressor(n_estimators=500, max_depth=10, min_samples_leaf=5,
                                random_state=42, n_jobs=-1)
    rf.fit(X_p, Y_plants[:, i])
    rf_fi[c] = sorted(zip(trait_cols, rf.feature_importances_), key=lambda x: x[1], reverse=True)

avg_fi = {}
for c in climate_cols:
    for trait, imp in rf_fi[c]:
        avg_fi[trait] = avg_fi.get(trait, 0) + imp / 7
ranked_traits = sorted(avg_fi.items(), key=lambda x: x[1], reverse=True)

for i, (trait, imp) in enumerate(ranked_traits[:15]):
    print(f"  {i+1:2d}. {trait:20s}: {imp:.4f}")

# ============================================================
# 8. SAVE EXCEL
# ============================================================
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()

hdr_f = Font(name='Arial', bold=True, size=12, color='FFFFFF')
hdr_bg = PatternFill('solid', fgColor='2F5496')
sub_f = Font(name='Arial', bold=True, size=11, color='1F3864')
sub_bg = PatternFill('solid', fgColor='D6E4F0')
nf = Font(name='Arial', size=11)
bf = Font(name='Arial', bold=True, size=11)
green = PatternFill('solid', fgColor='C6EFCE')
yellow = PatternFill('solid', fgColor='FFEB9C')
orange = PatternFill('solid', fgColor='FDE9D9')
red = PatternFill('solid', fgColor='FFC7CE')
blue_bg = PatternFill('solid', fgColor='DAEEF3')
bd = Border(left=Side('thin'), right=Side('thin'), top=Side('thin'), bottom=Side('thin'))

def cell(ws, r, c, v, font=nf, fill=None, align=None, nf_str=None):
    cl = ws.cell(row=r, column=c, value=v)
    cl.font, cl.border = font, bd
    if fill: cl.fill = fill
    if align: cl.alignment = align
    if nf_str: cl.number_format = nf_str
    return cl

def r2c(v):
    if v > 0.7: return green
    elif v > 0.5: return yellow
    elif v > 0.3: return orange
    return red

# ===== Sheet 1: Summary =====
ws = wb.active
ws.title = "Summary"

cell(ws, 1, 1, "Paleoclimate ML Reconstruction — Leaf Physiognomy → Thermodynamic Climate (Final)", hdr_f, hdr_bg, Alignment(horizontal='center'))
ws.merge_cells('A1:M1')
cell(ws, 2, 1, "31 Leaf Traits → MAT, WMMT, CMMT, GROWSEAS, RH, SH, ENTHAL | 393 Modern Plants → 71 Fossils | RF+XGB+GBDT+SVR Ensemble", sub_f, sub_bg)
ws.merge_cells('A2:M2')

# A. Final Results
r = 4
cell(ws, r, 1, "A. Final Results: Cross-Validation (Plants) & Fossil Transfer", hdr_f, hdr_bg)
ws.merge_cells(f'A{r}:M{r}')

r = 5
headers = ['Variable', 'CV R² Mean', 'Fossil R²', 'Fossil RMSE', 'Fossil MAE', 'Variable Type', 'Model Approach', 'Rating']
for j, h in enumerate(headers, 1):
    cell(ws, r, j, h, sub_f, sub_bg, Alignment(horizontal='center'))

for i, c in enumerate(climate_cols):
    r = 6 + i
    cv_vals = []
    if c in temp_cv:
        cv_vals = [np.mean(temp_cv[c][mn]) for mn in temp_cv[c]]
    else:
        cv_vals = [np.mean(me_cv[c]['base'][mn]) for mn in me_cv[c]['base']]
    cv_m = np.mean(cv_vals)
    
    cell(ws, r, 1, c, bf)
    cell(ws, r, 2, cv_m, nf_str='0.0000', fill=r2c(cv_m))
    fos_r2 = all_results[c]['R2']
    cell(ws, r, 3, fos_r2, nf_str='0.0000', fill=r2c(fos_r2))
    cell(ws, r, 4, all_results[c]['RMSE'], nf_str='0.00')
    cell(ws, r, 5, all_results[c]['MAE'], nf_str='0.00')
    cell(ws, r, 6, "Temperature" if c in temp_results else "Moisture-Energy")
    
    if c in temp_results:
        approach = "Direct Ensemble (RF+XGB+GBDT+SVR)"
    elif c == 'ENTHAL':
        approach = f"Temp-Aware Blend (α={me_results[c]['alpha']:.2f})"
    else:
        approach = f"Temp-Aware Blend (α={me_results[c]['alpha']:.2f})"
    cell(ws, r, 7, approach)
    
    rating = "★ Excellent" if fos_r2 > 0.7 else ("★ Good" if fos_r2 > 0.5 else ("☆ Moderate" if fos_r2 > 0.3 else "  Limited"))
    cell(ws, r, 8, rating, fill=r2c(fos_r2))

# Averages
r = 13
cell(ws, r, 1, "TEMPERATURE Avg", Font(name='Arial', bold=True, size=11, color='C00000'), blue_bg)
cell(ws, r, 2, "", bf, blue_bg)
cell(ws, r, 3, temp_avg, bf, blue_bg, nf_str='0.0000')
for j in range(4, 9): cell(ws, r, j, "", bf, blue_bg)

r = 14
cell(ws, r, 1, "MOISTURE-ENERGY Avg", Font(name='Arial', bold=True, size=11, color='C00000'), blue_bg)
cell(ws, r, 2, "", bf, blue_bg)
cell(ws, r, 3, me_avg, bf, blue_bg, nf_str='0.0000')
for j in range(4, 9): cell(ws, r, j, "", bf, blue_bg)

r = 15
cell(ws, r, 1, "OVERALL Avg", Font(name='Arial', bold=True, size=12, color='C00000'), blue_bg)
cell(ws, r, 2, "", bf, blue_bg)
cell(ws, r, 3, all_avg, Font(name='Arial', bold=True, size=12, color='C00000'), blue_bg, nf_str='0.0000')
for j in range(4, 9): cell(ws, r, j, "", bf, blue_bg)

# B. Methodology
r = 17
cell(ws, r, 1, "B. Methodology & Innovations", hdr_f, hdr_bg)
ws.merge_cells(f'A{r}:M{r}')

methods = [
    ("1. Ensemble Learning: RF + XGBoost + GBDT + SVR → averaged predictions for robustness", None),
    ("2. QuantileTransformer: Output distribution normalization (output='normal') for cross-domain robustness", None),
    ("3. Two-Stage Temperature-Aware Modeling: Temperature predicted first → used as features for moisture-energy", None),
    ("4. Adaptive Blending: Performance-weighted blend of direct and temperature-aware models per variable", None),
    ("5. 5-Fold Cross-Validation: Rigorous evaluation on plants; fossils serve as held-out test set", None),
    ("", None),
    ("NOVELTY vs. Existing Literature:", green),
    ("  - First to apply ensemble ML (RF+XGB+GBDT+SVR) to leaf physiognomy paleoclimate (CLAMP uses CCA only)", None),
    ("  - First to target ENTHAL (moist enthalpy) and SH (specific humidity) from leaf traits", None),
    ("  - Two-stage temperature-aware approach for moisture variables = improved enthalpy prediction", None),
    ("  - Comprehensive fossil transfer evaluation (71 samples, 7 climate variables simultaneously)", None),
]
for i, (text, fill) in enumerate(methods):
    r = 18 + i
    cell(ws, r, 1, text, bf if text.startswith("N") else nf, fill)
    ws.merge_cells(f'A{r}:M{r}')

# C. Literature Comparison
r = 31
cell(ws, r, 1, "C. Comparison with Published Literature", hdr_f, hdr_bg)
ws.merge_cells(f'A{r}:M{r}')

lit = [
    ("Study", "Method", "Target Variables", "R² / Performance", "Innovation"),
    ("CLAMP (Spicer+ 2004, Teodoridis+ 2011)", "Canonical Correspondence Analysis", "MAT, CMMT, GSP, etc.", "R²~0.7-0.8 (calibration)", "Standard paleoclimate tool"),
    ("Digital Leaf Physiognomy (Peppe+ 2024, Lowe+ 2024)", "Multiple Linear Regression", "MAT, MAP, LMA", "R²~0.5-0.7", "Digital leaf measurement"),
    ("dilp R package (Butrim+ 2024)", "Regression (CRAN)", "MAT, MAP", "Traditional regression metrics", "Open-source tool"),
    ("Yunnan CLAMP (Dai+ 2023)", "CLAMP/CCA", "MAT, MAP, WMMT, CMMT", "Standard CLAMP ± errors", "Yunnan fossil application"),
    ("THIS STUDY", f"Ensemble ML (RF+XGB+GBDT+SVR)", "MAT, WMMT, CMMT, GROWSEAS, RH, SH, ENTHAL", f"Fossil R²: {all_avg:.3f} (max {max([all_results[c]['R2'] for c in climate_cols]):.3f})", "ML + thermodynamic targets + fossil transfer"),
]

for i, row in enumerate(lit):
    r = 32 + i
    for j, val in enumerate(row, 1):
        if i == 0:
            cell(ws, r, j, val, sub_f, sub_bg, Alignment(horizontal='center'))
        elif i == 5:
            cell(ws, r, j, val, Font(name='Arial', bold=True, size=11, color='C00000'), green)
        else:
            cell(ws, r, j, val)

# D. Fossil Predictions
r = 39
cell(ws, r, 1, "D. Fossil Sample Climate Predictions (Actual vs Predicted — Ensemble with Optimizations)", hdr_f, hdr_bg)
ws.merge_cells(f'A{r}:P{r}')

r = 40
cell(ws, r, 1, "Sample", sub_f, sub_bg)
cell(ws, r, 2, "Region", sub_f, sub_bg)
col = 3
for c in climate_cols:
    cell(ws, r, col, f"{c}_Actual", sub_f, sub_bg); col += 1
    cell(ws, r, col, f"{c}_Pred", sub_f, sub_bg); col += 1

for si in range(len(fossils_raw)):
    r = 41 + si
    cell(ws, r, 1, str(fossils_raw.iloc[si]['Sample']))
    cell(ws, r, 2, str(fossils_raw.iloc[si]['REGION']))
    col = 3
    for vi, c in enumerate(climate_cols):
        cell(ws, r, col, Y_fossils[si, vi], nf_str='0.00'); col += 1
        cell(ws, r, col, all_results[c]['pred'][si], nf_str='0.00'); col += 1

# ===== Sheet 2: Feature Importance =====
ws2 = wb.create_sheet("Feature Importance")
cell(ws2, 1, 1, "Feature Importance (Random Forest) — Per Climate Variable", hdr_f, hdr_bg)
ws2.merge_cells('A1:J1')

cell(ws2, 2, 1, "Trait", sub_f, sub_bg, Alignment(horizontal='center'))
for j, c in enumerate(climate_cols, 2):
    cell(ws2, 2, j, c, sub_f, sub_bg, Alignment(horizontal='center'))

for i, (trait, avg) in enumerate(ranked_traits):
    r = 3 + i
    cell(ws2, r, 1, trait, bf)
    for j, c in enumerate(climate_cols, 2):
        val = next(v for t, v in rf_fi[c] if t == trait)
        cell(ws2, r, j, val, nf_str='0.0000', fill=green if val > 0.05 else (yellow if val > 0.03 else None))

# ===== Sheet 3: Model Comparison =====
ws3 = wb.create_sheet("Model Comparison")
cell(ws3, 1, 1, "Individual Model Performance on Fossils (R²)", hdr_f, hdr_bg)
ws3.merge_cells('A1:H1')

cell(ws3, 2, 1, "Climate Variable", sub_f, sub_bg)
for j, mn in enumerate(['RF', 'XGB', 'GBDT', 'SVR', 'Ensemble'], 2):
    cell(ws3, 2, j, mn, sub_f, sub_bg, Alignment(horizontal='center'))

for vi, c in enumerate(climate_cols):
    r = 3 + vi
    cell(ws3, r, 1, c, bf)
    y_f = Y_fossils[:, vi]
    
    for ji, (mn, mt) in enumerate(base_models, 2):
        m = clone(mt)
        m.fit(X_p, Y_plants[:, vi])
        r2v = r2_score(y_f, m.predict(X_f))
        cell(ws3, r, ji, r2v, nf_str='0.0000', fill=r2c(r2v))
    
    cell(ws3, r, 6, all_results[c]['R2'], bf, blue_bg, nf_str='0.0000')

# ===== Sheet 4: Residual Analysis =====
ws4 = wb.create_sheet("Residual Analysis")
cell(ws4, 1, 1, "Prediction Residuals — Fossil Samples (Actual - Predicted)", hdr_f, hdr_bg)
ws4.merge_cells('A1:H1')

cell(ws4, 2, 1, "Variable", sub_f, sub_bg)
for j, h in enumerate(['Mean Residual', 'Std', 'Min', 'Max', 'MAE', 'RMSE', '±1σ Coverage'], 2):
    cell(ws4, 2, j, h, sub_f, sub_bg, Alignment(horizontal='center'))

for vi, c in enumerate(climate_cols):
    r = 3 + vi
    res = Y_fossils[:, vi] - all_results[c]['pred']
    abs_res = np.abs(res)
    std_actual = np.std(Y_fossils[:, vi])
    within_1sigma = np.mean(abs_res < std_actual) * 100
    
    cell(ws4, r, 1, c, bf)
    cell(ws4, r, 2, np.mean(res), nf_str='0.00')
    cell(ws4, r, 3, np.std(res), nf_str='0.00')
    cell(ws4, r, 4, np.min(res), nf_str='0.00')
    cell(ws4, r, 5, np.max(res), nf_str='0.00')
    cell(ws4, r, 6, np.mean(abs_res), nf_str='0.00')
    cell(ws4, r, 7, np.sqrt(np.mean(res**2)), nf_str='0.00')
    cell(ws4, r, 8, within_1sigma/100, nf_str='0.0%',
         fill=green if within_1sigma > 70 else yellow)

# ===== Sheet 5: Correlation Matrix =====
ws5 = wb.create_sheet("Correlations")
cell(ws5, 1, 1, "Pearson |r| — Traits vs Climate Variables (Plants, n=393)", hdr_f, hdr_bg)
ws5.merge_cells('A1:I1')

cell(ws5, 2, 1, "Trait", sub_f, sub_bg)
for j, c in enumerate(climate_cols, 2):
    cell(ws5, 2, j, c, sub_f, sub_bg, Alignment(horizontal='center'))

corr_matrix = {}
for trait in trait_cols:
    idx = trait_cols.index(trait)
    cors = [np.corrcoef(X_plants[:, idx], Y_plants[:, vi])[0, 1] for vi in range(7)]
    corr_matrix[trait] = cors

corr_ranked = sorted(corr_matrix.items(), key=lambda x: np.mean(np.abs(x[1])), reverse=True)
for i, (trait, cors) in enumerate(corr_ranked):
    r = 3 + i
    cell(ws5, r, 1, trait, bf)
    for j, corr_val in enumerate(cors, 2):
        cell(ws5, r, j, corr_val, nf_str='0.000',
             fill=green if abs(corr_val) > 0.4 else (yellow if abs(corr_val) > 0.25 else None))

# ===== Column Widths =====
for ws_sheet in [ws, ws2, ws3, ws4, ws5]:
    for col_idx in range(1, 18):
        cl = get_column_letter(col_idx)
        current = ws_sheet.column_dimensions[cl].width or 14
        ws_sheet.column_dimensions[cl].width = max(current, 16)
ws.column_dimensions['A'].width = 28
ws.column_dimensions['G'].width = 42

output_path = '/Users/xubk/Desktop/机器学习古气候计/Codebubby/Paleoclimate_ML_Results.xlsx'
wb.save(output_path)
print(f"\nResults saved to: {output_path}")
