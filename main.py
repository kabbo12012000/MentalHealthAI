from engine import get_mental_health_help # Import your RAG logic
import time

def run_chatbot():
    print("--- Mental Health AI Friend (Ollama Edition) ---")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("AI Friend: Take care of yourself. Goodbye!")
            break
            
        print("AI Friend is thinking...")
        
        # Call the engine to get the RAG-based response
        response = get_mental_health_help(user_input)
        
        print(f"\nAI Friend: {response}\n")

if __name__ == "__main__":
    run_chatbot()