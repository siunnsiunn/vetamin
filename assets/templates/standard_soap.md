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
- **Pain Score**: {{pain_score}} (使用量表: {{pain_scale}})
- **Lab Highlights (異常指標)**:
    - {{lab_abnormalities}}
    - **Pattern Analysis**: {{lab_pattern_result}}

## 3. Assessment (臨床評估)
- **Problem List**: 
    {{problem_list}}
- **Diagnostic Hooks (硬指標)**: {{diagnostic_hooks}}
- **Differential Diagnosis (DDx)**: 
    - Based on DAMNIT-V: {{ddx_list}}
- **Refinement**: {{tentative_diagnosis}}

## 4. Plan (診斷與治療計畫)
- **Diagnostic Plan**: {{next_steps}}
- **Treatment Plan**:
    - {{medications_prescribed}}
    - {{fluid_therapy_plan}}
- **Client Education**: {{owner_brief_summary}}

---
**Status**: [ ] Stable [ ] Critical [ ] Handed over
