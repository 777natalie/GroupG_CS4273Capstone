# coveragePy.py

import re
from typing import List, Dict

STOPWORDS = {"a","an","the","is","are","of","to","your","my","our","their","his","her","there","this","that","what"}

def normalize(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    tokens = [t for t in text.split() if t and t not in STOPWORDS]
    return tokens

def token_overlap_score(question: str, transcript: str) -> float:
    q_tokens = set(normalize(question))
    if not q_tokens:
        return 0.0
    t_tokens = set(normalize(transcript))
    overlap = len(q_tokens & t_tokens)
    return overlap / len(q_tokens)

def check_coverage(transcript: str, required_questions: List[str], threshold: float = 0.6) -> Dict:
    asked = []
    missed = []
    for q in required_questions:
        score = token_overlap_score(q, transcript)
        rec = {"question": q, "match_score": round(score, 2)}
        if score >= threshold:
            asked.append(rec)
        else:
            missed.append(rec)
    coverage = round(len(asked) / max(1, len(required_questions)), 2)
    return {"asked": asked, "missed": missed, "coverage": coverage}
