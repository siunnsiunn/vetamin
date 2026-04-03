# 🐾 Vetamin: Veterinary Clinical Co-pilot Suite (v1.2)

獸醫臨床副駕駛系統，旨在減少行政摩擦並提供**基於實證醫學 (Evidence-Based Medicine)** 的臨床推理支援。

## 🛡️ Vetamin 臨床邏輯五大硬原則
為了確保臨床安全，所有 Vetamin 技能均遵循以下開發規範：
1. **實證溯源**：嚴禁 AI 幻覺，所有建議必須精確對標 Ettinger's, Plumb's, 或最新 Consensus。
2. **臨床紅線優先**：病患臨床指標（如嘔吐、拒食）優先權高於數學計算劑量。
3. **醫學術語去毒**：徹底捨棄過時術語（如 Somogyi），採用現代醫學框架。
4. **物理執行精度**：劑量計算自動校正至臨床可執行單位（如胰島素 0.5 IU）。
5. **生理反應窗口**：強調數據時效性與趨勢穩定，嚴禁盲目追逐單次血糖數值。

## 🌟 核心技能 (Core Skills)
- 💉 **/vet-dm-manager**: **【NEW】** 糖尿病長期管理（對標 **iCatCare 2025** & **Ettinger's 9th Ed**）。支援 ALIVE DCS 評分與 SGLT2i 監控。
- 🚨 **/vet-triage**: 急診分診與穩定處置（2024 CVJ 標準）。
- 📋 **/vet-history**: 結構化病史採集（LCPS 臨床推理框架）。
- 🧪 **/vet-lab-cross**: **專家級數據判判**（IDEXX 數據 + BSAVA 全書邏輯）。
- 📉 **/vet-pain-score**: **全方位疼痛評估**（FGS, UNESP, LOAD, FMPI 等）。
- 💉 **/vet-anesthesia-protocols**: **臨床麻醉協定**（針對風險分級提供精確用藥與 Crash Sheet）。
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

---

## 🛠️ 技術架構：數據閉環 (SSOT)
Vetamin 採用 Python 腳本作為邏輯引擎，所有臨床數據同步至 `~/.vet/current_patient.json`。系統會自動檢測數據時效（例如體重是否超過 7 天未更新），確保醫療決策的安全性。

---

## 🌐 語言架構與開發規範 (Language Architecture)
1. **Metadata**：全英文。確保 AI 代理人呼叫穩定。
2. **Workflow**：繁體中文 (Taiwan)。減少診間認知摩擦。
3. **Medical Logic**：臨床晶晶體 (Medical Chinglish)。保留英文名詞以求精確。

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
