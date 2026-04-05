---
name: vet-anesthesia-protocols
description: Generate tailored anesthesia plans and dosage calculations strictly bound to AAHA/WSAVA standards. Provide a printable OR checklist.
requires:
  ssot:
    - path: patient.weight
      freshness: 24h
    - path: vitals
      freshness: 4h
  skills: []
provides:
  ssot:
    - path: anesthesia
  downstream_hints: [vet-soap-gen]
---

# 💉 臨床麻醉協定 (Anesthesia Protocols)

## Metadata (English)
- **ID**: `vet-anesthesia-protocols`
- **Focus**: Perioperative Anesthesia & Analgesia Planning
- **Primary Standard**: AAHA Anesthesia Guidelines for Dogs and Cats (2020), WSAVA Global Pain Council Guidelines (2022), ACVAA Monitoring Standards (2025).
- **Anti-Hallucination Mandate**: DO NOT suggest drug dosages or protocols from generic AI knowledge. ALL dosages MUST be derived from recognized reference texts or calculated via internal scripts. You MUST run the python script `scripts/dose_calculator.py` for accurate doses. If a specific patient condition lacks a clear protocol, refuse to guess and recommend consulting a veterinary anesthesiologist.

## Workflow (繁體中文)
這是一份給獸醫師帶入開刀房 (OR) 使用的列印檢查表。絕對不能算錯藥物劑量。

### Step 1: 風險評估 (Context & Risk Assessment)
- 讀取 `.vet/current_patient.json` 裡的病患資訊 (Weight, Age, Breed) 與檢驗數據 (Renal/Liver status)。
- 若無指定，預設判定為 **ASA II**。
- 若缺乏必要資訊 (種別、體重、手術種類)，可先詢問飼主/醫師，或使用已知資訊生成。

### Step 2: 劑量計算 (Dose Calculation)
- **強制規定**：嚴禁使用 AI 猜測劑量。你必須呼叫 Python 腳本來取得精準的藥物劑量與抽藥體積 (mL)：
  ```bash
  python3 skills/vet-anesthesia-protocols/scripts/dose_calculator.py --weight <kg> --species <cat|dog> --asa <1-5> --format json
  ```
- 請將腳本回傳的結果直接填入下方的麻醉表單中。

### Step 3: 協定設計與臨床指引 (Protocol Design & Clinical Context)
- 根據病史與 ASA 等級，嚴格參照 AAHA/WSAVA 指引給予鎮靜與止痛建議。
- 在 Protocol 內加上指引來源 (如 "AAFP 2020", "ACVAA 2025")。

### Step 4: 生成麻醉計畫表 (Generate Protocol)
- **必須使用以下 ASCII 模板**，將數據填入對應欄位，產生一份可以直接列印的 Check List。

## ⚙️ Administrative Automation (Admin Mode)
- "是否執行 `/vet-soap-gen (Automatically aggregate clinical data from previous skill runs and current patient context to generate professional SOAP records, referral reports, or discharge summaries. (vet-soap-gen))` 生成病歷？"

## Protocol Template (列印模板)
請精確複製以下排版格式，包含打勾框 `□`，供獸醫師列印使用：

```text
═══════════════════════════════════════════════
  麻醉計畫 Anesthesia Protocol
═══════════════════════════════════════════════

📋 Patient Information
───────────────────────────────────────────────
Species/Breed:
Age:          Sex:          Weight:     kg
Procedure:
ASA Status:
Comorbidities:
Date:                       Anesthetist:

═══════════════════════════════════════════════

1️⃣ PREANESTHETIC CHECKLIST
───────────────────────────────────────────────
□ Physical exam completed
□ Bloodwork reviewed (CBC, biochem, ± coag)
□ Fasting confirmed: ____ hours (food) / ____ hours (water)
□ IV catheter placed: ____ G, site: ________
□ Fluid type: ____________  Rate: ____ mL/h
□ Emergency drugs calculated (see Section 7)
□ Monitoring equipment checked
□ [Add case-specific items]

2️⃣ PREMEDICATION
───────────────────────────────────────────────
Time: ____    Route: ____

Drug                  Dose        Volume      ✓
─────────────────────────────────────────────
[Drug 1]              ___ mg      ___ mL      □
[Drug 2]              ___ mg      ___ mL      □
[Drug 3 if needed]    ___ mg      ___ mL      □

Wait ____ min before induction
Notes: [clinical rationale for drug selection]

3️⃣ INDUCTION
───────────────────────────────────────────────
Drug                  Dose        Volume      ✓
─────────────────────────────────────────────
[Induction agent]     ___ mg      ___ mL      □
± [Co-induction]      ___ mg      ___ mL      □

□ Preoxygenate 3-5 min before induction
□ Titrate to effect (give ¼ dose increments q30s)
□ Intubate: ETT size ____ (have ±0.5 ready)
□ Cuff check
□ Connect to breathing circuit: □ NRC / □ RC
□ Connect capnograph + SpO2

4️⃣ MAINTENANCE
───────────────────────────────────────────────
□ Inhalant: □ Isoflurane / □ Sevoflurane
  Target vaporizer: ____% (adjust to effect)

CRI (if applicable):
Drug                  Rate                    ✓
─────────────────────────────────────────────
[CRI drug]            ___ µg/kg/min           □

5️⃣ LOCAL / REGIONAL ANALGESIA
───────────────────────────────────────────────
Block type: ________________
Drug                  Dose        Volume      ✓
─────────────────────────────────────────────
[Local anesthetic]    ___ mg      ___ mL      □

Notes: [technique, landmarks, timing]

6️⃣ MONITORING PLAN (per ACVAA 2025)
───────────────────────────────────────────────
Parameter         Frequency    Target Range
─────────────────────────────────────────────
HR                q5 min       ___-___ bpm
BP (MAP)          q5 min       60-100 mmHg
SpO2              continuous   ≥ 95%
ETCO2             continuous   35-55 mmHg
Temperature       q15 min      ≥ 37.8°C
ECG               continuous   Normal sinus
Reflexes          q5 min       [specify]
□ Dedicated anesthetist assigned
□ Anesthesia record prepared (record q5 min)

7️⃣ EMERGENCY DRUGS (pre-calculated)
───────────────────────────────────────────────
Drug              Dose         Volume     Route
─────────────────────────────────────────────
Atropine          ___ mg       ___ mL     IV
Glycopyrrolate    ___ mg       ___ mL     IV/IM
Epinephrine       ___ mg       ___ mL     IV
[Species-specific emergency drugs]

Crystalloid bolus: ___ mL (___mL/kg)
□ Drawn up and labeled before induction

8️⃣ RECOVERY
───────────────────────────────────────────────
□ Continue SpO2 + ETCO2 until extubation
□ Extubate when swallow reflex returns
□ Continue temperature monitoring q30 min
□ Supplemental O2 available
□ Pain assessment: ____ min post-extubation
□ Reversal agents (if needed):
  [Drug]            ___ mg       ___ mL     □

Recovery analgesia:
Drug              Dose         Route       Timing
─────────────────────────────────────────────
[Analgesic]       ___ mg       ___         q___h

9️⃣ CASE-SPECIFIC NOTES
───────────────────────────────────────────────
[Comorbidity-driven considerations, procedure-
 specific tips, guideline citations]
═══════════════════════════════════════════════
```

## Medical Logic (Clinical Decision Rules - Medical Chinglish)

當從腳本抓取劑量並組合計畫時，必須遵守以下臨床禁忌與防呆原則：

### Comorbidity-Driven Adjustments (共病調整)
- **HCM (cats)**: 絕對避免使用 Acepromazine (Vasodilation 會惡化 outflow obstruction)。優先選擇 Opioid + Midazolam，或 low-dose Dexmedetomidine。備妥 Esmolol。避免 aggressive fluid loading。
- **Renal/Hepatic Insufficiency**: 嚴格避免或大幅降低 Alpha-2 agonists (e.g., Dexmedetomidine) 與 NSAIDs 劑量。Prefer opioid-heavy protocols 或 local blocks。
- **Hyperthyroidism (cats)**: 避免 Ketamine (具 sympathomimetic 效果)。Prefer Alfaxalone or Propofol induction。
- **Brachycephalic (短吻犬)**: 極高氣道阻塞風險。必須 aggressive preoxygenation。準備多個 size 的 ETT。考慮 shorter-acting agents。延遲 extubation 直到出現 strong swallow reflex。
- **Geriatric (>8 yr dog, >10 yr cat)**: 減少劑量 25-50%。需要 longer monitoring 與 aggressive warming。
- **Pediatric (<6 mo)**: 極易發生 Hypoglycemia，必須監控 BG。藥物 volume 極小，需精確抽取。肝臟代謝尚未發育完全。

### Procedure-Driven Additions (手術特定需求)
- **Dental**: 必須加入 dental nerve blocks (infraorbital, inferior alveolar, mental)。若無 renal contraindication，確認有 NSAIDs。
- **Orthopedic**: Aggressive multimodal analgesia。強烈建議 epidural 或 regional blocks。intraop 應考慮 CRI。
- **Soft tissue / abdominal**: 考慮 intraperitoneal splash block (使用 local anesthetic)。
- **Ophthalmic**: 避免 Ketamine (會增加 IOP)。確保穩定的麻醉深度。

### ASA Status Adjustments (ASA 等級調整)
- **ASA I-II**: Standard protocols。ACVAA 2025 minimum monitoring。
- **ASA III**: 減少藥物劑量。考慮 arterial line / invasive monitoring。提前抽好 vasopressors。
- **ASA IV-V**: 使用 minimal sedation doses。優先考慮 Opioid + Benzodiazepine。Maximum monitoring，必須 ICU recovery。