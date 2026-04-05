---
name: vet-test-roi
description: 評估與排序檢驗項目的臨床投資報酬率 (ROI)。根據《Veterinary Clinical Pathology: A Case-Based Approach》，給出符合 "Spectrum of Care" 且「寧願多也不要少 (Comprehensive Standard first)」的實證醫學檢驗計畫與防衛性醫療建議。
requires:
  ssot:
    - path: problems
      freshness: 7d
  skills: [vet-history]
provides:
  ssot:
    - path: diagnostic_plan.roi_ranking
  downstream_hints: [vet-soap-gen]
---

# 📊 檢驗效益評估 (Diagnostic ROI & Spectrum of Care)

## Metadata (English)
- **ID**: `vet-test-roi`
- **Focus**: High-Value Care & Diagnostic Triage based on MDB
- **Primary Standard**: "Veterinary Clinical Pathology: A Case-Based Approach", "Choosing Wisely: 2025 Edition (SkeptVet)", WSAVA Spectrum of Care Guidelines, ISCAID Pyoderma, AAHA Oncology, AAFP Hyperthyroidism & Senior Care Guidelines.
- **Anti-Hallucination Mandate**: 必須尊崇教科書的核心哲學：「全面性的最低資料庫 (MDB，包含 CBC, 生化, 尿檢) 是確診前的標準配備」。同時必須遵循 **Choosing Wisely 2025** 的減法原則，主動識別低價值檢查與治療。只有在家長面臨極端限制時才提供降級方案，並強制伴隨醫療免責宣告。

## Workflow (繁體中文)
當獸醫師需要決定下一步該開立什麼檢驗項目，或者遇到家長因為預算考量猶豫不決時，啟動此流程。

### Step 1: 確立黃金標準與低價值項目 (Standard & Low-Value Identification)
- 永遠以「寧願多也不要少」的 MDB 作為推薦起點。
- 同時提醒醫師「哪些是目前實證顯示可以不做」的低價值項目（例如：急性腹瀉的 Metronidazole、無症狀菌尿症的抗生素）。

### Step 2: 執行 ROI 評分腳本 (Run ROI Engine)
- 呼叫內建的 Python 腳本 `scripts/rank_diagnostics.py`。
  ```bash
  python3 skills/vet-test-roi/scripts/rank_diagnostics.py --problem "<主訴>" --constraint "<None|LowBudget|Fractious>"
  ```
- 支援的情境 (Presentations)：
  - `acute_vomiting_diarrhoea` (急性嘔吐下痢 - Choosing Wisely & Case 4/18 實裝)
  - `severe_anaemia_pallor` (嚴重貧血蒼白 - Case 6 實裝)
  - `pu_pd_polyuria_polydipsia` (多渴多尿 - Case 9/12 實裝)
  - `icterus_hepatobiliary` (黃疸肝膽 - Case 5 實裝)
  - `pruritus_skin_lesions` (皮膚搔癢)
  - `skin_mass_nodule` (皮膚腫塊)
  - `feline_weight_loss_polyphagia` (高齡貓體重流失)
  - `acute_collapse_seizures` (休克癲癇 - Case 117 實裝)
  - `cavitary_effusion` (體腔積液 - POCUS 實裝)
  - `mitral_valve_disease_mmvd` (心臟瓣膜病)
  - `osteoarthritis_chronic_pain` (骨關節炎與慢性疼痛)
  - `coagulopathy_dic` (凝血功能與 DIC - Case 10 實裝)
  - `protein_disorders_gammopathy` (蛋白質電泳與漿細胞腫瘤 - Case 13 實裝)
  - `quality_control_artifacts` (檢驗誤差與人工抹片判讀 - Case 72 實裝)

### Step 3: 現實妥協與防衛性宣告 (Step-down & Defensive Communication)
- 若輸入了 `LowBudget` (低預算) 或 `Fractious` (極度不配合)，腳本會給出最低限度的續命妥協方案。
- **強制動作**：必須向家長明確傳達腳本輸出的 `防衛性醫療宣告 (Defensive Rationale)`，並強烈建議獸醫師將免責聲明複製貼上至病歷中。

## ⚙️ Administrative Automation (Admin Mode)

分析完畢後，主動詢問 user：
- "是否執行 `/vet-soap-gen (Automatically aggregate clinical data from previous skill runs and current patient context to generate professional SOAP records, referral reports, or discharge summaries. (vet-soap-gen))` 生成病歷？"