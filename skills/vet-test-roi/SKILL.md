---
name: vet-test-roi
description: 評估與排序檢驗項目的臨床投資報酬率 (ROI)。根據《Veterinary Clinical Pathology: A Case-Based Approach》，給出符合 "Spectrum of Care" 且「寧願多也不要少 (Comprehensive Standard first)」的實證醫學檢驗計畫與防衛性醫療建議。
---

# 📊 檢驗效益評估 (Diagnostic ROI & Spectrum of Care)

## Metadata (English)
- **ID**: `vet-test-roi`
- **Focus**: High-Value Care & Diagnostic Triage based on MDB
- **Primary Standard**: "Veterinary Clinical Pathology: A Case-Based Approach", WSAVA Spectrum of Care Guidelines.
- **Anti-Hallucination Mandate**: 必須尊崇教科書的核心哲學：「全面性的最低資料庫 (MDB，包含 CBC, 生化, 尿檢) 是確診前的標準配備」。只有在家長面臨極端預算限制或動物極度不配合時，才提供降級方案 (Step-down compromise)，並且必須伴隨強烈的醫療免責宣告。

## Workflow (繁體中文)
當獸醫師需要決定下一步該開立什麼檢驗項目，或者遇到家長因為預算考量猶豫不決時，啟動此流程。

### Step 1: 確立黃金標準 (Establish the Comprehensive Standard)
- 永遠以「寧願多也不要少」的 MDB 作為推薦起點。
- 說明為什麼漏掉這些檢查（例如：單純嘔吐可能隱藏了致命的 Addison's Disease 或 腎衰竭，如教科書 Case 3, Case 116 所示）是極度危險的。

### Step 2: 執行 ROI 評分腳本 (Run ROI Engine)
- 呼叫內建的 Python 腳本 `scripts/rank_diagnostics.py`。
  ```bash
  python3 skills/vet-test-roi/scripts/rank_diagnostics.py --problem "<主訴>" --constraint "<None|LowBudget|Fractious>"
  ```
- 支援的情境 (Presentations)：
  - `acute_vomiting_diarrhoea` (急性嘔吐與下痢)
  - `severe_anaemia_pallor` (嚴重貧血與蒼白)
  - `pu_pd_polyuria_polydipsia` (多渴多尿)
  - `icterus_hepatobiliary` (黃疸與肝膽異常)

### Step 3: 現實妥協與防衛性宣告 (Step-down & Defensive Communication)
- 若輸入了 `LowBudget` (低預算) 或 `Fractious` (極度不配合)，腳本會給出最低限度的續命妥協方案。
- **強制動作**：必須向家長明確傳達腳本輸出的 `防衛性醫療宣告 (Defensive Rationale)`，並強烈建議獸醫師將免責聲明複製貼上至病歷中。