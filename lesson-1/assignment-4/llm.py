import os
import ollama
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
# Also search in the script's directory for .env
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

def get_embedding(text, model_name="tinyllama:latest"):
    # Keep using local Ollama for embeddings
    emb_resp = ollama.embeddings(model=model_name, prompt=text)
    return emb_resp["embedding"]

def query_llm(prompt, model_name="llama-3.1-8b-instant"):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY not found in environment variables. Please add it to your .env file."
        
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )
    
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error calling Groq API: {e}"
