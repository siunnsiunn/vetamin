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


def calculate_emergency_doses(weight):
    if weight is None or weight <= 0:
        raise DataMissingError("weight", "A valid weight > 0 is required for emergency doses.")
    
    # 根據標準急診指引 (mg/kg)
    doses = {
        "Atropine (0.5mg/mL)": (0.04 * weight) / 0.5,
        "Epinephrine (1:1000)": (0.01 * weight), # 假設 1mg/mL
        "Naloxone (0.4mg/mL)": (0.04 * weight) / 0.4,
        "Lidocaine (20mg/mL)": (2.0 * weight) / 20 # 狗狗常用
    }
    return doses

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("Usage: python3 calc_emergency_doses.py [weight_kg]")
        else:
            weight = float(sys.argv[1])
            results = calculate_emergency_doses(weight)
            print(f"Emergency Doses for {weight}kg Patient:")
            for drug, ml in results.items():
                print(f"- {drug}: {ml:.2f} mL")
    except VetError as e:
        print(e.to_ai_message())
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
