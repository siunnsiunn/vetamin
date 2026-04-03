import sys

def calculate_fluid_rate(species, weight, dehydration_pct, ongoing_loss_24h=0):
    # 1. Maintenance (使用標準公式: 80 * kg^0.75 for cats, 132 * kg^0.75 for dogs)
    if species.lower() == "feline":
        maint_24h = 80 * (weight ** 0.75)
    else:
        maint_24h = 132 * (weight ** 0.75)
    
    # 2. Dehydration (ml) = weight(kg) * pct * 10
    dehyd_ml = weight * dehydration_pct * 10
    
    # 3. Total 24h volume
    total_24h = maint_24h + dehyd_ml + ongoing_loss_24h
    hourly_rate = total_24h / 24
    
    return {
        "maint_24h": maint_24h,
        "dehyd_total": dehyd_ml,
        "total_24h": total_24h,
        "hourly_rate": hourly_rate
    }

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 calc_fluid_rate.py [feline|canine] [weight_kg] [%_dehydration] [optional: ongoing_loss_ml]")
    else:
        res = calculate_fluid_rate(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), 
                                   float(sys.argv[4]) if len(sys.argv) > 4 else 0)
        print(f"Fluid Plan for {sys.argv[2]}kg {sys.argv[1]}:")
        print(f"- Maintenance: {res['maint_24h']:.1f} ml/day")
        print(f"- Dehydration Replacement: {res['dehyd_total']:.1f} ml")
        print(f"- Total 24h Volume: {res['total_24h']:.1f} ml")
        print(f"- Target Rate: {res['hourly_rate']:.1f} ml/hr")
