from transformers import pipeline
from nati.config_manager import ConfigManager
import os
import torch

# Load model name from config
config = ConfigManager()
model_name = config.get('ai.chat_model')
model_path = os.path.join('models', model_name)
print(model_path)

try:
    chatbot = pipeline("text-generation", model=model_path, device=0 if torch.cuda.is_available() else -1)
except Exception as e:
    print(f"Model load failed: {e}")
    chatbot = None

def get_bot_response(message):
    if chatbot is None:
        return "Model failed to load."
    prompt = f"""You are NATI, a helpful assistant for infrastructure, AI, and tooling.

User: {message}
NATI:"""
    result = chatbot(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)
    return result[0]['generated_text'].split("NATI:")[-1].strip()
