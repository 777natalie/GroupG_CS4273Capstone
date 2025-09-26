# Kaylee Nguyen
# STILL TESTING
# Extract Questions Asked in the Transcript for comparison and analysis to the flipbook
# Components Needed: Questions asked, Questions not asked, Timestamps, Dispatcher Name, Caller Name

import pandas as pd
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore  # Ensure correct import

# Step 1: read CSV to extract needed components (questions & conditions)
def read_csv(file_path):
    """
    Reads a CSV file with 'Section ID' and 'Question Text' columns,
    ensuring correct formatting and compatibility.
    Returns a list of (section_id, question) tuples.
    """
    try:
        df = pd.read_csv(file_path, encoding="utf-8")  # Handle encoding
        df.columns = df.columns.str.strip()  # .str.lower() Removing any extra spaces and symbols
        print("Detected columns:", df.columns)  # Debugging print
        
        if "Section ID" not in df.columns or "Question Text" not in df.columns:
            raise ValueError("The CSV file must contain 'Section ID' and 'Question Text' columns.")
        
        return list(df[["Section ID", "Question Text"]].itertuples(index=False, name=None))

    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        exit(1)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        exit(1)

# Step 2: Create an index with LlamaIndex
def create_index(questions):
    """
    Creates a searchable index using LlamaIndex and OpenAI embeddings.

    Parameters: List of (condition, question) tuples

    Returns: index: Searchable VectorStoreIndex object
    """
    documents = [{"text": f"{condition}: {question}"} for condition, question in questions]

    # Create a storage context with FaissVectorStore
    storage_context = FaissVectorStore()

    # Build the index using OpenAI-generated embeddings
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embedding=OpenAIEmbedding()
    )

    return index

# Step 3: Compare a call transcript to the questions in the index
def compare_transcript_to_questions(index, transcript, top_k=5):
    """
    Compares the call transcript to the stored questions in the index
    and returns the most relevant questions based on similarity.

    Returns: a list of the questions asked
    """
    query = transcript
    response = index.query(query, top_k=top_k)  # Retrieve top K matches
    return response

# Step 4: Main function
def main(csv_path, transcript):
    # Step 1: Read the conditions and questions from the CSV
    questions = read_csv(csv_path)

    # Step 2: Create an index from the questions
    index = create_index(questions)

    # Step 3: Compare the transcript with the questions in the index
    relevant_questions = compare_transcript_to_questions(index, transcript)

    # Output the results
    print(f"Relevant questions for the transcript:")
    for idx, question in enumerate(relevant_questions, 1):
        print(f"{idx}. {question.text}")

if __name__ == "__main__":
    import os
    
    # Ensure correct working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    csv_file_path = os.path.join(script_dir, "data", "(Updated) - EMS-Calltaking-QA.csv")
    
    # Example transcript
    example_transcript = """
    Patient reports chest pain, I would like to know if they have taken any drugs or medications in the past 12 hours.
    Also, were all key questions asked in order to ensure we didn't miss anything?
    """

    # Run the main function
    main(csv_file_path, example_transcript)

# MAKE THE CHANGE