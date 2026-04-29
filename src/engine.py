import os
import re
from pathlib import Path

import ollama
from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from utils import format_hospital_info, load_mental_health_data

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = os.getenv(
    "MENTAL_HEALTH_DATA_PATH",
    str(ROOT_DIR / "data" / "mental_health_india.json"),
)
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(ROOT_DIR / "db"))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ENABLE_RAG = os.getenv("ENABLE_RAG", "true").lower() in {"1", "true", "yes"}

client = ollama.Client(host=OLLAMA_BASE_URL)

data = load_mental_health_data(DATA_PATH) or {"mental_health_resources": {"major_hospitals": []}}
documents = format_hospital_info(data["mental_health_resources"].get("major_hospitals", []))

vector_db = None
if ENABLE_RAG and documents:
    try:
        embeddings = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL, base_url=OLLAMA_BASE_URL)
        vector_db = Chroma.from_texts(documents, embeddings, persist_directory=CHROMA_DB_PATH)
    except Exception as exc:
        # Fallback to non-RAG mode if embeddings cannot load (e.g., low memory).
        print(f"RAG disabled due to embedding error: {exc}")


def classify_intent(query):
    query = query.lower()

    if any(re.search(word, query) for word in ["kill", "suicid", "hurt my", "end it"]):
        return "CRISIS"

    resource_triggers = [
        "hospital",
        "doctor",
        "ngo",
        "clinic",
        "near me",
        "helpline",
        "counseling",
        "therapy",
        "psychiatrist",
        "psychologist",
    ]
    if any(word in query for word in resource_triggers):
        return "RESOURCE"

    emotional_triggers = ["sad", "lonely", "depressed", "anxious", "scared", "crying"]
    if any(word in query for word in emotional_triggers):
        return "EMOTIONAL"

    return "CASUAL"


def get_mental_health_help(user_query):
    intent = classify_intent(user_query)

    if intent == "CRISIS":
        return (
            "🚨 **I am very concerned about you.** Please reach out to Tele-Manas at "
            "**14416** immediately. You don't have to go through this alone."
        )

    if intent == "RESOURCE" and vector_db is not None:
        docs = vector_db.similarity_search(user_query, k=1)
        context = docs[0].page_content if docs else "No specific hospital found."
        prompt = f"You are a helpful friend. Use this resource to help: {context}\nUser: {user_query}"
    elif intent == "EMOTIONAL":
        prompt = f"You are an empathetic friend. The user is feeling down. Listen and comfort them: {user_query}"
    else:
        prompt = f"You are a friendly AI companion. Chat casually: {user_query}"

    response = client.generate(model=OLLAMA_MODEL, prompt=prompt)
    return response["response"]