import json
import os
from datetime import datetime

VET_DIR = os.path.expanduser("~/.vet")
CURRENT_PATIENT_FILE = os.path.join(VET_DIR, "current_patient.json")
BACKUP_DIR = os.path.join(VET_DIR, "backups")

DEFAULT_SCHEMA = {
    "patient": {"name": "", "species": "", "breed": "", "age": 0, "weight": 0, "sex": ""},
    "vitals": {"temp": 0, "hr": 0, "rr": 0, "bp": 0, "mm": "", "crt": 0},
    "problems": [],
    "labs": {"blood": {}, "bio": {}, "ua": {}},
    "pain_score": {"scale": "", "score": 0, "interpretation": ""},
    "meta": {"last_update": "", "status": "active"}
}

def init_patient():
    if not os.path.exists(VET_DIR): os.makedirs(VET_DIR)
    with open(CURRENT_PATIENT_FILE, 'w') as f:
        json.dump(DEFAULT_SCHEMA, f, indent=2)
    print(f"Initialized new patient context at {CURRENT_PATIENT_FILE}")

def load_data():
    if not os.path.exists(CURRENT_PATIENT_FILE):
        return DEFAULT_SCHEMA
    with open(CURRENT_PATIENT_FILE, 'r') as f:
        return json.load(f)

def update_data(category, key, value):
    data = load_data()
    if category in data:
        if isinstance(data[category], dict):
            data[category][key] = value
        elif isinstance(data[category], list):
            if value not in data[category]:
                data[category].append(value)
    data["meta"]["last_update"] = datetime.now().isoformat()
    with open(CURRENT_PATIENT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {category}.{key} successfully.")

def archive_patient():
    data = load_data()
    name = data["patient"].get("name", "Unknown")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(BACKUP_DIR): os.makedirs(BACKUP_DIR)
    backup_file = os.path.join(BACKUP_DIR, f"{name}_{timestamp}.json")
    with open(backup_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Archived patient record to {backup_file}")
    init_patient() # Reset for next patient

if __name__ == "__main__":
    # 這裡可以加入簡單的 CLI 介面供 Skill 呼叫
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "init": init_patient()
        elif cmd == "archive": archive_patient()
        elif cmd == "update" and len(sys.argv) == 5:
            update_data(sys.argv[2], sys.argv[3], sys.argv[4])
