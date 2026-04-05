import sys
import os

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

def get_iris_stage(species, crea, sdma=None):
    if not species:
        raise DataMissingError("species")
    if not crea or crea <= 0:
        raise DataMissingError("crea", "A valid CREA value > 0 is required for renal staging.")

    species = species.lower()
    if species not in ["feline", "canine"]:
        raise VetError(f"Species '{species}' not supported for IRIS staging. Use 'feline' or 'canine'.")

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
    try:
        if len(sys.argv) < 3:
            print("Usage: python3 calc_renal_staging.py [feline|canine] [CREA] [optional: SDMA]")
        else:
            species = sys.argv[1]
            try:
                crea = float(sys.argv[2])
                sdma = float(sys.argv[3]) if len(sys.argv) > 3 else None
            except ValueError:
                print("Error: CREA and SDMA must be numeric.")
                sys.exit(1)

            result = get_iris_stage(species, crea, sdma)
            output = f"IRIS CKD Result: Stage {result}"
            print(output)
            # 自動回寫
            data_manager.update_data("meta.renal_interpretation", output)
            data_manager.update_data("labs.iris_stage", result)
    except VetError as e:
        print(e.to_ai_message())
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)