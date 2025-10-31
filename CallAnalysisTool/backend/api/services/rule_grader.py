"""
Rule-based grading service
Wraps the test_case.py logic from unitTests
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class RuleBasedGrader:
    """
    Rule-based transcript grader using pattern matching
    Based on Kevin's test_case.py logic
    """
    
    # Grading code meanings
    KEY = {
        "1": "Asked Correctly",
        "2": "Not Asked",
        "3": "Asked Incorrectly",
        "4": "Not As Scripted",
        "5": "N/A",
        "6": "Obvious",
        "RC": "Recorded Correctly"
    }
    
    def __init__(self, rubric_path: Optional[str] = None, synonyms_path: Optional[str] = None):
        """
        Initialize grader with rubric and synonyms
        
        Args:
            rubric_path: Path to rubric.json (defaults to unitTests/rubric.json)
            synonyms_path: Path to synonyms.json (defaults to unitTests/synonyms.json)
        """
        # Default paths relative to project root
        base_path = Path(__file__).parent.parent.parent.parent / "unitTests"
        
        rubric_file = Path(rubric_path) if rubric_path else base_path / "rubric.json"
        synonyms_file = Path(synonyms_path) if synonyms_path else base_path / "synonyms.json"
        
        # Load configurations
        self.labels = self._load_json(rubric_file, self._get_default_labels())
        self.synonyms = self._load_json(synonyms_file, self._get_default_synonyms())
    
    def _get_default_labels(self) -> Dict[str, str]:
        """Default labels if rubric.json not found"""
        return {
            "1": "What's the location of the emergency?",
            "1a": "Address/location confirmed/verified?",
            "1b": "911 CAD Dump used to build the call?",
            "2": "What's the phone number you're calling from?",
            "2a": "Phone number documented in the entry?"
        }
    
    def _get_default_synonyms(self) -> Dict[str, List[str]]:
        """Default synonyms if synonyms.json not found"""
        return {
            "q1": ["location of the emergency", "address of the emergency", "what is the address"],
            "q2": ["phone number", "callback number", "what is your number", "whats your number"],
            "city_state": ["norman", "oklahoma", "ok"],
            "street_hints": ["street", "st", "avenue", "ave", "road", "rd", "drive", "dr", "lane", "ln", "highway", "hwy"]
        }
    
    def _load_json(self, path: Path, default: Any) -> Any:
        """Load JSON file or return default"""
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return default
        return default
    
    def normalize_text(self, text: str) -> str:
        """Lowercase, strip punctuation (except ?), collapse whitespace"""
        text = text.lower()
        text = re.sub(r"[^\w\s?]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text
    
    def parse_groupb_json(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse Group B's JSON transcript format into segments
        
        Expected format:
        {
            "segments": [
                {
                    "start": 0.0,
                    "end": 5.0,
                    "text": "Norman 911...",
                    "speaker": "SPEAKER_01",
                    ...
                }
            ]
        }
        
        Returns:
            List of segment dictionaries
        """
        if "segments" in data:
            return data["segments"]
        return []
    
    def said_exact_by_dispatcher(self, segments: List[Dict], target: str) -> Optional[Dict]:
        """Check if dispatcher (SPEAKER_01) said target exactly (normalized)"""
        target_norm = self.normalize_text(target)
        for i, seg in enumerate(segments):
            if seg.get("speaker") == "SPEAKER_01":
                if self.normalize_text(seg.get("text", "")) == target_norm:
                    return {"idx": i, "text": seg.get("text", "")}
        return None
    
    def said_contains_any_by_dispatcher(self, segments: List[Dict], phrases: List[str]) -> Optional[Dict]:
        """Check if dispatcher said any of the phrases (normalized substring)"""
        norm_phrases = [self.normalize_text(p) for p in phrases]
        for i, seg in enumerate(segments):
            if seg.get("speaker") != "SPEAKER_01":
                continue
            text_norm = self.normalize_text(seg.get("text", ""))
            if any(p in text_norm for p in norm_phrases):
                return {"idx": i, "text": seg.get("text", "")}
        return None
    
    def caller_mentions_address_bits(self, segments: List[Dict]) -> Optional[Dict]:
        """
        Heuristic for Q1a (verification):
        - Caller (SPEAKER_00) spells part of a street (e.g., B-R-O-M-P-T-O-N), OR
        - Caller says a street number with city/state or street-type word
        """
        spell_re = re.compile(r"\b([a-z])(?:\s*[-\s]\s*[a-z]){2,}\b", re.I)
        number_re = re.compile(r"\b\d{1,5}\b")
        city_state = set(self.synonyms.get("city_state", []))
        street_hints = set(self.synonyms.get("street_hints", []))
        
        for i, seg in enumerate(segments):
            if seg.get("speaker") != "SPEAKER_00":
                continue
            text = seg.get("text", "")
            text_norm = self.normalize_text(text)
            
            # Check for spelled letters
            if spell_re.search(text):
                return {"idx": i, "text": text}
            
            # Check for house number + street hints
            if number_re.search(text) and any(w in text_norm for w in city_state.union(street_hints)):
                return {"idx": i, "text": text}
        
        return None
    
    def caller_says_phone_digits(self, segments: List[Dict]) -> Optional[Dict]:
        """
        Heuristic for 2a (documented):
        Check if any 7-12 digit sequence appears anywhere
        """
        phone_re = re.compile(r"\b(?:\d[\s\-\.]?){7,12}\b")
        for i, seg in enumerate(segments):
            text = seg.get("text", "")
            if phone_re.search(text):
                return {"idx": i, "text": text}
        return None
    
    def grade_transcript(self, transcript_data: Dict[str, Any], show_evidence: bool = False) -> Dict[str, Any]:
        """
        Grade a transcript using rule-based logic
        
        Args:
            transcript_data: Group B's JSON format or dict with segments
            show_evidence: Include evidence in response
        
        Returns:
            Dictionary with grading results
        """
        segments = self.parse_groupb_json(transcript_data)
        
        # Q1 — address asked
        q1_exact = self.said_exact_by_dispatcher(segments, self.labels.get("1", ""))
        q1_loose = self.said_contains_any_by_dispatcher(segments, self.synonyms.get("q1", []))
        code_1 = "1" if q1_exact else ("4" if q1_loose else "2")
        ev1 = q1_exact or q1_loose
        
        # Q1a — address verified by caller
        ev1a = self.caller_mentions_address_bits(segments)
        code_1a = "1" if ev1a else "2"
        
        # Q1b — CAD dump used (not derivable from transcript)
        code_1b = "2"
        ev1b = None
        
        # Q2 — phone number asked
        q2_exact = self.said_exact_by_dispatcher(segments, self.labels.get("2", ""))
        q2_loose = self.said_contains_any_by_dispatcher(segments, self.synonyms.get("q2", []))
        code_2 = "1" if q2_exact else ("4" if q2_loose else "2")
        ev2 = q2_exact or q2_loose
        
        # Q2a — phone number documented
        ev2a = self.caller_says_phone_digits(segments)
        code_2a = "1" if ev2a else "2"
        
        # Build results
        grades = {
            "1": {
                "code": code_1,
                "label": self.labels["1"],
                "status": self.KEY.get(code_1, "Unknown")
            },
            "1a": {
                "code": code_1a,
                "label": self.labels["1a"],
                "status": self.KEY.get(code_1a, "Unknown")
            },
            "1b": {
                "code": code_1b,
                "label": self.labels["1b"],
                "status": self.KEY.get(code_1b, "Unknown")
            },
            "2": {
                "code": code_2,
                "label": self.labels["2"],
                "status": self.KEY.get(code_2, "Unknown")
            },
            "2a": {
                "code": code_2a,
                "label": self.labels["2a"],
                "status": self.KEY.get(code_2a, "Unknown")
            }
        }
        
        # Add evidence if requested
        if show_evidence:
            grades["1"]["evidence"] = ev1
            grades["1a"]["evidence"] = ev1a
            grades["1b"]["evidence"] = ev1b
            grades["2"]["evidence"] = ev2
            grades["2a"]["evidence"] = ev2a
        
        return grades

