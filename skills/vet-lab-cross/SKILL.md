---
name: vet-lab-cross
description: Advanced laboratory data interpretation engine using IDEXX standards and BSAVA algorithms.
---

# 🧪 深度檢驗判讀 (Laboratory Cross-Interpretation)

本技能作為臨床數據的「大腦」，負責將原始數值轉化為具備診斷意義的 Pattern。

## 🏥 臨床工作流 (Workflow)

1.  **Input Data**: 讀取 `.vet/current_patient.json` 裡的 `labs` 數據。若無數據，請引導醫師輸入關鍵數值 (CBC, Bio, UA)。
2.  **Pattern Recognition**: 結合 [idexx_ref.md](references/idexx_ref.md) 與 [bsava_*.md](references/) 進行深度分析：
    - **Erythrocytes**: 執行貧血分類 (Regenerative vs Non-regenerative) 與 RBC Indices 分析。
    - **Leukocytes**: 辨識 Stress, Excitement 與 Inflammatory Leukograms。
    - **Organ Function**: 區分肝臟 Hepatocellular vs Cholestatic Patterns，並評估 4 大肝功能指標。
    - **Renal**: 執行 IRIS 分級與投藥安全性評估。
3.  **Logical Reasoning**: 呼叫 Python 邏輯引擎（如 `calc_renal_staging.py`）進行精密校正。
4.  **Reporting**: 輸出判讀摘要，並詢問是否執行 `/vet-soap-gen` 生成病歷。

## ⚙️ 核心參考
- **IDEXX**: 官方物種正常值範圍。
- **BSAVA**: 第 3-12 章核心病理判讀邏輯。
