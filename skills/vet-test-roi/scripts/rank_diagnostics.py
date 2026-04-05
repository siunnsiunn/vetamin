import sys
import os
import json

# Dynamic root discovery
_current_dir = os.path.dirname(os.path.abspath(__file__))
while True:
    if os.path.exists(os.path.join(_current_dir, 'core')):
        sys.path.insert(0, _current_dir)
        break
    parent = os.path.dirname(_current_dir)
    if parent == _current_dir: # root reached
        break
    _current_dir = parent

from core.error_handler import VetError, DataMissingError

def load_matrix():
    matrix_path = os.path.join(os.path.dirname(__file__), '../references/roi_matrix.json')
    if not os.path.exists(matrix_path):
        raise FileNotFoundError(f"Matrix file not found at {matrix_path}")
    with open(matrix_path, 'r') as f:
        return json.load(f)

def rank_diagnostics(problem_key, constraint):
    if not problem_key:
        raise DataMissingError("presentation_key")
    if not constraint:
        raise DataMissingError("constraint", "Constraint (None|LowBudget|Fractious) is required.")

    matrix = load_matrix()
    if not matrix or problem_key not in matrix['presentations']:
        print(f"❌ 找不到 '{problem_key}' 的 ROI 評估矩陣。請輸入：")
        print("   " + ", ".join(matrix['presentations'].keys()))
        return

    data = matrix['presentations'][problem_key]
    
    print("====================================================================")
    print(f"🩺 Vetamin 臨床決策效益評估 (Diagnostic ROI & Choosing Wisely)")
    print("   Source: ClinPath Case-Based Approach & Choosing Wisely 2025")
    print(f"   [情境]: {problem_key} | [限制狀態]: {constraint}")
    print("====================================================================\n")

    print("🏆 黃金標準 (Comprehensive Minimum Database - MDB):")
    for i, item in enumerate(data.get('comprehensive_standard', [])):
        print(f"  {i+1}. {item['test']}\n     💡 {item['rationale']}")

    if 'low_value_stop_doing' in data:
        print("\n🚫 低價值/建議停止之項項目 (Low-Value / Stop Doing):")
        print("   (實證醫學顯示效益極低或有潛在風險，建議省下預算)")
        for i, item in enumerate(data['low_value_stop_doing']):
            name = item.get('test', item.get('item'))
            print(f"  - {name}\n    🛑 {item['rationale']}")

    print("\n--------------------------------------------------------------------")
    
    if constraint.lower() in ["lowbudget", "fractious"]:
        print("⚠️ 現實降級方案 (Step-Down Compromise):")
        for i, item in enumerate(data.get('step_down_compromise', [])):
            print(f"  {i+1}. {item['test']}\n     💡 {item['rationale']}")

    print("\n--------------------------------------------------------------------")
    print("🔍 進階/確診檢驗 (Add-on Investigations):")
    for i, item in enumerate(data.get('add_on_investigations', [])):
        print(f"  {i+1}. {item['test']}\n     💡 {item['rationale']}")

    print("\n====================================================================")
    print("⚖️ [防衛性醫療宣告 (Defensive Medicine Rationale)]:")
    print(f"  {data.get('defensive_rationale', '')}")
    if constraint.lower() in ["lowbudget", "fractious"]:
        print("\n  ✍️ 【建議病歷 (SOAP) 紀錄範例】:")
        print("  \"Strongly recommended comprehensive minimum database (CBC, Chem, UA).")
        print("   Owner declined due to financial constraints/Patient fractious.")
        print("   Implemented step-down diagnostics. Advised owner of high risk of ")
        print("   missing underlying metabolic, endocrine, or structural disease. ")
        print("   Owner understands risks and consents to symptomatic treatment.\"")
    print("====================================================================")

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print("Usage: python3 rank_diagnostics.py [presentation_key] [None|LowBudget|Fractious]")
            print("Available keys: acute_vomiting_diarrhoea, severe_anaemia_pallor, pu_pd_polyuria_polydipsia, icterus_hepatobiliary, pruritus_skin_lesions, skin_mass_nodule, feline_weight_loss_polyphagia, acute_collapse_seizures, cavitary_effusion, mitral_valve_disease_mmvd, osteoarthritis_chronic_pain")
        else:
            rank_diagnostics(sys.argv[1], sys.argv[2])
    except VetError as e:
        print(e.to_ai_message())
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)