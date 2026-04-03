import sys
import os
import json

# 引入 data_manager 邏輯
VET_DIR = os.path.expanduser("~/.vet")
CURRENT_PATIENT_FILE = os.path.join(VET_DIR, "current_patient.json")

def save_to_json(category, key, value):
    if os.path.exists(CURRENT_PATIENT_FILE):
        with open(CURRENT_PATIENT_FILE, 'r') as f:
            data = json.load(f)
        if category not in data: data[category] = {}
        data[category][key] = value
        with open(CURRENT_PATIENT_FILE, 'w') as f:
            json.dump(data, f, indent=2)

def get_iris_stage(species, crea, sdma=None):
    # ... (原有邏輯不變)
    species = species.lower()
    stage = 0
    if species == "feline":
        if crea < 140: stage = 1
        elif 140 <= crea <= 250: stage = 2
        elif 251 <= crea <= 440: stage = 3
        else: stage = 4
        if sdma:
            if sdma > 14 and stage == 1: stage = "1 (SDMA elevated)"
            if sdma > 25 and stage == 2: stage = 3
            if sdma > 45 and stage == 3: stage = 4
    elif species == "canine":
        if crea < 125: stage = 1
        elif 125 <= crea <= 250: stage = 2
        elif 251 <= crea <= 440: stage = 3
        else: stage = 4
        if sdma:
            if sdma > 14 and stage == 1: stage = "1 (SDMA elevated)"
            if sdma > 35 and stage == 2: stage = 3
            if sdma > 54 and stage == 3: stage = 4
    return stage

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 calc_renal_staging.py [feline|canine] [CREA] [optional: SDMA]")
    else:
        species = sys.argv[1]
        crea = float(sys.argv[2])
        sdma = float(sys.argv[3]) if len(sys.argv) > 3 else None
        result = get_iris_stage(species, crea, sdma)
        output = f"IRIS CKD Result: Stage {result}"
        print(output)
        # 自動回寫
        save_to_json("meta", "renal_interpretation", output)
        save_to_json("labs", "iris_stage", result)
