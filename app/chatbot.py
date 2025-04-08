from transformers import pipeline

# Load a model at startup (can replace with local model, RAG logic, etc.)
chatbot = pipeline("text-generation", model="gpt2")

def get_bot_response(user_input):
    result = chatbot(user_input, max_length=100, do_sample=True)
    return result[0]['generated_text']
