import json
import os
import sys
import copy
from datetime import datetime, timedelta

# Dynamic root discovery
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = None
while True:
    if os.path.exists(os.path.join(_current_dir, 'core')):
        _project_root = _current_dir
        if _project_root not in sys.path:
            sys.path.insert(0, _project_root)
        break
    parent = os.path.dirname(_current_dir)
    if parent == _current_dir:
        break
    _current_dir = parent

from core.error_handler import DataMissingError, DataStaleError

VET_DIR = os.getenv("VET_DIR_OVERRIDE", os.path.expanduser("~/.vet"))
CURRENT_PATIENT_FILE = os.path.join(VET_DIR, "current_patient.json")
BACKUP_DIR = os.path.join(VET_DIR, "backups")

# 1. 精細化時間戳記的預設結構
DEFAULT_SCHEMA = {
    "patient": {
        "name": "", "species": "", "breed": "", "sex": "",
        "age": {"value": 0, "unit": "years", "updated_at": ""},
        "weight": {"value": 0.0, "unit": "kg", "updated_at": ""}
    },
    "vitals": {
        "temp": {"value": 0.0, "unit": "C", "updated_at": ""},
        "hr": {"value": 0, "unit": "bpm", "updated_at": ""},
        "rr": {"value": 0, "unit": "bpm", "updated_at": ""},
        "bp": {"value": 0, "unit": "mmHg", "updated_at": ""},
        "crt": {"value": 0, "unit": "sec", "updated_at": ""}
    },
    "problems": [],
    "labs": {
        "blood": {}, # Example: "alt": {"value": 120, "unit": "U/L", "updated_at": "..."}
        "bio": {},
        "ua": {}
    },
    "pain_score": {
        "acute": {"value": 0, "scale": "", "interpretation": "", "updated_at": ""},
        "chronic": {"value": 0, "scale": "", "interpretation": "", "updated_at": ""}
    },
    "management": {
        "diabetes": {
            "insulin_type": "",
            "dose": {"value": 0, "unit": "IU", "updated_at": ""},
            "frequency": "",
            "last_curve_results": {}
        }
    },
    "anesthesia": {
        "risk_category": "", # ASA I-V
        "protocol": {},
        "premeds": [],
        "induction": "",
        "maintenance": ""
    },
    "diagnostic_plan": {
        "recommended_tests": [], # { "test": "ALT", "priority": "High", "reason": "..." }
        "roi_ranking": []
    },
    "meta": {"last_update": "", "status": "active"}
}

# 靜態欄位名單 (不需要更新時間的欄位)
STATIC_PATHS = [
    "patient.name", "patient.species", "patient.breed", "patient.sex",
    "anesthesia.risk_category", "management.diabetes.insulin_type", "management.diabetes.frequency",
    "pain_score.acute.scale", "pain_score.chronic.scale",
    "pain_score.acute.interpretation", "pain_score.chronic.interpretation"
]

def _parse_value(val):
    if isinstance(val, str):
        try: return int(val)
        except ValueError:
            try: return float(val)
            except ValueError: return val
    return val

def _get_nested(data, path):
    keys = path.split('.')
    current = data
    for k in keys:
        if k not in current:
            raise KeyError(f"Missing key: {k}")
        current = current[k]
    return current

def _set_nested(data, path, val):
    keys = path.split('.')
    current = data
    for k in keys[:-1]:
        if k not in current or not isinstance(current[k], dict):
            current[k] = {}
        current = current[k]
    current[keys[-1]] = val

def deep_merge(base, update):
    """Recursively merges update into base."""
    for key, value in update.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base

def init_patient():
    if not os.path.exists(VET_DIR): os.makedirs(VET_DIR)
    schema = copy.deepcopy(DEFAULT_SCHEMA)
    schema["meta"]["last_update"] = datetime.now().isoformat()
    with open(CURRENT_PATIENT_FILE, 'w') as f:
        json.dump(schema, f, indent=2)
    print(f"Initialized new patient context at {CURRENT_PATIENT_FILE}")

def load_data():
    if not os.path.exists(CURRENT_PATIENT_FILE):
        init_patient()
    
    with open(CURRENT_PATIENT_FILE, 'r') as f:
        try:
            stored_data = json.load(f)
        except json.JSONDecodeError:
            stored_data = {}
    
    # Reconcile existing patient files with expanded schema
    full_data = copy.deepcopy(DEFAULT_SCHEMA)
    return deep_merge(full_data, stored_data)

# 2. 精準的巢狀寫入引擎 (Dot-Notation Support)
def update_data(path, value, unit=""):
    """
    Examples: 
      update_data("patient.weight", 5.2, "kg")
      update_data("labs.blood.alt", 120, "U/L")
    """
    data = load_data()
    now_iso = datetime.now().isoformat()
    value = _parse_value(value)
    
    if path == "problems":
        if "problems" not in data: data["problems"] = []
        for p in data["problems"]:
            if isinstance(p, dict) and p.get("value") == value:
                p["updated_at"] = now_iso
                break
        else:
            data["problems"].append({"value": value, "updated_at": now_iso})
            
    elif path in STATIC_PATHS:
        _set_nested(data, path, value)
        
    else:
        # Dynamic field wrapping
        # If the path already ends in .value, .scale, .unit, .interpretation, etc., 
        # it's likely a manual update to a subfield, don't wrap it.
        keys = path.split('.')
        leaf = keys[-1]
        
        if leaf in ["value", "scale", "unit", "interpretation", "updated_at"]:
            _set_nested(data, path, value)
            if leaf == "value":
                parent_path = ".".join(keys[:-1])
                try:
                    parent_node = _get_nested(data, parent_path)
                    if isinstance(parent_node, dict) and "updated_at" in parent_node:
                        parent_node["updated_at"] = now_iso
                except (KeyError, ValueError):
                    pass
        else:
            # Determine if we should use 'scale' or 'unit'
            label = "scale" if "pain_score" in keys else "unit"
            item = {"value": value, label: unit, "updated_at": now_iso}
            _set_nested(data, path, item)
        
    data["meta"]["last_update"] = now_iso
    with open(CURRENT_PATIENT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {path} successfully.")

# 3. 核心：時效安全鎖 (Freshness Validator)
def get_validated_data(path, max_age_days=None, max_age_hours=None):
    """
    Example: 
      weight = get_validated_data("patient.weight", max_age_days=7)
    """
    data = load_data()
    
    try:
        item = _get_nested(data, path)
    except KeyError:
        raise DataMissingError(f"Data for '{path}' is missing.")
        
    if not isinstance(item, dict) or "updated_at" not in item:
        return item # 靜態欄位直接回傳
        
    value = item.get("value")
    updated_at_str = item.get("updated_at")
    
    if not updated_at_str:
        raise DataMissingError(f"Timestamp for '{path}' is missing.")
        
    updated_at = datetime.fromisoformat(updated_at_str)
    age = datetime.now() - updated_at
    
    if max_age_days is not None and age > timedelta(days=max_age_days):
        raise DataStaleError(
            f"[RED FLAG] '{path}' is {age.days} days old! "
            f"Maximum allowed age is {max_age_days} days. Please update first."
        )
        
    if max_age_hours is not None:
        total_hours = age.total_seconds() / 3600
        if total_hours > max_age_hours:
            raise DataStaleError(
                f"[RED FLAG] '{path}' is {total_hours:.1f} hours old! "
                f"Maximum allowed age is {max_age_hours} hours. Please update first."
            )
            
    return value

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "init": init_patient()
        elif cmd == "update" and len(sys.argv) >= 4:
            # Usage: python data_manager.py update patient.weight 5.0 kg
            unit = sys.argv[4] if len(sys.argv) > 4 else ""
            update_data(sys.argv[2], sys.argv[3], unit)
        elif cmd == "get" and len(sys.argv) >= 3:
            # Usage: python data_manager.py get patient.weight 7
            max_days = int(sys.argv[3]) if len(sys.argv) > 3 else None
            try:
                val = get_validated_data(sys.argv[2], max_age_days=max_days)
                print(val)
            except Exception as e:
                print(f"Error: {e}")
