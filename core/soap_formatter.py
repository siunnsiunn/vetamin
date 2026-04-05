import json
import os
import sys
import re
from datetime import datetime

# Dynamic root discovery
_current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = None
while True:
    if os.path.exists(os.path.join(_current_dir, 'core')):
        PROJECT_ROOT = _current_dir
        if PROJECT_ROOT not in sys.path:
            sys.path.insert(0, PROJECT_ROOT)
        break
    parent = os.path.dirname(_current_dir)
    if parent == _current_dir: # root reached
        break
    _current_dir = parent

from core.data_manager import load_data, _get_nested

VET_DIR = os.path.expanduser("~/.vet")
CURRENT_PATIENT_FILE = os.path.join(VET_DIR, "current_patient.json")
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "assets/templates/standard_soap.md")

def _get_val(data_dict, key, default="N/A"):
    try:
        val = _get_nested(data_dict, key)
        if isinstance(val, dict) and "value" in val:
            return val["value"]
        return val
    except (KeyError, ValueError):
        return default

def render_template(template, mapping):
    # Handle {{#section}}...{{/section}}
    def replace_section(match):
        section_name = match.group(1)
        section_content = match.group(2)
        if mapping.get(section_name):
            return section_content
        return ""

    pattern = re.compile(r'\{\{#(.*?)\}\}(.*?)\{\{/\1\}\}', re.DOTALL)
    rendered = pattern.sub(replace_section, template)

    # Handle standard {{variable}}
    for key, val in mapping.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(val))
    
    return rendered

def generate_soap():
    data = load_data()

    # 讀取範本
    if not os.path.exists(TEMPLATE_PATH):
        template = "# SOAP Record\n\nDate: {{date}}\nPatient: {{pet_name}}\n\n[Template Missing]"
    else:
        with open(TEMPLATE_PATH, 'r') as f:
            template = f.read()

    # Prepare mapping
    p = data.get("patient", {})
    v = data.get("vitals", {})
    ps = data.get("pain_score", {})
    mgmt = data.get("management", {})
    anes = data.get("anesthesia", {})
    diag = data.get("diagnostic_plan", {})
    
    problems_raw = data.get("problems", [])
    problems_list = [p["value"] if isinstance(p, dict) else str(p) for p in problems_raw]
            
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
        
        "pain_score_section": bool(ps.get("acute", {}).get("value") or ps.get("chronic", {}).get("value")),
        "pain_score": f"Acute: {_get_val(ps, 'acute.value')} | Chronic: {_get_val(ps, 'chronic.value')}",
        "pain_scale": f"{_get_val(ps, 'acute.scale')} / {_get_val(ps, 'chronic.scale')}",
        "pain_interpretation": _get_val(ps, 'acute.interpretation', 'N/A'),
        "pain_recommendation": _get_val(ps, 'acute.interpretation', 'Follow-up needed.'),

        "diabetes_section": bool(mgmt.get("diabetes", {}).get("insulin_type") or mgmt.get("diabetes", {}).get("dose", {}).get("value")),
        "dcs_score": _get_val(mgmt, "diabetes.last_curve_results.dcs_score", "0"),
        "dcs_interpretation": "TBD",
        "dm_calculated_dose": _get_val(mgmt, "diabetes.dose.value", "0"),
        "dm_insulin_type": _get_val(mgmt, "diabetes.insulin_type", "N/A"),
        "dm_clinical_guidance": _get_val(mgmt, "diabetes.clinical_guidance", "Monitor glucose curve."),

        "anesthesia_section": bool(anes.get("risk_category")),
        "asa_risk": anes.get("risk_category", "N/A"),
        "anesthesia_protocol": str(anes.get("protocol", "N/A")),
        "anesthesia_premeds": ", ".join(anes.get("premeds", [])),
        "anesthesia_induction": anes.get("induction", "N/A"),
        "anesthesia_maintenance": anes.get("maintenance", "N/A"),

        "diagnostic_plan_section": bool(diag.get("recommended_tests") or diag.get("roi_ranking")),
        "recommended_tests": ", ".join([str(t) for t in diag.get("recommended_tests", [])]),
        "roi_ranking": ", ".join([str(r) for r in diag.get("roi_ranking", [])]),

        "chief_complaint": ", ".join(problems_list) if problems_list else "N/A",
        "history_summary": "Followed standardized clinical reasoning workflow.",
        "current_meds": "Check medication list.",
        "lab_abnormalities": str(data.get("labs", {}).get("blood", {})),
        "lab_pattern_result": data.get("meta", {}).get("lab_patterns", "Pending analysis."),
        "problem_list": "\n".join([f"- {prob}" for prob in problems_list]),
        "diagnostic_hooks": "Pending specific skill output.",
        "ddx_list": "Metabolic, Inflammatory, Degenerative.",
        "tentative_diagnosis": "TBD",
        "next_steps": "Imaging / Follow-up Labs.",
        "medications_prescribed": "Pending order.",
        "fluid_therapy_plan": "Maintenance + Dehydration rate.",
        "owner_brief_summary": "Discussed clinical staging and management."
    }

    print(render_template(template, mapping))

if __name__ == "__main__":
    generate_soap()