#!/usr/bin/env python3
# test_case.py

import re, sys, json
from pathlib import Path
from typing import List, Dict, Any

KEY = {
    "1": "Asked Correctly",
    "2": "Not Asked",
    "3": "Asked Incorrectly",
    "4": "Not As Scripted",
    "5": "N/A"
}

LINE_RE = re.compile(r"^\[(\d{2}):(\d{2}\.\d)\s*[\u2013\-]\s*(\d{2}):(\d{2}\.\d)\]\s+(SPEAKER_\d{2}):\s*(.*)$")

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

def said_exact_by_dispatcher(segments, target: str) -> bool:
    tnorm = norm(target)
    return any(seg["speaker"]=="SPEAKER_01" and norm(seg["text"]) == tnorm for seg in segments)

def said_contains_all_by_dispatcher(segments, *kws: str) -> bool:
    kws = [norm(k) for k in kws]
    for seg in segments:
        if seg["speaker"] != "SPEAKER_01":
            continue
        u = norm(seg["text"])
        if all(k in u for k in kws):
            return True
    return False

def code_from(exact: bool, loose: bool) -> str:
    if exact: return "1"   # Asked Correctly
    if loose: return "4"   # Not As Scripted (intent matched via synonyms)
    return "2"             # Not asked

def grade_from_txt(txt_path: str) -> Dict[str, Dict[str,str]]:
    segs = load_segments(Path(txt_path))

    # Q1
    q1_exact = said_exact_by_dispatcher(segs, "What's the location of the emergency?")
    q1_loose = (
        said_contains_all_by_dispatcher(segs, "location", "emergency") or
        said_contains_all_by_dispatcher(segs, "address", "emergency") or
        said_contains_all_by_dispatcher(segs, "address of the emergency")
    )
    code_1 = code_from(q1_exact, q1_loose)

    # 1a (verified) — heuristic: caller spells street OR gives number + city/state anywhere
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

    # 1b — audio-only transcript cannot prove CAD dump usage
    code_1b = "2"

    # Q2
    q2_exact = said_exact_by_dispatcher(segs, "What’s the phone number you’re calling from?") or \
               said_exact_by_dispatcher(segs, "What's the phone number you're calling from?")
    q2_loose = (
        said_contains_all_by_dispatcher(segs, "phone", "number") or
        said_contains_all_by_dispatcher(segs, "callback", "number") or
        said_contains_all_by_dispatcher(segs, "whats your number") or
        said_contains_all_by_dispatcher(segs, "what is your number")
    )
    code_2 = code_from(q2_exact, q2_loose)

    # 2a — also not provable from transcript text
    code_2a = "2"

    labels = {
        "1":"What's the location of the emergency?",
        "1a":"Address/location confirmed/verified?",
        "1b":"911 CAD Dump used to build the call?",
        "2":"What’s the phone number you’re calling from?",
        "2a":"Phone number documented in the entry?",
    }

    

    return {k: {"code": v, "label": labels[k]} for k,v in {
        "1": code_1, "1a": code_1a, "1b": code_1b, "2": code_2, "2a": code_2a
    }.items()}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python grade_txt_case_entry.py <transcript.txt>")
        sys.exit(1)
    result = grade_from_txt(sys.argv[1])
    print("=== Case Entry: Minimal Grades (from TXT) ===")
    for k in ["1","1a","1b","2","2a"]:
        code = result[k]["code"]
        label = result[k]["label"]
        meaning = KEY.get(code, "")
        print(f"{k:>2}: {code} ({meaning})  - {label}")
