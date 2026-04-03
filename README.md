# 🐾 Vetamin: Veterinary Clinical Co-pilot Suite (v1.0)

基於 `gstack` 架構開發的獸醫臨床副駕駛系統，旨在減少行政摩擦並提供基於證據的臨床推理支援。

## 🌟 核心技能 (Core Skills)
- 🚨 **/vet-triage**: 急診分診與穩定處置（2024 CVJ 標準）。
- 📋 **/vet-history**: 結構化病史採集（LCPS 臨床推理框架）。
- 🧪 **/vet-lab-cross**: **專家級數據判讀**（IDEXX 數據 + BSAVA 全書邏輯）。
- 📈 **/vet-pain-score**: **全方位疼痛評估**（FGS, UNESP, LOAD, FMPI 等）。
- 🌿 **/vet-wellness**: 全生命週期健檢與預防醫學。
- ✍️ **/vet-soap-gen**: **一鍵病歷自動生成**（自動填充精密計算結果）。

---

## 📥 跨平台快速安裝指引

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

### 💻 Codex (Windsurf / Cursor) 部署
直接在 IDE 中開啟 `~/vetamin` 資料夾，並將其加入 `.cursorrules` 或 `.windsurfrules` 的上下文路徑中。

---

## 🛠️ 技術架構：數據閉環
Vetamin 採用 Python 腳本作為邏輯引擎，所有計算結果（如 IRIS Staging, Corrected Calcium, Pain Score）會自動回寫至 `~/.vet/current_patient.json`，確保診斷數據的一致性。

---
**Maintained by**: Dr. Jung
**Tech Stack**: Python, Markdown, gstack workflow.
