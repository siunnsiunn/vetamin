---
name: vet-dm-manager
description: Feline and Canine Diabetes Mellitus Management
requires:
  ssot:
    - path: labs.blood.glucose
      freshness: 1d
    - path: management.diabetes
      freshness: 30d
  skills: [vet-lab-cross]
provides:
  ssot:
    - path: management.diabetes.calculated_dose_iu
  downstream_hints: [vet-soap-gen]
---

# Skill: vet-dm-manager
## Metadata (English)
- **ID**: `vet-dm-manager`
- **Focus**: Feline and Canine Diabetes Mellitus Management
- **Primary Standard**: iCatCare 2025 (Feline), FECAVA 2024 (ALIVE), Ettinger's 9th Ed
- **Actions**: Insulin dosage calculation, U-100 to U-300 transition, DKA bridging

## Workflow (繁體中文)
### 1. 診斷與臨床評估 (ALIVE DCS & iCatCare 2025)
- 呼叫 `scripts/dcs_evaluator.py` 根據四大臨床指標（精神、體重、飲水、尿量）進行評分。
- 分數 $\ge$ 4 分需高度警惕，並評估是否發生 **血糖不穩定 (Brittle State)** 或併發症。
- 導入 **2025 iCatCare** 安全機制：血糖低於 **72 mg/dL (4 mmol/L)** 即視為劑量過高，必須立即減量。
- 捨棄過時的 Somogyi 術語，改採現代「血糖不穩定性」評估。

### 2. 起始與調整劑量 (Dose Adjustment)
- 呼叫 `scripts/dm_calculator.py` 根據體重、物種與 **iCatCare 2025** 扣除規則獲取建議量。
- **低血糖減量**: 若發生低血糖事件，建議立即減量 25-50% 或調降 0.5 - 1.0 IU。
- **穩定觀察期**: 調整劑量後，必須維持固定劑量 **至少 5-7 天**，禁止 Stop Chasing Numbers。

### 3. 藥物轉換 (Insulin Transition)
- 特別支援 **Lantus (U-100)** 轉換為 **Toujeo (U-300)** 的安全協議。

### 4. 數據回寫 (SSOT Sync)
- 腳本將自動更新 `~/.vet/current_patient.json` 中的 `management.diabetes` 區塊。

## ⚙️ Administrative Automation (Admin Mode)
- "是否執行 `/vet-soap-gen (Automatically aggregate clinical data from previous skill runs and current patient context to generate professional SOAP records, referral reports, or discharge summaries. (vet-soap-gen))` 生成病歷？"

## Medical Logic (Medical Chinglish)
- **Nadir Control**: Target 80 - 150 mg/dL (4.4 - 8.3 mmol/L).
- **Hypoglycemia Safety**: < 72 mg/dL is the red line. If < 60 mg/dL, stop and restart with 50% dose.
- **Brittle State**: Defined by high glycemic variability due to over-dosage or frequent titration.
- **Toujeo (U-300)**: Enhanced depot stability; use 1-unit SoloStar Pen (1 unit = 1 unit efficacy).
