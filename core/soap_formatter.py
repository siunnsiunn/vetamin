import json
import os
from datetime import datetime

VET_DIR = os.path.expanduser("~/.vet")
CURRENT_PATIENT_FILE = os.path.join(VET_DIR, "current_patient.json")
TEMPLATE_PATH = os.path.expanduser("~/.agents/skills/vet-soap-gen/assets/templates/standard_soap.md")

def _get_val(data_dict, key, default=0):
    val = data_dict.get(key, default)
    if isinstance(val, dict):
        return val.get("value", default)
    return val

def generate_soap():
    if not os.path.exists(CURRENT_PATIENT_FILE):
        print("No patient data found.")
        return

    with open(CURRENT_PATIENT_FILE, 'r') as f:
        data = json.load(f)

    # 讀取範本
    if not os.path.exists(TEMPLATE_PATH):
        template = "# SOAP Record\n\nDate: {date}\nPatient: {name}\n\n[Template Missing]"
    else:
        with open(TEMPLATE_PATH, 'r') as f:
            template = f.read()

    # 準備填入的數據 (處理回寫欄位與新的巢狀結構)
    p = data.get("patient", {})
    v = data.get("vitals", {})
    m = data.get("meta", {})
    ps = data.get("pain_score", {})
    
    # Problems 的結構變更 (list of dicts or list of strings)
    problems_raw = data.get("problems", [])
    problems_list = []
    for prob in problems_raw:
        if isinstance(prob, dict):
            problems_list.append(prob.get("value", "Unknown"))
        else:
            problems_list.append(str(prob))
            
    mapping = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "doctor_name": "Dr. Jung",
        "pet_name": p.get("name", "N/A"),
        "breed": p.get("breed", "N/A"),
        "age": f"{_get_val(p, 'age')}Y",
        "sex": p.get("sex", "N/A"),
        "weight": _get_val(p, 'weight'),
        "temp": _get_val(v, 'temp'),
        "hr": _get_val(v, 'hr'),
        "rr": _get_val(v, 'rr'),
        "bp": _get_val(v, 'bp'),
        "mm": _get_val(v, 'mm', 'N/A'),
        "crt": _get_val(v, 'crt'),
        "chief_complaint": ", ".join(problems_list) if problems_list else "N/A",
        "history_summary": "Followed standardized clinical reasoning workflow.",
        "current_meds": "Check medication list.",
        "pain_score": f"{_get_val(ps, 'score')} ({_get_val(ps, 'scale', 'N/A')})",
        "pain_scale": _get_val(ps, 'scale', 'N/A'),
        "lab_abnormalities": str(data.get("labs", {}).get("blood", {})),
        "lab_pattern_result": _get_val(m, 'renal_interpretation', 'Pending analysis.'),
        "problem_list": "\n".join([f"- {prob}" for prob in problems_list]),
        "diagnostic_hooks": "Azotemia staged by IRIS criteria." if "iris_stage" in data.get("labs", {}) else "Pending.",
        "ddx_list": "Metabolic, Inflammatory, Degenerative.",
        "tentative_diagnosis": f"CKD Stage {_get_val(data.get('labs', {}), 'iris_stage', 'TBD')}",
        "next_steps": "Imaging / Follow-up Labs.",
        "medications_prescribed": "Pending order.",
        "fluid_therapy_plan": "Maintenance + Dehydration rate.",
        "owner_brief_summary": "Discussed clinical staging and pain management."
    }

    # 簡單的模板填充
    for key, val in mapping.items():
        template = template.replace(f"{{{{{key}}}}}", str(val))

    print(template)

if __name__ == "__main__":
    generate_soap()