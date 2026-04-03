import sys

def calculate_emergency_doses(weight):
    # 根據標準急診指引 (mg/kg)
    doses = {
        "Atropine (0.5mg/mL)": (0.04 * weight) / 0.5,
        "Epinephrine (1:1000)": (0.01 * weight), # 假設 1mg/mL
        "Naloxone (0.4mg/mL)": (0.04 * weight) / 0.4,
        "Lidocaine (20mg/mL)": (2.0 * weight) / 20 # 狗狗常用
    }
    return doses

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 calc_emergency_doses.py [weight_kg]")
    else:
        weight = float(sys.argv[1])
        results = calculate_emergency_doses(weight)
        print(f"Emergency Doses for {weight}kg Patient:")
        for drug, ml in results.items():
            print(f"- {drug}: {ml:.2f} mL")
