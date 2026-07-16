import os
from dotenv import load_dotenv
from google import genai

# Load the API key from .env
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load all neighborhood summaries
with open("data/processed/neighborhood_summaries.txt") as f:
    all_summaries = f.readlines()

def retrieve_relevant_summaries(question, summaries, top_n=5):
    """Simple keyword-based retrieval, with a full-context fallback
    for general/comparison questions where no specific neighbourhood is named."""
    question_lower = question.lower()
    matches = [s for s in summaries if any(word in s.lower() for word in question_lower.split())]

    # If a specific neighbourhood name was matched, use just those lines
    if matches and len(matches) < len(summaries):
        return matches[:top_n]

    # Otherwise (general "best/top/which" questions) — pass the FULL dataset,
    # since 158 lines is small enough for the model to compare directly
    return summaries

def ask(question):
    context_chunks = retrieve_relevant_summaries(question, all_summaries)
    context_text = "".join(context_chunks)

    prompt = f"""You are a helpful real-estate data assistant.
Use ONLY the data below to answer the question. Be concise — 2-3 sentences max.
Always include actual numbers from the data. If the data doesn't answer the question, say so.

DATA:
{context_text}

QUESTION: {question}
"""
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question about the Airbnb data (or 'exit'): ")
        if q.lower() == "exit":
            break
        print("\n" + ask(q))