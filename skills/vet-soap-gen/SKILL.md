---
name: vet-soap-gen
description: Automatically aggregate clinical data from previous skill runs and current patient context to generate professional SOAP records, referral reports, or discharge summaries. (vet-soap-gen)
requires:
  ssot:
    - path: meta.status
      freshness: null
  skills: [vet-history]
provides:
  ssot: []
  downstream_hints: []
---

# Veterinary SOAP Generator (/vet-soap-gen)

本技能是整個系統的 **"Administrative Hub"**，負責將臨床數據轉化為正式病歷。

## 🏥 Clinical Workflow

2.  **Aggregate Data**: 
    - 自動掃描 `.vet/current_patient.json` 裡的最新數據。
    - 追蹤本次對話中跑過的技能（如 `/vet-history (Comprehensive veterinary history taking, clinical communication, and logical problem-solving protocols. Use when conducting physical exams, gathering patient histories, or applying the LCPS framework. (vet-history))`, `/vet-lab-cross (Advanced laboratory data interpretation engine using IDEXX standards and BSAVA algorithms.)`, `/vet-pain-score (Professional veterinary pain assessment using FGS, Glasgow, CSU, UNESP, LOAD, and HCPI scales. Supports both acute and chronic pain for dogs and cats. (vet-pain-score))`).
3.  **Select Template**:

    - **SOAP**: [Standard SOAP](assets/templates/standard_soap.md) (日常病歷)。
    - **Referral**: [Referral Report](assets/templates/referral_report.md) (轉診報告)。
    - **Discharge**: [Discharge Summary](assets/templates/discharge_summary.md) (出院摘要)。
3.  **Drafting**:
    - AI 會根據 {{mustache}} 標籤自動填充數據。
    - 針對缺失的區塊，AI 會主動提示醫師補全。
4.  **Finalize**:
    - 輸出完整的 Markdown 格式內容，方便醫師直接複製到醫院管理系統 (PMS)。

## ⚙️ Power Features (gstack Style)

- **Owner-Brief Mode**: 自動將 Assessment 內容轉化為白話版，方便跟家屬對談。
- **Auto-Archive**: 將生成的病歷存檔，並清除 `.vet/current_patient.json` 準備迎接下一個案例。

## 📝 Reference
- [Standard SOAP Template](assets/templates/standard_soap.md)
