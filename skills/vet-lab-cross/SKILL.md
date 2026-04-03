---
name: vet-lab-cross
description: Cross-analyze blood work, biochemistry, and urinalysis. Identify patterns (e.g., renal vs. pre-renal) and monitor drug safety (e.g., NSAID red flags). (vet-lab-cross)
---

# Veterinary Lab Cross-Interpretation Tool (/vet-lab-cross)

本技能協助醫師進行實驗室數據的 **cross-interpretation**，尋找隱藏的 **clinical patterns**。

## 🏥 Clinical Workflow

1.  **Input Data**: 
    - 讀取 `.vet/current_patient.json` 裡的 `labs` 區塊。
    - 若無資料，請引導醫師輸入關鍵數值：**CBC (HCT, WBC)**, **Bio (CREA, BUN, ALT, ALKP, ALB)**, **UA (USG, Protein)**。
2.  **Pattern Recognition & Reasoning**: 
    - AI 會根據 [lab_patterns.md](references/lab_patterns.md), **IDEXX 標準** ([idexx_ref.md](references/idexx_ref.md)), 以及 **BSAVA 全書專家標準 (Ch 3-12)** 進行深度分析：
        - **Electrolytes**: 計算 Na/K Ratio (Addison risk) 與 Corrected Calcium (HOGS IN YARD) ([bsava_electrolytes.md](references/bsava_electrolytes.md))。
        - **Endocrine**: 判讀甲狀腺功能與腎上腺測試 (LDDST/ACTH stim) 組合 ([bsava_endocrine.md](references/bsava_endocrine.md))。
        - **GI/Urinary**: 分析 B12/Folate 定位與 IRIS 進階腎病分級。
        - **Liver/Pancreas**: 區分酵素組合模式與 Spec fPL/cPL 判讀。
        - **Haematology**: 執行全方位的貧血與白血球相解析。
3.  **Recommendations**:
    - 提供 **Next Diagnostic Steps** (例如：掃心超、驗 UPC、做膽汁酸測試)。

## ⚙️ Administrative Features

- "要將解析結果存入 **patient record** (執行 **update-labs**) 嗎？"
- "需要生成一份 **lab-summary** (給飼主看的檢驗報告白話版) 嗎？"

## 📝 Reference
- [Lab Patterns & Thresholds](references/lab_patterns.md)
