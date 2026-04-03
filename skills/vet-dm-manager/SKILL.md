# Skill: vet-dm-manager
## Metadata (English)
- **ID**: `vet-dm-manager`
- **Focus**: Feline and Canine Diabetes Mellitus Management
- **Standard**: iCatCare 2025, FECAVA 2024 (ALIVE), Ettinger's 9th Ed
- **Actions**: Insulin dosage calculation, U-100 to U-300 transition, DKA bridging

## Workflow (繁體中文)
### 1. 診斷校準 (Diagnosis)
- 使用 `/vet-dm-manager` 根據 ALIVE 共識判定貓 (>270 mg/dL) 或狗 (>200 mg/dL) 的診斷。
### 2. 起始劑量 (Initial Dose)
- 呼叫 `scripts/dm_calculator.py` 根據體重與物種獲取建議量。
### 3. 藥物轉換 (Insulin Transition)
- 特別支援 **Lantus (U-100)** 轉換為 **Toujeo (U-300)** 的安全協議。
### 4. 數據回寫 (SSOT Sync)
- 腳本將自動更新 `~/.vet/current_patient.json` 中的 `management.diabetes` 區塊。

## Medical Logic (Medical Chinglish)
- **Nadir Control**: Target 80 - 150 mg/dL (4.4 - 8.3 mmol/L).
- **Hypoglycemia Safety**: < 72 mg/dL is the red line. If < 60 mg/dL, stop and restart with 50% dose.
- **Brittle State**: Defined by high glycemic variability due to over-dosage or frequent titration.
- **Toujeo (U-300)**: Enhanced depot stability; use 1-unit SoloStar Pen (1 unit = 1 unit efficacy).
