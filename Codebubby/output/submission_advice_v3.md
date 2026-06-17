# `Manuscript_Paleoclimate_ML_CP_v3.docx` 投稿建议与 Nature-style 预审意见

## Review setup

- **Input scope:** 已审阅 `Manuscript_Paleoclimate_ML_CP_v3.docx` 的题名、摘要、引言、方法、结果、讨论、结论、Data and Code Availability、参考文献结构，以及文稿中 5 张图和 2 个表的主要叙述。
- **Assessment boundary:** 本意见基于当前 Word 文稿内容和可见图表说明；未重新运行模型、未核验原始数据、未逐篇验证所有参考文献 DOI/元数据，也未进行外部文献系统检索。
- **Shared manuscript claim summary:** 文章提出用 31 个叶相性状、393 个现代样点和 71 个化石组合，构建 RF/XGBoost/GBDT/SVR 加权集成模型；直接预测温度变量，并通过两阶段温度感知结构预测 RH/SH/ENTHAL 等湿度-能量变量。核心结果包括 CMMT fossil transfer R² = 0.802、GROWSEAS R² = 0.608、MAT R² = 0.579，以及 SH/ENTHAL 经两阶段增强后达到 R² = 0.329/0.459。
- **Visible evidence base:** 5 张图：性状-气候相关热图、观测-预测散点、特征重要性、模型比较、两阶段残差；2 个表：模型总体性能与单模型/集成模型比较。
- **Missing materials affecting confidence:** 原始数据、空间折叠方案、外部验证细节、化石样点“真实值/参考值”来源、模型训练代码、超参数调优记录、source data、仓库 DOI、Zenodo DOI、图表源数据和补充材料尚未在文稿中以可审稿方式落实。

---

## Reviewer 1 — technical soundness foregrounded

### Overall assessment

该稿件有清晰的方法学目标：用非线性集成学习扩展传统叶相古气候重建，并尝试将温度预测传递到湿度-能量变量。思路有潜力，但当前技术证据链尚不足以支撑“first demonstration”和“fossil transfer performance”这样的强表述。最大问题不是写作，而是验证定义、数据泄漏风险、外部可迁移性和基准比较不足。

### Who would be interested in the results, and why

- 古植物学、古气候重建、CLAMP/LMA/DLP 使用者会关心，因为该方法试图从同一叶相性状集预测更多气候变量。
- 地球系统建模和古气候边界条件研究者可能关心 SH/ENTHAL，但前提是这些变量的预测误差和不确定性得到严格验证。
- 机器学习应用于地学 proxy calibration 的读者会关心其空间交叉验证和两阶段架构是否避免泄漏。

### Major strengths

- 问题定义明确：传统线性叶相方法变量范围窄、非线性关系不足。
- 结果组织完整：相关性、预测性能、特征重要性、模型比较、残差分析均已覆盖。
- 承认负结果：WMMT 与 RH 预测失败被明确报告，这比选择性呈现更可信。
- 两阶段温度增强的想法合理，和 Clausius-Clapeyron 物理约束存在概念联系。

### Major concerns

1. **“Fossil R²” 的定义需要立即澄清。** 化石组合通常没有直接观测的真实古气候值。文稿必须说明 `Fossil R²` 的参考真值来自哪里：独立 proxy？文献重建？现代对应点？还是模拟实验？如果只是与已有模型/插值气候比较，不能称为观测-预测 R²。
2. **两阶段模型存在潜在数据泄漏风险。** Stage 2 若使用由全训练集拟合的 Stage 1 预测温度作为特征，再进行 CV，会高估性能。必须使用 out-of-fold stage-1 predictions 训练 stage 2，并在化石/外部数据上保持完全独立流程。
3. **QuantileTransformer 可能泄漏。** 必须确认每个 CV fold 中 transformer 只在训练 fold 上拟合，再应用于验证 fold；不能在全数据上先拟合。
4. **权重优化缺少嵌套验证。** 模型权重通过 grid search 最小化 10-fold CV RMSE，若同一 CV 同时用于调权和报告性能，会造成乐观偏差。建议 nested CV 或独立 validation。
5. **空间交叉验证描述不足。** “10-fold stratified spatial split” 需要给出空间分组方式、距离阈值、坐标分布、fold 地图、是否按大陆/气候区分层。
6. **和传统方法缺少同数据集直接 benchmark。** 当前只引用 CLAMP/DLP 文献中的 R²，不能证明本方法优于传统方法。应在相同现代/化石数据上运行 CLAMP/LMA/DLP 或至少建立可比 baseline。

### Technical failings that need to be addressed before the case is established

- 明确 `Fossil R²` 的真值定义和误差传播。
- 重做或补充无泄漏的 nested spatial CV。
- 提供 independent hold-out 或 leave-region-out 验证，尤其是 Asia-dominant fossil dataset 的跨区域泛化。
- 给出预测区间/不确定性，而不仅是 R²/RMSE/MAE。
- 对两阶段增强做消融实验：traits-only、true temperature auxiliary、predicted temperature auxiliary、shuffled temperature control。
- 将所有图表源数据和代码归档到 DOI 仓库。

### Assessment against Nature-style criteria

- **Originality:** 中等偏强；两阶段温度增强用于叶相湿度-能量变量有新意，但“first demonstration”未被系统文献检索证实。
- **Scientific importance:** 对叶相 proxy 领域有意义；目前尚未达到很宽的跨学科突破级别。
- **Interdisciplinary readership:** 有潜力连接古植物、古气候、ML、地球系统建模，但当前结果仍偏方法应用。
- **Technical soundness:** 当前为主要短板，需要补充验证。
- **Readability:** 基本清楚，但方法细节不足导致审稿人无法复现判断。

### Recommendation posture

**Major revision before submission**。不建议现在直接投较高影响力 Nature-family 地学期刊；可以先作为 `Climate of the Past` 或 `Palaeogeography, Palaeoclimatology, Palaeoecology` 的方法型稿件修改。

---

## Reviewer 2 — originality and significance foregrounded

### Overall assessment

稿件的中心创意是把叶相机器学习从传统温度/降水目标扩展到 SH 和 enthalpy，并将温度预测作为物理相关辅助变量。这是一个有吸引力的方向，但当前叙述中“novelty”和“importance”有过度包装风险。要建立强投稿竞争力，作者需要更明确地区分：哪些是新的科学发现，哪些只是已有 proxy calibration 的机器学习实现。

### Who would be interested in the results, and why

- 叶相古气候研究者会关心是否能扩展目标变量。
- 古气候模型约束研究者会关心是否能得到 SH/ENTHAL 的可用 proxy 估计。
- ML-for-geoscience 读者会关心空间 CV 和物理增强特征是否真正提升 transferability。

### Major strengths

- 文章有明确 gap：传统叶相方法变量有限、线性模型较多。
- 目标变量设置比常规 MAT/MAP 更丰富。
- 讨论中没有回避 WMMT/RH 的失败，这为文章增加可信度。
- 特征重要性结果与 leaf margin/leaf size 的生态生理机制一致。

### Major concerns

1. **创新性需要更精确定位。** 如果核心贡献是“ensemble ML for leaf physiognomy”，需要说明和 DLP 2024、CLAMP 改进、已有 ML proxy calibration 的实质差异。如果核心贡献是“thermodynamic targets”，则应把 SH/ENTHAL 的验证做得更强。
2. **“outstanding scientific importance” 尚未成立。** 当前结果更像领域内有用的方法扩展，而不是会立即改变广泛地球科学读者认知的结论。
3. **SH/ENTHAL 的中等 R² 是否足以支持古气候解释？** R² = 0.329/0.459 有方法意义，但要进入高影响投稿，需要说明这种精度能解决什么具体古气候问题。
4. **缺少案例应用。** 文章没有展示一个有地质意义的 fossil assemblage case study，例如某一时期/地区的重建如何改变已有认识。没有案例会削弱科学重要性。
5. **参考文献支撑需要系统核查。** 文稿中的“first demonstration”“DLP 2024”“speleothem δ¹⁸O reconstruction”等陈述需要补充精确文献支持；ERA5-Land 也应正式引用。

### Technical failings that need to be addressed before the case is established

- 加入系统的 prior-work table：CLAMP、LMA、DLP、已有 ML proxy calibration、本文方法之间的数据、模型、变量、验证方式对比。
- 弱化或证实 “first demonstration”。若不能系统检索证明，改为 “to our knowledge”。
- 增加一个 geologically meaningful demonstration：用某个 fossil flora 展示 MAT/CMMT/SH/ENTHAL 联合重建如何解释环境变化。
- 增加对 `Climate of the Past` 读者的科学问题导向，而不是只报告模型指标。

### Assessment against Nature-style criteria

- **Originality:** 有方法组合创新，但目前区别于已有方法的论证不够强。
- **Scientific importance:** 对专业社区有价值；对广泛读者的 immediate and far-reaching implications 仍不足。
- **Interdisciplinary readership:** 需要更强的 paleoclimate question 或 model-data comparison 才能外溢到更广读者。
- **Technical soundness:** 依赖 Reviewer 1 所列验证补强。
- **Readability:** 结构清楚，但贡献层级需要更尖锐。

### Recommendation posture

**适合先投专业地学/古气候期刊，不宜当前冲 Nature/Nature Geoscience。** 若补强 benchmark、case study 和数据归档，可考虑 `Communications Earth & Environment` 或 `Scientific Reports`；若保持当前方法验证深度，更建议 `Climate of the Past`、`Palaeogeography, Palaeoclimatology, Palaeoecology`、`Paleobiology`。

---

## Reviewer 3 — broad readership and readability foregrounded

### Overall assessment

文稿比一般机器学习方法文更可读，摘要和讨论能解释为什么叶相、温度和湿度-能量变量相关。但对于非专业读者，当前版本仍然过多围绕 R²、模型名和变量缩写展开，缺少一个直观主线：这个方法解决了哪个古气候科学问题？预测 SH/ENTHAL 会让我们对过去气候系统多知道什么？

### Who would be interested in the results, and why

- 非机器学习的古气候读者会关心该工具是否可靠、何时可用、何时不可用。
- 植物功能性状读者会关心 tooth/leaf size 与 climate 的机制一致性。
- 数据科学读者会关心这个案例是否体现了物理约束辅助 ML 的有效性。

### Major strengths

- 摘要结构较完整：背景、gap、方法、结果、边界都有。
- 负结果表达清楚：WMMT/RH 不可靠。
- 图表逻辑较完整，五张图覆盖从输入关联到模型输出和误差。
- Data and Code Availability 已有基本框架。

### Major concerns

1. **标题过长且信息过载。** 现在标题同时包含 ensemble ML、two-stage、temperature-aware、thermodynamic targets，建议缩短并突出核心贡献。
2. **变量缩写密集。** MAT/WMMT/CMMT/GROWSEAS/RH/SH/ENTHAL 应在首次出现后加一个简短 interpretive phrase，例如 “cold-month temperature, a proxy-relevant winter thermal constraint”。
3. **缺少图形化工作流总览。** Nature-style 编辑标准特别重视非专业可读性；建议增加 Fig. 1 或 Extended Data schematic：modern traits → Stage 1 temperature → Stage 2 moisture-energy → fossil predictions → uncertainty。
4. **图件在 Word 中可见，但投稿时应单独提交高分辨率图。** 当前 Word 采用 4 英寸内嵌图适合阅读，但正式投稿建议另外提供 `.tiff/.pdf/.svg`，并保证文字大小、面板标签和色盲友好配色。
5. **Data Availability 仍是占位符。** `https://github.com/[placeholder]` 和 `DOI: [to be assigned]` 在投稿前必须替换为可供审稿人访问的真实链接或 private reviewer link。

### Technical failings that need to be addressed before the case is established

- 增加 schematic figure 或 graphical abstract。
- 将图表说明改为更 self-contained：每张图说明清楚样本量、训练/测试定义、误差指标来源。
- 用一段 “What this enables” 明确 SH/ENTHAL 的科学用途。
- 准备 Supplementary Methods：数据来源、fold design、hyperparameter grid、software versions、reproducibility commands。

### Assessment against Nature-style criteria

- **Originality:** 对专业读者可见；对广泛读者还需要更清楚地说“为什么重要”。
- **Scientific importance:** 目前表述偏方法学，科学问题驱动不足。
- **Interdisciplinary readership:** 有潜力，但需要 schematic 和 case study。
- **Technical soundness:** 取决于数据泄漏和验证问题能否解决。
- **Readability:** 中等偏好；可通过标题、图形摘要和变量解释明显提升。

### Recommendation posture

**投稿前应做一次“读者重构”而不只是语言润色。** 如果目标是 `Climate of the Past`，要强化方法透明和可复现；如果目标是 Nature-family，必须强化跨学科意义、概念图和独立验证。

---

## Cross-review synthesis

### Consensus strengths

- 研究问题有现实价值：叶相古气候重建确实需要非线性建模和更丰富气候变量。
- 两阶段温度增强架构是文稿最有潜力的创新点。
- 文章已经具备基本论文骨架：摘要、方法、结果、讨论、数据可用性、参考文献均已存在。
- 明确报告失败变量 WMMT/RH 是优点，有助于避免过度选择性结论。

### Consensus technical risks

1. **最高优先级：澄清 `Fossil R²`。** 如果没有独立真实古气候值，该指标会被审稿人强烈质疑。
2. **最高优先级：排除数据泄漏。** QuantileTransformer、模型权重优化、Stage 1→Stage 2 预测传递都必须在 fold 内完成。
3. **高优先级：补充基准比较。** 与 CLAMP/LMA/DLP 或简单线性/PLS/Ridge baseline 在同一数据集上比较。
4. **高优先级：外部验证和区域泛化。** Asia-dominant fossil set 需要 leave-region-out 或 continent/block CV。
5. **高优先级：数据和代码可用性不是投稿级。** GitHub/Zenodo 占位符必须替换。

### Where emphasis differs across reviewers

- Reviewer 1 认为当前最大风险是验证流程和性能指标定义。
- Reviewer 2 认为当前最大风险是创新性和科学重要性没有被充分证明。
- Reviewer 3 认为当前最大风险是非专业读者难以理解方法的科学意义。

### Broad-interest / significance readout

当前版本**不建议直接冲 `Nature` 主刊或 `Nature Geoscience`**。理由是：技术有效性尚未完全建立，科学问题导向不够强，跨学科影响还没有通过独立验证或关键案例展示出来。更现实的投稿路线是：

| 优先级 | 期刊/方向 | 建议理由 |
|---|---|---|
| 1 | `Climate of the Past` | 标题页已定位 CP；方法透明、数据可复现、古气候 proxy calibration 与该期刊范围匹配。 |
| 2 | `Palaeogeography, Palaeoclimatology, Palaeoecology` | 适合古生态/古气候方法与 fossil flora 应用。 |
| 3 | `Paleobiology` | 若强化叶形态性状和演化/生态机制解释，可考虑。 |
| 4 | `Geoscientific Model Development` | 若重点转向开源模型框架、代码、benchmark 和 reproducible workflow。 |
| 5 | `Scientific Reports` / `Communications Earth & Environment` | 需先补强独立验证、图形摘要、数据归档和 broader significance；当前不建议贸然投。 |

### Most important issues to resolve before a strong Nature-style case is established

1. **重新定义并解释所有性能指标。** 特别是 `Fossil R²`、CV R²、RMSE/MAE 的样本集、真值来源和计算方式。
2. **补充无泄漏验证。** nested spatial CV + out-of-fold two-stage prediction + independent holdout。
3. **补充直接 benchmark。** 同数据集上比较 CLAMP/LMA/DLP/linear baseline。
4. **增加 case study。** 选择一个化石植物群，展示该方法如何改变对古气候状态的解释。
5. **完善 Data/Code Availability。** 真实 DOI、reviewer access link、README、source data、模型文件、environment file。
6. **修订强表述。** 将 “first demonstration” 等未充分证实的句子改为更审慎版本，除非完成系统文献检索。
7. **投稿文件规范化。** Word 正文可保留小图预览，但正式投稿应另交高分辨率图文件和 source data。

---

## Risk / unsupported claims

- **“first demonstration”**：当前未见系统文献检索支撑；建议改为 “to our knowledge” 或补充系统检索结果。
- **“This adaptive mechanism ensures ... never underperforms baseline”**：该说法只可能在特定 CV 条件下成立，不能保证外部/化石数据表现；建议弱化。
- **“Fossil transfer R²”**：必须说明真实值来源，否则属于高风险指标。
- **Data Availability 占位符**：`GitHub [placeholder]`、`Zenodo DOI [to be assigned]` 投稿前不可保留。
- **ERA5-Land 数据引用**：Data Availability 中提到 ERA5-Land，但参考文献中未见正式引用。
- **73 vs 71 化石样本一致性**：工作区文件名含 `Fossil73`，文稿写 71 fossil assemblages；需确认是否有样本剔除，并在方法中说明。
- **图表源数据**：文稿声称 source data provided，但当前 Word 中不可评估；需准备 supplementary source data。

---

## 最直接的投稿建议

**建议路线：先按 `Climate of the Past` 进行 major technical revision 后投稿。** 当前稿件不宜以 Nature-family 高影响力稿件定位。若要提高档次，优先补验证，不要只继续润色语言。

### 投稿前 10 项必做清单

1. 写清楚 `Fossil R²` 的真值来源。
2. 确认 `QuantileTransformer`、权重优化、两阶段模型均无数据泄漏。
3. 增加 nested spatial CV 或 leave-region-out validation。
4. 与 CLAMP/LMA/DLP 或至少线性 baseline 做同数据集比较。
5. 增加 SH/ENTHAL 的消融实验和 uncertainty intervals。
6. 加一个 fossil case study，把模型结果转化为古气候解释。
7. 增加 workflow schematic figure。
8. 完成 GitHub + Zenodo/Dryad/PANGAEA/Dryad 等 DOI 归档。
9. 补充 source data、README、环境文件、模型权重和复现实验命令。
10. 全文核查引用，补 ERA5-Land、软件包、数据集和所有强 claim 的文献支撑。
