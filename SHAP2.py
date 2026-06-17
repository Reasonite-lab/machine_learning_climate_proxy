import joblib
import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取模型
model = joblib.load("ENTHAL_Stacking.joblib")

# 数据
file_path = "Global378+Tibet15+Fossil73_更正.xlsx"

# Modern calibration dataset (393 sites: 378 global + 15 Tibetan Plateau)
df_modern = pd.read_excel(file_path, sheet_name="plants")
# Fossil dataset (73 assemblages)
df_fossil = pd.read_excel(file_path, sheet_name="fossils")

feature_cols = [
    'Lobed', 'No Teeth', 'Teeth Regul', 'Teeth Close', 'Teeth Round', 'Teeth Acute', 'Teeth Compo',
    'Nanophyl', 'Leptophyl', 'Leptophyl 2', 'Microphyl 1', 'Microphyl 2', 'Microphyl 3',
    'Mesophyl 1', 'Mesophyl 2', 'Mesophyl 3', 'Apex Emargi', 'Apex Round', 'Apex Acute', 'Apex Attenu',
    'Base Cordat', 'Base Round', 'Base Acute', 'L:W <1:1', 'L:W 1-2:1', 'L:W 2-3:1', 'L:W 3-4:1',
    'L:W >4:1', 'Obovate', 'Elliptic', 'Ovate'
]


X = df_modern[feature_cols]

# SHAP
background = shap.sample(X, 100, random_state=42)

explainer = shap.KernelExplainer(
    model.predict,
    background
)

shap_values = explainer.shap_values(X)

importance = np.abs(shap_values).mean(axis=0)

imp_df = pd.DataFrame({
    "Feature": feature_cols,
    "Importance": importance
}).sort_values(
    "Importance",
    ascending=False
).head(10)


# Top10
imp_df = imp_df.sort_values(
    "Importance",
    ascending=True
)

# 渐变色
colors = plt.cm.viridis(
    np.linspace(
        0.2,
        0.9,
        len(imp_df)
    )
)

fig, ax = plt.subplots(
    figsize=(5,4)
)

y = np.arange(len(imp_df))

# 横线
for i in range(len(imp_df)):
    ax.hlines(
        y=y[i],
        xmin=0,
        xmax=imp_df["Importance"].iloc[i],
        color=colors[i],
        linewidth=3
    )

# 圆点
ax.scatter(
    imp_df["Importance"],
    y,
    color=colors,
    s=100,
    zorder=3
)

ax.set_yticks(y)
ax.set_yticklabels(
    imp_df["Feature"],
    fontsize=10
)

ax.set_xlabel(
    "Mean |SHAP value|",
    fontsize=12
)

# 美化
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.grid(
    axis='x',
    linestyle='--',
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "SHAP_importance_lollipop.svg",
    format='svg',
    dpi=600,
    bbox_inches='tight'
)

plt.show()
plt.tight_layout()

plt.savefig(
    "ENTHAL_SHAP_Importance.svg",
    format="svg",
    bbox_inches="tight"
)
