#!/usr/bin/env python3
# test_case.py
# Demo unit testing: grade a flat TXT transcript for Case Entry Questions (1, 1a, 1b, 2, 2a)

import re, sys, json
from pathlib import Path
from typing import List, Dict, Any

# Mapping of grading codes to their meanings (from QA sheet)
# Only codes 1,2,4 are used here; 3, 5, 6, and RC are for other contexts.
KEY = {
    "1": "Asked Correctly",
    "2": "Not Asked",
    "3": "Asked Incorrectly",
    "4": "Not As Scripted",
    "5": "N/A",
    "6": "Obvious",
    "RC": "Recorded Correctly"
}

# Parse through txt transcript lines using a regular expression
# [mm:ss.s–mm:ss.s] SPEAKER_XX: text
LINE_RE = re.compile(
    r"^\[(\d{2}):(\d{2}\.\d)\s*[\u2013\-]\s*(\d{2}):(\d{2}\.\d)\]\s+(SPEAKER_\d{2}):\s*(.*)$"
)

def load_segments(txt_path: Path) -> List[Dict[str, Any]]:
    """
    Load the transcript TXT file and return a list of segments.
    Each segment has: start time, end time, speaker, and text.
    """
    segs = []
    for line in txt_path.read_text(encoding="utf-8").splitlines():
        m = LINE_RE.match(line)
        if not m:
            continue  # skip lines that don't match the pattern
        m1, s1, m2, s2, spk, text = m.groups()
        start = int(m1) * 60 + float(s1)   # convert mm:ss.s to seconds
        end = int(m2) * 60 + float(s2)
        segs.append({"start": start, "end": end, "speaker": spk, "text": text})
    return segs

def norm(s: str) -> str:
    """
    Normalize a string for easier matching:
    - lowercase
    - strip punctuation
    - collapse extra spaces
    """
    s = s.lower()
    s = re.sub(r"[^\w\s?]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def said_exact_by_dispatcher(segments, target: str) -> bool:
    """
    Return True if dispatcher (SPEAKER_01) said exactly the target line
    after normalization.
    """
    tnorm = norm(target)
    return any(
        seg["speaker"] == "SPEAKER_01" and norm(seg["text"]) == tnorm
        for seg in segments
    )

def said_contains_all_by_dispatcher(segments, *kws: str) -> bool:
    """
    Return True if dispatcher said a line containing ALL given keywords.
    This is used to detect "Not As Scripted" synonyms.
    """
    kws = [norm(k) for k in kws]
    for seg in segments:
        if seg["speaker"] != "SPEAKER_01":
            continue
        u = norm(seg["text"])
        if all(k in u for k in kws):
            return True
    return False

def code_from(exact: bool, loose: bool) -> str:
    """
    Convert detection flags to a grade code.
    - exact → 1 (Asked Correctly)
    - loose → 4 (Not As Scripted)
    - neither → 2 (Not Asked)
    """
    if exact: return "1"
    if loose: return "4"
    return "2"

def grade_from_txt(txt_path: str) -> Dict[str, Dict[str,str]]:
    """
    Main grading function. Reads transcript, applies grading rules,
    and returns a dictionary of results for questions 1–2a.
    """
    segs = load_segments(Path(txt_path))

    # --- Q1: "What's the location of the emergency?"
    q1_exact = said_exact_by_dispatcher(segs, "What's the location of the emergency?")
    q1_loose = (
        said_contains_all_by_dispatcher(segs, "location", "emergency")
        or said_contains_all_by_dispatcher(segs, "address", "emergency")
        or said_contains_all_by_dispatcher(segs, "address of the emergency")
    )
    code_1 = code_from(q1_exact, q1_loose)

    # --- 1a: Was the address/location confirmed/verified?
    # Heuristic: caller spells out letters (B-R-O-M-P-T-O-N) OR
    # gives number + city/state (like "Norman, Oklahoma").
    spell_re = re.compile(r"\b([a-z])(?:\s*[-\s]\s*[a-z]){2,}\b", re.I)
    city_state_re = re.compile(r"\b(norman|oklahoma|ok)\b", re.I)
    number_re = re.compile(r"\b\d{1,5}\b")
    verified = False
    for seg in segs:
        if seg["speaker"] != "SPEAKER_00":
            continue
        t = seg["text"]
        if spell_re.search(t) or (number_re.search(t) and city_state_re.search(t)):
            verified = True
            break
    code_1a = "1" if verified else "2"

    # --- 1b: Was the 911 CAD Dump used to build the call?
    # Not detectable from transcript text → mark as Not Asked (2).
    code_1b = "2"

    # --- Q2: "What's the phone number you're calling from?"
    q2_exact = (
        said_exact_by_dispatcher(segs, "What’s the phone number you’re calling from?")
        or said_exact_by_dispatcher(segs, "What's the phone number you're calling from?")
    )
    q2_loose = (
        said_contains_all_by_dispatcher(segs, "phone", "number")
        or said_contains_all_by_dispatcher(segs, "callback", "number")
        or said_contains_all_by_dispatcher(segs, "whats your number")
        or said_contains_all_by_dispatcher(segs, "what is your number")
    )
    code_2 = code_from(q2_exact, q2_loose)

    # --- 2a: Was the phone number documented in the entry?
    # Also not provable from transcript text → Not Asked (2).
    code_2a = "2"

    # Human-readable labels for each item
    labels = {
        "1": "What's the location of the emergency?",
        "1a": "Address/location confirmed/verified?",
        "1b": "911 CAD Dump used to build the call?",
        "2": "What’s the phone number you’re calling from?",
        "2a": "Phone number documented in the entry?",
    }

    # Build final dictionary result
    return {k: {"code": v, "label": labels[k]} for k,v in {
        "1": code_1, "1a": code_1a, "1b": code_1b, "2": code_2, "2a": code_2a
    }.items()}

if __name__ == "__main__":
    # CLI entrypoint: user passes in transcript TXT
    if len(sys.argv) < 2:
        print("Usage: python test_case.py <transcript.txt>")
        sys.exit(1)

    result = grade_from_txt(sys.argv[1])

    # Print out results with code and meaning
    print("=== Case Entry: Minimal Grades (from TXT) ===")
    for k in ["1","1a","1b","2","2a"]:
        code = result[k]["code"]
        label = result[k]["label"]
        meaning = KEY.get(code, "")
        print(f"{k:>2}: {code} ({meaning})  - {label}")
