# 🐾 Vetamin: Veterinary Clinical Co-pilot Suite (v1.2)

獸醫臨床副駕駛系統，旨在減少行政摩擦並提供**基於實證醫學 (Evidence-Based Medicine)** 的臨床推理支援。

## 🌟 核心技能 (Core Skills)
- 💉 **/vet-dm-manager**: **【NEW】** 糖尿病長期管理（對標 **iCatCare 2025** & **Ettinger's 9th Ed**）。支援 ALIVE DCS 評分與 SGLT2i 監控。
- 🚨 **/vet-triage**: 急診分診與穩定處置（2024 CVJ 標準）。
- 📋 **/vet-history**: 結構化病史採集（LCPS 臨床推理框架）。
- 🧪 **/vet-lab-cross**: **專家級數據判讀**（IDEXX 數據 + BSAVA 全書邏輯）。
- 📉 **/vet-pain-score**: **全方位疼痛評估**（FGS, UNESP, LOAD, FMPI 等）。
- 💉 **/vet-anesthesia-protocols**: **臨床麻醉協定**（針對風險分級提供精確用藥建議）。
- 🌿 **/vet-wellness**: 全生命週期健檢與預防醫學。
- ✍️ **/vet-soap-gen**: **一鍵病歷自動生成**（自動填充精密計算結果）。

---

## 📥 跨平台安裝指引

### 1. 通用步驟
```bash
git clone https://github.com/siunnsiunn/vetamin.git ~/vetamin
```

### ♊ Gemini CLI 部署
Gemini CLI 預設讀取 `~/.agents/skills`。
```bash
mkdir -p ~/.agents/skills
ln -s ~/vetamin/skills/* ~/.agents/skills/
mkdir -p ~/.vet/backups
cp ~/vetamin/core/*.py ~/.vet/
```

### 🤖 Claude Code 部署
Claude Code 預設讀取 `~/.claude/skills`。
```bash
mkdir -p ~/.claude/skills
ln -s ~/vetamin/skills/* ~/.claude/skills/
```

### 💻 Codex 部署
Codex 系統會自動安裝 `.system` 目錄下的技能。
1. **手動安裝特定技能**：
   使用 `$skill-installer` 工具：
   ```bash
   $skill-installer install https://github.com/siunnsiunn/vetamin/tree/main/skills/vet-soap-gen
   ```
2. **重啟 Codex** 以載入新技能。

---

## 🛠️ 技術架構：數據閉環
Vetamin 採用 Python 腳本作為邏輯引擎，所有計算結果會自動回寫至 `~/.vet/current_patient.json`，確保診斷數據的一致性。系統會自動檢測數據時效（例如體重是否超過 7 天未更新），確保醫療決策的安全性。

## 🔧 Runtime Prerequisites

### Python dependencies
路徑自舉已內建於 `core/` 與 `skills/*/scripts/`，但仍需安裝外部 Python 套件：

```bash
pip install pyyaml
```

- `PyYAML`: `core/workflow_validator.py` 解析 `SKILL.md` frontmatter 所需。
- OCR 相關依賴請參考本文末的 OCR 安裝說明。

### SSOT write location

- 預設 SSOT 路徑為 `~/.vet/current_patient.json`
- 在沙盒、CI 或唯讀環境中，請改用 `VET_DIR_OVERRIDE` 指向可寫目錄：

```bash
VET_DIR_OVERRIDE=/tmp/vetamin python3 core/data_manager.py init
```

## ✅ Verification

本次 path bootstrap + SSOT alignment + validator + verifier 修復可用以下整合測試驗證：

```bash
python3 dev_internal/remedy_check.py
```

測試會在隔離 sandbox 中覆蓋以下關鍵路徑：

- `core/data_manager.py` CLI 初始化、讀寫與嵌套路徑更新
- `skills/vet-pain-score/scripts/score_pain_engine.py` 跨目錄執行與 `pain_score.acute` 對齊
- `skills/vet-dm-manager/scripts/dm_calculator.py` 臨床邏輯與 `management.diabetes` 回寫
- `core/workflow_validator.py` 容器型 SSOT 深度檢查
- `core/soap_formatter.py` 在任意 CWD 下的模板定位與渲染

---

## 🌐 語言架構與開發規範 (Language Architecture)
為了平衡 LLM 的理解精確度與台灣臨床醫師的作業效率，Vetamin 遵循以下**「三層語言規範」**：

1. **Metadata (元數據)**：**全英文**。確保各平台 AI 代理人（Gemini, Claude, Codex）索引與呼叫的穩定性。
2. **Workflow (工作流說明)**：**繁體中文 (Taiwan)**。減少醫師在忙碌診間的認知摩擦，直覺掌握下一步。
3. **Medical Logic (醫學邏輯與術語)**：**臨床晶晶體 (Medical Chinglish)**。醫學專有名詞（如 *Azotemia*, *Regenerative*）保留英文以求精確，描述性語句使用繁中。

---
**Maintained by**: DVM Siunn
**Tech Stack**: Python, Markdown.

## 📸 OCR 報告掃描功能說明
若要使用 `/vet-lab-import` 自動掃描紙本報告，請根據你的作業系統安裝對應依賴：

### 🍎 macOS
```bash
pip install ocrmac
```

### 🪟 Windows / 🐧 Linux
建議使用 EasyOCR：
```bash
pip install easyocr
```
*註：第一次執行時會下載約 100MB 的語系模型。*
