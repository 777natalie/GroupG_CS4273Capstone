# testCoveragePy.py

# cd to tests/python
# Run: python3 testCoveragePy.py
import json
from pathlib import Path
from coveragePy import check_coverage

BASE = Path(__file__).parent                  # .../tests/python
SAMPLE = BASE.parent / "sample_data"          # .../tests/sample_data

def load_paths():
    rq_path  = SAMPLE / "required_questions.json"
    pos_path = SAMPLE / "transcript_positive.txt"
    neg_path = SAMPLE / "transcript_negative.txt"
    for p in (rq_path, pos_path, neg_path):
        if not p.exists():
            raise FileNotFoundError(f"Missing required file: {p}")
    return rq_path, pos_path, neg_path

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def run_case(name, transcript_label, transcript_text, required, threshold, expect_asked, expect_coverage):
    print(f"\n===== CASE: {name} =====")
    print(f"--- Transcript ({transcript_label}) ---")
    print(transcript_text.strip())
    print("---------------------------------------")


    res = check_coverage(transcript_text, required, threshold)
    passed = (len(res["asked"]) == expect_asked) and (abs(res["coverage"] - expect_coverage) < 1e-9)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print("  asked:")
    for a in res["asked"]:
        print(f"    - {a['question']} (score={a['match_score']})")
    print("  missed:")
    for m in res["missed"]:
        print(f"    - {m['question']} (score={m['match_score']})")
    print(f"  coverage={res['coverage']}")
    print(f"\n")
    return passed

if __name__ == "__main__":
    rq_path, pos_path, neg_path = load_paths()
    rq = load_json(rq_path)
    required = rq["required"]
    threshold = float(rq.get("threshold", 0.6))

    pos = pos_path.read_text(encoding="utf-8").strip()
    neg = neg_path.read_text(encoding="utf-8").strip()

    if pos == neg:
        raise RuntimeError("Positive and negative transcripts are IDENTICAL. Fix tests/sample_data/*.txt.")

    total = 0; ok = 0
    total += 1
    if run_case("All detected", "positive", pos, required, threshold, 3, 1.0): ok += 1
    total += 1
    if run_case("None detected", "negative", neg, required, threshold, 0, 0.0): ok += 1
    print(f"\nRESULT: {ok}/{total} tests passed.")
