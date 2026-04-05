---
name: vet-pain-score
description: Professional veterinary pain assessment using FGS, Glasgow, CSU, UNESP, LOAD, and HCPI scales. Supports both acute and chronic pain for dogs and cats. (vet-pain-score)
requires:
  ssot:
    - path: vitals
      freshness: 4h
  skills: []
provides:
  ssot:
    - path: pain_score
  downstream_hints: [vet-anesthesia-protocols, vet-soap-gen]
---

# Veterinary Pain Assessment Tool (/vet-pain-score)

本技能提供全方位的 **pain assessment** 指引，涵蓋犬貓急性與慢性疼痛。

## 🏥 Assessment Selector

請根據 **patient** 狀況選擇合適的量表：

### 🐱 Feline (貓)
- **Acute/Post-op**: 
    - **FGS**: [Feline Grimace Scale](references/pain_scales_ref.md) (表情快速評估)。
    - **UNESP**: [Multidimensional Scale](references/unesp_feline.md) (最詳盡，包含生理數值)。
    - **CSU**: [Feline Acute](references/csu_acute.md) (行為與觸診綜合評分)。
- **Chronic/DJD**: 
    - **FMPI**: [Feline Musculoskeletal Pain Index](references/fmpi_questions.md) (生活品質追蹤)。

### 🐶 Canine (犬)
- **Acute/Post-op**: 
    - **CSU**: [Canine Acute](references/csu_acute.md) (經典臨床評分)。
- **Chronic/OA**: 
    - **LOAD**: [Liverpool Osteoarthritis](references/load_dog.md) (運動與環境影響)。
    - **HCPI**: [Helsinki Chronic Pain Index](references/hcpi_dog.md) (行為與情緒影響)。

## ⚙️ Administrative Features (Admin Mode)

1.  **Calculate Total Score**: AI 會引導醫師回答項目，並自動計算總分。
2.  **Compare with Threshold**: 根據結果判斷是否需要 **Analgesia intervention**。
3.  **Handoffs**:
    - "是否執行 `/vet-soap-gen (Automatically aggregate clinical data from previous skill runs and current patient context to generate professional SOAP records, referral reports, or discharge summaries. (vet-soap-gen))` 生成病歷？"
    - "要將 **Pain Score** 存入 **patient context** (執行 **update-patient**) 嗎？"
    - "需要生成 **client-handout** (給飼主的慢性病說明) 嗎？"

## 📝 Reference Library
- [Acute Scales (CSU/FGS)](references/csu_acute.md)
- [UNESP Feline Detail](references/unesp_feline.md)
- [LOAD Dog Detail](references/load_dog.md)
- [HCPI Dog Detail](references/hcpi_dog.md)
- [FMPI Cat Detail](references/fmpi_questions.md)
