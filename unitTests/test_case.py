#!/usr/bin/env python3
# test_case.py (improved)
# Minimal, standalone grader for Case Entry items 1, 1a, 1b, 2, 2a with better output.
# - Keeps your original behavior
# - Adds: --json / --pretty, --show-evidence, clearer exit codes
# - Uses tiny config files for labels & synonyms (optional, with safe defaults)
#
# Usage:
#   python3 test_case.py transcript_call.txt
#   python3 test_case.py transcript_call.txt --json --pretty --show-evidence

import re, sys, json, argparse
from pathlib import Path
from typing import List, Dict, Any

# === Config (labels & synonyms) ===
DEFAULT_LABELS = {
    "1":  "What's the location of the emergency?",
    "1a": "Address/location confirmed/verified?",
    "1b": "911 CAD Dump used to build the call?",
    "2":  "What’s the phone number you’re calling from?",
    "2a": "Phone number documented in the entry?",
}
DEFAULT_SYNONYMS = {
    # dispatcher prompts
    "q1": ["location of the emergency", "address of the emergency", "what is the address"],
    "q2": ["phone number", "callback number", "what is your number", "whats your number"],
    # caller evidence for verification (1a)
    "city_state": ["norman", "oklahoma", "ok"],
    "street_hints": ["street", "st", "avenue", "ave", "road", "rd", "drive", "dr", "lane", "ln", "highway", "hwy"]
}

KEY = {
    "1": "Asked Correctly",
    "2": "Not Asked",
    "3": "Asked Incorrectly",
    "4": "Not As Scripted",
    "5": "N/A",
    "6": "Obvious",
    "RC": "Recorded Correctly"
}

LINE_RE = re.compile(
    r"^\[(\d{2}):(\d{2}\.\d)\s*[\u2013\-]\s*(\d{2}):(\d{2}\.\d)\]\s+(SPEAKER_\d{2}):\s*(.*)$"
)

def load_json_if_exists(p: Path, default: dict) -> dict:
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return default
    return default

def load_segments(txt_path: Path) -> List[Dict[str, Any]]:
    segs = []
    for line in txt_path.read_text(encoding="utf-8").splitlines():
        m = LINE_RE.match(line)
        if not m:
            continue
        m1, s1, m2, s2, spk, text = m.groups()
        start = int(m1) * 60 + float(s1)
        end = int(m2) * 60 + float(s2)
        segs.append({"start": start, "end": end, "speaker": spk, "text": text})
    return segs

def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s?]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def said_exact_by_dispatcher(segments, target: str) -> Any:
    tnorm = norm(target)
    for i, seg in enumerate(segments):
        if seg["speaker"] == "SPEAKER_01" and norm(seg["text"]) == tnorm:
            return {"idx": i, "text": seg["text"]}
    return None

def said_contains_all_by_dispatcher(segments, *kws: str) -> Any:
    kws = [norm(k) for k in kws]
    for i, seg in enumerate(segments):
        if seg["speaker"] != "SPEAKER_01":
            continue
        u = norm(seg["text"])
        if all(k in u for k in kws):
            return {"idx": i, "text": seg["text"]}
    return None

def said_contains_any_by_dispatcher(segments, phrases: List[str]) -> Any:
    norm_phr = [norm(p) for p in phrases]
    for i, seg in enumerate(segments):
        if seg["speaker"] != "SPEAKER_01":
            continue
        u = norm(seg["text"])
        if any(p in u for p in norm_phr):
            return {"idx": i, "text": seg["text"]}
    return None

def caller_mentions_address_bits(segments, synonyms) -> Any:
    """Heuristic: caller (SPEAKER_00) says a street number + spelled letters OR city/state words."""
    spell_re = re.compile(r"\b([a-z])(?:\s*[-\s]\s*[a-z]){2,}\b", re.I)  # e.g., B-R-O-M-P-T-O-N
    number_re = re.compile(r"\b\d{1,5}\b")
    city_state = set(synonyms.get("city_state", []))
    street_hints = set(synonyms.get("street_hints", []))

    for i, seg in enumerate(segments):
        if seg["speaker"] != "SPEAKER_00":
            continue
        t = norm(seg["text"])
        if spell_re.search(seg["text"]):
            return {"idx": i, "text": seg["text"]}
        if number_re.search(seg["text"]) and any(w in t for w in city_state.union(street_hints)):
            return {"idx": i, "text": seg["text"]}
    return None

def caller_says_phone_digits(segments) -> Any:
    """Detect a phone-like number spoken by either party; if present at all, mark 2a as recorded."""
    # Looks for 7- or 10-digit sequences, with optional separators.
    phone_re = re.compile(r"\b(?:\d[\s\-\.]?){7,12}\b")
    for i, seg in enumerate(segments):
        t = seg["text"]
        if phone_re.search(t):
            return {"idx": i, "text": t}
    return None

def code_from(exact, loose) -> str:
    if exact: return "1"
    if loose: return "4"
    return "2"

def grade_from_txt(txt_path: Path, labels: dict, synonyms: dict, show_evidence: bool=False) -> Dict[str, Dict[str, Any]]:
    segs = load_segments(txt_path)

    # Q1
    q1_exact = said_exact_by_dispatcher(segs, labels.get("1", DEFAULT_LABELS["1"]))
    q1_loose = said_contains_any_by_dispatcher(segs, synonyms.get("q1", DEFAULT_SYNONYMS["q1"]))
    code_1 = code_from(q1_exact, q1_loose)
    ev1 = q1_exact or q1_loose

    # Q1a - verification by caller content
    ev1a = caller_mentions_address_bits(segs, synonyms)
    code_1a = "1" if ev1a else "2"

    # Q1b - not derivable from transcript text
    code_1b = "2"
    ev1b = None

    # Q2
    q2_exact = said_exact_by_dispatcher(segs, labels.get("2", DEFAULT_LABELS["2"]))
    q2_loose = said_contains_any_by_dispatcher(segs, synonyms.get("q2", DEFAULT_SYNONYMS["q2"]))
    code_2 = code_from(q2_exact, q2_loose)
    ev2 = q2_exact or q2_loose

    # Q2a - phone documented if any phone-like digits exist anywhere
    ev2a = caller_says_phone_digits(segs)
    code_2a = "1" if ev2a else "2"

    items = {
        "1":  {"code": code_1,  "label": labels["1"],  "evidence": ev1},
        "1a": {"code": code_1a, "label": labels["1a"], "evidence": ev1a},
        "1b": {"code": code_1b, "label": labels["1b"], "evidence": ev1b},
        "2":  {"code": code_2,  "label": labels["2"],  "evidence": ev2},
        "2a": {"code": code_2a, "label": labels["2a"], "evidence": ev2a},
    }

    if not show_evidence:
        for v in items.values():
            v.pop("evidence", None)
    return items

def main():
    ap = argparse.ArgumentParser(description="Minimal non‑AI case entry grader (TXT).")
    ap.add_argument("transcript", help="Path to transcript TXT")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    ap.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    ap.add_argument("--show-evidence", action="store_true", help="Include evidence (matching segment index/text)")
    ap.add_argument("--labels", default="rubric_min.json", help="Optional labels JSON (default: rubric_min.json)")
    ap.add_argument("--synonyms", default="synonyms.json", help="Optional synonyms JSON (default: synonyms.json)")
    args = ap.parse_args()

    tpath = Path(args.transcript)
    if not tpath.exists():
        print(f"Transcript not found: {tpath}", file=sys.stderr)
        sys.exit(2)

    labels = load_json_if_exists(Path(args.labels), DEFAULT_LABELS)
    synonyms = load_json_if_exists(Path(args.synonyms), DEFAULT_SYNONYMS)

    try:
        result = grade_from_txt(tpath, labels, synonyms, show_evidence=args.show_evidence)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)

    if args.json:
        print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
    else:
        print("=== Case Entry: Minimal Grades (from TXT) ===")
        for k in ["1","1a","1b","2","2a"]:
            code = result[k]["code"]
            label = result[k]["label"]
            meaning = KEY.get(code, "")
            print(f"{k:>2}: {code} ({meaning})  - {label}")
            if args.show_evidence and result[k].get("evidence"):
                ev = result[k]["evidence"]
                print(f"     evidence: seg#{ev['idx']} → {ev['text']}")

    # Exit 0 always after successful run
    sys.exit(0)

if __name__ == "__main__":
    main()
