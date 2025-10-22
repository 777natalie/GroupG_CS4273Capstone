#!/usr/bin/env python3
# ai_grading_trial.py

import csv
import sys
import re

grade_labels = {
    "1": "Asked Correctly",
    "2": "Not Asked",
    "3": "Asked Incorrectly",
    "4": "Not As Scripted",
    "5": "N/A"
    }

# loose matching rules for demo
LOOSE_MATCHES = {
    1: [["location", "address"], ["where"]],
    2: [["confirm", "verify", "address"], ["location"]],
    3: [["phone", "number"], ["callback", "number"], ["what", "is", "your", "number"]],
    4: [["what", "happened"], ["tell", "exactly", "happened"]],
    5: [["fast", "track"]],
    6: [["with", "patient"]],
    7: [["how", "many"], ["people", "hurt"], ["people", "sick"]],
    8: [["breathing"], ["coughing"]],
    9: [["how", "old"], ["age", "patient"], ["years", "old"]],
    10: [["approximately"]],
    11: [["awake"], ["conscious"]],
    12: [["breathing"]],
    140: [["fall"], ["how", "far"], ["distance"]],
    147: [["floor", "ground"], ["still", "on", "floor"]],
}

# normalize questions and transcript for matching
def normalize(text):
    text = text.lower()
    text = re.sub(r"[’']", "", text) 
    text = re.sub(r"[^a-z0-9\s]", "", text)  
    text = re.sub(r"\s+", " ", text)  
    return text.strip()

# read protocols from CSV file
def load_questions(csv_file):
    questions = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row['Question Text'])
    return questions

# read transcript from text file
def load_transcript(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as f:
        return normalize(f.read())

# checking for exact match of the question asked from transcript
def exact_match(transcript, question):
    return normalize(question) in transcript

# checking for loose match of the question asked from transcript
def loose_match(transcript, rules):
    for rule in rules:
        if all(any(word in transcript for word in r.split()) for r in rule):
            return True
    return False

# grading logic
def grade(transcript, questions):
    results = []
    # 
    for idx, q in enumerate(questions, 1):
        # if exact match found, code 1
        if exact_match(transcript, q):
            code = 1
        # if loose match found, code 1
        elif idx in LOOSE_MATCHES and loose_match(transcript, LOOSE_MATCHES[idx]):
            code = 1
        # if no match found, code 4
        else:
            code = 4
        results.append((idx, code, q))
    return results

# print results
def print_results(results):
    asked = [idx for idx, code, _ in results if code == 1]
    missed = [idx for idx, code, _ in results if code != 1]
    coverage = len(asked) / len(results) if results else 0


    print("=== Questions Asked Correctly ===")
    for idx, code, q in results:
        if code == 1:
            print(f"{idx}: {q}")

    print("\nSummary:")
    print(f"asked = {asked}")
    print(f"missed = {missed}")
    print(f"coverage = {coverage:.2f}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 ai_grading_trial.py ./data/EMS-Calltaking-QA.csv transcript_call.txt")
        sys.exit(1)

    questions = load_questions(sys.argv[1])
    transcript = load_transcript(sys.argv[2])
    results = grade(transcript, questions)
    print_results(results)

