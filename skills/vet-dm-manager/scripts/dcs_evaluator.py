import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../core')))
import data_manager

def evaluate_dcs(demeanour, body_weight, water_intake, urine_output):
    rubric_path = os.path.join(os.path.dirname(__file__), '..', 'references', 'alive_dcs_rubric.json')
    try:
        with open(rubric_path, 'r', encoding='utf-8') as f:
            rubric = json.load(f)
    except Exception as e:
        print(f"Error loading ALIVE DCS rubric: {e}")
        return

    # Validate inputs
    scores = [demeanour, body_weight, water_intake, urine_output]
    if any(s < 0 or s > 3 for s in scores):
        print("Error: Each score must be between 0 and 3.")
        return

    total_score = sum(scores)
    
    # Interpretation
    if total_score <= 3:
        status = rubric['interpretation']['0-3']
    elif total_score <= 7:
        status = rubric['interpretation']['4-7']
    else:
        status = rubric['interpretation']['8-12']

    # Update patient SSOT using data_manager
    try:
        data_manager.update_data("management.diabetes.alive_dcs.score", total_score)
        data_manager.update_data("management.diabetes.alive_dcs.status", status)
        data_manager.update_data("management.diabetes.alive_dcs.components.demeanour", demeanour)
        data_manager.update_data("management.diabetes.alive_dcs.components.body_weight", body_weight)
        data_manager.update_data("management.diabetes.alive_dcs.components.water_intake", water_intake)
        data_manager.update_data("management.diabetes.alive_dcs.components.urine_output", urine_output)
        
        print(f"ALIVE DCS Evaluation Complete. Total Score: {total_score}/12.")
        print(f"Clinical Status: {status}")
        print("Data synchronized to SSOT (current_patient.json) via data_manager.")
    except Exception as e:
        print(f"Error writing to SSOT: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 5:
        try:
            d = int(sys.argv[1])
            bw = int(sys.argv[2])
            wi = int(sys.argv[3])
            uo = int(sys.argv[4])
            evaluate_dcs(d, bw, wi, uo)
        except ValueError:
            print("Usage: python3 dcs_evaluator.py [Demeanour 0-3] [BodyWeight 0-3] [WaterIntake 0-3] [UrineOutput 0-3]")
    else:
        print("Usage: python3 dcs_evaluator.py [Demeanour 0-3] [BodyWeight 0-3] [WaterIntake 0-3] [UrineOutput 0-3]")