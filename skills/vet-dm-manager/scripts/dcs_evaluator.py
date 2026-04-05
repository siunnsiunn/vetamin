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
import core.data_manager as data_manager

def evaluate_dcs(demeanour, body_weight, water_intake, urine_output):
    # Validate inputs
    scores = {"demeanour": demeanour, "body_weight": body_weight, "water_intake": water_intake, "urine_output": urine_output}
    for field, val in scores.items():
        if val is None:
            raise DataMissingError(field)
        if val < 0 or val > 3:
            raise VetError(f"Invalid score for {field}: {val}. Must be 0-3.", field=field)

    rubric_path = os.path.join(os.path.dirname(__file__), '..', 'references', 'alive_dcs_rubric.json')
    try:
        with open(rubric_path, 'r', encoding='utf-8') as f:
            rubric = json.load(f)
    except Exception as e:
        print(f"Error loading ALIVE DCS rubric: {e}")
        return

    total_score = sum(scores.values())
    
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
    try:
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
    except VetError as e:
        print(e.to_ai_message())
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)