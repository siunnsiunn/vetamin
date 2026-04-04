---
type: clinical_algorithm
module: vet-lab-cross
topic: lab_patterns_and_staging
---
# Veterinary Lab Cross-Interpretation & Staging Patterns

這份文件彙整了跨系統的檢驗數據判讀模式 (Cross-Interpretation) 與國際公認的疾病分級指南 (如 IRIS 2023)，協助 Vetamin Agent 進行疾病分期與預後評估。

---

## 1. IRIS Chronic Kidney Disease (CKD) Staging (2023 Modified)

國際腎臟權益學會 (IRIS) 的慢性腎病分期，必須在病患處於 **Hydrated and Stable (水合良好且穩定)** 的狀態下，且經過至少兩次的空腹血液檢查才能確診分期。

### 1.1 Primary Staging (依據 CREA 與 SDMA)
當 CREA 與 SDMA 的分期結果出現分歧時，**SDMA 若持續超標，應以此作為更高的分期標準 (SDMA Overrules)**，因為它對 GFR 的下降更為敏感且不受肌肉量影響。

| Stage | Dog CREA (µmol/l) | Dog SDMA (µg/dl) | Cat CREA (µmol/l) | Cat SDMA (µg/dl) | Clinical Characteristics |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Stage 1** | < 125 (< 1.4 mg/dl) | < 18 | < 140 (< 1.6 mg/dl) | < 18 | Normal CREA/SDMA，但有其他異常 (如 inadequate concentration, renal proteinuria, abnormal imaging) |
| **Stage 2** | 125 - 250 (1.4 - 2.8) | 18 - 35 | 140 - 250 (1.6 - 2.8) | 18 - 25 | Mild renal azotaemia。臨床症狀通常 mild or absent。 |
| **Stage 3** | 251 - 440 (2.9 - 5.0) | 36 - 54 | 251 - 440 (2.9 - 5.0) | 26 - 38 | Moderate renal azotaemia。開始出現明顯 systemic signs。 |
| **Stage 4** | > 440 (> 5.0) | > 54 | > 440 (> 5.0) | > 38 | Severe renal azotaemia。極高風險發生 uraemic crises。 |

*Breed Exceptions*: 健康的 Birman cats 與 Greyhounds 的基礎 SDMA 與 CREA 可能本來就偏高，需謹慎判讀。

### 1.2 Substaging by Proteinuria (UPC 尿蛋白/肌酸酐比值)
必須排除 pre-renal (如 dysproteinemias) 與 post-renal (如 UTI, haemorrhage) 因素。
- **Non-proteinuric**: UPC < 0.2 (Dog & Cat)
- **Borderline proteinuric**: UPC 0.2 - 0.5 (Dog) / 0.2 - 0.4 (Cat)
- **Proteinuric**: UPC > 0.5 (Dog) / > 0.4 (Cat)

### 1.3 Substaging by Blood Pressure (Systolic Blood Pressure, SBP)
測量必須多次並給予病患 acclimatization (適應時間) 以避免白袍效應。
- **Normotensive (Minimal risk)**: SBP < 140 mmHg
- **Prehypertensive (Low risk)**: SBP 140 - 159 mmHg
- **Hypertensive (Moderate risk)**: SBP 160 - 179 mmHg
- **Severely hypertensive (High risk)**: SBP ≥ 180 mmHg

---

## 2. Liver & NSAID Monitoring Patterns (AAHA / AAFP Guidelines)

### 2.1 NSAID Hepatotoxicity / Reactive Hepatopathy
- **Pattern**: 服用 NSAIDs 期間，發現 **ALT / AST > 2-3x Upper Normal Limit (UNL)**。
- **Action**: **Red Flag (紅色警戒)**。必須立即停止 NSAID therapy 並啟動 washout period。
- **Follow-up**: 檢查 Bile acids, Albumin, Bilirubin 以評估是否有實質 Liver function decline。

### 2.2 Feline Cholangitis / Hepatic Lipidosis Complex
- **Pattern**: **ALKP 顯著 increased + GGT 正常或輕微 increased + Hyperbilirubinaemia** (在貓)。
- **Clinical Implication**: 強烈暗示 Hepatic Lipidosis (脂肪肝)，通常繼發於長期的 Anorexia。若 GGT 也顯著上升，則需考慮 concurrent Cholangitis (膽管炎) 或 Extrahepatic bile duct obstruction。

### 2.3 Canine Chronic Hepatitis (CH) & Copper-Associated Hepatitis (CuCH) (ACVIM Consensus)
- **Early Detection**: 持續 (> 2 個月) 的 **ALT 顯著 increased** 是早期 CH 的最佳 screening test。肝功能指標 (BUN, ALB, CHOL, TSBA, Ammonia) 在初期通常正常，直到後期才會異常。
- **Copper-Associated CH (CuCH)**:
  - **Breed Predisposition**: Bedlington Terriers (COMMD1 mutation), Labrador Retrievers, Doberman Pinschers, Dalmatians.
  - **Diagnostic Hook**: 必須透過肝臟 biopsy 且定量銅濃度 (**> 1000 µg/g dry weight**) 才能確診。
  - **Treatment Pattern**: D-penicillamine (chelator) + Lifelong Cu-restricted diet (< 0.12 mg/100 kcal) + Antioxidants (SAMe, Vitamin E)。**注意：絕對不可同時給予 Zinc (會互相拮抗)**。
- **Poor Prognostic Indicators in CH**: 
  - Hyperbilirubinaemia (黃疸)
  - Prolonged PT / aPTT
  - Hypoalbuminaemia (低白蛋白)
  - Ascites (腹水) 或 acquired portosystemic shunts (APSS) 的出現。

---

## 3. Advanced Hepatobiliary Patterns (Ettinger's 9th Ed)

### 3.1 Hepatic Encephalopathy (HE) Triggers & Management
- **Clinical Hooks**: ptyalism (貓特有, 75%), ataxia, head pressing, seizures.
- **Underlying Triggers**: GI bleeding, hypokalaemia, alkalosis, infections, high-protein diet. 
- **Diagnostic Caveat**: **Blood ammonia (血氨) 的絕對數值與 HE 的嚴重程度「沒有」絕對的正相關**。即使血氨正常，也不能完全排除 HE (特別是在有門脈高壓的病例)。
- **Treatment Pattern**: 
  - **Lactulose**: 改變腸道 pH 值 (trap ammonia as NH4+)，縮短腸道排空時間。
  - **Antibiotics (Metronidazole / Amoxicillin)**: 減少產氨細菌。
  - **Diet**: 限制蛋白質攝取 (但避免過度限制導致肌肉流失，因為 skeletal muscle 含有 glutamine synthetase，是清除體循環血氨的重要緩衝器官)。
  - **Seizure Control**: Levetiracetam 或 Propofol。**絕對禁用 Benzodiazepines (Diazepam)**，因為會與內生性受體結合惡化 HE。

### 3.2 Hepatobiliary Neoplasia
- **Hepatocellular Carcinoma (HCC)**: 
  - 狗最常見的原發性肝腫瘤 (>50%)，通常發生在老年犬 (>10歲)。
  - **Massive HCC** (佔 53-83%) 預後極佳！若能成功手術切除 (Liver lobectomy)，轉移率僅 0-13%，存活期可長達數年。
  - **Laboratory**: 可能出現 Paraneoplastic hypoglycaemia (副腫瘤性低血糖) 與 Thrombocytosis (血小板增多)。
- **Biliary Tract Tumours**:
  - 貓最常見的原發性肝腫瘤為 Biliary cystadenoma (良性) 與 Cholangiocarcinoma (惡性)。
  - **Cholangiocarcinoma**: 具高度侵略性，狗的轉移率高達 90% (主要轉移至淋巴結與肺臟)，預後極差。通常伴隨顯著的 Icterus 與 Cholestasis 酵素異常。

---

## 4. Cardiac & Respiratory Screening Patterns

### 4.1 Occult Heart Disease Screening (ISFM Guidelines)
- **Pattern**: 聽診有 Murmur (心雜音) 或 Gallop rhythm (奔馬律)，抽血 **NT-proBNP 顯著 increased**。
- **Action**: **Red Flag**。代表 myocardium (心肌) 正承受極大的 stretch stress，有極高的 Congestive Heart Failure (CHF) 風險。
- **Follow-up**: 必須立刻安排 Echocardiography (心臟超音波) 與 Thoracic Radiography (胸腔X光) 確認是否有 pulmonary oedema (肺水腫) 或 pleural effusion (胸水)。

### 4.2 Feline Asthma vs. Cardiac Cough
- **Pattern**: 貓咪出現 Chronic cough (慢性咳嗽) 伴隨 **Eosinophilia**。
- **Clinical Implication**: 貓咪的咳嗽**極罕見**是因為 heart failure 引起的。若伴隨 Eosinophilia，高度懷疑是 Feline Asthma (貓氣喘) 或 Heartworm disease (心絲蟲)。