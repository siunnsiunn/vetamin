import sys
import os
import json

def load_matrix():
    matrix_path = os.path.join(os.path.dirname(__file__), '../references/roi_matrix.json')
    if not os.path.exists(matrix_path):
        print(f"Error: Matrix file not found at {matrix_path}")
        return None
    with open(matrix_path, 'r') as f:
        return json.load(f)

def rank_diagnostics(problem_key, constraint):
    matrix = load_matrix()
    if not matrix or problem_key not in matrix['presentations']:
        print(f"❌ 找不到 '{problem_key}' 的 ROI 評估矩陣。請輸入：acute_vomiting_diarrhoea, severe_anaemia_pallor, pu_pd_polyuria_polydipsia, icterus_hepatobiliary, pruritus_skin_lesions, skin_mass_nodule, feline_weight_loss_polyphagia")
        return

    data = matrix['presentations'][problem_key]
    
    print("====================================================================")
    print(f"🩺 Vetamin 臨床檢驗效益評估 (Diagnostic ROI & Spectrum of Care)")
    print("   Source: Veterinary Clinical Pathology: A Case-Based Approach")
    print(f"   [情境]: {problem_key} | [限制狀態]: {constraint}")
    print("====================================================================\n")

    print("🏆 黃金標準 (Comprehensive Minimum Database - MDB):")
    print("   (教科書強烈建議：在確診前，這是找出潛在病因的最基礎且必要的組合)")
    for i, item in enumerate(data.get('comprehensive_standard', [])):
        print(f"  {i+1}. {item['test']}\n     💡 {item['rationale']}")

    print("\n--------------------------------------------------------------------")
    
    if constraint.lower() in ["lowbudget", "fractious"]:
        print("⚠️ 現實降級方案 (Step-Down Compromise):")
        print("   (因預算極低或病患具攻擊性，只能執行最低限度之續命/排除致死風險檢查)")
        for i, item in enumerate(data.get('step_down_compromise', [])):
            print(f"  {i+1}. {item['test']}\n     💡 {item['rationale']}")

    print("\n--------------------------------------------------------------------")
    print("🔍 進階/確診檢驗 (Add-on Investigations):")
    print("   (基於 MDB 的結果，若有特定懷疑方向，才加做的特異性檢查)")
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
    if len(sys.argv) < 3:
        print("Usage: python3 rank_diagnostics.py [acute_vomiting_diarrhoea|severe_anaemia_pallor|pu_pd_polyuria_polydipsia|icterus_hepatobiliary] [None|LowBudget|Fractious]")
    else:
        rank_diagnostics(sys.argv[1], sys.argv[2])