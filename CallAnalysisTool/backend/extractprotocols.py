import pandas as pd

# Load the Excel file 
file_path = "./data/PoliceFireEMSCalltakingQAForms.xlsm"

emd_df = pd.read_excel(file_path, sheet_name="EMD QA")

questions = []
current_section = None

for idx, row in emd_df.iterrows():
    section = str(row["Unnamed: 1"]) if pd.notna(row["Unnamed: 1"]) else None
    question = str(row["Unnamed: 2"]) if pd.notna(row["Unnamed: 2"]) else None

    # Detect section headers (they usually end with ":")
    if section and section.endswith(":"):
        current_section = section.replace(":", "").strip()
        continue

    # Get actual questions
    if question and len(question) > 3:
        questions.append({
            "ProtocolID": f"EMD-{len(questions)+1:03d}",
            "Section": current_section,
            "Question": question.strip(),
            "ScoringOptions": "1=Correct,2=Not Asked,3=Incorrect,4=Not Scripted,5=N/A,6=Obvious,RC=Recorded Correctly",
            "Notes": ""
        })

# Convert to DataFrame
emd_questions_df = pd.DataFrame(questions)

# Save to CSV
emd_questions_df.to_csv("EMD_protocol.csv", index=False)

print("EMD_protocol.csv has been created successfully.")
