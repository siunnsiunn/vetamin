---
name: vet-lab-import
description: Extract and structure laboratory data from external paper reports (images or PDFs). (vet-lab-import)
requires:
  ssot: []
  skills: []
provides:
  ssot:
    - path: labs
  downstream_hints: [vet-lab-cross]
---

# External Lab Importer (/vet-lab-import)

本技能用於將其他醫院的紙本報告（拍照或掃描檔）自動錄入系統。

## 🏥 Clinical Workflow

1.  **Image Upload**: 指導醫師提供圖片路徑（例如：`/Downloads/lab_report.jpg`）。
2.  **OCR Extraction & Fallback Chain**: 
    - 呼叫 `python3 core/ocr_engine.py [path]` 提取原始文字。
    - 如果 OCR 失敗或解析度過低，主動詢問醫師："文字不清晰，建議手動輸入關鍵指標：CREA, BUN, ALT, ALKP。"
3.  **IDEXX Cross-Validation**: 
    - AI 會將 OCR 的原始文字與 [idexx_ref.md](../vet-lab-cross/references/idexx_ref.md) 比對。
    - **Mapping Protocol**: 將縮寫（例如：CRE, Crea, CREAT）對應到標準欄位 `creatinine`。
    - **Reference Range Validation**: 比對報表上的參考範圍與系統內建的 [idexx_ref.md](../vet-lab-cross/references/idexx_ref.md)，若有明顯差異（如：貓狗混合、單位不一致），應主動提示醫師。
4.  **Unit Conversion Awareness**: 
    - 偵測數值單位。對於 Glucose, Creatinine, Electrolytes，檢查是否為常見單位誤認 (mg/dL vs mmol/L)。
    - **Alert Logic**: 若 CREA > 50 但報表標示為 mg/dL，可能是 µmol/L，需詢問確認。
5.  **Verification**: AI 顯示解析後的數值組合，請醫師確認是否正確。
6.  **Data Integration**: 確認後，呼叫 `data_manager.py` 將數值回寫入 `current_patient.json` 的 `labs` 區塊。

## ⚙️ Administrative Automation (Admin Mode)
- "是否執行 `/vet-lab-cross (Advanced laboratory data interpretation engine using IDEXX standards and BSAVA algorithms.)` 進行檢驗判讀？"

## ⚠️ Notes
- 對於解析不出的項目，AI 必須主動標記並詢問醫師。
- 請優先確認數值單位的正確性（如：mg/dL vs µmol/L）。
