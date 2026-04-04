---
type: clinical_algorithm
module: vet-lab-cross
topic: clinical_reasoning_framework
---
# Logical Clinical Problem-Solving (LCPS) Framework

這套框架改編自《Clinical Reasoning in Veterinary Practice: Problem Solved!》，是 Vetamin AI 代理人 (Agent) 進行疾病推論與生成 SOAP 報告的**核心決策樹 (Decision Tree)**。

在面對複雜的病患數據時，必須嚴格遵守此「四階段」推論邏輯。

---

## Stage 1: Problem List & Prioritisation (建立與排定問題清單)

將家長主訴與初步檢查結果轉化為明確的問題清單。優先處理具有**高特異性 (High Specificity)** 的「Diagnostic Hook (硬指標)」，忽略或延後處理「背景噪音 (Soft findings)」。

### 優先級分類 (Prioritisation)
- **High Priority (Diagnostic Hooks / 硬指標)**:
  - 這些症狀通常直接指向特定的 body system 或 disease process。
  - **例如**: Vomiting (嘔吐), PU/PD (多渴多尿), Seizures (癲癇), Icterus (黃疸), Bleeding (出血), Dyspnoea (呼吸困難), Haematuria (血尿)。
- **Low Priority (Background Noise / 軟指標)**:
  - 這些症狀特異性極低，可能出現在任何系統性疾病中。可以輔助判斷嚴重程度，但不應作為推論的起點。
  - **例如**: Anorexia (食慾不振), Depression (精神沉鬱), Lethargy (嗜睡), Weight loss (體重減輕)。

---

## Stage 2: Define & Refine the System (界定與細化受累系統)

對於每一個 Diagnostic Hook，必須回答兩個核心問題：

### Question A: Define the System (是哪個系統導致了這個異常？)
- 透過臨床症狀的特徵 (Characteristics) 進行分類。
- **例如 (Diarrhoea 下痢)**: 
  - 先區分是 Small bowel 還是 Large bowel diarrhoea。
  - Large bowel 幾乎一定代表 primary GI disease。
  - Small bowel 則可能是 primary GI disease 或 secondary metabolic disease。

### Question B: Refine the System (這個系統是原發性損傷還是繼發性異常？)
- **Primary / Structural Disease (原發性 / 結構性)**:
  - 該器官本身發生了實質的病變或結構損壞。
  - **診斷方向**: 需要 Imaging (X-ray, US) 或 Biopsy (組織生檢) 來確診。
  - **例如**: 肝臟長了腫瘤導致 ALT 上升、腸道異物導致嘔吐。
- **Secondary / Functional Disease (繼發性 / 功能性)**:
  - 該器官結構正常，但因為其他系統的內分泌、代謝物質或毒素影響，導致功能異常。
  - **診斷方向**: 需要 Blood / Urine test (血液生化尿檢) 或 Endocrine testing (內分泌測試) 來確診。
  - **例如**: Hyperthyroidism (甲狀腺亢進) 導致的 ALT 上升、Uraemia (尿毒症) 導致的嘔吐。

---

## Stage 3: Define the Lesion / Pathology (界定病灶與病理機制)

一旦鎖定了受累系統與原發/繼發性，下一步就是列出該系統所有可能發生的病理變化。此時必須導入 **DAMNIT-V 框架** 來進行 Differential Diagnoses (鑑別診斷) 的羅列與排除：

### The DAMNIT-V Scheme
- **D**egenerative (退化性)
- **A**nomalous (先天性異常 / 畸形)
- **M**etabolic (代謝性)
- **N**eoplastic (腫瘤性) / **N**utritional (營養性)
- **I**nfectious (感染性) / **I**nflammatory (發炎性) / **I**mmune-mediated (免疫媒介性) / **I**diopathic (特發性) / **I**atrogenic (醫源性)
- **T**raumatic (創傷性) / **T**oxic (毒性)
- **V**ascular (血管性)

**實務應用 (Clinical Tip)**: 不需要在每個系統中都把整個 DAMNIT-V 列滿。必須根據病患的 **Signalment (年齡、品種、性別)** 與 **臨床發病進程 (Clinical onset/course)** 來賦予權重。
- **例如**: 年輕動物應優先考慮 **A**nomalous, **I**nfectious, **T**oxin。
- **例如**: 老年動物應優先考慮 **D**egenerative, **M**etabolic, **N**eoplastic。

---

## Stage 4: Formulate the Diagnostic Plan (制定診斷計畫)

根據 Stage 3 列出的 Differential Diagnoses，選擇最安全、最具成本效益 (Cost-effective) 且能最大幅度 narrowing down (縮小範圍) 的檢查。

- **Rule of Thumb (大拇指法則)**: 
  - 常見的疾病在一般門診最常出現 (Common things occur commonly, 聽見馬蹄聲要先猜是馬，而不是斑馬)。
  - 對於有致死風險的鑑別診斷 (如 殺鼠藥中毒, IMHA, Addison's disease)，即使機率較低，也必須在初步計畫中進行快速篩檢或預防性給藥。