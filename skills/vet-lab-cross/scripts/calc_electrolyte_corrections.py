import sys

def correct_calcium(ca, alb):
    # 適用於狗狗的校正鈣公式
    return ca - alb + 3.5

def correct_chloride(cl, na, na_normal=146):
    # 判讀原發性氯變動
    return cl * (na_normal / na)

def get_na_k_ratio(na, k):
    return na / k

if __name__ == "__main__":
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
