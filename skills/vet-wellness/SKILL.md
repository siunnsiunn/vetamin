---
name: vet-wellness
description: Guidance for veterinary history taking, physical examination, and wellness care across different life stages (Kitten/Puppy to Senior). Based on AAHA/AAFP standards. (vet-wellness)
requires:
  ssot:
    - path: patient.age
      freshness: null
  skills: []
provides:
  ssot:
    - path: meta.wellness_recommendations
  downstream_hints: [vet-history, vet-soap-gen]
---

# Veterinary Wellness and Life Stage Care (/vet-wellness)

本技能提供 **preventative medicine** (預防醫學) 與各階段健康管理的臨床指引。

## 🏥 Clinical Workflow

1.  **Determine Life Stage**: 
    - 讀取 `.vet/current_patient.json` 裡的 **patient age** 與 **species**。
    - 根據 [canine_life_stage.md](references/canine_life_stage.md) 或 [feline_life_stage.md](references/feline_life_stage.md) 判斷目前是哪一個 **life stage** (Kitten/Puppy, Young Adult, Mature Adult, Senior)。
2.  **Conduct History Taking (Wellness Focus)**: 
    - 焦點放在 **lifestyle**, **behavior**, **nutrition**, 以及 **environmental needs**。
    - 運用 "Provocative Questions" 詢問 **owner** 以挖掘潛在問題。
3.  **Physical Exam (PE) Priorities**:
    - 必須包含 **5 Vital Assessments** (T, P, R, Pain, Nutrition)。
    - 針對 **life-stage** 進行重點篩查 (如：幼年期的 **congenital issues** 或老年期的 **OA screening**)。
4.  **Senior Care (若年齡 >10歲)**:
    - 參照 [senior_care.md](references/senior_care.md) 進行 **DISHA-AL** 篩選及衰弱評估。
    - 注意 **CKD** (慢性腎病) 與 **Hyperthyroidism** (甲亢) 的共病檢查。

## ⚙️ Administrative Automation (Admin Mode)

健檢結束後，主動詢問 user：
- "是否 **handover** 到 `/vet-history (Comprehensive veterinary history taking, clinical communication, and logical problem-solving protocols. Use when conducting physical exams, gathering patient histories, or applying the LCPS framework. (vet-history))` 進行更深度的病史追蹤？"
- "需要執行 `/vet-soap-gen (Automatically aggregate clinical data from previous skill runs and current patient context to generate professional SOAP records, referral reports, or discharge summaries. (vet-soap-gen))` 撰寫 **referral_report** (轉診報告範本) 嗎？"
- "需要為您生成 **vaccination_plan** (疫苗計畫) 嗎？"
- "要提供 **client_education** (給 **owner** 的衛教資訊) 嗎？"

## 📝 Key Reference Files
- [references/canine_life_stage.md](references/canine_life_stage.md)
- [references/feline_life_stage.md](references/feline_life_stage.md)
- [references/senior_care.md](references/senior_care.md)
- [references/referral_community.md](references/referral_community.md)
