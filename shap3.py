import joblib
import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数配置 ====================
# 模型文件路径列表（按套图顺序：第一行左->右，第二行左->右…）
model_files = [
    "MAT_Stacking.joblib",
    "WMMT_CatBoost.joblib",
    "CMMT_Stacking.joblib",
    "GROWSEAS_CatBoost.joblib",
    "RH_Stacking.joblib",
    "SH_Stacking.joblib",
    "ENTHAL_Stacking.joblib"
]

# 对应的子图标题（简短变量名）
titles = [
    "MAT",
    "WMMT",
    "CMMT",
    "GROWSEAS",
    "RH",
    "SH",
    "ENTHAL"
]

# 数据文件与特征列
file_path = "Global378+Tibet15+Fossil73_更正.xlsx"
feature_cols = [
    'Lobed', 'No Teeth', 'Teeth Regul', 'Teeth Close', 'Teeth Round',
    'Teeth Acute', 'Teeth Compo', 'Nanophyl', 'Leptophyl', 'Leptophyl 2',
    'Microphyl 1', 'Microphyl 2', 'Microphyl 3', 'Mesophyl 1', 'Mesophyl 2',
    'Mesophyl 3', 'Apex Emargi', 'Apex Round', 'Apex Acute', 'Apex Attenu',
    'Base Cordat', 'Base Round', 'Base Acute', 'L:W <1:1', 'L:W 1-2:1',
    'L:W 2-3:1', 'L:W 3-4:1', 'L:W >4:1', 'Obovate', 'Elliptic', 'Ovate'
]

# SHAP 背景样本数
background_samples = 100
random_state = 42

# 可选：为加速可将 nsamples 设为 500 或 "auto"
# shap_nsamples = 500   # 若不需要可注释，使用默认值
# =================================================

# 读取现代植物数据（仅需特征矩阵 X）
df_modern = pd.read_excel(file_path, sheet_name="plants")
X = df_modern[feature_cols]

# 创建全局背景数据集（所有模型共用，保证一致性）
background = shap.sample(X, background_samples, random_state=random_state)

# 创建 2 行 4 列子图
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(20, 10))
axes = axes.flatten()  # 展平便于循环

# 循环处理每个模型
for idx, (model_path, title) in enumerate(zip(model_files, titles)):
    ax = axes[idx]
    print(f"Processing {title} ({model_path}) ...")

    # 加载模型
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"  模型文件 {model_path} 未找到，跳过该子图。")
        ax.set_title(f"{title} (missing)", fontsize=12)
        ax.axis('off')
        continue

    # 创建 SHAP KernelExplainer（可根据需要设置 nsamples 参数）
    if 'shap_nsamples' in locals():
        explainer = shap.KernelExplainer(model.predict, background, nsamples=shap_nsamples)
    else:
        explainer = shap.KernelExplainer(model.predict, background)

    # 计算 SHAP 值（此处使用整个 X，若数据量大可考虑采样）
    shap_values = explainer.shap_values(X)

    # 计算平均绝对 SHAP 值（特征重要性）
    importance = np.abs(shap_values).mean(axis=0)

    # 构建 DataFrame 并取 Top10
    imp_df = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": importance
    }).sort_values("Importance", ascending=False).head(10)

    # 排序用于绘图（从小到大，方便棒棒糖图自下而上）
    imp_df = imp_df.sort_values("Importance", ascending=True)

    # 生成渐变色
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(imp_df)))
    y_pos = np.arange(len(imp_df))

    # 绘制横线
    for i in range(len(imp_df)):
        ax.hlines(y=y_pos[i], xmin=0, xmax=imp_df["Importance"].iloc[i],
                  color=colors[i], linewidth=3)

    # 绘制圆点
    ax.scatter(imp_df["Importance"], y_pos, color=colors, s=100, zorder=3)

    # 设置 y 轴标签
    ax.set_yticks(y_pos)
    ax.set_yticklabels(imp_df["Feature"], fontsize=9)

    # 设置 x 轴标签（仅左列和右列底部显示，避免重复）
    if idx % 4 == 0:  # 第一列
        ax.set_ylabel("Feature", fontsize=12)
    if idx >= 4:      # 最后一行
        ax.set_xlabel("Mean |SHAP value|", fontsize=12)

    # 子图标题
    ax.set_title(title, fontsize=13, fontweight='bold')

    # 美化
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)

# 调整整体布局
plt.suptitle("SHAP Feature Importance (Top 10)", fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout()

# 保存套图
output_file = "SHAP_importance_lollipop_panel.svg"
plt.savefig(output_file, format='svg', dpi=600, bbox_inches='tight')
print(f"\n套图已保存为 {output_file}")
plt.show()