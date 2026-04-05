import os
import sys
import subprocess
import json
import tempfile
import shutil
from datetime import datetime

# Dynamic root discovery
_current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = None
while True:
    if os.path.exists(os.path.join(_current_dir, 'core')):
        PROJECT_ROOT = _current_dir
        if PROJECT_ROOT not in sys.path:
            sys.path.insert(0, PROJECT_ROOT)
        break
    parent = os.path.dirname(_current_dir)
    if parent == _current_dir:
        break
    _current_dir = parent

if not PROJECT_ROOT:
    print("Error: Could not find project root (containing 'core' folder).")
    sys.exit(1)

def run_command(cmd, cwd=PROJECT_ROOT, env=None):
    """Helper to run shell commands and return results."""
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    
    # REMOVED: PYTHONPATH injection. Scripts must self-bootstrap.

    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        env=full_env
    )
    return result

def test_system_integration():
    print(f"=== Vetamin System Integration Test Suite ===")
    
    # 1. Environment Handling [Fix Finding P2]
    # Respect existing override or create a temp one
    external_override = os.getenv("VET_DIR_OVERRIDE")
    is_temp = False
    if external_override:
        test_vet_dir = external_override
        print(f"[Env] Using external VET_DIR_OVERRIDE: {test_vet_dir}")
    else:
        test_vet_dir = tempfile.mkdtemp(prefix="vet_integration_")
        os.environ["VET_DIR_OVERRIDE"] = test_vet_dir
        is_temp = True
        print(f"[Env] Using temporary sandbox: {test_vet_dir}")

    try:
        # 2. Core: Data Manager CLI [Fix Finding P2 Coverage]
        print("\n[Step 1] Testing core/data_manager.py CLI...")
        # Init
        res = run_command([sys.executable, "core/data_manager.py", "init"])
        if res.returncode != 0: raise Exception(f"Init failed: {res.stderr}")
        
        # Update (Nested path)
        res = run_command([sys.executable, "core/data_manager.py", "update", "patient.name", "Codex-Tester"])
        if res.returncode != 0: raise Exception(f"Update failed: {res.stderr}")
        
        # Get
        res = run_command([sys.executable, "core/data_manager.py", "get", "patient.name"])
        if res.stdout.strip() != "Codex-Tester": 
            raise Exception(f"Get failed. Expected 'Codex-Tester', got '{res.stdout.strip()}'")
        print("✓ Core Data Manager CLI functional.")

        # 3. Skill: Pain Engine (Path Robustness & Schema Alignment)
        print("\n[Step 2] Testing skills/vet-pain-score/scripts/score_pain_engine.py...")
        # Run from its own directory [Fix Finding P3]
        pain_script_dir = os.path.join(PROJECT_ROOT, "skills/vet-pain-score/scripts")
        res = run_command([sys.executable, "score_pain_engine.py", "fgs", "2", "3"], cwd=pain_script_dir)
        if res.returncode != 0: raise Exception(f"Pain engine failed: {res.stderr}")
        
        # Verify SSOT content
        with open(os.path.join(test_vet_dir, "current_patient.json"), 'r') as f:
            ssot = json.load(f)
            acute = ssot.get("pain_score", {}).get("acute", {})
            if acute.get("value") != 5 or acute.get("scale") != "FGS" or not acute.get("updated_at"):
                raise Exception(f"Pain SSOT mismatch: {acute}")
        print("✓ Pain Engine aligned and robust.")

        # 4. Skill: DM Calculator (Nested Schema Alignment)
        print("\n[Step 3] Testing skills/vet-dm-manager/scripts/dm_calculator.py...")
        # Usage: dog weight dose nadir peak appetite% vomiting_0/1
        dm_script_dir = os.path.join(PROJECT_ROOT, "skills/vet-dm-manager/scripts")
        res = run_command([sys.executable, "dm_calculator.py", "dog", "10", "2", "120", "250", "100", "0"], cwd=dm_script_dir)
        if res.returncode != 0: raise Exception(f"DM calculator failed: {res.stderr}")
        
        # Verify SSOT
        with open(os.path.join(test_vet_dir, "current_patient.json"), 'r') as f:
            ssot = json.load(f)
            dm = ssot.get("management", {}).get("diabetes", {})
            if dm.get("dose", {}).get("value") != 2.0 or "Modernized" not in dm.get("clinical_guidance", {}).get("value", ""):
                raise Exception(f"DM SSOT mismatch: {dm}")
        print("✓ DM Calculator aligned and robust.")

        # 5. Core: Workflow Validator (Deep Check Logic)
        print("\n[Step 4] Testing core/workflow_validator.py...")
        # Should report MISSING for vitals (since we haven't updated them)
        res = run_command([sys.executable, "core/workflow_validator.py", "vet-pain-score"])
        if "MISSING" not in res.stdout:
            raise Exception(f"Validator False Positive: Should report missing vitals. Output: {res.stdout}")
        
        # Update vitals to satisfy
        run_command([sys.executable, "core/data_manager.py", "update", "vitals.temp", "38.5", "C"])
        res = run_command([sys.executable, "core/workflow_validator.py", "vet-pain-score"])
        if "Ready: True" not in res.stdout:
            raise Exception(f"Validator False Negative: Should be ready after vitals update. Output: {res.stdout}")
        print("✓ Workflow Validator deep check functional.")

        # 6. Core: SOAP Formatter (Absolute Path Template Loading)
        print("\n[Step 5] Testing core/soap_formatter.py...")
        # Run from an unrelated directory [Fix Finding P2 Template Path]
        with tempfile.TemporaryDirectory() as unrelated_dir:
            res = run_command([sys.executable, os.path.join(PROJECT_ROOT, "core/soap_formatter.py")], cwd=unrelated_dir)
            if res.returncode != 0: raise Exception(f"SOAP formatter crashed: {res.stderr}")
            if "[Template Missing]" in res.stdout:
                raise Exception("SOAP Template Loading Failed: Found '[Template Missing]'.")
            if "Codex-Tester" not in res.stdout or "FGS" not in res.stdout:
                raise Exception("SOAP Content Mismatch: Missing patient name or pain score info.")
        print("✓ SOAP Formatter resource discovery functional.")

        print("\n" + "="*45)
        print("🏆 ALL INTEGRATION STEPS PASSED SUCCESSFULLY 🏆")
        print("="*45)

    except Exception as e:
        print(f"\n❌ INTEGRATION TEST FAILED")
        print(f"Reason: {str(e)}")
        sys.exit(1)
    finally:
        if is_temp:
            shutil.rmtree(test_vet_dir)
            # print(f"[Cleanup] Removed temporary sandbox: {test_vet_dir}")

if __name__ == "__main__":
    test_system_integration()
