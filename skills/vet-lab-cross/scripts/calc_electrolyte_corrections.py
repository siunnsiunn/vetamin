import os
import sys
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


def correct_calcium(ca, alb):
    if ca is None: raise DataMissingError("calcium")
    if alb is None: raise DataMissingError("albumin")
    # 適用於狗狗的校正鈣公式
    return ca - alb + 3.5

def correct_chloride(cl, na, na_normal=146):
    if cl is None: raise DataMissingError("chloride")
    if na is None: raise DataMissingError("sodium")
    if na == 0: raise VetError("Sodium cannot be zero for chloride correction.")
    # 判讀原發性氯變動
    return cl * (na_normal / na)

def get_na_k_ratio(na, k):
    if na is None: raise DataMissingError("sodium")
    if k is None: raise DataMissingError("potassium")
    if k == 0: raise VetError("Potassium cannot be zero for Na/K ratio.")
    return na / k

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("Usage: python3 calc_electrolyte_corrections.py [ca_corr|cl_corr|nak_ratio] [params...]")
        else:
            cmd = sys.argv[1]
            if cmd == "ca_corr" and len(sys.argv) == 4:
                print(f"Corrected Calcium: {correct_calcium(float(sys.argv[2]), float(sys.argv[3])):.2f} mg/dL")
            elif cmd == "cl_corr" and len(sys.argv) == 4:
                print(f"Corrected Chloride: {correct_chloride(float(sys.argv[2]), float(sys.argv[3])):.2f} mmol/L")
            elif cmd == "nak_ratio" and len(sys.argv) == 4:
                ratio = get_na_k_ratio(float(sys.argv[2]), float(sys.argv[3]))
                note = "(Addison Risk!)" if ratio < 27 else ""
                print(f"Na/K Ratio: {ratio:.2f} {note}")
    except VetError as e:
        print(e.to_ai_message())
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
