---
name: vet-lab-import
description: Extract and structure laboratory data from external paper reports (images or PDFs). (vet-lab-import)
---

# External Lab Importer (/vet-lab-import)

本技能用於將其他醫院的紙本報告（拍照或掃描檔）自動錄入系統。

## 🏥 Clinical Workflow

1.  **Image Upload**: 指導醫師提供圖片路徑（例如：`/Downloads/lab_report.jpg`）。
2.  **OCR Extraction**: 呼叫 `python3 core/ocr_engine.py [path]` 提取原始文字。
3.  **LLM Mapping**: 
    - AI 會將 OCR 的原始文字與 [idexx_ref.md](../vet-lab-cross/references/idexx_ref.md) 比對。
    - 識別關鍵項目：**HCT, WBC, CREA, BUN, ALT, ALKP, ALB, GLOB, USG**。
4.  **Verification**: AI 顯示解析後的數值組合，請醫師確認是否正確。
5.  **Data Integration**: 確認後，呼叫 `data_manager.py` 將數值回寫入 `current_patient.json` 的 `labs` 區塊。

## ⚠️ Notes
- 對於解析不出的項目，AI 必須主動標記並詢問醫師。
- 請優先確認數值單位的正確性（如：mg/dL vs µmol/L）。
