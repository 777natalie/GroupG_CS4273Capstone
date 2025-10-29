# detect_naturecodes.py
# natalie
# detects NatureCodes in EMS call transcripts using keyword matching and text embeddings
# will connect with grading later 

import pandas as pd
import json
import re
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import argparse
import os

# Step 0: Load the EMS protocol questions
df = pd.read_csv("data/EMSQA.csv")  # This has all our protocol questions

# Step 1: Load NatureCode keywords
with open("nature_keywords.json") as f:
    NATURE_KEYWORDS = json.load(f)

# Step 2: Organize protocol questions by NatureCode 
protocol_questions = defaultdict(list)
for _, row in df.iterrows():
    protocol_questions[row["NatureCode"]].append((row["Question_ID"], row["Question_Text"]))

# Step 3: Load embedding model 
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 4: Detection setup 
# Words that are super common and might trigger false positives
COMMON_WORDS = {
    "pain", "breathing", "awake", "okay", "help", "address",
    "speaking", "crying", "safe", "discomfort", "problems", "normal", "talk"
}

# NatureCodes that we consider high priority (only need one keyword hit to trigger)
HIGH_PRIORITY_CODES = {
    "Allergies / Envenomations",
    "Burns (Scalds) / Explosion (Blast)",
    "Breathing Problems",
    "Choking",
    "Cardiac or Respiratory Arrest / Death"
}

def run_detection(transcript_path, output_folder="keywordsOutput"):
    # Read the transcript
    with open(transcript_path, "r") as f:
        transcript_text = f.read().strip()

    # Split transcript into individual lines/segments
    segment_texts = [line.strip() for line in transcript_text.split("\n") if line.strip()]
    transcript_lower = transcript_text.lower()

    # Prepare embeddings for similarity comparison
    nature_names = list(NATURE_KEYWORDS.keys())
    nature_texts = [" ".join(NATURE_KEYWORDS[n]) for n in nature_names]
    nature_embeddings = model.encode(nature_texts, convert_to_numpy=True, normalize_embeddings=True)
    segment_embeddings = model.encode(segment_texts, convert_to_numpy=True, normalize_embeddings=True)
    transcript_embedding = model.encode(transcript_text, convert_to_numpy=True, normalize_embeddings=True)
    sims_to_transcript = cosine_similarity([transcript_embedding], nature_embeddings)[0]

    triggered_naturecodes = set()
    match_details = {}
    confidence_scores = {}

    # Go through each NatureCode and see if it should be triggered
    for i, nature in enumerate(nature_names):
        keywords = NATURE_KEYWORDS[nature]
        strong_hits = []

        for seg in segment_texts:
            seg_lower = seg.lower()
            for kw in keywords:
                kw_low = kw.lower()
                if re.search(rf"\b{re.escape(kw_low)}\b", seg_lower):
                    if kw_low in COMMON_WORDS and nature != "Sick Person (Specific Diagnosis)":
                        continue
                    strong_hits.append(kw_low)

        strong_hits = list(set(strong_hits))
        sim_score = float(sims_to_transcript[i])
        confidence = round(sim_score + 0.1 * len(strong_hits), 3)
        confidence_scores[nature] = confidence

        # Trigger rules
        if nature == "Case Entry":
            # Always include Case Entry
            case_keywords = ["emergency", "address", "phone", "patient", "confirmed", "verified"]
            case_hits = [kw for kw in case_keywords if kw in transcript_lower]
            triggered_naturecodes.add("Case Entry")
            match_details["Case Entry"] = case_hits or ["None"]
            confidence_scores["Case Entry"] = confidence_scores.get("Case Entry", 0.3)
        else:
            # High-priority codes only need one keyword, others need 2+
            if (nature in HIGH_PRIORITY_CODES and len(strong_hits) >= 1) or len(strong_hits) >= 2:
                triggered_naturecodes.add(nature)
                match_details[nature] = strong_hits

    # Remove "Unknown Problem" if other stronger codes exist
    if "Unknown Problem (Person Down)" in triggered_naturecodes and any(
        n for n in triggered_naturecodes if n not in ["Case Entry", "Unknown Problem (Person Down)"]
    ):
        triggered_naturecodes.remove("Unknown Problem (Person Down)")

    # Sort by confidence
    triggered_naturecodes = sorted(triggered_naturecodes, key=lambda n: confidence_scores.get(n, 0), reverse=True)

    # Step 5: Save output 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    transcript_name = os.path.basename(transcript_path).replace(".txt", "")
    log_filename = os.path.join(output_folder, f"{transcript_name}_naturecodes.txt")

    with open(log_filename, "w") as log_file:
        log_file.write("\nFiltered relevant NatureCodes (sorted by confidence):\n")
        for n in triggered_naturecodes:
            keywords_found = ", ".join(match_details.get(n, [])) or "None"
            conf = confidence_scores[n]
            log_file.write(f"- {n}\n   Keywords: {keywords_found}\n   Confidence: {conf:.3f}\n")

    print(f"Finished processing {transcript_path}, results saved to {log_filename}")


# Step 6: main, output
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect NatureCodes in a transcript")
    parser.add_argument("transcript", help="Path to transcript file (.txt)")
    parser.add_argument("--output", default="keywordsOutput", help="Folder to save outputs")
    args = parser.parse_args()

    run_detection(args.transcript, args.output)
