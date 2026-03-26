import json
import ollama
import re
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# 1. Load your JSON
with open('C:\\Users\\kabbo\\OneDrive\\Desktop\\MENTALHEALTHAI\\data\\mental_health_india.json', 'r') as f:
    data = json.load(f)

# Flatten the JSON into a list of strings for the AI to "read"
documents = []
for h in data['mental_health_resources']['major_hospitals']:
    text = f"Hospital: {h['name']}, City: {h['city']}, State: {h['state']}, Contact: {h['contact']}"
    documents.append(text)

# 2. Create Semantic Embeddings (The Librarian)
# This turns your text into numbers and stores them in a local folder called 'db'
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_db = Chroma.from_texts(documents, embeddings, persist_directory="./db")



def get_mental_health_help(user_query):
    # 1. Intent Detection: Does the user need a resource?
    # We ask a very fast model (or a local check) if this is a resource-seeking query.
    resource_keywords = ['hospital', 'doctor', 'ngo', 'helpline', 'near me', 'clinic', 'contact', 'emergency', 'support', 'counseling', 'therapy', 'psychiatrist', 'psychologist', 'mental health center', 'mental health clinic', 'mental health hospital', 'mental health support', 'mental health resources', 'mental health services', 'mental health help', 'mental health assistance', 'mental health care', 'mental health treatment','suicide prevention', 'crisis intervention', 'mental health organization', 'mental health foundation', 'mental health charity', 'mental health non-profit', 'mental health hotline', 'mental health counseling', 'mental health therapy', 'mental health support group', 'mental health peer support', 'mental health community resources','harm']
    
    needs_resource = any(word in user_query.lower() for word in resource_keywords)

    if needs_resource:
        # Only perform RAG if keywords are found
        docs = vector_db.similarity_search(user_query, k=1)
        context = docs[0].page_content if docs else "No specific hospital found."
        system_prompt = f"You are a helpful friend. Use this resource to help: {context}"
    else:
        # General conversation mode (No hospital info added)
        system_prompt = "You are a kind, empathetic friend. Just listen and talk. Do not suggest hospitals unless asked."

    # 2. Generate response
    prompt = f"{system_prompt}\nUser: {user_query}"
    response = ollama.generate(model='llama3', prompt=prompt)
    return response['response']
# Test it!


def classify_intent(query):
    query = query.lower()
    
    # Tier 1: Red Alert (Crisis)
    if any(re.search(word, query) for word in ['kill', 'suicid', 'hurt my', 'end it']):
        return "CRISIS"
    
    # Tier 2: Yellow Alert (Resource Seeking)
    resource_triggers = ['hospital', 'doctor', 'ngo', 'clinic', 'near me', 'helpline']
    if any(word in query for word in resource_triggers):
        return "RESOURCE"
    
    # Tier 3: Blue Alert (Emotional Venting)
    emotional_triggers = ['sad', 'lonely', 'depressed', 'anxious', 'scared', 'crying']
    if any(word in query for word in emotional_triggers):
        return "EMOTIONAL"

    return "CASUAL"

def get_mental_health_help(user_query):
    intent = classify_intent(user_query)
    
    if intent == "CRISIS":
        return "🚨 **I am very concerned about you.** Please reach out to Tele-Manas at **14416** immediately. You don't have to go through this alone."

    if intent == "RESOURCE":
        # PERFORM RAG SEARCH HERE
        # context = vector_db.similarity_search(user_query)
        return "I found some professionals who can help: [RAG DATA HERE]"

    if intent == "EMOTIONAL":
        prompt = f"You are an empathetic friend. The user is feeling down. Listen and comfort them: {user_query}"
    else:
        prompt = f"You are a friendly AI companion. Chat casually: {user_query}"

    response = ollama.generate(model='llama3', prompt=prompt)
    return response['response']

print(get_mental_health_help("I'm feeling anxious and I live in the capital of India."))