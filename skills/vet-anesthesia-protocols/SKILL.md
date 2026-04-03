---
name: vet-anesthesia-protocols
description: Generate individualized, patient-specific veterinary anesthesia protocols as printable OR checklists. Use this skill when the user provides patient details (species, weight, age, breed, ASA status, procedure, comorbidities) and wants a complete anesthesia plan — including premedication, induction, maintenance, monitoring plan, fluid therapy, local/regional blocks, emergency drugs, and recovery. Also trigger when the user asks for an "anesthesia protocol", "anesthesia plan", "anesthesia checklist", "drug sheet", or "麻醉計畫" / "麻醉方案". This skill generates actionable plans with calculated drug doses, NOT general guideline recommendations (that is the clinical-guidelines skill). Even if the user just gives a brief case description like "5kg dog OHE", generate the full protocol.
agent: vet-ai-assistant
---

# Veterinary Anesthesia Protocol Generator

You are generating an individualized anesthesia protocol that a veterinarian will print and bring into the operating room. Accuracy is critical — a wrong drug dose can harm or kill a patient. This is why all dose calculations are performed by a Python script, not by you.

## Target Audience

Licensed veterinarian. Use professional terminology. Output in 繁體中文 by default, but keep all drug names, medical abbreviations, units, and technical terms in English (e.g., dexmedetomidine, ETCO2, MAP, ASA III).

## Workflow

### Step 1: Gather Patient Information

You need these parameters to generate a protocol. If the user hasn't provided them, ask — but generate with what you have rather than blocking on missing non-critical info.

**Required:**
- Species (dog / cat)
- Body weight (kg)
- Procedure type

**Important but can infer/default:**
- ASA status (default: II if not stated)
- Age
- Breed
- Known comorbidities

### Step 2: Run the Dose Calculator

Execute the Python script to get precise, guideline-sourced drug doses. This is non-negotiable — the script exists because drug dose accuracy is a patient safety issue. Run it with Bash:

```bash
python3 /Users/Jung/.claude/skills/anesthesia-protocols/scripts/dose_calculator.py --weight <kg> --species <cat|dog> --asa <1-5> --format json
```

Use the **absolute path** above (do not use `<skill-path>` — it won't resolve). The script returns all drug categories with calculated doses and volumes. Use these numbers directly — never calculate doses yourself or round the script's output.

If Bash is unavailable (permission denied), tell the user: "dose_calculator.py 無法執行，請確認 Bash 權限設定" and stop. Do not attempt to calculate doses manually.

### Step 3: Consult Guidelines for Clinical Context

Read the relevant reference files from the clinical-guidelines skill for patient-specific considerations. These are at:

```
/Users/Jung/.claude/skills/clinical-guidelines/references/
├── aafp_2020.md   (feline-specific)
├── aaha_2020.md   (dogs & cats, full continuum)
└── acvaa_2025.md  (monitoring standards 2025)
```

**Be token-efficient**: only read the file(s) relevant to the case.
- Cat case → `aafp_2020.md` + `acvaa_2025.md` (monitoring)
- Dog case → `aaha_2020.md` + `acvaa_2025.md` (monitoring)
- Only read `aaha_2020.md` for a cat if you need complication algorithms or local block techniques not covered in AAFP

Use the guidelines to:
- Adjust drug choices based on comorbidities (e.g., avoid acepromazine in HCM cats, use midazolam for debilitated patients)
- Select appropriate monitoring parameters for ASA status
- Add procedure-specific notes (e.g., dental → dental nerve blocks, orthopedic → aggressive analgesia)
- Identify contraindicated drugs

### Step 4: Generate the Protocol

Assemble the checklist using the template below. Select specific drugs from the calculator output based on clinical judgment from Step 3. Present dose ranges AND a recommended starting dose where appropriate.

## Protocol Template

The output should follow this structure exactly. This is what the clinician prints and carries to the OR.

---

```
═══════════════════════════════════════════════
  麻醉計畫 Anesthesia Protocol
═══════════════════════════════════════════════

📋 Patient Information
───────────────────────────────────────────────
Species/Breed:
Age:          Sex:          Weight:     kg
Procedure:
ASA Status:
Comorbidities:
Date:                       Anesthetist:

═══════════════════════════════════════════════

1️⃣ PREANESTHETIC CHECKLIST
───────────────────────────────────────────────
□ Physical exam completed
□ Bloodwork reviewed (CBC, biochem, ± coag)
□ Fasting confirmed: ____ hours (food) / ____ hours (water)
□ IV catheter placed: ____ G, site: ________
□ Fluid type: ____________  Rate: ____ mL/h
□ Emergency drugs calculated (see Section 7)
□ Monitoring equipment checked
□ [Add case-specific items]

2️⃣ PREMEDICATION
───────────────────────────────────────────────
Time: ____    Route: ____

Drug                  Dose        Volume      ✓
─────────────────────────────────────────────
[Drug 1]              ___ mg      ___ mL      □
[Drug 2]              ___ mg      ___ mL      □
[Drug 3 if needed]    ___ mg      ___ mL      □

Wait ____ min before induction
Notes: [clinical rationale for drug selection]

3️⃣ INDUCTION
───────────────────────────────────────────────
Drug                  Dose        Volume      ✓
─────────────────────────────────────────────
[Induction agent]     ___ mg      ___ mL      □
± [Co-induction]      ___ mg      ___ mL      □

□ Preoxygenate 3-5 min before induction
□ Titrate to effect (give ¼ dose increments q30s)
□ Intubate: ETT size ____ (have ±0.5 ready)
□ Cuff check
□ Connect to breathing circuit: □ NRC / □ RC
□ Connect capnograph + SpO2

4️⃣ MAINTENANCE
───────────────────────────────────────────────
□ Inhalant: □ Isoflurane / □ Sevoflurane
  Target vaporizer: ____% (adjust to effect)

CRI (if applicable):
Drug                  Rate                    ✓
─────────────────────────────────────────────
[CRI drug]            ___ µg/kg/min           □

5️⃣ LOCAL / REGIONAL ANALGESIA
───────────────────────────────────────────────
Block type: ________________
Drug                  Dose        Volume      ✓
─────────────────────────────────────────────
[Local anesthetic]    ___ mg      ___ mL      □

Notes: [technique, landmarks, timing]

6️⃣ MONITORING PLAN (per ACVAA 2025)
───────────────────────────────────────────────
Parameter         Frequency    Target Range
─────────────────────────────────────────────
HR                q5 min       ___-___ bpm
BP (MAP)          q5 min       60-100 mmHg
SpO2              continuous   ≥ 95%
ETCO2             continuous   35-55 mmHg
Temperature       q15 min      ≥ 37.8°C
ECG               continuous   Normal sinus
Reflexes          q5 min       [specify]
□ Dedicated anesthetist assigned
□ Anesthesia record prepared (record q5 min)

7️⃣ EMERGENCY DRUGS (pre-calculated)
───────────────────────────────────────────────
Drug              Dose         Volume     Route
─────────────────────────────────────────────
Atropine          ___ mg       ___ mL     IV
Glycopyrrolate    ___ mg       ___ mL     IV/IM
Epinephrine       ___ mg       ___ mL     IV
[Species-specific emergency drugs]

Crystalloid bolus: ___ mL (___mL/kg)
□ Drawn up and labeled before induction

8️⃣ RECOVERY
───────────────────────────────────────────────
□ Continue SpO2 + ETCO2 until extubation
□ Extubate when swallow reflex returns
□ Continue temperature monitoring q30 min
□ Supplemental O2 available
□ Pain assessment: ____ min post-extubation
□ Reversal agents (if needed):
  [Drug]            ___ mg       ___ mL     □

Recovery analgesia:
Drug              Dose         Route       Timing
─────────────────────────────────────────────
[Analgesic]       ___ mg       ___         q___h

9️⃣ CASE-SPECIFIC NOTES
───────────────────────────────────────────────
[Comorbidity-driven considerations, procedure-
 specific tips, guideline citations]

═══════════════════════════════════════════════
  Generated from: AAFP 2020 / AAHA 2020 / ACVAA 2025
═══════════════════════════════════════════════
```

## Clinical Decision Rules

When selecting drugs from the calculator output, apply these principles:

### Comorbidity-Driven Adjustments
- **HCM (cats)**: Avoid acepromazine (vasodilation worsens outflow obstruction). Prefer opioid + midazolam or low-dose dexmedetomidine. Have esmolol ready. Minimize stress. Avoid aggressive fluid loading.
- **Renal disease**: Avoid NSAIDs. Use opioid-heavy protocols. Careful fluid management. Avoid prolonged hypotension.
- **Hyperthyroidism (cats)**: Avoid ketamine (sympathomimetic). Prefer alfaxalone or propofol induction.
- **Brachycephalic**: Preoxygenate aggressively. Have multiple ETT sizes. Consider shorter-acting agents. Delay extubation until strong swallow.
- **Geriatric (>8 yr dog, >10 yr cat)**: Reduce doses 25-50%. Longer monitoring. More aggressive warming.
- **Pediatric (<6 mo)**: Risk of hypoglycemia — check BG. Smaller drug volumes. Immature hepatic metabolism.

### Procedure-Driven Additions
- **Dental**: Add dental nerve blocks (infraorbital, inferior alveolar, mental). Ensure NSAIDs if no renal contraindication.
- **Orthopedic**: Aggressive multimodal analgesia. Consider epidural or regional blocks. CRI for intraop pain.
- **Soft tissue / abdominal**: Consider intraperitoneal splash block with local anesthetic.
- **Ophthalmic**: Avoid ketamine (increases IOP). Ensure stable plane.

### ASA Status Adjustments
- **ASA I-II**: Standard protocols. Full monitoring per ACVAA 2025 minimum.
- **ASA III**: Reduce doses. Consider arterial line / invasive monitoring. Have vasopressors drawn up.
- **ASA IV-V**: Minimal sedation doses. Opioid + benzodiazepine preferred. Maximum monitoring. ICU recovery.

## Important Reminders

- Every dose number in the protocol must come from the dose_calculator.py output. If a drug isn't in the calculator, state the dose range from the guideline with a citation and flag it clearly.
- The protocol is a starting point. Always include a note that doses should be titrated to effect.
- When the user provides follow-up info (e.g., "actually the cat is also diabetic"), regenerate the affected sections rather than starting from scratch.
- **Cite guideline sources throughout the protocol** — not just in Section 9. Each clinical decision (drug selection, contraindication, monitoring parameter, block technique) should have an inline citation like "(AAFP 2020)" or "(ACVAA 2025 Table 1)". This is what separates a guideline-backed protocol from generic advice. The clinician needs to know *why* you chose each drug and *where* the recommendation comes from.
