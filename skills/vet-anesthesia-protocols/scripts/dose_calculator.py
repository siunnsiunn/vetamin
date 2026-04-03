#!/usr/bin/env python3
"""
Veterinary Anesthesia Drug Dose Calculator

Calculates patient-specific drug doses based on body weight.
All dose ranges come from AAFP 2020, AAHA 2020, and ACVAA 2025 guidelines.

Usage:
    python dose_calculator.py --weight 4.5 --species cat --asa 2
    python dose_calculator.py --weight 25 --species dog --asa 3
    python dose_calculator.py --weight 4.5 --species cat --drugs "dexmedetomidine,ketamine,alfaxalone"
    python dose_calculator.py --weight 4.5 --species cat --category emergency
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional

# ---------------------------------------------------------------------------
# Drug database
# Each entry: (low_dose, high_dose, unit, routes, concentration_mg_per_mL, notes, source, category)
# concentration_mg_per_mL is the common commercial concentration for volume calc
# For µg/kg drugs, doses are stored as µg/kg and unit="µg/kg"
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

# Species-specific drug databases
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

    # --- Emergency ---
    DrugDose("atropine", 0.04, 0.04, "mg/kg", "IV, IM", 0.54, "Anticholinergic. For bradycardia", "AAFP 2020 Table 12", "emergency"),
    DrugDose("epinephrine", 0.01, 0.01, "mg/kg", "IV", 1.0, "Initial low dose. For cardiac arrest / severe hypotension", "AAFP 2020 Table 12", "emergency"),
    DrugDose("glycopyrrolate", 0.005, 0.01, "mg/kg", "IV, IM", 0.2, "Anticholinergic. Less tachycardia than atropine", "AAFP 2020 Table 12", "emergency"),
    DrugDose("lidocaine_emergency", 0.25, 0.25, "mg/kg", "IV", 20.0, "CATS: low dose only! Sensitive to lidocaine toxicity", "AAFP 2020 Table 12", "emergency"),

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

    # --- HCM-specific ---
    DrugDose("esmolol_loading", 0.1, 0.5, "mg/kg", "IV slow", 10.0, "Loading dose over 1 min. For HCM tachycardia", "AAFP 2020", "emergency"),
    DrugDose("esmolol_cri", 100.0, 200.0, "µg/kg/min", "IV CRI", 10.0, "After loading dose. For HCM tachycardia", "AAFP 2020", "maintenance"),
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

# Additional drugs for specific scenarios
SPECIAL_DRUGS = {
    "terbutaline_cat_asthma": DrugDose("terbutaline", 0.01, 0.01, "mg/kg", "SC", 1.0, "For asthmatic cats before anesthesia. Onset 15-30 min SC", "AAFP 2020", "premedication"),
}


def get_drug_db(species: str) -> list:
    if species == "cat":
        return FELINE_DRUGS
    elif species == "dog":
        return CANINE_DRUGS
    else:
        raise ValueError(f"Unknown species: {species}. Use 'cat' or 'dog'.")


def calculate_dose(drug: DrugDose, weight_kg: float) -> dict:
    """Calculate actual doses and volumes for a given drug and weight."""
    result = {
        "drug": drug.drug,
        "category": drug.category,
        "unit": drug.unit,
        "routes": drug.routes,
        "dose_range": f"{drug.low_dose}-{drug.high_dose} {drug.unit}",
        "notes": drug.notes,
        "source": drug.source,
    }

    if drug.unit == "mg/kg":
        low_mg = round(drug.low_dose * weight_kg, 4)
        high_mg = round(drug.high_dose * weight_kg, 4)
        result["calculated_low_mg"] = low_mg
        result["calculated_high_mg"] = high_mg
        result["calculated_range"] = f"{low_mg}-{high_mg} mg"
        if drug.concentration_mg_per_mL:
            low_mL = round(low_mg / drug.concentration_mg_per_mL, 3)
            high_mL = round(high_mg / drug.concentration_mg_per_mL, 3)
            result["volume_low_mL"] = low_mL
            result["volume_high_mL"] = high_mL
            result["volume_range"] = f"{low_mL}-{high_mL} mL (concentration: {drug.concentration_mg_per_mL} mg/mL)"

    elif drug.unit == "µg/kg":
        low_ug = round(drug.low_dose * weight_kg, 4)
        high_ug = round(drug.high_dose * weight_kg, 4)
        result["calculated_low_µg"] = low_ug
        result["calculated_high_µg"] = high_ug
        result["calculated_range"] = f"{low_ug}-{high_ug} µg"
        if drug.concentration_mg_per_mL:
            # Convert µg to mg for volume calc
            low_mL = round((low_ug / 1000) / drug.concentration_mg_per_mL, 3)
            high_mL = round((high_ug / 1000) / drug.concentration_mg_per_mL, 3)
            result["volume_low_mL"] = low_mL
            result["volume_high_mL"] = high_mL
            result["volume_range"] = f"{low_mL}-{high_mL} mL (concentration: {drug.concentration_mg_per_mL} mg/mL)"

    elif drug.unit in ("µg/kg/min", "mL/kg/h", "mL/kg"):
        low_val = round(drug.low_dose * weight_kg, 4)
        high_val = round(drug.high_dose * weight_kg, 4)
        if drug.unit == "µg/kg/min":
            result["calculated_range"] = f"{low_val}-{high_val} µg/min"
        elif drug.unit == "mL/kg/h":
            result["calculated_range"] = f"{low_val}-{high_val} mL/h"
        elif drug.unit == "mL/kg":
            result["calculated_range"] = f"{low_val}-{high_val} mL"

    return result


def calculate_all(weight_kg: float, species: str, asa: int = 2,
                  categories: list = None, drug_filter: list = None) -> dict:
    """Calculate all relevant drug doses for a patient."""
    db = get_drug_db(species)

    results = {
        "patient": {
            "weight_kg": weight_kg,
            "species": species,
            "asa_status": asa,
        },
        "drugs": {},
    }

    for drug in db:
        # Filter by category if specified
        if categories and drug.category not in categories:
            continue
        # Filter by drug name if specified
        if drug_filter and not any(f.lower() in drug.drug.lower() for f in drug_filter):
            continue

        calc = calculate_dose(drug, weight_kg)
        cat = drug.category
        if cat not in results["drugs"]:
            results["drugs"][cat] = []
        results["drugs"][cat].append(calc)

    return results


def format_output(results: dict) -> str:
    """Format results as a readable table for the skill to incorporate."""
    lines = []
    patient = results["patient"]
    lines.append(f"# Drug Dose Sheet: {patient['species'].upper()} {patient['weight_kg']} kg (ASA {patient['asa_status']})")
    lines.append("")

    category_order = ["premedication", "induction", "maintenance", "analgesic",
                      "local_block", "fluid", "emergency", "reversal"]

    category_labels = {
        "premedication": "Premedication",
        "induction": "Induction",
        "maintenance": "Maintenance / CRI",
        "analgesic": "Analgesics",
        "local_block": "Local / Regional Blocks",
        "fluid": "Fluid Therapy",
        "emergency": "Emergency Drugs",
        "reversal": "Reversal Agents",
    }

    for cat in category_order:
        if cat not in results["drugs"]:
            continue
        drugs = results["drugs"][cat]
        lines.append(f"## {category_labels.get(cat, cat)}")
        lines.append("")
        lines.append("| Drug | Dose Range | Calculated | Volume | Route | Notes |")
        lines.append("|------|-----------|------------|--------|-------|-------|")
        for d in drugs:
            vol = d.get("volume_range", d.get("calculated_range", "-"))
            calc = d.get("calculated_range", "-")
            lines.append(f"| {d['drug']} | {d['dose_range']} | {calc} | {vol} | {d['routes']} | {d['notes']} |")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Veterinary Anesthesia Drug Dose Calculator")
    parser.add_argument("--weight", type=float, required=True, help="Patient weight in kg")
    parser.add_argument("--species", choices=["cat", "dog"], required=True, help="Species")
    parser.add_argument("--asa", type=int, default=2, choices=[1, 2, 3, 4, 5], help="ASA status (default: 2)")
    parser.add_argument("--category", type=str, help="Filter by category (comma-separated): premedication,induction,maintenance,emergency,reversal,local_block,fluid")
    parser.add_argument("--drugs", type=str, help="Filter by drug names (comma-separated)")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")

    args = parser.parse_args()

    categories = [c.strip() for c in args.category.split(",")] if args.category else None
    drug_filter = [d.strip() for d in args.drugs.split(",")] if args.drugs else None

    results = calculate_all(args.weight, args.species, args.asa, categories, drug_filter)

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(format_output(results))


if __name__ == "__main__":
    main()
