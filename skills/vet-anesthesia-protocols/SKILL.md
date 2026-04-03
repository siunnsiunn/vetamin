---
name: vet-anesthesia-protocols
description: Generate tailored anesthesia plans and dosage calculations based on patient context.
---

# 💉 臨床麻醉協定 (Anesthesia Protocols)

本技能用於產出安全且結構化的麻醉計畫，降低周手術期風險。

## 🏥 臨床工作流 (Workflow)

1.  **Context Check**: 讀取 `.vet/current_patient.json` 裡的 `patient` (Weight) 與 `labs` (Renal/Liver status)。
2.  **Risk Assessment**: 自動判定 **ASA Physical Status Classification** (ASA 1-5)。
3.  **Protocol Design**:
    - **Pre-medication**: 根據品種（如短吻犬）與病史建議鎮靜與止痛組合。
    - **Induction**: 建議插管與誘導藥物。
    - **Maintenance**: 提供氣麻或全靜脈麻醉 (TIVA) 計畫。
4.  **Dose Calculation**: 呼叫 `scripts/dose_calculator.py` 輸出精確 mL 數。

## ⚙️ 核心邏輯
- 針對 **Renal/Hepatic Insufficiency** 的病人建議藥物減量或避開特定藥物（如 Dexmedetomidine）。
- 提供應對低血壓或心律不整的緊急預案。
