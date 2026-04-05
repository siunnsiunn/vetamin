import os
import sys
_current_dir = os.path.dirname(os.path.abspath(__file__))
while True:
    if os.path.exists(os.path.join(_current_dir, 'core')):
        if _current_dir not in sys.path:
            sys.path.insert(0, _current_dir)
        break
    parent = os.path.dirname(_current_dir)
    if parent == _current_dir:
        break
    _current_dir = parent


from core.error_handler import VetError, DataMissingError
import core.data_manager as data_manager

def score_fgs(scores):
    if not scores:
        raise DataMissingError("fgs_scores", "Feline Grimace Scale requires at least one score.")
    total = sum(scores)
    interpretation = "Intervention recommended (Analgesia needed)" if total >= 4 else "Comfortable (Monitor)"
    return total, 10, interpretation

def score_glasgow_canine(scores):
    if not scores:
        raise DataMissingError("glasgow_scores", "Glasgow Canine Pain Scale requires scores.")
    total = sum(scores)
    interpretation = "Analgesia required" if total >= 6 else "Monitor"
    return total, 24, interpretation

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print("Usage: python3 score_pain_engine.py [fgs|glasgow_dog] [score1] [score2] ...")
        else:
            scale = sys.argv[1].lower()
            if not scale:
                raise DataMissingError("pain_scale")

            try:
                input_scores = [int(x) for x in sys.argv[2:]]
            except ValueError:
                print("Error: Scores must be integers.")
                sys.exit(1)

            if scale == "fgs":
                total, max_val, note = score_fgs(input_scores)
            elif scale == "glasgow_dog":
                total, max_val, note = score_glasgow_canine(input_scores)
            else:
                print("Scale not implemented.")
                sys.exit(1)

            print(f"Pain Scale: {scale.upper()}")
            print(f"Total Score: {total}/{max_val}")
            print(f"Result: {note}")

            # 自動回寫 (對應新 Schema: pain_score.acute)
            data_manager.update_data("pain_score.acute.scale", scale.upper())
            data_manager.update_data("pain_score.acute.value", total)
            data_manager.update_data("pain_score.acute.interpretation", note)
    except VetError as e:
        print(e.to_ai_message())
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)