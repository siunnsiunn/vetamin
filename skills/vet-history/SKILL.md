---
name: vet-history
description: Comprehensive veterinary history taking, clinical communication, and logical problem-solving protocols. Use when conducting physical exams, gathering patient histories, or applying the LCPS framework. (vet-history)
requires:
  ssot:
    - path: patient.species
      freshness: null
  skills: [vet-triage]
provides:
  ssot:
    - path: problems
  downstream_hints: [vet-lab-import, vet-lab-cross, vet-soap-gen]
---

# Veterinary History and Clinical Reasoning (/vet-history)

本技能提供結構化的 **clinical data** 蒐集指引，協助醫師與 **owner** 進行有效溝通。

## 🏥 Clinical Workflow

1.  **Check Signalment**: 
    - 檢查 `.vet/current_patient.json` 裡的 **patient** 基本資料 (**signalment**)。
    - 若資料缺失，請詢問：**species**, **breed**, **age**, **sex**, **weight**。
2.  **Structured History (問診)**: 
    - 使用 [comprehensive_history.md](references/comprehensive_history.md) 框架。
    - 運用 "Funnel Sequence" (漏斗式提問)：先問開放式問題，再針對 **symptoms** (如 **lethargy**, **vomiting**, **diarrhea**) 進行細節確認。
3.  **Logical Clinical Problem Solving (LCPS)**:
    - 辨識 **Diagnostic Hooks**：優先處理具有高度特異性的 **problems** (如 **jaundice**, **seizures**)。
    - 定義 **Location & Lesion**：使用 [LCPS_canonical.md](../../references/LCPS_canonical.md) 的 **DAMNIT-V** 邏輯。
4.  **Data Capture**:
    - 蒐集完畢後，將整理好的 **history_summary** 與 **active_problems** 更新至 `.vet/current_patient.json`。

## ⚙️ Administrative Automation (Admin Mode)

蒐集完 **history** 與 **physical exam** 數據後，主動詢問 user：
- "要執行 `/vet-test-roi (評估與排序檢驗項目的臨床投資報酬率 (ROI)。根據《Veterinary Clinical Pathology: A Case-Based Approach》，給出符合 \"Spectrum of Care\" 且「寧願多也不要少 (Comprehensive Standard first)」的實證醫學檢驗計畫與防衛性醫療建議。)` (生成鑑別診斷與檢驗排序) 嗎？"
- "要預覽目前的 **SOAP** 草稿 (執行 `/vet-soap-gen (Automatically aggregate clinical data from previous skill runs and current patient context to generate professional SOAP records, referral reports, or discharge summaries. (vet-soap-gen))`) 嗎？"
- "需要撰寫 **discharge_summary** (出院摘要範本) 嗎？"

## 📝 Key Reference Files
- [references/comprehensive_history.md](references/comprehensive_history.md)
- [../../references/LCPS_canonical.md](../../references/LCPS_canonical.md)
- [references/emergency_triage_history.md](references/emergency_triage_history.md)
- [assets/templates/discharge_summary.md](assets/templates/discharge_summary.md)
