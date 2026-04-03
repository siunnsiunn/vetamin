---
name: vet-triage
description: Triage and stabilization guidelines for veterinary emergencies (Respiratory, Seizures, Bleeding, Cardiovascular, and Toxicology). Use when a patient is in a crisis state to determine urgency and provide immediate stabilization steps. (vet-triage)
---

# Veterinary Triage and Urgent Care (/vet-triage)

這是一個專門處理 **patient** 急診與 **triage** 的技能。請根據以下流程進行 **stabilization**：

## 🏥 Clinical Workflow

1.  **Check Context**: 
    - 首先檢查 `.vet/current_patient.json` 裡的 **patient weight** 與 **vitals**。
    - 如果沒有資料，請主動詢問 user: "請問 **patient** 的 **weight** 與目前的 **vitals** (HR, RR, T, BP, MM, CRT) 是多少？"
2.  **Determine Triage Color**: 
    - 根據 [triage_guidelines.md](references/triage_guidelines.md) 分級 (Red, Orange, Yellow, Green)。
3.  **ABCDEs & Stabilization**:
    - **Respiratory Distress**: 參考 [stabilization_protocols.md#1-acute-respiratory-distress](references/stabilization_protocols.md#1-acute-respiratory-distress)。
    - **Seizures**: 參考 [stabilization_protocols.md#2-seizures-and-cluster-seizures](references/stabilization_protocols.md#2-seizures-and-cluster-seizures)。
    - **Acute Bleeding**: 參考 [stabilization_protocols.md#3-acute-bleeding](references/stabilization_protocols.md#3-acute-bleeding)。
    - **Cardiovascular**: 參考 [stabilization_protocols.md#4-cardiovascular-stabilization](references/stabilization_protocols.md#4-cardiovascular-stabilization)。
4.  **Toxicology**:
    - 如果懷疑 **toxin ingestion**，查閱 [toxicology_quick_ref.md](references/toxicology_quick_ref.md) 進行 **decontamination**。

## ⚙️ Administrative Automation (Admin Mode)

當 **patient** 穩定後，請主動詢問 user：
- "需要為您 **calculate-doses** (根據 **weight** 計算急救藥物劑量) 嗎？"
- "要執行 **gen-soap** (生成初步的 SOAP 紀錄) 嗎？"
- "是否 **handover** 到 `/vet-history` 進行更深度的病史追蹤？"

## 📝 Key Reference Files
- [references/triage_guidelines.md](references/triage_guidelines.md)
- [references/stabilization_protocols.md](references/stabilization_protocols.md)
- [references/toxicology_quick_ref.md](references/toxicology_quick_ref.md)
