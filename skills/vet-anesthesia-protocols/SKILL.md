---
name: vet-anesthesia-protocols
description: Generate tailored anesthesia plans and dosage calculations strictly bound to AAHA/WSAVA standards.
---

# 💉 臨床麻醉協定 (Anesthesia Protocols)

## Metadata (English)
- **ID**: `vet-anesthesia-protocols`
- **Focus**: Perioperative Anesthesia & Analgesia Planning
- **Primary Standard**: AAHA Anesthesia Guidelines for Dogs and Cats (2020), WSAVA Global Pain Council Guidelines (2022)
- **Anti-Hallucination Mandate**: DO NOT suggest drug dosages or protocols from generic AI knowledge. ALL dosages MUST be derived from recognized reference texts (e.g., Plumb's, BSAVA Formulary) or explicitly calculated via internal scripts. If a specific patient condition (e.g., severe hepatic failure) lacks a clear protocol in provided references, refuse to guess and recommend consulting a veterinary anesthesiologist.

## Workflow (繁體中文)
### 1. 風險評估 (Context & Risk Assessment)
- 讀取 `.vet/current_patient.json` 裡的 `patient` (Weight, Age, Breed) 與 `labs` (Renal/Liver status)。
- 自動判定 **ASA Physical Status Classification** (ASA I-V)。
### 2. 協定設計 (Protocol Design - AAHA Standard)
- **Pre-medication**: 根據病史與 ASA 等級，嚴格參照 AAHA 指引建議鎮靜與止痛組合。
- **Induction & Maintenance**: 提供插管、誘導及氣麻或 TIVA 建議。
### 3. 劑量計算 (Dose Calculation)
- 呼叫 `scripts/dose_calculator.py` 輸出精確的劑量 (mg 與 mL)，嚴禁使用 AI 猜測的劑量。
### 4. 緊急預案 (Emergency Response)
- 針對低血壓、心跳過緩等併發症，提供基於 RECOVER 倡議的標準急救流程。

## Medical Logic (Medical Chinglish)
- **Hepatic/Renal Insufficiency**: Strictly avoid or heavily reduce dose of alpha-2 agonists (e.g., Dexmedetomidine) and NSAIDs. Prefer opioids or local blocks.
- **Brachycephalic Breeds**: High risk for airway obstruction. Pre-oxygenation and rapid intubation protocols are mandatory.
