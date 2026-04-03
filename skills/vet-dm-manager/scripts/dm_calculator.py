import sys
import json
import os

def calculate_icatcare_2025_adjustment(current_dose, nadir_bg):
    """
    套用 iCatCare 2025 安全優先邏輯。
    安全紅線: < 72 mg/dL (4 mmol/L)
    """
    recommendation = ""
    suggested_dose = current_dose
    alert = False

    if nadir_bg < 72:
        alert = True
        # iCatCare 建議：立即減量 25-50% 或調降 0.5 - 1.0 IU
        reduction = max(0.5, current_dose * 0.25)
        suggested_dose = max(0, current_dose - reduction)
        recommendation = f"【安全警示】最低血糖 {nadir_bg} mg/dL 低於 72 mg/dL 紅線！判定為劑量過高。建議立即減量至 {suggested_dose} IU (調降 {reduction} IU)。"
    elif 72 <= nadir_bg < 80:
        recommendation = "血糖接近安全下限，控制極其嚴格，請密切監控臨床表現，暫勿增加劑量。"
    elif 80 <= nadir_bg <= 150:
        recommendation = "理想 Nadir (80-150 mg/dL)。控制狀態極佳，建議維持目前劑量。"
    else:
        recommendation = "Nadir > 150 mg/dL。控制尚未達標，但請維持原劑量至少 5-7 天 (Stop Chasing Numbers)，觀察穩定度後再考慮增量。"

    return suggested_dose, recommendation, alert

def update_patient_data(insulin_type, dose, nadir_bg, recommendation, alert):
    patient_file = os.path.expanduser("~/.vet/current_patient.json")
    try:
        if os.path.exists(patient_file):
            with open(patient_file, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        
        if "management" not in data:
            data["management"] = {}
        
        data["management"]["diabetes"] = {
            "current_insulin": insulin_type,
            "dose_iu": dose,
            "nadir_bg_mgdl": nadir_bg,
            "safety_alert": alert,
            "recommendation": recommendation,
            "protocol_source": "iCatCare 2025",
            "last_update": "2024-04-03"
        }
        
        with open(patient_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        # 輸出臨床決策摘要
        print(f"\n--- iCatCare 2025 臨床決策支援 ---")
        print(f"建議方案: {recommendation}")
        print(f"最終決定劑量: {dose} IU ({insulin_type})")
        print(f"----------------------------------------")
        print(f"成功：決策數據已同步至 SSOT (current_patient.json)。")
    except Exception as e:
        print(f"Error writing to SSOT: {e}")

if __name__ == "__main__":
    # 使用方式: python3 dm_calculator.py [胰島素種類] [目前劑量] [最低血糖值]
    if len(sys.argv) >= 4:
        try:
            ins_type = sys.argv[1]
            curr_dose = float(sys.argv[2])
            nadir = float(sys.argv[3])
            
            new_dose, rec, is_alert = calculate_icatcare_2025_adjustment(curr_dose, nadir)
            update_patient_data(ins_type, new_dose, nadir, rec, is_alert)
        except ValueError:
            print("Error: Dose and Nadir must be numbers.")
    else:
        print("Usage: python3 dm_calculator.py [InsulinType] [CurrentDoseIU] [NadirBG]")
