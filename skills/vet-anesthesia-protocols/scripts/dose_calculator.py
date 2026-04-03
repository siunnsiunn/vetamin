#!/usr/bin/env python3
"""
Veterinary Anesthesia Drug Dose Calculator (V1.2.1 - Chief's Edition)

Calculates patient-specific drug doses based on body weight and comorbidities.
Integrates contraindication logic from AAFP 2020, AAHA 2020, and ACVAA 2025.
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict

# ---------------------------------------------------------------------------
# Contraindication Matrix (The "Chief's Brain")
# ---------------------------------------------------------------------------
CONTRAINDICATIONS = {
    "hyperthyroid": {
        "avoid": ["ketamine", "ketamine_combo_low", "ketamine_cri"],
        "reason": "甲亢禁忌：避免使用 Ketamine (Sympathomimetic)，以免引發心搏過速或高血壓風暴。"
    },
    "hcm": {
        "avoid": ["acepromazine"],
        "reason": "HCM 禁忌：避免使用 Acepromazine，其血管舒張作用會惡化左心室流出道阻塞 (LVOT obstruction)。"
    },
    "ckd": {
        "avoid": ["nsaids"],
        "warning": "CKD 警示：嚴禁使用 NSAIDs。輸液需採保守滴定 (Conservative titration)。",
        "adjust_fluids": 0.6  # Reduce maintenance fluid rate to 60%
    },
    "seizure": {
        "avoid": ["acepromazine", "ketamine", "ketamine_combo_low"],
        "reason": "癲癇病史：避免使用可能降低癲癇閾值的藥物。"
    },
    "liver_failure": {
        "reduce_dose": 0.5,
        "reason": "肝功能不全：建議劑量減半以應對代謝緩慢。"
    }
}

# ---------------------------------------------------------------------------
# Drug database (Restored from origin/main)
# ---------------------------------------------------------------------------

@dataclass
class DrugDose:
    drug: str
    low_dose: float
    high_dose: float
    unit: str
    routes: str
    concentration_mg_per_mL: Optional[float]
    notes: str
    source: str
    category: str  # premedication, induction, maintenance, emergency, analgesic, local_block, reversal, fluid

# Species-specific drug databases (COMPLETE DATA FROM MAIN)
FELINE_DRUGS = [
    # --- Premedication: Opioids ---
    DrugDose("buprenorphine", 0.01, 0.02, "mg/kg", "IM, IV", 0.3, "Duration 4-6h. May antagonize other mu-agonists", "AAFP 2020 Table 7", "premedication"),
    DrugDose("butorphanol", 0.1, 0.4, "mg/kg", "IM, IV", 10.0, "Duration 60-90 min. Good sedation, short-acting", "AAFP 2020 Table 7", "premedication"),
    DrugDose("methadone", 0.2, 0.5, "mg/kg", "IM, IV", 10.0, "Duration 2-4h. Moderate sedation", "AAFP 2020 Table 7", "premedication"),
    DrugDose("hydromorphone", 0.02, 0.1, "mg/kg", "IM, IV", 2.0, "Duration 2-4h. Higher doses: dysphoria risk", "AAFP 2020 Table 7", "premedication"),
    DrugDose("fentanyl", 2.0, 5.0, "µg/kg", "IV", 0.05, "Short duration. Minimal sedation", "AAFP 2020 Table 7", "premedication"),
    DrugDose("morphine", 0.1, 0.3, "mg/kg", "IM, IV", 10.0, "Duration 2-4h", "AAFP 2020 Table 7", "premedication"),
    DrugDose("meperidine", 2.0, 5.0, "mg/kg", "IM only", 50.0, "Short duration 60-90 min. IM ONLY", "AAFP 2020 Table 7", "premedication"),

    # --- Premedication: Sedatives ---
    DrugDose("acepromazine", 0.01, 0.05, "mg/kg", "SC, IM", 10.0, "Inconsistent in cats. Peak 20-30 min, lasts 4-6h. Avoid if hypotensive", "AAFP 2020", "premedication"),
    DrugDose("dexmedetomidine", 0.005, 0.02, "mg/kg", "IM, IV", 0.5, "Potent sedation. Reversible with atipamezole. Bradycardia expected", "AAFP 2020 Table 5", "premedication"),
    DrugDose("midazolam", 0.2, 0.5, "mg/kg", "IM, IV", 5.0, "Minimal cardiovascular effects. Good for debilitated patients", "AAFP 2020", "premedication"),

    # --- Premedication: Combinations ---
    DrugDose("ketamine_combo_low", 2.0, 3.0, "mg/kg", "IM, IV", 100.0, "With opioid + dexmedetomidine. Low dose in combo", "AAFP 2020 Table 5", "premedication"),
    DrugDose("alfaxalone_combo", 1.0, 2.0, "mg/kg", "IM, IV", 10.0, "With opioid + dexmedetomidine. High end may anesthetize", "AAFP 2020 Table 5", "premedication"),

    # --- Induction ---
    DrugDose("propofol", 4.0, 8.0, "mg/kg", "IV only", 10.0, "Titrate to effect. Co-induction with midazolam reduces dose needed", "AAFP 2020 Table 9", "induction"),
    DrugDose("alfaxalone", 1.0, 4.0, "mg/kg", "IV, IM", 10.0, "Co-induction with midazolam reduces dose. IM may need split injection", "AAFP 2020 Table 9", "induction"),
    DrugDose("ketamine", 5.0, 10.0, "mg/kg", "IV, IM", 100.0, "Usually combined with midazolam or dexmedetomidine", "AAFP 2020 Table 9", "induction"),

    # --- Maintenance CRI ---
    DrugDose("fentanyl_cri", 0.1, 0.4, "µg/kg/min", "IV CRI", 0.05, "CRI for intraoperative analgesia", "AAFP 2020 Table 10", "maintenance"),
    DrugDose("remifentanil_cri", 0.1, 0.4, "µg/kg/min", "IV CRI", 0.05, "Very short half-life. Ensure opioid dose at end of procedure", "AAFP 2020 Table 10", "maintenance"),
    DrugDose("ketamine_cri", 2.0, 20.0, "µg/kg/min", "IV CRI", 100.0, "Analgesic adjunct. Reduces inhalant requirement", "AAFP 2020 Table 10", "maintenance"),
    DrugDose("esmolol_cri", 100.0, 200.0, "µg/kg/min", "IV CRI", 10.0, "After loading dose. For HCM tachycardia", "AAFP 2020", "maintenance"),

    # --- Emergency ---
    DrugDose("atropine", 0.04, 0.04, "mg/kg", "IV, IM", 0.54, "Anticholinergic. For bradycardia", "AAFP 2020 Table 12", "emergency"),
    DrugDose("epinephrine", 0.01, 0.01, "mg/kg", "IV", 1.0, "Initial low dose. For cardiac arrest / severe hypotension", "AAFP 2020 Table 12", "emergency"),
    DrugDose("glycopyrrolate", 0.005, 0.01, "mg/kg", "IV, IM", 0.2, "Anticholinergic. Less tachycardia than atropine", "AAFP 2020 Table 12", "emergency"),
    DrugDose("lidocaine_emergency", 0.25, 0.25, "mg/kg", "IV", 20.0, "CATS: low dose only! Sensitive to lidocaine toxicity", "AAFP 2020 Table 12", "emergency"),
    DrugDose("esmolol_loading", 0.1, 0.5, "mg/kg", "IV slow", 10.0, "Loading dose over 1 min. For HCM tachycardia", "AAFP 2020", "emergency"),

    # --- Reversal ---
    DrugDose("atipamezole", 0.005, 0.02, "mg/kg", "IM", 5.0, "Reversal for dexmedetomidine. Same volume as dexmedetomidine given", "AAFP 2020", "reversal"),
    DrugDose("naloxone", 0.05, 0.05, "mg/kg", "IV, IM", 0.4, "Opioid reversal. Reverses ALL opioid effects including analgesia", "AAFP 2020 Table 12", "reversal"),

    # --- Local blocks ---
    DrugDose("bupivacaine_local", 1.0, 1.0, "mg/kg", "Local", 5.0, "Max dose for cats. For splash block: dilute to 0.4-0.6 mL/kg total vol", "AAHA 2020", "local_block"),
    DrugDose("lidocaine_local", 2.0, 4.0, "mg/kg", "Local", 20.0, "Max dose for cats", "AAHA 2020", "local_block"),
    DrugDose("ropivacaine_local", 1.0, 1.0, "mg/kg", "Local", 5.0, "Max dose for cats", "AAHA 2020", "local_block"),

    # --- Fluids ---
    DrugDose("crystalloid_bolus", 5.0, 10.0, "mL/kg", "IV", None, "Bolus for hypotension. Cats: use lower end. Reassess after each bolus", "AAHA 2020", "fluid"),
    DrugDose("crystalloid_maintenance", 3.0, 5.0, "mL/kg/h", "IV", None, "Intraoperative maintenance rate", "AAHA 2020", "fluid"),
]

CANINE_DRUGS = [
    # --- Premedication: Opioids ---
    DrugDose("buprenorphine", 0.01, 0.02, "mg/kg", "IM, IV", 0.3, "Duration 4-6h", "AAHA 2020", "premedication"),
    DrugDose("butorphanol", 0.1, 0.4, "mg/kg", "IM, IV", 10.0, "Duration 60-90 min. Good sedation", "AAHA 2020", "premedication"),
    DrugDose("methadone", 0.2, 0.5, "mg/kg", "IM, IV", 10.0, "Duration 2-4h", "AAHA 2020", "premedication"),
    DrugDose("hydromorphone", 0.05, 0.1, "mg/kg", "IM, IV", 2.0, "Duration 2-4h", "AAHA 2020", "premedication"),
    DrugDose("fentanyl", 2.0, 5.0, "µg/kg", "IV", 0.05, "Short duration", "AAHA 2020", "premedication"),
    DrugDose("morphine", 0.2, 0.5, "mg/kg", "IM", 10.0, "Duration 2-4h. IM preferred in dogs", "AAHA 2020", "premedication"),
    DrugDose("meperidine", 3.0, 5.0, "mg/kg", "IM only", 50.0, "Short duration. IM ONLY", "AAHA 2020", "premedication"),

    # --- Premedication: Sedatives ---
    DrugDose("acepromazine", 0.01, 0.05, "mg/kg", "SC, IM", 10.0, "Peak 20-30 min, lasts 4-6h. Max 1 mg total for large dogs. Avoid if hypotensive", "AAHA 2020", "premedication"),
    DrugDose("dexmedetomidine", 0.005, 0.02, "mg/kg", "IM, IV", 0.5, "Potent sedation. Reversible. Bradycardia expected", "AAHA 2020", "premedication"),
    DrugDose("midazolam", 0.2, 0.5, "mg/kg", "IM, IV", 5.0, "Minimal CV effects. Good for debilitated patients", "AAHA 2020", "premedication"),

    # --- Induction ---
    DrugDose("propofol", 2.0, 6.0, "mg/kg", "IV only", 10.0, "Titrate to effect. Lower dose after premedication", "AAHA 2020", "induction"),
    DrugDose("alfaxalone", 1.0, 3.0, "mg/kg", "IV", 10.0, "Titrate to effect", "AAHA 2020", "induction"),
    DrugDose("ketamine", 5.0, 10.0, "mg/kg", "IV, IM", 100.0, "Usually combined with midazolam", "AAHA 2020", "induction"),

    # --- Maintenance CRI ---
    DrugDose("fentanyl_cri", 0.1, 0.4, "µg/kg/min", "IV CRI", 0.05, "Intraoperative analgesia", "AAHA 2020", "maintenance"),
    DrugDose("ketamine_cri", 2.0, 20.0, "µg/kg/min", "IV CRI", 100.0, "Analgesic adjunct", "AAHA 2020", "maintenance"),
    DrugDose("lidocaine_cri", 25.0, 50.0, "µg/kg/min", "IV CRI", 20.0, "Dogs only. NOT for cats. Analgesic adjunct", "AAHA 2020", "maintenance"),

    # --- Emergency ---
    DrugDose("atropine", 0.04, 0.04, "mg/kg", "IV, IM", 0.54, "For bradycardia", "AAHA 2020", "emergency"),
    DrugDose("epinephrine", 0.01, 0.01, "mg/kg", "IV", 1.0, "Low dose. For cardiac arrest / severe hypotension", "AAHA 2020", "emergency"),
    DrugDose("glycopyrrolate", 0.005, 0.01, "mg/kg", "IV, IM", 0.2, "Anticholinergic", "AAHA 2020", "emergency"),
    DrugDose("lidocaine_emergency", 1.0, 2.0, "mg/kg", "IV slow", 20.0, "For ventricular arrhythmias. Dogs tolerate higher doses than cats", "AAHA 2020", "emergency"),

    # --- Reversal ---
    DrugDose("atipamezole", 0.005, 0.02, "mg/kg", "IM", 5.0, "Reversal for dexmedetomidine", "AAHA 2020", "reversal"),
    DrugDose("naloxone", 0.01, 0.04, "mg/kg", "IV, IM", 0.4, "Opioid reversal", "AAHA 2020", "reversal"),

    # --- Local blocks ---
    DrugDose("bupivacaine_local", 2.0, 2.0, "mg/kg", "Local", 5.0, "Max dose for dogs", "AAHA 2020", "local_block"),
    DrugDose("lidocaine_local", 4.0, 6.0, "mg/kg", "Local", 20.0, "Max dose for dogs", "AAHA 2020", "local_block"),
    DrugDose("ropivacaine_local", 2.0, 2.0, "mg/kg", "Local", 5.0, "Max dose for dogs", "AAHA 2020", "local_block"),

    # --- Fluids ---
    DrugDose("crystalloid_bolus", 10.0, 20.0, "mL/kg", "IV", None, "Bolus for hypotension. Reassess after each bolus", "AAHA 2020", "fluid"),
    DrugDose("crystalloid_maintenance", 5.0, 10.0, "mL/kg/h", "IV", None, "Intraoperative maintenance rate", "AAHA 2020", "fluid"),
]

def calculate_dose(drug: DrugDose, weight_kg: float, reduction: float = 1.0) -> dict:
    low = drug.low_dose * reduction
    high = drug.high_dose * reduction
    result = {
        "drug": drug.drug, "category": drug.category, "unit": drug.unit, "routes": drug.routes,
        "dose_range": f"{round(low,4)}-{round(high,4)} {drug.unit}", "notes": drug.notes, "source": drug.source,
        "is_contraindicated": False, "warning": ""
    }
    if drug.unit == "mg/kg":
        l_mg, h_mg = round(low*weight_kg,4), round(high*weight_kg,4)
        result.update({"calculated_range": f"{l_mg}-{h_mg} mg"})
        if drug.concentration_mg_per_mL:
            result["volume_range"] = f"{round(l_mg/drug.concentration_mg_per_mL,3)}-{round(h_mg/drug.concentration_mg_per_mL,3)} mL"
    elif drug.unit == "µg/kg":
        l_ug, h_ug = round(low*weight_kg,4), round(high*weight_kg,4)
        result.update({"calculated_range": f"{l_ug}-{h_ug} µg"})
        if drug.concentration_mg_per_mL:
            result["volume_range"] = f"{round((l_ug/1000)/drug.concentration_mg_per_mL,3)}-{round((h_ug/1000)/drug.concentration_mg_per_mL,3)} mL"
    elif drug.unit in ("µg/kg/min", "mL/kg/h", "mL/kg"):
        l_v, h_v = round(low*weight_kg,4), round(high*weight_kg,4)
        unit_map = {"µg/kg/min": "µg/min", "mL/kg/h": "mL/h", "mL/kg": "mL"}
        result["calculated_range"] = f"{l_v}-{h_v} {unit_map[drug.unit]}"
    return result

def calculate_all(weight: float, species: str, asa: int, comorbidities: List[str], cats: List[str]=None, drug_filter: List[str]=None) -> dict:
    db = FELINE_DRUGS if species == "cat" else CANINE_DRUGS
    res = {"patient": {"weight": weight, "species": species, "asa": asa, "comorbidities": comorbidities}, "drugs": {}}
    global_red = 0.75 if asa >= 4 else 1.0
    for d in db:
        if cats and d.category not in cats: continue
        if drug_filter and not any(f.lower() in d.drug.lower() for f in drug_filter): continue
        red, warn, is_avoid = global_red, "", False
        for cm in comorbidities:
            if cm in CONTRAINDICATIONS:
                p = CONTRAINDICATIONS[cm]
                if d.drug in p.get("avoid", []): is_avoid, warn = True, p["reason"]
                if "reduce_dose" in p: red *= p["reduce_dose"]
                if "warning" in p and d.category == "fluid": warn = p["warning"]
                if "adjust_fluids" in p and d.category == "fluid": red *= p["adjust_fluids"]
        calc = calculate_dose(d, weight, red)
        calc["is_contraindicated"], calc["warning"] = is_avoid, warn
        if d.category not in res["drugs"]: res["drugs"][d.category] = []
        res["drugs"][d.category].append(calc)
    return res

def format_output(results: dict) -> str:
    lines = [f"# Drug Dose Sheet: {results['patient']['species'].upper()} {results['patient']['weight']} kg (ASA {results['patient']['asa']})", ""]
    if results['patient']['comorbidities']:
        lines.append(f"**Comorbidities**: {', '.join(results['patient']['comorbidities'])}")
        lines.append("")
    order = ["premedication", "induction", "maintenance", "local_block", "fluid", "emergency", "reversal"]
    for cat in order:
        if cat not in results["drugs"]: continue
        lines.append(f"## {cat.capitalize()} {'(⚠️ CONTAINS CONTRAINDICATIONS)' if any(d['is_contraindicated'] for d in results['drugs'][cat]) else ''}")
        lines.append("| Drug | Calculated | Volume | Warning | Notes |")
        lines.append("|------|------------|--------|---------|-------|")
        for d in results["drugs"][cat]:
            indicator = "❌ " if d["is_contraindicated"] else ""
            warn = d["warning"] if d["warning"] else "-"
            lines.append(f"| {indicator}{d['drug']} | {d.get('calculated_range','-')} | {d.get('volume_range','-')} | {warn} | {d['notes']} |")
        lines.append("")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weight", type=float, required=True)
    parser.add_argument("--species", required=True)
    parser.add_argument("--asa", type=int, default=2)
    parser.add_argument("--comorbidities", type=str, default="")
    parser.add_argument("--category", type=str)
    parser.add_argument("--drugs", type=str)
    parser.add_argument("--format", default="table")
    args = parser.parse_args()
    comorbs = [c.strip().lower() for c in args.comorbidities.split(",")] if args.comorbidities else []
    cats = [c.strip() for c in args.category.split(",")] if args.category else None
    d_filter = [d.strip() for d in args.drugs.split(",")] if args.drugs else None
    results = calculate_all(args.weight, args.species, args.asa, comorbs, cats, d_filter)
    if args.format == "json": print(json.dumps(results, indent=2, ensure_ascii=False))
    else: print(format_output(results))

if __name__ == "__main__":
    main()
