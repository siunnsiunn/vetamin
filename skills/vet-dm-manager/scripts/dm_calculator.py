import sys
import os
import math
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../core')))
import data_manager

def clinical_round(value, step=0.5):
    return round(value / step) * step

def calculate_modern_dm_logic(species, current_dose, weight_kg, nadir_bg, peak_bg, appetite_pct=100, is_vomiting=False):
    """
    V1.2: 現代化臨床版本。
    - 徹底捨棄 Somogyi 術語。
    - 採用 Ettinger's 9th Ed 的「血糖不穩定性 (Glycemic Variability)」框架。
    """
    recommendation = []
    suggested_dose = current_dose
    alert = False
    
    unit_per_kg = current_dose / weight_kg if weight_kg > 0 else 0

    # 1. 安全第一 (Safety Interlock)
    if is_vomiting:
        return 0, "【🔴 緊急停藥】出現嘔吐！疑似 DKA/eDKA/胰臟炎。指令：立即送醫。", True
    if appetite_pct == 0:
        return 0, "【🔴 安全跳過】拒食。絕對禁止注射，聯繫獸醫。", True
    if appetite_pct < 50:
        suggested_dose = clinical_round(current_dose * 0.5)
        return suggested_dose, f"【⚠️ 劑量減半】食慾極差 ({appetite_pct}%)。建議減半施打並觀察。", True

    # 2. 現代化頑固型病例排查 (對標 Ettinger's 9th Ed Fig 291.4)
    if unit_per_kg > 1.0:
        recommendation.append(f"⚠️ 警示：當前劑量 ({unit_per_kg:.2f} U/kg) 偏高。")
        if nadir_bg < 80:
            # 取代過時的 Somogyi 術語
            recommendation.append("【臨床排查】偵測到低血糖事件，且臨床症狀持續。此為「血糖不穩定性 (Glycemic Variability)」，主因通常是劑量過高或蓄積池 (Depot) 異常，而非拮抗激素反彈。指令：調降劑量。")
        elif nadir_bg > 150:
            recommendation.append("【臨床排查】胰島素無效。請排查 Cushing's、胰臟炎或發情等阻抗因子。")

    # 3. 物種特異性目標
    if species == "dog":
        if nadir_bg < 80:
            alert = True
            suggested_dose = clinical_round(current_dose * 0.75)
            recommendation.append(f"【⚠️ 低血糖】Nadir {nadir_bg} < 80。調降至 {suggested_dose} IU。")
        elif nadir_bg > 150:
            suggested_dose = clinical_round(current_dose * 1.1)
            recommendation.append(f"【📈 未達標】建議微加至 {suggested_dose} IU。警告：必須已穩定施打舊劑量 5-7 天。")
        else:
            recommendation.append("【✅ 目標達成】80-150 mg/dL。提醒：先吃飯再打針。")
            
    else: # 貓咪
        if nadir_bg < 72:
            alert = True
            suggested_dose = max(0, clinical_round(current_dose - 0.5))
            recommendation.append(f"【⚠️ 安全警示】低於 72 (iCatCare 2025 線)。調降至 {suggested_dose} IU。")
        elif 72 <= nadir_bg <= 150:
            recommendation.append("【✅ 貓咪目標達成】控制良好。")
        else:
            recommendation.append("【📈 未達標】評估低碳水飲食。調整前請確認數據時效。")

    return suggested_dose, " | ".join(recommendation), alert

def update_ssot_v1_2(species, dose, nadir, rec, alert):
    try:
        data_manager.update_data("management.diabetes.version", "V1.2 Modernized")
        data_manager.update_data("management.diabetes.evidence", "Ettinger's 9th Ed (2021) & iCatCare 2025")
        data_manager.update_data("management.diabetes.calculated_dose_iu", dose)
        data_manager.update_data("management.diabetes.clinical_guidance", rec)
        data_manager.update_data("management.diabetes.timestamp", datetime.now().isoformat())
        
        print(f"\n=== [Clinical Copilot V1.2] 現代化實證版本 ===")
        print(f"核心變動: 徹底移除 Somogyi 術語，改採 Glycemic Variability 框架。")
        print(f"決策結果: {dose} IU")
        print(f"臨床建議: {rec}")
        print(f"================================================")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) >= 8:
        new_dose, rec, alert = calculate_modern_dm_logic(
            sys.argv[1].lower(), float(sys.argv[3]), float(sys.argv[2]), 
            float(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6]), sys.argv[7] == "1"
        )
        update_ssot_v1_2(sys.argv[1], new_dose, float(sys.argv[4]), rec, alert)
    else:
        print("Usage: python3 dm_calculator.py [dog/cat] [weight] [dose] [nadir] [peak] [appetite%] [vomiting_0/1]")