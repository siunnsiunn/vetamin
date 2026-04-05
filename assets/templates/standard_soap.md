# 🐾 獸醫臨床病歷 - SOAP Record

**Date**: {{date}}
**Doctor**: {{doctor_name}}
**Patient**: {{pet_name}} ({{breed}} / {{sex}} / {{age}})

---

## 1. Subjective (主觀描述)
- **Chief Complaint (CC)**: {{chief_complaint}}
- **History**: 
    - {{history_summary}}
    - **Current Medications**: {{current_meds}}

## 2. Objective (客觀檢查)
- **Vitals**: 
    - Weight: {{weight}} kg
    - T: {{temp}} °C | HR: {{hr}} bpm | RR: {{rr}} brpm
    - BP: {{bp}} mmHg | MM: {{mm}} | CRT: {{crt}}s

{{#pain_score_section}}
- **Pain Score**: {{pain_score}} (使用量表: {{pain_scale}})
- **Interpretation**: {{pain_interpretation}}
{{/pain_score_section}}

- **Lab Highlights (異常指標)**:
    - {{lab_abnormalities}}
    - **Pattern Analysis**: {{lab_pattern_result}}

{{#diabetes_section}}
## 2b. Endocrine — Diabetes
- **ALIVE DCS**: {{dcs_score}}/12 ({{dcs_interpretation}})
- **Current Dose**: {{dm_calculated_dose}} IU {{dm_insulin_type}}
- **Guidance**: {{dm_clinical_guidance}}
{{/diabetes_section}}

{{#anesthesia_section}}
## 2c. Anesthesia Summary
- **ASA Risk Category**: {{asa_risk}}
- **Protocol Highlights**: {{anesthesia_protocol}}
- **Premeds**: {{anesthesia_premeds}}
- **Induction**: {{anesthesia_induction}}
- **Maintenance**: {{anesthesia_maintenance}}
{{/anesthesia_section}}

## 3. Assessment (臨床評估)
- **Problem List**: 
    {{problem_list}}
- **Diagnostic Hooks (硬指標)**: {{diagnostic_hooks}}
- **Differential Diagnosis (DDx)**: 
    - Based on DAMNIT-V: {{ddx_list}}
- **Refinement**: {{tentative_diagnosis}}

## 4. Plan (診斷與治療計畫)
{{#diagnostic_plan_section}}
- **Recommended Tests**: {{recommended_tests}}
- **ROI Ranking**: {{roi_ranking}}
{{/diagnostic_plan_section}}

- **Treatment Plan**:
    - {{medications_prescribed}}
    - {{fluid_therapy_plan}}
- **Client Education**: {{owner_brief_summary}}

---
**Status**: [ ] Stable [ ] Critical [ ] Handed over
