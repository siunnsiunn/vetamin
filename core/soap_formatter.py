import json
import os
from datetime import datetime

VET_DIR = os.path.expanduser("~/.vet")
CURRENT_PATIENT_FILE = os.path.join(VET_DIR, "current_patient.json")
TEMPLATE_PATH = os.path.expanduser("~/.agents/skills/vet-soap-gen/assets/templates/standard_soap.md")

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

    # 準備填入的數據 (處理回寫欄位)
    p = data["patient"]
    v = data["vitals"]
    m = data.get("meta", {})
    ps = data.get("pain_score", {})
    
    mapping = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "doctor_name": "Dr. Jung",
        "pet_name": p.get("name", "N/A"),
        "breed": p.get("breed", "N/A"),
        "age": f"{p.get('age', 0)}Y",
        "sex": p.get("sex", "N/A"),
        "weight": p.get("weight", 0),
        "temp": v.get("temp", 0),
        "hr": v.get("hr", 0),
        "rr": v.get("rr", 0),
        "bp": v.get("bp", 0),
        "mm": v.get("mm", "N/A"),
        "crt": v.get("crt", 0),
        "chief_complaint": ", ".join(data.get("problems", [])) if data.get("problems") else "N/A",
        "history_summary": "Followed standardized clinical reasoning workflow.",
        "current_meds": "Check medication list.",
        "pain_score": f"{ps.get('score', 0)} ({ps.get('scale', 'N/A')})",
        "pain_scale": ps.get("scale", "N/A"),
        "lab_abnormalities": str(data["labs"].get("bio", {})),
        "lab_pattern_result": m.get("renal_interpretation", "Pending analysis."),
        "problem_list": "\n".join([f"- {prob}" for prob in data.get("problems", [])]),
        "diagnostic_hooks": "Azotemia staged by IRIS criteria." if "iris_stage" in data["labs"] else "Pending.",
        "ddx_list": "Metabolic, Inflammatory, Degenerative.",
        "tentative_diagnosis": f"CKD Stage {data['labs'].get('iris_stage', 'TBD')}",
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
