from sentence_transformers import SentenceTransformer, util
import pandas as pd
import json

# Load your data
questions_df = pd.read_csv("EMSQA.csv")
with open("transcript_call.json") as f:
    responses_data = json.load(f)

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define similarity thresholds
def get_grade(similarity):
    if similarity > 0.8:
        return "Asked Correctly"
    elif similarity > 0.5:
        return "Asked Incorrectly"
    else:
        return "Not Asked"

# Grading loop
for _, row in questions_df.iterrows():
    q_id = str(row["Question_ID"])
    question = row["Question_Text"]
    allowed_alts = row.get("Allowed_Alternatives", "")
    
    response = responses_data.get(q_id, {}).get("Response", "")
    if not response:
        print(f"Question: {question}\nGrade: Not Asked\n----------------------------------------")
        continue
    
    # Use allowed alternatives or question text
    reference_texts = [question] + (allowed_alts.split("|") if allowed_alts else [])
    
    # Encode
    ref_emb = model.encode(reference_texts, convert_to_tensor=True)
    resp_emb = model.encode(response, convert_to_tensor=True)
    
    # Compute max similarity
    similarity = util.cos_sim(resp_emb, ref_emb).max().item()
    
    grade = get_grade(similarity)
    print(f"Question: {question}\nGrade: {grade}\n----------------------------------------")
