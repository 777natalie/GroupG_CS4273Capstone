# ems_grading_demo.py
from sentence_transformers import SentenceTransformer, util

# lightweight model for text similarity for now... 
model = SentenceTransformer("all-MiniLM-L6-v2")

# EMS protocol questions
questions = [
    "What is the patient's age?",
    "What is the patient's gender?",
    "What is the chief complaint?",
]

# example transcript
transcript = [
    "Okay, so how old is she?",
    "She is a 45-year-old female.",
    "She’s been complaining about chest pain since this morning."
]

# encode questions and transcript
q_embeddings = model.encode(questions, convert_to_tensor=True)
t_embeddings = model.encode(transcript, convert_to_tensor=True)

# similarity threshold for considering a question as "asked"
THRESHOLD = 0.4

results = []
for i, q in enumerate(questions):
    sims = util.cos_sim(q_embeddings[i], t_embeddings)
    best_score = float(sims.max())

    # show comparisons
    print(f"\nQuestion: {q}")
    for j, line in enumerate(transcript):
        print(f"   vs. \"{line}\" -> similarity={sims[0][j]:.2f}")

    asked = best_score >= THRESHOLD
    results.append((q, asked, best_score))

# report
print("\n--- EMS Grading Report ---")
asked_count = 0
for q, asked, score in results:
    status = "Asked" if asked else "Missed"
    if asked:
        asked_count += 1
    print(f"{status}: {q}  (best similarity={score:.2f})")

coverage = asked_count / len(questions) * 100
print(f"\nCoverage Score: {coverage:.1f}%")
