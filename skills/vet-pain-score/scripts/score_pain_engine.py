import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../core')))
import data_manager

def score_fgs(scores):
    total = sum(scores)
    interpretation = "Intervention recommended (Analgesia needed)" if total >= 4 else "Comfortable (Monitor)"
    return total, 10, interpretation

def score_glasgow_canine(scores):
    total = sum(scores)
    interpretation = "Analgesia required" if total >= 6 else "Monitor"
    return total, 24, interpretation

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 score_pain_engine.py [fgs|glasgow_dog] [score1] [score2] ...")
    else:
        scale = sys.argv[1].lower()
        input_scores = [int(x) for x in sys.argv[2:]]
        
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
        
        # 自動回寫
        data_manager.update_data("pain_score.scale", scale.upper())
        data_manager.update_data("pain_score.score", f"{total}/{max_val}")
        data_manager.update_data("pain_score.interpretation", note)