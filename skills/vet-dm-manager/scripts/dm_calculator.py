import sys
import json
import os

def update_patient_data(insulin_type, dose, protocol="FECAVA 2024"):
    patient_file = os.path.expanduser("~/.vet/current_patient.json")
    try:
        if os.path.exists(patient_file):
            with open(patient_file, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        
        # 建立或更新 DM 管理數據區塊
        if "management" not in data:
            data["management"] = {}
        
        data["management"]["diabetes"] = {
            "current_insulin": insulin_type,
            "dose_iu": dose,
            "frequency": "q12h",
            "protocol_source": protocol,
            "last_update": "2024-04-03"
        }
        
        with open(patient_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Success: Decision [ {dose}U {insulin_type} ] written to SSOT.")
    except Exception as e:
        print(f"Error writing to SSOT: {e}")

if __name__ == "__main__":
    # 範例執行：python3 dm_calculator.py Toujeo 2.0
    if len(sys.argv) >= 3:
        ins_type = sys.argv[1]
        dose_val = float(sys.argv[2])
        update_patient_data(ins_type, dose_val)
    else:
        print("Usage: python3 dm_calculator.py [InsulinType] [DoseIU]")
